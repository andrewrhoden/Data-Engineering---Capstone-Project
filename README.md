

Project Name: Credit Card System Data Extraction, Transformation and Loading using Python and PySpark

Project Overview:

The Credit Card System Data Extraction, Transformation and Loading project involves reading and extracting data from JSON files using Python and PySpark, transforming the data according to the specifications outlined in the mapping document, and loading the transformed data into an RDBMS (MariaDB) using Python and PySpark.

The project has two functional requirements:

1.Data Extraction and Transformation with Python and PySpark

2. Data loading into Database

Technical Challenges:

The following technical challenges were faced during the project development:

1.Mapping the JSON file fields to the database fields.

2.Transforming the data types and formats.

3.Handling default values such as a phone number having only 7 digits.

4.Validating user inputs in the console menus.

How the technical challenges were resolved:

1.Mapping the JSON file fields to the database fields:
To map the JSON file fields to the database fields, we used the mapping document as a reference guide. The mapping document provided the field names and data types for each database table. This allowed us to create a mapping between the JSON file fields and the database fields.

2.Transforming the data types and formats:
To transform the data types and formats, we used Python and PySpark functions such as title() to convert the text to title case, and str() to convert the data types. We also used regular expressions to validate and format data such as phone numbers and email addresses.

3.Handling null values and default values:
To handle null values and default values, we used Python and PySpark functions such as if statement to check if a field is null, and if it is, we assigned a default value to the field.

4.Validating user inputs:
To validate user inputs, we used Python and PyInputPlus library functions such as inputInt() or inputstring to ensure that the input is an integer/string, and use validate_email module to ensure that the input is a valid email address.

Conclusion:

The Credit Card System Data Extraction, Transformation and Loading project involved extracting data from JSON files, transforming the data according to the specifications outlined in the mapping document, and loading the transformed data into an RDBMS using Python and PySpark. The project faced technical challenges such as mapping JSON fields to database fields, transforming data types and formats, handling null values and default values, and validating user inputs. These challenges were resolved using Python and PySpark functions and libraries such as title(), str(), regular expressions, if statement, and PyInputPlus.