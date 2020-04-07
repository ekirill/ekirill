from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.urls import path, include


urlpatterns = [
    path('', include('social_django.urls', namespace='social')),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),

    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
    path('cameras/', include('cameras.urls', namespace='cameras')),
]
