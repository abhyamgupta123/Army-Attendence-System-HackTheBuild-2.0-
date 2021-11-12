from typing import Optional, Union
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


def writeData(attendenceString: str) -> Optional[Union[int, None]]:

    writer = SimpleMFRC522()
    try:
            text = input('New data:')
            print("Place your tag to mark attendence")
            reader.write(text)
            print("Written")
            return 1

    except Exception as e:
        print("error occured while reading card")
        print(e)
        return None

    finally:
            GPIO.cleanup()

