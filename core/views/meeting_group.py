from django.shortcuts import render, get_object_or_404, redirect
from core.models.meeting_group import MeetingGroup
from django.http import JsonResponse


def group_list(request):
    groups = MeetingGroup.objects.all()
    group_list = [{"id": group.id, "name": group.name}]
    return JsonResponse({"groups": group_list}, safe=False)


def group_detail(request, id):
    group = get_object_or_404(MeetingGroup, id=id)
    return JsonResponse(
        {"id": group.id, "name": group.name, "description": group.description}
    )


def group_create(request):
    if request.method == "POST":
        name = request.POST.get["name"]
        description = request.POST.get["description"]
        group = MeetingGroup.objects.create(name=name, description=description)
        return JsonResponse({"success": True, "group_id": group.id})
    return JsonResponse({"success": False})


def group_edit(request, id):
    group = get_object_or_404(MeetingGroup, id=id)
    if request.method == "POST":
        group.name = request.POST.get["name"]
        group.description = request.POST.get["description"]
        group.save()
        return JsonResponse({"success": True, "group_id": group.id})
    return JsonResponse(
        {"id": group.id, "name": group.name, "description": group.description}
    )


def group_delete(request, id):
    group = get_object_or_404(MeetingGroup, id=id)
    if request.method == "POST":
        group.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})
