import datetime


def getMonth():
    return datetime.datetime.now().month

def getYear():
    return datetime.datetime.now().year

def validator(dataString: str):

    print("===>", len(dataString), dataString)
    if len(dataString.strip()) == 0:
        return False

    if dataString.strip()[:3] != "ATT":
        return False

    startDateString = f"{getYear()}-{getMonth()}-{1}"
    startMonthDate = datetime.datetime.strptime(startDateString, "%Y-%m-%d")

    today = datetime.datetime.today()
    
    differnce = (today - startMonthDate).days

    if len(dataString) >= differnce-1:
        return False

    for i in dataString[3:]:
        if i != "0" or i != "1":
            return False
        
    return True

    # currentDay = datetime.datetime.now().day
    # if currentDay == 1:
    #     if len(dataString) != 0:
    #         return False

    # if len(dataString) != currentDay-1:
