import os
from django.views.generic import (
    DetailView, TemplateView, 
    ListView, UpdateView,
    DeleteView, CreateView
)
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

from .models import Category, Post, Comment, Likes, Subscribe
from authsystem.models import User 
from .forms import CommentCreationalFrom, PostCreationalFrom
from services.mailing_service import notificate


class HomeTemplateView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['latest'] = Post.objects.latest('created')
            context['popular'] = Post.objects.exclude(pk=context['latest'].pk).order_by('-created')[:12]
            context['futured'] = Post.objects.exclude(pk=context['latest'].pk).order_by('-created')[:12]
        except:
            context['latest'] = []
            context['popular'] = []
            context['futured'] = []

        from server.settings import STATIC_ROOT
        print(STATIC_ROOT+'/pages/styles')

        return context
    

class CategoryListView(ListView):
    model = Category
    template_name = 'blog/category/category_list.html'
    context_object_name = 'categories'

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post/post_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('post_list')

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blog/post/post_update.html'
    fields = ['title', 'text', 'category', 'photo_preview']
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['likes'] = Likes.objects.filter(post=context['post']).count()
        context['comments'] = Comment.objects.filter(post=context['post'].id)
        context['comment_form'] = CommentCreationalFrom
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('text').strip() == '':
            return super().get(request, *args, **kwargs)
        comment = Comment.objects.create(
            author=request.user,
            post=Post.objects.get(pk=str(kwargs['pk'])),
            text=request.POST.get('text'),)
        return super().get(request, *args, **kwargs)

class PostListView(ListView):
    model = Post
    template_name = 'blog/post/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created']

    def get_queryset(self):
        categories = Category.objects.all()
        query = self.request.GET.get('category')
        for i in categories:
            if str(i.pk) == query:
                return Post.objects.filter(category__pk=query)
        return super().get_queryset()

class PostCreateView(CreateView):
    model = Post
    form_class = PostCreationalFrom
    template_name = 'blog/post/post_create.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.cleaned_data['author'] = request.user
            post = Post.objects.create(**form.cleaned_data)
            print(Subscribe.objects.filter(author=request.user).select_related())
            notificate.delay(str(request.user.pk))
            return redirect(reverse_lazy('post_detail', kwargs={'pk': post.pk}))
        else:
            return self.form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('post_detail',kwargs={'pk': self.get_object().id})
