from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from blog.paytm import Checksum

@never_cache
@csrf_exempt
def processOrder(request):
    req = request.POST
    order_id = 1
    customer_id = 10
    email = "priyanka.pakhale54@gmail.com"
    mobile_no = "7777777777"

    # initialize a dictionary
    paytmParams = dict()

    # put checksum parameters in Dictionary
    paytmParams["MID"] = "dbcAUx53699294235269"
    paytmParams["ORDERID"] = order_id

    # Generate checksum by parameters we have
    # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
    checksum = Checksum.generate_checksum(paytmParams, "HJFvS_G&ppt9T5@_")
    return HttpResponse(json.dumps("Done"), content_type='application/json')

