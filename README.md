# Assignment Submission Portal

## Project Description
A Flask web application for student assignment submissions with automated testing.

## Features
- Assignment submission form
- Required field validation
- Invalid URL rejection
- Automated tests using pytest
- JSON test report generation
- Local report receiver

## Requirements
Python 3, Flask, pytest, and requests.

## Run the Application
`python app.py`

## Run Tests
`python -m pytest -v`

## Generate Test Report
1. Run `python report_receiver.py` in the first terminal.
2. Run `python send_report.py` in a second terminal.
3. Check the generated `test-report.json` file.

## GitHub Repository
https://github.com/Ezzakanwal/assignment-submission-portal
