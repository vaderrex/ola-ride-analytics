CREATE TABLE ola_rides (
    booking_id        VARCHAR(50) PRIMARY KEY,
    booking_date      DATE,
    booking_status    VARCHAR(20),
    customer_id       VARCHAR(50),
    vehicle_type      VARCHAR(50),
    ride_distance     FLOAT,
    fare_amount       FLOAT,
    payment_method    VARCHAR(20),
    customer_rating   FLOAT,
    driver_rating     FLOAT,
    cancel_reason     VARCHAR(100)
);
