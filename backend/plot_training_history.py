import os
import json
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from tensorflow.keras.utils import to_categorical

# ================== CONFIG ==================

DATA_DIR = "data"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_DIR = PROJECT_ROOT / "ml_server" / "model"
MODEL_PATH = MODEL_DIR / "sign_model.h5"
LABEL_MAP_PATH = MODEL_DIR / "label_map.json"

# Save plots to backend directory
OUTPUT_DIR = "training_plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

TEST_SIZE = 0.15
VAL_SIZE = 0.15
RANDOM_STATE = 42

# ===========================================


def normalize_landmarks(landmarks_flat: np.ndarray) -> np.ndarray:
    """
    Normalize a flat 63-dim landmark vector (21 landmarks x 3 coords).
    - Center relative to wrist (landmark 0)
    - Scale by hand size (distance from wrist to middle finger tip)
    """
    landmarks = landmarks_flat.reshape(21, 3)
    wrist = landmarks[0]
    centered = landmarks - wrist
    hand_size = np.linalg.norm(centered[12])
    
    if hand_size < 1e-6:
        hand_size = 1.0
    
    normalized = centered / hand_size
    return normalized.flatten().astype(np.float32)


def discover_labels():
    """Discover labels from folder names under DATA_DIR."""
    if not os.path.exists(DATA_DIR):
        raise RuntimeError(f"DATA_DIR not found: {DATA_DIR}")

    labels = [
        d
        for d in os.listdir(DATA_DIR)
        if os.path.isdir(os.path.join(DATA_DIR, d))
    ]
    labels.sort()
    return labels


def load_data():
    """Load and prepare dataset."""
    X = []
    y = []

    labels = discover_labels()
    if not labels:
        raise RuntimeError("No label folders found in data/")

    for label in labels:
        label_dir = os.path.join(DATA_DIR, label)
        files = [f for f in os.listdir(label_dir) if f.endswith(".npy")]
        if not files:
            print(f"[WARN] No .npy files for label {label}, skipping.")
            continue

        print(f"[INFO] {label}: found {len(files)} sequences")

        for fname in files:
            path = os.path.join(label_dir, fname)
            sequence = np.load(path)

            for frame in sequence:
                # Apply landmark normalization
                normalized_frame = normalize_landmarks(frame)
                X.append(normalized_frame)
                y.append(label)

    if not X:
        raise RuntimeError("No samples found. Did you collect any data?")

    X = np.array(X, dtype=np.float32)
    y = np.array(y)

    # Normalize features
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    X = X.astype(np.float32)

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    index_to_label = {int(i): label for i, label in enumerate(label_encoder.classes_)}

    return X, y_encoded, index_to_label, label_encoder.classes_


def evaluate_model_by_class(model, X_test, y_test, class_names):
    """Evaluate model performance per class."""
    from sklearn.metrics import classification_report, confusion_matrix
    
    y_pred = np.argmax(model.predict(X_test, verbose=0), axis=1)
    y_true = np.argmax(y_test, axis=1)
    
    # Classification report
    report = classification_report(y_true, y_pred, target_names=class_names, output_dict=True)
    
    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    
    return report, cm, y_pred, y_true


