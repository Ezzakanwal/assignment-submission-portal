
import json
import subprocess
import sys
from pathlib import Path

import requests

BASE_DIR = Path(__file__).parent
REPORT_FILE = BASE_DIR / "test-report.json"
RECEIVER_URL = "http://127.0.0.1:5001/report"

result = subprocess.run(
    [sys.executable, "-m", "pytest", "-v", "--tb=short"],
    cwd=BASE_DIR,
    capture_output=True,
    text=True
)

report = {
    "project": "Assignment Submission Portal",
    "test_command": "pytest -v",
    "exit_code": result.returncode,
    "status": "passed" if result.returncode == 0 else "failed",
    "stdout": result.stdout,
    "stderr": result.stderr
}

REPORT_FILE.write_text(
    json.dumps(report, indent=4),
    encoding="utf-8"
)

print("Test status:", report["status"])
print("Report saved:", REPORT_FILE.name)

try:
    response = requests.post(RECEIVER_URL, json=report, timeout=10)
    print("Receiver response:", response.status_code)
    print(response.text)
except requests.RequestException as error:
    print("Could not send report:", error)
