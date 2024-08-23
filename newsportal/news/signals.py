from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from .models import PostCategory, Post


def send_notification(preview, pk, title, subs, url):
    html_content = (f'Заголовок: {title}<br>'
                    f'Превью текста: {preview}<br><br>'
                    f'<a href="http://127.0.0.1:8000{url}">'
                    f'Ссылка на пост</a>')

    text_content = (f'Заголовок: {title}\n'
                    f'Превью текста: {preview}\n\n'
                    f'Ссылка на пост:  http://127.0.0.1:8000{url}')

    msg = EmailMultiAlternatives(subject=title, body=text_content, to=subs)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def post_created_notify(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        cats = instance.postCategory.all()
        subs = []

        for cat in cats:
            subs += cat.subscribers.all()

        subs = [s.email for s in subs]

        send_notification(instance.preview(), instance.pk, instance.title, subs, instance.get_absolute_url())


# @receiver(post_save, sender=Post)
# def post_created_noti(sender, created, instance, **kwargs):
#     if not created:
#         return
#
#     cats = instance.postCategory.all()
#     subs = []
#
#     for cat in cats:
#         subs += cat.subscribers.all()
#
#     subs = [s.email for s in subs]
#
#     send_notification(instance.preview(), instance.pk, instance.title, subs, instance.categoryType)



# @receiver(post_save, sender=Post)
# def post_created(instance, created, **kwargs):
#     if not created:
#         return
#
#     emails = User.objects.filter(
#         subscription__category=instance.postсategory__id
#     ).values_list('email', flat=True)
#
#     subject = f'Новая {"новость" if instance.categoryType == "News" else "статья"} в категории {instance.postCategory}'
#
#     text_content = (
#         f'Заголовок: {instance.title}\n'
#         f'Превью текста: {instance.preview()}\n\n'
#         f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
#     )
#     html_content = (
#         f'Заголовок: {instance.title}<br>'
#         f'Превью текста: {instance.preview()}<br><br>'
#         f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
#         f'Ссылка на пост</a>'
#     )
#     for email in emails:
#         msg = EmailMultiAlternatives(subject, text_content, None, [email])
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()
