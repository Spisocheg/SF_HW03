from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Subscription
from .filters import PostFilter
from .forms import PostNewsForm, PostArticleForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Exists, OuterRef

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from datetime import datetime


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        cat = request.POST.get('cat')
        category = Category.objects.get(id=cat)
        action = request.POST.get('action')

        if action == 'sub':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsub':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('id')

    return render(
        request,
        'subscriptions.html',
        {'cats': categories_with_subscriptions},
    )


class PostsList(ListView):
    model = Post
    ordering = '-creationDate'
    template_name = 'list.html'
    context_object_name = 'news'
    extra_context = {'categories': Category.objects.all(), 'default': datetime(1999, 12, 31, 23, 59).strftime('%Y-%m-%d %H:%M')}
    paginate_by = 10


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostNewsForm
    model = Post
    template_name = 'create.html'
    context_object_name = 'news'
    extra_context = {'is_edit': False}
    raise_exception = True


class PostsSearch(ListView):
    model = Post
    ordering = '-creationDate'
    template_name = 'search.html'
    context_object_name = 'news'
    extra_context = {'categories': Category.objects.all(), 'default': datetime(1999, 12, 31, 23, 59).strftime('%Y-%m-%d %H:%M')}
    paginate_by = 10

    def get_queryset(self):
        if self.request.GET.get('date') == '':
            date = datetime(1999, 12, 31, 23, 59).strftime('%Y-%m-%d %H:%M')
        else:
            date = self.request.GET.get('date')
        posts = Post.objects.filter(title__icontains=self.request.GET.get('title'),
                                    postCategory__categoryName__icontains=self.request.GET.get('cat'),
                                    creationDate__gt=date)\
                            .order_by('-creationDate').distinct()

        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'title={self.request.GET.get("title")}&'
        context['cat'] = f'cat={self.request.GET.get("cat")}&'
        context['date'] = f'date={self.request.GET.get("date")}&'
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'detail.html'
    context_object_name = 'news'


class PostNewsList(ListView):
    queryset = Post.objects.filter(categoryType__icontains='News')
    ordering = '-creationDate'
    template_name = 'list.html'
    context_object_name = 'news'
    extra_context = {'categories': Category.objects.all(),
                     'default': datetime(1999, 12, 31, 23, 59).strftime('%Y-%m-%d %H:%M')}
    paginate_by = 10


class PostNewsDetail(DetailView):
    queryset = Post.objects.filter(categoryType__icontains='News')
    template_name = 'detail.html'
    context_object_name = 'news'


# class PostNewsCreate(PermissionRequiredMixin, CreateView):
#     permission_required = ('news.add_post',)
#     form_class = PostNewsForm
#     model = Post
#     template_name = 'news_create.html'
#     context_object_name = 'news'
#     extra_context = {'is_edit': False}
#     raise_exception = True

    # def form_valid(self, form):
    #     post = form.save()
    #     post.categoryType = 'News'
    #     return super().form_valid(form)


class PostNewsEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostNewsForm
    model = Post
    template_name = 'news_create.html'
    context_object_name = 'news'
    extra_context = {'is_edit': True}
    raise_exception = True


class PostNewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news_delete.html'
    context_object_name = 'news'
    success_url = reverse_lazy('news_list')
    raise_exception = True


class PostArticlesList(ListView):
    queryset = Post.objects.filter(categoryType__icontains='Article')
    ordering = '-creationDate'
    template_name = 'list.html'
    context_object_name = 'news'
    extra_context = {'categories': Category.objects.all(),
                     'default': datetime(1999, 12, 31, 23, 59).strftime('%Y-%m-%d %H:%M')}
    paginate_by = 10


class PostArticlesDetail(DetailView):
    queryset = Post.objects.filter(categoryType__icontains='Article')
    template_name = 'detail.html'
    context_object_name = 'news'


# class PostArticlesCreate(PermissionRequiredMixin, CreateView):
#     permission_required = ('news.add_post',)
#     form_class = PostArticleForm
#     model = Post
#     template_name = 'article_create.html'
#     context_object_name = 'news'
#     extra_context = {'is_edit': False}
#     raise_exception = True

    # def form_valid(self, form):
    #     post = form.save()
    #     post.categoryType = 'Article'
    #     return super().form_valid(form)


class PostArticlesEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostArticleForm
    model = Post
    template_name = 'article_create.html'
    context_object_name = 'news'
    extra_context = {'is_edit': True}
    raise_exception = True


class PostArticlesDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'article_delete.html'
    context_object_name = 'news'
    success_url = reverse_lazy('article_list')
    raise_exception = True
