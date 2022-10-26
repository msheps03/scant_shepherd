from stepper_class import *
import os
import numpy as np
from pathlib import Path
from dictionaries import *
# name, ID, limitSwitchType, homePos, maxAccel, maxVelocity, stepMode, current, maxPos, minPos, stepSize, scanStep, scanMin, scanMax


class ScannerController:
    def __init__(self):
        # using self limits scope of the stepper class to only being called within Scanner
        self.stepperX = StepperMotor(dictX) # init class stepperX
        self.stepperY = StepperMotor(dictY) # init class stepperY
        self.stepperZ = StepperMotor(dictZ) # init class stepperZ
        
        self.scanPos = [self.stepperX.scanPos, self.stepperY.scanPos, self.stepperZ.scanPos]
        
        self.imagesTaken = 0
        self.imagesToTake = sum([len(i) for i in self.scanPos])
        
        self.progress = self.getProgress()
        self.cam = None
        self.outputFolder = ''
        
    def deEnergise(self):
        self.stepperX.deEnergise()
        self.stepperY.deEnergise()
        self.stepperZ.deEnergise()
        return
    
    def resume(self): 
        self.stepperX.resume()
        self.stepperY.resume()
        self.stepperZ.resume()
        return
      
    def getProgress(self):
        return 100 * (self.images_taken / self.images_to_take)
        
    def initCam(self, cam):
        self.cam = cam
        
    def runScan(self, defaultX=0, defaultZ=0):
        for posX in self.scanPos[0]: # maybe make a dictionary for readability
            self.stepperX.moveToPosition(posX)
            for posY in self.scanPos[1]:
                self.stepperY.moveToPosition(posY + self.completedRotations * self.stepperY.maxPos)
                for posZ in self.scanPos[2]:
                    self.stepperZ.moveToPosition(posZ)
                    # to follow the naming convention when focus stacking
                    img_name = self.outputFolder + "x_" + "{:>6}".format(posX) + "_y_" + "{:>6}".format(posY) + "_step_" + "{:>6}".format(posZ) + "_.tif"

                    self.cam.capture_image(img_name=img_name)
                    self.progress = self.getProgress()

                self.completedStacks += 1

            self.completedRotations += 1

        # return to default position
        print("Returning to default position")
        self.stepperX.moveToPosition(pos=defaultX)
        self.stepperY.moveToPosition(pos=self.stepperY.completedRotations * self.stepperY.maxPos)
        self.stepperZ.moveToPosition(pos=-defaultZ)