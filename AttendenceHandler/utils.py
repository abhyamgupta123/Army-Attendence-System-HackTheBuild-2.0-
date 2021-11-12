from typing import Optional, Union
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import datetime
from calendar import monthrange


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
            return text.strip(), _id
            
    except Exception as e:
        print("error occured while reading card")
        print(e)
        return None, None

    finally:
            GPIO.cleanup()

def verifyCard() -> Optional[Union[int, None]]:
    try:
            _id, text = RF_obj.read()
            # print(id)
            # print(text)
            return _id, text

    except Exception as e:
        print("error occured while reading card")
        print(e)
        return None, None

    finally:
            GPIO.cleanup()


def getMonth():
    return str(datetime.datetime.now().month)

def getYear():
    return str(datetime.datetime.now().year)


def markAttendence(dataString: str) -> str:

    dataString = dataString.strip()[3:]

    # startDateString = f"{getYear()}-{getMonth()}-{1}"
    # startMonthDate = datetime.datetime.strptime(startDateString, "%Y-%m-%d")

    total_days = monthrange(int(getYear()), int(getMonth()))[1]
    days = {}

    for i in range(1, total_days+1):
        days[i] = "0"

    for j in range(1, len(dataString)+1):
        days[j] = dataString[j-1]

    today = datetime.datetime.today().day

    # marking attendence
    days[today] = "1"

    ans = ""

    for i in range(1, total_days+1):
        ans += days[i]

    ans = "ATT" + ans
    print(ans, days, today)

    # difference = int((today - startMonthDate).days)

    # print("===>", difference, today, startMonthDate)
    # if (len(dataString) - 3) <= difference:
    #     len_diff = difference - len(dataString) - 3 
        
    #     dataString += "0" * len_diff
    #     print("===> place 1", dataString, len_diff)

    # else:
    #     return None

    # dataString += "1"

    # print("===> place 2", dataString)

    return ans.strip()

def getAttendenceFromString(dataString: str):

    dataString = dataString.strip()[3:]

    total_days = monthrange(int(getYear()), int(getMonth()))[1]
    days = {}

    for i in range(1, total_days+1):
        days[i] = "0"

    for j in range(1, len(dataString)+1):
        days[j] = dataString[j-1]

    return days
        
