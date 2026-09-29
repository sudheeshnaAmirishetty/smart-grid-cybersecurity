from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import ThreatRecord
import json

MODULE_TITLE = 'Cybersecurity Analysis'

@login_required(login_url='login')
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
    if request.method == 'GET':
        return render(request, 'cybersecurity/cia_classify.html')

    if request.method != 'POST':
        return HttpResponseNotAllowed(['GET', 'POST'])

    try:
        if request.content_type == 'application/json':
            body = json.loads(request.body.decode('utf-8') or '{}')
        else:
            body = request.POST
    except Exception:
        body = request.POST

    c = int(body.get('confidentiality', 0) or 0)
    i = int(body.get('integrity', 0) or 0)
    a = int(body.get('availability', 0) or 0)
    score = c + i + a
    if score > 20:
        level = 'high'
    elif score > 10:
        level = 'medium'
    else:
        level = 'low'
    recommendations = []
    if c >= 7:
        recommendations.append('Apply encryption, access controls, and secure device authentication.')
    if i >= 7:
        recommendations.append('Enable data validation, integrity checks, and tamper-evident logging.')
    if a >= 7:
        recommendations.append('Deploy redundancy, failover systems, and DDoS protection to maintain availability.')
    if not recommendations:
        recommendations.append('Maintain secure configurations, patching, and continuous monitoring.')

    result = {
        'cia': {'confidentiality': c, 'integrity': i, 'availability': a},
        'risk_level': level,
        'score': score,
        'recommendations': recommendations,
    }

    if request.content_type == 'application/json':
        return JsonResponse(result)
    return render(request, 'cybersecurity/cia_classify.html', {'result': result, 'values': {'confidentiality': c, 'integrity': i, 'availability': a}})
