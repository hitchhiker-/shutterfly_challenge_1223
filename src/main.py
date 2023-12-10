import json

from event_ingestor import ingest
from ltv_calculator import top_x_simple_ltv_customers

def main():
    data_store = {
        "customers": {},
        "site_visits": {},
        "images": {},
        "orders": {}
    }

    # Adjust the path if your working directory is different
    with open('input/input.txt', 'r') as file:
        events = json.load(file)

    for event in events:
        ingest(event, data_store)

    # Further processing...

if __name__ == "__main__":
    main()