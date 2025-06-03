from helper import *
from connection import MyConnection

def main():
    filter_warnings()
    
    connection = MyConnection(
        host='localhost',
        user='mp',
        password='eecs118',
        database='flight_data'
    )
    connection.create_connection()

    print("Welcome to the Query Application!")

    while True:
        display_menu()
        choice = input("\nSelect an option: ")
        
        ##############    1. Show relational queries    ##############
        if choice == '1':
            display_relational_queries()

            query_choice = input("\nChoose a query to execute: ")
            query_to_execute = get_relational_query(selection=query_choice)
            if not query_to_execute:
                handle_invalid_input()
                continue
            
            headers, result = connection.execute_query(query=query_to_execute)
            print_query_results(query_results=result, headers=headers)
        
        ##############    2. Show non-relational queries    ##############
        elif choice == '2':
            display_nonrelational_queries()

            query_choice = input("\nChoose a query to execute: ")
            results = execute_nonrelational_query(selection=query_choice, connection=connection.connection)
            if results is None:
                handle_invalid_input()
                continue
            
            print(results)
        
        ##############    3. Load/Reload data    ##############
        elif choice == '3':
            connection.load_data()

        ##############    4. Exit program    ##############
        elif choice == '4':
            print("\nExiting program.")
            break

        else:
            handle_invalid_input()

    connection.connection.close()

if __name__ == "__main__":
    main()