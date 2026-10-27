
from flask import Flask, request, redirect, render_template_string
from datetime import date

app = Flask(__name__)

# Sample student list
students = [
    {"id": "101", "name": "Arun"},
    {"id": "102", "name": "Priya"},
    {"id": "103", "name": "Rahul"}
]

# Attendance records stored while the app is running
records = []

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Attendance System - v1</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #eef2f7;
            margin: 40px;
        }
        .container {
            max-width: 700px;
            margin: auto;
            background: white;
            padding: 25px;
            border-radius: 12px;
        }
        h1 { color: #244b87; }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 12px;
            border: 1px solid #ddd;
            text-align: left;
        }
        th { background: #244b87; color: white; }
        button {
            background: #244b87;
            color: white;
            padding: 10px 18px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        select { padding: 7px; }
        .success { color: green; }
    </style>
</head>
<body>
<div class="container">
    <h1>Student Attendance System</h1>
    <h3>Version 1 - Mark Daily Attendance</h3>
    <p>Date: {{ today }}</p>

    {% if message %}
        <p class="success">{{ message }}</p>
    {% endif %}

    <form method="POST" action="/mark">
        <label>Student:</label>
        <select name="student_id" required>
            {% for student in students %}
                <option value="{{ student.id }}">
                    {{ student.id }} - {{ student.name }}
                </option>
            {% endfor %}
        </select>

        <br><br>

        <label>Attendance:</label>
        <select name="status" required>
            <option value="Present">Present</option>
            <option value="Absent">Absent</option>
        </select>

        <br><br>
        <button type="submit">Mark Attendance</button>
    </form>

    <h3>Today's Attendance Records</h3>
    <table>
        <tr>
            <th>Student ID</th>
            <th>Name</th>
            <th>Date</th>
            <th>Status</th>
        </tr>
        {% for record in records %}
        <tr>
            <td>{{ record.id }}</td>
            <td>{{ record.name }}</td>
            <td>{{ record.date }}</td>
            <td>{{ record.status }}</td>
        </tr>
        {% endfor %}
    </table>
</div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(
        PAGE,
        students=students,
        records=records,
        today=date.today().isoformat(),
        message=request.args.get("message", "")
    )

@app.route("/mark", methods=["POST"])
def mark_attendance():
    student_id = request.form["student_id"]
    status = request.form["status"]

    student = next(
        (s for s in students if s["id"] == student_id),
        None
    )

    if student:
        records.append({
            "id": student["id"],
            "name": student["name"],
            "date": date.today().isoformat(),
            "status": status
        })

    return redirect("/?message=Attendance+marked+successfully")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
