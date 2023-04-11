from django.db import models
from django.utils import timezone

# Create your models here.
class item(models.Model):
  item_name = models.CharField(max_length = 100)
  item_count = models.IntegerField(default = 1)

class order(models.Model):
  item = models.ForeignKey(item, on_delete = models.CASCADE)
  order_date = models.DateTimeField(default = timezone.now)
  quantity = models.IntegerField(default = 1)

