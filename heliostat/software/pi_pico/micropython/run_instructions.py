
from enumerations
import uart
import pan_tilt_mechanism


# init instruction ID class for enumerations
instruction_ID = enumerations.instruction_ID()

pan_tilt_mechanism = pan_tilt_mechanism()

def run_instructions(instruction, data):
  
  #if instruction == instruction_ID.ndef:
    # do nothing, no instruction
    
    if instruction == instruction_ID.auto_home:
        print("running auto home")
        pan_tilt_mechanism.auto_home()

    elif instruction == instruction_ID.find_end_points:
        print("finding end points")
        pan_tilt_mechanism.find_end_points()

    elif instruction == instruction_ID.move_to_target:
        print("moving to target")
        # move axis to target positions
        pan_angle = ((data[0] << 8) | data[1]) / 100
        tilt_angle = ((data[2] << 8) | data[3]) / 100
        pan_tilt_mechanism.move_to_target(pan_angle, tilt_angle)

    elif instruction == instruction_ID.auto_zero:
        print("auto zero position")
        # auto zero x,y axis to get mirror horizontal, allows for pan axis inclination determination
        # auto home both axis
        pan_tilt_mechanism.auto_zero()
        
    elif instruciton == instruction_ID.store_target_location:
      print("storing target location")
      
    elif instruciton == instruction_ID.sun_location:
      print("new sun location received")
    
  #end if
  
#end def
