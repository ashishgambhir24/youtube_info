from functools import reduce
import operator
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from video.models import Video

class AllVideosView(APIView):
    def get(self, request):
        videos = Video.objects.all().order_by('-published_at')
        results = []
        start = int(request.query_params.get('start', 0))
        entries = int(request.query_params.get('entries', 20))
        for video in videos[start:start+entries]:  #pagination
            results.append(video.jsonify())

        return Response(results)

class SearchVideoView(APIView):
    def get(self, request):
        print(request.query_params)
        q = request.query_params['q']
        words = q.split(' ')

        # If all words of query string lies in either title or description
        title_query = Q()  # empty Q object
        for word in words:
            title_query &= Q(title__icontains=word)

        description_query = Q()  # empty Q object
        for word in words:
            description_query &= Q(description__icontains=word)

        videos = Video.objects.filter(
            reduce(operator.or_, [title_query, description_query])
        ).order_by('-published_at')

        # If all words of query string lies in combination of title and description
        # q_objects = Q()  # empty Q object
        # for word in words:
        #     query = Q(title__icontains=word) | Q(description__icontains=word)
        #     q_objects &= query

        # videos = Video.objects.filter(
        #     reduce(operator.and_, [q_objects])
        # ).order_by('-published_at')

        results = []
        for video in videos:
            results.append(video.jsonify())

        return Response(results)
