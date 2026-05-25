from __future__ import annotations

from contextlib import AbstractContextManager

from .buttons import Point
from .model_assets import ensure_hand_model


class HandTracker(AbstractContextManager["HandTracker"]):
    def __init__(
        self,
        max_num_hands: int = 1,
        min_detection_confidence: float = 0.8,
        min_tracking_confidence: float = 0.8,
        model_path: str | None = None,
    ) -> None:
        import mediapipe as mp

        self._mp = mp
        self._backend = "tasks"
        self._hands = None
        self._landmarker = None

        if hasattr(mp, "solutions") and hasattr(mp.solutions, "hands"):
            self._backend = "solutions"
            self._hands_solution = mp.solutions.hands
            self._drawing = mp.solutions.drawing_utils
            self._hands = self._hands_solution.Hands(
                max_num_hands=max_num_hands,
                min_detection_confidence=min_detection_confidence,
                min_tracking_confidence=min_tracking_confidence,
            )
            return

        vision = mp.tasks.vision
        resolved_model = ensure_hand_model(model_path)
        options = vision.HandLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=str(resolved_model.resolve())),
            running_mode=vision.RunningMode.IMAGE,
            num_hands=max_num_hands,
            min_hand_detection_confidence=min_detection_confidence,
            min_hand_presence_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )
        self._connections = vision.HandLandmarksConnections.HAND_CONNECTIONS
        self._landmarker = vision.HandLandmarker.create_from_options(options)

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    def close(self) -> None:
        if self._hands is not None:
            self._hands.close()
        if self._landmarker is not None:
            close = getattr(self._landmarker, "close", None)
            if close is not None:
                close()

    def detect(self, frame, cv2) -> tuple[list[Point] | None, object | None]:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        height, width = frame.shape[:2]

        if self._backend == "solutions":
            result = self._hands.process(rgb)
            if not result.multi_hand_landmarks:
                return None, None

            hand_landmarks = result.multi_hand_landmarks[0]
            points = [
                (int(landmark.x * width), int(landmark.y * height))
                for landmark in hand_landmarks.landmark
            ]
            return points, hand_landmarks

        image = self._mp.Image(image_format=self._mp.ImageFormat.SRGB, data=rgb)
        result = self._landmarker.detect(image)
        if not result.hand_landmarks:
            return None, None

        normalized_landmarks = result.hand_landmarks[0]
        points = [
            (int(landmark.x * width), int(landmark.y * height))
            for landmark in normalized_landmarks
        ]
        return points, points

    def draw(self, frame, landmarks) -> None:
        if self._backend == "solutions":
            self._drawing.draw_landmarks(frame, landmarks, self._hands_solution.HAND_CONNECTIONS)
            return

        import cv2

        for connection in self._connections:
            start = landmarks[connection.start]
            end = landmarks[connection.end]
            cv2.line(frame, start, end, (0, 200, 255), 2)

        for point in landmarks:
            cv2.circle(frame, point, 4, (0, 255, 120), cv2.FILLED)
