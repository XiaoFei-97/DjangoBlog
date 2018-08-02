from django.shortcuts import get_object_or_404, render
from .models import Post, Category  # ReadNum
from django.core.paginator import *   # 导入分页功能
from django.conf import settings   # 导入settings,可以使用其中自定义的全局变量
from read_statistics.utils import read_statistics_once_read, get_seven_days_read_data, \
                                get_year_read_data, get_new_recommend_post, get_random_recomment, \
                                get_7_days_read_posts, get_30_days_read_posts, get_all_read_posts  # 导入自定义工具包
# contenttypes 是Django内置的一个应用，可以追踪项目中所有app和model的对应关系，并记录在ContentType表中
from django.contrib.contenttypes.models import ContentType
from user.forms import LoginForm  # 导入登录表单
# from django.core.cache import cache  # 缓存数据
# from comment.forms import CommentForm  # 导入评论表单
# from comment.models import Comment   # 导入Comment评论模块


def home(request):
    """
        作用:网站首页的视图处理
        request:请求对象
    """
    # 所有分类
    category_list = Category.objects.all()

    # 所有博客列表
    post_list = Post.objects.all()

    # 最新发表的15篇博客
    new_publish = Post.objects.all()[:15]

    # 获取Post模型类或模型的实例，并返回ContentType表示该模型的实例
    post_content_type = ContentType.objects.get_for_model(Post)

    # 最新推荐的15篇博客
    new_recommend = get_new_recommend_post(post_content_type)

    # 随机推荐的15篇博客
    random_recommend = get_random_recomment()

    # 使用自定义的utils工具包get_seven_days_read_data,取出七天内每天的阅读计数总和
    seven_dates, seven_read_nums = get_seven_days_read_data(post_content_type)

    # 使用自定义的utils工具包get_year_read_data,取出当年每月的阅读计数总和
    thirty_dates, thirty_read_nums, year = get_year_read_data(post_content_type)

    # 阅读量周榜博客榜单
    last_7_days_hot_data = get_7_days_read_posts()

    # 阅读量月榜博客榜单
    last_30_days_hot_data = get_30_days_read_posts()

    # 阅读量总榜博客榜单
    all_hot_posts = get_all_read_posts()

    # 获取7天热门博客的缓存数据
    # last_7_days_hot_data = cache.get('last_7_days_hot_data')
    # if last_7_days_hot_data is None:
    #     last_7_days_hot_data = get_7_days_read_posts()
    #     # 60*60表示60秒*60,也就是1小时
    #     cache.set('last_7_days_hot_data', last_7_days_hot_data, 60*60)

    # 今日热门博客数据
    # today_hot_data = get_today_hot_data(post_content_type)

    # context用来渲染模板
    context = {
        'category_list': category_list, 'post_count': post_list.count,
        'new_publish':new_publish, 'new_recommend': new_recommend,
        'random_recommend':random_recommend, 'seven_dates': seven_dates,
        'seven_read_nums': seven_read_nums, 'thirty_dates': thirty_dates,
        'thirty_read_nums': thirty_read_nums, 'year': str(year),
        'last_7_days_hot_data': last_7_days_hot_data, 'last_30_days_hot_data': last_30_days_hot_data,
        'all_hot_posts': all_hot_posts,
        # 'today_hot_data': today_hot_data,
    }
    return render(request, 'home.html', context)


def get_blog_list_common_data(request, post_all_list):
    """
        作用:博客列表,分类列表,时间排序列表的公共分页代码
        request:请求对象
        post_all_list:经过处理后的博客列表
    """
    # 创建一个分页器对象,参数分别是文章列表,每页最大文章数量
    # 这里的EACH_RAGE_BLOG_NUMBER等于10,已经当成常量写进了seetings里
    paginator = Paginator(post_all_list, settings.EACH_RAGE_BLOG_NUMBER)

    # 采用get方式获取用户访问的页码,如果获取不到,默认为第一页
    page_num = request.GET.get('page', 1)

    # 因为用户输入不一定是数字,所以需要用int(page_num),而django里的get_page会自动识别用户输入以及页码范围
    # 注意这里的page_of_list是一个paginator对象
    page_of_list = paginator.page(int(page_num))

    # 获取当前页码
    current_page_num = page_of_list.number

    # page_range = [current_page_num - 2, current_page_num - 1,
    # current_page_num, current_page_num + 1, current_page_num + 2]

    # 获取当前页码前后各两页的页码范围
    # 需要注意判断的是:如果当前页是第一页,那么前两页不能是0,也不能是-1,所以要使用内置max函数来与1比较最大值
    # 同理:如果当前页已经是最后一页,那么就不能取到当前页+2的页码了,所以要使用内置min函数来与最大页码比较最小值
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
                 list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))

    # 加上省略页码标记
    # paginator.num_pages表示一共有多少页码
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')

    # 加上首页尾页
    # paginator.num_pages表示一共有多少页码
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 所有博客的列表,且按时间越早创建越靠后排
    # post_list = Post.objects.all().order_by('-created_time')

    # count()是延伸下来的方法,用于计算总博客的数量
    # post_count = Post.objects.all().count()

    # 获取所有的分类
    category_list = Category.objects.all()

    # 获取博客分类对应的博客数量
    # 给每个category对象绑定post_count字段
    post_category_list = []
    for category in category_list:
        category.post_count = Post.objects.filter(category=category).count()
        post_category_list.append(category)

    # 获取博客的创建时间,且按创建时间月份排序
    post_dates = Post.objects.dates('created_time', 'month', order='DESC')

    # 获取日期归档对应的博客数量
    # 利用字典
    post_date_dict = {}
    for post_date in post_dates:
        post_date_count = Post.objects.filter(created_time__year=post_date.year, created_time__month=post_date.month).count()
        post_date_dict[post_date] = post_date_count

    # 随机推荐的15篇博客
    random_recommend = get_random_recomment()

    # 最新推荐的15篇博客
    post_content_type = ContentType.objects.get_for_model(Post)
    new_recommend = get_new_recommend_post(post_content_type)

    # 阅读量总榜博客榜单
    all_hot_posts = get_all_read_posts()

    # context用来渲染模板
    context = {'post_list': page_of_list.object_list,
               'page_of_list': page_of_list,
               'category_list': category_list,
               'page_range': page_range,
               'post_dates': post_date_dict,
               'random_recommend': random_recommend,
               'new_recommend': new_recommend,
               'all_hot_posts': all_hot_posts,
               }
    return context


