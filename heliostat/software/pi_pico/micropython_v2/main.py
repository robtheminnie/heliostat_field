import machine
import enumerations
import stepper


# init steppers
spin_stepper = stepper.stepper(pin_assignments.spin_coil_A, \
                              pin_assignments.spin_coil_B, \
                              pin_assignments.spin_coil_C, \
                              pin_assignments.spin_coil_D, \
                              pin_assignments.spin_min_stop, \
                              pin_assignments.spin_max_stop)

tilt_stepper = stepper.stepper(pin_assignments.tilt_coil_A, \
                               pin_assignments.tilt_coil_B, \
                               pin_assignments.tilt_coil_C, \
                               pin_assignments.tilt_coil_D, \
                               pin_assignments.tilt_min_stop, \
                               pin_assignments.tilt_max_stop)


ldr_tilt_up = machine.Pin(pin_assignments.tilt_up_ldr, machine.Pin.OUT)
ldr_tilt_down = machine.Pin(pin_assignments.tilt_down_ldr, machine.Pin.OUT)
ldr_spin_up = machine.Pin(pin_assignments.spin_up_ldr, machine.Pin.OUT)
ldr_spin_down = machine.Pin(pin_assignments.spin_down_ldr, machine.Pin.OUT)

def main():
    
  while True:
    
    if (ldr_tilt_up.value() == 1):
      tilt_stepper.step_forward()
      
    if (ldr_tilt_down.value() == 1):
      tilt_stepper.step_backward()
    
    if (ldr_spin_up.value() == 1):
      spin_stepper.step_forward()
      
    if (ldr_spin_down.value() == 1):
      spin_stepper.step_backward()
    
    utime.sleep(1)
            
  # end while

# end def


if __name__ == "__main__":
    main()
# end if
