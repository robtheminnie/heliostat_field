import machine
import utime

class uart_interface:
    def __init__(self):
        # init uart ports
        self.uart_from_master = machine.UART(0, baudrate=19200)
        self.uart_to_slaves = machine.UART(1, baudrate=19200)
        self.rx_data_from_master = bytearray()
        self.rx_data_from_slaves = bytearray()
        self.tx_data_to_master = bytearray()
        self.tx_data_to_slaves = bytearray()
        self.new_data_from_master = 0
        self.new_data_from_slave = 0
        self.led = machine.Pin(25, machine.Pin.OUT)
        

    def check_for_data(self):
        print("checking for data")
        if self.uart_from_master.any() > 0:
            temp_buffer = bytearray()
            while self.uart_from_master.any() > 0:
                temp_buffer += self.uart_from_master.read(1)
            self.rx_data_from_master = temp_buffer
            self.rx_data_from_master[0] -= 1
            print("data from master")
            print(self.rx_data_from_master)
                
            if self.rx_data_from_master[0] == 0:
                # this is for me, do something
                print("this is for me")
                self.led.toggle()
                return self.rx_data_from_master[0], self.rx_data_from_master[2] 
            else:
                # this is not for me, pass it on
                print("forward from master")
                self.tx_data_to_slaves = self.rx_data_from_master
                self.uart_to_slaves.write(self.tx_data_to_slaves)
            
        if self.uart_to_slaves.any() > 0:
            temp_buffer = bytearray()
            while self.uart_to_slaves.any() > 0:
                temp_buffer += self.uart_to_slaves.read(1)
            self.rx_data_from_slaves = temp_buffer
            self.rx_data_from_slaves[0] -= 1
            print("data from slave")
            print(self.rx_data_from_slaves)
                    
                    
            if self.rx_data_from_slaves[0] == 0:
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
