#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase


left = Motor(Port.A)
right = Motor(Port.D)
gyro = GyroSensor(Port.S4)
ultra = UltrasonicSensor(Port.S3)
color = ColorSensor(Port.S1)

def 아니요() :
    brick.sound.file(SoundFile.YES) 

def 예() :
    brick.sound.file(SoundFile.NO) 

def 움직여(leftp, rightp) :
    left.run(leftp)
    right.run(rightp)

def 멈춰() :
    left.stop(Stop.BRAKE);
    right.stop(Stop.BRAKE);

def 자이로센서() :
    return gyro.angle ()

def 거리측정() :
    return ultra.distance()/10

def 목적지() : 
    return (color.color() == Color.RED)
# Write your program here
# 여기서 부터 프로그램을 작성하세요 

L0=400 #왼쪽 파워
R0=400 #오른쪽 파워 
baseDeg = 0 # 처음각도
distWall = 15 # 장애물 거리
Kp = 10

def Run() :
    while True :
        if 거리측정() < distWall :
            멈춰()
            break
        c = 자이로센서()
        e = baseDeg - c
        Li = L0 + (e*Kp)
        Ri = R0 - (e*Kp)
        움직여(Li,Ri)

def Turn(d) : 
    global baseDeg
    baseDeg += d
    while True :
        wait(10)
        c = 자이로센서() # 현재 각도 얻기
        e = baseDeg - c
        if abs(e) < 1 :
            멈춰()
            break
        Li = 100 + (e*Kp)
        Ri = 100 - (e*Kp)
        움직여(Li,Ri)    

while True :
    Run()
    
    if 목적지() :
        break

    Turn(90) #오른쪽 90
    r = 거리측정()
    Turn(-90) # 원래방향 복귀

    Turn(-90) # 왼쪽 90
    l = 거리측정()
    Turn(90) #원래방향 복귀
    
    if r > l :
        Turn(90) # 넓은 쪽으로 방향 전환
    else :
        Turn(-90) # 넓은 쪽으로 방향 전환
