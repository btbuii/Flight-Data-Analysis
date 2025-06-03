import pymysql, csv

class MyConnection():
    def __init__(self, host:str, user:str, password:str, database:str) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.database = database    
        
    def create_connection(self) -> None:
        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            db=self.database
        )
        self.cursor = self.connection.cursor()
    
    def load_data(self) -> None:
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        table_names = ["flights", "airports"]
        for table in table_names:
            self.cursor.execute(f"TRUNCATE TABLE {table}") # Truncate before loading to avoid duplicate entry
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
            
        datasets = [
            {
                "file_path": "airports.dat",
                "table_name": "airports",
                "columns": ["airport_id", "city", "state_abbreviation", "airport"]
            },
            {
                "file_path": "flights.dat",
                "table_name": "flights",
                "columns": ["day_of_month", "day_of_week", "carrier", "origin_airport_id", "dest_airport_id", "dep_delay", "arr_delay"]
            },
        ]

        for dataset in datasets:
            with open(dataset["file_path"], "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    values = ", ".join(["%s"] * len(dataset["columns"]))
                    query = f"""
                    INSERT INTO {dataset['table_name']} ({', '.join(dataset['columns'])})
                    VALUES ({values})
                    """
                    self.cursor.execute(query, row)
        self.connection.commit()
        
    def execute_query(self, query) -> tuple:
        """
        Execute a query and return the results.
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                column_headers = [desc[0] for desc in cursor.description]
                return column_headers, result
        except Exception as e:
            print("Error executing query:", e)
            return None