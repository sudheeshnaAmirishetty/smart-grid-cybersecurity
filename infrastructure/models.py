from django.db import models

class Device(models.Model):
    name = models.CharField(max_length=180)
    type = models.CharField(max_length=128)
    status = models.CharField(max_length=128, default='online')
    last_heartbeat = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} ({self.type})'