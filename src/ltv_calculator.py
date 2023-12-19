from datetime import timedelta
import math

def TopXSimpleLTVCustomers(x, D):
    lifespan_years = 10  # Average customer lifespan (t), 10 years
    weeks_per_year = 52  # Number of weeks per year

    customer_expenditures = {} # Total customer expenditure (a)
    customer_site_visits = {} # Total customer visits (v)
    customer_visit_dates = {} # Earliest and latest visit dates

    # Process customers
    for customer_id, customer in D['customers'].items():
        customer_visit_dates[customer_id] = {'earliest': customer.event_time, 'latest': customer.event_time} # Set the earliest and latest visit dates to the customer creation date
    
    # Process site visits
    for visit in D['site_visits'].values(): # Iterate through the site visits
        update_customer_visit_dates(visit.customer_id, visit.event_time, customer_visit_dates) # Update the earliest and latest visit dates for the customer
        customer_site_visits[visit.customer_id] = customer_site_visits.get(visit.customer_id, 0) + 1 # Increment the customer site visits by 1

    # Process image uploads
    for image in D['images'].values():
        update_customer_visit_dates(image.customer_id, image.event_time, customer_visit_dates) # Update the earliest and latest visit dates for the customer

    # Process orders
    for order in D['orders'].values(): # Iterate through the orders
        update_customer_visit_dates(order.customer_id, order.event_time, customer_visit_dates) # Update the earliest and latest visit dates for the customer
        customer_expenditures[order.customer_id] = customer_expenditures.get(order.customer_id, 0) + order.total_amount # Add the order total amount to the customer expenditure
            
    customer_ltv = {} # Customer LTV (c)
    for customer_id, dates in customer_visit_dates.items(): # Iterate through the customers
        total_expenditure = customer_expenditures.get(customer_id, 0) # Get the total expenditure
        total_visits = customer_site_visits.get(customer_id, 0) # Get the total visits

        if total_visits == 0 or total_expenditure == 0: # Skip customers with no visits or no expenditure
            continue 
        
        # Adjust the dates to the nearest Sunday and Saturday as week boundaries (to avoid partial weeks) 
        adjusted_earliest = get_sunday(dates['earliest'])
        adjusted_latest = get_saturday(dates['latest'])
                
        avg_expenditure_per_visit = total_expenditure / total_visits # average customer expenditure per visit (a)
        date_range = adjusted_latest - adjusted_earliest # timedelta
        num_weeks = max(math.ceil(date_range.days / 7), 1)  # Number of weeks between the earliest and latest visits (t) (at least 1), considering a week as sunday to saturday
        avg_visits_per_week = total_visits / num_weeks # average customer visits per week (v)

        # Average customer value per week (a)
        a = avg_expenditure_per_visit * avg_visits_per_week 

        # Calculate LTV
        ltv = weeks_per_year * a * lifespan_years 
        customer_ltv[customer_id] = ltv # Add the customer LTV to the dictionary
        
    # Sort customers by LTV and return the top x
    top_customers = sorted(customer_ltv.items(), key=lambda item: item[1], reverse=True)[:x] # Sort by LTV and get the top x
    return [(customer_id, ltv) for customer_id, ltv in top_customers] 


# Helper functions
# Update the earliest and latest visit dates for a customer if the current event time is earlier or later than the existing dates respectively
def update_customer_visit_dates(customer_id, event_time, customer_visit_dates):
    if customer_id in customer_visit_dates:
        customer_visit_dates[customer_id]['earliest'] = min(customer_visit_dates[customer_id]['earliest'], event_time)
        customer_visit_dates[customer_id]['latest'] = max(customer_visit_dates[customer_id]['latest'], event_time)

# Get the week boundaries for a given date (Sunday and Saturday)
def get_sunday(date):
    # Get the previous Sunday (or the same day if it's already a Sunday)
    return date - timedelta(days=date.weekday() + 1)

def get_saturday(date):
    # Get the next Saturday (or the same day if it's already a Saturday)
    days_until_saturday = (5 - date.weekday()) % 7
    if days_until_saturday == 0:
        # If it's already Saturday, return the same day
        return date
    else:
        # Otherwise, add the number of days until the next Saturday
        return date + timedelta(days=days_until_saturday)
