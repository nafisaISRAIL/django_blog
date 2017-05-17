from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.formsets import formset_factory
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib import auth

from django.core.mail import send_mail
from django.conf import settings


from blog2.posts.models import Category, Post, Author
from .forms import (
    AuthorForm,
    PostForm, PostDeleteForm,
    PostUpdateForm, AuthorUpdateForm,
    ContactForm, UserUpdateForm,
)
from blog2.comments.forms import CommentForm
from blog2.comments.models import Comment


@login_required
def add_author(request):
    user = request.user
    try:
        author = user.author
    except AttributeError, e:
        author = None

    user_form = UserUpdateForm(request.POST or None, instance=user)
    author_form = AuthorForm(request.POST or None,
                             request.FILES or None, instance=author)
    if request.method == 'POST':
        if author_form.is_valid() and user_form.is_valid():
            user = user_form.save()
            author.user = user
            author_form.save()
            return redirect(reverse('about-author', args=[author.id]))
    return render(request, 'posts/add_author.html', locals())


@login_required
def add_post(request):
    author = request.user.author
    post_form = PostForm(request.POST or None,
                         request.FILES or None)
    if request.method == 'POST':
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = author
            post.save()
            messages.success(request, '{} has been added'.format(post))
            return redirect(reverse('post_detail', args=[post.id]))

        else:
            default_error = 'Somethong went wrong. Please try again.'
            error_message = post_form.errors['__all__'] \
                if '__all__' in post_form.errors else default_error
            messages.error(request, error_message)

    context = {
        'form': post_form
    }
    return render(request, 'posts/add_post.html', context)


@method_decorator([login_required, ], name='dispatch')
class PostAddClassForm(View):
    template_name = 'posts/add_post2.html'
    from_class = PostForm

    def get(self, request, *args, **kwargs):
        form = self.from_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.from_class(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.author
            post.save()
            return redirect(reverse('details', args=[post.id]))
        else:
            return render(request, self.template_name, {'form': form})


def add_post_set(request):
    PostFormSet = formset_factory(PostForm, extra=2)
    if request.method == 'POST':
        formset = PostFormSet(request.POST, request.FILES)
        if formset.is_valid():
            [_.save() for _ in formset]
            messages.success(request, 'Posts added')
            return redirect(reverse('about'))
        else:
            messages.error(request, 'Something went wrong.')
    formset = PostFormSet()
    return render(request, 'posts/add_with_set.html', {'formset': formset})


class MainPage(ListView):
    template_name = "posts/main.html"
    queryset = Post.published.order_by('-id')
    paginate_by = 10


class AuthorList(ListView):
    model = Author


class PostDetail(DetailView):
    model = Post
    template_name = 'posts/detail.html'
    context_object_name = 'post'
    class_form = CommentForm

    def post(self, request, *args, **kwargs):
        form = self.class_form(request.POST)
        self.post = Post.objects.get(id=self.kwargs['pk'])
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = auth.get_user(request)
            comment.post = self.post
            comment.save()
            return redirect(reverse('post_detail', args=[self.post.id]))
        else:
            return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        self.object = Post.objects.get(id=self.kwargs['pk'])
        context['form'] = self.class_form
        context['comments'] = Comment.objects.filter(
            post=self.object).order_by('-id')
        return context


def about_page(request):
    users = User.objects.all()
    return render(request, 'posts/about.html', locals())


def contact_page(request):
    form = ContactForm(request.POST or None,)
    if request.method == 'POST':
        if form.is_valid():
            email_subject = 'Message from site contact from'
            email_body = 'Sender name {} \n. \
                          Sender e-mail {} \n. \
                          Message {}'.format(
                form.clean_name,
                form.clean_email,
                form.clean_message)
            send_mail(email_subject, email_subject,
                      settings.EMAIL_HOST_USER,
                      ['simply@gmail.com'],
                      fail_silently=False)
            return redirect(reverse('email_sended'))
    return render(request, 'posts/contact.html', locals())


def sended(request):
    return render(request, 'posts/email_sended.html')


def media_page(request):
    return render(request, 'posts/media.html')


def get_categories(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'posts/main.html', context)


def post_update(request, post_id):
    post = Post.objects.get(id=post_id)
    form = PostUpdateForm(request.POST or None, request.FILES or None,
                          instance=post)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Title has been changed.')
            return redirect(reverse('post_detail', args=[post.id]))
        else:
            messages.error(request, 'Something went wrong. Try again')
    return render(request, 'posts/edit_title.html', locals())


def author_update(request, id):
    author = Author.objects.get(id=id)
    form = AuthorUpdateForm(request.POST or None, request.FILES or None,
                            instance=author)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Update passed successul')
            return redirect(reverse('about-author', args=[author.id]))
        else:
            messages.error(request, 'Something went wrong')
    return render(request, 'posts/edit_author.html', locals())


@require_POST
def post_delete(request, id):
    post_to_delete = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostDeleteForm(request.POST, instance=post_to_delete)
        if form.is_valid():
            post_to_delete.delete()
            messages.success(request, 'Post {} has been deleted.'.format(id))
            return redirect(reverse('main'))
        else:
            form = PostDeleteForm(instance=post_to_delete)
            messages.error(request, 'Could not delete post {}'.format(id))
    return redirect(reverse('post_detail', args=[id, ]))


def about_author(request, id):
    author = Author.objects.get(id=id)
    posts = author.post_set.all()
    return render(request, 'posts/author_detail.html', locals())


def get_post_by_category(request, id):
    posts_by_category = Post.objects.filter(category__id=id)
    category = Category.objects.get(id=id)
    return render(request, 'posts/category.html', locals())


def personal_page(request, id):
    user = User.objects.get(id=id)
    author = Author.objects.get(user=user)
    published_posts = author.post_set.filter(status='p')
    draft_posts = author.post_set.filter(status='d')
    return render(request, 'posts/personal_page.html', locals())
