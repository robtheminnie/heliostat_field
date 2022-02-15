import machine

class stepper:
    def __init__(self, A, B, C, D, stop_A, stop_B):
        self.coil_A = machine.Pin(A, machine.Pin.OUT)
        self.coil_B = machine.Pin(B, machine.Pin.OUT)
        self.coil_C = machine.Pin(C, machine.Pin.OUT)
        self.coil_D = machine.Pin(D, machine.Pin.OUT)
        self.actual = 0
        self.target = 0
        self.state = 0
        self.stop_A = machine.Pin(stop_A, machine.Pin.IN)
        self.stop_B = machine.Pin(stop_B, machine.Pin.IN)
        
        # set coil A high
        self.coil_A.value(1)
        
    def step_forward(self):
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
        
            if self.actual > self.target:
                self.step_backward()
                
    
    def increment_to_target(self):
        # incremenet to target will move to target one step per call until the target is reached
            if self.actual < self.target:
                self.step_forward()
        
            if self.actual > self.target:
                self.step_backward()
            
            