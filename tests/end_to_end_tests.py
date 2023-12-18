import unittest
from src.event_ingestor import ingest
from src.ltv_calculator import TopXSimpleLTVCustomers, get_saturday, get_sunday
from src.events import Customer, SiteVisit, Image, Order

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
            {"type": "CUSTOMER", "verb": "UPDATE", "key": "cust1", "event_time": "2020-01-04T12:00:00.000Z", "last_name": "Smith1", "adr_city": "CityB", "adr_state": "StateB"},
            {"type": "SITE_VISIT", "verb": "NEW", "key": "visit2", "event_time": "2020-01-05T12:00:00.000Z", "customer_id": "cust1", "tags": []},
            {"type": "IMAGE", "verb": "UPLOAD", "key": "img2", "event_time": "2020-01-05T13:00:00.000Z", "customer_id": "cust1", "camera_make": "Canon", "camera_model": "EOS 80D"},
            {"type": "ORDER", "verb": "NEW", "key": "order2", "event_time": "2020-01-06T12:00:00.000Z", "customer_id": "cust1", "total_amount": "200.00 USD"},
            {"type": "CUSTOMER", "verb": "NEW", "key": "cust2", "event_time": "2020-01-01T12:00:00.000Z", "last_name": "Doe", "adr_city": "CityC", "adr_state": "StateC"},
            {"type": "SITE_VISIT", "verb": "NEW", "key": "visit3", "event_time": "2020-01-02T12:00:00.000Z", "customer_id": "cust2", "tags": []},
            {"type": "IMAGE", "verb": "UPLOAD", "key": "img3", "event_time": "2020-01-02T13:00:00.000Z", "customer_id": "cust2", "camera_make": "Canon", "camera_model": "EOS 80D"},
            {"type": "ORDER", "verb": "NEW", "key": "order3", "event_time": "2020-01-03T12:00:00.000Z", "customer_id": "cust2", "total_amount": "300.00 USD"},
            {"type": "CUSTOMER", "verb": "UPDATE", "key": "cust2", "event_time": "2020-01-04T12:00:00.000Z", "last_name": "Doe1", "adr_city": "CityD", "adr_state": "StateD"},
            {"type": "SITE_VISIT", "verb": "NEW", "key": "visit4", "event_time": "2020-01-05T12:00:00.000Z", "customer_id": "cust2", "tags": []},
            {"type": "IMAGE", "verb": "UPLOAD", "key": "img4", "event_time": "2020-01-05T13:00:00.000Z", "customer_id": "cust2", "camera_make": "Canon", "camera_model": "EOS 80D"},
            {"type": "ORDER", "verb": "NEW", "key": "order4", "event_time": "2020-01-06T12:00:00.000Z", "customer_id": "cust2", "total_amount": "400.00 USD"},
            {"type": "CUSTOMER", "verb": "NEW", "key": "cust3", "event_time": "2020-01-01T12:00:00.000Z", "last_name": "Johnson", "adr_city": "CityE", "adr_state": "StateE"},
            {"type": "SITE_VISIT", "verb": "NEW", "key": "visit5", "event_time": "2020-01-02T12:00:00.000Z", "customer_id": "cust3", "tags": []},
            {"type": "IMAGE", "verb": "UPLOAD", "key": "img5", "event_time": "2020-01-02T13:00:00.000Z", "customer_id": "cust3", "camera_make": "Canon", "camera_model": "EOS 80D"},
            {"type": "ORDER", "verb": "NEW", "key": "order5", "event_time": "2020-01-03T12:00:00.000Z", "customer_id": "cust3", "total_amount": "500.00 USD"},
            {"type": "CUSTOMER", "verb": "UPDATE", "key": "cust3", "event_time": "2020-01-04T12:00:00.000Z", "last_name": "Johnson1", "adr_city": "CityF", "adr_state": "StateF"},
            {"type": "SITE_VISIT", "verb": "NEW", "key": "visit6", "event_time": "2020-01-05T12:00:00.000Z", "customer_id": "cust3", "tags": []},
            {"type": "IMAGE", "verb": "UPLOAD", "key": "img6", "event_time": "2020-01-05T13:00:00.000Z", "customer_id": "cust3", "camera_make": "Canon", "camera_model": "EOS 80D"},
            {"type": "ORDER", "verb": "NEW", "key": "order6", "event_time": "2020-01-06T12:00:00.000Z", "customer_id": "cust3", "total_amount": "600.00 USD"}
        ]

        # Ingest events
        for event in events:
            ingest(event, self.data_store)

        # Calculate LTV for top X customers
        top_customers = TopXSimpleLTVCustomers(5, self.data_store)

        # Print the output
        print(top_customers)

        # Assertions
        self.assertEqual(len(top_customers), min(5, len(self.data_store["customers"])))
        self.assertIn("cust1", {cust_id for cust_id, _ in top_customers})

        # Detailed LTV assertions
        for customer_id, ltv in top_customers:
            self.assertIsInstance(ltv, float)
            # Comparing with manually calculated LTV
            expected_ltv = ltv_calc_manual.get(customer_id)
            self.assertAlmostEqual(ltv, expected_ltv, places=2)

        # Validation of customer ranking
        expected_ranking = sorted(ltv_calc_manual, reverse=True)  # Sort manually calculated LTVs
        actual_ranking = [cust_id for cust_id, _ in top_customers]
        self.assertEqual(actual_ranking, expected_ranking[:len(actual_ranking)])

        

# Manual calculation of expected LTV
ltv_calc_manual = {"cust1": 78000.00, "cust2": 182000.00, "cust3": 286000.00}



if __name__ == '__main__':
    unittest.main()
