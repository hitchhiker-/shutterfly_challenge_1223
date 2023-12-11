import unittest
from ltv_calculator import TopXSimpleLTVCustomers
from events import Customer, SiteVisit, Image, Order

class TestLTVCalculator(unittest.TestCase):

    def test_top_x_simple_ltv_customers(self):
        data_store = {
            "customers": {
                "customer1": Customer("customer1", "2017-01-01T00:00:00.000Z"),  # Mocked Customer instances
                "customer2": Customer("customer2", "2017-01-01T00:00:00.000Z")
            },
            "site_visits": {
                "visit1": SiteVisit("visit1", "2017-01-01T00:00:00.000Z", "customer1"),  # Mocked SiteVisit instances
                "visit2": SiteVisit("visit2", "2017-01-01T00:00:00.000Z", "customer2")
            },
            "images": {
                "image1": Image("image1", "2017-01-01T00:00:00.000Z", "customer1"),  # Mocked Image instances
                "image2": Image("image2", "2017-01-01T00:00:00.000Z", "customer2")
            },
            "orders": {
                "order1": Order("order1", "2017-01-01T00:00:00.000Z", "customer1", "100.00 USD"),  # Mocked Order instances
                "order2": Order("order2", "2017-01-01T00:00:00.000Z", "customer2", "200.00 USD")
            }
        }
        result = TopXSimpleLTVCustomers(2, data_store)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].customer_id, "customer2")
        self.assertEqual(result[1].customer_id, "customer1")

if __name__ == '__main__':
    unittest.main()
