import requests
from datetime import datetime, timedelta
from pushbullet import Pushbullet
import os

url = 'https://groceries.asda.com/api/v3/slot/view'

# Config Section - os.environ['xxx']
_days = os.environ['AdvDays']
_postCode = os.environ['PostCode']
_maxPrice = os.environ['MaxPrice']
_pbApiKey = os.environ['PbApiKey']

startDate = datetime.today().date().strftime('%Y-%m-%dT%H:%M:%S')
endDate = (datetime.today().date() + timedelta(days=_days)).strftime('%Y-%m-%dT%H:%M:%S')

jsonRequest = {
                "requestorigin":"gi",
                "data":
                {
                    "start_date": startDate,
                    "end_date": endDate,
                    "service_info":
                    {
                        "fulfillment_type":"DELIVERY",
                        "enable_express":"false",
                        "is_unattended_slot":"false"
                    },
                        "reserved_slot_id":"",
                        "request_window":"P3D",
                        "service_address":
                    {
                        "postcode": _postCode,
                        #"latitude":"52.1336150",
                        #"longitude":"-2.3353446"
                    },
                    "customer_info":
                    {
                        "account_id":"18f4a1c3-2ef7-4792-b2d4-cf4a5c6defb7"
                    },
                    "order_info":
                    {
                        "order_id":"22636675648",
                        "parent_order_id":"",
                        "restricted_item_types":[],
                        "volume":0,
                        "weight":0,
                        "sub_total_amount":0,
                        "line_item_count":0,
                        "total_quantity":0
                    }
                }
            }


# POST request to API, using the required json data above
retVal = requests.post(url, json=jsonRequest)
# Create array to hold avalible slot data
availableDateTimes = []

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
        if (slot_status == 'AVAILABLE' and slot_price < _maxPrice):
            #print(slot_info)
            availableDateTimes.append(('\n' if (len(availableDateTimes) > 0) else '') 
            + pSlot_start.strftime('%d-%m-%Y %H:%M:%S') + ' - Now ' + slot_status.title() + f' at £{slot_price:.2f}')

if (len(availableDateTimes) > 0):
    sList = f'{" ".join(availableDateTimes)}'
    pb = Pushbullet(_pbApiKey)
    print (sList)
    push = pb.push_note("Asda Checker", sList)
else:
    print('No slots at: ' + datetime.today().time().strftime('%H:%M:%S'))
