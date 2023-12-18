from src.events import Customer, SiteVisit, Image, Order

# Ingests the event and updates the data store
def ingest(event, data_store):
    try: # Validate the event
        event_type = event.get('type')
        key = event.get('key')
        
        if event_type == 'CUSTOMER':
            verb = event.get('verb')
            if verb == 'NEW' or (verb == 'UPDATE' and key not in data_store['customers']):
                # Create a new Customer instance
                data_store['customers'][key] = Customer(
                    customer_id=key,
                    event_time=event['event_time'],
                    last_name=event['last_name'],
                    city=event['adr_city'],
                    state=event['adr_state']
                )
            elif verb == 'UPDATE':
                # Update the existing Customer instance
                data_store['customers'][key].update_details(
                    last_name=event.get('last_name'),
                    city=event.get('adr_city'),
                    state=event.get('adr_state')
                )

        elif event_type == 'SITE_VISIT':
            # Create a new SiteVisit instance
            data_store['site_visits'][key] = SiteVisit(
                page_id=key,
                event_time=event['event_time'],
                customer_id=event['customer_id'],
                tags=event['tags']
            )

        elif event_type == 'IMAGE':
            # Create a new Image instance
            data_store['images'][key] = Image(
                image_id=key,
                event_time=event['event_time'],
                customer_id=event['customer_id'],
                camera_make=event['camera_make'],
                camera_model=event['camera_model']
            )

        elif event_type == 'ORDER':
            verb = event.get('verb')
            if verb == 'NEW' or (verb == 'UPDATE' and key not in data_store['orders']):
                # Create a new Order instance
                data_store['orders'][key] = Order(
                    order_id=key,
                    event_time=event['event_time'],
                    customer_id=event['customer_id'],
                    total_amount=event['total_amount']
                )
            elif verb == 'UPDATE':
                # Update the existing Order instance
                data_store['orders'][key].update_order(
                    total_amount=event.get('total_amount')
                )
        
        else: # Invalid event type
            raise ValueError(f"Invalid event type: {event_type}")
    
    # Handle missing keys and invalid values
    except KeyError as e:
        raise ValueError(f"Invalid key: {e}") from e
    except ValueError as e:
        raise ValueError(f"Invalid value: {e}") from e

