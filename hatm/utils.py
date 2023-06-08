import random
import datetime
from .models import Hatm, Juz


def create_or_publish_public_hatm(user):
    #get not published public hatms sorted by creation date
    hatms = Hatm.objects.filter(is_public=True, is_published=False).order_by('created_at')
    if len(hatms) > 0:
        hatm = hatms[0]
        hatm.is_published = True
        hatm.save()
    else:
        hatm = Hatm.objects.create(user=user, is_public=True, is_published=True)
    return hatm


def is_all_completed(hatm_id):
    juzs = Juz.objects.filter(hatm_id=hatm_id, type='juz')
    for juz in juzs:
        if juz.status != 'completed':
            return False
    return True


def is_over_limited():
    hatms = Hatm.objects.filter(is_public=True, is_published=True, is_completed=False)
    if len(hatms) >= 3:
        return True
    else:
        return False