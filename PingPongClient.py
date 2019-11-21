from turtle import Turtle, Screen

from socket import socket, AF_INET, SOCK_STREAM

from _thread import start_new_thread

from time import sleep


def receive_thread(s):
    while True:
        y = s.recv(500).decode('UTF-8')
        paddle_a.sety(int(y))

def send_function(y):
    x = str(y)
    s.send(x.encode('UTF-8'))

def gameloop(s):

    score_a = 0
    score_b = 0
    

    sleep(10)

    while True:
        wind.update()
        

        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)
    
    

        if ball.ycor() > 300:
            ball.sety(300)
            ball.dy *= -1
    
        if ball.ycor() < -300:
            ball.sety(-300)
            ball.dy *= -1
    
        if ball.xcor() > 390:
            ball.goto(0, 0)
            ball.dx *= -1
            score_a += 1
            pen.clear()
            pen.write("Player A: {}          Player B: {}".format(score_a, score_b), align="center", font=("Comic Sans MS", 15, "normal"))
    
        if ball.xcor() < -390:
            ball.goto(0, 0)
            ball.dx *= -1
            score_b += 1
            pen.clear()
            pen.write("Player A: {}          Player B: {}".format(score_a, score_b), align="center", font=("Comic Sans MS", 15, "normal"))
    

        if ball.xcor() > 350 and ball.xcor() < 360 and ball.ycor() < paddle_b.ycor() + 50 and ball.ycor() > paddle_b.ycor() -50:
            ball.setx(350)
            ball.dx *= -1.2
    
        if ball.xcor() < -350 and ball.xcor() > -360 and ball.ycor() < paddle_a.ycor() + 50 and ball.ycor() > paddle_a.ycor() -50:
            ball.setx(-350)
            ball.dx /= -1.2
                

def paddle_b_up():
    y = paddle_b.ycor()
    y += 100
    paddle_b.sety(y)
    send_function(y)

def paddle_b_down():
    y = paddle_b.ycor()
    y -= 100
    paddle_b.sety(y)
    send_function(y)

wind = Screen()
wind.title("Ping Pong: Client player")
wind.bgcolor("#222222")
wind.setup(width=1000, height=650)
wind.tracer(0)


paddle_a = Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("blue")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-360, 0)


paddle_b = Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("#fcff30")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(360, 0)


ball = Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 1
ball.dy = -1


pen = Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 110)
pen.write("Player A: 0          Player B: 0", align="center", font=("Comic Sans MS", 15, "normal"))


wind.listen()
wind.onkeypress(paddle_b_up, "Up")
wind.onkeypress(paddle_b_down, "Down")

s=socket(AF_INET, SOCK_STREAM)
s.connect(('192.168.1.9',7010))

start_new_thread(receive_thread,(s,))
start_new_thread(gameloop,(s,))
wind.mainloop()