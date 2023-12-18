import unittest
from src.ltv_calculator import TopXSimpleLTVCustomers
from src.events import Customer, SiteVisit, Image, Order

class TestLTVCalculator(unittest.TestCase):

    def test_top_x_simple_ltv_customers(self):
        data_store = {
            "customers": {
                "customer1": Customer("customer1", "2017-01-01T00:00:00.000Z", "Doe", "New York", "NY"),
                "customer2": Customer("customer2", "2017-01-01T00:00:00.000Z", "Smith", "Los Angeles", "CA")
            },
            "site_visits": {
                "visit1": SiteVisit("visit1", "2017-01-01T00:00:00.000Z", "customer1", []),
                "visit2": SiteVisit("visit2", "2017-01-01T00:00:00.000Z", "customer2", [])
            },
            "images": {
                "image1": Image("image1", "2017-01-01T00:00:00.000Z", "customer1", "Canon", "EOS 80D"),
                "image2": Image("image2", "2017-01-01T00:00:00.000Z", "customer2", "Nikon", "D3500")
            },
            "orders": {
                "order1": Order("order1", "2017-01-01T00:00:00.000Z", "customer1", "100.00 USD"),
                "order2": Order("order2", "2017-01-01T00:00:00.000Z", "customer2", "200.00 USD")
            }
        }

        result = TopXSimpleLTVCustomers(2, data_store)
        self.assertEqual(len(result), 2)
        
        # Check the order of customers
        self.assertEqual(result[0][0], "customer2")  
        self.assertEqual(result[1][0], "customer1")

if __name__ == '__main__':
    unittest.main()
