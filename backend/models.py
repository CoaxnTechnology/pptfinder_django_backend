from django.db import models

class Pptdata(models.Model):
    keyword = models.CharField(max_length=255)
    object = models.TextField()  # This field type is a guess.
    timestamp = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        db_table = 'pptdata'