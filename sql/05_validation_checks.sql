-- Check for null booking IDs
SELECT COUNT(*) FROM dbo.OLA_Rides_Riview WHERE booking_id IS NULL;

-- Ratings should exist only for successful rides
SELECT COUNT(*)
FROM dbo.OLA_Rides_Riview
WHERE booking_status <> 'Success'
AND (customer_rating IS NOT NULL OR driver_rating IS NOT NULL);

-- Revenue should not exist for cancelled rides
SELECT COUNT(*)
FROM dbo.OLA_Rides_Riview
WHERE booking_status <> 'Success'
AND Booking_Value > 0;
`