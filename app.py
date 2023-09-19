from flask import Flask, request, jsonify
import sqlite3
import pandas as pd

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS departments (id INTEGER, department TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS jobs (id INTEGER, job TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS hired_employees (id INTEGER, name TEXT, datetime TEXT, department_id INTEGER, job_id INTEGER)')
    conn.commit()

init_db()

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Globant Challenge API"}), 200

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    try:
        csv_file = request.files.get('csv_file')
        table_name = request.form.get('table_name')
        allowed_tables = ['departments', 'jobs', 'hired_employees']

        if not csv_file or not table_name:
            return jsonify({"message": "Both csv_file and table_name are required"}), 400

        if table_name not in allowed_tables:
            return jsonify({"message": f"Invalid table_name. Allowed values are {', '.join(allowed_tables)}"}), 400

        df = pd.read_csv(csv_file, header=None)
        if table_name == 'departments':
            df.columns = ['id', 'department']
        elif table_name == 'jobs':
            df.columns = ['id', 'job']
        elif table_name == 'hired_employees':
            df.columns = ['id', 'name', 'datetime', 'department_id', 'job_id']

        conn = sqlite3.connect('mydatabase.db')
        df.to_sql(table_name, conn, if_exists='append', index=False)
        conn.commit()

        return jsonify({"message": f"{table_name} CSV uploaded and data inserted into DB"}), 201

    except Exception as e:
        print(str(e))
        return jsonify({"message": "An error occurred while processing the request"}), 500

@app.route('/insert_batch', methods=['POST'])
def insert_batch():
    try:
        data = request.json.get('data')
        table_name = request.json.get('table_name')
        if not data or not table_name:
            return jsonify({"message": "Both data and table_name are required"}), 400

        if len(data) > 1000:
            return jsonify({"message": "Cannot insert more than 1000 rows in a single request"}), 400

        conn = sqlite3.connect('mydatabase.db')
        df = pd.DataFrame(data)
        df.to_sql(table_name, conn, if_exists='append', index=False)
        conn.commit()

        return jsonify({"message": "Batch inserted"}), 201

    except Exception as e:
        print(str(e))
        return jsonify({"message": "An error occurred while processing the request"}), 500

@app.route('/metric1', methods=['GET'])
def metric1():
    try:
        with sqlite3.connect('mydatabase.db') as conn:
            query = '''
            SELECT 
                d.department, 
                j.job, 
                CASE 
                    WHEN strftime('%m', datetime) BETWEEN '01' AND '03' THEN 'Q1'
                    WHEN strftime('%m', datetime) BETWEEN '04' AND '06' THEN 'Q2'
                    WHEN strftime('%m', datetime) BETWEEN '07' AND '09' THEN 'Q3'
                    WHEN strftime('%m', datetime) BETWEEN '10' AND '12' THEN 'Q4'
                END as quarter,
                COUNT(*) as hires
            FROM hired_employees h
            JOIN departments d ON h.department_id = d.id
            JOIN jobs j ON h.job_id = j.id
            WHERE strftime('%Y', datetime) = '2021'
            GROUP BY d.department, j.job, quarter
            ORDER BY d.department ASC, j.job ASC;
            '''
            df = pd.read_sql(query, conn)
        return jsonify(df.to_dict(orient='records')), 200
    except Exception as e:
        print(str(e))
        return jsonify({"message": "An error occurred while processing the request"}), 500

@app.route('/metric2', methods=['GET'])
def metric2():
    try:
        with sqlite3.connect('mydatabase.db') as conn:
            mean_query = '''
            SELECT AVG(hires) FROM (
                SELECT 
                    department_id,
                    COUNT(*) as hires
                FROM hired_employees
                WHERE strftime('%Y', datetime) = '2021'
                GROUP BY department_id
            );
            '''
            mean_hires = pd.read_sql(mean_query, conn).iloc[0, 0]
            
            query = '''
            SELECT 
                d.id, 
                d.department,
                COUNT(*) as hires
            FROM hired_employees h
            JOIN departments d ON h.department_id = d.id
            WHERE strftime('%Y', datetime) = '2021'
            GROUP BY d.id, d.department
            HAVING COUNT(*) > ?
            ORDER BY COUNT(*) DESC;
            '''
            df = pd.read_sql(query, conn, params=(mean_hires,))
        return jsonify(df.to_dict(orient='records')), 200
    except Exception as e:
        print(str(e))
        return jsonify({"message": "An error occurred while processing the request"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
