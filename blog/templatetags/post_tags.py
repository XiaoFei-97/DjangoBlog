from django import template
from blog.models import Post
import random

register = template.Library()


@register.simple_tag
def get_category_post(obj):
    """获取该目录下的所有博客"""
    post_list = Post.objects.filter(category=obj)
    return post_list[0:14]


@register.simple_tag
def get_date_post(year, month):
    """获取该月份下的博客"""
    post_list = Post.objects.all().filter(created_time__year=year, created_time__month=month)
    return post_list[:14]

@register.simple_tag
def get_date_to_month(obj):

    return (str(obj.year) +'年' + str(obj.month) + '月')

@register.simple_tag
def get_category_to_post(obj):
    return Post.objects.filter(category=obj).count()

@register.simple_tag
def get_date_to_post(year, month):
    return Post.objects.filter(created_time__year=year, created_time__month=month).count()

@register.simple_tag
def get_random_recomment():
    random_posts = []
    post_list = Post.objects.all()
    for i in range(1, 16):
        random_posts.append(random.choice(post_list))
    return random_posts


@register.simple_tag
def get_category_count(category):
    return Post.objects.filter(category=category).count()



