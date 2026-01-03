--Ride Volume Over Time
SELECT
    FORMAT(booking_date, 'yyyy-MM') AS month,
    COUNT(*) AS total_rides
FROM dbo.dbo.OLA_Rides_Riview_Riview
GROUP BY FORMAT(booking_date, 'yyyy-MM')
ORDER BY month;

--Top 5 Vehicle Types by Distance
SELECT TOP 5
    vehicle_type,
    SUM(ride_distance) AS total_distance
FROM dbo.OLA_Rides_Riview
GROUP BY vehicle_type
ORDER BY total_distance DESC;

--Revenue by Payment Method
SELECT
    payment_method,
    SUM(fare_amount) AS revenue
FROM dbo.OLA_Rides_Riview
WHERE booking_status = 'Success'
GROUP BY payment_method;

--Top 5 Customers by Booking Value
SELECT TOP 5
    customer_id,
    SUM(fare_amount) AS total_spent
FROM dbo.OLA_Rides_Riview
WHERE booking_status = 'Success'
GROUP BY customer_id
ORDER BY total_spent DESC;