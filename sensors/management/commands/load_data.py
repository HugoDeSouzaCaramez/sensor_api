import os
import pandas as pd
from datetime import datetime
from django.core.management.base import BaseCommand
from sensors.models import SensorAcquisition
from django.conf import settings

class Command(BaseCommand):
    help = "Importa dados do CSV para o modelo SensorAcquisition"

    def handle(self, *args, **kwargs):
        # Construir o caminho absoluto para o arquivo CSV
        absolute_file_path = os.path.join(settings.BASE_DIR, 'smartfeed_v0_acquisition - smartfeed_v0_acquisition.csv')

        # Verificar se o arquivo existe
        if not os.path.exists(absolute_file_path):
            self.stdout.write(self.style.ERROR(f"Arquivo não encontrado: {absolute_file_path}"))
            return

        # Ler o arquivo CSV
        data = pd.read_csv(absolute_file_path)

        # Iterar sobre as linhas do DataFrame
        for index, row in data.iterrows():
            try:
                SensorAcquisition.objects.create(
                    platform_id=row['platform_id'],
                    fetch_datetime=datetime.strptime(row['fetch_datetime'], "%Y-%m-%d %H:%M:%S.%f"),
                    datetime_received=datetime.strptime(row['datetime_received'], "%Y-%m-%d %H:%M:%S.%f"),
                    sensor_acquisitions=row['sensor_acquisitions']
                )
                self.stdout.write(self.style.SUCCESS(f"Importado registro {index + 1} com sucesso."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Erro ao importar o registro {index + 1}: {e}"))
