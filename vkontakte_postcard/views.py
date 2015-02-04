# -*- coding: utf-8 -*-
from django.http import HttpResponse

from vkontakte_groups.models import Group
from vkontakte_photos.models import Album, Photo
from vkontakte_postcard.post import send_postcard
from vkontakte_users.models import User


POSTCARD_GROUP_ID = 59154616
POSTCARD_ALBUM_ID = 210546417

#POSTCARD_GROUP_ID = 16297716 # cocacola
#POSTCARD_ALBUM_ID = 187237395 # Есть кто-то, кто очень любит тебя!



def send_postcards(request):
    group = Group.remote.fetch(ids=[POSTCARD_GROUP_ID])[0]
    album = Album.remote.fetch(owner=group, ids=[POSTCARD_ALBUM_ID])[0]

    while 1:
        c = send_postcard(album)
        if c:
            print "postcard %s was sended" % c.id
        else:
            break;

    return HttpResponse("END")


def send_user_postcards(request):
    user = User.remote.fetch(ids=[201164356])[0]
    album = Album.remote.fetch(owner=user, ids=[209873101])[0]

    while 1:
        c = send_postcard(album)
        if c:
            print "postcard %s was sended" % c.id
        else:
            break;

    return HttpResponse("END")
