from django.contrib import admin
from .models import Category, Tag, Post  # ReadNum


# 自定义
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('id', 'name')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    list_display = ('id', 'name')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'created_time', 'modified_time', 'category', 'author', 'get_read_num')


'''
@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):

    list_display = ('read_num', 'post')
'''

