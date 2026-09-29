from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import AnomalyRecord
import json

MODULE_TITLE = 'Artificial Intelligence'

@login_required(login_url='login')
def index(request):
    result = None
    if request.method == 'POST':
        device_id = request.POST.get('device_id', 'unknown')
        temperature = request.POST.get('temperature', '0')
        voltage = request.POST.get('voltage', '0')
        humidity = request.POST.get('humidity', '0')
        status = request.POST.get('device_status', 'normal')
        try:
            temperature = float(temperature)
        except (TypeError, ValueError):
            temperature = 0.0
        try:
            voltage = float(voltage)
        except (TypeError, ValueError):
            voltage = 0.0
        try:
            humidity = float(humidity)
        except (TypeError, ValueError):
            humidity = 0.0

        payload = {
            'temperature': temperature,
            'voltage': voltage,
            'humidity': humidity,
            'device_status': status,
        }
        score = compute_anomaly_score(payload)
        is_anomaly = score > 0.6
        prediction = 'potential attack' if is_anomaly else 'normal operation'
        rec = AnomalyRecord.objects.create(device_id=device_id, data=payload, score=score, is_anomaly=is_anomaly)
        result = {
            'device_id': device_id,
            'payload': payload,
            'score': score,
            'is_anomaly': is_anomaly,
            'prediction': prediction,
        }

    anomalies = AnomalyRecord.objects.order_by('-created_at')[:10]
    total_anomalies = AnomalyRecord.objects.count()
    return render(request, 'ai_module/index_v2.html', {
        'title': MODULE_TITLE,
        'anomalies': anomalies,
        'total_anomalies': total_anomalies,
        'result': result,
    })

# Anomaly detection support

def compute_anomaly_score(payload):
    temp = payload.get('temperature') or payload.get('temp') or 0
    voltage = payload.get('voltage') or 0
    try:
        temp = float(temp)
    except (TypeError, ValueError):
        temp = 0.0
    try:
        voltage = float(voltage)
    except (TypeError, ValueError):
        voltage = 0.0
    temp_deviation = min(abs(temp - 25) / 15, 1.0)
    voltage_deviation = min(abs(voltage - 220) / 30, 1.0)
    return round(min(max((temp_deviation + voltage_deviation) / 2, 0.0), 1.0), 3)


def list_anomalies(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    return JsonResponse(list(AnomalyRecord.objects.order_by('-created_at').values()), safe=False)


def analyze_data(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    body = json.loads(request.body.decode('utf-8'))
    device_id = body.get('device_id', 'unknown')
    payload = body.get('data', {})
    score = compute_anomaly_score(payload)
    is_anomaly = score > 0.6
    prediction = 'potential attack' if is_anomaly else 'normal operation'
    rec = AnomalyRecord.objects.create(device_id=device_id, data=payload, score=score, is_anomaly=is_anomaly)
    return JsonResponse({
        'id': rec.id,
        'device_id': device_id,
        'is_anomaly': is_anomaly,
        'score': score,
        'prediction': prediction,
    }, status=201)


def anomaly_detail(request, anom_id):
    rec = get_object_or_404(AnomalyRecord, pk=anom_id)
    if request.method == 'GET':
        return JsonResponse({'id': rec.id, 'device_id': rec.device_id, 'score': rec.score, 'is_anomaly': rec.is_anomaly, 'data': rec.data})
    if request.method in ['PUT', 'PATCH']:
        body = json.loads(request.body.decode('utf-8'))
        rec.score = float(body.get('score', rec.score))
        rec.is_anomaly = body.get('is_anomaly', rec.is_anomaly)
        rec.data = body.get('data', rec.data)
        rec.save()
        return JsonResponse({'id': rec.id, 'is_anomaly': rec.is_anomaly, 'score': rec.score})
    if request.method == 'DELETE':
        rec.delete()
        return JsonResponse({'deleted': anom_id})
    return HttpResponseNotAllowed(['GET', 'PUT', 'PATCH', 'DELETE'])