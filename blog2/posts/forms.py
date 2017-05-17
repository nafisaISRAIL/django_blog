import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.forms.extras import SelectDateWidget
from django.forms import Textarea
from models import Author, Post
from django.contrib.auth.models import User

BIRTH_YEAR_CHOICES = [x for x in range(1955, 2018)]
STATUS = (
    ('p', 'Published'),
    ('d', 'Draft'),
)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ['biography', 'gender', 'birth', 'image']

        widgets = {
            'birth': SelectDateWidget(
                years=BIRTH_YEAR_CHOICES),
            'biography': Textarea(attrs={'cols': 40, 'rows': 10})
        }

    def __init__(self, *args, **kwargs):
        super(AuthorForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = True

    def clean_birth(self):
        bd = self.cleaned_data['birth']
        date = datetime.date(2000, 01, 01)
        if bd > date:
            raise ValidationError('You are so young!')
        return bd


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'description',
                  'status', 'image']
        widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 10}),
            'category': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False

    def clean_author(self):
        author = self.cleaned_data['author']
        if author == 'if cond is None':
            raise ValidationError('Please choice author')
        return author

    def clean_category(self):
        category = self.cleaned_data['category']
        if category == 'if cond is None':
            raise ValidationError('Please choice category')
        return category

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 2:
            raise ValidationError('Your title is so short')
        return title

    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) < 20:
            raise ValidationError('Description is so short!')
        return description


class PostDeleteForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = []


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'category', 'image', 'status']
        widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 10}),
            'category': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super(PostUpdateForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False


class AuthorUpdateForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['biography', 'image']

    def __init__(self, *args, **kwargs):
        super(AuthorUpdateForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = True


class ContactForm(forms.Form):
    name = forms.CharField(required=True,
                           label='Your name',
                           widget=forms.TextInput)

    email = forms.EmailField(required=True,
                             label='e-mail',
                             widget=forms.EmailInput)

    message = forms.CharField(
        required=True,
        widget=forms.Textarea)

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 2:
            raise ValidationError('Enter your name')
        return name

    def clean_email(self):
        email = self.cleaned_data['email']
        if len(email) < 2:
            raise ValidationError('Enter email')
        return email

    def clean_message(self):
        message = self.cleaned_data['message']
        if len(message) < 10:
            raise ValidationError('Enter your content')
        return message
