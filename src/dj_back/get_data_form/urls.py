from django.urls import path

from . import views

urlpatterns = [
    path('', views.submit_data, name='submit_data'),
    path('get_file', views.get_file, name='get_file'),
    path('upload_antennas', views.upload_antennas, name='upload_antennas')
    # path('success', views.submit_success, name='submit_success'),
]
