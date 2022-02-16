import stepper
import pin_assignment


# init instruction ID class for enumerations
instruction_ID = instruction_ID()

# init pin assignemnt class for enumerations
pin_assignemnt = pin assignemnt()

print("init steppers")
pan_stepper = stepper.stepper(pin_assignment.pan_coil_A, \
                              pin_assignment.pan_coil_B, \
                              pin_assignment.pan_coil_C, \
                              pin_assignment.pan_coil_D, \
                              pin_assignment.pan_min_stop, \ 
                              pin_assignment.pan_max_stop)

tilt_stepper = stepper.stepper(pin_assignment.tilt_coil_A, \
                               pin_assignment.tilt_coil_B, \
                               pin_assignment.tilt_coil_C, \
                               pin_assignment.tilt_coil_D, \
                               pin_assignment.tilt_min_stop, \
                               pin_assignment.tilt_max_stop)


def run_instructions(instruction, data):
  
  if instruction = instruction_ID.ndef:
    # do nothing, no instruction
    
  elif instruction = instruction_ID.auto_home:
    print("running auto home")
    # auto home both axis
    pan_stepper.auto_home()
    tilt_stepper.auto_home()
    
  elif instruction = instruction_ID.find_end_points:
    print("finding end points")
    # find end points of both axis
    pan_stepper.find_end_points()
    tilt_stepper.find_end_points()
    
  elif instruction = instruction_ID.move_to_target:
    print("moving to target")
    # move axis to target positions
    pan_stepper.move_to_target((data[0] << 8) | data[1])
    tilt_stepper.move_to_target((data[2] << 8) | data[3])
  
  elif instruction = instruction_ID.auto_zero:
    print("auto zero position")
    # auto zero x,y axis to get mirror horizontal, allows for detemrining pan axis inclination
    
  #end if
  
#end def
