# _*_ coding:utf-8 _*_
"""
@author:jack
@time:18-5-30下午10:09
"""
import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum, ReadDetail
from blog.models import Post


def read_statistics_once_read(request, obj):
    """阅读+1的处理逻辑功能"""
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)
    if not request.COOKIES.get(key):

        # 第一种办法：新增阅读计数功能
        # post.read_num += 1
        # post.save()

        # 第二种办法：新增阅读计数功能
        '''
        if ReadNum.objects.filter(post=post).count():
            # 存在记录
            readnum = ReadNum.objects.get(post=post)
        else:
            # 不存在记录
            readnum = ReadNum(post=post)

        # 计数+1
        readnum.read_num += 1
        readnum.save()
        '''

        # 第三种办法：创建应用型的
        '''
        if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
            # 存在记录
            readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        else:
            # 不存在记录
            readnum = ReadNum(content_type=ct, object_id=obj.pk)
        '''
        # 如果使用get_or_create就能省略上面一大段，可以简化
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)

        # 总阅读计数+1
        readnum.read_num += 1
        readnum.save()

        # 当天阅读数+1
        date = timezone.now().date()
        # if ReadDetail.objects.filter(content_type=ct, object_id=obj.pk, date=date).count():
        #     readDetail = ReadDetail.objects.get(content_type=ct, object_id=obj.pk, date=date)
        #
        # else:
        #     readDetail = ReadDetail(content_type=ct, object_id=obj.pk, date=date)

        readdetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readdetail.read_num += 1
        readdetail.save()
    return key


def get_seven_days_read_data(content_type):
    """获取七天内的阅读记录"""
    today = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(7, 0, -1):
        # timedelta表示日期差量
        date = today - datetime.timedelta(days=i-1)
        dates.append(date.strftime('%m/%d'))
        read_detail = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_detail.aggregate(read_num_sum=Sum('read_num'))
        # 如果前面不为false就取前面的,如为false则取后面的
        read_nums.append(result['read_num_sum'] or 0)
    return dates, read_nums


def get_30_days_read_data(content_type):
    # 获取每个月的阅读记录
    months = []
    read_nums = []
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month

    for month in range(1, month+1):
        months.append(str(month) + '月')
        read_month_data = ReadDetail.objects.filter(content_type=content_type, date__year=year, date__month=month)
        result = read_month_data.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)

    return months, read_nums, year


def get_today_hot_data(content_type):
    """获取今日博客排行榜"""
    today = timezone.now().date()
    read_detail = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    return read_detail[:7]  # 前七条


def get_yesterday_hot_data(content_type):
    """获取昨天博客额排行榜"""
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_detail = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
    return read_detail[0:15]  # 前七条


def get_7_days_read_posts():
    """获取博客7天排行榜"""
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    posts = Post.objects \
        .filter(read_detail__date__lt=today, read_detail__date__gte=date) \
        .values('id', 'title') \
        .annotate(read_num_sum=Sum('read_detail__read_num')) \
        .order_by('-read_num_sum')
    return posts[:15]


def get_30_days_read_posts():
    """获取博客30天排行榜"""
    today = timezone.now().date()
    date = today - datetime.timedelta(days=30)
    posts = Post.objects \
        .filter(read_detail__date__lt=today, read_detail__date__gte=date) \
        .values('id', 'title') \
        .annotate(read_num_sum=Sum('read_detail__read_num')) \
        .order_by('-read_num_sum')
    return posts[:15]

def get_all_read_posts():
    """获取博客排行总榜"""
    today = timezone.now().date()
    date = today - datetime.timedelta(days=30)
    posts = Post.objects \
        .filter(read_detail__date__lt=today, read_detail__date__gte=date) \
        .values('id', 'title') \
        .annotate(read_num_sum=Sum('read_detail__read_num')) \
        .order_by('-read_num_sum')
    return posts[:15]
