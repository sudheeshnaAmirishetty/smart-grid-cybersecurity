import os

root = os.path.dirname(os.path.abspath(__file__))
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
    write(os.path.join(root, app, '__init__.py'), '')
    write(os.path.join(root, app, 'apps.py'), f"""from django.apps import AppConfig

class {app.capitalize().replace('_','')}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '{app}'
""")
    write(os.path.join(root, app, 'models.py'), """from django.db import models

class StatusEntry(models.Model):
    name = models.CharField(max_length=180)
    status = models.CharField(max_length=128)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}: {self.status}"
""")
    write(os.path.join(root, app, 'views.py'), f"""from django.shortcuts import render

MODULE_TITLE = '{title}'

def index(request):
    return render(request, '{app}/index.html', {{'title': MODULE_TITLE}})
""")
    write(os.path.join(root, app, 'urls.py'), """from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
""")
    write(os.path.join(root, app, 'admin.py'), """from django.contrib import admin
from .models import StatusEntry

admin.site.register(StatusEntry)
""")
    template = f"""{{% extends 'base.html' %}}
{{% block content %}}
<h1>{title}</h1>
<p>{title} module landing page.</p>
<ul>
  <li>Designed function for this module</li>
  <li>Replace with real logic and APIs</li>
</ul>
{{% endblock %}}
"""
    write(os.path.join(root, 'templates', app, 'index.html'), template)

print('Apps scaffolding complete')
