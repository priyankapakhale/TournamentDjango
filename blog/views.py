from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from blog.paytm import Checksum
from django.core import serializers
from .models import Tournament, Order, UserOrders, UserTournaments
from blog import ProfileHelper

@never_cache
@csrf_exempt
def addUserTournament(request):
    pass

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
    #respons_dict['CALLBACK_URL'] = 'https://securegw-stage.paytm.in/theia/paytmCallback?ORDER_ID='+req['ORDER_ID']
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
        x['tournament_id'] = item['pk']
        tournament_list.append(x)


    mydata = dict()
    mydata['tournament_list'] = tournament_list
    print(mydata)

    return HttpResponse(json.dumps(mydata), content_type='application/json')

@never_cache
@csrf_exempt
def addUserTournament(request):
    req = request.POST
    user_id = req['user_id']
    tournament_id = req['tournament_id']

    #check joined count
    query_set = Tournament.objects.get(id = tournament_id)
    json_data = serializers.serialize(query_set)
    data = json.loads(json_data)
    data = data[0]['fields']
    joined_count = data['joined_count']
    team_count = data['team_count']

    #if tournament not full, then increment joined count by 1
    if joined_count < team_count:
        joined_count += 1
        Tournament.objects.get(id = tournament_id).update(joined_count = joined_count)
        ProfileHelper.addUserTournament(user_id, tournament_id)
        return HttpResponse('done')
    #else return team full message
    else:
        return HttpResponse('tournament full')





@never_cache
@csrf_exempt
def getUserTournamentList(request):
    req = request.POST
    #user_id = req['user_id']
    user_id = 1

    query_set = UserTournaments.objects.filter(user = user_id)
    json_data = serializers.serialize('json', query_set)
    data = json.loads(json_data)

    tournament_list = list()
    print('data = ')
    print(data)
    for item in data:
        print(item)
        print(item['fields'])
        x = item['fields']
        tournament_id = x['tournament']
        print(tournament_id)
        query_set = Tournament.objects.filter(id = tournament_id)
        json_data = serializers.serialize('json',query_set)
        tournament = json.loads(json_data)

        print(tournament)
        x = tournament[0]['fields']
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

        x['tournament_id'] = tournament_id
        print(x)
        tournament_list.append(x)

    mydata = dict()
    mydata['tournament_list'] = tournament_list

    return HttpResponse(json.dumps(mydata), content_type='application/json')

