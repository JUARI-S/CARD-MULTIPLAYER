from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('auth/', include('authentication.urls')),
    path('online_28/', include('online_28.urls'))
]
