from django.urls import  path, include
from blog import  views
from django.views.generic import TemplateView


app_name= 'blog'
urlpatterns = [
    path('fbv-index/', views.index_view, name='index'),
    # path('cbv-index/', TemplateView.as_view(template_name='index.html', extra_context={'name': 'farhad'}), name='index'),
    path('cbv-index/', views.IndexView.as_view(), name='cbv-index'),
    path('', views.PostList.as_view(), name='post-list'),
    path('<int:pk>/', views.PostDetail.as_view(), name='post-detail'),
    path('post/create/', views.PostCreateView.as_view(), name='post-create'),
    path('post/update/<int:pk>/', views.PostEditView.as_view(), name='post-edit'),
    path('post/del/<int:pk>/', views.PostDeleteView.as_view(), name='post-delete'),
    path('api/v1/', include('blog.api.v1.urls'))
]
