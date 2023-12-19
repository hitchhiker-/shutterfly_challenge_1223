# Shutterfly Customer Lifetime Value Code-Challenge

### Design Decisions:
what the performance characteristic of the code is and how it could be improved in the future.

1. The ingest function in `event_ingestor.py` has several mechanisms for handling errors and missing data:
    * Invalid Event Types: The function raises a `ValueError` if an unrecognized event type is encountered.
    * Missing Keys: A KeyError is raised and caught if required fields (like event_time) are missing in the event data. This is converted into a `ValueError` with relevant details about the missing key.
    * Updates for Non-Existent Entries: The function treats updates for non-existent `CUSTOMER` and `ORDER` entries as new entries, creating them instead of discarding or flagging as errors. As it was stated in the challenge that entries can come in any order.
    * Error Propagation: The function actively raises `ValueError` in cases of invalid or missing data, enabling external handling of these exceptions.
2. Partial weeks are avoided when calculating LTV. `Earliest` and `latest` event times are adjusted during calculations to nearest Sunday and Saturday respectively.

### Performance
1. Selected python `dictionaries` as the in-memory data structure, lookup time for dictionary is `O(1)`.
2. The algorithm used for sorting the top LTV customers is `Timsort`, used in Python's default `sorted()` method, it's a hybrid algorithm derived from merge sort and insertion sort. It calculates the LTV for each customer in single pass, which is `O(n)` complexity where `n` is the number of customers.

### Future improvements
1. Modularity can be improved by placing each class in a separate module. As there may be more logic and more methods for each class.
2. As there may be more data to ingest and process, Pandas DataFrames offer more efficient ways to handle the data.

### Assumptions
1. A week is assumed strictly to be from `Sunday` to `Saturday`, partial weeks are counted as full weeks for calculating time delta between first and last event for each customer.
2. It is assumed that event_times of all events (`Customer`, `Image`, `SiteVisits`, `Orders`) contribute towards calculation of number of weeks between first and last event for each customer. 

## The additional SQL Challenge:

1. Can you solve the same challenge shared via GIT repo through SQL?
    * Yes, the challenge can be solved with SQL

2. Can you come up with Data models and corresponding SQL querying the data model?
    * Please see the following solution

#### Data Model:
##### Customer Table
    * CustomerID (Primary Key): Unique identifier for each customer.
    * LastName: Customer's last name.
    * AddressCity: City in the customer's address.
    * AddressState: State in the customer's address.
    * EventTime: The date and time when the customer record was created.

#### Site Visit Table
    * PageID (Primary Key): Unique identifier for each site visit.
    * CustomerID (Foreign Key): Links to the Customer table.
    * EventTime: The date and time of the site visit.
    * Tags: (Array of name/value properties).

#### Image Table
    * ImageID (Primary Key): Unique identifier for each image.
    * CustomerID (Foreign Key): Links to the Customer table.
    * EventTime: The date and time when the image was uploaded.
    * CameraMake: The make of the camera used for the image.
    * CameraModel: The model of the camera used for the image.

#### Order Table
    * OrderID (Primary Key): Unique identifier for each order.
    * CustomerID (Foreign Key): Links to the Customer table.
    * EventTime: The date and time when the order was placed.
    * TotalAmount: The total amount of the order.

#### Entity-Relationship 
#### How these tables relate to each other:
1. Customers
    * One customer can have multiple site visits, image uploads, and orders.
2. Site Visits, Images, Orders
    * Each of these entities references the Customer table through the CustomerID foreign key.
    * They are linked to the Customer table in a "many-to-one" relationship (many site visits, images, or orders can be associated with one customer).

### SQL Query:
```sql
SELECT 
    c.customer_id,
    -- Calculate the number of weeks between the first and last event
    CASE 
        WHEN MAX(e.event_time) IS NOT NULL AND MIN(e.event_time) IS NOT NULL THEN
            GREATEST(DATEDIFF(MAX(e.event_time), MIN(e.event_time)) / 7.0, 1)
        ELSE
            1
    END AS weeks_active,
    -- Calculate LTV (assuming site_visit events includes order events)
    (COALESCE(SUM(o.total_amount), 0) / GREATEST(COUNT(DISTINCT sv.visit_id), 1)) * 52 * 10 AS ltv
FROM 
    Customers c
LEFT JOIN 
    Orders o ON c.customer_id = o.customer_id
LEFT JOIN 
    SiteVisits sv ON c.customer_id = sv.customer_id
LEFT JOIN 
    (SELECT customer_id, event_time FROM SiteVisits
     UNION ALL
     SELECT customer_id, event_time FROM Orders
     UNION ALL
     SELECT customer_id, event_time FROM Images) e ON c.customer_id = e.customer_id
GROUP BY 
    c.customer_id
ORDER BY 
    ltv DESC;
```

