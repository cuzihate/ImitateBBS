from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'(?P<nid>\d+)/', views.ModuleView.as_view()),
]
