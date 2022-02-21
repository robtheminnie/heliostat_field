import stepper
from enumerations
import uart
from imu import MPU6050
import machine


# init instruction ID class for enumerations
instruction_ID = enumerations.instruction_ID()

# init pin assignemnt class for enumerations
pin_assignments = enumerations.pin_assignments()


print("init steppers")
pan_stepper = stepper.stepper(pin_assignments.pan_coil_A, \
                              pin_assignments.pan_coil_B, \
                              pin_assignments.pan_coil_C, \
                              pin_assignments.pan_coil_D, \
                              pin_assignments.pan_min_stop, \
                              pin_assignments.pan_max_stop)

tilt_stepper = stepper.stepper(pin_assignments.tilt_coil_A, \
                               pin_assignments.tilt_coil_B, \
                               pin_assignments.tilt_coil_C, \
                               pin_assignments.tilt_coil_D, \
                               pin_assignments.tilt_min_stop, \
                               pin_assignments.tilt_max_stop)

print("init MPU6050")
i2c = machine.I2C(pin_assignments.imu_i2c_port, sda=machine.Pin(pin_assignments.imu_sda), scl=machine.Pin(pin_assignments.imu_sdl), freq=400000)
imu = MPU6050(i2c)


def run_instructions(instruction, data):
  
  #if instruction == instruction_ID.ndef:
    # do nothing, no instruction
    
    if instruction == instruction_ID.auto_home:
        print("running auto home")
        # auto home both axis
        pan_stepper.auto_home()
        tilt_stepper.auto_home()

    elif instruction == instruction_ID.find_end_points:
        print("finding end points")
        # find end points of both axis
        pan_stepper.find_end_points()
        tilt_stepper.find_end_points()

    elif instruction == instruction_ID.move_to_target:
        print("moving to target")
        # move axis to target positions
        pan_angle = ((data[0] << 8) | data[1]) / 100
        tilt_angle = ((data[2] << 8) | data[3]) / 100
        pan_stepper.move_to_target_angle(pan_angle)
        tilt_stepper.move_to_target_angle(tilt_angle)

    elif instruction == instruction_ID.auto_zero:
        print("auto zero position")
        # auto zero x,y axis to get mirror horizontal, allows for pan axis inclination determination
        # auto home both axis
        pan_stepper.auto_home()
        tilt_stepper.auto_home()
    
    
  #end if
  
#end def
