import pandas as pd
from celery import shared_task

@shared_task(bind=True)
def test_func(self):
    counts = []
    for i in range(10):
        print(i, "Count")
        counts.append(i)
        print(counts)
    return counts

@shared_task(bind=True)
def add_numbers(a, b):
    return a + b


@shared_task(bind=True)
def read_sheet():
    # Specify the path to your CSV file.
    csv_file_path = 'combined_AARTIIND.csv'
    # Use the read_csv function to read the CSV file into a DataFrame.
    df = pd.read_csv(csv_file_path)
    return df
