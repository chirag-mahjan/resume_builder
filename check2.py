import tkinter as tk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf():
    name = entry_name.get()
    email = entry_email.get()
    phone = entry_phone.get()
    education = entry_education.get("1.0", tk.END).strip()
    skills = entry_skills.get("1.0", tk.END).strip()
    experience = entry_experience.get("1.0", tk.END).strip()

    if not name or not email or not phone:
        messagebox.showerror("Error", "Please fill all required fields!")
        return

    import os

# Save in the same folder as this script
    save_path = os.path.join(os.getcwd(), name.replace(" ", "_") + "_Resume.pdf")
    file_name = save_path

    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter

    # Header
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, name)

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Email: {email}")
    c.drawString(50, height - 100, f"Phone: {phone}")
    c.line(50, height - 110, 550, height - 110)

    # Sections
    y = height - 140
    c.drawString(50, y, "Education:")
    text = c.beginText(150, y)
    text.setFont("Helvetica", 12)
    text.textLines(education)
    c.drawText(text)

    y -= (20 * (education.count('\n') + 2))
    c.drawString(50, y, "Skills:")
    text = c.beginText(150, y)
    text.setFont("Helvetica", 12)
    text.textLines(skills)
    c.drawText(text)

    y -= (20 * (skills.count('\n') + 2))
    c.drawString(50, y, "Experience:")
    text = c.beginText(150, y)
    text.setFont("Helvetica", 12)
    text.textLines(experience)
    c.drawText(text)

    c.save()
    messagebox.showinfo("Success", f"Resume generated:\n{file_name}")


# GUI setup
root = tk.Tk()
root.title("Resume Builder")
root.geometry("500x600")
root.configure(bg="#f0f0f0")

# Labels + Inputs
tk.Label(root, text="Name *", bg="#f0f0f0").pack()
entry_name = tk.Entry(root, width=50)
entry_name.pack(pady=5)

tk.Label(root, text="Email *", bg="#f0f0f0").pack()
entry_email = tk.Entry(root, width=50)
entry_email.pack(pady=5)

tk.Label(root, text="Phone *", bg="#f0f0f0").pack()
entry_phone = tk.Entry(root, width=50)
entry_phone.pack(pady=5)

tk.Label(root, text="Education", bg="#f0f0f0").pack()
entry_education = tk.Text(root, height=4, width=50)
entry_education.pack(pady=5)

tk.Label(root, text="Skills", bg="#f0f0f0").pack()
entry_skills = tk.Text(root, height=4, width=50)
entry_skills.pack(pady=5)

tk.Label(root, text="Experience", bg="#f0f0f0").pack()
entry_experience = tk.Text(root, height=4, width=50)
entry_experience.pack(pady=5)

# Button
tk.Button(root, text="Generate Resume", bg="#4CAF50", fg="white",
          font=("Arial", 12, "bold"), command=generate_pdf).pack(pady=20)

root.mainloop()
