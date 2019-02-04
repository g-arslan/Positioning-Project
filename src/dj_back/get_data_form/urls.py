from django.urls import path

from . import views

urlpatterns = [
    path('', views.submit_data, name='submit_data'),
    # path('success', views.submit_success, name='submit_success'),
]
