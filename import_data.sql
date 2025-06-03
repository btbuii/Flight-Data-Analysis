-- Import data into the airports table
LOAD DATA LOCAL INFILE 'airports.csv'
INTO TABLE airports
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(airport_id, city, state, name);

-- Import data into the flights table
LOAD DATA LOCAL INFILE 'flights.csv'
INTO TABLE flights
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(day_of_month, day_of_week, carrier, origin_airport_id, dest_airport_id, dep_delay, arr_delay);

-- Import data into the raw_flight_data table
LOAD DATA LOCAL INFILE 'raw-flight-data.csv'
INTO TABLE raw_flight_data
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(day_of_month, day_of_week, carrier, origin_airport_id, dest_airport_id, dep_delay, arr_delay);