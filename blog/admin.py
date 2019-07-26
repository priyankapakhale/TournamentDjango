from django.contrib import admin
from .models import Tournament, User

# Register your models here.
class TournamentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Tournament._meta.get_fields()]

admin.site.register(Tournament, TournamentAdmin)
admin.site.register(User)
