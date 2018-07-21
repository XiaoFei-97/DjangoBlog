from django.db import models
from django.db.models.fields import exceptions
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone


class ReadNum(models.Model):
    """单篇博客计数的模型类"""
    read_num = models.IntegerField(u'阅读计数', default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    # 使用contenttypes模型类来找出关联blog
    content_object = GenericForeignKey('content_type', 'object_id')


    class Meta:
        verbose_name = '阅读计数'
        verbose_name_plural = '阅读计数'
        ordering = ['-read_num']




class ReadNumExpandMethod(object):
    """计数扩展类,此方法放在admin的list_display中"""
    def get_read_num(self):
        ct = ContentType.objects.get_for_model(self)
        # 此处的一个异常处理,用来捕获没有计数对象的情况
        # 例如在admin后台中,没有计数值会显示为‘-’
        try:
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)
            return readnum.read_num
        # 对象不存在就返回0
        except exceptions.ObjectDoesNotExist:
            return 0


class ReadDetail(models.Model):
    """根据日期计数的模型类"""
    read_num = models.IntegerField(default=0)
    date = models.DateField(default=timezone.now)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = '阅读记录'
        verbose_name_plural = '阅读记录'
        ordering = ['-date']

