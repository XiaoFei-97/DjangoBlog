from django import template
from blog.models import Post
from django.db.models import Q
import random

register = template.Library()


@register.simple_tag
def get_category_post(category):
    """
        作用：获取该目录下的所有博客
        obj：模板传递的参数，也就是category
    """
    post_list = Post.objects.filter(category=category)
    return post_list[0:15]


@register.simple_tag
def get_category_count(category):
    """
        作用：计算当前分类的文章数量，并返回到模板中
        category：模板页面传入的category
    """
    return Post.objects.filter(category=category).count()


@register.simple_tag
def get_date_post(year, month):
    """
        作用：获取该年月下的博客
        year：模板传递的年份
        month：模板传递的月份
    """
    post_list = Post.objects.all().filter(created_time__year=year, created_time__month=month)
    return post_list[:15]


@register.simple_tag
def get_date_to_month(post_date):
    """
        作用：将日期格式转换成年月的形式
        obj: 对应的post_date
    """
    return (str(post_date.year) +'年' + str(post_date.month) + '月')


@register.simple_tag
def get_date_count(year, month):
    """
        作用：获得该年月下的博客数量
        year: 模板传递的年份
        month：模板传递的月份
    """
    return Post.objects.filter(created_time__year=year, created_time__month=month).count()


@register.simple_tag
def get_random_recomment():
    # 随机推荐
    random_posts = set()
    post_list = Post.objects.all()
    while random_posts.__len__() < 15:
        random_posts.add(random.choice(post_list))

    return random_posts


@register.simple_tag
def get_like_post(category, id):
    # 猜你喜欢
    # 使用Q可以过滤出不要的条件
    post_list =  Post.objects.filter(~Q(id=id), category=category)
    return post_list[:15]




