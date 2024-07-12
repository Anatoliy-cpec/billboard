from django.db import models
from django.contrib.auth.models import User



class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    profile_photo = models.ImageField(default='images/no_avatar.jpg', blank=True, null=True, upload_to='images/%Y/%m/%d/')
    bio = models.TextField(default=None, blank=True, null=True, max_length=400)
    first_name = models.CharField(max_length=15, blank=True, null=True,)

    def __str__(self) -> str:
        return self.user.username

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()




class Category(models.Model):
    category_name = models.CharField(max_length=12)

    def __str__(self) -> str:
        return self.category_name
    
class Message(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор', name='author')
    message_text = models.CharField(max_length=64, verbose_name='Текст')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self) -> str:
        return (f'{self.message_text[0:15]}...')

class Advertisement(models.Model):

    class AdvertisementState(models.TextChoices):

        in_progress = 'IN'
        unfinished = 'UN'
        finished = 'FI'

    state = models.CharField(
        max_length=2,
        choices=AdvertisementState,
        default=AdvertisementState.in_progress,
    )

    header = models.CharField(max_length=40, verbose_name='Заголовок')
    body = models.TextField(max_length=300, verbose_name='Содержание')
    file_1 = models.FileField(verbose_name='Файл 1', blank=True, null=True, upload_to='files/%Y/%m/%d/')
    file_2 = models.FileField(verbose_name='Файл 2', blank=True, null=True, upload_to='files/%Y/%m/%d/')
    file_3 = models.FileField(verbose_name='Файл 3', blank=True, null=True, upload_to='files/%Y/%m/%d/')
    header_image = models.FileField(verbose_name='Обложка', blank=True, null=True, upload_to='files/%Y/%m/%d/')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.BooleanField(default=True, verbose_name='Статус')
    slots = models.PositiveIntegerField(default=1, verbose_name = 'Слотов доступно')
    chat_id = models.PositiveIntegerField(default=0, blank=True, null=True)

    
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='author', verbose_name='Автор')
    viewers = models.ManyToManyField(Author, verbose_name='Просмотры', related_name='viewers', blank=True)
    category = models.ManyToManyField(Category, verbose_name='Категория')
    response = models.ManyToManyField(Message, verbose_name='Отклики', blank=True, related_name='responses')
    accepted_authors = models.ManyToManyField(Author, verbose_name='Участники', blank=True, related_name='accepted_users')
    liked_authors = models.ManyToManyField(Author, verbose_name='Лайки', blank=True, related_name='liked_authors')
    disliked_authors = models.ManyToManyField(Author, verbose_name='Дизлайки', blank=True, related_name='disliked_authors')

    def rating_confirmation(self):
        
        if self.liked_authors:
            for author in self.liked_authors.all():
                author.like()

        if self.disliked_authors:
            for author in self.disliked_authors.all():
                author.dislike()


    @property
    def is_all_liked(self):
        count = self.liked_authors.all().count() + self.disliked_authors.all().count()
        users_count = self.accepted_authors.all().count()
        if count == users_count:
            return True
        else: return False
        


    def change_status(self):
        if self.state == 'IN':
            if self.slots <= 0:
                self.status = False
                self.save()
            else:
                self.status = True
                self.save()
            return self.status

    def add_author(self, user):
        if self.state == 'IN':
            if self.slots > 0 and not user in self.accepted_authors.all():
                self.accepted_authors.add(user)
                self.slots -= 1
                self.save()
                self.change_status()
                return True
            else:
                return False
        
    def remove_author(self, user):
        if self.state == 'IN':
            if self.slots > 0 and user in self.accepted_authors.all():
                self.accepted_authors.remove(user)
                self.slots += 1
                self.save()
                self.change_status()
                return True
            else:
                return False

    def delete_response(self, response_pk):
        if self.state == 'IN':
            if self.response.get(pk=response_pk):
                response = self.response.get(pk=response_pk)
                self.response.remove(response)
                response.delete()
                self.save()
                return True
            else:
                return False

    def views_conuter_add(self, viewer):
        if self.state == 'IN':
            if viewer not in self.viewers.all():
                self.viewers.add(viewer)
                self.save()
                return True
            else:
                return False

        
    def get_all_advertisement_users(self):
        _users = []
        _users.append(self.author.user)
        for user in self.accepted_authors.all():
            _users.append(user.user)

        return _users

    def __str__(self) -> str:
        return f'{self.header}'
