#!/usr/bin/env python3
"""
HSHL Line Following Student Lab — Team 6
=====================================================

Line following using an SVM model.
"""

import cv2          # type: ignore
import numpy as np  # type: ignore
import rclpy        # type: ignore
import joblib

from .interface import LineFollowingInterface


class MyLineFollower(LineFollowingInterface):

    def __init__(self):
        super().__init__("my_line_follower")

        self._frame_count = 0
        self._last_steering = 0.0

        # Load trained SVM model
        self.svm_model = joblib.load(
            "svm_model.pkl"
        )

        # Register camera callback
        self.on_camera_image(
            self.detect_line
        )

        self.get_logger().info(
            "SVM Line Follower initialized"
        )

    def preprocess_image(
        self,
        image: np.ndarray
    ) -> np.ndarray:
        """
        Preprocess image exactly like training notebook.
        """

        h, w = image.shape[:2]

        # Crop lower region
        roi = image[int(h * 0.6):h, :]

        # Convert to grayscale
        gray = cv2.cvtColor(
            roi,
            cv2.COLOR_BGR2GRAY
        )

        # Resize to 64x32
        resized = cv2.resize(
            gray,
            (64, 32)
        )

        # Flatten to 2048 features
        features = resized.flatten()

        return features

    def detect_line(
        self,
        image: np.ndarray
    ) -> float | None:

        self._frame_count += 1

        # Preprocess image
        features = self.preprocess_image(
            image
        )

        # Predict class
        prediction = self.svm_model.predict(
            [features]
        )[0]

        # Convert class to steering
        if prediction == -1:
            steering = -0.6

        elif prediction == 0:
            steering = 0.0

        elif prediction == 1:
            steering = 0.6

        else:
            steering = 0.0

        # Smooth steering
        steering = (
            0.7 * self._last_steering +
            0.3 * steering
        )

        self._last_steering = steering

        # Debug info
        if self._frame_count % 30 == 0:
            self.get_logger().info(
                f"Prediction={prediction} "
                f"Steering={steering:.3f}"
            )

        return steering


def main(args=None):

    rclpy.init(args=args)

    follower = MyLineFollower()

    try:
        rclpy.spin(follower)

    except KeyboardInterrupt:
        pass

    finally:
        follower.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()