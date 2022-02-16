import machine
import utime


# class to define instruciton IDs, used like a enumeration (bluh!)
class instruction_ID:
    def __init__(self):
        self.ndef = 0
        self.get_ID = 1
        self.auto_home = 2
        self.find_end_points = 3

instruction_ID = instruction_ID()


# class to define uart message structure
class uart_message:
    def __init__(self):
        self.source = bytearray([0])
        self.destination = bytearray([0])
        self.instruction_ID = bytearray([0])
        self.data = bytearray([0, 0])
        self.raw = bytearray([0, 0, 0, 0, 0])
    #end def
        
    def struct_to_raw(self):
        # convert structured data to raw byte array
        self.raw = self.source + self.destination + self.inctruction_ID + self.data
    #end def
        
    def raw_to_struct(self):
        # convert raw data to structured data
        self.source = self.raw[0]
        self.destination = self.raw[1]
        self.instruction_ID = self.raw[2]
        self.data = self.raw[3:5]
    #end def
    
    def fill_raw(self, raw):
        self.raw = raw
        self.raw_to_struct()
    #end def
    
    def fill_struct(self, source, destination, instruction, data):
        self.source = source
        self.destination = destination
        self.instruction = instruction
        self.data = data
        self.struct_to_raw
    #end def
        
#end class
     
uart_message = uart_message()
        

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
        self.led = machine.Pin(25, machine.Pin.OUT)
    # end def
    
    
    def send_down_chain(self, message):
        # this sends the message down chain, away from master
        self.uart_to_slaves.write(message.raw)
    #end def
    
    
    def send_up_chain(self, message):
        # this sends the message up chain, towards master
        self.uart_from_master.write(message.raw)
    #end def

    
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
                uart_message.fill_raw(temp_buffer)
                
                # decrement destination ID
                uart_message.destination_ID -= 1
                
                print("data from master")
                print(uart_message)
                
                
                if uart_message.destination == 0:
                    # destination ID is 0, this must be for me!
                    print("this is for me")
                    self.led.toggle()
                    return uart_message
                else:
                    # not for me
                    
                    # check if instruction is a get ID
                    if uart_message.instruction_ID == instruction_ID.get_ID:
                        # it is, increment destination by 1, this is my ID, then forward to next slave
                        uart_message.destination += 1
                        self.myID = uart_message.destination
                    #end if
                        
                    # this is not for me, pass it on
                    print("forward from master")
                    uart_message.struct_to_raw()
                    self.send_down_chain(uart_message.raw)
                #end if
            
    
        # check if any data from slaves
        if self.uart_to_slaves.any() > 0:
            temp_buffer = bytearray()
            
            # read data to temp buffer
            while self.uart_to_slaves.any() > 0:
                temp_buffer += self.uart_to_slaves.read(1)
            # end while
            
            # check buffer length is correct
            if len(temp_buffer) == 5:
                # copy buffer ready to transmit onwards
                uart_message.fill_raw(temp_buffer)
                
                print("data from slave")
                print(uart_message)
                
            #end if
                
                # data always heading to master camera, increment source ID, then pass it on
                uart_message.source += 1
                
                print("forward to master")
                
                # pack and send data
                uart_message.struct_to_raw()
                self.send_up_chain(uart_message.raw)

            #end if
        #end if
                
        return 0, 0
    
    #end def
        
#end class
