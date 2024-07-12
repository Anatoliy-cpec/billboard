from .models import Author, Message, Advertisement
import random
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.signals import request_finished




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.author.save()

@receiver(m2m_changed, sender=Advertisement.response.through)
def notify_about_new_response(sender, instance, pk_set, *args, **kwargs):

    if kwargs['action'] == 'post_add':
        advertisement = instance
        response = Message.objects.get(pk__in=pk_set)

        subject = f'{response.author.user.username} откликнулся на ваш зов'
        text = f'{response.author.user.username} отправил отклик на одно из ваших объявлений'
        html = (
            f'<b>{response.author.user.username}</b>, откликнулся на ваше объявление '
            f'<a href="http://127.0.0.1:8000/advertisements/{advertisement.id}/responses/">тут</a>!'
        )
        msg = EmailMultiAlternatives(subject=subject, body=text, from_email=None, to=[advertisement.author.user.email])
        msg.attach_alternative(html, "text/html")
        # msg.send()


@receiver(m2m_changed, sender=Advertisement.accepted_authors.through)
def notify_about_author_add(sender, instance, pk_set, *args, **kwargs):

    if kwargs['action'] == 'post_add':
        advertisement = instance
        author = Author.objects.get(pk__in=pk_set)

        subject = f'{advertisement.author.user.username} принял ваш отклик'
        text = f'{advertisement.author.user.username} принял вашу помощь, вы зачислены в лобби'
        html = (
            f'<b>{advertisement.author.user.username}</b>, принял вашу помощь, вы можете ознакомиться с лобби  '
            f'<a href="http://127.0.0.1:8000/advertisements/{advertisement.id}">тут</a>!'
        )
        msg = EmailMultiAlternatives(subject=subject, body=text, from_email=None, to=[author.user.email])
        msg.attach_alternative(html, "text/html")
        # msg.send()

@receiver(post_save, sender=Advertisement)
def notify_about_close(sender, instance, dispatch_uid=random.randint(0, 1000), *args, **kwargs):
            

            advertisement = instance
            authors = Author.objects.get_queryset().order_by('id')

            if advertisement.state == Advertisement.AdvertisementState.finished:
                 
                    for author in authors:
                        print(author, '| author;')
                        if author in advertisement.liked_authors.all():
                            print(author, '| author liked ;')
                            subject = f'{advertisement.author.user.username} закрыл объявление'
                            text = f'{advertisement.author.user.username} оценил вас'
                            html = (
                                f'<b>{author.user.username}, {advertisement.author.user.username}</b>, оценил вас лайком! Просмотреть резуьтат можно  '
                                f'<a href="http://127.0.0.1:8000/advertisements/{advertisement.id}">тут</a>!'
                            )
                            msg = EmailMultiAlternatives(subject=subject, body=text, from_email=None, to=[author.user.email])
                            msg.attach_alternative(html, "text/html")
                            # msg.send()

                        elif author in advertisement.disliked_authors.all():
                            print(author, '| author disliked ;')
                            subject = f'{advertisement.author.user.username} закрыл объявление'
                            text = f'{advertisement.author.user.username} оценил вас'
                            html = (
                                f'<b>{advertisement.author.user.username}</b>, оценил вас дизлайком! Просмотреть резуьтат можно  '
                                f'<a href="http://127.0.0.1:8000/advertisements/{advertisement.id}">тут</a>!'
                            )
                            msg = EmailMultiAlternatives(subject=subject, body=text, from_email=None, to=[author.user.email])
                            msg.attach_alternative(html, "text/html")
                            # msg.send()
                        else:
                            pass
                    


