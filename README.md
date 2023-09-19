# Data Engineering Coding Challenge

## Author

Andres Bonilla

## Overview

This project is a Data Engineering coding challenge for Globant. It consists of a Flask API that serves as an interface to upload CSV files and perform batch transactions on an SQLite database.

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- SQLite
- pandas

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/YourUsername/YourRepoName.git
   ```
   
2. Navigate to the project directory:
   ```
   cd YourRepoName
   ```
   
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
   
### Running the API

To run the API, execute the following command in the project directory:

```
python app.py
```

The API will be accessible at `http://127.0.0.1:5000/`

## API Endpoints

### POST `/upload_csv`

Uploads a CSV file and inserts its data into the specified table.

- Parameters:
  - `csv_file`: The CSV file to be uploaded
  - `table_name`: The table where the data will be inserted
  
### POST `/insert_batch`

Inserts a batch of rows into a specified table.

- Parameters:
  - `data`: JSON array containing the rows to be inserted
  - `table_name`: The table where the data will be inserted

### GET `/metrics/employees_per_department`

Returns the number of employees hired for each job and department in 2021 divided by quarter.

### GET `/metrics/departments_above_average`

Returns the list of departments that hired more employees than the mean of employees hired in 2021 for all departments.


