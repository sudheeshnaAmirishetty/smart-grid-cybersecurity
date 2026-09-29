from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import IoTMessage, IoTDatasetUpload
from ai_module.models import AnomalyRecord
import json
import csv

MODULE_TITLE = 'IoT Integration'

@login_required(login_url='login')
def index(request):
    return render(request, 'iot_integration/index.html', {'title': MODULE_TITLE})


def compute_iot_threat_score(payload):
    temp = payload.get('temperature') or payload.get('temp') or 0
    voltage = payload.get('voltage') or 0
    humidity = payload.get('humidity') or 0
    try:
        temp = float(temp)
    except (TypeError, ValueError):
        temp = 0.0
    try:
        voltage = float(voltage)
    except (TypeError, ValueError):
        voltage = 0.0
    try:
        humidity = float(humidity)
    except (TypeError, ValueError):
        humidity = 0.0

    score = 0.0
    if temp < 18 or temp > 35:
        score += 0.4
    if voltage < 200 or voltage > 240:
        score += 0.3
    if humidity < 20 or humidity > 75:
        score += 0.2
    if payload.get('device_status') == 'critical':
        score += 0.2
    return min(round(score, 2), 1.0)


def detect_threat(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    body = json.loads(request.body.decode('utf-8'))
    payload = body.get('payload', {})
    score = compute_iot_threat_score(payload)
    if score >= 0.7:
        level = 'high'
        recommendation = 'Isolate the device immediately, verify firmware, and block suspicious traffic.'
    elif score >= 0.4:
        level = 'medium'
        recommendation = 'Monitor the sensor closely and validate telemetry signatures.'
    else:
        level = 'low'
        recommendation = 'Continue normal operation with regular monitoring.'
    return JsonResponse({
        'payload': payload,
        'threat_score': score,
        'threat_level': level,
        'recommendation': recommendation,
    })


def parse_iot_dataset_file(file_obj):
    content = file_obj.read().decode('utf-8')
    if file_obj.name.lower().endswith('.csv'):
        reader = csv.DictReader(content.splitlines())
        return [row for row in reader if any((value or '').strip() for value in row.values())]

    parsed = json.loads(content)
    if isinstance(parsed, dict):
        if 'records' in parsed and isinstance(parsed['records'], list):
            return parsed['records']
        return [parsed]
    if isinstance(parsed, list):
        return parsed

    raise ValueError('Unable to parse the uploaded dataset. Please upload valid CSV or JSON content.')


@login_required(login_url='login')
def upload_dataset(request):
    result = None
    errors = []
    if request.method == 'POST':
        uploaded_file = request.FILES.get('dataset')
        if not uploaded_file:
            errors.append('Please select a dataset file to upload.')
        else:
            try:
                records = parse_iot_dataset_file(uploaded_file)
            except Exception as exc:
                errors.append(str(exc))
                records = []

            if records:
                total_records = 0
                anomaly_count = 0
                processed = []
                for raw in records:
                    device_id = raw.get('device_id') or raw.get('device') or raw.get('sensor_id') or 'unknown-device'
                    protocol = raw.get('protocol', 'MQTT')
                    temperature = raw.get('temperature') or raw.get('temp') or 0
                    voltage = raw.get('voltage') or 0
                    humidity = raw.get('humidity') or 0
                    status = raw.get('device_status') or raw.get('status') or 'normal'

                    payload = {
                        'temperature': temperature,
                        'voltage': voltage,
                        'humidity': humidity,
                        'device_status': status,
                    }

                    message = IoTMessage.objects.create(
                        device_id=device_id,
                        protocol=protocol,
                        payload=payload,
                    )

                    score = compute_iot_threat_score(payload)
                    is_anomaly = score >= 0.6
                    AnomalyRecord.objects.create(
                        device_id=device_id,
                        data=payload,
                        score=score,
                        is_anomaly=is_anomaly,
                    )
                    if is_anomaly:
                        anomaly_count += 1

                    processed.append({
                        'device_id': device_id,
                        'protocol': protocol,
                        'score': score,
                        'is_anomaly': is_anomaly,
                        'message_id': message.id,
                    })
                    total_records += 1

                summary = {
                    'dataset_name': uploaded_file.name,
                    'total_records': total_records,
                    'anomalies_detected': anomaly_count,
                    'anomaly_rate': round(anomaly_count / max(total_records, 1), 3),
                }

                upload_record = IoTDatasetUpload.objects.create(
                    name=uploaded_file.name,
                    total_records=total_records,
                    anomalies_detected=anomaly_count,
                    summary=summary,
                )

                result = {
                    'summary': summary,
                    'session_id': upload_record.id,
                    'processed_rows': processed[:10],
                }

    return render(request, 'iot_integration/upload.html', {
        'result': result,
        'errors': errors,
    })

# message CRUD + sample payload

def list_messages(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    messages = list(IoTMessage.objects.values())
    return JsonResponse(messages, safe=False)


def create_message(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    body = json.loads(request.body.decode('utf-8'))
    msg = IoTMessage.objects.create(
        device_id=body.get('device_id', 'unknown'),
        protocol=body.get('protocol', 'MQTT'),
        payload=body.get('payload', {'temperature': 0, 'voltage': 0}),
    )
    return JsonResponse({'id': msg.id, 'device_id': msg.device_id, 'protocol': msg.protocol, 'payload': msg.payload}, status=201)


def message_detail(request, message_id):
    message = get_object_or_404(IoTMessage, pk=message_id)
    if request.method == 'GET':
        return JsonResponse({'id': message.id, 'device_id': message.device_id, 'protocol': message.protocol, 'payload': message.payload, 'received_at': message.received_at})
    if request.method in ['PUT', 'PATCH']:
        body = json.loads(request.body.decode('utf-8'))
        message.device_id = body.get('device_id', message.device_id)
        message.protocol = body.get('protocol', message.protocol)
        message.payload = body.get('payload', message.payload)
        message.save()
        return JsonResponse({'id': message.id, 'device_id': message.device_id, 'protocol': message.protocol, 'payload': message.payload})
    if request.method == 'DELETE':
        message.delete()
        return JsonResponse({'deleted': message_id})
    return HttpResponseNotAllowed(['GET', 'PUT', 'PATCH', 'DELETE'])


def sample_message(request):
    return JsonResponse({'device_id': 'sensor-001', 'payload': {'temp': 23.7, 'voltage': 220.3, 'humidity': 50}, 'protocol': 'MQTT', 'transport': 'LoRaWAN'})