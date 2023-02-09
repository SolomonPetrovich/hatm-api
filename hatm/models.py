from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from user_auth.models import CustomUser as User
from django.db.models.signals import post_save
import datetime


class Hatm(models.Model):
    creator_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    is_public = models.BooleanField()
    is_completed = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    created_at = models.DateField(default=datetime.date.today)
    deadline = models.DateField()

    class Meta:
        verbose_name = ("Hatm")
        verbose_name_plural = ("Hatms")

    def __str__(self):
        return self.title


class Juz(models.Model):
    juzStatus = (
        ('free', 'Free'),
        ('in Progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    entityType = (
        ('juz', 'Juz'),
        ('dua', 'Dua')
    )
    hatm_id = models.ForeignKey(Hatm, on_delete=models.CASCADE, related_name='juz')
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='juz_set')
    juz_number = models.PositiveIntegerField(blank=False, validators=[MinValueValidator(1), MaxValueValidator(31)])
    type = models.CharField(choices=entityType, max_length=50)
    status = models.CharField(choices=juzStatus, default='free', max_length=20)

    class Meta:
        verbose_name = ("Juz")
        verbose_name_plural = ("Juzs")

    def __str__(self):
        if self.type == 'juz':
            return str(self.hatm_id.creator_id) + '`s Hatm, Juz = ' + str(self.juz_number)
        else:
            return str(self.hatm_id.creator_id) + '`s Hatm, Dua'


def create_children(sender, instance, created, **kwargs):
    if created:
        for i in range(30):
            Juz.objects.create(
                hatm_id=instance, 
                juz_number=i+1,
                type='juz'
            )
        Juz.objects.create(
            hatm_id=instance,
            juz_number=31,
            type='dua'
        )

        user = User.objects.get(id=instance.creator_id.id)
        user.hatms_created = user.hatms_created + 1
        user.active_hatms = user.active_hatms + 1
        user.save()

post_save.connect(create_children, sender=Hatm)