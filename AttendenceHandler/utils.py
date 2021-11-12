from typing import Optional, Union
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import datetime


RF_obj = SimpleMFRC522()

def writeData(attendenceString: str) -> Optional[Union[int, None]]:

    try:
            # text = input('New data:')
            print("Place your tag to mark attendence")
            RF_obj.write(attendenceString.strip())
            print("Attendence Marked Sucessfully.")
            return 1

    except Exception as e:
        print("error occured while reading card")
        print(e)
        return None

    finally:
            GPIO.cleanup()

def readCardData() -> Optional[Union[str, None]]:
    try:
            _id, text = RF_obj.read()
            print(id)
            print(len(text))
            return text.strip()
            
    except Exception as e:
        print("error occured while reading card")
        print(e)
        return None

    finally:
            GPIO.cleanup()


def getMonth():
    return str(datetime.datetime.now().month)

def getYear():
    return str(datetime.datetime.now().year)


def markAttendence(dataString: str) -> str:

    dataString = dataString.strip()

    startDateString = f"{getYear()}-{getMonth()}-{1}"
    startMonthDate = datetime.datetime.strptime(startDateString, "%Y-%m-%d")

    today = datetime.datetime.today()
    
    difference = int((today - startMonthDate).days)

    print("===>", difference, today, startMonthDate)
    if (len(dataString) - 3) <= difference:
        len_diff = difference - len(dataString) - 3 
        
        dataString += "0" * len_diff

    else:
        return None

    dataString += "1"

    return dataString.strip()

