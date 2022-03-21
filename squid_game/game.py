import cv2
import sys
sys.path.insert(1, "C:\\Users\\Raych\\Documents\\Computer Vision Projects\\Hand Tracking")
import track_module.trackmodule as tm
import time
import math
import numpy as np
import ctypes

# Drawing parameters
STARTING_POINT_RADIUS = 20
DRAWING_POINT_RADIUS = 15
RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
PURPLE = (255, 0, 255)
THICKNESS = 3
FILLED = -1

def check_collision(a, b, c, x, y, radius):
      
    # Finding the distance of line 
    # from center.
    dist = ((abs(a * x + b * y + c)) /
            math.sqrt(a * a + b * b))
  
    # Checking if the distance is less 
    # than, greater than or equal to radius.
    if (radius >= dist):
        return True
    else:
        return False

def prepare_target_image(image_path):
    target_image = cv2.imread(image_path)
    target_image = cv2.resize(target_image, (512, 512))

    # Create a blank image
    blank = np.zeros([1080, 1440, 3],dtype=np.uint8)
    blank.fill(255)
    blank_height, blank_width, blank_c = blank.shape
    blank_cy, blank_cx = blank_height // 2, blank_width // 2

    # Place the target image in the center of the blank image
    blank[blank_cy - (512//2):blank_cy + (512//2), blank_cx - (512//2):blank_cx + (512//2)] = target_image

    return blank

def prepare_broken_target_image(image_path):
    broken_target_image = cv2.imread(image_path)
    broken_target_image = cv2.resize(broken_target_image, (512, 512))
    broken_target_image_height, broken_target_image_width, channel = broken_target_image.shape

    # Create a blank image
    broken_blank = np.zeros([1080, 1440, 3],dtype=np.uint8)
    broken_blank.fill(255)
    broken_blank_height, broken_blank_width, broken_blank_c = broken_blank.shape
    broken_blank_cy, broken_blank_cx = broken_blank_height // 2, broken_blank_width // 2

    # Place the target image in the center of the blank image
    broken_blank[broken_blank_cy - (512//2):broken_blank_cy + (512//2), broken_blank_cx - (512//2):broken_blank_cx + (512//2)] = broken_target_image

    return broken_blank

def preprocess_target_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 30, 100)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 150, np.array([]), 50, 10)
    line_1_x1 = []
    line_1_x2 = []
    line_1_y1 = []
    line_1_y2 = []
    line_2_x1 = []
    line_2_x2 = []
    line_2_y1 = []
    line_2_y2 = []
    line_3_x1 = []
    line_3_x2 = []
    line_3_y1 = []
    line_3_y2 = []

    for line in lines:
        for x1, y1, x2, y2 in line:
            if((y2-y1)/(x2-x1)) > 0:
                line_1_x1.append(x1)
                line_1_x2.append(x2)
                line_1_y1.append(y1)
                line_1_y2.append(y2)

            elif((y2-y1)/(x2-x1)) < 0:
                line_2_x1.append(x1)
                line_2_x2.append(x2)
                line_2_y1.append(y1)
                line_2_y2.append(y2)

            else:
                line_3_x1.append(x1)
                line_3_x2.append(x2)
                line_3_y1.append(y1)
                line_3_y2.append(y2) 

    line_1_x1_mean = np.mean(line_1_x1)
    line_1_x2_mean = np.mean(line_1_x2)
    line_1_y1_mean = np.mean(line_1_y1)
    line_1_y2_mean = np.mean(line_1_y2)
    line_2_x1_mean = np.mean(line_2_x1)
    line_2_x2_mean = np.mean(line_2_x2)
    line_2_y1_mean = np.mean(line_2_y1)
    line_2_y2_mean = np.mean(line_2_y2)
    line_3_x1_mean = np.mean(line_3_x1)
    line_3_x2_mean = np.mean(line_3_x2)
    line_3_y1_mean = np.mean(line_3_y1)
    line_3_y2_mean = np.mean(line_3_y2)
    print("Mean of x1 in line 1: ", line_1_x1_mean)
    print("Mean of x2 in line 1: ", line_1_x2_mean)
    print("Mean of y1 in line 1: ", line_1_y1_mean)
    print("Mean of y2 in line 1: ", line_1_y2_mean)
    print("Mean of x1 in line 2: ", line_2_x1_mean)
    print("Mean of x2 in line 2: ", line_2_x2_mean)
    print("Mean of y1 in line 2: ", line_2_y1_mean)
    print("Mean of y2 in line 2: ", line_2_y2_mean)
    print("Mean of x1 in line 3: ", line_3_x1_mean)
    print("Mean of x2 in line 3: ", line_3_x2_mean)
    print("Mean of y1 in line 3: ", line_3_y1_mean)
    print("Mean of y2 in line 3: ", line_3_y2_mean)

    return line_1_x1_mean, line_1_x2_mean, line_1_y1_mean, line_1_y2_mean, line_2_x1_mean, line_2_x2_mean, line_2_y1_mean, line_2_y2_mean, line_3_x1_mean, line_3_x2_mean, line_3_y1_mean, line_3_y2_mean

def find_line_length(a, b, c, x1, y1, x2, y2):
    a1 = a
    b1 = b
    c1 = c
    line_len = math.sqrt(((x2-x1)**2+(y2-y1)**2))
    return line_len

# # Biscuit image to overlay
target_image_path = "images/triangle_biscuit.jpg"
blank = prepare_target_image(target_image_path)

# Broken biscuit image to overlay
broken_target_image_path = "images/triangle_biscuit_broken.jpg"
broken_blank = prepare_broken_target_image(broken_target_image_path)

# Preprocess the image to get the outline of the shape
blank_copy = blank.copy()
line_1_x1_mean, line_1_x2_mean, line_1_y1_mean, line_1_y2_mean, line_2_x1_mean, line_2_x2_mean, line_2_y1_mean, line_2_y2_mean, line_3_x1_mean, line_3_x2_mean, line_3_y1_mean, line_3_y2_mean = preprocess_target_image(blank_copy)

# Starting point
cv2.circle(blank, (int(line_1_x1_mean), int(line_1_y1_mean)), STARTING_POINT_RADIUS, RED, FILLED)

# Line parameters (ax + by + c = 0)
# Line 1
a1 = -1.8077
b1 = 1
c1 = 954.7308
line_1_len = find_line_length(a1, b1, c1, line_1_x1_mean, line_1_y1_mean, line_1_x2_mean, line_1_y2_mean)

# Line 2
a2 = 0.009035
b2 = 1
c2 = -658.762
line_2_len = find_line_length(a2, b2, c2, line_1_x2_mean, line_1_y2_mean, line_3_x1_mean, line_3_y1_mean)

# Line 3
a3 = 1.7977
b3 = 1
c3 = -1637.57
line_3_len = find_line_length(a3, b3, c3, line_1_x1_mean, line_1_y1_mean, line_3_x1_mean, line_3_y1_mean)

# Total length of lines
total_len = line_1_len + line_2_len + line_3_len

# Get screen size
user32 = ctypes.windll.user32
screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


##############################################################################################################
# Start video
cap = cv2.VideoCapture(0)

detector = tm.HandDetector(detectionCon=0.7)

# Booleans
toStartGame = False
toStartTime = False
gameLost = False
gameWon = False

# Points and distance
curr_pt_x, curr_pt_y = 0, 0
prev_pts_x, prev_pts_y = [], []
distance_drawn = 0

# Time
pTime = 0
start_time = 0
duration = 0

while True:
    success, img = cap.read()
    
    # Adjust the size of the frame
    img = cv2.flip(img, 1)
    frame_height, frame_width, _ = img.shape
    scaleWidth = float(screen_width) / float(frame_width)
    scaleHeight = float(screen_height) / float(frame_height)

    if scaleHeight > scaleWidth:
        imgScale = scaleWidth
    else:
        imgScale = scaleHeight

    newX, newY = img.shape[1] * imgScale, img.shape[0] * imgScale
    img = cv2.resize(img, (int(newX), int(newY)))   # Screen width: 1440, Screen height: 1080

    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)

    if len(lmlist) != 0:
        x1, y1 = lmlist[8][1], lmlist[8][2]
        
        curr_pt_x, curr_pt_y = x1, y1

        starting_pt_dist = math.sqrt((curr_pt_x - line_1_x1_mean)**2 + (curr_pt_y - line_1_y1_mean)**2)
        # Begin game
        if starting_pt_dist < 5:
            toStartGame = True
            toStartTime = True

        if toStartGame:
            # Points drawn by player
            prev_pts_x.append(curr_pt_x)
            prev_pts_y.append(curr_pt_y)
            cv2.circle(blank, (curr_pt_x, curr_pt_y), DRAWING_POINT_RADIUS, PURPLE, FILLED)
            
            if len(prev_pts_x) > 2 and len(prev_pts_y) > 2:
                # Calculate distance drawn
                distance_drawn += math.sqrt((curr_pt_x - prev_pts_x[-2])**2 + (curr_pt_y - prev_pts_y[-2])**2)

            # Line 1
            cv2.line(img, (int(line_1_x1_mean), int(line_1_y1_mean)), (int(line_1_x2_mean), int(line_1_y2_mean)), GREEN, THICKNESS)

            # Line 2
            cv2.line(img, (int(line_1_x2_mean), int(line_1_y2_mean)), (int(line_3_x1_mean), int(line_3_y1_mean)), GREEN, THICKNESS)

            # Line 3
            cv2.line(img, (int(line_1_x1_mean), int(line_1_y1_mean)), (int(line_3_x1_mean), int(line_3_y1_mean)), GREEN, THICKNESS)

            # Check collision between index finger point and lines
            collided_line1 = check_collision(a1, b1, c1, int(x1), int(y1), DRAWING_POINT_RADIUS)
            collided_line2 = check_collision(a2, b2, c2, int(x1), int(y1), DRAWING_POINT_RADIUS)
            collided_line3 = check_collision(a3, b3, c3, int(x1), int(y1), DRAWING_POINT_RADIUS)

            if collided_line1 is True or collided_line2 is True or collided_line3 is True:
                pass
            else:
                gameLost = True
        
        if toStartTime:
            start_time = time.time()
            toStartTime = False

        # End game
        if starting_pt_dist < 5 and distance_drawn > total_len:
            toStartGame = False
            gameWon = True

    if not gameLost:
        dst = cv2.addWeighted(img, 0.5, blank, 0.5, 0.0)
    else:
        dst = cv2.addWeighted(img, 0.5, broken_blank, 0.5, 0.0)

    # Time taken
    if toStartGame and gameLost == False:
        end_time = time.time()
        duration = end_time - start_time
        cv2.putText(dst, f'Time: {int(duration)} sec', (35, 100), cv2.FONT_HERSHEY_COMPLEX, 0.7, BLUE, 2)

    if gameWon:
        cv2.putText(dst, 'Congratulations Player 456!', (300, 150), cv2.FONT_HERSHEY_COMPLEX, 2, BLUE, 2)            
        cv2.putText(dst, "{:.2f} seconds".format(duration), (500, 230), cv2.FONT_HERSHEY_COMPLEX, 2, RED, 2)
    elif gameLost:
        cv2.putText(dst, "Player 456, You have been eliminated!", (130, 150), cv2.FONT_HERSHEY_COMPLEX, 1.5, RED, 2)
    elif not gameLost and not gameWon:
        # Instructions
        cv2.putText(dst, f'Show hand on screen and place index finger on red dot to start game.', (35, 50), cv2.FONT_HERSHEY_COMPLEX, 0.7, BLUE, 2)

    # FPS
    cTime = time.time()
    fps = 1 / (cTime-pTime)
    pTime = cTime
    # cv2.putText(dst, f'FPS: {int(fps)}', (35, 50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 0), 2)

    cv2.imshow("Squid Game Dalgona", dst)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break    

cap.release()
cv2.destroyAllWindows()