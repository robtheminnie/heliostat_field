import utime
import machine
import run_instructions
import uart
import imu_driver


    
def main():
    
    print("init uart")
    uart_interface = uart.uart_interface()
    
    pan_stepper.target = 20
    tilt_stepper.target = -20
    
    instruction_source = 0
    instruction = 0
    
    while True:
        utime.sleep(1)
                
        message = uart_interface.check_for_data()
        
        print(instruction_source)
        print(instruction)
        
        # run_instruction(message.instruction, message.data)
        
        get_imu_data()
        
    # end while

# end def


if __name__ == "__main__":
    main()
# end if
