import cv2
import winsound

cap = cv2.VideoCapture(0)
perSecond = 100
trackImage = 300

startCapturing = False
countdownActive = False

while True:
    ret, frame = cap.read()
    cv2.imshow('Camera', frame)

    # Show the countdown in the console while the camera feed is active
    if startCapturing and countdownActive:
        if perSecond > 0:
            print(f"Preparing... Photo will be captured in {perSecond} seconds", end='\r')
            perSecond -= 1
        else:
            cv2.imwrite(f'captured_image_{trackImage}.jpg', frame)
            print(f"\nPhoto {trackImage + 1} captured!")
            trackImage += 1
            perSecond = 100
            countdownActive = False
            winsound.MessageBeep(winsound.MB_OK)

    # Keypress controls for starting and stopping capture
    key = cv2.waitKey(1)
    
    if key == ord('q'):
        print(f"Total images captured: {trackImage}. The process will stop now.")
        break
    elif key == ord('s'):
        print("The process has started. Prepare yourself to register the images.")
        startCapturing = True
        countdownActive = True
    elif key == ord('p'):
        startCapturing = False
        countdownActive = False
        print("The process is stopped. Press 'R' when you're ready to resume.")
    elif key == ord('r'):
        print("Resuming the process, the countdown has been reset!")
        perSecond = 100
        startCapturing = True
        countdownActive = True

cap.release()
cv2.destroyAllWindows()
