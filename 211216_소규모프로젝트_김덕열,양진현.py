# import curses and GPIO
import curses
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

RIGHT_FORWARD = 6
RIGHT_BACKWARD = 5
RIGHT_PWM = 0
LEFT_FORWARD = 13
LEFT_BACKWARD = 19
LEFT_PWM = 26

SPEED = 35

# set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BCM)

GPIO.setup(RIGHT_FORWARD, GPIO.OUT)
GPIO.setup(RIGHT_BACKWARD, GPIO.OUT)
GPIO.setup(RIGHT_PWM, GPIO.OUT)

GPIO.output(RIGHT_PWM, 0)
RIGHT_MOTOR = GPIO.PWM(RIGHT_PWM, 100)
RIGHT_MOTOR.start(0)
RIGHT_MOTOR.ChangeDutyCycle(SPEED)

GPIO.setup(LEFT_BACKWARD, GPIO.OUT)
GPIO.setup(LEFT_FORWARD, GPIO.OUT)
GPIO.setup(LEFT_PWM, GPIO.OUT)

GPIO.output(LEFT_PWM, 0)
LEFT_MOTOR = GPIO.PWM(LEFT_PWM, 100)
LEFT_MOTOR.start(0)
LEFT_MOTOR.ChangeDutyCycle(SPEED)

# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

try:
    while True:
        char = screen.getch()
        if char == ord('q'):
            break
        elif char == 43:  # plus(+) key
            SPEED += 5
            if SPEED == 100:
                SPEED = 100
            RIGHT_MOTOR.ChangeDutyCycle(SPEED - 10)
            LEFT_MOTOR.ChangeDutyCycle(SPEED)
        elif char == 45:  # minus(-) key
            SPEED -= 5
            if SPEED == 0:
                SPEED = 0
            RIGHT_MOTOR.ChangeDutyCycle(SPEED - 10)
            LEFT_MOTOR.ChangeDutyCycle(SPEED)
        elif char == curses.KEY_UP:
            GPIO.output(RIGHT_BACKWARD, False)
            GPIO.output(RIGHT_FORWARD, True)
            GPIO.output(LEFT_BACKWARD, False)
            GPIO.output(LEFT_FORWARD, True)
        elif char == curses.KEY_DOWN:
            GPIO.output(RIGHT_BACKWARD, True)
            GPIO.output(RIGHT_FORWARD, False)
            GPIO.output(LEFT_BACKWARD, True)
            GPIO.output(LEFT_FORWARD, False)
        elif char == curses.KEY_LEFT:
            GPIO.output(RIGHT_BACKWARD, True)
            GPIO.output(RIGHT_FORWARD, False)
            GPIO.output(LEFT_BACKWARD, False)
            GPIO.output(LEFT_FORWARD, True)
        elif char == curses.KEY_RIGHT:
            GPIO.output(RIGHT_BACKWARD, False)
            GPIO.output(RIGHT_FORWARD, True)
            GPIO.output(LEFT_BACKWARD, True)
            GPIO.output(LEFT_FORWARD, False)
        elif char == 32:  # space bar
            GPIO.output(RIGHT_BACKWARD, False)
            GPIO.output(RIGHT_FORWARD, False)
            GPIO.output(LEFT_BACKWARD, False)
            GPIO.output(LEFT_FORWARD, False)
        elif char == 85 | char == 117:

            RIGHT_MOTOR.ChangeDutyCycle(60)
            LEFT_MOTOR.ChangeDutyCycle(70)
            GPIO.output(RIGHT_BACKWARD, False)
            GPIO.output(RIGHT_FORWARD, True)
            GPIO.output(LEFT_BACKWARD, True)
            GPIO.output(LEFT_FORWARD, False)


finally:
    # Close down curses properly, inc turn echo back on!
    curses.nocbreak();
    screen.keypad(0);
    curses.echo()
    curses.endwin()
    GPIO.cleanup()
