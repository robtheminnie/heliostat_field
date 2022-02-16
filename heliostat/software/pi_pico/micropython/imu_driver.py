from imu import MPU6050
import pin_assignments
import machine


i2c = machine.I2C(pin_assignments.imu_i2c_port, sda=machine.Pin(pin_assignments.imu_sda), scl=machine.Pin(pin_assignments.imu_sdl), freq=400000)
imu = MPU6050(i2c)


def get_imu_data():
  
  #print(imu.accel.xyz,imu.gyro.xyz,imu.temperature,end='\r')

  ax=round(imu.accel.x,2)
  ay=round(imu.accel.y,2)
  az=round(imu.accel.z,2)
  tem=round(imu.temperature,2)

  print(ax,"\t",ay,"\t",az,"\t",tem,"        ",end="\r")
