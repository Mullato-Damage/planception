# Planception User Manual

# Introduction

Planception is a lightweight task management system designed to help multidisciplinary users (students, writers, professionals) organize assignments and deadlines. This guide will walk you through installation, usage, and troubleshooting.

## 1\. Installation & Setup

### Prerequisites

* Windows 10/11 (Linux/Mac supported with slight path differences)  
* Python 3.10+  
* Git (optional, for pulling updates)

### Setup Steps

1. Clone or download the repository:

   \[git clone https://github.com/\<your-username\>/planception.git\]

   \[cd planception\]

2. Create a virtual environment:

   \[python \-m venv .venv\]

   \[. .\\.venv\\Scripts\\Activate.ps1\]

3. Install dependencies:

   \[pip install \-r requirements.txt\]

4. Initialize the database (first run will auto-create it in \[/instance/\]).

## 2\. Running the Application

1. Set the Flask environment:

   \[$env:FLASK\_APP="app.py"\]

   \[flask run\]

2. Open your browser to:

   \[[http://127.0.0.1:5000](http://127.0.0.1:5000)\]

## 3\. Using Planception

### Create a Task

* Navigate to the Add Task form.  
* Enter:  
  * Title (required)  
  * Due Date (YYYY-MM-DD)  
  * Priority (Low / Medium / High)  
  * Category (School, Work, Writing, etc.)  
* Click Add Task.  
* ✅ Success: Task appears in All Tasks, Today (if due today), and Overdue (if past due).

### View Tasks

* All Tasks → full list of entries.  
* Today’s Tasks → highlights tasks due today.  
* Overdue → tasks past their due date.

### Delete a Task

* Press the Delete button next to a task.  
* Confirmation message will appear at the top.

(Editing and sorting will arrive in V2 \- future releases will expand features.)

## 4\. Running Tests

From the project root:  
\[python \-m pytest \-q\]

* ✔ 5 passing tests \= everything works.  
* To view coverage:  
  \[pytest \--cov=./ \--cov-report=html\]  
  Then open \[htmlcov/index.html\] in your browser.

## 5\. Troubleshooting

* Error: \[ModuleNotFoundError: No module named 'app'\]

  Run tests with:

  \[python \-m pytest \-q\]

  (instead of just \[pytest\]).

* Database not creating?

  Make sure \[/instance/\] exists in your project root. Flask will populate \[planception.sqlite\].

* Styles not showing?  
  Confirm \[/static/styles.css\] is linked in \[templates/base.html\].

## 6\. Versioning

* V1 (MVP): Create, delete, date-based filtering, basic persistence, and tests.  
* V1.1: Docs, diagrams, README, testing report.  
* V2 (Planned): Editing tasks, sorting by category/priority, optional time fields.

## 7\. Credits

Author: Terione Martin  
Course: Software Engineering – Final Project  
Tools: Python 3.10, Flask, SQLAlchemy, pytest  
