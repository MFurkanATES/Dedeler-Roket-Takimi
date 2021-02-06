from __future__ import print_function
from dronekit import connect, VehicleMode
import cv2
import time
import numpy as np

connection_string = "/dev/ttyACM0"
baudrate = 115200
atis_yeri = "TUZ GOLU TEKNOFEST"

height =720 
width = 1280

lock1 = 0.0
lock2 = 0.0
stage1 = True
stage2 = False


roll = 0.0
pitch = 0.0
yaw = 0.0

accel_x = 0.0
accel_y = 0.0
accel_z = 0.0

velo_x = 0.0
velo_y = 0.0
velo_z = 0.0

max_vel = 0.0

max_vel_x = 0.0
max_vel_y = 0.0
max_vel_z = 0.0

peak_vel_x = 0.0
peak_vel_y = 0.0
peak_vel_z = 0.0


screen_a = np.zeros((720,1280,3),dtype = np.uint8)

video = cv2.VideoCapture(0)



  


print("Dedeler Roketcilik Yer Kontrol V0.1\n")

#time.sleep(1.5)

print("YETKILILER\n\nM.Furkan ATES\nBekir KOLE\nA.Berdan MINAZ\n")
#time.sleep(1)

print("Rokete baglaniliyor\n \nBaglanti portu : %s  \nBaglanti hizi: %s " % (connection_string,baudrate))

vehicle = connect(connection_string, wait_ready=True,baud=baudrate)



def gps_line():  
  cv2.rectangle(screen,((width-270),0),(width-1,60),(150,255,50),1) 

def time_line():
  cv2.rectangle(screen,((270),0),(0,60),(150,255,50),1) 


#cv2.line(image,(pixel_yatay/2+new_dot_yatay_hud ,pixel_dikey/2 + new_dot_dikey_hud),(pixel_new_yatay,pixel_new_dikey),(150,255,50),1)
def stream_line():
  cv2.rectangle(screen,(320,120),(960,600),(150,255,50),1) 
 

def right_part_line():
  cv2.line(screen,(1100,60),(1100,560),(150,255,50),1)  #accel ust
  cv2.line(screen,(1100,200),(1280,200),(150,255,50),1) #velocity ust
  cv2.line(screen,(1100,560),(1280,560),(150,255,50),1) #velocity alt

def left_part_line():
  cv2.line(screen,(180,60),(180,560),(150,255,50),1)  #accel ust
  cv2.line(screen,(180,200),(1,200),(150,255,50),1) #velocity ust
  cv2.line(screen,(180,560),(1,560),(150,255,50),1) #velocity alt 

def lines():
  gps_line()
  time_line()
  stream_line()
  right_part_line()
  left_part_line()

def orientation():
  roll = round(np.degrees(vehicle.attitude.roll),4)
  pitch = round(np.degrees(vehicle.attitude.pitch),4)
  yaw = round(np.degrees(vehicle.attitude.yaw),4)

  cv2.putText(screen,("ORIENTATION"),(20,230),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)
  cv2.putText(screen,("ROLL: "+str(roll)),(20,260),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)
  cv2.putText(screen,("PITCH: "+str(pitch)),(20,290),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)
  cv2.putText(screen,("YAW: "+str(yaw)),(20,320),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)

def accel():
  
  cv2.putText(screen,("ACCELERATION"),(1125,90),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)
  cv2.putText(screen,("X: "+str(accel_x)),(1125,120),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)
  cv2.putText(screen,("Y: "+str(accel_y)),(1125,150),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)
  cv2.putText(screen,("Z: "+str(accel_z)),(1125,180),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)
  
