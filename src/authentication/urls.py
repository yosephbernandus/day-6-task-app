from django.urls import path

from authentication import views


urlpatterns = [
    path('', views.index, name="login"),
    path('submit-login', views.submit_login, name="submit_login"),
    path('logout', views.logout_view, name="logout"),
]
