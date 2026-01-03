--Total Rides
SELECT COUNT(DISTINCT booking_id) AS total_rides
FROM dbo.OLA_Rides_Riview;

--Successful Rides
SELECT COUNT(*) AS successful_rides
FROM dbo.OLA_Rides_Riview
WHERE booking_status = 'Success';

--Cancellation Rate
SELECT
    CAST(SUM(CASE WHEN booking_status <> 'Success' THEN 1 ELSE 0 END) * 100.0
    / COUNT(*) AS DECIMAL(5,2)) AS cancellation_rate
FROM dbo.OLA_Rides_Riview;

--Total Revenue
SELECT SUM(fare_amount) AS total_revenue
FROM dbo.OLA_Rides_Riview
WHERE booking_status = 'Success';