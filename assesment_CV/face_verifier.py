import cv2
import sys


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access the webcam.")
    sys.exit()

while True:
    # Read a frame from the webcam
    success, frame = cap.read()
    if not success:
        print("Error: Failed to grab frame.")
        break

   
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=6,
        minSize=(80, 80)
    )

   
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # green box
        cv2.putText(frame, "Agent Detected", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Show the live frame
    cv2.imshow("Delivery Agent Verifier", frame)

   
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        cv2.imwrite("agent_snapshot.jpg", frame)
        print("Snapshot saved as agent_snapshot.jpg")

    elif key == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()