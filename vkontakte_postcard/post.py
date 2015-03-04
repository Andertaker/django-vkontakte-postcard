# -*- coding: utf-8 -*-
from django.utils import timezone

from vkontakte_comments.models import Comment

from . models import Postcard



def send_postcard(album):
    '''
        Отправляет открытки и оставляет комменты к ним
    '''
    # TODO: Может быть вызвана лишь 3 раза подряд дальше требует капчу

    cards = Postcard.objects.filter(comment=None).order_by('id')[:1] # , id__gt=458

    if not cards:
        return None

    c = cards[0]

    # upload photo
    if not c.photo:
        files = [c.image.file.name]
        c.photo = album.upload_photos(files)[0]
        c.save()

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


def send_postcard_x(album):
    """
        Посылает открытки и с подписью
        эту подпись потом можно скопипастить, чтобы оставить коммент
        если будет коммент тогда будут отпрвлены уведомления (это уже ВК рассылает)
    """

    cards = Postcard.objects.filter(photo=None, id__gt=459).order_by('id')[:1] #

    if not cards:
        return None

    c = cards[0]

    print c.id

    # create comment
    receiver = u'[id%(receiver_id)s|%(receiver_name)s]' % {'receiver_id': c.receiver_id, 'receiver_name': c.receiver_name, }
    sender = u'[id%(sender_id)s|%(sender_name)s]' % {'sender_id': c.sender_id, 'sender_name': c.sender_name}

    text = c.comment_text
    text = text.replace('user1', receiver)
    text = text.replace('user2', sender)

    # upload photo
    if not c.photo:
        files = [c.image.file.name]
        c.photo = album.upload_photos(files, caption=text)[0]
        c.save()


    return c








def send_postcard2(album):
    cards = Postcard.objects.filter(comment=None, id__gt=458).order_by('id')[:10]

    if not cards:
        return None

    files = []
    for c in cards:
        if not c.photo:
            files.append(c.image.file.name)


    photos = album.upload_photos(files)

    for i, c in enumerate(cards):
        c.photo = photos[i]
        c.save()

        # upload photo
        if not c.photo:
            files = [c.image.file.name]
            c.photo = album.upload_photos(files)[0]
            c.save()

    for c in cards:
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

        print "postcard %s was sended" % c.id

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
