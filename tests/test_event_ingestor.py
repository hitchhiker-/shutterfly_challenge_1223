import unittest
from src.event_ingestor import ingest
from src.events import Customer, SiteVisit, Image, Order

class TestEventIngestor(unittest.TestCase):

    def setUp(self):
        self.data_store = {
            "customers": {},
            "site_visits": {},
            "images": {},
            "orders": {}
        }

    def test_ingest_customer(self):
        event = {
            "type": "CUSTOMER",
            "verb": "NEW",
            "key": "96f55c7d8f42",
            "event_time": "2017-01-06T12:46:46.384Z",
            "last_name": "Smith",
            "adr_city": "Middletown",
            "adr_state": "AK"
        }
        ingest(event, self.data_store)
        self.assertIn("96f55c7d8f42", self.data_store["customers"].keys()[0])
        self.assertIsInstance(self.data_store["customers"]["96f55c7d8f42"], Customer)

    def test_ingest_site_visit(self):
        event = {
            "type": "SITE_VISIT",
            "verb": "NEW",
            "key": "ac05e815502f",
            "event_time": "2017-01-06T12:45:52.041Z",
            "customer_id": "96f55c7d8f42"
        }
        ingest(event, self.data_store)
        self.assertIn("ac05e815502f", self.data_store["site_visits"])
        self.assertIsInstance(self.data_store["site_visits"]["ac05e815502f"], SiteVisit)

    def test_ingest_image(self):
        event = {
            "type": "IMAGE",
            "verb": "UPLOAD",
            "key": "d8ede43b1d9f",
            "event_time": "2017-01-06T12:47:12.344Z",
            "customer_id": "96f55c7d8f42",
            "camera_make": "Canon",
            "camera_model": "EOS 80D"
        }
        ingest(event, self.data_store)
        self.assertIn("d8ede43b1d9f", self.data_store["images"])
        self.assertIsInstance(self.data_store["images"]["d8ede43b1d9f"], Image)

    def test_ingest_order(self):
        event = {
            "type": "ORDER",
            "verb": "NEW",
            "key": "68d84e5d1a88",
            "event_time": "2017-01-06T12:55:55.555Z",
            "customer_id": "96f55c7d8f42",
            "total_amount": "12.34 USD"
        }
        ingest(event, self.data_store)
        self.assertIn("68d84e5d1a88", self.data_store["orders"])
        self.assertIsInstance(self.data_store["orders"]["68d84e5d1a88"], Order)

if __name__ == '__main__':
    unittest.main()
