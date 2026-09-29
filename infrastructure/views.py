from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import Device
import json

MODULE_TITLE = 'Smart Grid Infrastructure'

@login_required(login_url='login')
def index(request):
    return render(request, 'infrastructure/index.html', {'title': MODULE_TITLE})

# CRUD

def list_devices(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    devices = list(Device.objects.values())
    return JsonResponse(devices, safe=False)


def create_device(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    body = json.loads(request.body.decode('utf-8'))
    device = Device.objects.create(
        name=body.get('name', 'unnamed'),
        type=body.get('type', 'sensor'),
        status=body.get('status', 'online'),
    )
    return JsonResponse({'id': device.id, 'name': device.name, 'type': device.type, 'status': device.status}, status=201)


def device_detail(request, device_id):
    device = get_object_or_404(Device, pk=device_id)
    if request.method == 'GET':
        return JsonResponse({'id': device.id, 'name': device.name, 'type': device.type, 'status': device.status, 'last_heartbeat': device.last_heartbeat})
    if request.method in ['PUT', 'PATCH']:
        body = json.loads(request.body.decode('utf-8'))
        device.name = body.get('name', device.name)
        device.type = body.get('type', device.type)
        device.status = body.get('status', device.status)
        device.save()
        return JsonResponse({'id': device.id, 'name': device.name, 'type': device.type, 'status': device.status})
    if request.method == 'DELETE':
        device.delete()
        return JsonResponse({'deleted': device_id})
    return HttpResponseNotAllowed(['GET', 'PUT', 'PATCH', 'DELETE'])