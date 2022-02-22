import enumerations
import stepper
from imu import MPU6050

# init pin assignemnt class for enumerations
pin_assignments = enumerations.pin_assignments()

step_state = steppers.step_state()


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
    
    self.azimuth_target = 0
    self.inclination_target = 0
    
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
    
    
    def move_to_target(self, azimuth_target, inclination_target):
      # move to azimuth
      result = step_state.step_successful
      error = self.imu.azimuth - azimuth_target
      while ((error > 1) or (error < 1)) and ((result != step_state.min_stop_hit) and (result != step_state.max_stop_hit)):
        
        # do several steps together
        steps = round(error * 20, 0)
        
        for s in range(steps)
          if (error > 0)
            result = self.azimuth_stepper.step_forward()
          #end if

          if (error < 0)
            result = self.azimuth_stepper.step_backward()
          #end if
          
          utime.sleep(0.005)
        # end for

        # check error
        error = self.imu.azimuth - azimuth_target
      # end while
      
      # move to inclination
      result = step_state.step_successful
      error = self.imu.inclination - inclination_target
      while ((error > 1) or (error < 1)) and ((result != step_state.min_stop_hit) and (result != step_state.max_stop_hit)):
        
        # do several steps together
        steps = round(error * 20, 0)
        
        for s in range(steps)
          if (error > 0)
            result = self.inclination_stepper.step_forward()
          #end if

          if (error < 0)
            result = self.inclination_stepper.step_backward()
          #end if
          
          utime.sleep(0.005)
        # end for

        # check error
        error = self.imu.inclination - inclination_target
      # end while
      
    # end def
    
    def auto_zero(self):
      # auto zero x,y axis to get mirror horizontal, allows for pan axis inclination determination
      self.move_to_target(0, 0)
      
    # end def
    
  # end def
  
#end class
