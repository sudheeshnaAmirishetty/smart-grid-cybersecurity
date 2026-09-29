from django.db import models

class AnomalyRecord(models.Model):
    device_id = models.CharField(max_length=140)
    data = models.JSONField(default=dict)
    score = models.FloatField(default=0.0)
    is_anomaly = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.device_id} anomaly={self.is_anomaly}'