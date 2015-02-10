# -*- coding: utf-8 -*-
from django.utils import timezone

from vkontakte_comments.models import Comment

from . models import Postcard



def send_postcard(album):
    cards = Postcard.objects.filter(comment=None).order_by('id')[:1]

    if not cards:
        return None

    c = cards[0]

    # upload photo
    if not c.photo:
        files = [c.image.file.name]
        c.photo = album.upload_photos(files)[0]

    # create comment
    receiver = u'[id%(receiver_id)s|%(receiver_name)s]' % {'receiver_id': c.receiver_id, 'receiver_name': c.receiver_name, }
    sender = u'[id%(sender_id)s|%(sender_name)s]' % {'sender_id': c.sender_id, 'sender_name': c.sender_name}

    text = c.comment_text
    text = text.replace('user1', receiver)
    text = text.replace('user2', sender)

    comment = Comment(text=text, object=c.photo, owner=album.owner, date=timezone.now())
    comment.save(commit_remote=True)

    c.comment = comment
    c.save()

    return c




# Mass upload for test purpose
# dos't set caption for photos
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

        # author=user,
        # create comment
        text = u'[id%(receiver_id)s|%(receiver_name)s], эту открытку тебе прислал [id%(sender_id)s|%(sender_name)s]' % {
            'receiver_id': c.receiver_id,
            'receiver_name': c.receiver_name,
            'sender_id': c.sender_id,
            'sender_name': c.sender_name}

        print text
        comment = Comment(text=text, object=c.photo, owner=album.owner, date=timezone.now())
        comment.save(commit_remote=True)

        c.comment = comment
        c.save()
