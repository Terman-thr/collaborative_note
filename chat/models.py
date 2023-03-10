from django.db import models


# Create your models here.
class Text(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    text = models.TextField()


class Note(models.Model):
    articleId = models.IntegerField()
    commentId = models.IntegerField()
    comment = models.TextField()

