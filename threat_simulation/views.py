from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import SimulationScenario
import json

MODULE_TITLE = 'Threat Simulation'

@login_required(login_url='login')
def index(request):
    scenarios = SimulationScenario.objects.order_by('-id')[:12]
    total_scenarios = SimulationScenario.objects.count()
    active_scenarios = SimulationScenario.objects.filter(is_active=True).count()
    return render(request, 'threat_simulation/index.html', {
        'title': MODULE_TITLE,
        'scenarios': scenarios,
        'total_scenarios': total_scenarios,
        'active_scenarios': active_scenarios,
    })

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
    return HttpResponseNotAllowed(['GET', 'DELETE'])