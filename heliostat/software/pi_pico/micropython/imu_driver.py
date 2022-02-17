from imu import MPU6050
import pin_assignments
import machine
import math

pin_assignments = pin_assignments.pin_assignment()


i2c = machine.I2C(pin_assignments.imu_i2c_port, sda=machine.Pin(pin_assignments.imu_sda), scl=machine.Pin(pin_assignments.imu_sdl), freq=400000)
imu = MPU6050(i2c)

theta = 0

def get_imu_data():
  
  #print(imu.accel.xyz,imu.gyro.xyz,imu.temperature,end='\r')

  ax=round(imu.accel.x,4)
  ay=round(imu.accel.y,4)
  az=round(imu.accel.z,4)
  tem=round(imu.temperature,2)
  
  theta = math.atan(math.sqrt((ax * ax) + (ay * ay)) / az) / (2 * 3.1415) * 360

  print(theta,"\t",tem,"        ",end="\r")
