import json
from event_ingestor import ingest
from ltv_calculator import TopXSimpleLTVCustomers

def main():
    data_store = {
        "customers": {},
        "site_visits": {},
        "images": {},
        "orders": {}
    }

    # Read and process the input file
    with open('input/input.txt', 'r') as file:
        events = json.load(file)
        for event in events:
            ingest(event, data_store)
    
    # Calculate and display the top X customers based on LTV
    top_customers = TopXSimpleLTVCustomers(10, data_store)  # Adjust the number as needed
    
    # Write the output to 'output/output.txt'
    with open('output/output.txt', 'w') as output_file:
        for customer_id, ltv in top_customers:
            output_file.write(f"Customer ID: {customer_id}, LTV: {ltv}\n")
    
    # Print the output file path
    print("\nOutput written to output/output.txt\n")

if __name__ == "__main__":
    main()