def velo():
  global max_vel
  global max_vel_x
  global max_vel_y
  global max_vel_z
  global peak_vel_x
  global peak_vel_y
  global peak_vel_z

  velo_x = float(vehicle.velocity[0])
  velo_y = float(vehicle.velocity[1])
  velo_z = float(vehicle.velocity[2])

  vector_vel = np.sqrt(velo_x**2 + velo_y**2 + velo_z**2)

  if(np.sqrt(max_vel**2) < np.sqrt(vector_vel**2)):
    max_vel = round(vector_vel,4)
    max_vel_x = velo_x
    max_vel_y = velo_y
    max_vel_z = velo_z 

  if(np.sqrt(peak_vel_x**2) < np.sqrt(velo_x**2)):
    peak_vel_x = velo_x

  if(np.sqrt(peak_vel_y**2) < np.sqrt(velo_y**2)):
    peak_vel_y = velo_y

  if(np.sqrt(peak_vel_z**2) < np.sqrt(velo_z**2)):
    peak_vel_z = velo_z

  cv2.putText(screen,("VELOCITY"),(1125,230),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)
  cv2.putText(screen,("X : "+str(velo_x)),(1125,260),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)
  cv2.putText(screen,("Y : "+str(velo_y)),(1125,290),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)
  cv2.putText(screen,("Z : "+str(velo_z)),(1125,320),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)
  cv2.putText(screen,("PEAK X : "+str(peak_vel_x)),(1125,350),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)
  cv2.putText(screen,("PEAK Y : "+str(peak_vel_y)),(1125,380),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)
  cv2.putText(screen,("PEAK Z : "+str(peak_vel_z)),(1125,410),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)
  cv2.putText(screen,("MAX : "+str(max_vel)),(1125,440),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)
  cv2.putText(screen,("MAX X : "+str(max_vel_x)),(1125,470),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)
  cv2.putText(screen,("MAX Y : "+str(max_vel_y)),(1125,500),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)
  cv2.putText(screen,("MAX Z : "+str(max_vel_z)),(1125,530),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)

def Time():
  cv2.putText(screen,("TIME"),(25,20),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)

def Gps():
  cv2.putText(screen,("HOME"),(width-260,30),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)
  cv2.putText(screen,(str(round(vehicle.location.global_relative_frame.lat,4))),(width-210,30),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)
  cv2.putText(screen,(str(round(vehicle.location.global_relative_frame.lon,4))),(width-130,30),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)
  cv2.putText(screen,(str(round(vehicle.location.global_relative_frame.alt,2))),(width-50,30),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)

  
  #su an ki gps datasi
  cv2.putText(screen,("CURR"),(width-260,50),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)
  cv2.putText(screen,(str(round(vehicle.location.global_relative_frame.lat,4))),(width-210,50),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)
  cv2.putText(screen,(str(round(vehicle.location.global_relative_frame.lon,4))),(width-130,50),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)
  cv2.putText(screen,(str(round(vehicle.location.global_relative_frame.alt,2))),(width-50,50),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)
  #vehicle.location.global_relative_frame.lat)

def stages():
  #2 adet stm yada arduino rcInden girip butonun tetiklemesi sonrasi pwm degistirecek 
  global lock1
  global lock2 
  global stage1
  global stage2

  if(vehicle.armed == True):
    cv2.putText(screen,("ARMED"),(25,180),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)
  else:
    cv2.putText(screen,("DISARMED"),(25,180),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)

  lock1 = vehicle.channels[4]
  lock2 = vehicle.channels[5]
  if (lock1 > 1500 and lock2 > 1500):
    stage1 = False
    stage2 = True

  else:
    stage1 = True
    stage2 = False 

  if(stage1 == True):
    stage1_txt = "ACTIVE"
    stage2_txt = "PASSIVE"

  if (stage2 == True):   
    stage1_txt = "PASSIVE"
    stage2_txt = "ACTIVE" 
  
  cv2.putText(screen,("STAGES"),(25,90),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)
  cv2.putText(screen,("STAGE 1:"+str(stage1_txt)),(25,120),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)
  cv2.putText(screen,("STAGE 2:"+str(stage2_txt)),(25,150),cv2.FONT_HERSHEY_PLAIN,1,(150,255,50),1)

  


while True:
  screen = np.copy(screen_a)
  Gps()
  Time()
  accel()
  velo()
  orientation()
  stages()

  lines()
  ret,frame = video.read()
  #print(np.size(frame))
  #frame2  =  cv2.resize(frame,(640,480))
  for i in range (480):
    for j in range (640):
      screen_a[120 + i , 320+j] = frame[i,j]
  cv2.imshow("s",screen)
  
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
#cv2.waitKey()

#def TIME():

#def label_bottom():
