import RPi.GPIO as GPIO
import time

# (c) IDWizard 2017 - https://github.com/IDWizard/uln2003
# (c) NNTin 2020
# MIT License.

LOW = 0
HIGH = 1
FULL_ROTATION = int(4075.7728395061727 / 8) # http://www.jangeox.be/2013/10/stepper-motor-28byj-48_25.html

HALF_STEP = [
    [LOW,  LOW,  LOW,  HIGH],
    [LOW,  LOW,  HIGH, HIGH],
    [LOW,  LOW,  HIGH, LOW ],
    [LOW,  HIGH, HIGH, LOW ],
    [LOW,  HIGH, LOW,  LOW ],
    [HIGH, HIGH, LOW,  LOW ],
    [HIGH, LOW,  LOW,  LOW ],
    [HIGH, LOW,  LOW,  HIGH],
]

FULL_STEP = [
    [HIGH, LOW,  HIGH, LOW ],
    [LOW,  HIGH, HIGH, LOW ],
    [LOW,  HIGH, LOW,  HIGH],
    [HIGH, LOW,  LOW,  HIGH]
]

class Command():
    """Tell a stepper to move X many steps in direction"""
    def __init__(self, stepper, steps, direction=1):
        self.stepper = stepper
        self.steps = steps
        self.direction = direction

class Driver():
    """Drive a set of motors, each with their own commands"""

    @staticmethod
    def run(commands):
        """Takes a list of commands and interleaves their step calls"""
        
        # Work out total steps to take
        max_steps = sum([c.steps for c in commands])

        count = 0
        while count < max_steps:
            for command in commands:
                # we want to interleave the commands
                if command.steps > 0:
                    command.stepper.step(1, command.direction)
                    command.steps -= 1
                    count += 1
        
class Stepper():
    def __init__(self, mode, pin1, pin2, pin3, pin4, delay=2):
        self.mode = mode
        self.pin1 = pin1
        self.pin2 = pin2
        self.pin3 = pin3
        self.pin4 = pin4
        self.delay = delay  # Recommend 10+ for FULL_STEP, 1 is OK for HALF_STEP
        
        # Initialize all to 0
        self.reset()
        
    def step(self, count, direction=1):
        """Rotate count steps. direction = -1 means backwards"""
        for x in range(count):
            for bit in self.mode[::direction]:
                GPIO.output(self.pin1, bit[0])
                GPIO.output(self.pin2, bit[1])
                GPIO.output(self.pin3, bit[2])
                GPIO.output(self.pin4, bit[3])
                time.sleep(self.delay/1000)
        self.reset()
        
    def reset(self):
        # Reset to 0, no holding, these are geared, you can't move them
        GPIO.output(self.pin1, 0)
        GPIO.output(self.pin2, 0)
        GPIO.output(self.pin3, 0)
        GPIO.output(self.pin4, 0)

if __name__ == '__main__':
    STEP1_IN1 = 4
    STEP1_IN2 = 17
    STEP1_IN3 = 27
    STEP1_IN4 = 22

    STEP2_IN1 = 14
    STEP2_IN2 = 15
    STEP2_IN3 = 18
    STEP2_IN4 = 23

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(STEP1_IN1, GPIO.OUT)
    GPIO.setup(STEP1_IN2, GPIO.OUT)
    GPIO.setup(STEP1_IN3, GPIO.OUT)
    GPIO.setup(STEP1_IN4, GPIO.OUT)
    GPIO.setup(STEP2_IN1, GPIO.OUT)
    GPIO.setup(STEP2_IN2, GPIO.OUT)
    GPIO.setup(STEP2_IN3, GPIO.OUT)
    GPIO.setup(STEP2_IN4, GPIO.OUT)
    

    s1 = Stepper(HALF_STEP, STEP1_IN1, STEP1_IN2, STEP1_IN3, STEP1_IN4, delay=1)
    s2 = Stepper(HALF_STEP, STEP2_IN1, STEP2_IN2, STEP2_IN3, STEP2_IN4, delay=1)
    s1.step(FULL_ROTATION)
    s2.step(FULL_ROTATION, direction=-1)

    #runner = Driver()
    #runner.run([Command(s1, FULL_ROTATION, 1), Command(s2, FULL_ROTATION, -1)])

    GPIO.cleanup()
