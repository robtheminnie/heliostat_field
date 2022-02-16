import machine
import utime

class step_state:
    def __init__(self):
        self.step_successful = 0
        self.target_hit = 1
        self.min_stop_hit = 2
        self.max_stop_hit = 3
    #end def
        

step_state = step_state()
        
class stepper:
    def __init__(self, A, B, C, D, min_end_stop, max_end_stop):
        # init class
        
        # init all coil pins
        self.coil_A = machine.Pin(A, machine.Pin.OUT) # pin that drives motor coil A
        self.coil_B = machine.Pin(B, machine.Pin.OUT) # pin that drives motor coil B
        self.coil_C = machine.Pin(C, machine.Pin.OUT) # pin that drives motor coil C
        self.coil_D = machine.Pin(D, machine.Pin.OUT) # pin that drives motor coil D
        
        # init target and actual position
        self.actual = 0 # actual position
        self.target = 0 # target position
        
        # init end stop pins
        self.min_stop = machine.Pin(min_end_stop, machine.Pin.IN)  # start end stop switch
        self.max_stop = machine.Pin(max_end_stop, machine.Pin.IN)  # end end stop switch
        
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
        if self.max_stop.value() != 1:
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
        if self.min_stop.value() != 1:
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
        
        
    def move_to_target(self):
        # move to target in one call
        result = step_state.target_hit
        while ((self.actual != self.target) and (result != step_state.min_stop_hit) and (result != step_state.max_stop_hit)):
            if self.actual < self.target:
                result = self.step_forward()
                utime.sleep(0.01)
            #end if
        
            if self.actual > self.target:
                result = self.step_backward()
                utime.sleep(0.01)
            #endif
        #end while
        
        return result # will return 1 if target hit, 0 if end stop hit
    # end def
                
    
    def increment_to_target(self):
        # incremenet to target will move to target one step per call until the target is reached
        result = step_state.target_hit
        if self.actual < self.target:
            result = self.step_forward()
        #end if
        
        if self.actual > self.target:
            result = self.step_backward()
        #end if
        
        return result # return result of step
    # end def
        
        
    def auto_home(self):
        # home to zero position
        
        # first move quick to min end stop
        result = step_state.step_successful
        while result != step_state.min_stop_hit:
            # step backward towards start end stop until end stop hit
            self.step_backward()
            
            # pause briefly
            utime.sleep(0.01)
        # end while
        
        # end stop hit, set actual to 0
        self.actual = 0
        
        # move forward away from end stop
        self.target = 50
        self.move_to_target()
        
        # move towards end stop slowly
        result = step_state.step_successful
        while result != step_state.min_stop_hit:
            # step backward towards start end stop until end stop hit
            result = self.step_backward()
            
            # pause briefly
            utime.sleep(0.1)
        # end while
        
        # hit end stop, set zero position
        self.actual = 0
    # end def
        
        
    def find_end_points(self):
        # find steps between end points
        # first auto home to set 0 position
        self.auto_home()
        
        # step forward quickly until end stop hit
        result = step_state.step_successful
        while result != step_state.max_stop_hit:
            result = self.step_forward()
            
            # short pause
            utime.sleep(0.01)
        # end while
            
        # move away from end stop
        self.target = self.actual - 50
        self.move_to_target()
        
        
        # step forward slowly until end stop hit
        result = step_state.step_successful
        while result != step_state.max_stop_hit:
            self.step_forward()
            
            # pause
            utime.sleep(0.1)
        # end while
            
        # hit end stop, store range
        self.total_step_range = self.actual
        
        # return to home position
        self.auto_home()
        
    # end def
        
        
            
            
