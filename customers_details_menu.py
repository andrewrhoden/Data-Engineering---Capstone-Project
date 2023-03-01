import mysql.connector
import configparser
import pyinputplus as pyip
from pyspark.sql.functions import  concat_ws, regexp_replace, concat,lit,col,udf, lpad,when, length,expr,substring
 


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
    print("CUSTOMER DETAILS MENU")
    print("1. Check existing account details")
    print("2. Modify existing account details")
    print("3. Generate monthly bill")
    print("4. Display transactions between two dates")
    print("5. Exit")
    choice = pyip.inputInt("Enter your choice (1-5):\n ", min=1, max=5)

    if choice == 1:
        # Check existing account details
        credit_card_no = pyip.inputStr("Enter credit card number: \n")
        query = f"SELECT * FROM CDW_SAPP_CUSTOMER WHERE CREDIT_CARD_NO = '{credit_card_no}'"
        cursor.execute(query)
        result = cursor.fetchall()
        if result:
            print(result)
        else:
            print("Customer not found.")

    elif choice == 2:
        # Modify existing account details
        credit_card_no = pyip.inputStr("Enter credit card number: ")
        query = f"SELECT * FROM CDW_SAPP_CUSTOMER WHERE CREDIT_CARD_NO = '{credit_card_no}'"
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            print(f"Customer Details for {credit_card_no}:\n")
            print(f"1. Name: {result[1]} {result[2]} {result[3]}\n")
            print(f"2. Address: {result[9]} {result[10]} {result[11]} {result[12]} {result[13]}\n")
            print(f"3. Phone: {result[14]}\n")
            print(f"4. Email: {result[15]}\n")
            field = pyip.inputInt("Enter field number to modify (1-5): ", min=1, max=5)
            if field == 1:
                first_name = pyip.inputStr("Enter first name: \n")
                middle_name = pyip.inputStr("Enter middle name: \n")
                last_name = pyip.inputStr("Enter last name: \n")
                first_name = first_name.title()
                middle_name = middle_name.lower()
                last_name = last_name.title()
                query = f"UPDATE CDW_SAPP_CUSTOMER SET FIRST_NAME = '{first_name}', MIDDLE_NAME = '{middle_name}', LAST_NAME = '{last_name}' WHERE CREDIT_CARD_NO = '{credit_card_no}'"
                cursor.execute(query)
                db.commit()
                print("Customer details updated successfully.\n")
            elif field == 2:
                apt_no = pyip.inputStr("Enter apartment number: \n")
                street = pyip.inputStr("Enter street name: \n")
                full_street_address = f"{apt_no}, {street} "
                query = f"UPDATE CDW_SAPP_CUSTOMER SET FULL_STREET_ADDRESS = '{full_street_address}' WHERE CREDIT_CARD_NO = '{credit_card_no}'"
                cursor.execute(query)
                db.commit()
                print("Customer details updated successfully.\n")
            elif field == 3:
                phone = pyip.inputStr("Enter the 10 digit phone number without spaces or hyphen: \n")
                phone = f"({phone[:3]}){phone[3:6]}-{phone[6:]}"
                query = f"UPDATE CDW_SAPP_CUSTOMER SET CUST_PHONE = '{phone}' WHERE CREDIT_CARD_NO = '{credit_card_no}'"
                cursor.execute(query)
                db.commit()
                print("Customer details updated successfully.\n")
            elif field == 4:
                email = pyip.inputStr("Enter email address: \n")
                query = f"UPDATE CDW_SAPP_CUSTOMER SET EMAIL = '{email}' WHERE CREDIT_CARD_NO = '{credit_card_no}'"
                cursor.execute(query)
                db.commit()
                print("Customer details updated successfully.\n")
            elif field == 5:
                print("Returning to main menu...\n")
            else:
                print("Invalid field number. Returning to main menu...\n")

    elif choice == 3:
        # Generate monthly bill
        credit_card_no = pyip.inputStr("Enter credit card number: ")
        month = pyip.inputInt("Enter month (1-12): ", min=1, max=12)
        year = pyip.inputInt("Enter year (yyyy): ")
        query = f"SELECT * FROM CDW_SAPP_CREDITCARD WHERE CREDIT_CARD_NO = '{credit_card_no}' AND MONTH = {month} AND YEAR = {year}"
        cursor.execute(query)
        result = cursor.fetchall()
        if result:
            for row in result:
                print(f"Credit Card No: {row[0]}")
                print(f"Year: {row[1]}")
                print(f"Month: {row[2]}")
                print(f"Outstanding Balance: {row[3]}")
                print(f"Minimum Payment: {row[4]}")
                print(f"Credit Limit: {row[5]}\n")
        else:
            print("No bill found for this month.")

    elif choice == 4:
        # Display transactions between two dates
        credit_card_no = pyip.inputStr("Enter credit card number: ")
        from_date = pyip.inputStr("Enter start date (yyyy-mm-dd): ")
        to_date = pyip.inputStr("Enter end date (yyyy-mm-dd): ")
        query = f"SELECT * FROM CDW_SAPP_TRANSACTIONS WHERE CREDIT_CARD_NO = '{credit_card_no}' AND TRANSACTION_DATE BETWEEN '{from_date}' AND '{to_date}'"
        cursor.execute(query)
        result = cursor.fetchall()
        if result:
            for row in result:
                print(f"Credit Card No: {row[0]}")
                print(f"Transaction ID: {row[1]}")
                print(f"Transaction Type: {row[2]}")
                print(f"Transaction Value: {row[3]}")
                print(f"Transaction Date: {row[4]}")
                print(f"Branch Code: {row[5]}\n")
            else:
                print("No transactions found between these dates.")

    elif choice == 5:
        print("Thank you for using the system.")
        db.close()
        break

    else:
        print("Invalid choice. Please try again.")










