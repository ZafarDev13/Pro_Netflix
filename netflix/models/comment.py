from django.db import models
from django.contrib.auth import get_user_model
from .movie import Movie

User = get_user_model()

class Comment(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.movie_id}  {self.text}"