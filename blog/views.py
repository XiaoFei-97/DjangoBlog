from django.shortcuts import get_object_or_404, render
from .models import Post, Category  # ReadNum
# from comment.models import Comment   # 导入Comment评论模块
from django.core.paginator import *   # 导入分页功能
from django.core.cache import cache  # 缓存数据
from django.conf import settings   # 导入settings,可以使用其中自定义的全局变量
from read_statistics.utils import read_statistics_once_read, get_seven_days_read_data, get_30_days_read_data,  get_today_hot_data,\
    get_yesterday_hot_data, get_7_days_read_posts, get_30_days_read_posts, rank_all_read_num # 导入自定义工具包
from django.contrib.contenttypes.models import ContentType
# contenttypes 是Django内置的一个应用，可以追踪项目中所有app和model的对应关系，并记录在ContentType表中
# from comment.models import Comment
# from comment.forms import CommentForm
from user.forms import LoginForm


def home(request):
    """网站的首页"""
    # 从django内置应用中获取Post的表结构
    post_content_type = ContentType.objects.get_for_model(Post)
    # 使用自定义的utils工具包get_seven_days_read_data,获取出post对应日期的和该日期阅读计数的总和
    seven_dates, seven_read_nums = get_seven_days_read_data(post_content_type)
    thirty_dates, thirty_read_nums = get_30_days_read_data(post_content_type)
    # 获取7天热门博客的缓存数据
    last_7_days_hot_data = cache.get('last_7_days_hot_data')
    if last_7_days_hot_data is None:
        last_7_days_hot_data = get_7_days_read_posts()
        # 60*60表示60秒*60,也就是1小时
        cache.set('last_7_days_hot_data', last_7_days_hot_data, 60*60)

    # 今日热门博客数据
    today_hot_data = get_today_hot_data(post_content_type)
    # 昨天热门博客
    yesterday_hot_data = get_yesterday_hot_data(post_content_type)
    # 过去七天热门博客
    last_7_days_hot_data = get_7_days_read_posts()
    # 过去三十天热门博客
    last_30_days_hot_data = get_30_days_read_posts()

    context = {'seven_read_nums': seven_read_nums, 'seven_dates': seven_dates,
               'thirty_read_nums': thirty_read_nums, 'thirty_dates': thirty_dates,
               'today_hot_data': today_hot_data,
               'yesterday_hot_data': yesterday_hot_data,
               'last_7_days_hot_data': last_7_days_hot_data,
               'last_30_days_hot_data': last_30_days_hot_data,
               }

    return render(request, 'home.html', context)


def get_blog_list_common_data(request, blogs_all_list):
    """这是一个博客列表,分类列表,时间排序列表的公共分页部分代码"""
    paginator = Paginator(blogs_all_list, settings.EACH_RAGE_BLOG_NUMBER)  # 每十个篇进行分页
    page_num = request.GET.get('page', 1)  # get获取页码请求
    # 因为用户输入不一定是数字,所以需要用int(page_num),而django里的get_page会自动识别用户输入以及页码范围
    # 注意这里的page_of_list是一个paginator对象
    page_of_list = paginator.page(int(page_num))
    current_page_num = page_of_list.number  # 获取当前页码
    # page_range = [current_page_num - 2, current_page_num - 1,
    # current_page_num, current_page_num + 1, current_page_num + 2]
    # 获取当前页码前后各两页的页码范围
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
                 list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))

    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')

    # 加上首页尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    post_dates = Post.objects.dates('created_time', 'month', order='DESC')
    # post_list是文章的集合
    # post_list = Post.objects.all().order_by('-created_time')
    category_list = Category.objects.all()
    # count()是延伸下来的方法
    # post_count = Post.objects.all().count()

    # 获取博客分类对应的博客数量
    post_category_list = []
    for category in category_list:
        category.post_count = Post.objects.filter(category=category).count()
        post_category_list.append(category)

    # 获取日期归档对应的博客数量
    # 利用字典
    post_date_dict = {}
    for post_date in post_dates:
        post_date_count = Post.objects.filter(created_time__year=post_date.year, created_time__month=post_date.month).count()
        post_date_dict[post_date] = post_date_count

    # 获取阅读量最大的总榜博客
    post_content_type = ContentType.objects.get_for_model(Post)
    hot_posts = rank_all_read_num(post_content_type)

    # context用来渲染模板
    context = {'post_list': page_of_list.object_list,
               'page_of_list': page_of_list,
               'category_list': category_list,
               'page_range': page_range,
               'post_dates': post_date_dict,
               'hot_posts': hot_posts,
               }
    return context


