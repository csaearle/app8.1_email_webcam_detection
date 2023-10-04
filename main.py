import cv2
import time
from email_webcam import send_email
import glob

#  Start the webcam
video = cv2.VideoCapture(0)  #  (0) is the embedded camera
                            # (1) is an external usb camera
                            #  VideoCapture() is a class of cv2
time.sleep(1)  # Give the camera time to load and avoid black/ blank frames

# Capture the first frame for comparison
first_frame = None
status_list = []
count = 1  # count is a variable that counts the frame value of frame = 30 fps

while True:
    status = 0
    check, frame = video.read()

    # Convert all frames to grayscale to reduce information of RGB channels
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Apply GaussianBlur to grayscal image in order to reduce frame size further
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # Do frame comparison in while loop between all subsequent frames and first_frame
    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    # Show the captured delta_frame in Grayscale and Gaussian Blur applied as compared to first_frame
    # in video format

    # Seperate the black from the white in frame6
    thresh_frame = cv2.threshold(delta_frame, 67, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    #  Now show the dil_frame
    cv2.imshow("My video", dil_frame)

    # To find the contours, frame7, white areas (of interest) from black areas
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:  # If this is a fake object, run the loop again
        if cv2.contourArea(contour) < 5000:
            continue

        # extract from frame8 the dimensions of the rectangle over object
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            # To store images from frames (object enters frame )
            # Only capture an image if staus = 1 === an image has entered the frame + rectangle added
            cv2.imwrite(f"images/{count}image.png", frame)  #  capture still=image.png from frame
            count = count + 1
            #  After capturing many images after an object enters frame, select middle one
            # to send by email as middle one should be approximately best quality image
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            image_with_object = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        send_email()

    # exit condition from while loop = "q"
    cv2.imshow("Video", frame)
    key = cv2.waitKey(1)  #  create a keyboard key object

    if key == ord("q"):
        break

video.release()   #  release/end the video if "q" is pressed above