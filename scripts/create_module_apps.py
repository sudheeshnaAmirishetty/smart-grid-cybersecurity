import os
root = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(root, '..'))
apps = [
    ('infrastructure','Smart Grid Infrastructure'),
    ('iot_integration','IoT Integration'),
    ('cybersecurity','Cybersecurity Analysis'),
    ('ai_module','Artificial Intelligence'),
    ('blockchain','Blockchain Security'),
    ('sdn','SDN'),
    ('threat_simulation','Threat Simulation'),
    ('monitoring','Monitoring and Reporting'),
]

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

for app, title in apps:
    if app == 'monitoring':
        continue
    write(os.path.join(root, app, '__init__.py'), '')
    write(os.path.join(root, app, 'apps.py'), f"""from django.apps import AppConfig

class {app.capitalize().replace('_','')}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '{app}'
""")
    # Model placeholder
    write(os.path.join(root, app, 'models.py'), """from django.db import models

class StatusEntry(models.Model):
    name = models.CharField(max_length=180)
    status = models.CharField(max_length=128)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}: {self.status}"
""")
    # Views placeholder
    write(os.path.join(root, app, 'views.py'), f"""from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import StatusEntry

MODULE_TITLE = '{title}'

def index(request):
    return render(request, '{app}/index.html', {{'title': MODULE_TITLE}})

# API CRUD for module status

def list_items(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    objects = list(StatusEntry.objects.values())
    return JsonResponse(objects, safe=False)


def create_item(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    import json
    data = json.loads(request.body.decode('utf-8'))
    item = StatusEntry.objects.create(name=data.get('name', 'unknown'), status=data.get('status', 'ok'))
    return JsonResponse({{'id': item.id, 'name': item.name, 'status': item.status}}, status=201)


def detail(request, item_id):
    item = get_object_or_404(StatusEntry, pk=item_id)
    return JsonResponse({{'id': item.id, 'name': item.name, 'status': item.status, 'updated': item.updated}})


def update_item(request, item_id):
    if request.method not in ['PUT', 'PATCH']:
        return HttpResponseNotAllowed(['PUT', 'PATCH'])
    import json
    data = json.loads(request.body.decode('utf-8'))
    item = get_object_or_404(StatusEntry, pk=item_id)
    item.name = data.get('name', item.name)
    item.status = data.get('status', item.status)
    item.save()
    return JsonResponse({{'id': item.id, 'name': item.name, 'status': item.status}})


def delete_item(request, item_id):
    if request.method != 'DELETE':
        return HttpResponseNotAllowed(['DELETE'])
    item = get_object_or_404(StatusEntry, pk=item_id)
    item.delete()
    return JsonResponse({{'deleted': item_id}})
""")
    write(os.path.join(root, app, 'urls.py'), """from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', views.list_items, name='api_list'),
    path('api/create/', views.create_item, name='api_create'),
    path('<int:item_id>/', views.detail, name='api_detail'),
    path('<int:item_id>/edit/', views.update_item, name='api_update'),
    path('<int:item_id>/delete/', views.delete_item, name='api_delete'),
]
""")
    write(os.path.join(root, 'templates', app, 'index.html'), f"""{{% extends 'base.html' %}}
{{% block content %}}
<h1>{title}</h1>
<p>This is the {title} module. Use /{app}/api/ for CRUD JSON interface.</p>
{{% endblock %}}
""")

print('Created apps, models, views, urls, templates for module scaffold')