def blog(request):
    """ip根目录首页的显示"""
    post_all_list = Post.objects.all()
    # 使用公共的get_blog_list_common_data的方法
    context = get_blog_list_common_data(request, post_all_list)

    # 给request返回一个index.html文件
    return render(request, 'blog/blog.html', context)


def detail(request, pk):
    """显示当前选择文章内容"""
    # 接收了一个pk值,这个值是在url中传递的主键,利用该主键可以找到文章的对象
    # get_object_or_404的用法是(模型名,get方法)
    post = get_object_or_404(Post, pk=pk)
    post_all_list = Post.objects.all()
    # 使用公共的get_blog_list_common_data的方法
    context = get_blog_list_common_data(request, post_all_list)

    # read_statistics_once_read是在read_statistics应用中的方法,表示计数+1
    read_cookie_key = read_statistics_once_read(request, post)

    post_content_type = ContentType.objects.get_for_model(Post)
    # comments = Comment.objects.filter(content_type=post_content_type, object_id=post.pk, parent=None)

    # 在django中不能使用>=或<=,所以django自定义了__gt和__lt
    # 目的:得出创建时间比当前博客创建时间较晚的所有博客列表的最后一篇博客,也就是当前博客的上一篇
    # 因为博客是按照创建时间的先后来排序的:即先创建的靠后,那么上一篇博客创建时间晚于当前博客
    previous_post = Post.objects.filter(created_time__gt=post.created_time).last()

    # 目的:得出创建时间比当前博客创建时间较早的所有博客列表的第一篇博客,也就是当前博客的下一篇
    # 因为博客是按照创建时间的先后来排序的:即先创建的靠后,那么上一篇博客创建时间早于当前博客
    next_post = Post.objects.filter(created_time__lt=post.created_time).first()

    context.update({'article': post.body, 'title': post.title,
               'author': post.author, 'created_time': post.created_time,
               'category': post.category, 'previous_post': previous_post,
               'next_post': next_post, 'read_num': post.get_read_num,
               'user': request.user, 'post_id': post.id, 'post': post,
               'login_form': LoginForm()
               # 'comments': comments.order_by('-comment_time'),
               # 'comment_form': CommentForm(initial={'content_type': post_content_type.model, 'object_id': pk, 'reply_comment_id': 0}),
               # 'comment_count':Comment.objects.filter(content_type=post_content_type, object_id=post.pk).count()
               })
    response = render(request, 'blog/detail.html', context)
    # 第一个参数是键,键值,和过期时间
    response.set_cookie(read_cookie_key, 'true')  # 阅读cookie标记
    return response


def category_list(request):
    """博客分类"""
    # 获得所有的分类
    category_list = Category.objects.all()

    context = {'category_list':category_list}
    return render(request, 'blog/category_list.html', context)


def category(request, pk):
    """显示全部文章分类"""
    category1 = get_object_or_404(Category, pk=pk)
    # 因为从url中获得了一个category的pk,就可以在post中进行过滤
    post_list = Post.objects.all().filter(category=category1)

    # 使用公共部分的 get_blog_list_common_data方法
    context = get_blog_list_common_data(request, post_list)

    # 新增了一个当前分类名称的键
    context.update({'category_name': category1.name})
    # 给request返回一个index.html文件

    return render(request, 'blog/category.html', context)


def date_list(request):
    """日期归档"""
    # date_list = []
    date_list = Post.objects.dates('created_time', 'month', order='DESC')
    # for post_date in post_dates:
    #     date_list.append(str(post_date.year) +'年' + str(post_date.month) + '月')

    context = {'date_list': date_list}
    return render(request, 'blog/date_list.html', context)

def date(request, year, month):
    """日期归档分类"""
    # django比较坑的地方就是使用mysql存储数据时，因为时区的问题无法得到Asia/Shanghai的时间，即无法过滤出月份
    # 在这里采用的方法是先将月份转化为字符串的形式，然后再使用，发现可行
    month1 = str(month)

    post_list = Post.objects.all().filter(created_time__year=year, created_time__month=month1)
    # 将年月拼接一下
    post_time = year+'年'+month+'月'

    context = get_blog_list_common_data(request, post_list)
    context.update({'post_time': post_time})

    return render(request, 'blog/date.html', context)

def search_list(request):
    # 搜索功能的逻辑处理
    return render(request, 'search/search.html')