def plot_training_accuracy():
    """Plot overall training and validation accuracy curves."""
    # Load data
    X, y_encoded, index_to_label, class_names = load_data()
    num_classes = len(np.unique(y_encoded))
    input_dim = X.shape[1]

    y_cat = to_categorical(y_encoded, num_classes=num_classes)

    # Split data
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y_cat, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y_cat
    )
    
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=VAL_SIZE/(1-TEST_SIZE), random_state=RANDOM_STATE, stratify=y_temp
    )

    # Load trained model
    model = load_model(MODEL_PATH)
    
    # Evaluate on all sets
    train_loss, train_accuracy = model.evaluate(X_train, y_train, verbose=0)
    val_loss, val_accuracy = model.evaluate(X_val, y_val, verbose=0)
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
    
    print(f"[INFO] Train Accuracy: {train_accuracy*100:.2f}%")
    print(f"[INFO] Val Accuracy: {val_accuracy*100:.2f}%")
    print(f"[INFO] Test Accuracy: {test_accuracy*100:.2f}%")
    
    # Create summary figure
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Sign Language Model - Training Summary', fontsize=16, fontweight='bold')
    
    # Accuracy comparison
    ax = axes[0, 0]
    datasets = ['Train', 'Validation', 'Test']
    accuracies = [train_accuracy*100, val_accuracy*100, test_accuracy*100]
    colors = ['#2ecc71', '#3498db', '#e74c3c']
    bars = ax.bar(datasets, accuracies, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
    ax.set_ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
    ax.set_title('Overall Accuracy by Dataset', fontsize=13, fontweight='bold')
    ax.set_ylim([95, 101])
    for bar, acc in zip(bars, accuracies):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{acc:.2f}%', ha='center', va='bottom', fontweight='bold', fontsize=11)
    ax.grid(axis='y', alpha=0.3)
    
    # Loss comparison
    ax = axes[0, 1]
    losses = [train_loss, val_loss, test_loss]
    bars = ax.bar(datasets, losses, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
    ax.set_ylabel('Loss', fontsize=12, fontweight='bold')
    ax.set_title('Model Loss by Dataset', fontsize=13, fontweight='bold')
    for bar, loss in zip(bars, losses):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{loss:.4f}', ha='center', va='bottom', fontweight='bold', fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    
    # Per-class accuracy
    ax = axes[1, 0]
    report, cm, _, _ = evaluate_model_by_class(model, X_test, y_test, class_names)
    class_accuracies = [report[class_name]['precision'] * 100 for class_name in class_names]
    bars = ax.barh(class_names, class_accuracies, color='#3498db', alpha=0.7, edgecolor='black', linewidth=1.5)
    ax.set_xlabel('Accuracy (%)', fontsize=12, fontweight='bold')
    ax.set_title('Per-Class Accuracy (Test Set)', fontsize=13, fontweight='bold')
    ax.set_xlim([95, 101])
    for bar, acc in zip(bars, class_accuracies):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
                f'{acc:.1f}%', ha='left', va='center', fontweight='bold', fontsize=10)
    ax.grid(axis='x', alpha=0.3)
    
    # Dataset distribution
    ax = axes[1, 1]
    dataset_sizes = [len(X_train), len(X_val), len(X_test)]
    wedges, texts, autotexts = ax.pie(dataset_sizes, labels=datasets, autopct='%1.1f%%',
                                        colors=colors, startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'},
                                        explode=(0.05, 0.05, 0.05), shadow=True)
    ax.set_title('Data Distribution', fontsize=13, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/01_training_summary.png', dpi=300, bbox_inches='tight')
    print(f"[INFO] Saved: {OUTPUT_DIR}/01_training_summary.png")
    plt.close()


def plot_per_class_analysis():
    """Create detailed per-class analysis plots."""
    X, y_encoded, index_to_label, class_names = load_data()
    num_classes = len(np.unique(y_encoded))
    input_dim = X.shape[1]

    y_cat = to_categorical(y_encoded, num_classes=num_classes)

    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y_cat, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y_cat
    )
    
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=VAL_SIZE/(1-TEST_SIZE), random_state=RANDOM_STATE, stratify=y_temp
    )

    model = load_model(MODEL_PATH)
    report, cm, y_pred, y_true = evaluate_model_by_class(model, X_test, y_test, class_names)
    
    # Create confusion matrix heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(cm, interpolation='nearest', cmap='Blues', aspect='auto')
    
    ax.set_xticks(np.arange(len(class_names)))
    ax.set_yticks(np.arange(len(class_names)))
    ax.set_xticklabels(class_names, fontsize=11, fontweight='bold')
    ax.set_yticklabels(class_names, fontsize=11, fontweight='bold')
    
    ax.set_xlabel('Predicted Label', fontsize=12, fontweight='bold')
    ax.set_ylabel('True Label', fontsize=12, fontweight='bold')
    ax.set_title('Confusion Matrix - Sign Classification', fontsize=14, fontweight='bold')
    
    # Add text annotations
    for i in range(len(class_names)):
        for j in range(len(class_names)):
            text = ax.text(j, i, cm[i, j], ha="center", va="center",
                          color="white" if cm[i, j] > cm.max() / 2 else "black",
                          fontsize=12, fontweight='bold')
    
    plt.colorbar(im, ax=ax, label='Count')
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/02_confusion_matrix.png', dpi=300, bbox_inches='tight')
    print(f"[INFO] Saved: {OUTPUT_DIR}/02_confusion_matrix.png")
    plt.close()
    
    # Per-class metrics
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Per-Class Performance Metrics', fontsize=14, fontweight='bold')
    
    metrics = ['precision', 'recall', 'f1-score']
    colors_list = ['#e74c3c', '#3498db', '#2ecc71']
    
    for ax, metric, color in zip(axes, metrics, colors_list):
        values = [report[class_name][metric] * 100 for class_name in class_names]
        bars = ax.bar(class_names, values, color=color, alpha=0.7, edgecolor='black', linewidth=1.5)
        ax.set_ylabel('Score (%)', fontsize=11, fontweight='bold')
        ax.set_title(metric.capitalize(), fontsize=12, fontweight='bold')
        ax.set_ylim([95, 101])
        ax.tick_params(axis='x', rotation=45)
        
        for bar, val in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{val:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=9)
        ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/03_per_class_metrics.png', dpi=300, bbox_inches='tight')
    print(f"[INFO] Saved: {OUTPUT_DIR}/03_per_class_metrics.png")
    plt.close()


