import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json


BASE_URL = "http://localhost:8000"
LIST_SENSORS_ENDPOINT = '/sensor_acquisitions/'
LAST_ACQUISITION_ENDPOINT = "/sensor_last_acquisition/"

def get_sensor_platform_ids():
    response = requests.get(f"{BASE_URL}{LIST_SENSORS_ENDPOINT}")
    response.raise_for_status()
    sensor_data = response.json()
    platform_ids = [sensor['platform_id'] for sensor in sensor_data]
    return platform_ids

def get_last_acquisition(platform_id):
    response = requests.get(f"{BASE_URL}{LAST_ACQUISITION_ENDPOINT}{platform_id}/")
    response.raise_for_status()
    acquisition = response.json()
    acquisition['sensor_acquisitions'] = json.loads(acquisition['sensor_acquisitions'])
    return acquisition

def process_data(data):
    distances = data['distance']
    return {
        "mean": pd.Series(distances).mean(),
        "median": pd.Series(distances).median(),
        "max": pd.Series(distances).max(),
        "min": pd.Series(distances).min(),
        "std_dev": pd.Series(distances).std()
    }

def main():
    platform_ids = get_sensor_platform_ids()
    results = []

    for platform_id in platform_ids:
        try:
            data = get_last_acquisition(platform_id)
            stats = process_data(data['sensor_acquisitions'])
            stats['platform_id'] = platform_id
            results.append(stats)
        except Exception as e:
            print(f"Erro ao processar platform_id {platform_id}: {e}")


    df = pd.DataFrame(results)
    df.to_csv("sensor_statistics.csv", index=False)

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df[['mean', 'median', 'max', 'min', 'std_dev']])
    plt.title("Distribuição das Estatísticas por Sensor")
    plt.show()

if __name__ == "__main__":
    main()
