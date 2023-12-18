import unittest
from src.ltv_calculator import TopXSimpleLTVCustomers
from src.events import Customer, SiteVisit, Image, Order

class TestLTVCalculator(unittest.TestCase):

    # Sample data store with a mix of different customers and activities
    def setUp(self):
        self.data_store = {
            "customers": {
                "customer1": Customer("customer1", "2017-01-01T00:00:00.000Z", "Doe", "New York", "NY"),
                "customer2": Customer("customer2", "2017-01-01T00:00:00.000Z", "Smith", "Los Angeles", "CA"),
                "customer3": Customer("customer3", "2017-01-02T00:00:00.000Z", "Johnson", "Chicago", "IL")
            },
            "site_visits": {
                "visit1": SiteVisit("visit1", "2017-01-01T00:00:00.000Z", "customer1", []),
                "visit2": SiteVisit("visit2", "2017-01-02T00:00:00.000Z", "customer2", []),
                "visit3": SiteVisit("visit3", "2017-01-03T00:00:00.000Z", "customer3", [])
            },
            "images": {
                "image1": Image("image1", "2017-01-01T00:00:00.000Z", "customer1", "Canon", "EOS 80D"),
                "image2": Image("image2", "2017-01-02T00:00:00.000Z", "customer2", "Nikon", "D3500"),
                "image3": Image("image3", "2017-01-03T00:00:00.000Z", "customer3", "Sony", "Alpha A7III")
            },
            "orders": {
                "order1": Order("order1", "2017-01-01T00:00:00.000Z", "customer1", "100.00 USD"),
                "order2": Order("order2", "2017-01-02T00:00:00.000Z", "customer2", "200.00 USD"),
                "order3": Order("order3", "2017-01-03T00:00:00.000Z", "customer3", "300.00 USD")
            }
        }

    # Sample expected LTV values for the above data store
    def test_customers_with_varying_activities(self):
        result = TopXSimpleLTVCustomers(3, self.data_store)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0][0], "customer3")  # Customer3 with the highest LTV
        self.assertEqual(result[1][0], "customer2")  # Customer2 with the next highest LTV
        self.assertEqual(result[2][0], "customer1")  # Customer1 with the lowest LTV

    # Test for zero activity customers not be included in the result
    def test_customers_with_zero_activity(self):
        # Add a customer with zero activity
        self.data_store["customers"]["customer4"] = Customer("customer4", "2017-01-04T00:00:00.000Z", "Wilson", "Miami", "FL") # Customer4 with zero activity
        result = TopXSimpleLTVCustomers(3, self.data_store) # Calculate LTV for top 3 customers
        customer_ids = [customer_id for customer_id, _ in result]  # Extract customer IDs from the result
        self.assertNotIn("customer4", customer_ids)  # Customer4 should not be in the list

    def test_less_customers_than_requested(self):
        result = TopXSimpleLTVCustomers(5, self.data_store)
        self.assertEqual(len(result), 3)  # Only 3 customers exist

    

    # Additional tests for handling of invalid data, edge cases, etc. can be added here

if __name__ == '__main__':
    unittest.main()
