import os
import django
import uuid
import random
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartgrid.settings')
django.setup()

from infrastructure.models import Device
from iot_integration.models import IoTMessage
from cybersecurity.models import ThreatRecord
from ai_module.models import AnomalyRecord
from blockchain.models import TransactionRecord
from sdn.models import FlowRule
from threat_simulation.models import SimulationScenario


def create_devices():
    samples = [
        {'name': 'Substation-01', 'type': 'substation', 'status': 'online'},
        {'name': 'Transformer-03', 'type': 'transformer', 'status': 'online'},
        {'name': 'GridSensor-12', 'type': 'sensor', 'status': 'offline'},
        {'name': 'ControlUnit-07', 'type': 'controller', 'status': 'online'},
    ]
    for item in samples:
        Device.objects.update_or_create(name=item['name'], defaults=item)


def create_iot_messages():
    protocols = ['MQTT', 'CoAP', 'HTTPS']
    for idx in range(8):
        payload = {
            'temperature': round(20 + random.random() * 12, 2),
            'voltage': round(210 + random.random() * 25, 2),
            'humidity': round(30 + random.random() * 40, 1),
            'device_status': random.choice(['normal', 'warning', 'critical']),
        }
        IoTMessage.objects.create(
            device_id=f'sensor-{100 + idx}',
            protocol=random.choice(protocols),
            payload=payload,
        )


def create_threats():
    examples = [
        {'name': 'Data exfiltration', 'confidentiality': 9, 'integrity': 5, 'availability': 3, 'summary': 'Sensitive patient data at risk.'},
        {'name': 'Firmware tampering', 'confidentiality': 6, 'integrity': 9, 'availability': 4, 'summary': 'Malicious update may corrupt device firmware.'},
        {'name': 'DDoS attack', 'confidentiality': 2, 'integrity': 4, 'availability': 9, 'summary': 'Flooding the grid control network to disrupt service.'},
    ]
    for item in examples:
        ThreatRecord.objects.update_or_create(name=item['name'], defaults=item)


def create_anomalies():
    for idx in range(6):
        payload = {
            'temperature': round(18 + random.random() * 18, 2),
            'voltage': round(200 + random.random() * 35, 2),
            'event': 'sensor_reading',
        }
        score = round(random.random(), 3)
        AnomalyRecord.objects.create(
            device_id=f'sensor-{200 + idx}',
            data=payload,
            score=score,
            is_anomaly=score > 0.65,
        )


def create_transactions():
    for idx in range(5):
        TransactionRecord.objects.create(
            tx_id=str(uuid.uuid4()),
            sender=f'node-{random.randint(1,5)}',
            receiver=f'node-{random.randint(6,12)}',
            amount=round(random.uniform(100.0, 1500.0), 2),
            data={'message': 'secure grid event', 'tx_hash': str(uuid.uuid4())},
        )


def create_flow_rules():
    rules = [
        {'src': '10.0.0.1', 'dst': '10.0.0.2', 'protocol': 'TCP', 'action': 'allow'},
        {'src': '10.0.0.5', 'dst': '10.0.0.8', 'protocol': 'UDP', 'action': 'deny'},
        {'src': '192.168.1.20', 'dst': '192.168.1.30', 'protocol': 'ICMP', 'action': 'deny'},
    ]
    for rule in rules:
        FlowRule.objects.update_or_create(src=rule['src'], dst=rule['dst'], defaults=rule)


def create_scenarios():
    scenarios = [
        {'name': 'Grid access breach', 'attack_type': 'Insider threat', 'is_active': True, 'score': 12},
        {'name': 'Service disruption', 'attack_type': 'DDoS', 'is_active': False, 'score': 8},
    ]
    for item in scenarios:
        SimulationScenario.objects.update_or_create(name=item['name'], defaults=item)


def run():
    create_devices()
    create_iot_messages()
    create_threats()
    create_anomalies()
    create_transactions()
    create_flow_rules()
    create_scenarios()
    print('Sample Smart Grid dataset created successfully.')


if __name__ == '__main__':
    run()
