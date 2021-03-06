import machine
import utime
import enumerations



# init pin_assignment class for enumerations
pin_assignments = enumerations.pin_assignments()

class step_state:
    def __init__(self):
        self.step_successful = 0
        self.target_hit = 1
        self.min_stop_hit = 2
        self.max_stop_hit = 3
    #end def
    

step_state = step_state()


class stop_state:
    def __init__(self):
        self.hit = 0
        self.not_hit = 1
        
stop_state = stop_state()    

class stepper:
    def __init__(self, A, B, C, D, min_end_stop, max_end_stop):
        # init class
        
        # init all coil pins
        self.coil_A = machine.Pin(A, machine.Pin.OUT) # pin that drives motor coil A
        self.coil_B = machine.Pin(B, machine.Pin.OUT) # pin that drives motor coil B
        self.coil_C = machine.Pin(C, machine.Pin.OUT) # pin that drives motor coil C
        self.coil_D = machine.Pin(D, machine.Pin.OUT) # pin that drives motor coil D
        
        
        # stepper is 64 step per rotation with gear ratio
        # 32/9, 22/11, 26/9, 31/10
        # results in 0.08832 degrees output shaft rotation per step
        self.steps_per_rotation = (64 * (32 * 22 * 26 * 31) / (9 * 11 * 9 * 10))
        
        # init target and actual position
        self.actual_step_position = 0 # actual position in motor steps
        self.target_step_position = 0 # target position in motor steps
        
        self.actual_angle_position = 0 # actual position in motor angle
        self.target_angle_position = 0 # target position in motor angle
        
        # init end stop pins, end stops switch to ground, 0 = end stop hit, 1 = end stop not hit
        self.min_stop = machine.Pin(min_end_stop, machine.Pin.IN, machine.Pin.PULL_UP)  # start end stop switch, switch connected to pin and ground
        self.max_stop = machine.Pin(max_end_stop, machine.Pin.IN, machine.Pin.PULL_UP)  # end end stop switch, switch connected to pin and ground
        
        # init total step range
        self.total_step_range = 0;  # number of steps between start end stop, and end end stop
        
        # set current state to 0
        self.set_state_0()
    # end def
  
        
# states:
    # 0, A
    # 1, A+B
    # 2, B
    # 3, B+C
    # 4, C
    # 5, C+D
    # 6, D
    # 7, D+A
    
    def set_state_0(self):
        self.coil_A.value(1)
        self.coil_B.value(0)
        self.coil_C.value(0)
        self.coil_D.value(0)
        self.state = 0
    # end def
        
        
    def set_state_1(self):
        self.coil_A.value(1)
        self.coil_B.value(1)
        self.coil_C.value(0)
        self.coil_D.value(0)
        self.state = 1
    # end def
        
        
    def set_state_2(self):
        self.coil_A.value(0)
        self.coil_B.value(1)
        self.coil_C.value(0)
        self.coil_D.value(0)
        self.state = 2
    # end def
        
        
    def set_state_3(self):
        self.coil_A.value(0)
        self.coil_B.value(1)
        self.coil_C.value(1)
        self.coil_D.value(0)
        self.state = 3
    # end def
        
        
    def set_state_4(self):
        self.coil_A.value(0)
        self.coil_B.value(0)
        self.coil_C.value(1)
        self.coil_D.value(0)
        self.state = 4
    # end def
        
        
    def set_state_5(self):
        self.coil_A.value(0)
        self.coil_B.value(0)
        self.coil_C.value(1)
        self.coil_D.value(1)
        self.state = 5
    # end def
        
        
    def set_state_6(self):
        self.coil_A.value(0)
        self.coil_B.value(0)
        self.coil_C.value(0)
        self.coil_D.value(1)
        self.state = 6
    # end def
        
        
    def set_state_7(self):
        self.coil_A.value(1)
        self.coil_B.value(0)
        self.coil_C.value(0)
        self.coil_D.value(1)
        self.state = 7
    # end def
        
        
    def step_forward(self):
        # step forward only in end stop not hit
        if self.check_max_stop() == stop_state.not_hit:
            # not against end stop
            if self.state == 0:
                self.set_state_1()
            elif self.state == 1:
                self.set_state_2()
            elif self.state == 2:
                self.set_state_3()
            elif self.state == 3:
                self.set_state_4()
            elif self.state == 4:
                self.set_state_5()
            elif self.state == 5:
                self.set_state_6()
            elif self.state == 6:
                self.set_state_7()
            elif self.state == 7:
                self.set_state_0()
            #end if
                
            self.actual += 1
            
            return step_state.step_successful # step complete
        else:
            return step_state.max_stop_hit # step not complete, end stop hit
        #end if
    # end def
        
    
    def step_backward(self):
        # step backward only if end stop not hit
        if self.check_min_stop() == stop_state.not_hit:
            # not against end stop
            if self.state == 0:
                self.set_state_7()
            elif self.state == 1:
                self.set_state_0()
            elif self.state == 2:
                self.set_state_1()
            elif self.state == 3:
                self.set_state_2()
            elif self.state == 4:
                self.set_state_3()
            elif self.state == 5:
                self.set_state_4()
            elif self.state == 6:
                self.set_state_5()
            elif self.state == 7:
                self.set_state_6()
            #end if
            
            self.actual -= 1
            
            return step_state.step_successful # step complete
        else:
            return step_state.min_stop_hit # step not complete, end stop hit
        #end if
    # end def
    
    
    def check_min_stop(self):
        return self.min_stop.value()
    # end def
    
    
    def check_max_stop(self):
        return self.max_stop.value()
    # end def
        
        
