# 📚 Library Information Management System (LIMS)

A Django-based Library Information Management System designed to manage library readers. The application supports full CRUD operations and CSV export of reader data to an AWS S3 bucket. It also includes pagination, Django template rendering, and unit test coverage.

---

## 📦 Features

- 🧍 Add, edit, delete library readers
- 📄 Paginated list view of readers
- ☁️ Export reader data as CSV to AWS S3
- ✅ Unit tests for core functionality
- 🌐 Bootstrap-styled templates
- 🔐 Environment-based configuration

---

## 📁 Project Structure

LibraryInformationManagementSystem/
├── lims_portal/
│ ├── lims_app/ # App logic
│ │ ├── migrations/
│ │ ├── templates/
│ │ ├── static/
│ │ ├── views.py # Business logic
│ │ ├── models.py # Database models
│ │ ├── urls.py # App routes
│ │ ├── tests.py # Unit tests
│ ├── lims_portal/
│ │ ├── settings.py # Main settings
│ │ ├── urls.py # Project URL conf
│ ├── manage.py
├── .env # Environment variables (not checked into Git)
├── README.md

yaml
Copy
Edit

---

## 🛠️ Setup Instructions

### ✅ 1. Clone the Repository

```bash
git clone <your-repo-url>
cd LibraryInformationManagementSystem
✅ 2. Set Up Virtual Environment
bash
Copy
Edit
python3 -m venv .venv
source .venv/bin/activate
✅ 3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
✅ 4. Create and Configure .env File
Create a .env file in the root with the following:

ini
Copy
Edit
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_REGION=ap-south-1
Do NOT commit .env into GitHub.

✅ 5. Apply Migrations
bash
Copy
Edit
python3 manage.py migrate
✅ 6. Start Development Server
bash
Copy
Edit
python3 manage.py runserver
Visit: http://127.0.0.1:8000/

🌐 Application URLs
Route	Description
/ or /home	Home page
/readers	Readers table view
/readers/add	Add a new reader
/readers/edit/<id>/	Edit reader
/readers/delete/<id>/	Delete reader
/readers/export/	Export all readers to AWS S3

☁️ AWS S3 Integration
📌 What it does:
When the "Export" button is clicked on the /readers/ page,

Reader data is saved to a temporary CSV file in /tmp

Then it is uploaded to the specified S3 bucket

🧠 How it works:
python
Copy
Edit
import boto3

s3 = boto3.client("s3", ...)
s3.upload_file(path, bucket_name, key)
The export function is defined in: lims_app/views.py > export_readers_to_s3

You must configure AWS credentials properly in .env

✅ Running Tests
bash
Copy
Edit
python3 manage.py test
All tests are defined inside lims_app/tests.py

You can also install coverage to get test report:

bash
Copy
Edit
pip install coverage
coverage run manage.py test
coverage report -m
🧪 Test Cases Include
Page accessibility (home, readers)

POST reader creation

Edit/delete reader logic

S3 upload success/failure handling

Export route integration

📋 Example Reader CSV Format
The CSV exported to S3 will look like:

python-repl
Copy
Edit
Reference ID,Name,Contact,Address
R123,John Doe,9999999999,New York
R124,Jane Smith,8888888888,California
...
⚠️ Environment Notes
Requires Python ≥ 3.9

Django version: 5.x

AWS S3 bucket must be publicly accessible or authenticated using credentials

🔒 Security Tips
Never hardcode AWS credentials

Use .env and python-decouple if needed

Set proper bucket permissions on AWS

Sanitize all user inputs (Django ORM handles most of this)

👨‍💻 Author
Priyanshu Sheoran (SWE)
Email: priyanshusheoran1234@gmail.com

📄 License
This project is licensed under the MIT License.

yaml
Copy
Edit

---

## ✅ Next Steps

To make it production-ready:
- Add CI/CD (GitHub Actions)
- Connect to PostgreSQL or RDS
- Add login & permission system
- Store uploaded CSV paths in the database

