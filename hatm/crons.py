import datetime
from .models import *
import oauth2_provider

def take_juz_from_user():
    juzs = Juz.objects.filter(status='in Progress', deadline__lt=datetime.datetime.now())
    for juz in juzs:
        juz.status = 'free'
        juz.user_id = None
        juz.deadline = None
        juz.save()


def extend_the_deadline_of_hatm():
    hatms = Hatm.objects.filter(is_completed=False, is_public=True, is_published=True, deadline__date=datetime.date.today())
    for hatm in hatms:
        hatm.deadline = hatm.deadline + datetime.timedelta(days=1)
        hatm.save()

def delete_expired_refresh_tokens():
    oauth2_provider.models.get_refresh_token_model().objects.filter(access_token=None).delete()