import os
import pandas as pd
from datetime import datetime
from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate


class SensorsConfig(AppConfig):
    name = 'sensors'

    def ready(self):
        post_migrate.connect(self.load_data, sender=self)

    def load_data(self, *args, **kwargs):
        from sensors.models import SensorAcquisition

        absolute_file_path = os.path.join(settings.BASE_DIR, 'smartfeed_v0_acquisition - smartfeed_v0_acquisition.csv')

        if not os.path.exists(absolute_file_path):
            print(f"Arquivo não encontrado: {absolute_file_path}")
            return

        data = pd.read_csv(absolute_file_path)

        for index, row in data.iterrows():
            try:
                if not SensorAcquisition.objects.filter(
                    platform_id=row['platform_id'],
                    fetch_datetime=datetime.strptime(row['fetch_datetime'], "%Y-%m-%d %H:%M:%S.%f")
                ).exists():
                    SensorAcquisition.objects.create(
                        platform_id=row['platform_id'],
                        fetch_datetime=datetime.strptime(row['fetch_datetime'], "%Y-%m-%d %H:%M:%S.%f"),
                        datetime_received=datetime.strptime(row['datetime_received'], "%Y-%m-%d %H:%M:%S.%f"),
                        sensor_acquisitions=row['sensor_acquisitions']
                    )
                    print(f"Importado registro {index + 1} com sucesso.")
                else:
                    print(f"Registro {index + 1} já existe no banco de dados.")
            except Exception as e:
                print(f"Erro ao importar o registro {index + 1}: {e}")
