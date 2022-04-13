# class to enumerate pin assignments
class pin_assignments:
  def __init__(self):
    
    # pan actuation
    self.spin_coil_A = 11
    self.spin_coil_B = 12
    self.spin_coil_C = 13
    self.spin_coil_D = 14
    self.spin_min_stop = 15
    self.spin_max_stop = 16


    #tilt actuation
    self.tilt_coil_A = 17
    self.tilt_coil_B = 18
    self.tilt_coil_C = 19
    self.tilt_coil_D = 20
    self.tilt_min_stop = 21
    self.tilt_max_stop = 22
    
    # ldr inputs
    self.tilt_up_ldr = 23
    self.tilt_down_ldr = 24
    self.spin_up_ldr = 25
    self.spin_down_ldr = 26
    
  #end def
#end class
