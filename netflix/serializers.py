from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from datetime import datetime
from .models.comment import User
from .models import Movie, Actor, Comment


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'name', 'birthdate', 'gender']

    def validate_birthdate(self, value):
        date_str = '01-01-1950'
        date_str = datetime.strptime(date_str, '%m-%d-%Y').date()
        if value < date_str:
            raise serializers.ValidationError('1950 yildan kichkina sana kiritish mumkin emas.')
        return value

class MovieSerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True)
    class Meta:
        model = Movie
        fields = ['id', 'name', 'year', 'imdb', 'genre', 'actors']

class CommentSerializer(serializers.ModelSerializer):
    # movie_id = MovieSerializer()
    class Meta:
        model = Comment
        fields = ['id', 'movie_id', 'user_id', 'text']