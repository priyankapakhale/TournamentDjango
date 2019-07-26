from django.contrib import admin
from .models import Tournament

# Register your models here.
class TournamentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Tournament._meta.get_fields()]

admin.site.register(Tournament, TournamentAdmin)