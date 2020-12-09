from datetime import datetime, timedelta

class Utils:
    def GetJsonBody(_days, _postCode):
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
        return jsonRequest