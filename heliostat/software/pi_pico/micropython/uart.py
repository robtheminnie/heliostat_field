import machine
import utime


class instruction_ID:
    def __init__(self):
    self.none = 0
    self.get_ID = 1
    self.auto_home = 2
    self.find_end_points = 3

instruction_ID = instruction_ID()
    

class uart_interface:
    def __init__(self):
        # init uart ports
        self.uart_from_master = machine.UART(0, baudrate=19200)
        self.uart_to_slaves = machine.UART(1, baudrate=19200)
        self.rx_data_from_master = bytearray()
        self.rx_data_from_slaves = bytearray()
        self.tx_data_to_master = bytearray()
        self.tx_data_to_slaves = bytearray()
        self.led = machine.Pin(25, machine.Pin.OUT)
        

    def check_for_data(self):
        print("checking for data")
        if self.uart_from_master.any() > 0:
            temp_buffer = bytearray()
            while self.uart_from_master.any() > 0:
                temp_buffer += self.uart_from_master.read(1)
            
            if len(temp_buffer) == 5:

                self.rx_data_from_master = temp_buffer
                self.rx_data_from_master[1] -= 1
                print("data from master")
                print(self.rx_data_from_master)
                    
                if self.rx_data_from_master[1] == 0:
                    # this is for me, do something
                    print("this is for me")
                    self.led.toggle()
                    return self.rx_data_from_master[0], self.rx_data_from_master[2]
                else:
                    # check if instruction is a get ID
                    if self.rx_data_from_master[2] == instruction_ID.get_ID:
                        # it is, increment destination by 1, this is my ID, then forward to next slave
                        self.rx_data_from_master[1] += 1
                        self.myID = self.rx_data_from_master[1]
                        
                    # this is not for me, pass it on
                    print("forward from master")
                    self.tx_data_to_slaves = self.rx_data_from_master
                    self.uart_to_slaves.write(self.tx_data_to_slaves)
            
    
        if self.uart_to_slaves.any() > 0:
            temp_buffer = bytearray()
            while self.uart_to_slaves.any() > 0:
                temp_buffer += self.uart_to_slaves.read(1)
            
            if len(temp_buffer) == 5:
                self.rx_data_from_slaves = temp_buffer
                self.rx_data_from_slaves[1] -= 1
                print("data from slave")
                print(self.rx_data_from_slaves)
                        
                        
                if self.rx_data_from_slaves[1] == 0:
                    # this is for me, do something
                    print("this is for me")
                    self.led.toggle()
                    return self.rx_data_from_slaves[0], self.rx_data_from_slaves[2]
                else:
                    # this is not for me, pass it on
                    print("forward to slave")
                    self.tx_data_to_master = self.rx_data_from_slaves
                    self.uart_from_master.write(self.tx_data_to_master)
                
        return 0, 0            
