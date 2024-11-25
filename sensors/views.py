from django.http import JsonResponse, Http404
from .models import SensorAcquisition

def sensor_acquisitions(request):
    data = SensorAcquisition.objects.all().values()
    return JsonResponse(list(data), safe=False)

def sensor_last_acquisition(request, platform_id):
    try:
        latest_acquisition = SensorAcquisition.objects.filter(platform_id=platform_id).order_by('-fetch_datetime').first()

        if not latest_acquisition:
            raise Http404("Nenhum dado encontrado para o sensor especificado.")


        data = {
            "id": latest_acquisition.id,
            "platform_id": latest_acquisition.platform_id,
            "fetch_datetime": latest_acquisition.fetch_datetime,
            "datetime_received": latest_acquisition.datetime_received,
            "sensor_acquisitions": latest_acquisition.sensor_acquisitions,
        }
        return JsonResponse(data)
    except SensorAcquisition.DoesNotExist:
        raise Http404("Sensor não encontrado.")