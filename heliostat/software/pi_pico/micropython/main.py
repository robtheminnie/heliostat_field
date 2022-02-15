import utime
import machine
import stepper
import uart

def main():
    
    print("init steppers")
    pan_stepper = stepper.stepper(11, 12, 13, 14, 15, 16)
    tilt_stepper = stepper.stepper(17, 18, 19, 20, 21, 22)
    
    print("init uart")
    uart_interface = uart.uart_interface()
    
    pan_stepper.target = 20
    tilt_stepper.target = -20
    
    instruction_source = 0
    instruction = 0
    
    while True:
        utime.sleep(0.1)
        
        print(pan_stepper.actual)
        print(tilt_stepper.actual)
        
        pan_stepper.increment_to_target()
        tilt_stepper.increment_to_target()
        
        instruction_source, instruction = uart_interface.check_for_data()
    
if __name__ == "__main__":
    main()