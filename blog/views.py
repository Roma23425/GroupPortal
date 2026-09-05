from django.shortcuts import render

from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View

from .models import Post, Comment
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CommentForm, PostForm

class GroupInfoView(TemplateView):
    """Представлення для головної сторінки з інформацією про групу"""
    template_name = 'home.html'

class RegisterView(CreateView):
    """Представлення для реєстрації нових користувачів"""
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login') 


class CustomLoginView(LoginView):
    """Представлення для логіну"""
    form_class = CustomAuthenticationForm 
    template_name = 'login.html'

class PostListView(ListView):
    """Представлення для списку постів"""
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    ordering = ['-id'] 


class PostDetailView(DetailView):
    """Представлення для детального перегляду поста та виводу коментарів"""
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author').all()
        return context

class AddCommentView(LoginRequiredMixin, View):
    """
    Представлення для обробки збереження коментаря.
    LoginRequiredMixin не пустить сюди неавторизованих користувачів.
    """
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            
        return redirect(reverse('post_detail', kwargs={'pk': pk}))

class PostCreateView(LoginRequiredMixin, CreateView):
    """Створення нового поста (лише для авторизованих)"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редагування поста (лише для автора або модератора/адміна)"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.role in ['admin', 'moderator']

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Видалення поста (лише для автора або модератора/адміна)"""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.role in ['admin', 'moderator']