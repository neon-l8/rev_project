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
   - [ ] Set up celery


2. **Feature 2: Data ingestion**
   - [x] Prepare admin interface to upload the file
   - [x] Set up excel processor: panda
   - [x] Saves data from spreadsheet and saves it in db
      - [x] Implement spreadsheet structure validation
   - [x] Implement spreadsheet data validation
      - [x] Incorrect rows filtered out
   - [x] Test on structure validation
   - [x] Test on data validation

3. **Feature 3: DB Analizer service**
   - [x] Create service that analyzes data in database and creates the totals per client-revenue source
   - [x] Design the math equations for the analyzer
   - [x] Create function that analyzes the db and process the totals
   - [x] Create tests to validate the calculus.
   - [x] Create JSON view to retrieve data from customers


### Future Additions

1. **Feature 4: Queue system**
   - [ ] Adding celery to data ingestion feature and to analizer feature

2. **Feature 5: Excel data validation**
   - [ ] Create excel with the invalid data rows and send it through email to the person that uploaded it

3. **Feature 6: PostgreSQL migration**
   - [ ] Migration to PostgreSQL

4. **Feature 7:Dockerized application**
   - [ ] Dockerize the environment for easier installation

5. **Feature 8: Django query counter**
   - [ ] Install tool to check some optimizable queries


## Getting Started
1. **Download the Project:**
   ```bash
   git clone https://github.com/neon-l8/rev_project.git
2. **Navigate to the project directory**
   ```bash
   cd revving
3. **Create a virtual environment**
   ```bash
      python -m venv rev_environment
4. **Activate the virtal environment**
   ```bash
      source rev_environment/bin/activate
5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
6. **Apply database migrations**
   ```bash
   python manage.py migrate
7. **Create superuser**
   ```bash
   python manage.py createsuperuser
8. **Run development server**
   ```bash
   python manage.py runserver
9. **Access the django admin**
   ```bash
   go to http://localhost:8000/admin and log in with the superuser credentials.
10. **Upload Spreadsheet file** 
   ```bash
   Upload the excel file in csv format on the InvoiceFile model in the admin page.
11. **Create a user for a customer**
   ```bash
   Go to a customer and create them a user
12. **Access the api JSON view**
   ```bash
   You have to options:
   1. You can log in as the user you just created and access the link http://127.0.0.1:8000/api/revenue_list/
   2. Because you are the superuser you can access http://127.0.0.1:8000/api/revenue_list/?customer_id={id of any customer}