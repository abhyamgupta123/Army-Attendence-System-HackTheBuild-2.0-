import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


RF_obj = SimpleMFRC522()

def readCard():
    try:
            _id, text = RF_obj.read()
            # print(id)
            # print(text)
            return _id

    except Exception as e:
        print("error occured while reading card")
        print(e)
        return None

    finally:
            GPIO.cleanup()


def formatCard():
    try:
            RF_obj.write("ATT")
            return 1

    except Exception as e:
        print("error occured while reading card")
        print(e)
        return None

    finally:
            GPIO.cleanup()
