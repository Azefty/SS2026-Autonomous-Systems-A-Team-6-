#!/usr/bin/env python3
"""
HSHL Line Following Student Lab — Team 6
=====================================================

Detect a green line and steer to stay centered on it.
"""

import cv2          # type: ignore
import numpy as np  # type: ignore
import rclpy        # type: ignore

from .interface import LineFollowingInterface


class MyLineFollower(LineFollowingInterface):
  

    def __init__(self):
        super().__init__("my_line_follower")

        self._frame_count = 0
        self._last_steering = 0.0

        # Register camera callback
        self.on_camera_image(self.detect_line)

        self.get_logger().info(
            "MyLineFollower initialized — ready to detect green line"
        )

    def detect_line(self, image: np.ndarray) -> float | None:
        """
        Detect the green line and return steering command.

        Args:
            image: BGR image from camera, shape (720, 1280, 3)

        Returns:
            Steering value in [-1.0, 1.0], or None if line not detected.
        """

        self._frame_count += 1

        height, width = image.shape[:2]

        # Use lower part of image
        roi_start = int(height * 0.55)
        roi = image[roi_start:, :]

        # Convert image to HSV
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # Green color range
        lower_green = np.array([40, 60, 60])
        upper_green = np.array([90, 255, 255])

        # Create mask
        mask = cv2.inRange(hsv, lower_green, upper_green)

        # Reduce noise
        kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE,
            (5, 5)
        )

        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # Find contours
        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if not contours:
            return self._last_steering

        # Largest contour is assumed to be the line
        largest_contour = max(contours, key=cv2.contourArea)

        area = cv2.contourArea(largest_contour)

        # Ignore very small areas
        if area < 200:
            return self._last_steering

        # Calculate contour center
        M = cv2.moments(largest_contour)

        if M["m00"] == 0:
            return self._last_steering

        line_center_x = M["m10"] / M["m00"]

        # Calculate steering
        image_center_x = width / 2.0

        offset = (
            line_center_x - image_center_x
        ) / image_center_x

        steering = offset * 0.8

        steering = float(
            np.clip(steering, -1.0, 1.0)
        )

        # Smooth steering
        steering = (
            0.7 * self._last_steering +
            0.3 * steering
        )

        self._last_steering = steering

        # Debug output
        if self._frame_count % 30 == 0:
            self.get_logger().info(
                f"offset={offset:.3f} "
                f"steer={steering:.3f} "
                f"area={area:.1f}"
            )

        return steering


def main(args=None):
    """Main entry point for the line follower node."""

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