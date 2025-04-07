from flask import Flask, request, jsonify, send_from_directory, abort
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

app = Flask(__name__, static_folder='static')

# Load environment variables
load_dotenv()

# Database config
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_PORT = os.getenv('DB_PORT')

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )

# Serve frontend
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# --- Mechanics Endpoints ---
@app.route('/api/mechanics', methods=['GET'])
def list_mechanics():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, name, specialization, created_at FROM mechanics ORDER BY id;")
    mechanics = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(mechanics)

@app.route('/api/mechanics', methods=['POST'])
def create_mechanic():
    data = request.get_json()
    name = data.get('name')
    specialization = data.get('specialization')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO mechanics (name, specialization) VALUES (%s, %s) RETURNING id;",
        (name, specialization)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'id': new_id}), 201

# --- Customers Endpoints ---
@app.route('/api/customers', methods=['GET'])
def list_customers():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, name, phone, email, created_at FROM customers ORDER BY id;")
    customers = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(customers)

@app.route('/api/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    name = data.get('name')
    phone = data.get('phone')
    email = data.get('email')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO customers (name, phone, email) VALUES (%s, %s, %s) RETURNING id;",
        (name, phone, email)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'id': new_id}), 201

# --- Appointments Endpoints ---
@app.route('/api/appointments', methods=['GET'])
def list_appointments():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('''
        SELECT
            a.id,
            a.appointment_time,
            a.description,
            m.name AS mechanic_name,
            c.name AS customer_name
        FROM appointments a
        JOIN mechanics m ON a.mechanic_id = m.id
        JOIN customers c ON a.customer_id = c.id
        ORDER BY a.appointment_time;
    ''')
    appointments = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(appointments)

@app.route('/api/appointments', methods=['POST'])
def create_appointment():
    data = request.get_json()
    mechanic_id = data.get('mechanic_id')
    customer_id = data.get('customer_id')
    appointment_time = data.get('appointment_time')
    description = data.get('description')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO appointments (mechanic_id, customer_id, appointment_time, description)
        VALUES (%s, %s, %s, %s) RETURNING id;
    ''', (mechanic_id, customer_id, appointment_time, description))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'id': new_id}), 201

@app.route('/api/appointments/<int:appointment_id>', methods=['PUT', 'PATCH'])
def update_appointment(appointment_id):
    data = request.get_json()
    appointment_time = data.get('appointment_time')
    description = data.get('description')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE appointments SET appointment_time = %s, description = %s WHERE id = %s;",
                (appointment_time, description, appointment_id))
    if cur.rowcount == 0:
        cur.close()
        conn.close()
        abort(404, 'Appointment not found')
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'message': 'Appointment updated'})

@app.route('/api/appointments/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM appointments WHERE id = %s;", (appointment_id,))
    if cur.rowcount == 0:
        cur.close()
        conn.close()
        abort(404, 'Appointment not found')
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'message': 'Appointment deleted'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
