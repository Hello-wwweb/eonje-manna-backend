from functools import partial


from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Vote, Member, Event
from core.serializers.vote import VoteSerializer, VoteRequestSerializer
from drf_yasg.utils import swagger_auto_schema

class VoteListView(APIView):


    def get(self, request):

        place = request.GET.get('place')
        if not place:
            return Response({"error": "Place query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)


        count = Vote.objects.filter(voted_places=place).count()
        return Response({"place": place, "count": count}, status=status.HTTP_200_OK)


    @swagger_auto_schema(
        request_body=VoteRequestSerializer,
        responses={
            200: VoteSerializer(),
            201: VoteSerializer(),
            400: "Bad Request",
        },
    )
    def post(self, request):
        user = request.user
        voting_member = Member.objects.get(user = user)
        voting_event = request.data.get('event')

        # 멤버 미존재, 첫 투표,  ....코드 최적화 필요
        if not Vote.objects.filter(event = voting_event, member= voting_member).exists():
            event_instance = Event.objects.get(id = voting_event)

            serializer = VoteSerializer(data=request.data)
            if serializer.is_valid():
                vote = Vote.objects.create(
                    member = voting_member,
                    event = event_instance,
                    voted_places = request.data.get('voted_places')
                )
                response_data = VoteSerializer(vote)
                return Response(response_data.data, status = status.HTTP_201_CREATED)
            else:
                return Response("first, but err", status=status.HTTP_400_BAD_REQUEST)

        #멤버 존재, 투표 바꾸기
        else:
            obj = Vote.objects.get(event = voting_event, member= voting_member)
            serializer = VoteSerializer(obj, data=request.data, partial = True) #수정
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_200_OK)
            else:
                return Response("not first, but err", status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=VoteRequestSerializer,
        responses={
            200: VoteSerializer(),
            201: VoteSerializer(),
            400: "Bad Request",
        },
    )
    def delete(self, request):
        voting_event = request.data.get('event')
        user = request.user
        voting_member = Member.objects.get(user=user)
        votes = Vote.objects.filter(event = voting_event, member=voting_member)
        votes.delete()





