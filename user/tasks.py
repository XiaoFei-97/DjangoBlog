from __future__ import absolute_import
from django.core.mail import send_mail
from celery import shared_task


@shared_task
def send_email_by_celery(code, email):
    """
    作用：使用celery异步发送邮件
    :param code: 验证码
    :param email: 邮件内容
    """
    try:
        send_mail(
            '绑定邮箱',
            '验证码: %s' % code,
            'XiaoFei-97@outlook.com',
            [email],
            fail_silently=False,
        )
    except Exception:
        # 出错尝试重新执行1次任务
        send_email_by_celery(code, email)
