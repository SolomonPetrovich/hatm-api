import random
import datetime
from .models import Hatm, Juz


def create_public_hatm(user):
    title_vars = [
        {
            'title': 'hatm.io',
            'description': 'ARO'
        },
        {
            'title': 'hatm.io',
            'description': 'ARO'
        },
        {
            'title': 'hatm.io',
            'description': 'ARO'
        }
    ]
    title_var = random.choice(title_vars)
    hatm_deadine = datetime.date.today() + datetime.timedelta(days=30)
    hatm = Hatm.objects.create(creator_id=user, is_completed=False, is_public=True, is_published=True, title=title_var['title'], description=title_var['description'], deadline=hatm_deadine)
    hatm.save()


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