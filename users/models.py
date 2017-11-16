from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    node_id = models.IntegerField(default=-1)

    class Meta(AbstractUser.Meta):
        pass