# elif choice == 3:
# # Add new account
# first_name = pyip.inputStr("Enter first name: \n")
# middle_name = pyip.inputStr("Enter middle name: \n")
# last_name = pyip.inputStr("Enter last name: \n")
# first_name = first_name.title()
# middle_name = middle_name.lower()
# last_name = last_name.title()
# apt_no = pyip.inputStr("Enter apartment number: \n")
# street = pyip.inputStr("Enter street name: \n")
# city = pyip.inputStr("Enter city: \n")
# state = pyip.inputStr("Enter state abbreviation (e.g. NY): \n")
# zip_code = pyip.inputStr("Enter zip code: \n")
# full_street_address = f"{apt_no}, {street} {city} {state} {zip_code}"
# phone = pyip.inputStr("Enter the 10 digit phone number without spaces or hyphen: \n")
# phone = f"({phone[:3]}){phone[3:6]}-{phone[6:]}"
# email = pyip.inputStr("Enter email address: \n")
# credit_card_no = pyip.inputStr("Enter credit card number: \n")
# branch_code = pyip.inputStr("Enter branch code (e.g. AA1): \n")
# query = f"INSERT INTO CDW_SAPP_CUSTOMER (CREDIT_CARD_NO, FIRST_NAME, MIDDLE_NAME, LAST_NAME, SSN, CUST_STREET_ADDRESS, CUST_CITY, CUST_STATE, CUST_COUNTRY, CUST_ZIP, CUST_PHONE, CUST_EMAIL, LAST_UPDATED, BRANCH_CODE) VALUES ('{credit_card_no}', '{first_name}', '{middle_name}', '{last_name}', '0', '{full_street_address}', '{city}', '{state}', 'USA', '{zip_code}', '{phone}', '{email}', '2022-02-14', '{branch_code}')"
# cursor.execute(query)
# db.commit()
# print("New account created successfully.\n")

# elif choice == 4:
# # Delete existing account
# credit_card_no = pyip.inputStr("Enter credit card number: ")
# query = f"SELECT * FROM CDW_SAPP_CUSTOMER WHERE CREDIT_CARD_NO = '{credit_card_no}'"
# cursor.execute(query)
# result = cursor.fetchone()
# if result:
# confirmation = pyip.inputYesNo(f"Are you sure you want to delete the account for {result[1]} {result[2]} {result[3]}? (y/n)\n")
# if confirmation == "yes":
# query = f"DELETE FROM CDW_SAPP_CUSTOMER WHERE CREDIT_CARD_NO = '{credit_card_no}'"
# cursor.execute(query)
# db.commit()
# print("Account deleted successfully.\n")
# else:
# print("Deletion cancelled.\n")
# else:
