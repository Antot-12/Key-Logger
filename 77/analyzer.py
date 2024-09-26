import os
import matplotlib.pyplot as plt
from datetime import datetime

import config


def analyze_data():
    if config['data_analysis']:
        log_path = os.path.join(config['log_directory'], config['log_file'])
        if os.path.exists(log_path):
            with open(log_path, 'r') as file:
                data = file.readlines()

            key_counts = {}
            for line in data:
                if 'COMBO' in line:
                    continue
                key = line.split(' ')[-1].strip()
                key_counts[key] = key_counts.get(key, 0) + 1

            analysis_dir = config['analysis_directory']
            if not os.path.exists(analysis_dir):
                os.makedirs(analysis_dir)

            plt.figure(figsize=(10, 6))
            plt.bar(key_counts.keys(), key_counts.values())
            plt.xlabel('Keys')
            plt.ylabel('Frequency')
            plt.title('Key Press Frequency Analysis')
            plt.xticks(rotation=90)
            plt.tight_layout()
            plt.savefig(os.path.join(analysis_dir, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"))
            plt.close()
