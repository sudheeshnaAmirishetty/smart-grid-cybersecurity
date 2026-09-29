from django.db import models

class Report(models.Model):
    module = models.CharField(max_length=120)
    rv = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.module} report @ {self.created_at}"