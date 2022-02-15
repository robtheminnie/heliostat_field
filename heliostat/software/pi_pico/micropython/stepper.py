import machine
import utime

class stepper:
    def __init__(self, A, B, C, D, stop_A, stop_B):
        self.coil_A = machine.Pin(A, machine.Pin.OUT) # pin that drives motor coil A
        self.coil_B = machine.Pin(B, machine.Pin.OUT) # pin that drives motor coil B
        self.coil_C = machine.Pin(C, machine.Pin.OUT) # pin that drives motor coil C
        self.coil_D = machine.Pin(D, machine.Pin.OUT) # pin that drives motor coil D
        self.actual = 0 # actual position
        self.target = 0 # taregt position
        self.state = 0  # current active state/ phase
        self.stop_A = machine.Pin(stop_A, machine.Pin.IN)  # start end stop switch
        self.stop_B = machine.Pin(stop_B, machine.Pin.IN)  # end end stop switch
        self.total_step_range = 0;  # number of steps between start end stop, and end end stop
        
        # set coil A high
        self.coil_A.value(1)
        
    def step_forward(self):
        if self.stop_B.value() != 1:
            # not against end stop
            if self.state == 0:
                self.coil_A.value(0)
                self.coil_B.value(1)
                self.state = 1
            elif self.state == 1:
                self.coil_B.value(0)
                self.coil_C.value(1)
                self.state = 2
            elif self.state == 2:
                self.coil_C.value(0)
                self.coil_D.value(1)
                self.state = 3
            elif self.state == 3:
                self.coil_D.value(0)
                self.coil_A.value(1)
                self.state = 0
            
            self.actual += 1
        
    
    def step_backward(self):
        if self.stop_A.value() != 1:
            # not against end stop
            if self.state == 0:
                self.coil_A.value(0)
                self.coil_D.value(1)
                self.state = 3
            elif self.state == 1:
                self.coil_B.value(0)
                self.coil_A.value(1)
                self.state = 0
            elif self.state == 2:
                self.coil_C.value(0)
                self.coil_B.value(1)
                self.state = 1
            elif self.state == 3:
                self.coil_D.value(0)
                self.coil_C.value(1)
                self.state = 2
            
            self.actual -= 1
        
        
    def move_to_target(self):
        # move to target will move to target in one call
        while self.actual != self.target:
            if self.actual < self.target:
                self.step_forward()
                utime.sleep(0.01)
        
            if self.actual > self.target:
                self.step_backward()
                utime.sleep(0.01)
                
    
    def increment_to_target(self):
        # incremenet to target will move to target one step per call until the target is reached
            if self.actual < self.target:
                self.step_forward()
        
            if self.actual > self.target:
                self.step_backward()
        
        
    def auto_home(self):
        # home to zero position
        
        # first move quick to end stop
        while self.stop_A.value() != 1:
            # step backward towards start end stop until end stop hit
            self.step_backward()
            
            # pause briefly
            utime.sleep(0.01)
        
        # end stop hit, set actual to 0
        self.actual = 0
        
        # move forward away from end stop
        self.target = 50
        self.move_to_target()
        
        # move towards end stop slowly
        while self.stop_A.value() != 1:
            # step backward towards start end stop until end stop hit
            self.step_backward()
            
            # pause briefly
            utime.sleep(0.1)
        
        # end stop hit, reset actual to more refined zero position
        self.actual = 0
        
        
    def find_end_points(self):
        # find steps between end points
        # first auto home to set 0 position
        self.auto_home()
        
        # step forward quickly until end stop hit
        while self.stop_B.value() != 1:
            self.step_forward()
            
            # short pause
            utime.sleep(0.01)
            
        # move away from end stop
        self.target = self.actual - 50
        self.move_to_target()
        
        
        # step forward slowly until end stop hit
        while self.stop_B.value() != 1:
            self.step_forward()
            
            # pause
            utime.sleep(0.1)
            
        # end stop hit, store range
        self.total_step_range = self.actual
        
        
        
            
            