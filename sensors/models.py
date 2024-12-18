from django.db import models

class SensorAcquisition(models.Model):
    id = models.AutoField(primary_key=True)
    platform_id = models.CharField(max_length=255)
    fetch_datetime = models.DateTimeField()
    datetime_received = models.DateTimeField()
    sensor_acquisitions = models.TextField()

    def __str__(self):
        return f"{self.platform_id} - {self.fetch_datetime}"
