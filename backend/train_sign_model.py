import os
import json
from typing import Dict, Tuple, List
from pathlib import Path

import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Dropout, BatchNormalization
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.regularizers import l2

# ================== CONFIG ==================

# Directory with .npy data (still under backend/)
DATA_DIR = "data"

# Compute project root: one level above backend/
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Point to the REAL ml_server/model directory at top level
MODEL_DIR = PROJECT_ROOT / "ml_server" / "model"

MODEL_OUTPUT_PATH = MODEL_DIR / "sign_model.h5"
LABEL_MAP_PATH = MODEL_DIR / "label_map.json"
SCALER_PATH = MODEL_DIR / "scaler.pkl"

TEST_SIZE = 0.15
VAL_SIZE = 0.15
RANDOM_STATE = 42
EPOCHS = 100
BATCH_SIZE = 16
LEARNING_RATE = 0.001

# ===========================================


def discover_labels() -> List[str]:
    """
    Discover labels from folder names under DATA_DIR.
    Each subfolder is treated as a separate class.
    """
    if not os.path.exists(DATA_DIR):
        raise RuntimeError(f"DATA_DIR not found: {DATA_DIR}")

    labels = [
        d
        for d in os.listdir(DATA_DIR)
        if os.path.isdir(os.path.join(DATA_DIR, d))
    ]
    labels.sort()
    print("[INFO] Discovered labels (folders):", labels)
    return labels


def normalize_landmarks(landmarks_flat: np.ndarray) -> np.ndarray:
    """
    Normalize a flat 63-dim landmark vector (21 landmarks x 3 coords).
    - Center relative to wrist (landmark 0)
    - Scale by hand size (distance from wrist to middle finger tip)
    This makes features position/scale invariant.
    """
    # Reshape to (21, 3)
    landmarks = landmarks_flat.reshape(21, 3)
    
    # Use wrist (landmark 0) as reference
    wrist = landmarks[0]
    
    # Center relative to wrist
    centered = landmarks - wrist
    
    # Calculate hand size (distance to middle finger tip, landmark 12)
    hand_size = np.linalg.norm(centered[12])
    
    # Avoid division by zero
    if hand_size < 1e-6:
        hand_size = 1.0
    
    # Scale by hand size
    normalized = centered / hand_size
    
    # Flatten back to 63-dim
    return normalized.flatten().astype(np.float32)


def load_data() -> Tuple[np.ndarray, np.ndarray, Dict[int, str], object]:
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
            sequence = np.load(path)  # (seq_len, 63)

            # Add each frame of the sequence as a separate sample
            for frame in sequence:
                # Apply landmark normalization
                normalized_frame = normalize_landmarks(frame)
                X.append(normalized_frame)
                y.append(label)

    if not X:
        raise RuntimeError("No samples found. Did you collect any data?")

    X = np.array(X, dtype=np.float32)
    y = np.array(y)

    print(f"[INFO] Total samples: {X.shape[0]}")
    print(f"[INFO] Feature dimension: {X.shape[1]}")

    # Normalize features
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    X = X.astype(np.float32)

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    index_to_label = {int(i): label for i, label in enumerate(label_encoder.classes_)}
    print("[INFO] Final label mapping:", index_to_label)

    return X, y_encoded, index_to_label, scaler


def build_model(input_dim: int, num_classes: int) -> Sequential:
    """
    Build improved model with dropout, batch normalization, and L2 regularization.
    """
    model = Sequential([
        Input(shape=(input_dim,)),
        Dense(256, activation="relu", kernel_regularizer=l2(0.001)),
        BatchNormalization(),
        Dropout(0.3),
        
        Dense(128, activation="relu", kernel_regularizer=l2(0.001)),
        BatchNormalization(),
        Dropout(0.3),
        
        Dense(64, activation="relu", kernel_regularizer=l2(0.001)),
        BatchNormalization(),
        Dropout(0.2),
        
        Dense(32, activation="relu", kernel_regularizer=l2(0.001)),
        Dropout(0.2),
        
        Dense(num_classes, activation="softmax"),
    ])

    optimizer = Adam(learning_rate=LEARNING_RATE)
    model.compile(
        loss="categorical_crossentropy",
        optimizer=optimizer,
        metrics=["accuracy"],
    )

    model.summary()
    return model


def main():
    X, y_encoded, index_to_label, scaler = load_data()

    num_classes = len(np.unique(y_encoded))
    input_dim = X.shape[1]

    y_cat = to_categorical(y_encoded, num_classes=num_classes)

    # Split data: 70% train, 15% val, 15% test
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y_cat, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y_cat
    )
    
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=VAL_SIZE/(1-TEST_SIZE), random_state=RANDOM_STATE, stratify=y_temp
    )

    print(f"[INFO] Train samples: {X_train.shape[0]}")
    print(f"[INFO] Val samples: {X_val.shape[0]}")
    print(f"[INFO] Test samples: {X_test.shape[0]}")

    model = build_model(input_dim, num_classes)

    # Callbacks for better training
    early_stop = EarlyStopping(
        monitor="val_accuracy",
        patience=15,
        restore_best_weights=True,
        verbose=1
    )
    
    reduce_lr = ReduceLROnPlateau(
        monitor="val_accuracy",
        factor=0.5,
        patience=5,
        min_lr=0.00001,
        verbose=1
    )

    history = model.fit(
        X_train,
        y_train,
        validation_data=(X_val, y_val),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=[early_stop, reduce_lr],
        verbose=1,
    )

    # Evaluate on test set
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"\n[INFO] Test Accuracy: {test_accuracy*100:.2f}%")
    print(f"[INFO] Test Loss: {test_loss:.4f}")

    # Make sure ml_server/model exists at the project root
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    model.save(MODEL_OUTPUT_PATH)
    print(f"[INFO] Saved Keras model to {MODEL_OUTPUT_PATH}")

    with open(LABEL_MAP_PATH, "w") as f:
        json.dump(index_to_label, f)
    print(f"[INFO] Saved label map to {LABEL_MAP_PATH}")

    # Save the scaler for use during inference
    with open(SCALER_PATH, "wb") as f:
        pickle.dump(scaler, f)
    print(f"[INFO] Saved scaler to {SCALER_PATH}")


if __name__ == "__main__":
    main()
