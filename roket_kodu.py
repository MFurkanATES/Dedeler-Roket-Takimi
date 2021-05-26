from dronekit import *
import dronekit
import numpy as np

#egu icin rs232 baglantisi ve mesaj eklenecek
#otopilot konfigure edilmeden kod duzgun calismaz
#kanallarin hepsi otopilotta servo yada role olarak ayarlanacak
#bu baglantiların ucuna mosfet anahtar gerekli barut ateslemeye
#hiz aliniyor fakat kullanilmadi,ivme vektorsel olarak alinmaya calisilacak
#mosfet acilma süreleri belirlenecek time.sleep eklemeyeateslemeler icin

#otopilot baglantisi mavproxy dronekit 
"""connection_string = "/dev/ttyACM0"
baudrate = 115200
vehicle = connect(connection_string, wait_ready=True,baud=baudrate)"""

vehicle = connect('127.0.0.1:14550', wait_ready=True)

#yuksekiklerin belirlenmesi
#-------------------------------
#yuzdelik deger 
#sayi girisi 0.5 gibi olmali
per_drouge = 0.8
per_payload = 0.7
per_main = 0.6
#-------------------------------
#ilk kademenin kacinci metrede ayrilacagi
stage_sep = 15.0

#sakin bu degiskene dokunma
#!!!!!!!!!!!!
apogee = 0.0
#!!!!!!!!!!!!


# sensor degiskenleri
lat = 0.0 
lon = 0.0
alt = 0.0

roll = 0.0
pitch = 0.0
yaw = 0.0

accel_x = 0.0
accel_y = 0.0
accel_z = 0.0

peak_accel_x = 0.0
peak_accel_y = 0.0
peak_accel_z = 0.0

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


#bayraklar
#ilk kademe flag
stage_lock = 0

#tirmanma icin 1,dusus icin 0
flight_status = 1

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

def orientation():
  global roll
  global pitch
  global yaw
  roll = round(np.degrees(vehicle.attitude.roll),4)
  pitch = round(np.degrees(vehicle.attitude.pitch),4)
  yaw = round(np.degrees(vehicle.attitude.yaw),4)

def location():
  global lat 
  global lon
  global alt
  lat = vehicle.location.global_relative_frame.lat
  lon = vehicle.location.global_relative_frame.lon
  alt = vehicle.location.global_relative_frame.alt

  #print(alt)

def egu_signal():
  print("2.kademe atesleniyor")
  #egu atesleme baglantisi 1.kanal
  vehicle.channels.overrides['1'] = 2000

def drouge_parasutu():
  print("drouge parasutu atesleniyor")
  #drouge parasutu atesleme baglantisi 2.kanal
  vehicle.channels.overrides['2'] = 2000

def payload():
  print("payload atesleniyor")
  #payload atesleme baglantisi 3.kanal 
  vehicle.channels.overrides['3'] = 2000

def main_parasutu():
  print("main arasutu atesleniyor")
  #main parasutu atesleme baglantisi 4.kanal
  vehicle.channels.overrides['4'] = 2000


lock1 = 0
lock2 = 0
lock3 = 0

while True:
  
  location()
  velo()

  if (alt > apogee):
    apogee = alt
  #print("apogee",apogee)
  alt_diff= alt - apogee
  if (alt_diff < -5.0):
    flight_status = 0
  #print("flight_status",flight_status)
#kademe ayirma ,tirmanma ve stage kilidi dahil-diff araligi 30 metre
  if(stage_sep < alt < stage_sep+5.0 and stage_lock == 0 and flight_status == 1):
    stage_lock = 1
    #send egu signal
    egu_signal()

#drouge parasutu ilk ayirma-apogeenin %80  miktari ve dusus
  if (alt <= apogee * per_drouge and  flight_status == 0 and lock1 == 0):
    drouge_parasutu()
    lock1 = 1
  
  if (alt <= apogee * per_payload and  flight_status == 0 and lock2 == 0):
    payload()
    lock2 = 1

  if (alt <= apogee * per_main  and  flight_status == 0 and lock3 == 0):
    main_parasutu()
    lock3 = 1



