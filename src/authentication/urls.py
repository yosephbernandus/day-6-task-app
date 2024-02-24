from django.urls import path

from authentication import views


urlpatterns = [
    path('', views.index, name="login"),
    path('logout', views.logout_view, name="logout"),
]
