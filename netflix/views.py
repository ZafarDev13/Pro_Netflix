import django_filters
from django.contrib.postgres.search import TrigramSimilarity
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import filters
from rest_framework import status
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, api_view

from .serializers import MovieSerializer, ActorSerializer, CommentSerializer
from .models import Movie, Actor, Comment

class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter,]
    ordering_fields = ['imdb', '-imdb']
    search_fields = ['name',]

    # search_fields = ['name', 'actors__name', 'genre']

    # def get_queryset(self):
    #     queryset = Movie.objects.all()
    #     genre = self.request.query_params.get('genre')
    #     if genre is not None:
    #         queryset = queryset.filter(genre__icontains=genre)
    #         return queryset

    # def get_queryset(self):
    #     queryset = Movie.objects.all()
    #     query = self.request.query_params.get('search')
    #     if query is not None:
    #         queryset = Movie.objects.annotate(similarity=TrigramSimilarity('name', query)).filter(similarity__gt=0.3).order_by('-similarity')
    #     return queryset

    @action(detail=True, methods=['GET']) #movie ga tegishli actor larni qaytaradi
    def actors(self, request, *args, **kwargs):
        movie_obj = self.get_object()
        seralizer = ActorSerializer(movie_obj.actors, many=True)
        return Response(seralizer.data)

    @action(detail=True, methods=['POST']) #movie ga yangi actor qo'shish (birdaniga yangi actor yaratadi)
    def add_actor(self, request, *args, **kwargs):
        movie_obj = self.get_object()
        serializer = ActorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            new_actor = Actor.objects.get(id=serializer.data['id'])
            movie_obj.actors.add(new_actor)
        serializer = MovieSerializer(movie_obj)
        return Response(serializer.data)


    @action(detail=True, methods=['PATCH'])
    def add_actor_movie(self, request, *args, **kwargs):
        movie_obj = self.get_object()
        data = request.data

        movie_obj.name = data.get("name", movie_obj.name)
        movie_obj.year = data.get("year", movie_obj.year)
        movie_obj.imdb = data.get("imdb", movie_obj.imdb)
        movie_obj.genre = data.get("genre", movie_obj.genre)
        movie_obj.save()
        movie_obj.actors.set(data["actors"])

        serializer = MovieSerializer(movie_obj)
        return Response(serializer.data)

    @action(detail=True, methods=['DELETE'])  #1-usul movie listidan actorni o'chirish un id=int bittalab
    def remove_actor(self, request, *args, **kwargs):
        movie_obj = self.get_object()
        data = request.data
        rm_actor = Actor.objects.get(id=data['actors'])
        movie_obj.actors.remove(rm_actor)
        serializer = MovieSerializer(movie_obj)
        return Response(serializer.data)

    @action(detail=True, methods=['DELETE']) #2-usul movie listidan actorni o'chirish id larni list ko'rinishida
    def remove_actors(self, request, *args, **kwargs):
        movie_obj = self.get_object()
        remove_item_id = request.data.pop('actors', [])
        items_remove = Actor.objects.filter(id__in=remove_item_id).all()
        movie_obj.actors.remove(*items_remove)
        serializer = MovieSerializer(movie_obj)
        return Response(serializer.data)



class ActorViewSet(ModelViewSet):
    serializer_class = ActorSerializer
    queryset = Actor.objects.all()

    @action(detail=True, methods=['PUT'])
    def actor_put(self, request, *args, **kwargs):
        actor_obj = self.get_object()
        data = request.data
        actor_obj.name = data["name"]
        actor_obj.birthdate = data["birthdate"]
        actor_obj.gender = data["gender"]
        actor_obj.save()
        serializer = ActorSerializer(actor_obj)
        return Response(serializer.data)

    @action(detail=True, methods=['PATCH'])
    def actor_patch(self, request, *args, **kwargs):
        actor_obj = self.get_object()
        data = request.data
        actor_obj.name = data.get("name", actor_obj.name)
        actor_obj.birthdate = data.get("birthdate", actor_obj.birthdate)
        actor_obj.gender = data.get("gender", actor_obj.gender)
        actor_obj.save()
        serializer = ActorSerializer(actor_obj)
        return Response(serializer.data)

class MovieActorListAPIView(APIView):

    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return  Response(data=serializer.data)


class MovieActorDetailAPIView(APIView):  # /movies/<int:id>/actors 5-vazifa
    def get_object(self, pk):
        try:
            return Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        movie_obj = self.get_object(pk)
        actors = movie_obj.actors.all()
        serializer = ActorSerializer(actors, many=True)
        return Response(serializer.data)


class CommentCRAPIview(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        comments = Comment.objects.all()
        serilizer = CommentSerializer(comments, many=True)
        return Response(serilizer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

class CommentDetailAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def delete(self, request, pk):
        comment = self.get_object(pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)