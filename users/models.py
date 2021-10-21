from core.models import TimeStampModel
from django.db   import models

class User(TimeStampModel):
    email    = models.EmailField(max_length=250, unique=True)
    password = models.CharField(max_length=1000)
    nickname = models.CharField(max_length=100)

    class Meta:
        db_table = 'users'