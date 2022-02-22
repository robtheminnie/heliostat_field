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
      
      # check azimuth error
      # check inclination error
      # adjust azimuth
      # recheck inclination
      # adjust inclination
      # recheck azimuth
      # restart
      
      azimuth_result = step_state.step_successful
      inclination_result = step_state.step_successful
        
      # check azimuth error
      azimuth_error = self.imu.azimuth - azimuth_target

      if ((azimuth_error < 1) and (azimuth_error > -1)):
        azimuth_on_target = 1
      else:
        azimuth_on_target = 0
      #end if

      # check inclination error
      inclination_error = self.imu.inclination - inclination_target

      if ((inclination_error < 1) and (inclination_error > -1)):
        inclination_on_target = 1
      else:
        inclination_on_target = 0
      #end if
      
      azimuth_on_limit = 0
      inclination_on_limit = 0
      
      print("inclination error = ")
      print(inclination_error)
      
      print("azimuth error = ")
      print(azimuth_error)
      
      # for azimuth and inclination, try to work towards the target until we either hit the target of hit a limit switch
      while ((!azimuth_on_target and !azimuth_on_limit) or (!inclination_on_target and !inclination_on_limit)):
        
        # do several steps together
        steps = round(azimuth_error * 20, 0)
        
        for s in range(steps)
          if (azimuth_error > 0)
            azimuth_result = self.azimuth_stepper.step_forward()
            
            # check stop
            if (azimuth_result == step_state.max_stop_hit):
              azimuth_on_limit = 1
            else:
              azimuth_on_limit = 0
          #end if

          if (azimuth_error < 0)
            azimuth_result = self.azimuth_stepper.step_backward()
            
            # check stop
            if (azimuth_result == step_state.max_stop_hit):
              azimuth_on_limit = 1
            else:
              azimuth_on_limit = 0
          #end if
          
          utime.sleep(0.005)
        # end for
        
        # check inclination error
        inclination_error = self.imu.inclination - inclination_target
        
        if ((inclination_error < 1) and (inclination_error > -1)):
          inclination_on_target = 1
        else:
          inclination_on_target = 0
        #end if
        
        # do several steps together
        steps = round(inclination_error * 20, 0)
        
        for s in range(steps)
          if (inclination_error > 0)
            inclination_result = self.inclination_stepper.step_forward()
            
            # check stop
            if (inclination_result == step_state.max_stop_hit):
              inclination_on_limit = 1
            else:
              inclination_on_limit = 0
          #end if

          if (inclination_error < 0)
            inclination_result = self.inclination_stepper.step_backward()
            
            # check stop
            if (inclination_result == step_state.min_stop_hit):
              inclination_on_limit = 1
            else:
              inclination_on_limit = 0
          #end if
          
          utime.sleep(0.005)
        # end for

        # recheck azimuth errors
        azimuth_error = self.imu.azimuth - azimuth_target
        
        if ((azimuth_error < 1) and (azimuth_error > -1)):
          azimuth_on_target = 1
        else:
          azimuth_on_target = 0
        #end if
        
        print("inclination error = ")
        print(inclination_error)

        print("azimuth error = ")
        print(azimuth_error)
        
      # end while
      
    # end def
    
    def auto_zero(self):
      # auto zero x,y axis to get mirror horizontal, allows for pan axis inclination determination
      self.move_to_target(0, 0)
      
    # end def
    
  # end def
  
#end class
