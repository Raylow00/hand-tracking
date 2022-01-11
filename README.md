Hand Tracking Application

The goal of this hand tracking application is to explore and attempt to build the functionalities that would enable a person to control desktop applications to high precisions using only a webcam, ultimately removing the mouse.

As a starting point, there will be multiple scripts trying to accomplish different goals within a desktop window. Later, there will be an application packaging all the scripts for better usability.

Available scripts:
- gesture_mousecursor.py: 
    - Description: This script attempts to take the user's fingers as input and calculates the distance between the index finger and thumb to perform a click. Currently, it is able to click and resize/close windows, or generally perform any clicks as if using a mouse. 
    - Required fix: The mouse cursor is currently not in sync with the fingers positions accurately. The action of closing the index finger and thumb to indicate a click is also not smooth.

- gesture_volumecontroller.py:
    - Description: This script attempts to take the user's fingers as input and calculates the distance between the index finger and thumb to control the volume of the speaker connected. Currently, it is able to slide the volume slider of the master speaker.
    - Required fix: The slider is not exactly smooth and the range of the distance does not correspond correctly to the range of volume available.
