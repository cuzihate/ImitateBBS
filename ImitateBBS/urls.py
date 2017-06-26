"""ImitateBBS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from users import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^modules/', include('modules.urls')),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^login/', views.LoginView.as_view(), name='login'),
    url(r'^register/', views.RegisterView.as_view(), name='register'),
    url(r'^send_email/', views.SendEmailView.as_view(), name='send_email'),
    url(r'^favour/', views.FavourView.as_view(), name='favour'),
]
