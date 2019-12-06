from tkinter import *

import random
import socket 
from threading import Thread



WIDTH = 500
HEIGHT = 400
 

LEFT_PAD_W = 0
PAD_W = 10

LEFT_PAD_H = 0
PAD_H = 100
 

BALL_SPEED_UP = 1.0

BALL_MAX_SPEED = 40

BALL_RADIUS = 30

INITIAL_SPEED = 10
BALL_X_SPEED = INITIAL_SPEED
BALL_Y_SPEED = INITIAL_SPEED


PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0

left_comp_ip = "192.168.255.132"
middle_comp_ip = "192.168.255.130"
right_comp_ip = "192.168.255.131"

SEND_IP_PORT1 = (left_comp_ip,10000)
SEND_IP_PORT2 = (middle_comp_ip,10002)
SEND_IP_PORT2_2 = (middle_comp_ip,10003)
SEND_IP_PORT3 = (right_comp_ip,10004)

RECV_IP_PORT1 = (left_comp_ip,11000)
RECV_IP_PORT2 = (middle_comp_ip,11001)
RECV_IP_PORT3 = (right_comp_ip,11002)



have_ball = True

def send() : 
    global BALL_X_CHANGE,BALL_Y_CHANGE,have_ball,BALL_X_SPEED,BALL_Y_SPEED
    soc = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    soc.bind(SEND_IP_PORT3)
    msg_l = c.coords(BALL)
    msg = str(msg_l[0]) + ',' + str(msg_l[1]) + ',' + str(msg_l[2]) + ',' + str(msg_l[3]) + ',' + str(BALL_X_SPEED) + ','+ str(BALL_Y_SPEED) + ',' + 'RIGHT'
    BALL_X_SPEED = 0
    BALL_Y_SPEED = 0
    msg =  msg.encode('UTF-8')
    soc.sendto(msg,RECV_IP_PORT2)
    have_ball = False
    c.coords(BALL,200,200,200,200)
def t_func_recv() :
    global have_ball,BALL_Y_CHANGE,BALL_X_CHANGE,BALL_X_SPEED,BALL_Y_SPEED
    if have_ball == False :
        BALL_Y_SPEED = 0
        BALL_X_SPEED = 0
        soc = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        soc.bind(RECV_IP_PORT3)
        msg = soc.recv(1024)
        msg = msg.decode('UTF-8')
        msg = msg.split(',')
        print(msg)
        c.coords(BALL,50,msg[1],20,msg[3])

        BALL_Y_SPEED = float(msg[5])
        BALL_X_SPEED = 10
        have_ball = True
    if have_ball == True : 
        pass
    root.after(10,t_func_recv)


right_line_distance = WIDTH - PAD_W


def t_func_score_check():
    pass


def update_score(player):
    pass

def spawn_ball():
    global BALL_X_SPEED

    c.coords(BALL, WIDTH/2-BALL_RADIUS/2,
             HEIGHT/2-BALL_RADIUS/2,
             WIDTH/2+BALL_RADIUS/2,
             HEIGHT/2+BALL_RADIUS/2)

    BALL_X_SPEED = 10

def bounce(action):
    global BALL_X_SPEED, BALL_Y_SPEED

    if action == "strike":
        BALL_Y_SPEED = random.randrange(-10, 10)
        if abs(BALL_X_SPEED) < BALL_MAX_SPEED:
            BALL_X_SPEED *= -BALL_SPEED_UP
        else:
            BALL_X_SPEED = -BALL_X_SPEED
    else:
        BALL_Y_SPEED = -BALL_Y_SPEED



root = Tk()
root.title("client(right)")
 

c = Canvas(root, width=WIDTH, height=HEIGHT, background="#000000")
c.pack()
 

 

c.create_line(WIDTH-PAD_W, 0, WIDTH-PAD_W, HEIGHT, fill="white")


 

 

BALL = c.create_oval(WIDTH/2-BALL_RADIUS/2,
                     HEIGHT/2-BALL_RADIUS/2,
                     WIDTH/2+BALL_RADIUS/2,
                     HEIGHT/2+BALL_RADIUS/2, fill="white")
 

LEFT_PAD = c.create_line(LEFT_PAD_W/2, 0, LEFT_PAD_W/2, LEFT_PAD_H, width=LEFT_PAD_W, fill="blue")
 

RIGHT_PAD = c.create_line(WIDTH-PAD_W/2, 0, WIDTH-PAD_W/2, 
                          PAD_H, width=PAD_W, fill="yellow")




BALL_X_CHANGE = 20

BALL_Y_CHANGE = 0
 
def move_ball():

    ball_left, ball_top, ball_right, ball_bot = c.coords(BALL)
    ball_center = (ball_top + ball_bot) / 2
 

    if ball_right + BALL_X_SPEED < right_line_distance and \
            ball_left + BALL_X_SPEED > PAD_W:
        c.move(BALL, BALL_X_SPEED, BALL_Y_SPEED)

    elif ball_right == right_line_distance or ball_left == PAD_W:

        if ball_right > WIDTH / 2:

            if c.coords(RIGHT_PAD)[1] < ball_center < c.coords(RIGHT_PAD)[3]:
                bounce("strike")
            else:

                update_score("right")
                spawn_ball()
        else:

            if c.coords(LEFT_PAD)[1] < ball_center < c.coords(LEFT_PAD)[3]:
                bounce("strike")
            else:
                send()

    else:
        if ball_right > WIDTH / 2:
            c.move(BALL, right_line_distance-ball_right, BALL_Y_SPEED)
        else:
            c.move(BALL, -ball_left+PAD_W, BALL_Y_SPEED)

    if ball_top + BALL_Y_SPEED < 0 or ball_bot + BALL_Y_SPEED > HEIGHT:
        bounce("ricochet")


PAD_SPEED = 20

LEFT_PAD_SPEED = 0

RIGHT_PAD_SPEED = 0
 

def move_pads():

    PADS = {LEFT_PAD: LEFT_PAD_SPEED, 
            RIGHT_PAD: RIGHT_PAD_SPEED}

    for pad in PADS:

        c.move(pad, 0, PADS[pad])

        if c.coords(pad)[1] < 0:
            c.move(pad, 0, -c.coords(pad)[1])
        elif c.coords(pad)[3] > HEIGHT:
            c.move(pad, 0, HEIGHT - c.coords(pad)[3])

 
def main():
    move_ball()
    move_pads()

    root.after(30, main)


c.focus_set()
 

def movement_handler(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym == "w":
        LEFT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "s":
        LEFT_PAD_SPEED = PAD_SPEED
    elif event.keysym == "Up":
        RIGHT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "Down":
        RIGHT_PAD_SPEED = PAD_SPEED
 

c.bind("<KeyPress>", movement_handler)
 

def stop_pad(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym in "ws":
        LEFT_PAD_SPEED = 0
    elif event.keysym in ("Up", "Down"):
        RIGHT_PAD_SPEED = 0
 

c.bind("<KeyRelease>", stop_pad)


main()
 

t1 = Thread(target=t_func_recv)
t1.start()

t2 = Thread(target=t_func_score_check)
t2.start()


root.mainloop()
