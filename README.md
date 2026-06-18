# Placement_Portal_App
App with flask api , vue UI and cli for placement of students though admin to companies 

# Placement Portal Application (PPA)
## Overview

Placement Portal Application (PPA) is a web-based platform that simplifies campus recruitment activities for institutes. It enables interaction between three stakeholders:

* **Admin (Institute Placement Cell)**
* **Companies**
* **Students**

The system manages company registrations, placement drives, student applications, interview processes, and placement reports efficiently.

---

# Technology Stack

### Backend

* Flask (REST APIs)
* SQLite Database
* Redis (Caching)
* Celery + Redis (Background Jobs)

### Frontend

* Vue.js 3
* Vue Router
* Axios
* Bootstrap 5

### Other Tools

* Flask-CORS
* Werkzeug Password Hashing
* CSV Export
* Email Services for Notifications
* HTML/PDF Report Generation

---

# Main Features

## Authentication and Role Management

* Role-based login system.
* Single pre-created Admin account.
* Separate access for Admin, Company and Student.
* Session/JWT based authentication.

---

## Placement Drive Management

* Companies can create placement drives after approval.
* Admin can approve or reject drives.
* Students can browse approved drives.
* Eligibility validation based on branch, CGPA and graduation year.
* Prevent duplicate applications.

---

## Application Management

* Students can apply to drives.
* Companies can shortlist candidates.
* Companies can update status:

  * Applied
  * Shortlisted
  * Selected
  * Rejected
* Interview scheduling support.
* Complete placement history maintained.

---

## Email Notification System

Email notifications are integrated throughout the application.

### Student Notifications

* New placement drive announcements.
* Application confirmation emails.
* Reminder emails before application deadlines.
* Shortlisting notifications.
* Final selection or rejection notifications.

### Company Notifications

* Registration approval or rejection emails.
* Placement drive approval notifications.
* Notifications when students apply to drives.

### Admin Notifications

* Monthly placement activity reports sent via email.
* System alerts and summary reports.

Implemented using:

* SMTP (Gmail)
* Flask-Mail / smtplib
* Celery asynchronous tasks

---

## Analytics Dashboard and Charts

Interactive dashboards provide insights into placement activities.

### Admin Dashboard

Charts include:

* Students registered by branch.
* Companies approved over time.
* Placement drives created each month.
* Total applications received.
* Selection statistics.
* Overall placement percentage.

### Company Dashboard

Charts include:

* Applications received per drive.
* Shortlisted vs rejected students.
* Final selected candidates.
* Drive-wise applicant statistics.

### Student Dashboard

Charts include:

* Total applications submitted.
* Application status distribution.
* Placement history timeline.

Implemented using:

* Chart.js
* Vue.js
* Bootstrap cards
* Dynamic API endpoints

---

## Search and Filtering

* Search companies.
* Search placement drives.
* Search students.
* Eligibility-based filtering.
* Branch and CGPA filtering.

---

## CSV Export

Students can export application history asynchronously.

CSV includes:

* Student ID
* Company Name
* Drive Title
* Application Status
* Application Date

Implemented using:

* Celery
* Redis

---

## Background Jobs

### Daily Reminder Job

Runs every day.

Sends email reminders regarding:

* Upcoming application deadlines.
* Interview schedules.
* Pending actions.

---

### Monthly Report Job

Runs on the first day of every month.

Generates institute reports containing:

* Number of drives conducted.
* Applications received.
* Students selected.
* Company participation statistics.

Reports are generated in HTML/PDF format and emailed to Admin.

---

## Caching and Performance Optimization

Redis caching is used for:

* Dashboard statistics.
* Frequently accessed placement drives.
* Company details.
* Application counts.

Cache expiry is implemented to improve response time and reduce database load.

---

## Responsive User Interface

* Mobile and desktop compatible.
* Bootstrap-based design.
* Unified interface across devices.
* Form validation on frontend and backend.

---

## Additional Features

* Resume upload support.
* Placement history tracking.
* Interview scheduling.
* Blacklisting/deactivation of users.
* Real-time statistics.
* Email-based notifications.
* Dashboard analytics and charts.


# Database Schema

## Users Table

| Field      |
| ---------- |
| id         |
| username   |
| email      |
| password   |
| role       |
| active     |
| created_at |

---

## Students Table

| Field           |
| --------------- |
| student_id      |
| user_id         |
| full_name       |
| branch          |
| cgpa            |
| graduation_year |
| phone           |
| resume_path     |

---

## Companies Table

| Field           |
| --------------- |
| company_id      |
| user_id         |
| company_name    |
| hr_name         |
| hr_email        |
| website         |
| description     |
| approval_status |
| active          |

---

## Placement Drives Table

| Field                |
| -------------------- |
| drive_id             |
| company_id           |
| job_title            |
| job_description      |
| branch_eligibility   |
| min_cgpa             |
| graduation_year      |
| application_deadline |
| status               |
| created_at           |

---

## Applications Table

| Field            |
| ---------------- |
| application_id   |
| student_id       |
| drive_id         |
| application_date |
| status           |
| interview_date   |
| remarks          |

---

# User Roles

## Admin

* Manage students
* Manage companies
* Approve companies
* Approve placement drives
* View reports
* Search users

## Company

* Create drives
* Manage applicants
* Shortlist students
* Schedule interviews
* Update results

## Student

* View drives
* Apply for jobs
* Check application status
* Export application history

---

# Core Functionalities

### Authentication

* Role-based login
* Single admin account
* Session/JWT authentication

### Placement Drives

* Admin approval required
* Eligibility validation
* Prevent duplicate applications
* Dynamic status updates

### Search

* Search companies
* Search students
* Search placement drives

### Placement History

* Complete history maintained for every student

---

# Background Jobs

## Daily Reminder Job

Runs daily and sends reminders to students regarding upcoming application deadlines.

Can use:

* Email
* SMS
* Google Chat Webhooks

Implemented using:

* Celery
* Redis

---

## Monthly Activity Report

Runs on the first day of every month.

Includes:

* Number of placement drives conducted
* Total applications
* Total selected students

Report format:

* HTML
* PDF (optional)

Sent to Admin via Email.

---

## CSV Export Job

User-triggered asynchronous task.

Exports:

* Student ID
* Company Name
* Drive Title
* Application Status
* Dates

CSV generation runs as a Celery task and sends notification when completed.

---

# Caching

Redis cache is used for:

* Dashboard statistics
* Placement drives
* Company details
* Frequently accessed APIs

Cache expiry is implemented to improve performance.

---

# Project Structure

```
placement-portal/

backend/
│
├── app.py
├── config.py
├── db.py
├── models.py
├── auth_routes.py
├── admin_routes.py
├── company_routes.py
├── student_routes.py
├── tasks.py
├── celery_worker.py
└── utils/
    ├── mail_service.py
    ├── csv_export.py
    └── report_generator.py

frontend/
│
├── src/
│   ├── components/
│   ├── views/
│   │    ├── Login.vue
│   │    ├── Register.vue
│   │    ├── AdminDashboard.vue
│   │    ├── CompanyDashboard.vue
│   │    ├── StudentDashboard.vue
│   │    ├── PlacementDrives.vue
│   │    ├── Applications.vue
│   │    └── Profile.vue
│   ├── router/
│   ├── App.vue
│   └── main.js

database/
    placement.db
```

---

# Installation

## Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Server:

```
http://127.0.0.1:5000
```

---

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```
http://localhost:5173
```

---

## Redis

Start Redis server:

```bash
redis-server
```

---

## Celery Worker

```bash
celery -A celery_worker.celery worker --pool=solo -l info
```

---

---

