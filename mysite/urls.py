"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import blog
from django.conf import settings
from django.conf.urls.static import static


from django.urls import path, include
from django.conf.urls import url
from blog import views


urlpatterns = [
    path('admin/', admin.site.urls),
    #url(r'^admin/', admin.site.urls),
    url(r'^processOrder/', views.processOrder),
    url(r'^getTournamentList/', views.getTournamentList),
    url(r'^handlePayment/',views.handlePayment),
    url(r'^addUserTournament/', views.addUserTournament),
    url(r'^getUserTournamentList/',views.getUserTournamentList),
    url(r'^getUser/',views.getUser),
    url(r'^addUser/',views.addUser),
    url(r'^setProfilePic/',views.setProfilePic),
    url(r'^getProfile/',views.getProfile),

]
