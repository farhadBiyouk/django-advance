from django.shortcuts import render
from django.views.generic.base import  TemplateView, RedirectView
from blog.models import Post
from django.views.generic import ListView, DetailView

def index_view(request):

    name = 'reza'
    context = {'name': name}
    return render(request, 'index.html', context)


class IndexView(TemplateView):
    template_name  ='index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = 'gholi'
        context['posts'] = Post.objects.all()
        return context


class RedirectViewMaktab(RedirectView):
    
    url = 'https://maktabkhooneh.org'

    def get_redirect_url(self, *args, **kwargs):
        post = Post.objects.all()[1]
        print(post)
        return super().get_redirect_url(*args, **kwargs)


class PostList(ListView):

    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        posts = Post.objects.all()
        return posts

class PostDetail(DetailView):

    template_name = 'blog/post_detail.html' 
    context_object_name: str = 'single_post'
    model = Post
