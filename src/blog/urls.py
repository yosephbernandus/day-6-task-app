from django.urls import path

from blog import views


urlpatterns = [
    path('', views.index, name='index'),
    path('submit-post', views.submit_post, name='submit-post'),
    path('detail/<str:slug>', views.detail_post, name='detail-post'),
    path('submit-comment/<int:post_id>', views.submit_comment, name='submit-comment'),
]
