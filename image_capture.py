import os
import cv2
import time

# Create the main data directory
DATA_DIR = './data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

number_of_classes = 3     # You can change this to however many classes you need
dataset_size = 1000       # Images per class

# Start the webcam
cap = cv2.VideoCapture(0)

# Loop through each class
for j in range(number_of_classes):
    class_dir = os.path.join(DATA_DIR, str(j))
    if not os.path.exists(class_dir):
        os.makedirs(class_dir)

    print(f'\n📸 Collecting data for class {j}')

    # Wait until user is ready
    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Failed to grab frame. Exiting...")
            break
        cv2.putText(frame, 'Ready? Press "Q" to start :)', (100, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1.2, (0, 255, 0), 3, cv2.LINE_AA)
        cv2.imshow('frame', frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            print("⏳ Starting capture in 3 seconds...")
            time.sleep(3)
            break
        elif key == 27:  # Esc key
            print("🛑 ESC pressed. Exiting program.")
            cap.release()
            cv2.destroyAllWindows()
            exit()

    counter = 0
    while counter < dataset_size:
        ret, frame = cap.read()
        if not ret:
            continue

        # Show current frame with count
        cv2.putText(frame, f'Class {j} | Image {counter + 1}/{dataset_size}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        cv2.imshow('frame', frame)

        # Resize and save image
        resized_frame = cv2.resize(frame, (224, 224))
        file_path = os.path.join(class_dir, f'{counter}.jpg')
        cv2.imwrite(file_path, resized_frame)
        print(f'✅ Captured image {counter + 1} of {dataset_size} for class {j}')

        # Handle keypresses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('e'):
            print("🛑 Early exit from this class capture requested.")
            break
        elif key == 27:  # Esc key
            print("🛑 ESC pressed. Exiting program.")
            cap.release()
            cv2.destroyAllWindows()
            exit()

        counter += 1

print("\n🎉 Data collection complete.")
cap.release()
cv2.destroyAllWindows()
