from .models import User, Order, Tournament, UserTournaments, UserOrders, User

def addUserTournament(user_id, tournament_id):
    user = User.objects.filter(id = user_id)
    tournament = Tournament.objects.filter(id = tournament_id)

    ut = UserTournaments(
        user = user[0],
        tournament = tournament[0]
    )
    ut.save()

def addUser(email, password, name):
    u = User(
        email = email,
        password = password,
        name = name
    )
    u.save()