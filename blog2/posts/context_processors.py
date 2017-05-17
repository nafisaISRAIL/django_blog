# -*- coding:utf-8 -*-

from blog2.posts.models import Category


def categories(request):
    return {
        'categories': Category.objects.all()
    }
