# -*- coding: utf-8 -*-
from django.db import models

from vkontakte_comments.models import Comment
from vkontakte_photos.models import Photo


class Postcard(models.Model):

    image = models.ImageField("Изображние открытки", upload_to="postcards")
    comment_text = models.TextField("Текст комментария")
    sender_id = models.BigIntegerField()
    sender_name = models.CharField("Имя отправителя", max_length=30)
    receiver_id = models.BigIntegerField()
    receiver_name = models.CharField("Имя получателя", max_length=30)

    photo = models.ForeignKey(Photo)
    comment = models.ForeignKey(Comment)
