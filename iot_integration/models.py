from django.db import models

class IoTMessage(models.Model):
    device_id = models.CharField(max_length=140)
    protocol = models.CharField(max_length=80, default='MQTT')
    payload = models.JSONField(default=dict)
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.device_id} @ {self.received_at}'


class IoTDatasetUpload(models.Model):
    name = models.CharField(max_length=200)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    total_records = models.IntegerField(default=0)
    anomalies_detected = models.IntegerField(default=0)
    summary = models.JSONField(default=dict)

    def __str__(self):
        return f'{self.name} ({self.uploaded_at:%Y-%m-%d %H:%M})'