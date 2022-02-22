from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('watch/', include("watchlist.api.urls")),
    path('accounts/', include("user_app.api.urls"))
]
