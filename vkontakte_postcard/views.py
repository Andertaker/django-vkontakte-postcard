# -*- coding: utf-8 -*-
import csv
from django.db import connection
from django.http import HttpResponse

from vkontakte_groups.models import Group
from vkontakte_photos.models import Album, Photo
from vkontakte_postcard.post import send_postcard, send_postcard_x
from vkontakte_users.models import User


from . models import Postcard


POSTCARD_GROUP_ID = 59154616
POSTCARD_ALBUM_ID = 210546417

POSTCARD_GROUP_ID = 16297716 # cocacola
#POSTCARD_ALBUM_ID = 187237395 # Есть кто-то, кто очень любит тебя!
POSTCARD_ALBUM_ID = 211119701



def import_csv(request):
    print "____ import_csv"

    #f = open('csv/postcards2.csv')
    #print f.read()
    #return HttpResponse("END")

    cursor = connection.cursor()

    imported_records = []
    wrong_records = []

    with open('csv/postcards2.csv') as csvfile:
        #print dir(csvfile)
        #csvfile.encoding('utf-8')

        reader = csv.DictReader(csvfile)
        for row in reader:


            #row['image'] = 'blank'

            row['is_anonymous'] = (row['is_anonymous'] == 'Да')

            if not Postcard.objects.filter(id=row['id']).exists():
                print row

                if not row['image']:
                    pass
                elif len(row['receiver_name']) > 50 or len(row['sender_name']) > 50:
                    wrong_records.append(row['id'])
                elif not 'user1' in row['comment_text']:
                    wrong_records.append(row['id'])
                elif not row['receiver_id'] or not row['receiver_name']:
                    wrong_records.append(row['id'])
                #elif (not row['sender_id'] or not row['sender_name']) and not row['is_anonymous']:
                #    wrong_records.append(row['id'])
                else:

                    imported_records.append(row['id'])

                    if not row['sender_id']:
                        row['sender_id'] = None



                    cursor.execute(
                        '''
                            INSERT INTO vkontakte_postcard_postcard (id,image,comment_text,receiver_name,sender_name,receiver_id,sender_id,is_anonymous,created_at)
                            VALUES (%(id)s,%(image)s,%(comment_text)s,%(receiver_name)s,%(sender_name)s,%(receiver_id)s,%(sender_id)s,%(is_anonymous)s,NOW())

                        ''', row)


            #break;
        #print reader[0]

    if imported_records:
        print imported_records

    if wrong_records:
        print wrong_records

    return HttpResponse("END")

def send_postcards(request):
    group = Group.remote.fetch(ids=[POSTCARD_GROUP_ID])[0]
    album = Album.remote.fetch(owner=group, ids=[POSTCARD_ALBUM_ID])[0]

    while 1:
        c = send_postcard_x(album)
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
