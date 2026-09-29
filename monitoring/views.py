from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import Http404

MODULES = [
    ('infrastructure', 'Smart Grid Infrastructure'),
    ('iot', 'IoT Integration'),
    ('cybersecurity', 'Cybersecurity Analysis'),
    ('ai', 'Artificial Intelligence'),
    ('blockchain', 'Blockchain Security'),
    ('sdn', 'Software-Defined Networking (SDN)'),
    ('threat', 'Threat Simulation and Testing'),
    ('monitoring', 'Monitoring and Reporting'),
]


def ensure_sample_data():
    from infrastructure.models import Device
    from iot_integration.models import IoTMessage
    from cybersecurity.models import ThreatRecord
    from ai_module.models import AnomalyRecord
    from blockchain.models import TransactionRecord
    from sdn.models import FlowRule
    from threat_simulation.models import SimulationScenario

    if Device.objects.exists() or IoTMessage.objects.exists():
        return

    Device.objects.bulk_create([
        Device(name='Central Substation', type='substation', status='online'),
        Device(name='Grid Sensor A1', type='sensor', status='online'),
        Device(name='Control Node B2', type='controller', status='online'),
        Device(name='Transformer T5', type='transformer', status='maintenance'),
    ])

    IoTMessage.objects.bulk_create([
        IoTMessage(device_id='sensor-001', protocol='MQTT', payload={'temperature': 24.5, 'voltage': 221.0, 'humidity': 52, 'device_status': 'normal'}),
        IoTMessage(device_id='sensor-002', protocol='CoAP', payload={'temperature': 39.0, 'voltage': 250.0, 'humidity': 18, 'device_status': 'critical'}),
        IoTMessage(device_id='sensor-003', protocol='HTTPS', payload={'temperature': 18.3, 'voltage': 215.7, 'humidity': 60, 'device_status': 'warning'}),
    ])

    ThreatRecord.objects.bulk_create([
        ThreatRecord(name='Data exfiltration', confidentiality=9, integrity=5, availability=3, summary='Unauthorized transmission of sensitive grid data.'),
        ThreatRecord(name='Firmware tampering', confidentiality=6, integrity=9, availability=4, summary='Device firmware may have been altered.'),
        ThreatRecord(name='DDoS flood', confidentiality=2, integrity=4, availability=9, summary='A distributed denial-of-service event targeting control plane traffic.'),
    ])

    AnomalyRecord.objects.bulk_create([
        AnomalyRecord(device_id='sensor-002', data={'temperature': 39.0, 'voltage': 250.0}, score=0.85, is_anomaly=True),
        AnomalyRecord(device_id='sensor-003', data={'temperature': 18.3, 'voltage': 215.7}, score=0.45, is_anomaly=False),
    ])

    TransactionRecord.objects.bulk_create([
        TransactionRecord(tx_id='tx-001', sender='node-01', receiver='node-02', amount=120.5, data={'message': 'secure exchange', 'tx_hash': 'abc123'}),
        TransactionRecord(tx_id='tx-002', sender='node-03', receiver='node-04', amount=450.0, data={'message': 'state update', 'tx_hash': 'def456'}),
    ])

    FlowRule.objects.bulk_create([
        FlowRule(src='10.0.0.1', dst='10.0.0.2', protocol='TCP', action='allow'),
        FlowRule(src='10.0.0.5', dst='10.0.0.8', protocol='UDP', action='deny'),
    ])

    SimulationScenario.objects.bulk_create([
        SimulationScenario(name='Grid access breach', attack_type='Insider threat', is_active=True, score=12),
        SimulationScenario(name='Service disruption', attack_type='DDoS', is_active=False, score=8),
    ])


def ensure_default_portal_admin():
    if not User.objects.filter(username='portal_admin').exists():
        admin_user = User.objects.create_user(
            username='portal_admin',
            email='admin@smartgrid.local',
            password='Admin@12345',
            is_staff=True,
            is_superuser=False,
        )
        admin_user.save()


def admin_login(request):
    ensure_default_portal_admin()
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, 'Portal admin logged in successfully.')
            return redirect('admin_dashboard')
        error = 'Invalid credentials or you are not authorized as portal admin.'
    return render(request, 'monitoring/admin_login.html', {'error': error})


