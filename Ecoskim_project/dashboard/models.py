from django.db import models


class WasteDetection(models.Model):

    detected_at = models.DateTimeField(auto_now_add=True)

    waste_name = models.CharField(max_length=100)

    waste_type = models.CharField(max_length=50)

    confidence = models.FloatField()

    classification = models.CharField(max_length=50)

    def __str__(self):
        return self.waste_name