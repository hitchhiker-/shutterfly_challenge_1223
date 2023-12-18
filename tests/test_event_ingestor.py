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

    def test_ingest_new_customer(self):
        event = {
            "type": "CUSTOMER",
            "verb": "NEW",
            "key": "customer1",
            "event_time": "2020-01-01T00:00:00.000Z",
            "last_name": "Doe",
            "adr_city": "New York",
            "adr_state": "NY"
        }
        ingest(event, self.data_store)
        self.assertIn("customer1", self.data_store["customers"])
        self.assertIsInstance(self.data_store["customers"]["customer1"], Customer)

    def test_ingest_site_visit(self):
        event = {
            "type": "SITE_VISIT",
            "verb": "NEW",
            "key": "visit1",
            "event_time": "2020-01-02T00:00:00.000Z",
            "customer_id": "customer1",
            "tags": []
        }
        ingest(event, self.data_store)
        self.assertIn("visit1", self.data_store["site_visits"])
        self.assertIsInstance(self.data_store["site_visits"]["visit1"], SiteVisit)

    def test_ingest_image_upload(self):
        event = {
            "type": "IMAGE",
            "verb": "UPLOAD",
            "key": "image1",
            "event_time": "2020-01-03T00:00:00.000Z",
            "customer_id": "customer1",
            "camera_make": "Canon",
            "camera_model": "EOS 80D"
        }
        ingest(event, self.data_store)
        self.assertIn("image1", self.data_store["images"])
        self.assertIsInstance(self.data_store["images"]["image1"], Image)

    def test_ingest_new_order(self):
        event = {
            "type": "ORDER",
            "verb": "NEW",
            "key": "order1",
            "event_time": "2020-01-04T00:00:00.000Z",
            "customer_id": "customer1",
            "total_amount": "100.00 USD"
        }
        ingest(event, self.data_store)
        self.assertIn("order1", self.data_store["orders"])
        self.assertIsInstance(self.data_store["orders"]["order1"], Order)

    # Continuing from the previous test class...

    def test_ingest_update_customer(self):
        # Testing update functionality for an existing customer
        new_event = {
            "type": "CUSTOMER",
            "verb": "UPDATE",
            "key": "customer1",
            "event_time": "2020-01-05T00:00:00.000Z",
            "last_name": "Smith",
            "adr_city": "Boston",
            "adr_state": "MA"
        }
        ingest(new_event, self.data_store)
        updated_customer = self.data_store["customers"]["customer1"]
        self.assertEqual(updated_customer.last_name, "Smith")
        self.assertEqual(updated_customer.city, "Boston")
        self.assertEqual(updated_customer.state, "MA")

    def test_ingest_update_order(self):
        # Testing update functionality for an existing order
        new_event = {
            "type": "ORDER",
            "verb": "UPDATE",
            "key": "order1",
            "event_time": "2020-01-06T00:00:00.000Z",
            "customer_id": "customer1",
            "total_amount": "150.00 USD"
        }
        ingest(new_event, self.data_store)
        updated_order = self.data_store["orders"]["order1"]
        self.assertEqual(updated_order.total_amount, 150.00)

    def test_ingest_invalid_event_type(self):
        # Testing ingestion of an event with an invalid type
        invalid_event = {
            "type": "INVALID_TYPE",
            "verb": "NEW",
            "key": "somekey",
            "event_time": "2020-01-07T00:00:00.000Z"
        }
        ingest(invalid_event, self.data_store)
        # Assuming the ingest function silently ignores invalid events
        # Verify that no new entries are created in the data store
        self.assertNotIn("somekey", self.data_store["customers"])
        self.assertNotIn("somekey", self.data_store["site_visits"])
        self.assertNotIn("somekey", self.data_store["images"])
        self.assertNotIn("somekey", self.data_store["orders"])

    # Add more tests to cover edge cases or error handling scenarios



if __name__ == '__main__':
    unittest.main()
