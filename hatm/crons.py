import datetime
from .models import *

def take_juz_from_user():
    juzs = Juz.objects.filter(status='in Progress', deadline__date=datetime.date.today())
    for juz in juzs:
        if juz.deadline < datetime.now():
            juz.status = 'free'
            juz.user_id = None
            juz.deadline = None
            juz.save()


def extend_the_deadline_of_hatm():
    hatms = Hatm.objects.filter(is_completed=False, is_public=True, is_published=True, deadline__date=datetime.date.today())
    for hatm in hatms:
        hatm.deadline = hatm.deadline + datetime.timedelta(days=1)
        hatm.save()