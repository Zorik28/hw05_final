from django.core.paginator import Paginator

NUMBER_OF_POSTS = 10


def get_paginator(queryset, request):
    paginator = Paginator(queryset, NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
