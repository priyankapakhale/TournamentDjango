from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from blog.paytm import Checksum
from django.core import serializers
from .models import Tournament, Order, UserOrders, UserTournaments, User, Profile
from blog import ProfileHelper
from django.utils import timezone

@never_cache
@csrf_exempt
def addUser(request):
    req = request.POST
    email = req['email']
    password = req['password']
    name = req['name']

    #ProfileHelper.addUser(email, password, name)
    u = User(email = email, password = password, name = name)
    u.save()

    mydata = dict()
    mydata['response'] = 'Done'

    return HttpResponse(json.dumps(mydata), content_type='application/json')

@never_cache
@csrf_exempt
def getUser(request):
    req = request.POST
    email = req['email']

    query_set = User.objects.filter(email = email)
    json_data = serializers.serialize('json', query_set)
    data = json.loads(json_data)

    #TODO : check if user does not exists

    data = data[0]
    mydata = dict()
    mydata['id'] = data['pk']
    mydata['user'] = data['fields']

    return HttpResponse(json.dumps(mydata), content_type='application/json')


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

def getUserIdFromEmail(email):
    # get user_id from email
    query_set = User.objects.filter(email = email)
    json_data = serializers.serialize('json', query_set)
    data = json.loads(json_data)
    print("fetched user = ")
    print(data)
    data = data[0]
    user_id = data['pk']

    return user_id

@never_cache
@csrf_exempt
def getTournamentList(request):
    req = request.POST
    email = req['email']
    print("email = ")
    print(email)
    user_id = getUserIdFromEmail(email)

    query_set = Tournament.objects.all().order_by('tournament_date')
    json_data = serializers.serialize('json', query_set)
    data = json.loads(json_data)

    tournament_list = list()
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
        query_set = UserTournaments.objects.filter(user_id = user_id, tournament_id = item['pk'])
        if not query_set:
            x['has_registered'] = False
        else:
            x['has_registered'] = True
        tournament_list.append(x)


    mydata = dict()
    mydata['tournament_list'] = tournament_list
    print(mydata)

    return HttpResponse(json.dumps(mydata), content_type='application/json')

@never_cache
@csrf_exempt
def addUserTournament(request):
    req = request.POST
    email = req['email']
    user_id = getUserIdFromEmail(email)
    tournament_id = req['tournament_id']

    #first check if user has already registered or not
    query_set = UserTournaments.objects.filter(user_id = user_id, tournament_id = tournament_id)
    print(query_set)
    if query_set:
        mydata = dict()
        mydata['response'] = 'Already registered';
        return HttpResponse(json.dumps(mydata), content_type='application/json')

    else:
        #check joined count
        query_set = Tournament.objects.filter(id = tournament_id)
        json_data = serializers.serialize('json',query_set)
        data = json.loads(json_data)
        data = data[0]['fields']
        joined_count = data['joined_count']
        team_count = data['team_count']
        is_registration_open = data['is_registration_open']

        #if tournament not full, then increment joined count by 1
        if joined_count < team_count and is_registration_open:
            joined_count += 1
            Tournament.objects.filter(id = tournament_id).update(joined_count = joined_count)
            ProfileHelper.addUserTournament(user_id, tournament_id)

            #change is_registration_open field to false is team_count = joined_count
            if team_count == joined_count:
                #also change registration end date to now
                Tournament.objects.filter(id = tournament_id).update(is_registration_open = False, registration_end_date = timezone.now())


            mydata = dict()
            mydata['response'] = 'Done';
            return HttpResponse(json.dumps(mydata), content_type='application/json')

        #else return team full message and change
        else:
            mydata = dict()
            mydata['response'] = 'Registration is closed';
            return HttpResponse(json.dumps(mydata), content_type='application/json')





@never_cache
@csrf_exempt
def getUserTournamentList(request):
    req = request.POST
    email = req['email']
    user_id = getUserIdFromEmail(email)

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
        json_data = serializers.serialize('json', query_set)
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

@never_cache
@csrf_exempt
def hasRegisteredForTournament(request):
    req = request.POST
    user_id = req['user_id']
    tournament_id = req['tournament_id']

    query_set = UserTournaments.objects.filter(user_id = user_id, tournament_id = tournament_id)
    json_data = serializers.serialize('json', query_set)
    data = json.loads(json_data)

    mydata = dict()

    if len(data) != 0:
        mydata['response'] = 'true'
    else:
        mydata['response'] = 'false'

    return HttpResponse(json.dumps(mydata), content_type='application/json')

@never_cache
@csrf_exempt
def setProfilePic(request):
    req = request.POST
    profile_pic = req['profile_pic']
    email = req['email']

    user_id = getUserIdFromEmail(email)
    user = User.objects.filter(id = user_id)
    p = Profile(user = user[0], mobile_number="7777777777", profile_pic = profile_pic)
    p.save()

    mydata = dict()
    mydata['response'] = 'Done'
    print(mydata)

    return HttpResponse(json.dumps(mydata), content_type='application/json')
