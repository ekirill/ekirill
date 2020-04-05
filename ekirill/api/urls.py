from django.urls import path, include


app_name = 'api'

urlpatterns = [
    path('cameras/', include('cameras.api.urls')),
]
