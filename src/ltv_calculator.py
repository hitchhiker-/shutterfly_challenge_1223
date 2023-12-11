from datetime import datetime

def TopXSimpleLTVCustomers(x, D):
    lifespan_years = 10  # Average customer lifespan (t)
    weeks_per_year = 52  # Number of weeks per year

    customer_expenditures = {}
    customer_site_visits = {}
    customer_visit_dates = {}

    for order in D['orders'].values():
        customer_expenditures[order.customer_id] = customer_expenditures.get(order.customer_id, 0) + order.total_amount

    for visit in D['site_visits'].values():
        customer_id = visit.customer_id
        customer_site_visits[customer_id] = customer_site_visits.get(customer_id, 0) + 1

        visit_date = visit.event_time
        if customer_id in customer_visit_dates:
            customer_visit_dates[customer_id]['earliest'] = min(customer_visit_dates[customer_id]['earliest'], visit_date)
            customer_visit_dates[customer_id]['latest'] = max(customer_visit_dates[customer_id]['latest'], visit_date)
        else:
            customer_visit_dates[customer_id] = {'earliest': visit_date, 'latest': visit_date}


    customer_ltv = {}
    for customer_id, dates in customer_visit_dates.items():
        total_expenditure = customer_expenditures.get(customer_id, 0)
        total_visits = customer_site_visits.get(customer_id, 0)

        if total_visits == 0 or total_expenditure == 0:
            continue

        avg_expenditure_per_visit = total_expenditure / total_visits
        date_range = dates['latest'] - dates['earliest']
        num_weeks = max(date_range.days / 7, 1)  # Ensure at least 1 week
        avg_visits_per_week = total_visits / num_weeks

        # Average customer value per week (a)
        a = avg_expenditure_per_visit * avg_visits_per_week

        # Calculate LTV
        ltv = weeks_per_year * a * lifespan_years
        customer_ltv[customer_id] = ltv

    # Sort customers by LTV and return the top x
    top_customers = sorted(customer_ltv.items(), key=lambda item: item[1], reverse=True)[:x]
    return [(customer_id, ltv) for customer_id, ltv in top_customers]
