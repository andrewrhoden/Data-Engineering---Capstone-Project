import mysql.connector
import configparser
import pyinputplus as pyip
import prettytable
from prettytable import PrettyTable
import re
 
from datetime import datetime

config= configparser.ConfigParser()
config.read('config.ini')

host = config['DATABASE']['host']
user = config['DATABASE']['user']
password = config['DATABASE']['password']
database = config['DATABASE']['database']
 
 # Connect to the database
db = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

# Create a cursor object to execute SQL queries
cursor = db.cursor()



while True:
    print("CUSTOMER DETAILS MENU \n")
    print("1. Check existing account details")
    print("2. Modify existing account details")
    print("3. Generate monthly bill")
    print("4. Display transactions between two dates")
    print("5. Exit")
    
    
    choice = pyip.inputInt("Enter your choice (1-5):\n ", min=1, max=5)

    if choice == 1:
        # Check existing account details
        credit_card_no = pyip.inputStr("Enter credit card number: \n")
        if not credit_card_no:
            print("Invalid input. Credit card number cannot be empty.")
            continue
        query = f"SELECT * FROM CDW_SAPP_CUSTOMER WHERE CREDIT_CARD_NO = '{credit_card_no}'"
        cursor.execute(query)
        result = cursor.fetchall()
        if result:
            table = prettytable.PrettyTable()
            table.field_names = [i[0] for i in cursor.description]
            for row in result:
                table.add_row(row)
            print(table)
        else:
            print("Customer not found.")

    elif choice == 2:
        # Modify existing account details
        credit_card_no = pyip.inputStr("Enter customer credit card number: \n")
        if len(credit_card_no) != 16:
            print("Invalid input. Credit card number should be 16 digits long.")
            continue
        if not credit_card_no:
            print("Invalid input. Credit card number cannot be empty.")
            continue
        query = f"SELECT * FROM CDW_SAPP_CUSTOMER WHERE CREDIT_CARD_NO = '{credit_card_no}'"
        cursor.execute(query)
        result = cursor.fetchall()
        if not result:
            print("Customer not found.")
            continue
        print("Which customer account detail would you like to update?")
        print("1. Name")
        print("2. Full Street Address")
        print("3. City")
        print("4. State")
        print("5. Zipcode")
        print("6. Phone")
        print("7. Exit to main menu")
        choice = pyip.inputInt("Enter your choice (1-7): ", min=1, max=7)
        if choice == 1:
            first_name = pyip.inputStr("Enter new first name: ")
            if not first_name:
                print("Invalid input. First name cannot be empty.")
                continue
            middle_name = pyip.inputStr("Enter new middle name: ")
            last_name = pyip.inputStr("Enter new last name: ")
            query = f"UPDATE CDW_SAPP_CUSTOMER SET FIRST_NAME='{first_name}', MIDDLE_NAME='{middle_name}', LAST_NAME='{last_name}' WHERE CREDIT_CARD_NO = '{credit_card_no}'"
            cursor.execute(query)
            db.commit()
            print(f"Customer {credit_card_no} name updated successfully.")
        elif choice == 2:
            apt_no = pyip.inputStr("Enter apartment number: ")
            street_name = pyip.inputStr("Enter street name: ")
            full_address = f"{apt_no}, {street_name}"
            query = f"UPDATE CDW_SAPP_CUSTOMER SET FULL_STREET_ADDRESS = '{full_address}' WHERE CREDIT_CARD_NO = '{credit_card_no}'"
            cursor.execute(query)
            db.commit()
            print("full_Street_Address updated successfully.")
        elif choice == 3:
            new_city = pyip.inputStr("Enter new city: \n")
            if not new_city:
                print("Invalid input. City cannot be empty.\n")
                continue
            query = f"UPDATE CDW_SAPP_CUSTOMER SET CUST_CITY = '{new_city}' WHERE CREDIT_CARD_NO = '{credit_card_no}'"
            cursor.execute(query)
            db.commit()
            print("City updated successfully.")
        elif choice == 4:
            new_state = pyip.inputStr("Enter new state: \n")
            if not new_state:
                print("Invalid input. State cannot be empty.")
                continue
            query = f"UPDATE CDW_SAPP_CUSTOMER SET CUST_STATE = '{new_state}' WHERE CREDIT_CARD_NO = '{credit_card_no}'"
            cursor.execute(query)
            db.commit()
            print("State updated successfully.")
        elif choice == 5:
            new_zip = pyip.inputStr("Enter new zipcode: \n")
            if not new_zip:
                print("Invalid input. Zipcode cannot be empty.")
                continue
            query = f"UPDATE CDW_SAPP_CUSTOMER SET CUST_ZIP = '{new_zip}' WHERE CREDIT_CARD_NO = '{credit_card_no}'"
            cursor.execute(query)
            db.commit()
            print("Zipcode updated successfully.")
        elif choice ==6:
            phone = pyip.inputStr("Enter phone number (XXX-XXX-XXXX): \n")
            if not phone:
                print("Invalid input. Phone number cannot be empty.")
                continue
            phone = re.sub(r'\D', '', phone)
            if len(phone) != 10:
                print("Invalid input. Phone number must be 10 digits.")
                continue
            phone = f"({phone[:3]}){phone[3:6]}-{phone[6:]}"
            query = f"UPDATE CDW_SAPP_CUSTOMER SET CUST_PHONE = '{phone}' WHERE CREDIT_CARD_NO = '{credit_card_no}'"
            cursor.execute(query)
            db.commit()
            print("Phone number updated successfully.\n")   
        elif choice == 7:
            #exit to main menu
            continue
    elif choice == 3:
        # Generate monthly bill
        credit_card_no = pyip.inputStr("Enter customer credit card number: \n")
        if len(credit_card_no) != 16:
            print("Invalid input. Credit card number should be 16 digits long.\n")
            continue
        if not credit_card_no:
            print("Invalid input. Credit card number cannot be empty.\n")
            continue
        year = pyip.inputInt("Enter year (YYYY): ")
        if len(year) != 4:
            print("Invalid input. Year should be in the format of YYYY.\n")
            continue
        if not year.isdigit():
            print("Invalid input. Year should be a number.\n")
            continue
        
        month = pyip.inputInt("Enter month (MM): ")
        if len(month) != 2:
            print("Invalid input. Month should be in the format of MM.\n")
            continue
        if not month.isdigit():
            print("Invalid input. Month should be a number.\n")
            continue
         
        # Format year and month as YYYYMM
        timeid = str(year) + str(month).zfill(2) 
        
        # Query for transactions of the given credit card and month/year
        query = "SELECT * FROM CDW_SAPP_CREDIT_CARD WHERE CUST_CC_NO = %s AND TIMEID LIKE %s "
        arg = (credit_card_no, f"{timeid}%")
        cursor.execute(query, arg)
        result = cursor.fetchall()
        
        if result:
            # Display results in a pretty table
            table = prettytable.PrettyTable()
            table.field_names = [i[0] for i in cursor.description]
            for row in result:
                table.add_row(row)
            print(table)
            # Calculate total amount due
            total = sum(row[-1] for row in result)
            print(f"\nTotal amount bill due for {month}/{year}: ${total:.2f}\n")
        else:
            print("No transactions found for the given credit card and month/year.\n")



    
    elif choice == 4:
    # Display transactions between two dates
        # Get start date
        credit_card_no = pyip.inputStr("Enter customer credit card number: \n")
        if len(credit_card_no) != 16:
            print("Invalid input. Credit card number should be 16 digits long.\n")
            continue
        if not credit_card_no:
            print("Invalid input. Credit card number cannot be empty.\n")
            continue
        start_date_str = pyip.inputStr("Enter start date (YYYYMMDD): ")
        while not re.match(r'^\d{8}$', start_date_str):
            print("Invalid input. Date should be in YYYYMMDD format.")
            start_date_str = pyip.inputStr("Enter start date (YYYYMMDD): ")
        start_date = datetime.strptime(start_date_str, '%Y%m%d').date()

        # Get end date
        end_date_str = pyip.inputStr("Enter end date (YYYYMMDD): ")
        while not re.match(r'^\d{8}$', end_date_str):
            print("Invalid input. Date should be in YYYYMMDD format.")
            end_date_str = pyip.inputStr("Enter end date (YYYYMMDD): ")
        end_date = datetime.strptime(end_date_str, '%Y%m%d').date()
        
        query = f"SELECT * FROM CDW_SAPP_CREDIT_CARD WHERE CUST_CC_NO ='{credit_card_no}' AND TIMEID BETWEEN '{start_date_str}' AND '{end_date_str}'"

        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            if  not rows:
                print("No transactions found between the given dates.\n")
            else:
                table = PrettyTable(['Transaction ID', 'Credit Card No', 'Transaction Type', 'Transaction Value', 'Transaction Date'])
                for row in rows:
                    transaction_id = row[0]
                    credit_card_no = row[1]
                    transaction_type = row[2]
                    transaction_value = row[3]
                    transaction_date = row[4]
                    table.add_row([transaction_id, credit_card_no, transaction_type, transaction_value, transaction_date])
                print(table)
        except Exception as err:
            print("Error executing query:", err)


    elif choice == 5:
    
        print("Exiting program.\n")
        break

    else:
        print("Invalid choice. Please try again.\n")

    
    