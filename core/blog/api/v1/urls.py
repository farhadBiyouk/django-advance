from django.urls import  path
from blog.api.v1 import  views



app_name= 'blog'
urlpatterns = [
    path('post-list', views.api_get_list_view, name='api_get_list_view'),

]
