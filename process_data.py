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
        "média": pd.Series(distances).mean(),
        "mediana": pd.Series(distances).median(),
        "máximo": pd.Series(distances).max(),
        "mínimo": pd.Series(distances).min(),
        "desvio_padrão": pd.Series(distances).std()
    }


def plot_and_save_graphs(df, output_dir="plots"):
    import os

    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df[['média', 'mediana', 'máximo', 'mínimo', 'desvio_padrão']])
    plt.title("Distribuição das Estatísticas por Sensor")
    plt.xlabel("Métricas")
    plt.ylabel("Valores")
    original_filepath = os.path.join(output_dir, "todas_metricas_boxplot.png")
    plt.savefig(original_filepath)
    print(f"Gráfico original salvo em: {original_filepath}")
    plt.show()
    plt.close()

    metrics = ['média', 'mediana', 'máximo', 'mínimo', 'desvio_padrão']
    for metric in metrics:
        plt.figure(figsize=(10, 6))
        sns.boxplot(y=df[metric])
        plt.title(f"Distribuição de {metric} por Sensor")
        plt.ylabel(metric)
        plt.xlabel("Sensores")
        metric_filepath = os.path.join(output_dir, f"{metric}_boxplot.png")
        plt.savefig(metric_filepath)
        print(f"Gráfico de {metric} salvo em: {metric_filepath}")
        plt.show()
        plt.close()

    plt.figure(figsize=(12, 8))
    for metric in metrics:
        sns.kdeplot(df[metric], label=metric, fill=True, alpha=0.4)
    plt.title("Distribuição das Métricas por Sensor")
    plt.xlabel("Valores")
    plt.ylabel("Densidade")
    plt.legend()
    distribution_filepath = os.path.join(output_dir, "distribuicao_metricas.png")
    plt.savefig(distribution_filepath)
    print(f"Gráfico de distribuição salvo em: {distribution_filepath}")
    plt.show()
    plt.close()


def main():
    platform_ids = get_sensor_platform_ids()
    results = []

    for i, platform_id in enumerate(platform_ids):
        if i >= 3:
            break
        try:
            data = get_last_acquisition(platform_id)
            stats = process_data(data['sensor_acquisitions'])
            stats['platform_id'] = platform_id
            results.append(stats)
        except Exception as e:
            print(f"Erro ao processar platform_id {platform_id}: {e}")

    df = pd.DataFrame(results)
    df.to_csv("sensor_statistics.csv", index=False)

    plot_and_save_graphs(df)

if __name__ == "__main__":
    main()
