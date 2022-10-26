class StepperMotor:
    def __init__(self, dictionary):
        self.name = dictionary['name']
        self.ID = str(dictionary['ID'])
        self.limitSwitchType = dictionary['limitSwitchType']
        self.homePos = dictionary['homePos']
        self.maxAccel = dictionary['maxAccel']
        self.maxVelocity = dictionary['maxVelocity']
        self.stepMode = dictionary['stepMode']
        self.current = dictionary['current']
        self.maxPos = dictionary['maxPos']
        self.minPos = dictionary['minPos']
        
        self.stepSize = dictionary['stepSize']
        self.position = None # Above line in question
        self.scanPosition = None # Difference between this and the above line
        self.completedRotations = 0 # Positions during scanning-- Y-Axis only
        self.completedStacks = 0 # positions during scanning-- Y-Axis only?
        self.scanPos = None
        
        self.scanStepSize = dictionary['stepSize']
        
        self.scanMin = dictionary['scanMin']
        self.scanMax = dictionary['scanMax']
        
        self.setScanRange()
        
        self.setStepMode()
        self.setCurrent()
        self.setMaxAccel()
        self.setMaxSpeed()
        self.getStepperPosition()
        
        '''
        Set stepper vals and get position
        ie send ticcmd commands
        '''
        
        '''
            At no point does this grab values from the UI, are the independent of the scan?
            If so, ideally add an option to UI for it
        '''


    def setScanRange(self):
        # set min and max poses according to input (within range)
        if self.scanMax > self.maxPos:  # this may be redundant, do once in the init. Or call seperate function to fix scanMax
            self.scanMax = self.maxPos
        elif self.scanMin < self.minPos:
            self.scanMin = self.minPos

        # set desired step size (limited by GUI inputs as well as min and max values)

        self.scanPos = [self.scanMin, self.scanMax,self.scanStepSize]  # may be unnecessary, exists to check against original code
        if len(self.scan_pos) == 0:  # if empty, try an if not self.scan_pos:
            print("INPUT ERROR FOUND!")
            self.scanPos = np.array([0])
        return

    def setMin(self, min):
        self.scanMin = min
        return

    def setMax(self, max):
        self.scanMax = max
        return

    def setStep(self, step):
        self.scanStepSize = step
        return

    def correctName(self, stepperPos):
        return "{:>6}".format(stepperPos)
        
    def setStepMode(self):
        os.system('ticcmd --step-mode ' + str(self.step_mode) + ' -d ' + self.ID)
        return

    def setCurrent(self):
        os.system('ticcmd --current ' + str(self.current) + ' -d ' + self.ID)
        return

    def setMaxAccel(selfl):
        os.system('ticcmd --max-accel ' + str(self.max_accel) + ' -d ' + self.ID)
        return

    def setMaxSpeed(self): 
        os.system('ticcmd --max-speed ' + str(self.max_velocity) + ' -d ' + self.ID)
        return
        
    def deEnergise(self): # sister function in scanner_class
        os.system('ticcmd --deenergize -d ' + self.ID)
        return
        
    def resume(self): # sister function in scanner_class
        os.system('ticcmd --resume --reset-command-timeout -d ' + self.ID)
        return
        
    def getSettings(self): # get settings stored on driver
        '''
        ticcmd --get-settings FILE
        (reads all settings from device to file)
        init class with this
        '''
        return

    def home(self):
        if self.homePos != 0: # if not homed
            print("Homing stepper", self.name)
            os.system('ticcmd --resume --position ' + str(self.homePos) + ' --reset-command-timeout -d ' + self.ID)

            while not self.getLimitState():
                os.system('ticcmd --resume --reset-command-timeout -d ' + self.ID
                # sleep(0.2)

        os.system('ticcmd --halt-and-set-position 0 -d ' + self.ID) # limit activated set position to 0
        return
    
    def getLimitState(self):
        info = os.popen('ticcmd --status -d ' + self.ID).read()
        # split returned results into its elements
        lines = info.split("\n")

        # what is going on here?
        if self.limitSwitchType == "fwd":
            state = lines[12].split(" ")[-1]
        elif self.limitSwitchType == "rev":
            state = lines[13].split(" ")[-1]
        else:
            print("Home direction is not defined for stepper:", self.name)
            return True

        if state == "Yes":
            print("Home reached for stepper:", self.name)
            return True
        else:
            return False
            
    def getStepperPosition(self):
        info = os.popen('ticcmd --status -d ' + self.ID).read()
        # split returned results into its elements
        lines = info.split("\n")
        current_position = int(lines[21].split(" ")[-1])
        self.position = current_position 
        return
        
    def moveToPosition(self, pos):
        # for axes that do not require limits
        pos = int(pos)
        if self.home is not None: 
            if pos > self.maxPos:
                pos = self.maxPos
            elif pos < self.minPos:
                pos = self.minPos

            # if pos is passed as string the above if statements may be flawed ie comparing str and int
 
            print("Moving stepper", self.name, "to position", pos)
        else:
            print("Moving stepper", self.name, "to position", pos)

        
        os.system('ticcmd --resume --position ' + str(pos) + ' --reset-command-timeout -d ' + self.ID)
        self.getStepperPosition()
        while self.position != pos:
            os.system('ticcmd --resume --position ' + str(pos) + ' --reset-command-timeout -d ' + self.ID)
            self.getStepperPosition()
        return
        
    