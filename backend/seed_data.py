from database import SessionLocal
from models.document import Document
from models.task import TaskItem
from models.report import Report
from models.whatsapp import WhatsAppMessage
from models.crm import Customer
from models.email import EmailMessage
from models.quotation import Quotation
from datetime import datetime, timedelta

def seed_db():
    db = SessionLocal()
    
    # Check if we already have data
    if db.query(TaskItem).count() > 0:
        print("Database already seeded.")
        return

    # 1. Documents
    docs = [
        Document(title="Employee Handbook", content="Welcome to the company! Working hours are 9 to 5.", author="HR Dept", document_type="pdf"),
        Document(title="Sales Playbook 2026", content="Target the enterprise sector with our new AI module. Emphasize automation and cost savings.", author="Sales Lead", document_type="pdf"),
        Document(title="API Integration Guide", content="To integrate our API, use Bearer token authentication. Endpoint is /api/v1/.", author="Engineering", document_type="docx")
    ]
    db.add_all(docs)

    # 2. Tasks
    tasks = [
        TaskItem(title="Prepare Q3 Sales Report", description="Compile all sales data for the upcoming board meeting.", assigned_to="Sales Team", status="todo", due_date=datetime.now() + timedelta(days=2)),
        TaskItem(title="Review new employee resumes", description="Screen candidates for the frontend developer role.", assigned_to="HR Dept", status="in_progress", due_date=datetime.now() + timedelta(days=1)),
        TaskItem(title="Fix command center bug", description="Investigate the suspense hook issue in Next.js", assigned_to="Engineering", status="done", due_date=datetime.now() - timedelta(days=1))
    ]
    db.add_all(tasks)

    # 3. Reports
    reports = [
        Report(title="Monthly Sales Performance", report_type="sales", data=[{"name": "Jan", "value": 4000}, {"name": "Feb", "value": 3000}, {"name": "Mar", "value": 2000}, {"name": "Apr", "value": 2780}, {"name": "May", "value": 1890}]),
        Report(title="Server Uptime Analytics", report_type="analytics", data=[{"name": "Week 1", "value": 99.9}, {"name": "Week 2", "value": 99.8}, {"name": "Week 3", "value": 100}, {"name": "Week 4", "value": 99.9}]),
        Report(title="Q2 Expenses", report_type="expense", data=[{"name": "Marketing", "value": 5000}, {"name": "Software", "value": 2000}, {"name": "Office", "value": 1500}, {"name": "Travel", "value": 1000}])
    ]
    db.add_all(reports)

    # 4. WhatsApp Messages
    whatsapp = [
        WhatsAppMessage(phone_number="+1234567890", message="Hey, when is the meeting tomorrow?", direction="inbound", status="received"),
        WhatsAppMessage(phone_number="+1234567890", message="The meeting is at 10 AM.", direction="outbound", status="delivered"),
        WhatsAppMessage(phone_number="+9876543210", message="Can you send over the latest quotation?", direction="inbound", status="received")
    ]
    db.add_all(whatsapp)

    # 5. Customers
    import uuid
    customers = [
        Customer(id=uuid.uuid4().hex, name="CodeCelix", email="contact@codecelix.com", phone="+923001234567", company="CodeCelix", status="active", notes="Key enterprise client."),
        Customer(id=uuid.uuid4().hex, name="TechCorp", email="info@techcorp.com", phone="+1987654321", company="TechCorp", status="lead", notes="Interested in AI modules.")
    ]
    db.add_all(customers)

    db.commit()
    print("Successfully seeded the database with fake/real mock data!")

if __name__ == "__main__":
    seed_db()
