from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from blog.paytm import Checksum
from django.core import serializers
from .models import Tournament, Order

@never_cache
@csrf_exempt
def processOrder(request):
    req = request.POST
    amount = req['TXN_AMOUNT']

    # initialize a dictionary
    paytmParams = dict()


    MERCHANT_KEY = 'HJFvS_G&ppt9T5@_'
    # import cgi

    # form = cgi.FieldStorage()
    respons_dict = {}

    respons_dict['MID'] = 'dbcAUx53699294235269'  # Provided by Paytm
    respons_dict['ORDER_ID'] = req['ORDER_ID']  # unique OrderId for every request
    respons_dict['CUST_ID'] = req['CUST_ID']  # unique customer identifier
    respons_dict['INDUSTRY_TYPE_ID'] = 'Retail'  # Provided by Paytm
    respons_dict['CHANNEL_ID'] = 'WAP' # Provided by Paytm
    respons_dict['TXN_AMOUNT'] = amount  # transaction amount
    respons_dict['WEBSITE'] = 'WEBSTAGING'  # Provided by Paytm
    respons_dict['EMAIL'] = 'abc@gmail.com'  # customer email id
    respons_dict['MOBILE_NO'] = '7777777777'  # customer 10 digit mobile no.
    respons_dict['CALLBACK_URL'] = 'https://priyanka030493.pythonanywhere.com/handlePayment/'
    respons_dict['CALLBACK_URL'] = req['CALLBACK_URL']

    checksum = Checksum.generate_checksum(respons_dict, MERCHANT_KEY)

    # paramarr = {};

    # paramarr = respons_dict;

    respons_dict['CHECKSUMHASH'] = checksum

    print(respons_dict)
    url = "https://securegw-stage.paytm.in/order/process"

    # Generate checksum by parameters we have
    # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys

    return HttpResponse(json.dumps(respons_dict), content_type='application/json')

@never_cache
@csrf_exempt
def handlePayment(request):
    return HttpResponse('done')

@never_cache
@csrf_exempt
def getTournamentList(request):

    req = request.POST


    query_set = Tournament.objects.all()
    json_data = serializers.serialize('json', query_set)
    data = json.loads(json_data)

    tournament_list =list()
    for item in data:
        x = item['fields']
        if x['game_mode'] == 1:
            x['game_mode'] = 'SOLO'
        elif x['game_mode'] == 2:
            x['game_mode'] = 'DUO'
        else:
            x['game_mode'] = 'SQUAD'

        if x['platform'] == 1:
            x['platform'] = 'Mobile'
        elif x['platform'] == 2:
            x['platform'] = 'PC'
        elif x['platform'] == 3:
            x['platform'] = 'XBOX'
        else:
            x['platform'] = 'Playstation'
        tournament_list.append(x)


    mydata = dict()
    mydata['tournament_list'] = tournament_list
    print(mydata)

    return HttpResponse(json.dumps(mydata), content_type='application/json')


