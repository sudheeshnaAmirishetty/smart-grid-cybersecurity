from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import FlowRule
import json

MODULE_TITLE = 'SDN Control'

@login_required(login_url='login')
def index(request):
    rules = FlowRule.objects.order_by('-id')[:12]
    total_rules = FlowRule.objects.count()
    blocked = FlowRule.objects.filter(action__iexact='deny').count()
    return render(request, 'sdn/index.html', {
        'title': MODULE_TITLE,
        'rules': rules,
        'total_rules': total_rules,
        'blocked': blocked,
    })

# dynamic routing rules CRUD

def list_rules(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    return JsonResponse(list(FlowRule.objects.values()), safe=False)


def create_rule(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    body = json.loads(request.body.decode('utf-8'))
    suspicious = body.get('suspicious', False)
    action = 'deny' if suspicious else body.get('action', 'allow')
    note = 'Suspicious node isolated and denied traffic.' if suspicious else 'Traffic rule created.'
    rule = FlowRule.objects.create(
        src=body.get('src', '0.0.0.0'),
        dst=body.get('dst', '0.0.0.0'),
        protocol=body.get('protocol', 'TCP'),
        action=action,
    )
    return JsonResponse({'id': rule.id, 'action': rule.action, 'note': note}, status=201)


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
    return HttpResponseNotAllowed(['GET', 'PUT', 'PATCH', 'DELETE'])