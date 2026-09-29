from django.db import models

class ThreatRecord(models.Model):
    name = models.CharField(max_length=180)
    confidentiality = models.IntegerField(default=0)
    integrity = models.IntegerField(default=0)
    availability = models.IntegerField(default=0)
    summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def risk_level(self):
        score = self.confidentiality + self.integrity + self.availability
        if score > 20:
            return 'high'
        if score > 10:
            return 'medium'
        return 'low'

    def __str__(self):
        return f'{self.name} ({self.risk_level()})'