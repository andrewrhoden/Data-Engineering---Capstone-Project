import mysql.connector
import configparser
import pyinputplus as pyip
from prettytable import PrettyTable
import prettytable
config= configparser.ConfigParser()
config.read('config.ini')

host = config['DATABASE']['host']
user = config['DATABASE']['user']
password = config['DATABASE']['password']
database = config['DATABASE']['database']

# Connect to the creditcard_capstone database
db = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
    

)
# Create a cursor to execute SQL queries
cursor = db.cursor()
 



while True:
    print("Transaction Details Menu")
    print("1) Display transactions by zip code and date")
    print("2) Display number and total value of transactions by type")
    print("3) Display number and total value of transactions by branch state")
    print("4) Quit")
    
    choice = pyip.inputInt(prompt="Enter your choice (1-4): \n", min=1, max=4)
    
    if choice == 1:
        # Display transactions by zip code and date
        zip_code = pyip.inputInt(prompt="Enter zip code:\n ")
        year = pyip.inputInt(prompt="Enter year (YYYY):\n ")
        month = pyip.inputInt(prompt="Enter month (MM):\n ")
        
        # Execute SQL query to retrieve transactions by zip code and date
        query = f"SELECT cust_zip,transaction_id,transaction_type,transaction_value FROM cdw_sapp_credit_card cc JOIN cdw_sapp_customer c on ssn=cust_ssn WHERE MONTH(TIMEID)={month} AND YEAR(TIMEID)={year} AND CUST_ZIP={zip_code} ORDER BY DAY(TIMEID) DESC"
        cursor.execute(query)
        results = cursor.fetchall()
        table = PrettyTable(['Zip Code', 'Transaction ID', 'Transaction Type', 'Transaction Value'])

        
        # Display the results
        if results:
            for result in results:
                table.add_row(result)
            print(table)
        else:
            print("No results found.\n")
        
    elif choice == 2:
        # Display number and total value of transactions by type
        transaction_type = pyip.inputStr(prompt="Enter transaction type: \n")
        
        # Execute SQL query to retrieve number and total value of transactions by type
        query = f"SELECT COUNT(TRANSACTION_ID), SUM(TRANSACTION_VALUE) FROM cdw_sapp_credit_card WHERE TRANSACTION_TYPE='{transaction_type.upper()}'"
        cursor.execute(query)
        results = cursor.fetchone()

        # Display the results in a table format
        if results[0] > 0:
            table = prettytable.PrettyTable()
            table.field_names = ["Number of Transactions", "Total Value"]
            table.add_row([results[0], "${:,.2f}".format(results[1])])
            print(f"Results for {transaction_type} transactions:\n")
            print(table)
        else:
            print(f"No {transaction_type} transactions found.") 
                
    elif choice == 3:
        # Display number and total value of transactions by branch state
        branch_state = pyip.inputStr(prompt="Enter branch state: \n ")
        
        # Execute SQL query to retrieve number and total value of transactions by branch state
        query = f"SELECT COUNT(TRANSACTION_ID), SUM(TRANSACTION_VALUE) FROM cdw_sapp_credit_card c JOIN cdw_sapp_branch b ON c.BRANCH_CODE=b.BRANCH_CODE WHERE b.BRANCH_STATE='{branch_state.upper()}'"
        cursor.execute(query)
        results = cursor.fetchone()

        # Create a PrettyTable instance and add the column headers
        table = PrettyTable()
        table.field_names = ["Number of Transactions", "Total Value"]

        # Add the query results to the table
        if results[0] > 0:
            table.add_row([results[0], f"${results[1]:,.2f}"])
        else:
            print(f"No transactions found in {branch_state}.")

        # Print the table
        print(table)  
            
        
    elif choice == 4:
        # Quit the program
        print("Exiting program.")
        break
        
    else:
        print("Invalid choice. Please try again.")
        
# Close the database connection
db.close()