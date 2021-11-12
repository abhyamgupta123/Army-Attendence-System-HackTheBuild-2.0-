import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


def readCard():
    reader = SimpleMFRC522()
    try:
            id, text = reader.read()
            # print(id)
            # print(text)
            return id
    except Exception as e:
        print("error occured while reading card")
        print(e)
        return None

    finally:
            GPIO.cleanup()