import uuid
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField
from user_auth.models import CustomUser as User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime


class Hatm(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    is_public = models.BooleanField()
    is_completed = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    created_at = models.DateField(default=datetime.date.today)
    deadline = models.DateTimeField(null=True)
    members = models.ManyToManyField(User, related_name='members', blank=True, null=True)

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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hatm_id = models.ForeignKey(Hatm, on_delete=models.CASCADE, related_name='juz')
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='juz_set')
    juz_number = models.PositiveIntegerField(blank=False, validators=[MinValueValidator(1), MaxValueValidator(31)])
    type = models.CharField(choices=entityType, max_length=50)
    status = models.CharField(choices=juzStatus, default='free', max_length=20)
    deadline = models.DateTimeField(null=True)

    class Meta:
        verbose_name = ("Juz")
        verbose_name_plural = ("Juzs")

    def __str__(self):
        if self.type == 'juz':
            return str(self.hatm_id.creator_id) + '`s Hatm, Juz = ' + str(self.juz_number)
        else:
            return str(self.hatm_id.creator_id) + '`s Hatm, Dua'


def add_creator_to_members(sender, instance, created, **kwargs):
    if created:
        instance.members.add(instance.creator_id)
        instance.save()


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


post_save.connect(add_creator_to_members, sender=Hatm)
post_save.connect(create_children, sender=Hatm)



class JoinRequest(models.Model):
    statusTypes = [
        ('rejected', 'Rejected'),
        ('approved', 'Approved'),
        ('pending', 'Pending')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hatm = models.ForeignKey(Hatm, on_delete=models.CASCADE, related_name='join_requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=statusTypes, default='pending')


    def __str__(self) -> str:
        return f'User: {self.user}, Hatm: {self.hatm}'