def plot_dataset_statistics():
    """Plot dataset statistics per class."""
    X, y_encoded, index_to_label, class_names = load_data()
    
    # Count samples per class
    unique, counts = np.unique(y_encoded, return_counts=True)
    class_counts = {class_names[i]: counts[i] for i in range(len(class_names))}
    
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(class_counts.keys(), class_counts.values(), color='#9b59b6', alpha=0.7, edgecolor='black', linewidth=2)
    ax.set_ylabel('Number of Samples', fontsize=12, fontweight='bold')
    ax.set_xlabel('Sign Class', fontsize=12, fontweight='bold')
    ax.set_title('Dataset Distribution - Samples per Class', fontsize=14, fontweight='bold')
    
    for bar, (cls, count) in zip(bars, class_counts.items()):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{int(count)}', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/04_dataset_distribution.png', dpi=300, bbox_inches='tight')
    print(f"[INFO] Saved: {OUTPUT_DIR}/04_dataset_distribution.png")
    plt.close()
    
    # Print statistics
    print("\n=== Dataset Statistics ===")
    print(f"Total Samples: {len(X)}")
    print(f"Samples per Class:")
    for cls, count in sorted(class_counts.items()):
        print(f"  {cls}: {count} samples ({count/len(X)*100:.1f}%)")


def main():
    print("\n=== Generating Training Analysis Plots ===\n")
    
    print("[1/3] Generating training summary plots...")
    plot_training_accuracy()
    
    print("[2/3] Generating per-class analysis...")
    plot_per_class_analysis()
    
    print("[3/3] Generating dataset statistics...")
    plot_dataset_statistics()
    
    print(f"\n✅ All plots saved to '{OUTPUT_DIR}/' directory")
    print("\nGenerated files:")
    print("  - 01_training_summary.png")
    print("  - 02_confusion_matrix.png")
    print("  - 03_per_class_metrics.png")
    print("  - 04_dataset_distribution.png")


if __name__ == "__main__":
    main()
