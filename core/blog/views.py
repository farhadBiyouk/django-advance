from django.shortcuts import render
from django.views.generic.base import TemplateView, RedirectView
from blog.models import Post
from django.views.generic import (
    ListView,
    DetailView,
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
)
from blog.forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


def index_view(request):

    name = "reza"
    context = {"name": name}
    return render(request, "index.html", context)


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "gholi"
        context["posts"] = Post.objects.all()
        return context


class RedirectViewMaktab(RedirectView):

    url = "https://maktabkhooneh.org"

    def get_redirect_url(self, *args, **kwargs):
        post = Post.objects.all()[1]
        print(post)
        return super().get_redirect_url(*args, **kwargs)


class PostList(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = "blog.view_post"

    template_name = "blog/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        posts = Post.objects.all()
        return posts


class PostDetail(LoginRequiredMixin,DetailView):

    template_name = "blog/post_detail.html"
    context_object_name: str = "single_post"
    model = Post


# class PostCreateView(FormView):

#     template_name = 'blog/create_post_form.html'
#     form_class = PostForm
#     success_url = '/blog/'

#     def form_valid(self, form) :
#         form.save()
#         return super().form_valid(form)


class PostCreateView(CreateView):

    model = Post
    form_class = PostForm
    template_name = "blog/create_post_form.html"
    success_url = "/blog/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostEditView(UpdateView):
    model = Post
    template_name = "blog/update_post.html"
    form_class = PostForm
    success_url = "/blog/"


class PostDeleteView(DeleteView):

    model = Post
    success_url = "/blog/"
