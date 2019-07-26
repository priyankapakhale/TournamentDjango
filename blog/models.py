from django.db import models

# Create your models here.
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.CharField(max_length=50)
    customer_id = models.IntegerField()
    email = models.CharField(max_length=50)
    mobile_no = models.CharField(max_length=10)
    amount = models.FloatField(default=0)

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


    id = models.AutoField(primary_key=True)
    platform = models.IntegerField(choices = PLATFORMS)
    game_name = models.CharField(max_length=50)
    game_mode = models.IntegerField(choices = GAME_MODES)
    entry_fee = models.FloatField(default=0)
    tournament_date = models.DateTimeField()
    registration_end_date = models.DateTimeField()
    team_count = models.IntegerField()
    joined_count = models.IntegerField()
    host_name = models.CharField(max_length=50)






