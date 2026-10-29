
from flask import Flask, request, redirect, url_for, render_template_string
from urllib.parse import urlparse
from datetime import datetime

app = Flask(__name__)
submissions = []

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Assignment Submission Portal</title>
<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    font-family: "Segoe UI", Arial, sans-serif;
    background: #f1f5fb;
    color: #17365d;
}
header {
    background: linear-gradient(120deg, #102b4e, #1763a6);
    color: white;
    padding: 24px 6%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 15px;
    flex-wrap: wrap;
}
.brand { display: flex; align-items: center; gap: 15px; }
.logo { font-size: 40px; }
header h1 { margin: 0; font-size: 25px; }
header p { margin: 6px 0 0; color: #dbeafe; }
nav { color: #e5efff; }
main { max-width: 1200px; margin: 32px auto; padding: 0 20px; }
.card {
    background: white;
    border: 1px solid #e1eaf5;
    border-radius: 14px;
    padding: 28px;
    margin-bottom: 25px;
    box-shadow: 0 5px 20px #17365d12;
}
h2 { margin: 0 0 10px; font-size: 23px; }
.description { color: #6b7f99; margin-bottom: 25px; line-height: 1.6; }
.form-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 22px;
}
label { display: block; font-weight: 600; margin-bottom: 9px; }
.required { color: #dc3545; }
input {
    width: 100%;
    padding: 14px;
    border: 1px solid #cedbea;
    border-radius: 8px;
    font-size: 15px;
}
input:focus {
    outline: none;
    border-color: #1683e8;
    box-shadow: 0 0 0 3px #1683e81c;
}
button {
    width: 100%;
    padding: 15px;
    margin-top: 25px;
    border: 0;
    border-radius: 8px;
    background: linear-gradient(100deg, #087ee8, #145dd5);
    color: white;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
}
button:hover { filter: brightness(.94); }
.alert { padding: 13px; border-radius: 8px; margin-bottom: 18px; }
.success { background: #e8f8ed; color: #176536; }
.table-wrap { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; min-width: 700px; }
th { background: #edf4fb; text-align: left; padding: 14px 12px; }
td { padding: 14px 12px; border-bottom: 1px solid #e7edf5; }
tbody tr:hover { background: #f7faff; }
a { color: #087ee8; overflow-wrap: anywhere; }
.empty { text-align: center; color: #71839a; padding: 30px; }
.count {
    display: inline-block; margin-left: 8px; padding: 4px 10px;
    border-radius: 20px; background: #e7f1ff; color: #1559a6;
    font-size: 12px;
}
footer { text-align: center; padding: 5px 15px 25px; color: #71839a; }
@media(max-width:650px) {
    header { padding: 20px; }
    header h1 { font-size: 20px; }
    nav { display: none; }
    main { padding: 0 12px; margin-top: 20px; }
    .card { padding: 20px 15px; }
    .form-grid { grid-template-columns: 1fr; }
}
</style>
</head>
<body>
<header>
    <div class="brand">
        <div class="logo">🎓</div>
        <div>
            <h1>Assignment Submission Portal</h1>
            <p>Submit your work. Track your progress.</p>
        </div>
    </div>
    <nav>Submit &nbsp; • &nbsp; Track &nbsp; • &nbsp; Learn</nav>
</header>
<main>
    <section class="card">
        <h2>➤ Submit Your Assignment</h2>
        <p class="description">
            Enter your details and provide a link to your assignment.
            All fields are required.
        </p>
        {% if message %}
        <div class="alert success">{{ message }}</div>
        {% endif %}
        <form method="POST" action="/submit">
            <div class="form-grid">
                <div>
                    <label for="name">Student Name <span class="required">*</span></label>
                    <input id="name" name="name" placeholder="Enter your full name" required>
                </div>
                <div>
                    <label for="registration">Registration Number <span class="required">*</span></label>
                    <input id="registration" name="registration" placeholder="e.g. BSE-062" required>
                </div>
                <div>
                    <label for="title">Assignment Title <span class="required">*</span></label>
                    <input id="title" name="title" placeholder="Enter assignment title" required>
                </div>
                <div>
                    <label for="url">Submission URL <span class="required">*</span></label>
                    <input id="url" name="url" type="url" placeholder="https://example.com" required>
                </div>
            </div>
            <button type="submit">➤ &nbsp; Submit Assignment</button>
        </form>
    </section>
    <section class="card">
        <h2>☷ Saved Submissions <span class="count">{{ submissions|length }} total</span></h2>
        <p class="description">View the assignments submitted during this session.</p>
        <div class="table-wrap">
        <table>
            <thead>
                <tr>
                    <th>#</th><th>Student Name</th><th>Registration No.</th>
                    <th>Assignment Title</th><th>Submission URL</th><th>Submitted At</th>
                </tr>
            </thead>
            <tbody>
                {% for s in submissions %}
                <tr>
                    <td>{{ loop.index }}</td>
                    <td>{{ s.name }}</td>
                    <td>{{ s.registration }}</td>
                    <td>{{ s.title }}</td>
                    <td><a href="{{ s.url }}" target="_blank" rel="noopener noreferrer">Open link ↗</a></td>
                    <td>{{ s.timestamp }}</td>
                </tr>
                {% else %}
                <tr><td colspan="6" class="empty">📄 No assignments submitted yet.</td></tr>
                {% endfor %}
            </tbody>
        </table>
        </div>
    </section>
</main>
<footer>Assignment Submission Portal | Built for better learning 🚀</footer>
</body>
</html>
"""


def valid_url(value):
    try:
        parsed = urlparse(value)
        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.netloc)
            and "." in parsed.netloc
            and " " not in value
        )
    except ValueError:
        return False


@app.route("/")
def index():
    return render_template_string(
        HTML,
        submissions=submissions,
        message=request.args.get("message", "")
    )


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "").strip()
    registration = request.form.get("registration", "").strip()
    title = request.form.get("title", "").strip()
    url = request.form.get("url", "").strip()

    if not all([name, registration, title, url]):
        return "Validation error: All fields are required.", 400

    if not valid_url(url):
        return "Validation error: Please enter a valid HTTP or HTTPS URL.", 400

    submissions.append({
        "name": name,
        "registration": registration,
        "title": title,
        "url": url,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    return redirect(url_for("index", message="Assignment submitted successfully!"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
