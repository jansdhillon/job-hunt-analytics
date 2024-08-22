from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
]
