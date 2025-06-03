import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.exceptions import ConvergenceWarning
import warnings

def filter_warnings() -> None:
    warnings.filterwarnings("ignore", category=UserWarning, message="pandas only supports SQLAlchemy connectable")
    warnings.filterwarnings("ignore", category=ConvergenceWarning)

def handle_invalid_input() -> None:
    """
    Helper function to print error message
    """
    print("Invalid input detected.")

def display_menu() -> None:
    """
    Display menu options
    """
    print("\nApplication Options:")
    print("1. Relational Queries")
    print("2. Non-Relational Queries")
    print("3. Load/Reload Dataset (est. 5-10 min)")
    print("4. Exit")
    return

def display_relational_queries() -> None:
    """
    Display list of relational queries
    """
    queries = {
        1:"Get total number of flights",
        2:"Get total number of airports",
        3:"Get most common flight routes",
        4:"Get airports with most departures",
        5:"Get airports with longest average departure delays",
        6:"Get carriers with longest delays",
        7:"Get most popular cities by destination",
        8:"Get carriers with best on-time performance"
    }
    
    print("\nAvailable Relational Queries:")
    for key, value in queries.items():
        print(f"{key}. {value}")

def get_relational_query(selection: str) -> str:
    """
    Get SQL query depending on selection
    
    Returns:
        str: Containing SQL query
    """
    if selection == "1": # Get total number of flights
        query = """
        SELECT COUNT(*) AS total_flights
        FROM flights;
        """
    elif selection == "2": # Get total number of airports
        query = """
        SELECT COUNT(*) AS total_airports
        FROM airports;
        """
    else:
        try:
            num_results = int(input("Number of results to display: "))
        except:
            return ""
        if selection == "3": # Get most common flight routes
            query = f"""
            SELECT 
                a1.city AS origin_city, 
                a2.city AS destination_city, 
                COUNT(*) AS total_flights
            FROM 
                flights f
            JOIN 
                airports a1 ON f.origin_airport_id = a1.airport_id
            JOIN 
                airports a2 ON f.dest_airport_id = a2.airport_id
            GROUP BY 
                f.origin_airport_id, f.dest_airport_id
            ORDER BY 
                total_flights DESC
            LIMIT {num_results};
            """
        elif selection == "4": # Get airports with most departures
            query = f"""
            SELECT 
                a.city AS airport_city, 
                COUNT(*) AS total_departures
            FROM 
                flights f
            JOIN 
                airports a ON f.origin_airport_id = a.airport_id
            GROUP BY 
                f.origin_airport_id
            ORDER BY 
                total_departures DESC
            LIMIT {num_results};
            """
        elif selection == "5": # Get airports with longest average departure delays
            query = f"""
            SELECT 
                a.city AS airport_city, 
                AVG(f.dep_delay) AS avg_departure_delay
            FROM 
                flights f
            JOIN 
                airports a ON f.origin_airport_id = a.airport_id
            WHERE 
                f.dep_delay > 0  -- Only consider delayed flights
            GROUP BY 
                f.origin_airport_id
            ORDER BY 
                avg_departure_delay DESC
            LIMIT {num_results};
            """
        elif selection == "6": # Get carriers with longest delays
            query = f"""
            SELECT 
                f.carrier, 
                AVG(f.dep_delay) AS avg_departure_delay, 
                AVG(f.arr_delay) AS avg_arrival_delay
            FROM 
                flights f
            WHERE 
                f.dep_delay > 0 OR f.arr_delay > 0  -- Only consider delayed flights
            GROUP BY 
                f.carrier
            ORDER BY 
                avg_departure_delay DESC, avg_arrival_delay DESC
            LIMIT {num_results};"""
        elif selection == "7": # Get most popular cities by destination
            query = f"""
            SELECT 
                a.city AS destination_city, 
                COUNT(*) AS total_flights
            FROM 
                flights f
            JOIN 
                airports a ON f.dest_airport_id = a.airport_id
            GROUP BY 
                f.dest_airport_id
            ORDER BY 
                total_flights DESC
            LIMIT {num_results};"""
        elif selection == "8": # Get carriers with best on-time performance
            query = f"""
            SELECT 
                f.carrier, 
                SUM(CASE WHEN f.dep_delay <= 0 AND f.arr_delay <= 0 THEN 1 ELSE 0 END) AS on_time_flights,
                COUNT(*) AS total_flights,
                (SUM(CASE WHEN f.dep_delay <= 0 AND f.arr_delay <= 0 THEN 1 ELSE 0 END) / COUNT(*)) * 100 AS on_time_percentage
            FROM 
                flights f
            GROUP BY 
                f.carrier
            ORDER BY 
                on_time_percentage DESC
            LIMIT {num_results};"""
        else: # Invalid input
            query = ""
        
    return query

