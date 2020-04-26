from django.db import models
from django.contrib.postgres.fields import JSONField
from rest_framework.utils.encoders import JSONEncoder
# Create your models here.


class Bookinfo(models.Model):
    sid = models.IntegerField(primary_key=True)
    name = models.TextField(null=True)
    star = models.TextField(null=True)
    tag = models.TextField(null=True)
    score = models.TextField(null=True)
    info = models.TextField(null=True)
    tfidf = JSONField(null=True)
    pesg_name = JSONField(null=True)
    pesg_list = JSONField(null=True)
    word_cloud = models.TextField(null=True)

    class Meta:
        # db_table = "book_info"
        verbose_name = '图书信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Bookcomment(models.Model):
    sid = models.IntegerField(null=True)
    # bookinfo = models.ForeignKey('Bookinfo', on_delete=models.PROTECT)
    num = models.TextField(null=True)
    name = models.TextField(null=True)
    time = models.TextField(null=True)
    like_num = models.TextField(null=True)
    comment = models.TextField(null=True)
    snow_nlp = models.TextField(null=True)

    class Meta:
        # db_table = "book_comment"
        verbose_name = '图书评论'
        verbose_name_plural = verbose_name


if __name__ == "__main__":
    pass
