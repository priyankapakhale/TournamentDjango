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


class UserOrders(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

class Tournament(models.Model):
    PLATFORMS = (
        (1, 'Mobile'),
        (2, 'PC'),
        (3, 'XBOX'),
        (4, 'Playstation'),
    )
    GAME_MODES = (
        (1, 'SOLO'),
        (2, 'DUO'),
        (3, 'SQUAD'),
    )
    STATUSES = (
        (1, 'Upcoming'),
        (2, 'Ongoing'),
        (3, 'Past'),
    )

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    status = models.IntegerField(choices = STATUSES)
    platform = models.IntegerField(choices = PLATFORMS)
    game_name = models.CharField(max_length=50)
    game_mode = models.IntegerField(choices = GAME_MODES)
    entry_fee = models.FloatField(default=0)
    tournament_date = models.DateTimeField()
    registration_end_date = models.DateTimeField()
    team_count = models.IntegerField()
    joined_count = models.IntegerField()
    host_name = models.CharField(max_length=50)
    description = models.CharField(max_length=5000)
    structure = models.CharField(max_length=5000)
    contact = models.CharField(max_length=100)
    prize = models.CharField(max_length=5000)
    rules = models.CharField(max_length=5000)
    is_registration_open = models.BooleanField()



class UserTournaments(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)



