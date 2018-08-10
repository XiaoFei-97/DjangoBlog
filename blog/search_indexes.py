from haystack import indexes
from haystack.views import SearchView
from read_statistics.utils import get_random_recomment, get_new_recommend_post, get_all_read_posts
from django.contrib.contenttypes.fields import ContentType
from .models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    # 创建文章索引类
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class MySeachView(SearchView):
    def extra_context(self):  # 重载extra_context来添加额外的context内容
        context = super(MySeachView, self).extra_context()
        # 随机推荐的15篇博客
        random_recommend = get_random_recomment()

        # 最新推荐的15篇博客
        post_content_type = ContentType.objects.get_for_model(Post)
        new_recommend = get_new_recommend_post(post_content_type)

        # 阅读量总榜博客榜单
        all_hot_posts = get_all_read_posts()
        context = {
                   'random_recommend': random_recommend,
                   'new_recommend': new_recommend,
                   'all_hot_posts': all_hot_posts,
                   }
        return context
