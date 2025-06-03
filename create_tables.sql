-- Create the airports table
CREATE TABLE airports (
    airport_id INT PRIMARY KEY,      -- Unique identifier for the airport
    city VARCHAR(255),               -- City where the airport is located
    state_abbreviation VARCHAR(255), -- State abbreviation
    airport VARCHAR(255)             -- Name of the airport
);

-- Create the flights table
CREATE TABLE flights (
    day_of_month INT,                -- Day of the month
    day_of_week INT,                 -- Day of the week (1 = Monday, 7 = Sunday)
    carrier CHAR(2),                 -- Airline carrier code
    origin_airport_id INT,           -- Origin airport ID (foreign key)
    dest_airport_id INT,             -- Destination airport ID (foreign key)
    dep_delay INT,                   -- Departure delay in minutes
    arr_delay INT,                   -- Arrival delay in minutes
    FOREIGN KEY (origin_airport_id) REFERENCES airports(airport_id),
    FOREIGN KEY (dest_airport_id) REFERENCES airports(airport_id)
);