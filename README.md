# 🎉 Event Management System (Django + Tailwind + DaisyUI)

An advanced **Event Management System** built using the **Django MVT architecture** with a modern frontend powered by **Tailwind CSS** and **DaisyUI**.  
The project features a **role-based access control system** with three roles — **Admin**, **Organizer**, and **User**.  
Data is managed through **PostgreSQL**, and the project is **deployed live on Render**.

🌐 **Live Demo:** [(https://event-management-system-assignment3-3.onrender.com/)]

---

## 🚀 Features

### 👑 Admin
The admin has full control over all data and users.

**Permissions:**
- Manage Users (add, edit, delete, view)
- Manage Organizers
- Manage Events, Categories, and RSVPs
- Manage Groups, Permissions, and Content Types
- View Log Entries and Sessions

---

### 🧑‍💼 Organizer
Organizers can manage their own events and categories.

**Permissions:**
- Add, change, delete, and view **Categories**
- Add, change, delete, and view **Events**

---

### 🙋‍♂️ User
Users can browse events and manage their RSVPs.

**Permissions:**
- View Categories and Events
- Add, change, delete, and view **RSVPs**

---

## 🧩 Tech Stack

| Component | Technology |
|------------|-------------|
| **Framework** | Django (MVT Pattern) |
| **Frontend** | Tailwind CSS + DaisyUI |
| **Database** | PostgreSQL |
| **Deployment** | Render |
| **Authentication** | Django’s built-in auth system |
| **Template Engine** | Django Template Language (DTL) |

---

## ⚙️ Installation Guide (Local Setup)

### 1️⃣ Clone the Repository
```bash

https://github.com/pritomcse29/Event-Management-System-assignment3.git
cd event-management-system

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Setup Environment Variables

Create a .env file in your project root:

DEBUG=True
SECRET_KEY=your_secret_key_here
DATABASE_URL=postgresql://username:password@localhost:5432/db_name
ALLOWED_HOSTS=127.0.0.1,localhost

5️⃣ Run Migrations
python manage.py makemigrations
python manage.py migrate

6️⃣ Create Superuser
python manage.py createsuperuser

7️⃣ Run Server
python manage.py runserver

Open your browser at:

http://127.0.0.1:8000/

🌐 Deploying to Render
Steps:

Push your code to GitHub

Go to Render.com

Create a New Web Service

Connect your GitHub repo

Set Environment Variables:

SECRET_KEY=your_secret_key
DEBUG=False
DATABASE_URL=render_postgres_url
ALLOWED_HOSTS=your-app-name.onrender.com


Add Build & Start Commands:

Build Command: pip install -r requirements.txt && python manage.py collectstatic --noinput
Start Command: gunicorn your_project_name.wsgi


Deploy and visit your live app!

🧑‍💻 Project Structure (MVT)
event_management/
├── manage.py
├── event_app/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│   ├── forms.py
│   └── admin.py
├── static/
│   ├── css/
│   └── js/
├── templates/
│   └── base.html
└── requirements.txt

🖌️ Styling with Tailwind & DaisyUI

Tailwind and DaisyUI are used for a clean and responsive UI.

To rebuild CSS manually:

npx tailwindcss -i ./static/src/input.css -o ./static/css/output.css --watch

🔐 Role & Permission Overview
Role	   Category 	    Event     RSVP	     User	      Admin Tools
Admin	    ✅ Full	   ✅ Full	    ✅ Full	  ✅ Full	✅ Logs, Groups, Permissions
Organizer	✅ CRUD	   ✅ CRUD	     ❌	        ❌	         ❌
User	    👀 View	   👀 View	    ✅ CRUD	    ❌	         ❌

🤝 Contributing

Contributions are always welcome!
To contribute:

Fork the repository

Create a new branch (git checkout -b feature-name)

Commit your changes (git commit -m "Added new feature")

Push to your branch (git push origin feature-name)

Open a Pull Request



