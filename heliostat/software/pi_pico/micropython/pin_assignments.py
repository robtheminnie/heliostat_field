

class pin_assignments(self):
  def __init__(self):
    # uart to master
    self.uart_to_master_TX = 0
    self.uart_to_master_RX = 1

    # uart to slaves
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
  #end def
#end class