from django.db import models

class SimulationScenario(models.Model):
    name = models.CharField(max_length=180)
    attack_type = models.CharField(max_length=120)
    is_active = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.attack_type})'