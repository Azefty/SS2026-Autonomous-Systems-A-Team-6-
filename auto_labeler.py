import os
import cv2
import csv
import glob

# Import the instructor's advanced line detection function
from docs.line_detection_example import detect_green_line_advanced

def main():
    # 1. Define your input and output paths
    image_dir = 'extracted_images'
    output_csv = 'training_labels.csv'

    # Check if the extracted_images folder exists
    if not os.path.exists(image_dir):
        print(f"Error: Could not find the folder '{image_dir}'.")
        return

    # Look for both .png and .jpg files
    image_paths = glob.glob(os.path.join(image_dir, '*.png'))
    image_paths.extend(glob.glob(os.path.join(image_dir, '*.jpg')))

    if not image_paths:
        print(f"Error: No images found in '{image_dir}'.")
        return

    print(f"Found {len(image_paths)} images. Starting auto-labeling...")

    valid_count = 0
    skipped_count = 0

    # 2. Open a new CSV file to save our labels
    with open(output_csv, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['filename', 'label']) # Write the header row

        # 3. Loop through every image
        for img_path in image_paths:
            filename = os.path.basename(img_path)
            image = cv2.imread(img_path)

            if image is None:
                continue

            # 4. Get the steering value from the instructor's example
            steering = detect_green_line_advanced(image, show_debug=False)

            # If the algorithm couldn't find the line, skip this image
            # We only want clean, confident data for our SVM
            if steering is None:
                skipped_count += 1
                continue

            # 5. Bin the continuous steering value into discrete classes
            if steering < -0.2:
                label = -1  # LEFT
            elif steering > 0.2:
                label = 1   # RIGHT
            else:
                label = 0   # STRAIGHT

            # Write the result to the CSV
            writer.writerow([filename, label])
            valid_count += 1

            # Print progress every 100 images
            if (valid_count + skipped_count) % 100 == 0:
                print(f"Processed {valid_count + skipped_count} / {len(image_paths)} images...")

    print("\n--- Auto-Labeling Complete ---")
    print(f"Successfully labeled: {valid_count} images")
    print(f"Skipped (no line found): {skipped_count} images")
    print(f"Labels saved to: {output_csv}")

if __name__ == '__main__':
    main()