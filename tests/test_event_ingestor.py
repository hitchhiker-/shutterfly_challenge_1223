import unittest
from event_ingestor import ingest
from events import Customer, SiteVisit, Image, Order

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
        self.assertIn("96f55c7d8f42", self.data_store["customers"])
        self.assertIsInstance(self.data_store["customers"]["96f55c7d8f42"], Customer)

    # Additional tests for SITE_VISIT, IMAGE, ORDER

if __name__ == '__main__':
    unittest.main()
