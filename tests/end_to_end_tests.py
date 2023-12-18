import unittest
from src.event_ingestor import ingest
from src.ltv_calculator import TopXSimpleLTVCustomers

class EndToEndTest(unittest.TestCase):
    def setUp(self):
        self.data_store = {
            "customers": {},
            "site_visits": {},
            "images": {},
            "orders": {}
        }

    def test_full_workflow(self):
        # Sample events with a mix of different customers and activities
        events = [
            {"type": "CUSTOMER", "verb": "NEW", "key": "cust1", "event_time": "2020-01-01T12:00:00.000Z", "last_name": "Smith", "adr_city": "CityA", "adr_state": "StateA"},
            {"type": "SITE_VISIT", "verb": "NEW", "key": "visit1", "event_time": "2020-01-02T12:00:00.000Z", "customer_id": "cust1", "tags": []},
            {"type": "IMAGE", "verb": "UPLOAD", "key": "img1", "event_time": "2020-01-02T13:00:00.000Z", "customer_id": "cust1", "camera_make": "Canon", "camera_model": "EOS 80D"},
            {"type": "ORDER", "verb": "NEW", "key": "order1", "event_time": "2020-01-03T12:00:00.000Z", "customer_id": "cust1", "total_amount": "100.00 USD"},
            # Add events for additional customers and activities to simulate a real-world scenario
        ]

        # Ingest events
        for event in events:
            ingest(event, self.data_store)

        # Calculate LTV for top X customers
        top_customers = TopXSimpleLTVCustomers(5, self.data_store)

        # Assertions
        self.assertEqual(len(top_customers), min(5, len(self.data_store["customers"])))  # Ensure we don't exceed the number of customers
        self.assertIn("cust1", {cust_id for cust_id, _ in top_customers})  # Assert 'cust1' is in the top customers

        # Further detailed assertions
        for customer_id, ltv in top_customers:
            self.assertIsInstance(ltv, float)  # Ensure that LTV is a float value
            # Add additional assertions as necessary

if __name__ == '__main__':
    unittest.main()
    