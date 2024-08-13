from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse


class Author(models.Model):
    authorName = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        ratingPost = Post.objects.filter(author=self).aggregate(models.Sum('rating'))['rating__sum']
        ratingComment = Comment.objects.filter(user=self.authorName).aggregate(models.Sum('rating'))['rating__sum']
        ratingPostComments = Comment.objects.filter(post__author=self).aggregate(models.Sum('rating'))['rating__sum']

        self.rating = ratingPost * 3 + ratingComment + ratingPostComments
        self.save()


class Category(models.Model):
    categoryName = models.CharField(max_length=50, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    TYPE = (
        ('News', 'Новость'),
        ('Article', 'Статья')
    )
    categoryType = models.CharField(max_length=7, choices=TYPE)
    creationDate = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=150)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:21]}...'

    def get_absolute_url(self):
        return reverse(f'{str(self.categoryType).lower()}_detail', kwargs={'pk': self.pk})


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    creationDate = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
