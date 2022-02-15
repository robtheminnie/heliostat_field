import machine
import utime


class instruction_ID:
    def __init__(self):
    self.none = 0
    self.get_ID = 1
    self.auto_home = 2
    self.find_end_points = 3

instruction_ID = instruction_ID()

# When data is transmitted from master camera down the chain, the master sets the source as 0, and the destination to the desired slave ID.
# Each slave decrements the destination ID.
# Once the ID is 0, the message has reached it's destination
# When data is sent from a slave up the chain towards the master camera, the destination is set by originator, and the source is set to 0
# As the message moves up the chain, to the master camera, each slave will incrmenet the source ID
# Once the message has reached the master camera, the source will contian the correct ID
    

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
    # end def
        

    def check_for_data(self):
        print("checking for data")
        
        # check if data from master
        if self.uart_from_master.any() > 0:
            temp_buffer = bytearray()
            
            # read data from master into temp buffer
            while self.uart_from_master.any() > 0:
                temp_buffer += self.uart_from_master.read(1)
            # end while
            
            if len(temp_buffer) == 5:
                # buffer is correct length
                
                # copy data ready to transmit onwards
                self.rx_data_from_master = temp_buffer
                
                # decrement destination ID
                self.rx_data_from_master[1] -= 1
                
                print("data from master")
                print(self.rx_data_from_master)
                
                
                if self.rx_data_from_master[1] == 0:
                    # destination ID is 0, this must be for me!
                    print("this is for me")
                    self.led.toggle()
                    return self.rx_data_from_master[0], self.rx_data_from_master[2]
                else:
                    # not for me
                    
                    # check if instruction is a get ID
                    if self.rx_data_from_master[2] == instruction_ID.get_ID:
                        # it is, increment destination by 1, this is my ID, then forward to next slave
                        self.rx_data_from_master[1] += 1
                        self.myID = self.rx_data_from_master[1]
                    #end if
                        
                    # this is not for me, pass it on
                    print("forward from master")
                    self.tx_data_to_slaves = self.rx_data_from_master
                    self.uart_to_slaves.write(self.tx_data_to_slaves)
                #end if
            
    
        # check if any data form slaves
        if self.uart_to_slaves.any() > 0:
            temp_buffer = bytearray()
            
            # read data to temp buffer
            while self.uart_to_slaves.any() > 0:
                temp_buffer += self.uart_to_slaves.read(1)
            # end while
            
            # check buffer length is correct
            if len(temp_buffer) == 5:
                # copy buffer ready to transmit onwards
                self.rx_data_from_slaves = temp_buffer
                
                print("data from slave")
                print(self.rx_data_from_slaves)
                
            #end if
                
                # data always heading to master camera, increment source ID, then pass it on
                self.rx_data_from_slaves[0] += 1
                
                print("forward to master")
                
                # copy and send data
                self.tx_data_to_master = self.rx_data_from_slaves
                self.uart_from_master.write(self.tx_data_to_master)

            #end if
        #end if
                
        return 0, 0
    #end def
