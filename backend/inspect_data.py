import os
import numpy as np

DATA_DIR = "data"

def main():
    if not os.path.exists(DATA_DIR):
        print(f"DATA_DIR not found: {DATA_DIR}")
        return

    labels = [d for d in os.listdir(DATA_DIR)
              if os.path.isdir(os.path.join(DATA_DIR, d))]

    print("Found label folders:", labels)

    for label in labels:
        label_dir = os.path.join(DATA_DIR, label)
        files = [f for f in os.listdir(label_dir) if f.endswith(".npy")]
        print(f"{label}: {len(files)} sequences")

        if files:
            path = os.path.join(label_dir, files[0])
            arr = np.load(path)
            print(f"  Example shape: {arr.shape}")

if __name__ == "__main__":
    main()
