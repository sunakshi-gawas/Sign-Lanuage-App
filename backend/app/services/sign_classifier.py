from typing import List, Tuple
import os

import numpy as np
import requests


class SignClassifier:
    """
    Classifier that ONLY uses the external ML inference server.

    - If max probability >= CONF_THRESHOLD -> return that label
    - If max probability <  CONF_THRESHOLD -> return "UNKNOWN"

    No rule-based fallback.
    """

    def __init__(self):
        # URL of ML server endpoint
        self.ml_server_url = os.environ.get(
            "ML_SERVER_URL", "http://127.0.0.1:8001/api/predict"
        )
        # Confidence threshold for accepting a prediction
        # Set to 0.15 (15%) since we have 7 classes, random would be ~14%
        # This allows any confident prediction to pass
        self.CONF_THRESHOLD = float(os.environ.get("CONF_THRESHOLD", 0.15))

        print(f"[INFO] SignClassifier using ML server at: {self.ml_server_url}")
        print(f"[INFO] Confidence threshold: {self.CONF_THRESHOLD}")

    # ---------- helpers ----------

    def _normalize_landmarks(
        self, landmarks: List[Tuple[float, float, float]]
    ) -> List[Tuple[float, float, float]]:
        """
        Normalize landmarks to be position/scale invariant.
        - Center landmarks relative to wrist (landmark 0)
        - Scale by hand size
        This makes the model robust to different hand positions and sizes.
        """
        landmarks_array = np.array(landmarks)  # Shape: (21, 3)
        
        # Use wrist (landmark 0) as reference point
        wrist = landmarks_array[0]
        
        # Center all landmarks relative to wrist
        centered = landmarks_array - wrist
        
        # Calculate hand size (distance from wrist to middle finger tip)
        # Landmark 12 is middle finger tip
        hand_size = np.linalg.norm(centered[12])
        
        # Avoid division by zero
        if hand_size < 1e-6:
            hand_size = 1.0
        
        # Scale by hand size
        normalized = centered / hand_size
        
        return [tuple(point) for point in normalized]

    def _landmarks_to_vector(
        self, landmarks: List[Tuple[float, float, float]]
    ) -> np.ndarray:
        """
        Convert 21 landmarks (x, y, z) -> flat 63-dim vector.
        Applies normalization to make features position/scale invariant.
        """
        if not landmarks or len(landmarks) != 21:
            raise RuntimeError(
                f"Expected 21 landmarks, got {0 if not landmarks else len(landmarks)}"
            )

        # Normalize landmarks first
        normalized_landmarks = self._normalize_landmarks(landmarks)
        
        coords = []
        for (x, y, z) in normalized_landmarks:
            coords.extend([x, y, z])
        return np.array(coords, dtype=np.float32)

    def _call_ml_server(self, features: List[float]) -> Tuple[str, float]:
        """
        Send features to ML server and return (predicted_label, confidence_score).
        Returns ("UNKNOWN", confidence) if confidence is below threshold.

        Raises RuntimeError on communication / format errors.
        """
        try:
            payload = {"features": features}
            print(f"[DEBUG] Calling ML server {self.ml_server_url}")
            resp = requests.post(self.ml_server_url, json=payload, timeout=3.0)
            print(f"[DEBUG] ML server status: {resp.status_code}")

            if resp.status_code != 200:
                raise RuntimeError(
                    f"ML server error {resp.status_code}: {resp.text}"
                )

            data = resp.json()
            print("[DEBUG] ML server response:", data)

            if "label" not in data or "probs" not in data:
                raise RuntimeError("ML response missing 'label' or 'probs'")

            label = data["label"]
            probs = data["probs"]

            if not isinstance(probs, list) or len(probs) == 0:
                raise RuntimeError("ML response 'probs' is invalid")

            max_prob = max(probs)
            print(f"[DEBUG] max_prob={max_prob:.3f}, raw_label={label}")

            if max_prob < self.CONF_THRESHOLD:
                print(
                    f"[INFO] Prediction below threshold ({max_prob:.3f} < {self.CONF_THRESHOLD}), using UNKNOWN"
                )
                return ("UNKNOWN", max_prob)

            print("[INFO] ML label accepted:", label, f"(conf={max_prob:.3f})")
            return (label, max_prob)

        except Exception as e:
            # Wrap any error in a RuntimeError so FastAPI can decide what to show
            raise RuntimeError(f"Failed to get prediction from ML server: {e}") from e

    # ---------- public API ----------

    def predict(self, features: List[float]) -> Tuple[str, float]:
        """
        For /api/sign-to-text when client passes raw feature vector.
        Returns (label, confidence_score)
        """
        if not features:
            raise RuntimeError("Empty feature vector")

        return self._call_ml_server(features)

    def predict_from_landmarks(
        self, landmarks: List[Tuple[float, float, float]]
    ) -> Tuple[str, float]:
        """
        For /api/sign-to-text-image when we have MediaPipe landmarks.
        Returns (label, confidence_score)
        """
        vec = self._landmarks_to_vector(landmarks)
        return self._call_ml_server(vec.tolist())
