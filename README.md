# Revving invoice analyzer
A web application that process a spreadsheet and calculates the total values and fees of the invoices 

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)


Features

### Minimum Viable Product (MVP)

1. **App scaffolding:**
   - [x] Selecting sqlite for simplicity
   - [x] Create Customer model
   - [x] Create model to store the uploaded file
   - [x] Create model to store the data from the uploaded file
   - [x] Create model to store data of total values per revenue/client
   - [x] Set up celery


2. **Feature 2: Data ingestion**
   - [ ] Prepare admin interface to upload the file
   - [ ] Set up excel processor: panda
   - [ ] Saves data from spreadsheet and saves it in db
      - [ ] Implement spreadsheet structure validation
   - [ ] Implement spreadsheet data validation
      - [ ] Incorrect rows filtered out
   - [ ] Test on structure validation
   - [ ] Test on data validation

3. **Feature 3: DB Analizer service**
   - [ ] Create service that analyzes data in database and creates the totals per client-revenue source
   - [ ] Design the math equations for the analyzer
   - [ ] Create function that analyzes the db and process the totals
   - [ ] run periodically everyday to update results


### Future Additions

1. **Feature 4: Queue system**
   - [ ] Adding celery to data ingestion feature and to analizer feature

2. **Feature 5: Excel data validation**
   - [ ] Create excel with the invalid data rows and send it through email to the person that uploaded it

3. **Feature 6: PostgreSQL migration**
   - [ ] Migration to PostgreSQL DB and consider NoSQL

4. **Feature 7:Dockerized application**
   - [ ] Dockerize the environment for easier installation

5. **Feature 8: Django query counter**
   - [ ] Install tool to check some optimizable queries


## Getting Started



### Prerequisites



