from django.shortcuts import render
from blog.paytm import Checksum, generateChecksum, verifyChecksum


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


