from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.db.models import Q
import json

from core.models import Member
from core.models.event import Event
from core.models.event_data_selection import EventDateSelection
from core.models.event_location_selection import EventLocationSelection


def create_event(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            event = Event.objects.create(
                group_id=data.get("group_id"),
                name=data.get("name"),
                description=data.get("description"),
                created_by_id=data.get("created_by_id"),
            )
            return JsonResponse({"message": "Event create successful", "event_id": event.id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return HttpResponse(status=405)


def update_event(request, event_id):
    if request.method == "PUT":
        try:
            user = request.user
            data = json.loads(request.body)
            event = get_object_or_404(Event, id=event_id)

            #authenticate
            if not Member.objects.filter(group = event.group, user=user).exists():
                return JsonResponse({"error": "Permission Denied"},status = 403)

            event.name = data.get("name", event.name)
            event.description = data.get("description", event.description)
            event.event_date = data.get("event_date", event.event_date)
            event.event_location = data.get("event_location", event.event_location)
            event.save()
            return JsonResponse({"message": "Event update successful"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return HttpResponse(status=405)


def delete_event(request, event_id):
    if request.method == "DELETE":
        try:
            user = request.user
            event = get_object_or_404(Event, id=event_id)

            # authenticate
            if not Member.objects.filter(group=event.group, user=user).exists():
                return JsonResponse({"error": "Permission Denied"}, status=403)


            event.delete()
            return JsonResponse({"message": "Event deleted"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return HttpResponse(status=405)

def retrieve_event(request, event_id):
    if request.method == "GET":
        try:
            user = request.user
            event = get_object_or_404(Event, id=event_id)

            # authenticate
            if not Member.objects.filter(group=event.group, user=user).exists():
                return JsonResponse({"error": "Permission Denied"}, status=403)

            event_data = {
                "id": event.id,
                "group_id": event.group_id,
                "name": event.name,
                "description": event.description,
                "event_date": event.event_date,
                "event_location": event.event_location,
                "created_by_id": event.created_by_id,
            }
            return JsonResponse(event_data, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return HttpResponse(status=405)


