from django.urls import path

from blog import views


urlpatterns = [
    path('', views.index, name='index'),
    path('submit-post', views.submit_post, name='submit-post')
]
