from django.db import models

CHOICES_JINSI = [
    ('E','Erkak'),
    ('A','Ayol'),
]

class Actor(models.Model):
    name = models.CharField(max_length=500)
    birthdate = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=50, choices=CHOICES_JINSI)

    def __str__(self):
        return self.name
