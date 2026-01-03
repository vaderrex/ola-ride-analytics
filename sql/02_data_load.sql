#checks
SELECT COUNT(*) FROM dbo.OLA_Rides_Riview;

SELECT TOP 10 * FROM dbo.OLA_Rides_Riview;

select * from dbo.OLA_Rides_Riview;

-- Retrieve all successful bookings
SELECT *
FROM dbo.OLA_Rides_Riview
WHERE Booking_Status = 'Success';

-- Find the average ride distance for each vehicle type
SELECT 
    Vehicle_Type,
    ROUND (AVG(Ride_Distance), 2) AS avg_ride_distance
FROM dbo.OLA_Rides_Riview
WHERE Ride_Distance IS NOT NULL
GROUP BY Vehicle_Type;

----Get the total number of cancelled rides by customers
Select 
COUNT(*) AS total_customer_cancellations
FROM dbo.OLA_Rides_Riview 
WHERE Booking_Status = 'Canceled by Customer';

--List the top 5 customers who booked the highest number of rides
SELECT TOP 5
    Customer_ID,
    COUNT(Booking_ID) AS total_rides
FROM dbo.OLA_Rides_Riview 
GROUP BY Customer_ID
ORDER BY Total_Rides DESC;

--Get the number of rides cancelled by drivers due to
SELECT 
    Canceled_Rides_by_Driver,
    COUNT(*) AS total_cancellations
FROM dbo.OLA_Rides_Riview 
WHERE Canceled_Rides_by_Driver = 'Personal & Car related issue'
GROUP BY Canceled_Rides_by_Driver;

--Find the maximum and minimum driver ratings for Prime Sedan bookings
SELECT 
    MAX(Driver_Rating) AS max_driver_rating,
    MIN(Driver_Rating) AS min_driver_rating
FROM dbo.OLA_Rides_Riview
WHERE Vehicle_Type = 'Prime Sedan'
  AND Driver_Rating IS NOT NULL;

  --
  select Booking_Status, Driver_Ratings, Customer_Rating
  FROM dbo.OLA_Rides_Riview
  WHERE Booking_Status = 'Success';

  --
  SELECT
    COUNT(*) AS total_success_rows,
    COUNT(Customer_Rating) AS customer_rating_present,
    COUNT(Driver_Ratings) AS driver_rating_present
FROM dbo.OLA_Rides_Riview
WHERE Booking_Status = 'Success';

--
SELECT DISTINCT Customer_Rating
FROM dbo.OLA_Rides_Riview
WHERE Customer_Rating IS NOT NULL;

----
--Retrieve all rides where payment was made using UPI
SELECT *
FROM dbo.OLA_Rides_Riview
WHERE payment_method = 'UPI';
----
--Find the average customer rating per vehicle type
SELECT 
    vehicle_type,
    ROUND(AVG(customer_rating), 1) AS avg_customer_rating
FROM dbo.OLA_Rides_Riview
WHERE customer_rating IS NOT NULL
GROUP BY vehicle_type;
--
--Calculate the total booking value of successfully completed rides
SELECT 
    SUM(booking_value) AS total_successful_booking_value
FROM dbo.OLA_Rides_Riview
WHERE Booking_status = 'Success';
--
-- List all non-successful rides along with the reason
SELECT 
    booking_id,
    customer_id,
  Booking_status
FROM dbo.OLA_Rides_Riview
WHERE Booking_status IS NULL
   OR Booking_status <> 'Success';
--
--Performance Tips for SSMS--Create indexes for faster execution:
CREATE INDEX idx_Booking_status ON ola_rides (Booking_status);
CREATE INDEX idx_vehicle_type ON ola_rides (vehicle_type);
CREATE INDEX idx_payment_method ON ola_rides (payment_method);
CREATE INDEX idx_customer_id ON dbo.OLA_Rides_Riview (customer_id);