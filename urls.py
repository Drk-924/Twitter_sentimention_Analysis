"""Recommendationsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from . import index
from . import AdminDashboard
from . import ProposedImpl
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('page1',index.page1),
    path('register',index.register),
    path('logout',AdminDashboard.logout),
    path('login',index.login),
    path('userlogin',index.userlogin), 
    path('adminhome',AdminDashboard.adminhome),
    path('addtotext',AdminDashboard.addtotext),
    path('exquestiongen',AdminDashboard.exquestiongen), 
    path('proposedque',AdminDashboard.proposedque),   
    path('uploadedstatements',AdminDashboard.uploadedstatements),
    path('statementtoken',AdminDashboard.statementtoken),
    path('wordtoken',AdminDashboard.wordtoken), 
    path('stopwordremoval',AdminDashboard.stopwordremoval),
    path('wordvectorisation',AdminDashboard.wordvectorisation),
    path('paraformation',AdminDashboard.paraformation),
    path('proposedqagen',AdminDashboard.proposedqagen), 
    path('dummy',AdminDashboard.dummy),
    path('t5question_gen',AdminDashboard.t5question_gen),
    path('UserFeedback',AdminDashboard.UserFeedback),
    path('prstatementtoken',AdminDashboard.prstatementtoken),
    path('tweetsbymeth2',AdminDashboard.tweetsbymeth2),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

