from datetime import datetime

class Customer:
    def __init__(self, customer_id, event_time, last_name, city, state):
        self.customer_id = customer_id
        self.event_time = self.parse_event_time(event_time)
        self.last_name = last_name
        self.city = city
        self.state = state

    @staticmethod
    def parse_event_time(event_time_str):
        return datetime.fromisoformat(event_time_str)

    def update_details(self, last_name=None, city=None, state=None):
        if last_name is not None:
            self.last_name = last_name
        if city is not None:
            self.city = city
        if state is not None:
            self.state = state

class SiteVisit:
    def __init__(self, page_id, event_time, customer_id, tags):
        self.page_id = page_id
        self.event_time = Customer.parse_event_time(event_time)  # Reuse the method from Customer
        self.customer_id = customer_id
        self.tags = tags if isinstance(tags, list) else []  # Ensure tags is a list


class Image:
    def __init__(self, image_id, event_time, customer_id, camera_make, camera_model):
        self.image_id = image_id
        self.event_time = Customer.parse_event_time(event_time)  # Reuse the method from Customer
        self.customer_id = customer_id
        self.camera_make = camera_make
        self.camera_model = camera_model

class Order:
    def __init__(self, order_id, event_time, customer_id, total_amount):
        self.order_id = order_id
        self.event_time = Customer.parse_event_time(event_time)  # Reuse the method from Customer
        self.customer_id = customer_id
        self.total_amount = self.parse_total_amount(total_amount)

    @staticmethod
    def parse_total_amount(amount_str):
        # Extracting numeric value from the string (assumes format "xx.xx USD")
        amount = amount_str.split()[0]
        return float(amount) if amount.replace('.', '', 1).isdigit() else 0

    def update_order(self, total_amount=None):
        if total_amount is not None:
            self.total_amount = self.parse_total_amount(total_amount)

