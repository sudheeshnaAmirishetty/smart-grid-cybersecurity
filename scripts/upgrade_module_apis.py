import os
root = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(root, '..'))

module_specs = {
    'infrastructure': {
        'model': """from django.db import models

class Device(models.Model):
    name = models.CharField(max_length=180)
    type = models.CharField(max_length=128)
    status = models.CharField(max_length=128, default='online')
    last_heartbeat = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} ({self.type})'""",
        'views': """from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import Device
import json

MODULE_TITLE = 'Smart Grid Infrastructure'

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
    return HttpResponseNotAllowed(['GET', 'PUT', 'PATCH', 'DELETE'])""",
        'urls': """from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='infrastructure_index'),
    path('api/devices/', views.list_devices, name='infrastructure_list'),
    path('api/devices/create/', views.create_device, name='infrastructure_create'),
    path('api/devices/<int:device_id>/', views.device_detail, name='infrastructure_detail'),
]
""",
    },
    'iot_integration': {
        'model': """from django.db import models

class IoTMessage(models.Model):
    device_id = models.CharField(max_length=140)
    payload = models.JSONField(default=dict)
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.device_id} @ {self.received_at}'""",
        'views': """from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import IoTMessage
import json

MODULE_TITLE = 'IoT Integration'

def index(request):
    return render(request, 'iot_integration/index.html', {'title': MODULE_TITLE})

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
        payload=body.get('payload', {'temperature': 0, 'voltage': 0}),
    )
    return JsonResponse({'id': msg.id, 'device_id': msg.device_id, 'payload': msg.payload}, status=201)


def message_detail(request, message_id):
    message = get_object_or_404(IoTMessage, pk=message_id)
    if request.method == 'GET':
        return JsonResponse({'id': message.id, 'device_id': message.device_id, 'payload': message.payload, 'received_at': message.received_at})
    if request.method in ['PUT', 'PATCH']:
        body = json.loads(request.body.decode('utf-8'))
        message.device_id = body.get('device_id', message.device_id)
        message.payload = body.get('payload', message.payload)
        message.save()
        return JsonResponse({'id': message.id, 'device_id': message.device_id, 'payload': message.payload})
    if request.method == 'DELETE':
        message.delete()
        return JsonResponse({'deleted': message_id})
    return HttpResponseNotAllowed(['GET', 'PUT', 'PATCH', 'DELETE'])


def sample_message(request):
    return JsonResponse({'device_id': 'sensor-001', 'payload': {'temp': 23.7, 'rh': 50}, 'protocol': 'MQTT', 'transport': 'LoRaWAN'})""",
        'urls': """from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='iot_index'),
    path('api/messages/', views.list_messages, name='iot_list'),
    path('api/messages/create/', views.create_message, name='iot_create'),
    path('api/messages/<int:message_id>/', views.message_detail, name='iot_detail'),
    path('api/messages/sample/', views.sample_message, name='iot_sample'),
]
""",
    },
    'cybersecurity': {
        'model': """from django.db import models

class ThreatRecord(models.Model):
    name = models.CharField(max_length=180)
    confidentiality = models.IntegerField(default=0)
    integrity = models.IntegerField(default=0)
    availability = models.IntegerField(default=0)
    summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def risk_level(self):
        score = self.confidentiality + self.integrity + self.availability
        if score > 20:
            return 'high'
        if score > 10:
            return 'medium'
        return 'low'

    def __str__(self):
        return f'{self.name} ({self.risk_level()})'""",
        'views': """from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import ThreatRecord
import json

MODULE_TITLE = 'Cybersecurity Analysis'

def index(request):
    return render(request, 'cybersecurity/index.html', {'title': MODULE_TITLE})

# CIA-based CRUD

def list_threats(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    threats = list(ThreatRecord.objects.values())
    return JsonResponse(threats, safe=False)


def create_threat(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    body = json.loads(request.body.decode('utf-8'))
    item = ThreatRecord.objects.create(
        name=body.get('name', 'Unnamed threat'),
        confidentiality=int(body.get('confidentiality', 0)),
        integrity=int(body.get('integrity', 0)),
        availability=int(body.get('availability', 0)),
        summary=body.get('summary', ''),
    )
    return JsonResponse({'id': item.id, 'risk': item.risk_level()}, status=201)


def threat_detail(request, threat_id):
    rec = get_object_or_404(ThreatRecord, pk=threat_id)
    if request.method == 'GET':
        return JsonResponse({'id': rec.id, 'name': rec.name, 'confidentiality': rec.confidentiality, 'integrity': rec.integrity, 'availability': rec.availability, 'risk': rec.risk_level(), 'summary': rec.summary})
    if request.method in ['PUT', 'PATCH']:
        body = json.loads(request.body.decode('utf-8'))
        rec.name = body.get('name', rec.name)
        rec.confidentiality = int(body.get('confidentiality', rec.confidentiality))
        rec.integrity = int(body.get('integrity', rec.integrity))
        rec.availability = int(body.get('availability', rec.availability))
        rec.summary = body.get('summary', rec.summary)
        rec.save()
        return JsonResponse({'id': rec.id, 'risk': rec.risk_level()})
    if request.method == 'DELETE':
        rec.delete()
        return JsonResponse({'deleted': threat_id})
    return HttpResponseNotAllowed(['GET', 'PUT', 'PATCH', 'DELETE'])


def cia_classification(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    body = json.loads(request.body.decode('utf-8'))
    c = int(body.get('confidentiality', 0))
    i = int(body.get('integrity', 0))
    a = int(body.get('availability', 0))
    score = c + i + a
    if score > 20:
        level = 'high'
    elif score > 10:
        level = 'medium'
    else:
        level = 'low'
    return JsonResponse({'cia': {'confidentiality': c, 'integrity': i, 'availability': a}, 'risk_level': level, 'score': score})""",
        'urls': """from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='cybersecurity_index'),
    path('api/threats/', views.list_threats, name='cybersecurity_list'),
    path('api/threats/create/', views.create_threat, name='cybersecurity_create'),
    path('api/threats/<int:threat_id>/', views.threat_detail, name='cybersecurity_detail'),
    path('api/cia-classify/', views.cia_classification, name='cia_classification'),
]
""",
    },
    'ai_module': {
        'model': """from django.db import models

class AnomalyRecord(models.Model):
    device_id = models.CharField(max_length=140)
    data = models.JSONField(default=dict)
    score = models.FloatField(default=0.0)
    is_anomaly = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.device_id} anomaly={self.is_anomaly}'""",
        'views': """from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import AnomalyRecord
import json

MODULE_TITLE = 'Artificial Intelligence'

def index(request):
    return render(request, 'ai_module/index.html', {'title': MODULE_TITLE})

# Anomaly detection stub

def list_anomalies(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    return JsonResponse(list(AnomalyRecord.objects.values()), safe=False)


def analyze_data(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    body = json.loads(request.body.decode('utf-8'))
    device_id = body.get('device_id', 'unknown')
    payload = body.get('data', {})
    score = float(payload.get('anomaly_score', 0.0))
    is_anomaly = score > 0.7
    rec = AnomalyRecord.objects.create(device_id=device_id, data=payload, score=score, is_anomaly=is_anomaly)
    return JsonResponse({'id': rec.id, 'device_id': device_id, 'is_anomaly': is_anomaly, 'score': score}, status=201)


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
    return HttpResponseNotAllowed(['GET', 'PUT', 'PATCH', 'DELETE'])""",
        'urls': """from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ai_index'),
    path('api/anomalies/', views.list_anomalies, name='ai_list'),
    path('api/anomalies/analyze/', views.analyze_data, name='ai_analyze'),
    path('api/anomalies/<int:anom_id>/', views.anomaly_detail, name='ai_detail'),
]
""",
    },
    'blockchain': {
        'model': """from django.db import models

class TransactionRecord(models.Model):
    tx_id = models.CharField(max_length=200, unique=True)
    sender = models.CharField(max_length=140)
    receiver = models.CharField(max_length=140)
    amount = models.FloatField()
    data = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.tx_id}: {self.sender}->{self.receiver} ({self.amount})'""",
        'views': """from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import TransactionRecord
import json, uuid

MODULE_TITLE = 'Blockchain Security'

def index(request):
    return render(request, 'blockchain/index.html', {'title': MODULE_TITLE})

# Transaction CRUD

def list_transactions(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    return JsonResponse(list(TransactionRecord.objects.order_by('-timestamp').values()), safe=False)


def create_transaction(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    body = json.loads(request.body.decode('utf-8'))
    tx_id = body.get('tx_id', str(uuid.uuid4()))
    tx = TransactionRecord.objects.create(
        tx_id=tx_id,
        sender=body.get('sender', 'nodeA'),
        receiver=body.get('receiver', 'nodeB'),
        amount=float(body.get('amount', 0.0)),
        data=body.get('data', {}),
    )
    return JsonResponse({'tx_id': tx.tx_id, 'status': 'recorded', 'immutable': True}, status=201)


def transaction_detail(request, tx_id):
    tx = get_object_or_404(TransactionRecord, tx_id=tx_id)
    if request.method == 'GET':
        return JsonResponse({'tx_id': tx.tx_id, 'sender': tx.sender, 'receiver': tx.receiver, 'amount': tx.amount, 'data': tx.data, 'timestamp': tx.timestamp})
    if request.method == 'DELETE':
        # blockchain transactions are immutable; we can only mark as deleted in an audit track
        return JsonResponse({'error': 'immutable transactions cannot be deleted'}, status=405)
    return HttpResponseNotAllowed(['GET', 'DELETE'])


def audit_log(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    data = list(TransactionRecord.objects.order_by('-timestamp').values('tx_id', 'sender', 'receiver', 'amount', 'timestamp'))
    return JsonResponse({'audit': data}, safe=False)
""",
        'urls': """from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='blockchain_index'),
    path('api/transactions/', views.list_transactions, name='blockchain_list'),
    path('api/transactions/create/', views.create_transaction, name='blockchain_create'),
    path('api/transactions/<str:tx_id>/', views.transaction_detail, name='blockchain_detail'),
    path('api/transactions/audit/', views.audit_log, name='blockchain_audit'),
]
""",
    },
    'sdn': {
        'model': """from django.db import models

class FlowRule(models.Model):
    src = models.CharField(max_length=140)
    dst = models.CharField(max_length=140)
    protocol = models.CharField(max_length=40, default='TCP')
    action = models.CharField(max_length=40, default='allow')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.src}->{self.dst} {self.protocol} {self.action}'""",
        'views': """from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import FlowRule
import json

MODULE_TITLE = 'SDN Control'

def index(request):
    return render(request, 'sdn/index.html', {'title': MODULE_TITLE})

# dynamic routing rules CRUD

def list_rules(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    return JsonResponse(list(FlowRule.objects.values()), safe=False)


def create_rule(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    body = json.loads(request.body.decode('utf-8'))
    rule = FlowRule.objects.create(src=body.get('src', '0.0.0.0'), dst=body.get('dst', '0.0.0.0'), protocol=body.get('protocol', 'TCP'), action=body.get('action', 'allow'))
    return JsonResponse({'id': rule.id, 'action': rule.action}, status=201)


def rule_detail(request, rule_id):
    rule = get_object_or_404(FlowRule, pk=rule_id)
    if request.method == 'GET':
        return JsonResponse({'id': rule.id, 'src': rule.src, 'dst': rule.dst, 'protocol': rule.protocol, 'action': rule.action})
    if request.method in ['PUT', 'PATCH']:
        body = json.loads(request.body.decode('utf-8'))
        rule.src = body.get('src', rule.src)
        rule.dst = body.get('dst', rule.dst)
        rule.protocol = body.get('protocol', rule.protocol)
        rule.action = body.get('action', rule.action)
        rule.save()
        return JsonResponse({'id': rule.id, 'action': rule.action})
    if request.method == 'DELETE':
        rule.delete()
        return JsonResponse({'deleted': rule_id})
    return HttpResponseNotAllowed(['GET', 'PUT', 'PATCH', 'DELETE'])""",
        'urls': """from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='sdn_index'),
    path('api/rules/', views.list_rules, name='sdn_list'),
    path('api/rules/create/', views.create_rule, name='sdn_create'),
    path('api/rules/<int:rule_id>/', views.rule_detail, name='sdn_detail'),
]
""",
    },
    'threat_simulation': {
        'model': """from django.db import models

class SimulationScenario(models.Model):
    name = models.CharField(max_length=180)
    attack_type = models.CharField(max_length=120)
    is_active = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.attack_type})'""",
        'views': """from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import SimulationScenario
import json

MODULE_TITLE = 'Threat Simulation'

def index(request):
    return render(request, 'threat_simulation/index.html', {'title': MODULE_TITLE})

# scenario CRUD

def list_scenarios(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    return JsonResponse(list(SimulationScenario.objects.values()), safe=False)


def create_scenario(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    body = json.loads(request.body.decode('utf-8'))
    scenario = SimulationScenario.objects.create(name=body.get('name', 'Unnamed'), attack_type=body.get('attack_type', 'DoS'), is_active=bool(body.get('is_active', False)), score=int(body.get('score', 0)))
    return JsonResponse({'id': scenario.id, 'status': 'created'}, status=201)


def scenario_detail(request, scenario_id):
    scenario = get_object_or_404(SimulationScenario, pk=scenario_id)
    if request.method == 'GET':
        return JsonResponse({'id': scenario.id, 'name': scenario.name, 'attack_type': scenario.attack_type, 'is_active': scenario.is_active})
    if request.method == 'DELETE':
        scenario.delete()
        return JsonResponse({'deleted': scenario_id})
    return HttpResponseNotAllowed(['GET', 'DELETE'])""",
        'urls': """from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='threat_index'),
    path('api/scenarios/', views.list_scenarios, name='threat_list'),
    path('api/scenarios/create/', views.create_scenario, name='threat_create'),
    path('api/scenarios/<int:scenario_id>/', views.scenario_detail, name='threat_detail'),
]
""",
    },
}

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

for app, spec in module_specs.items():
    write(os.path.join(root, app, 'models.py'), spec['model'])
    write(os.path.join(root, app, 'views.py'), spec['views'])
    write(os.path.join(root, app, 'urls.py'), spec['urls'])
    # Ensure template exists
    os.makedirs(os.path.join(root, 'templates', app), exist_ok=True)
    write(os.path.join(root, 'templates', app, 'index.html'), f"{{% extends 'base.html' %}}\n{{% block content %}}\n<h1>{{{{ title }}}}</h1>\n<p>Module dashboard for {app}</p>\n{{% endblock %}}\n")

print('Module API upgrade complete.')
