from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from user_auth.models import CustomUser as User
from django.db.models.signals import post_save
import datetime


class Hatim(models.Model):
    creator_id = models.ForeignKey(User, on_delete=models.CASCADE)
    isPublic = models.BooleanField(default=True)
    title = models.CharField(max_length=150)
    description = models.TextField()
    isCompleted = models.BooleanField(default=False)
    created_at = models.DateField(default=datetime.date.today)
    deadline = models.DateField()

    class Meta:
        verbose_name = ("Hatim")
        verbose_name_plural = ("Hatims")

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
    hatim_id = models.ForeignKey(Hatim, on_delete=models.CASCADE, related_name='juz')
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='juz_set')
    juz_number = models.PositiveIntegerField(blank=False, validators=[MinValueValidator(1), MaxValueValidator(31)])
    type = models.CharField(choices=entityType, max_length=50)
    status = models.CharField(choices=juzStatus, default='free', max_length=20)

    class Meta:
        verbose_name = ("Juz")
        verbose_name_plural = ("Juzs")

    def __str__(self):
        if self.type == 'juz':
            return str(self.hatim_id.creator_id) + '`s Hatim, Juz = ' + str(self.juz_number)
        else:
            return str(self.hatim_id.creator_id) + '`s Hatim, Dua'


def create_children(sender, instance, created, **kwargs):
    if created:
        for i in range(30):
            Juz.objects.create(
                hatim_id=instance, 
                juz_number=i+1,
                type='juz'
            )
        Juz.objects.create(
            hatim_id=instance,
            juz_number=31,
            type='dua'
        )

post_save.connect(create_children, sender=Hatim)