@user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='admin_login')
def admin_dashboard(request):
    ensure_sample_data()
    from infrastructure.models import Device
    from iot_integration.models import IoTMessage
    from iot_integration.models import IoTDatasetUpload
    from cybersecurity.models import ThreatRecord
    from ai_module.models import AnomalyRecord
    from blockchain.models import TransactionRecord
    from sdn.models import FlowRule
    from threat_simulation.models import SimulationScenario

    counts = {
        'users': User.objects.filter(is_active=True).count(),
        'datasets': IoTDatasetUpload.objects.count(),
        'activities': 0,
    }

    users = User.objects.order_by('username')
    recent_uploads = IoTDatasetUpload.objects.order_by('-uploaded_at')[:10]

    activity_logs = []
    for upload in recent_uploads:
        activity_logs.append({
            'timestamp': upload.uploaded_at,
            'event': 'Dataset upload',
            'details': f"{upload.name} ({upload.total_records} records, {upload.anomalies_detected} anomalies)",
        })
    for user in users:
        if user.last_login:
            activity_logs.append({
                'timestamp': user.last_login,
                'event': 'User login',
                'details': f"{user.username} logged in",
            })

    activity_logs.sort(key=lambda item: item['timestamp'], reverse=True)
    counts['activities'] = len(activity_logs)

    return render(request, 'monitoring/admin_dashboard.html', {
        'counts': counts,
        'users': users,
        'recent_uploads': recent_uploads,
        'activity_logs': activity_logs,
        'hide_nav_links': True,
    })


@login_required(login_url='login')
def index(request):
    ensure_sample_data()
    from infrastructure.models import Device
    from iot_integration.models import IoTMessage
    from iot_integration.models import IoTDatasetUpload
    from cybersecurity.models import ThreatRecord
    from ai_module.models import AnomalyRecord
    from blockchain.models import TransactionRecord
    from sdn.models import FlowRule
    from threat_simulation.models import SimulationScenario

    counts = {
        'devices': Device.objects.count(),
        'messages': IoTMessage.objects.count(),
        'threats': ThreatRecord.objects.count(),
        'anomalies': AnomalyRecord.objects.filter(is_anomaly=True).count(),
        'transactions': TransactionRecord.objects.count(),
        'flow_rules': FlowRule.objects.count(),
        'simulations': SimulationScenario.objects.count(),
        'dataset_uploads': IoTDatasetUpload.objects.count(),
    }

    top_anomalies = AnomalyRecord.objects.filter(is_anomaly=True).order_by('-score')[:5]
    top_threats = ThreatRecord.objects.order_by('-confidentiality', '-integrity', '-availability')[:5]
    recent_transactions = TransactionRecord.objects.order_by('-timestamp')[:5]
    active_scenarios = SimulationScenario.objects.filter(is_active=True)

    return render(request, 'monitoring/index.html', {
        'modules': MODULES,
        'counts': counts,
        'has_dataset': counts['dataset_uploads'] > 0,
        'top_anomalies': top_anomalies,
        'top_threats': top_threats,
        'recent_transactions': recent_transactions,
        'active_scenarios': active_scenarios,
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome to the Smart Grid platform.')
            return redirect('monitoring_index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required(login_url='login')
def module_detail(request, key):
    from infrastructure.models import Device
    from iot_integration.models import IoTMessage
    from cybersecurity.models import ThreatRecord
    from ai_module.models import AnomalyRecord
    from blockchain.models import TransactionRecord
    from sdn.models import FlowRule
    from threat_simulation.models import SimulationScenario

    module = next((m for m in MODULES if m[0] == key), None)
    if not module:
        raise Http404('Module not found')

    metrics = {}
    if key == 'infrastructure':
        metrics = {
            'Total devices': Device.objects.count(),
            'Online devices': Device.objects.filter(status__iexact='online').count(),
            'Last heartbeat': Device.objects.order_by('-last_heartbeat').first().last_heartbeat if Device.objects.exists() else 'N/A',
        }
    elif key == 'iot':
        metrics = {
            'Total messages': IoTMessage.objects.count(),
            'Last protocol': IoTMessage.objects.order_by('-received_at').first().protocol if IoTMessage.objects.exists() else 'N/A',
        }
    elif key == 'cybersecurity':
        metrics = {
            'Total threats': ThreatRecord.objects.count(),
            'High risk threats': ThreatRecord.objects.filter(confidentiality__gte=8).count(),
        }
    elif key == 'ai':
        metrics = {
            'Anomaly records': AnomalyRecord.objects.count(),
            'Active alerts': AnomalyRecord.objects.filter(is_anomaly=True).count(),
        }
    elif key == 'blockchain':
        metrics = {
            'Ledger entries': TransactionRecord.objects.count(),
            'Most recent transaction': TransactionRecord.objects.order_by('-timestamp').first().tx_id if TransactionRecord.objects.exists() else 'N/A',
        }
    elif key == 'sdn':
        metrics = {
            'Flow rules': FlowRule.objects.count(),
            'Blocked flows': FlowRule.objects.filter(action__iexact='deny').count(),
        }
    elif key == 'threat':
        metrics = {
            'Simulation scenarios': SimulationScenario.objects.count(),
            'Active scenarios': SimulationScenario.objects.filter(is_active=True).count(),
        }
    else:
        metrics = {
            'Modules available': len(MODULES),
        }

    return render(request, 'monitoring/module_detail.html', {'module': module, 'metrics': metrics})
