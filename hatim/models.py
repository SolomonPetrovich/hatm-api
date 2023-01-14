from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from user_auth.models import CustomUser as User
from django.db.models.signals import post_save


class Hatim(models.Model):
    creator_id = models.ForeignKey(User, on_delete=models.CASCADE)
    isPublic = models.BooleanField()
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()

    class Meta:
        verbose_name = ("Hatim")
        verbose_name_plural = ("Hatims")

    def delete(self, *args, **kwargs):
        self.creator_id.hatims_created = 0
        self.creator_id.save()
        super().delete(*args, **kwargs)


    def __str__(self):
        return self.title


class Juz(models.Model):
    juzStatus = (
        ('free', 'Free'),
        ('in Progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    hatim_id = models.ForeignKey(Hatim, on_delete=models.CASCADE, related_name='juz')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='juz_set')
    juz_number = models.PositiveIntegerField(blank=False, validators=[MinValueValidator(1), MaxValueValidator(30)])
    status = models.CharField(choices=juzStatus, default='free', max_length=20)
    pageInterval = ArrayField(models.JSONField(default=dict), null=True)

    class Meta:
        verbose_name = ("Juz")
        verbose_name_plural = ("Juzs")

    def __str__(self):
        return str(self.hatim_id.creator_id) + '`s Hatim, Juz = ' + str(self.juz_number)


def create_children(sender, instance, created, **kwargs):
    if created:
        for i in range(30):
            Juz.objects.create(
                hatim_id=instance, 
                juz_number=i+1,
                pageInterval=[]
                )

post_save.connect(create_children, sender=Hatim)