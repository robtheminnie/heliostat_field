import uart
import stepper


## init instruction ID class for enumerations
instruction_ID = instruction_ID()


print("init steppers")
pan_stepper = stepper.stepper(11, 12, 13, 14, 15, 16)
tilt_stepper = stepper.stepper(17, 18, 19, 20, 21, 22)


def run_instructions(instruction, data):
  
  if instruction = instruction_ID.auto_home:
    # auto home both axis
    pan_stepper.auto_home()
    tilt_stepper.auto_home()
    
  elif instruction = instruction_ID.find_end_points:
    # find end points of both axis
    pan_stepper.find_end_points()
    tilt_stepper.find_end_points()
    
  elif instruction = instruction_ID.move_to_target:
    # move axis to target positions
    pan_stepper.move_to_target((data[0] << 8) | data[1])
    tilt_stepper.move_to_target((data[2] << 8) | data[3])
    
  #end if
  
#end def
