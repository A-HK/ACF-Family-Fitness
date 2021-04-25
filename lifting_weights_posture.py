import cv2 as cv
import mediapipe as mp
import math
import numpy as np

mp_pose = mp.solutions.pose
counter = 0
counter1 = 0
position = 'up'
position1 = 'down'

mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

def calc_angle1(a, b, c):
    angle = 0
    try:
        AB = np.array([b[0] - a[0], b[1] - a[1]])
        BC = np.array([c[0] - b[0], c[1] - b[1]])
        
        radians = math.acos(np.dot(AB, BC)/(np.linalg.norm(AB) * np.linalg.norm(BC)))
        angle = np.abs(radians*180.0/np.pi)
        
        if angle >180.0:
            angle = 360-angle
    
    except:
         pass
        
    return 180.0 - angle
        

cap = cv.VideoCapture(0)


with mp_pose.Pose() as pose:
    while cap.isOpened():
        
        ret, img = cap.read()
        width, height, _ = img.shape
        imgResult = img.copy()
        results = pose.process(cv.cvtColor(img, cv.COLOR_BGR2RGB))
        shoulder, elbow, wrist = [0, 0, 0], [0, 0, 0], [0, 0, 0]
        shoulder1, elbow1, wrist1 = [0, 0, 0], [0, 0, 0], [0, 0, 0]
        
        try:
        
            landmarks = results.pose_landmarks.landmark
            #print(landmarks)

            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].z]

            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y,
                        landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].z]

            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y,
                        landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].z]

            shoulder1 = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y,
                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].z]

            elbow1 = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y,
                        landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].z]

            wrist1 = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y,
                        landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].z]
        except:
            pass

        angle = calc_angle1(shoulder, elbow, wrist)
        angle1 = calc_angle1(shoulder1, elbow1, wrist1)
        #print(angle)
        
        cv.putText(imgResult, str(angle), tuple(np.multiply(elbow[:2], [640, 480]).astype(int)),
                   cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA)

        cv.putText(imgResult, str(angle1), tuple(np.multiply(elbow1[:2], [640, 480]).astype(int)),
                   cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA)
        

        if angle > 160:
            position = "down"
        elif angle < 30 and position =='down':
            position="up"
            counter +=1

        if angle1 > 160:
            position1 = "down"
        elif angle1 < 30 and position1 =='down':
            position1="up"
            counter1 +=1
       
            
        
        cv.putText(imgResult, str(counter), (width - 20, 60),
                    cv.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv.LINE_AA)

        cv.putText(imgResult, str(counter1), (30, 60),
                    cv.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv.LINE_AA)

        mp_drawing.draw_landmarks(
            image = imgResult,
            landmark_list = results.pose_landmarks,
            connections = mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec = drawing_spec,
            connection_drawing_spec = drawing_spec)

        cv.imshow('Result', imgResult)
        key = cv.waitKey(1)
        if key == 27:
            break

cap.release()
cv.destroyAllWindows()


    

