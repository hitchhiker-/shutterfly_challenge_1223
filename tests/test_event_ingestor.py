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
        # Testing ingestion of a new customer
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
        # Testing ingestion of a new site visit
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
        # Testing ingestion of a new image upload
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
        # Testing ingestion of a new order
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
        # We are expecting an exception to be raised
        new_event = {
            "type": "INVALID_TYPE",
            "verb": "NEW",
            "key": "event1",
            "event_time": "2020-01-08T00:00:00.000Z"
        }
        with self.assertRaises(ValueError):
            ingest(new_event, self.data_store)

    def test_ingest_missing_key(self):
        # Testing ingestion of an event with a missing key
        # We are expecting an exception to be raised
        new_event = {
            "type": "SITE_VISIT",
            "verb": "NEW",
            "event_time": "2020-01-09T00:00:00.000Z",
            "customer_id": "customer1"
            # Missing 'tags' key
        }
        with self.assertRaises(ValueError):
            ingest(new_event, self.data_store)


    def test_ingest_missing_event_time(self):
        # Testing ingestion of an event with a missing event_time
        # We are expecting an exception to be raised
        new_event = {
            "type": "IMAGE",
            "verb": "UPLOAD",
            "key": "image1",
            "customer_id": "customer1",
            "camera_make": "Nikon",
            "camera_model": "D850"
        }
        with self.assertRaises(ValueError):
            ingest(new_event, self.data_store)


    def test_ingest_partial_update_customer(self):
        # Create an initial customer
        initial_event = {
            "type": "CUSTOMER",
            "verb": "NEW",
            "key": "customer1",
            "event_time": "2020-01-01T00:00:00.000Z",
            "last_name": "Doe",
            "adr_city": "New York",
            "adr_state": "NY"
        }
        ingest(initial_event, self.data_store)

        # Update the customer with partial data
        update_event = {
            "type": "CUSTOMER",
            "verb": "UPDATE",
            "key": "customer1",
            "event_time": "2020-01-02T00:00:00.000Z",
            "last_name": "Smith"
        }
        ingest(update_event, self.data_store)
    
        updated_customer = self.data_store["customers"]["customer1"]
        self.assertEqual(updated_customer.last_name, "Smith")
        self.assertEqual(updated_customer.city, "New York")  # City should remain unchanged

    def test_ingest_invalid_event_time_format(self):
        # Testing ingestion of an event with an invalid event_time format
        invalid_event = {
            "type": "CUSTOMER",
            "verb": "NEW",
            "key": "customer2",
            "event_time": "invalid_date",
            "last_name": "Johnson",
            "adr_city": "Boston",
            "adr_state": "MA"
        }
        with self.assertRaises(ValueError):
            ingest(invalid_event, self.data_store)

    def test_ingest_update_customer_before_new(self):
        # Testing ingestion of an 'UPDATE' event for a customer before a 'NEW' event
        update_event = {
            "type": "CUSTOMER",
            "verb": "UPDATE",
            "key": "customer2",
            "event_time": "2020-01-01T00:00:00.000Z",
            "last_name": "Doe",
            "adr_city": "New York",
            "adr_state": "NY"
        }
        new_event = {
            "type": "CUSTOMER",
            "verb": "NEW",
            "key": "customer2",
            "event_time": "2020-01-01T00:00:00.000Z",
            "last_name": "Smith",
            "adr_city": "Los Angeles",
            "adr_state": "CA"
        }
        ingest(update_event, self.data_store)
        ingest(new_event, self.data_store)
        self.assertIn("customer2", self.data_store["customers"])
        self.assertIsInstance(self.data_store["customers"]["customer2"], Customer)
        self.assertEqual(self.data_store["customers"]["customer2"].last_name, "Doe")
        self.assertEqual(self.data_store["customers"]["customer2"].city, "New York")
        self.assertEqual(self.data_store["customers"]["customer2"].state, "NY")

    def test_ingest_update_order_before_new(self):
        # Testing ingestion of an 'UPDATE' event for an order before a 'NEW' event
        update_event = {
            "type": "ORDER",
            "verb": "UPDATE",
            "key": "order2",
            "event_time": "2020-01-01T00:00:00.000Z",
            "customer_id": "customer2",
            "total_amount": "100 USD"
        }
        new_event = {
            "type": "ORDER",
            "verb": "NEW",
            "key": "order2",
            "event_time": "2020-01-01T00:00:00.000Z",
            "customer_id": "customer2",
            "total_amount": "200 USD"
        }
        ingest(update_event, self.data_store)
        ingest(new_event, self.data_store)
        self.assertIn("order2", self.data_store["orders"])
        self.assertIsInstance(self.data_store["orders"]["order2"], Order)
        self.assertEqual(self.data_store["orders"]["order2"].total_amount, 100.0)

if __name__ == '__main__':
    unittest.main()
