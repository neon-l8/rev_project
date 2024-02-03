# rev_project

# Revving invoice analyzer
A web application that process a spreadsheet and calculates the total values and fees of the invoices 

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)


Features

### Minimum Viable Product (MVP)

1. **App scaffolding:**
   - Selecting sqlite for simplicity
   - Creating model to store the uploaded file
   - Create a model to store the data from the uploaded file
   - Create model to store data of total values per revenue/client
   - set up celery


2. **Feature 2: Data ingestion**
   - Saves data from spreadsheet and saves it in db
   - Set up excel processor: panda
   - Prepare admin interface to upload the file
   - Implement spreadsheet structure validation
   - Implement spreadsheet data validation
        - Create excel with invalid data rows and send it through email to the person that uploaded it.
   - Test on structure validation
   - Test on data validation

3. **Feature 3: DB Analizer service**
   - Create service that analyzes data in database and creates the totals per client-revenue source.
   - Design the math equations for the analyzer
   - Create the celery function that analyzes the db.
   - run periodically everyday to update results. 


### Future Additions

1. **Feature 4: PostgreSQL migration**
   - Migration to PostgreSQL DB and consider NoSQL

2. **Feature 5:Dockerized application**
   - Dockerize the environment for easier installation


## Getting Started



### Prerequisites



