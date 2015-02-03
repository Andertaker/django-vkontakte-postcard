# -*- coding: utf-8 -*-

from . models import Postcard
from django.core.files.storage import FileSystemStorage



def upload_postcard_images(album):

    #cards = Postcard.objects.filter(photo=None)[:1]
    cards = Postcard.objects.all()[:1]

    if not cards:
        return None

    files = []
    for c in cards:
        files.append(c.image.file.name)

    photos = album.upload_photos(files)

    for i, c in enumerate(cards):
        c.photo = photos[i]
        c.save()
