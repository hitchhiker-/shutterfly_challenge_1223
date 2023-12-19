# Shutterfly Customer Lifetime Value Code-Challenge

### Design Decisions:
1. The ingest function in `event_ingestor.py` has several mechanisms for handling errors and missing data:
    * Invalid Event Types: When the function encounters an invalid event type or invalid data format (such as an incorrect event_time format), it logs an error message to `output/app.log`.
    * Missing Keys: Similarly, for missing keys, an error message is logged.
    * Storing Invalid Events: In cases of errors (whether due to invalid event types, data formats, or missing keys), the problematic event data is stored in `output/invalid_data.json`. This allows for post-processing or manual review of these events.
    * Enhanced Resilience: This approach enhances the resilience of the data ingestion process by ensuring that issues with specific events do not halt the entire ingestion pipeline. It allows for continued processing while keeping a record of any issues that need attention.
    * Updates for Non-Existent Entries: When a new `CUSTOMER` or `ORDER` event is recieved, the `ingest` method checks if there is an existing key already present in the `data_store` (in-memory data structure, dictionary). If not, a new instance is created and added to `data_store`. If a CUSTOMER or ORDER with the same key already exists, the new event is ignored and does not overwrite the existing customer. The function treats updates for non-existent `CUSTOMER` and `ORDER` entries as new entries, creating them instead of discarding or flagging as errors. (It is assumed that updates will have all the entries not just the changed attributes, can be improved in the future if so)
2. Partial weeks are avoided when calculating LTV. `Earliest` and `latest` event times are adjusted during calculations to nearest Sunday and Saturday respectively.

### Performance
1. Selected python `dictionaries` as the in-memory data structure, lookup time for dictionary is `O(1)`.
2. The algorithm used for sorting the top LTV customers is `Timsort`, used in Python's default `sorted()` method, it's a hybrid algorithm derived from merge sort and insertion sort. It calculates the LTV for each customer in single pass, which is `O(n)` complexity where `n` is the number of customers.

### Future improvements
1. Modularity can be improved by placing each class in a separate module. As there may be more logic and more methods for each class.
2. As there may be more data to ingest and process, Pandas DataFrames offer more efficient ways to handle the data.
3. Improve logging for better debugging and monitoring.
4. Current handling of out of order entries especially for `NEW` and `UPDATE` is simple, more robust approach can be implemented in the future. Example, if `UPDATE` entry has missing or partial data.
5. Sorting strategy can be revisited based on data charecteristics.

### Assumptions
1. A week is assumed strictly to be from `Sunday` to `Saturday`, partial weeks are counted as full weeks for calculating time delta between first and last event for each customer.
2. It is assumed that event_times of all events (`Customer`, `Image`, `SiteVisits`, `Orders`) contribute towards calculation of number of weeks between first and last event for each customer.
3. 52 weeks in a year and average customer lifespan at Shtterfly is 10 years.

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
    -- Calculate LTV
    (COALESCE(SUM(o.total_amount), 0) / GREATEST(CEIL(DATEDIFF(MAX(e.event_time), MIN(e.event_time)) / 7.0), 1)) * 52 * 10 AS ltv
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
