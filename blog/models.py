from django.db import models
from django.contrib.auth.models import  AbstractUser
from django_ckeditor_5.fields import CKEditor5Field

class User(AbstractUser):
    ROLE_CHOICES =(
        ('admin', 'Адміністратор'),
        ('moderator', 'Модератор'),
        ('user', 'Користувач'),
    )

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username
class Post(models.Model):
    title = models.CharField(max_length=255)

    content = CKEditor5Field('Контент', config_name='extends')

    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Коментар від {self.author.username} до {self.post.title}"
