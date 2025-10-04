from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def build_resume():
    # Step 1: Collect user details
    name = input("Enter your full name: ")
    email = input("Enter your email: ")
    phone = input("Enter your phone number: ")
    education = input("Enter your education details: ")
    skills = input("Enter your skills (comma separated): ")
    experience = input("Enter your experience (if any): ")

    # Step 2: Create a PDF
    file_name = name.replace(" ", "_") + "_Resume.pdf"
    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter

    # Step 3: Add content to PDF
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, name)

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Email: {email}")
    c.drawString(50, height - 100, f"Phone: {phone}")

    c.line(50, height - 110, 550, height - 110)

    c.drawString(50, height - 140, "Education:")
    c.drawString(150, height - 140, education)

    c.drawString(50, height - 170, "Skills:")
    c.drawString(150, height - 170, skills)

    c.drawString(50, height - 200, "Experience:")
    c.drawString(150, height - 200, experience)

    # Step 4: Save PDF
    c.save()
    print(f"✅ Resume generated successfully: {file_name}")

build_resume()
