def top_x_simple_ltv_customers(x, data):
    lifespan_years = 10  # Average customer lifespan
    weeks_per_year = 52

    # Calculate total expenditures and total site visits for each customer
    customer_expenditures = {}
    customer_site_visits = {}
    for order in data['orders'].values():
        customer_expenditures[order.customer_id] = customer_expenditures.get(order.customer_id, 0) + order.total_amount
    
    for visit in data['site_visits'].values():
        customer_site_visits[visit.customer_id] = customer_site_visits.get(visit.customer_id, 0) + 1

    # Calculate LTV for each customer
    customer_ltv = {}
    for customer_id in data['customers']:
        total_expenditure = customer_expenditures.get(customer_id, 0)
        total_visits = customer_site_visits.get(customer_id, 0)

        # Calculate average expenditure per visit (avoid division by zero)
        avg_expenditure_per_visit = total_expenditure / total_visits if total_visits > 0 else 0

        # Calculate the number of weeks spanned by the customer's data
        # This requires event_time data from customer's first and last site visit
        # Assuming you have a way to determine the time span in weeks (num_weeks)

        num_weeks = ... # Calculate this based on the customer's site visit data

        # Calculate the average number of visits per week
        avg_visits_per_week = total_visits / num_weeks if num_weeks > 0 else 0

        # Calculate average customer value per week (a)
        a = avg_expenditure_per_visit * avg_visits_per_week

        # Calculate LTV
        ltv = weeks_per_year * a * lifespan_years
        customer_ltv[customer_id] = ltv

    # Sort customers by LTV and return the top x
    top_customers = sorted(customer_ltv.items(), key=lambda item: item[1], reverse=True)
    return top_customers[:x]
