
# class to define instruciton IDs, used like a enumeration (bluh!)
class instruction_ID:
    def __init__(self):
        self.ndef = 0                           # does nothing
        self.get_ID = 1                         # get node ID
        self.auto_home = 2                      # auto home all axis
        self.find_end_points = 3                # find end points of all axis
        self.move_to_target = 4                 # move to target azimuth and inclination
        self.auto_zero = 5                      # auto zero, set position to 0 degrees azimuth, 0 degrees inclination, as per on board accelerometer
        self.store_target_location = 6          # store current azimuth and inclination values as location of target
        self.sun_location = 7                   # azimuth and inclination location of sun, relative to target
        self.calibrate_actuation = 8            # calibrate relationship between actuator steps and accelerometer movement
    #end def
    
#end class


# class to enumerate pin assignments
class pin_assignments:
  def __init__(self):
    # uart to master, uart 0
    self.uart_from_master_port = 0
    self.uart_from_master_TX = 0
    self.uart_from_master_RX = 1

    # uart to slaves, uart 1
    self.uart_to_slaves_port = 1
    self.uart_to_slaves_TX = 4
    self.uart_to_slaves_RX = 5


    # pan actuation
    self.pan_coil_A = 11
    self.pan_coil_B = 12
    self.pan_coil_C = 13
    self.pan_coil_D = 14
    self.pan_min_stop = 15
    self.pan_max_stop = 16


    #tilt actuation
    self.tilt_coil_A = 17
    self.tilt_coil_B = 18
    self.tilt_coil_C = 19
    self.tilt_coil_D = 20
    self.tilt_min_stop = 21
    self.tilt_max_stop = 22
    
    
    # i2c port for imu, i2c 0
    self.imu_i2c_port = 1
    self.imu_sda = 6
    self.imu_sdl = 7
    
  #end def
#end class
