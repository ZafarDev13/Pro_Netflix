from django.db import models
from .actor import Actor

GENER_CHOISES = [
    ("Komediya","Komediya"),
    ("Tarix","Tarix"),
    ("Drama","Drama"),
    ("Hujjatli","Hujjatli"),
]

class Movie(models.Model):
    name = models.CharField(max_length=350)
    year = models.DateField()
    imdb = models.IntegerField()
    genre = models.CharField(max_length=20, choices=GENER_CHOISES)
    actors = models.ManyToManyField(Actor, blank=True, null=True)

    def __str__(self):
        return self.name