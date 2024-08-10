import cv2
import numpy as np
import random

bird_frame=1
bird_x = 200
bird_y = 200
bird_size=[40,30]
bird_image=[1,1]
bird_image[0]=cv2.imread(r'.\flappy_bird\Flappy-Bird1.png')
bird_image[1]=cv2.imread(r'.\flappy_bird\Flappy-Bird2.png')
bird_image[0] = cv2.resize(bird_image[0],(bird_size[0],bird_size[1]))
bird_image[1] = cv2.resize(bird_image[1],(bird_size[0],bird_size[1]))

pipes=[[0,200,False],[-350,300,False],[-700,100,False]]#[pipe_x,gap_y,pass or not]
pipe_width=70
pipe_gap = 150

speed = 15
score = 0
run = True

def draw_pipe(img):
    global score
    height= img.shape[0]
    width = img.shape[1]
    for pipe in pipes:
        cv2.rectangle(img, (width-pipe[0], 0),(width-pipe[0]-pipe_width,pipe[1]),(88, 218,125 ),cv2.FILLED)
        cv2.rectangle(img, (width-pipe[0], pipe[1]+pipe_gap),(width-pipe[0]-pipe_width,height),(88, 218,125 ),cv2.FILLED)
        pipe[0]+=speed+int(score*0.1)
        if width-pipe[0]<bird_x-bird_size[0] and pipe[2]==False:
            score=score+1
            pipe[2]=True
        if(pipe[0]>width):
            pipe[0] = min(pipes[0][0],pipes[1][0],pipes[2][0])-350
            pipe[1]=random.randint(100,300) 
            pipe[2]=False

def draw_bird(img):
    width = img.shape[1]
    global run, bird_frame
    for pipe in pipes:
        if width-pipe[0]-70<bird_x+bird_size[0] and width-pipe[0]>bird_x and (bird_y<pipe[1] or bird_y+bird_size[1]>pipe_gap+pipe[1]):
            run=False
            break
    img[bird_y:bird_y+bird_size[1],bird_x:bird_x+bird_size[0]]=bird_image[bird_frame]
    if bird_frame==0:
        bird_frame=1
    else:
        bird_frame=0
def game_over(img):
    cv2.putText(img,"Your Score:"+str(score),(50,100),cv2.FONT_HERSHEY_SIMPLEX,1.5,(255,255,255),4)
    cv2.putText(img,"press q to quit the game",(50,200),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
    return 0

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame,(0,0),fx=1.2,fy=1.2)
        gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        if(run==True):
            faceCascade=cv2.CascadeClassifier(r'.\flappy_bird\face_detect.xml')
            faceRect = faceCascade.detectMultiScale(gray_frame, 1.1, 6)
            for(x,y,w,h)in faceRect:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                bird_y = int(y+h/2)
            draw_pipe(frame)
            draw_bird(frame)
            cv2.putText(frame, str(score),(int(frame.shape[1]/2),100),cv2.FONT_HERSHEY_SIMPLEX,1.5,(255,255,255),4)
        else:
            game_over(frame)
        cv2.imshow('video',frame)
    else:
        break
    if cv2.waitKey(10)==ord('q'):
        break