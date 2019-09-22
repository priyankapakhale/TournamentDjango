from django.db import models

# Create your models here.
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.CharField(max_length=50)
    customer_id = models.IntegerField()
    email = models.CharField(max_length=50)
    mobile_no = models.CharField(max_length=10)
    amount = models.FloatField(default=0)

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=30)

class Profile(models.Model):
    id = models.AutoField(primary_key = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=10, null=True)
    profile_pic_uri = models.CharField(max_length=500, null=True)


class UserOrders(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

class Tournament(models.Model):
    TYPES = (
        (1, 'SOLO'),
        (2, 'DUO'),
        (3, 'SQUAD'),
    )
    STATUSES = (
        (1, 'Upcoming'),
        (2, 'Ongoing'),
        (3, 'Past'),
    )

    TPP_FPP = (
        (1, 'TPP'),
        (2, 'FPP'),
    )

    MAPS = (
        (1, 'ERANGLE'),
        (2, 'MIRAMAR'),
        (3, 'SANHOK'),
        (4, 'VIKENDI'),
        (5, 'ALL')
    )

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    status = models.IntegerField(choices = STATUSES)
    type = models.IntegerField(choices = TYPES)
    entry_fee = models.FloatField(default=0)
    tournament_date = models.DateTimeField()
    team_count = models.IntegerField()
    joined_count = models.IntegerField()
    win_prize = models.FloatField(default=0)
    per_kill = models.FloatField(default=0)
    tpp_fpp = models.IntegerField(choices=TPP_FPP)
    map = models.IntegerField(choices = MAPS)


    description = models.TextField(max_length=5000)
    structure = models.TextField(max_length=5000)
    contact = models.CharField(max_length=100)
    prize = models.TextField(max_length=5000)
    rules = models.TextField(max_length=5000)
    is_registration_open = models.BooleanField()



class UserTournaments(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)



