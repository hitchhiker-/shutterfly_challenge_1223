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

        # Assertions
        self.assertEqual(len(top_customers), min(5, len(self.data_store["customers"])))
        self.assertIn("cust1", {cust_id for cust_id, _ in top_customers})

        # Detailed LTV assertions
        for customer_id, ltv in top_customers:
            self.assertIsInstance(ltv, float)
            # Assuming a method to calculate expected LTV
            expected_ltv = calculate_expected_ltv(customer_id, self.data_store)
            self.assertAlmostEqual(ltv, expected_ltv, places=2)

        # Validation of customer ranking
        expected_ranking = calculate_expected_ranking(self.data_store)  # Assume this method sorts customers by their expected LTV
        actual_ranking = [cust_id for cust_id, _ in top_customers]
        self.assertEqual(actual_ranking, expected_ranking[:len(actual_ranking)])

        # Add more assertions and edge cases as necessary

def calculate_expected_ltv(customer_id, data_store):
    lifespan_years = 10  # Average customer lifespan (t), 10 years
    weeks_per_year = 52  # Number of weeks per year

    total_amount = sum(order.total_amount for order in data_store['orders'].values() if order.customer_id == customer_id)
    number_of_visits = len([visit for visit in data_store['site_visits'].values() if visit.customer_id == customer_id])

    if number_of_visits > 0 and total_amount > 0:
        # Adjust the dates to the nearest Sunday and Saturday
        earliest_visit_date = min(visit.event_time for visit in data_store['site_visits'].values() if visit.customer_id == customer_id)
        latest_visit_date = max(visit.event_time for visit in data_store['site_visits'].values() if visit.customer_id == customer_id)
        adjusted_earliest = get_sunday(earliest_visit_date)
        adjusted_latest = get_saturday(latest_visit_date)

        avg_expenditure_per_visit = total_amount / number_of_visits
        date_range = adjusted_latest - adjusted_earliest
        num_weeks = max(date_range.days // 7, 1)
        avg_visits_per_week = number_of_visits / num_weeks

        # Average customer value per week (a)
        a = avg_expenditure_per_visit * avg_visits_per_week

        # Calculate LTV
        ltv = weeks_per_year * a * lifespan_years
        return ltv
    else:
        return 0


def calculate_expected_ranking(data_store):
    lifespan_years = 10  # Average customer lifespan (t)
    weeks_per_year = 52  # Number of weeks per year

    def calculate_ltv(customer_id):
        total_amount = sum(order.total_amount for order in data_store['orders'].values() if order.customer_id == customer_id)
        number_of_visits = len([visit for visit in data_store['site_visits'].values() if visit.customer_id == customer_id])
        if number_of_visits > 0:
            return (total_amount / number_of_visits) * weeks_per_year * lifespan_years
        else:
            return 0

    customer_ltvs = {customer_id: calculate_ltv(customer_id) for customer_id in data_store['customers']}
    sorted_customers = sorted(customer_ltvs, key=customer_ltvs.get, reverse=True)

    return sorted_customers

if __name__ == '__main__':
    unittest.main()
