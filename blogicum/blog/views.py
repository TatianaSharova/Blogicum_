from typing import Any

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import CommentForm, PostForm, UserForm
from .models import Category, Comment, Post, User

NUMBER_OF_POSTS_ON_PAGE = 10


def get_list_of_posts():
    """Выводит список отсортированных постов."""
    return Post.objects.select_related(
        'category', 'author', 'location').filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()).order_by(
        '-pub_date', ).annotate(comment_count=Count('comment'))


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = NUMBER_OF_POSTS_ON_PAGE
    queryset = get_list_of_posts()


class PostsCategoryListView(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = NUMBER_OF_POSTS_ON_PAGE

    def get_queryset(self):
        return get_list_of_posts().filter(
            category__slug=self.kwargs['category_slug']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(
            Category,
            is_published=True,
            slug=self.kwargs['category_slug']
        )
        context['category'] = category
        return context


def get_profile(request, username):
    """Открывает страницу профиля,
    на которую выводит информацию о пользователе
    и постраничный список его постов."""
    try:
        profile = get_object_or_404(User, username=username)
    except User.DoesNotExist:
        raise Http404('User matching query does not exist')
    posts = Post.objects.select_related(
        'category', 'author', 'location'
    ).filter(author=profile.pk).order_by(
        '-pub_date').annotate(comment_count=Count('comment'))
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'profile': profile,
        'page_obj': page_obj,
    }
    return render(request, 'blog/profile.html', context)


def edit_profile(request):
    """Открывает страницу редактирования данных пользователя."""
    try:
        instance = User.objects.get(username=request.user)
    except User.DoesNotExist:
        raise Http404('User matching query does not exist')
    form = UserForm(request.POST or None, instance=instance)
    context = {'form': form, }
    if form.is_valid():
        form.save()
    return render(request, 'blog/user.html', context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        if post.author == request.user or (
            post.is_published and post.pub_date <= timezone.now()
                and post.category.is_published):
            return super().dispatch(request, *args, **kwargs)
        raise Http404('Post not found')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comment.select_related('author')
        )
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:profile',
                            kwargs={'username': self.object.author.username})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['post_id'])
        if instance.author != request.user:
            return redirect('blog:post_detail', pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.id})


class DispatchMixin:

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(self.model, pk=kwargs[self.pk_url_kwarg])
        if instance.author != request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(DispatchMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.object)
        return context


@login_required
def add_comment(request, pk):
    """Добавляет комментарии к постам."""
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', pk=pk)


class CommentMixin(DispatchMixin):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'
    fields = ('text',)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.post.id})


class CommentUpdateView(CommentMixin, LoginRequiredMixin, UpdateView):
    pass


class CommentDeleteView(CommentMixin, LoginRequiredMixin, DeleteView):
    pass
