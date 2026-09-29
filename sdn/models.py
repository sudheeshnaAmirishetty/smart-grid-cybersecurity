from django.db import models

class FlowRule(models.Model):
    src = models.CharField(max_length=140)
    dst = models.CharField(max_length=140)
    protocol = models.CharField(max_length=40, default='TCP')
    action = models.CharField(max_length=40, default='allow')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.src}->{self.dst} {self.protocol} {self.action}'