def display_nonrelational_queries() -> None:
    """
    Display list of nonrelational queries
    """
    queries = {
        1:"Get busiest travel day (Analysis)",
        2:"Get airport with highest total delays (Analysis)",
        3:"Get percentage of flights delayed by carrier (Analysis)",
        4:"Predict probability of flight delay (Machine Learning)",
        5:"Predict probability of flight delay flying American Airlines (Machine Learning)",
    }
    
    print("\nAvailable Non-Relational Queries:")
    for key, value in queries.items():
        print(f"{key}. {value}")
        
def execute_nonrelational_query(selection: str, connection):
    if selection == "1": # Get busiest travel day (Analysis)
        query = "SELECT day_of_month, COUNT(*) AS total_flights FROM flights GROUP BY day_of_month"
        flights_by_day = pd.read_sql(query, connection)
        
        busiest_day = flights_by_day.loc[flights_by_day['total_flights'].idxmax()]
        query_result = f"Busiest day: {busiest_day['day_of_month']} with {busiest_day['total_flights']} flights"
        
    elif selection == "2": # Get airport with highest total delays (Analysis)
        query = """
        SELECT a.city, SUM(f.dep_delay + f.arr_delay) AS total_delay
        FROM flights f
        JOIN airports a ON f.origin_airport_id = a.airport_id
        GROUP BY a.city;
        """
        delays = pd.read_sql(query, connection)

        most_delayed_airports = delays.sort_values(by='total_delay', ascending=False)
        query_result = most_delayed_airports.head(5)
        
    elif selection == "3": # Get percentage of flights delayed by carrier (Analysis)
        query = """
        SELECT carrier, 
            COUNT(*) AS total_flights,
            SUM(CASE WHEN dep_delay > 0 OR arr_delay > 0 THEN 1 ELSE 0 END) AS delayed_flights
        FROM flights
        GROUP BY carrier;
        """
        carrier_delays = pd.read_sql(query, connection)
        
        carrier_delays['delay_percentage'] = (carrier_delays['delayed_flights'] / carrier_delays['total_flights']) * 100
        query_result = carrier_delays
        
    elif selection == "4": # Predict probability of flight delay (Machine Learning)
        query = "SELECT carrier, origin_airport_id, dest_airport_id, dep_delay FROM flights"
        flights = pd.read_sql(query, connection)
        
        flights['delayed'] = flights['dep_delay'].apply(lambda x: 1 if x > 0 else 0)

        X = flights[['carrier', 'origin_airport_id', 'dest_airport_id']]
        X = pd.get_dummies(X, columns=['carrier'])
        y = flights['delayed']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        model = LogisticRegression()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        
        report = classification_report(y_test, y_pred, output_dict=True)

        accuracy = accuracy_score(y_test, y_pred)
        precision_0 = report["0"]["precision"]
        recall_0 = report["0"]["recall"]
        precision_1 = report["1"]["precision"]
        recall_1 = report["1"]["recall"]

        query_result = f"""
Logistic Regression Results:
----------------------------
Overall Accuracy: {accuracy * 100:.2f}%
Flights Not Delayed (Class 0):
- Precision: {precision_0 * 100:.2f}%
- Recall: {recall_0 * 100:.2f}%
Flights Delayed (Class 1):
- Precision: {precision_1 * 100:.2f}%
- Recall: {recall_1 * 100:.2f}%

Note: Precision measures how accurate predictions were, while Recall measures how well delays were identified.
"""
        
    elif selection == "5": # Predict probability of flight delay flying American Airlines (Machine Learning)
        query = """
        SELECT 
            day_of_week,
            carrier,
            dep_delay
        FROM flights
        WHERE dep_delay IS NOT NULL;
        """
        flights = pd.read_sql(query, connection)
        
        flights['on_time'] = flights['dep_delay'].apply(lambda x: 1 if x <= 0 else 0)
        flights = flights.drop(['dep_delay'], axis=1)
        flights = pd.get_dummies(flights, columns=['carrier'])

        X = flights.drop('on_time', axis=1)
        y = flights['on_time']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        model = LogisticRegression()
        model.fit(X_train, y_train)

        try:
            day_input = int(input("Enter a number (1-7) for day of week (e.g. 3 for Wednesday): "))
        except:
            print("Invalid input for day. Automatically setting default day as Wednesday.")
            day_input = 3
            
        sample_data = pd.DataFrame({
            'day_of_week': [day_input],
            'carrier_AA': [1],  # American Airlines
        })

        sample_data = sample_data.reindex(columns=X.columns, fill_value=0)

        likelihood = model.predict_proba(sample_data)[0][1] * 100
        number_to_day = {1:"Monday", 2:"Tuesday", 3:"Wednesday", 4:"Thursday", 5:"Friday", 6:"Saturday", 7:"Sunday"}
        
        return f"Likelihood of being on-time: {likelihood:.2f}% on a {number_to_day.get(day_input)} with American Airlines."
        
    else:
        query_result = None
    
    return query_result

def print_query_results(query_results, headers) -> None:
    print("\nQuery Result:")
    header_line = " | ".join(headers)
    print(header_line)
    print(f"{'-' * len(header_line)}")
    for record in query_results:
        print(" | ".join(map(str, record)))
    return