def blog(request):
    """
        作用：博客列表的视图处理
        request: 请求对象
    """
    post_all_list = Post.objects.all()

    # 使用公共的get_blog_list_common_data的方法
    context = get_blog_list_common_data(request, post_all_list)

    # 给request返回一个blog.html文件
    return render(request, 'blog/blog.html', context)


def detail(request, pk):
    """
        作用：显示当前选择文章内容
        request:请求对象
        pk：每篇文章的pk值
    """
    # 接收了一个pk值,这个值是在url中传递的主键,利用该主键可以找到文章的对象
    # get_object_or_404的用法是(模型名,get方法)
    post = get_object_or_404(Post, pk=pk)
    post_all_list = Post.objects.all()

    # 使用公共的get_blog_list_common_data的方法
    context = get_blog_list_common_data(request, post_all_list)

    # read_statistics_once_read是在read_statistics应用中的方法,表示计数+1
    read_cookie_key = read_statistics_once_read(request, post)

    # post_content_type = ContentType.objects.get_for_model(Post)
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
                    'login_form': LoginForm(),
                    # 'comments': comments.order_by('-comment_time'),
                    # 'comment_form': CommentForm(initial={'content_type': post_content_type.model, 'object_id': pk, 'reply_comment_id': 0}),
                    # 'comment_count':Comment.objects.filter(content_type=post_content_type, object_id=post.pk).count()
               })
    response = render(request, 'blog/detail.html', context)

    # 第一个参数是键,键值,和过期时间
    response.set_cookie(read_cookie_key, 'true')  # 阅读cookie标记
    return response


def category_list(request):
    """
        作用：博客分类的视图处理
        request：请求对象
    """
    # 获得所有的分类
    category_list = Category.objects.all()

    context = {'category_list': category_list}
    return render(request, 'blog/category_list.html', context)


def category(request, pk):
    """
        作用：显示某分类下的全部文章
        pk：分类的主键值
    """
    category = get_object_or_404(Category, pk=pk)

    # 因为从url中获得了一个category的pk,就可以在post中进行过滤
    post_list = Post.objects.all().filter(category=category)

    # 使用公共部分的 get_blog_list_common_data方法
    context = get_blog_list_common_data(request, post_list)

    # 新增了一个当前分类名称的键
    context.update({'category_name': category.name})

    # 给request返回一个category.html文件
    return render(request, 'blog/category.html', context)


def date_list(request):
    """
        作用：日期归档的视图处理
        request：请求对象
    """
    # date_list = []
    date_list = Post.objects.dates('created_time', 'month', order='DESC')
    post_count = Post.objects.all().count()
    # for post_date in date_list:
    #     date_list.append(str(post_date.year) +'年' + str(post_date.month) + '月')

    context = {'date_list': date_list,
               'post_count': post_count,}
    return render(request, 'blog/date_list.html', context)


def date(request, year, month):
    """
        作用：显示某归档下的全部文章
    """
    # django比较坑的地方就是使用mysql存储数据时，因为时区的问题无法得到Asia/Shanghai的时间，即无法过滤出月份
    # 在这里采用的方法是先将月份转化为字符串的形式，然后再使用，发现可行
    month = str(month)

    post_list = Post.objects.all().filter(created_time__year=year, created_time__month=month)
    # 将年月拼接一下
    post_time = year+'年'+month+'月'

    context = get_blog_list_common_data(request, post_list)
    context.update({'post_time': post_time})

    return render(request, 'blog/date.html', context)


def search_list(request):
    # 搜索功能的逻辑处理
    return render(request, 'search/search.html')
