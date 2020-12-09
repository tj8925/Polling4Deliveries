import requests
from datetime import datetime, timedelta
from pushbullet import Pushbullet
from Utils import Utils
import os

url = 'https://groceries.asda.com/api/v3/slot/view'

# Config Section - os.environ['xxx']
_days = int(os.environ['AdvDays'])
_postCode = os.environ['PostCode']
_maxPrice = float(os.environ['MaxPrice'])
_pbApiKey = os.environ['PbApiKey']

# Create array to hold avalible slot data
availableDateTimes = []
for postCode in _postCode.split(','):
    # POST request to API, using the required json data above
    postCode = postCode.strip()
    retVal = requests.post(url, json=Utils.GetJsonBody(_days, postCode))

    #loop though all slot days
    for dayData in retVal.json()['data']['slot_days']:
        #loop each slot for that day
        for slotData in dayData['slots']: 
            slot_info = slotData['slot_info']
            slot_start = slot_info['start_time']
            slot_price = slot_info['final_slot_price']
            slot_status = slot_info['status']
            # parse the start date as a date time object using the json formatted date time from the json T:Z
            pSlot_start = datetime.strptime(slot_start, '%Y-%m-%dT%H:%M:%SZ')
            if (slot_status == 'AVAILABLE' and slot_price <= _maxPrice):
                #convert start date into formatted date time
                sSlot_start = pSlot_start.strftime('%d-%m-%Y %H:%M:%S')
                availableDateTimes.append(('\n' if (len(availableDateTimes) > 0) else '') 
                + f'({postCode}) {sSlot_start} - £{slot_price:.2f}')

if (len(availableDateTimes) > 0):
    sList = f'{" ".join(availableDateTimes)}'
    pb = Pushbullet(_pbApiKey)
    print (sList)
    push = pb.push_note(f"Asda Checker", sList)
else:
    print('No slots at: ' + datetime.today().time().strftime('%H:%M:%S'))
