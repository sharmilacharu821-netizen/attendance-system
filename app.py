

from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

students = [
    {"id": "101", "name": "Arun", "attended": 34, "conducted": 40},
    {"id": "102", "name": "Priya", "attended": 30, "conducted": 40},
    {"id": "103", "name": "Rahul", "attended": 25, "conducted": 40},
    {"id": "104", "name": "Divya", "attended": 36, "conducted": 40},
    {"id": "105", "name": "Karthik", "attended": 28, "conducted": 40}
]

TARGET = 75

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Attendance System V3</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #eef2f7;
            padding: 20px;
            margin: 0;
        }

        .container {
            max-width: 1000px;
            margin: auto;
            background: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 4px 14px #ccd3dd;
        }

        h1 {
            text-align: center;
            color: #173b67;
        }

        .subtitle {
            text-align: center;
            color: #64748b;
        }

        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 12px;
            margin: 20px 0;
        }

        .card {
            background: #eaf3ff;
            padding: 16px;
            border-radius: 9px;
        }

        .card h3 {
            margin: 0 0 8px;
            font-size: 14px;
            color: #475569;
        }

        .card p {
            font-size: 25px;
            font-weight: bold;
            margin: 0;
            color: #173b67;
        }

        input, select, button {
            padding: 10px;
            border: 1px solid #cbd5e1;
            border-radius: 5px;
        }

        input {
            box-sizing: border-box;
            width: 100%;
            margin: 10px 0;
        }

        button {
            background: #1769aa;
            color: white;
            border: none;
            cursor: pointer;
        }

        button:hover {
            background: #104d80;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }

        th, td {
            padding: 11px;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }

        th {
            background: #173b67;
            color: white;
        }

        .good {
            color: #137333;
            font-weight: bold;
        }

        .low {
            color: #c62828;
            font-weight: bold;
        }

        .message {
            color: #137333;
            font-weight: bold;
        }

        @media (max-width: 650px) {
            .container {
                padding: 12px;
                overflow-x: auto;
            }

            th, td {
                padding: 7px;
                font-size: 12px;
            }
        }
    </style>
</head>

<body>
<div class="container">
    <h1>Attendance Management System</h1>
    <p class="subtitle">Version 3 | Individual Class Attendance Tracker</p>

    {% if message %}
        <p class="message">{{ message }}</p>
    {% endif %}

    <div class="summary">
        <div class="card">
            <h3>Total Students</h3>
            <p>{{ students|length }}</p>
        </div>
        <div class="card">
            <h3>Total Classes Per Student (example)</h3>
            <p>40</p>
        </div>
        <div class="card">
            <h3>Required Attendance</h3>
            <p>{{ target }}%</p>
        </div>
    </div>

    <h2>Search Students</h2>
    <input id="search" onkeyup="searchStudents()"
           placeholder="Search by student name or ID">

    <h2>Mark a Class Attendance</h2>
    <form action="/mark" method="POST">
        <select name="student_id" required>
            {% for s in students %}
                <option value="{{ s.id }}">{{ s.name }} ({{ s.id }})</option>
            {% endfor %}
        </select>

        <select name="status" required>
            <option value="Present">Present</option>
            <option value="Absent">Absent</option>
        </select>

        <button type="submit">Save Attendance</button>
    </form>

    <h2>Individual Attendance Details</h2>
    <table id="studentTable">
        <thead>
            <tr>
                <th>ID</th>
                <th>Student</th>
                <th>Classes Conducted</th>
                <th>Attended</th>
                <th>Missed</th>
                <th>Percentage</th>
                <th>More Classes You Can Miss</th>
            </tr>
        </thead>
        <tbody>
            {% for s in students %}
            <tr>
                <td>{{ s.id }}</td>
                <td>{{ s.name }}</td>
                <td>{{ s.conducted }}</td>
                <td>{{ s.attended }}</td>
                <td>{{ s.conducted - s.attended }}</td>
                <td class="{{ 'good' if s.percentage >= target else 'low' }}">
                    {{ s.percentage }}%
                </td>
                <td>
                    {% if s.percentage >= target %}
                        {{ s.safe_absences }}
                    {% else %}
                        Attend {{ s.classes_needed }} consecutive classes
                    {% endif %}
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    <p>Attendance target: {{ target }}%. Values shown are sample data.</p>
</div>

<script>
function searchStudents() {
    const query = document.getElementById("search").value.toLowerCase();
    document.querySelectorAll("#studentTable tbody tr").forEach(row => {
        row.style.display = row.textContent.toLowerCase().includes(query)
            ? "" : "none";
    });
}
</script>
</body>
</html>
"""


@app.route("/")
def home():
    for student in students:
        conducted = student["conducted"]
        attended = student["attended"]

        student["percentage"] = (
            round(attended / conducted * 100, 2)
            if conducted > 0 else 0
        )

        if student["percentage"] >= TARGET and TARGET < 100:
            student["safe_absences"] = max(
                0,
                int((attended - (TARGET / 100) * conducted)
                    // (TARGET / 100))
            )
            student["classes_needed"] = 0
        else:
            student["safe_absences"] = 0
            student["classes_needed"] = (
                max(0, int(
                    (TARGET / 100 * conducted - attended)
                    / (1 - TARGET / 100)
                ) + (
                    1 if (TARGET / 100 * conducted - attended)
                    % (1 - TARGET / 100) != 0 else 0
                ))
                if TARGET < 100 else 0
            )

    return render_template_string(
        PAGE,
        students=students,
        target=TARGET,
        message=request.args.get("message", "")
    )


@app.route("/mark", methods=["POST"])
def mark_attendance():
    student_id = request.form.get("student_id")
    status = request.form.get("status")

    student = next(
        (s for s in students if s["id"] == student_id),
        None
    )

    if student and status in ["Present", "Absent"]:
        student["conducted"] += 1

        if status == "Present":
            student["attended"] += 1

    return redirect("/?message=Attendance+updated+successfully")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=False)

