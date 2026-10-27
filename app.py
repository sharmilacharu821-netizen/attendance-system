

from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

students = [
    {"id": "101", "name": "Arun"},
    {"id": "102", "name": "Priya"},
    {"id": "103", "name": "Rahul"},
    {"id": "104", "name": "Divya"},
    {"id": "105", "name": "Karthik"}
]

records = []

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Attendance System V2</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f0f4f8;
            margin: 0;
            padding: 25px;
        }

        .container {
            max-width: 850px;
            margin: auto;
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 15px #d0d7de;
        }

        h1 {
            text-align: center;
            color: #173b67;
        }

        .subtitle {
            text-align: center;
            color: #64748b;
        }

        .search {
            width: 100%;
            box-sizing: border-box;
            padding: 12px;
            margin: 15px 0;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }

        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }

        th {
            background: #173b67;
            color: white;
        }

        select, button {
            padding: 8px;
            border-radius: 5px;
            border: 1px solid #cbd5e1;
        }

        button {
            background: #1769aa;
            color: white;
            cursor: pointer;
            border: none;
        }

        button:hover {
            background: #104d80;
        }

        .summary {
            background: #e8f3ff;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
        }

        .records {
            background: #f8fafc;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
        }

        .message {
            color: #137333;
            font-weight: bold;
        }

        @media (max-width: 600px) {
            body {
                padding: 10px;
            }

            .container {
                padding: 12px;
            }

            th, td {
                padding: 7px;
                font-size: 13px;
            }
        }
    </style>
</head>

<body>
<div class="container">

    <h1>Attendance Management System</h1>
    <p class="subtitle">Version 2 | Student Attendance Dashboard</p>

    {% if message %}
        <p class="message">{{ message }}</p>
    {% endif %}

    <h2>Search Students</h2>

    <input
        class="search"
        type="text"
        id="searchInput"
        placeholder="Search by student name or ID..."
        onkeyup="searchStudents()"
    >

    <h2>Mark Attendance</h2>

    <table id="studentTable">
        <thead>
            <tr>
                <th>ID</th>
                <th>Student Name</th>
                <th>Attendance</th>
            </tr>
        </thead>

        <tbody>
        {% for student in students %}
            <tr>
                <td>{{ student.id }}</td>
                <td>{{ student.name }}</td>
                <td>
                    <form action="/mark" method="POST">
                        <input
                            type="hidden"
                            name="student_id"
                            value="{{ student.id }}"
                        >

                        <select name="status">
                            <option value="Present">Present</option>
                            <option value="Absent">Absent</option>
                        </select>

                        <button type="submit">Submit</button>
                    </form>
                </td>
            </tr>
        {% endfor %}
        </tbody>
    </table>

    <div class="summary">
        <h2>Attendance Summary</h2>
        <p>Total Students: {{ total }}</p>
        <p>Present: {{ present }}</p>
        <p>Absent: {{ absent }}</p>
        <p>Attendance Percentage: {{ percentage }}%</p>
    </div>

    <div class="records">
        <h2>Recent Attendance Records</h2>

        {% if records %}
            <table>
                <tr>
                    <th>Student ID</th>
                    <th>Name</th>
                    <th>Status</th>
                </tr>

                {% for record in records %}
                <tr>
                    <td>{{ record.id }}</td>
                    <td>{{ record.name }}</td>
                    <td>{{ record.status }}</td>
                </tr>
                {% endfor %}
            </table>
        {% else %}
            <p>No attendance marked yet.</p>
        {% endif %}
    </div>

</div>

<script>
function searchStudents() {
    let input = document.getElementById("searchInput");
    let filter = input.value.toLowerCase();
    let rows = document.querySelectorAll("#studentTable tbody tr");

    rows.forEach(function(row) {
        let text = row.textContent.toLowerCase();
        row.style.display = text.includes(filter) ? "" : "none";
    });
}
</script>

</body>
</html>
"""


@app.route("/")
def home():
    total = len(students)

    present = sum(
        1 for record in records
        if record["status"] == "Present"
    )

    absent = sum(
        1 for record in records
        if record["status"] == "Absent"
    )

    percentage = round((present / total) * 100, 2) if total else 0

    return render_template_string(
        PAGE,
        students=students,
        records=list(reversed(records)),
        total=total,
        present=present,
        absent=absent,
        percentage=percentage,
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
        records.append({
            "id": student["id"],
            "name": student["name"],
            "status": status
        })

    return redirect("/?message=Attendance+marked+successfully")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=False)