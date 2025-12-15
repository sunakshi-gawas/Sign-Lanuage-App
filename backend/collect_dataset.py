import os
import time
import argparse

import cv2
import mediapipe as mp
import numpy as np

# ========= Mediapipe setup =========
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

DATA_DIR = "data"  # base directory for dataset


def parse_args():
    parser = argparse.ArgumentParser(
        description="Collect hand landmarks dataset for one or more labels."
    )
    parser.add_argument(
        "--label",
        type=str,
        help="Single label to collect (e.g., HELLO). If omitted, collects for all existing label folders.",
    )
    parser.add_argument(
        "--sequences",
        type=int,
        default=30,
        help="Number of sequences to record for each label (default: 30).",
    )
    parser.add_argument(
        "--frames",
        type=int,
        default=30,
        help="Number of frames per sequence (default: 30).",
    )
    return parser.parse_args()


def get_labels_from_folders() -> list[str]:
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
        return []
    labels = [
        d
        for d in os.listdir(DATA_DIR)
        if os.path.isdir(os.path.join(DATA_DIR, d))
    ]
    labels.sort()
    return labels


def collect_for_label(label: str, num_sequences: int, frames_per_seq: int):
    """
    Simple collection - Press SPACE ONCE at the start, then auto-records all sequences!
    1. Press SPACE once to start
    2. Hold each sign for 30 frames (auto-captures)
    3. Auto-pauses between sequences (2 seconds to change hand position)
    4. Repeats automatically until done
    5. Press 'q' anytime to quit
    """
    label_dir = os.path.join(DATA_DIR, label)
    os.makedirs(label_dir, exist_ok=True)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Cannot open webcam")
        return

    print(f"\n{'='*70}")
    print(f"📹 COLLECTING DATA FOR: {label.upper()}")
    print(f"{'='*70}")
    print(f"Total sequences to record: {num_sequences}")
    print(f"Frames per sequence: {frames_per_seq}")
    print(f"\n{'INSTRUCTIONS':^70}")
    print(f"{'─'*70}")
    print(f"1. Press SPACE ONCE to start collecting all {num_sequences} sequences")
    print(f"2. Hold the sign for each sequence (auto-records 30 frames)")
    print(f"3. 2-second break between sequences - change hand position")
    print(f"4. Everything repeats automatically!")
    print(f"5. Press 'q' anytime to stop and quit")
    print(f"{'─'*70}\n")

    time.sleep(2)  # Give user time to read instructions

    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as hands:
        # ========== WAIT FOR USER TO PRESS SPACE ONCE ==========
        print(f"⏳ Waiting for you to press SPACE to start...")
        
        waiting = True
        while waiting:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            h, w, c = frame.shape

            # Display waiting screen
            cv2.rectangle(frame, (0, 0), (w, h), (50, 50, 50), -1)
            cv2.putText(
                frame,
                f"PREPARING TO COLLECT {label.upper()}",
                (30, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0, 255, 0),
                3,
            )
            cv2.putText(
                frame,
                f"Sequences: {num_sequences} x {frames_per_seq} frames",
                (80, 180),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (255, 255, 255),
                2,
            )
            cv2.putText(
                frame,
                "PRESS SPACE ONCE TO START",
                (w // 2 - 250, h // 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (0, 165, 255),
                3,
            )
            cv2.putText(
                frame,
                "(After this, just hold the sign - everything is automatic!)",
                (80, h // 2 + 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 200, 0),
                2,
            )
            cv2.putText(
                frame,
                "Press 'q' to QUIT",
                (w // 2 - 150, h - 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2,
            )

            cv2.imshow("Dataset Collection", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord(" "):  # SPACE pressed
                waiting = False
                print(f"✓ Starting automatic collection...\n")
                time.sleep(1)
            elif key == ord("q"):  # Q pressed
                print(f"\n✗ Quit before starting!")
                cap.release()
                cv2.destroyAllWindows()
                return

        # ========== AUTO-COLLECT ALL SEQUENCES ==========
        for seq_idx in range(num_sequences):
            print(f"\n{'─'*70}")
            print(f"📸 Sequence {seq_idx + 1}/{num_sequences}")
            print(f"{'─'*70}")
            
            # Brief pause between sequences
            if seq_idx > 0:
                print(f"Pause (change hand position)...")
                for pause_frame in range(60):  # 2 second pause at 30fps
                    ret, frame = cap.read()
                    if not ret:
                        break

                    frame = cv2.flip(frame, 1)
                    h, w, c = frame.shape

                    # Pause screen
                    cv2.rectangle(frame, (0, 0), (w, h), (50, 50, 50), -1)
                    cv2.putText(
                        frame,
                        f"PREPARING SEQUENCE {seq_idx + 1}",
                        (w // 2 - 280, 100),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.2,
                        (0, 200, 255),
                        3,
                    )
                    cv2.putText(
                        frame,
                        "Get ready with the sign...",
                        (w // 2 - 220, 200),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0,
                        (255, 255, 255),
                        2,
                    )
                    
                    remaining = 2 - (pause_frame // 30)
                    cv2.putText(
                        frame,
                        f"Starting in: {remaining} seconds",
                        (w // 2 - 200, h // 2),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.5,
                        (0, 165, 255),
                        3,
                    )

                    cv2.imshow("Dataset Collection", frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord("q"):
                        print(f"\n✗ Quit! Collected {seq_idx}/{num_sequences} sequences")
                        cap.release()
                        cv2.destroyAllWindows()
                        return

            # ========== RECORD 30 FRAMES FOR THIS SEQUENCE ==========
            print(f"🔴 Recording {frames_per_seq} frames...")
            sequence_data = []
            frame_count = 0

            while frame_count < frames_per_seq:
                ret, frame = cap.read()
                if not ret:
                    print("[ERROR] Failed to read frame during recording.")
                    break

                frame = cv2.flip(frame, 1)
                h, w, c = frame.shape

                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                results = hands.process(image)
                image.flags.writeable = True

                # Draw landmarks if hand is detected
                hand_detected = False
                if results.multi_hand_landmarks:
                    hand_detected = True
                    hand_landmarks = results.multi_hand_landmarks[0]
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                    )

                    # Capture the landmarks
                    landmarks_vec = []
                    for lm in hand_landmarks.landmark:
                        landmarks_vec.extend([lm.x, lm.y, lm.z])
                    sequence_data.append(landmarks_vec)
                    frame_count += 1

                # ===== UI =====
                # Top bar - Recording status
                cv2.rectangle(frame, (0, 0), (w, 80), (20, 20, 20), -1)
                cv2.putText(
                    frame,
                    f"{label.upper()} - Seq {seq_idx + 1}/{num_sequences}",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    (0, 0, 255),
                    2,
                )

                # Frame counter in center
                progress_percent = int((frame_count / frames_per_seq) * 100)
                cv2.putText(
                    frame,
                    f"RECORDING: {frame_count}/{frames_per_seq} frames ({progress_percent}%)",
                    (w // 2 - 250, h // 2),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2,
                    (0, 255, 0),
                    3,
                )

                # Progress bar
                bar_width = int((frame_count / frames_per_seq) * (w - 40))
                cv2.rectangle(frame, (20, h - 60), (w - 20, h - 30), (100, 100, 100), 2)
                cv2.rectangle(frame, (20, h - 60), (20 + bar_width, h - 30), (0, 255, 0), -1)

                # Hand status
                hand_text = "✓ Hand Detected" if hand_detected else "✗ No Hand"
                hand_color = (0, 255, 0) if hand_detected else (0, 0, 255)
                cv2.putText(
                    frame,
                    hand_text,
                    (20, h - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    hand_color,
                    2,
                )

                cv2.imshow("Dataset Collection", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    print(f"\n✗ Quit! Collected {seq_idx}/{num_sequences} sequences")
                    cap.release()
                    cv2.destroyAllWindows()
                    return

            # ========== SAVE SEQUENCE ==========
            if len(sequence_data) == frames_per_seq:
                out_path = os.path.join(label_dir, f"{label}_{seq_idx}.npy")
                np.save(out_path, np.array(sequence_data, dtype=np.float32))
                print(f"✓ Saved sequence {seq_idx + 1}")
            else:
                print(f"✗ Error! Only got {len(sequence_data)}/{frames_per_seq} frames for sequence {seq_idx + 1}")

        cap.release()
        cv2.destroyAllWindows()
        print(f"\n{'='*70}")
        print(f"✓ COMPLETED! All {num_sequences} sequences collected for {label}")
        print(f"{'='*70}\n")


def main():
    args = parse_args()

    print("\n" + "=" * 60)
    print("HAND LANDMARK DATASET COLLECTOR")
    print("=" * 60)
    print(f"Base directory: {DATA_DIR}")

    if args.label:
        labels = [args.label]
        print(f"Collecting for: {args.label}")
    else:
        labels = get_labels_from_folders()
        if labels:
            print(f"Found existing labels: {', '.join(labels)}")
        else:
            print("[WARN] No labels found. Use --label NEW_LABEL to start.")
            return

    if not labels:
        print("[WARN] No labels specified. Exiting.")
        return

    print(f"\nSequences per label: {args.sequences}")
    print(f"Frames per sequence: {args.frames}")
    print("\n" + "=" * 60)

    for label in labels:
        collect_for_label(label, args.sequences, args.frames)

    print("\n" + "=" * 60)
    print("Collection Complete!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
