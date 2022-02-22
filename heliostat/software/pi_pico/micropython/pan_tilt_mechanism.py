import enumerations
import stepper
from imu import MPU6050

# init pin assignemnt class for enumerations
pin_assignments = enumerations.pin_assignments()


class pan_tilt_mechanism:
  def __init__(self):
    
    # init steppers
    self.azimuth_stepper = stepper.stepper(pin_assignments.pan_coil_A, \
                              pin_assignments.pan_coil_B, \
                              pin_assignments.pan_coil_C, \
                              pin_assignments.pan_coil_D, \
                              pin_assignments.pan_min_stop, \
                              pin_assignments.pan_max_stop)

    self.inclination_stepper = stepper.stepper(pin_assignments.tilt_coil_A, \
                               pin_assignments.tilt_coil_B, \
                               pin_assignments.tilt_coil_C, \
                               pin_assignments.tilt_coil_D, \
                               pin_assignments.tilt_min_stop, \
                               pin_assignments.tilt_max_stop)
    
    # init imu
    self.imu = MPU6050(machine.I2C(pin_assignments.imu_i2c_port, sda=machine.Pin(pin_assignments.imu_sda), scl=machine.Pin(pin_assignments.imu_sdl), freq=400000))
    
    # set properties
    self.imu.accel_range(0)   # accel = +/- 2g
    self.imu.accel_filer_range(6)  # filter = 5Hz
    
    # azimuth and inclinatoin offset for tilted axis
    self.azimuth_offset = 0       # angle required to rotate pan axis to get til axis horizontal
    self.inclination_offset = 0   # angle required to rotate tilt axis to get mirror flat when tilt axis is horizontal

    
    def auto_home(self):
      # auto home both axis
      self.azimuth_stepper.auto_home()
      self.inclination_stepper.auto_home()
    # end def
    
      
    def find_end_points(self):
      # find end points of both axis
      self.azimuth_stepper.find_end_points()
      self.inclination_stepper.find_end_points()
    #end def
    
    
    def move_to_target(self, pan_angle, tilt_angle):
      self.azimuth_stepper.move_to_target_angle(pan_angle)
      self.inclination_stepper.move_to_target_angle(tilt_angle)
    # end def
    
    
    def auto_zero(self):
      # auto zero x,y axis to get mirror horizontal, allows for pan axis inclination determination
      self.azimuth_stepper.auto_home()
      self.inclination_stepper.auto_home()
      
      # store position
      self.azimuth_offset = self.imu.azimuth
      self.inclination_offset = self.imu.inclination
      
      # move to azimuth
      self.azimuth_stepper.move_to_target_angle(self.azimuth_offset)
      
      # move to inclination
      self.inclination_stepper.move_to_target_angle(self.inclination_offset)
      
    # end def
    
  # end def
  
#end class
