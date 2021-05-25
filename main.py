# import system libraries
from subprocess import call
import json
import datetime
import time

# import cowin libaries
from cowin import CoWinAPI

# FIXME: Update this variable
pin_code = ""


def getDatesForaWeek():

    datee = datetime.date.today()
    datee = datee - datetime.timedelta(days=1)

    datesList = []
    for i in range(0, 7):
        datee = datee + datetime.timedelta(days=1)
        datesList.append(datee)

    return datesList


def getVaccineDataForaWeek(cowin, pincode):

    vaccineData = {}

    for date in getDatesForaWeek():
        temp = cowin.get_availability_by_pincode(
            pincode, date.strftime("%d-%m-%y"))
        if len(temp) == 0:
            print('No data available for {pincode} for {datee}')
            continue

        vaccineData[date] = temp['sessions']

    return vaccineData


def checkEmptyVaccineData(filteredVaccineData):

    for val in filteredVaccineData.values():
        if len(val) > 0:
            return False

    return True


def formatMessage(row):

    message = f'Date: {key}\n, Vaccine: {row["vaccine"]},\n\t Centre:{row["name"]},\n\t dose1:{row["available_capacity_dose1"]},\n\t dose2:{row["available_capacity_dose2"]},\n\t age:{row["min_age_limit"]}\n'

    return message


cowin = CoWinAPI()
prevVaccineData = {}

while True:
    print('='*10, f'Running {datetime.datetime.now()}')
    vaccineData = getVaccineDataForaWeek(cowin, pin_code)

    # Lets filter out the list
    filteredVaccineData = {}
    for key in vaccineData:
        lst = vaccineData[key]
        if len(lst) == 0:
            filteredVaccineData[key] = lst
            continue

        # filteredList = [row for row in lst if row['available_capacity']]
        filteredVaccineData[key] = [
            row for row in lst if row['available_capacity']]

    message = ""
    if checkEmptyVaccineData(filteredVaccineData):
        print('No vaccination available for next 7 days')
    else:
        for key in filteredVaccineData:
            for row in filteredVaccineData[key]:
                if key not in prevVaccineData:
                    message += formatMessage(row)
                elif row not in prevVaccineData[key]:
                    message += formatMessage(row)

    prevVaccineData = vaccineData
    if len(message) > 0:
        print(message)
        call(["telegram-send", message])

    print(f'Going to sleep 60 seconds')
    time.sleep(60)
