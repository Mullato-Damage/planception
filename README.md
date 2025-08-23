  # Planception: A Smart Task Manager for Multidisciplinary Minds

Planception is a lightweight task management application designed to help students, professionals, and creatives with ADHD or multidisciplinary projects stay organized. The system supports creating, categorizing, and prioritizing tasks across different domains (school, work, writing, publishing, etc.). The goal is to provide structure while remaining simple and distraction-free, with a foundation for future AI assistant integration.

---

## Features
- ✅ Create, edit, and delete tasks  
- 📅 Assign due dates and priority levels  
- 🗂️ Organize tasks by category (e.g., School, Writing, Publishing)  
- 🔍 View tasks by filters (priority, category, deadline)  
- 🧩 Extensible design for future AI-powered task suggestions  

---

## Technology Stack
- **Language:** Python 3.10+  
- **Framework:** Flask (for app structure and routing)  
- **Testing:** Pytest (unit tests)  
- **Version Control:** Git/GitHub  

---

## Installation

1. Clone the repository:
   
   '''bash
   
       git clone https://github.com/YOUR-USERNAME/planception.git
   
       cd planception
   
2. Create a virtual environment (recommended):

    '''bash

       python -m venv venv
   
       source venv/bin/activate   # Mac/Linux
   
       venv\Scripts\activate      # Windows
   
4. Install dependencies:

   '''bash

       pip install -r requirements.txt

---

## Usage 

Run the application:
    
   '''bash
    
    python app.py
   
Then open your browser and navigate to:

    http://127.0.0.1:5000/
    
---

## Running Tests

To run the unit test suite:

   '''bash
    
    pytest
    
If successful, you'll see output showing all tests passing.

---

## Project Structure

planception/

│── app.py             # Application entry point

│── models.py          # Task model (Task class, data handling)

│── requirements.txt   # Python dependencies

│── README.md          # Project documentation

│

└── tests/

   └── test_app.py    # Unit tests for core functionality

---

## Documentation

- [Software Requirements Specification (SRS)](docs/Planception_SRS.pdf)
- [UML Class Diagram](docs/UML_ClassDiagram.png)
- [UML Use Case Diagram](docs/UML_UseCaseDiagram.png)

---

## Future Roadmap

- AI-powered task recommendations
- Calendar view and notifications
- Multi-user support with login system
- Cross-platform deployment (desktop and mobile)

---

## Author

Planception was created by Terione Martin as part of a Software Engineering course final project.

---

## License

This project is for academic purposes. For reuse or modification, please provide attribution.



