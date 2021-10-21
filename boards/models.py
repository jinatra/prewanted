from django.db                       import models
from django.db.models.fields.related import ForeignKey

from core.models                     import TimeStampModel
from users.models import User

class Board(TimeStampModel):
    title   = models.CharField(max_length=100)
    content = models.TextField()
    user    = ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'boards'