import tkinter as tk
from tkinter import messagebox, filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import os

def generate_pdf():
    name = entry_name.get()
    email = entry_email.get()
    phone = entry_phone.get()
    education = entry_education.get("1.0", tk.END).strip()
    skills = entry_skills.get("1.0", tk.END).strip()
    experience = entry_experience.get("1.0", tk.END).strip()
    color_choice = color_var.get()

    if not name or not email or not phone:
        messagebox.showerror("Error", "Please fill all required fields!")
        return

    # Let user pick where to save
    file_name = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        initialfile=name.replace(" ", "_") + "_Resume.pdf"
    )

    if not file_name:
        return

    # Choose theme color
    color_map = {
        "Blue": colors.HexColor("#1E90FF"),
        "Green": colors.HexColor("#2E8B57"),
        "Gray": colors.HexColor("#444444")
    }
    theme_color = color_map.get(color_choice, colors.black)

    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter

    # Header Bar
    c.setFillColor(theme_color)
    c.rect(0, height - 70, width, 70, fill=1, stroke=0)

    # Name in header
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(50, height - 45, name)

    # Contact info
    c.setFont("Helvetica", 12)
    c.drawRightString(width - 50, height - 45, f"Email: {email}")
    c.drawRightString(width - 50, height - 60, f"Phone: {phone}")

    # Reset text color
    c.setFillColor(colors.black)

    # Sections
    y = height - 110

    def draw_section(title, content):
        nonlocal y
        if not content.strip():
            return
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(theme_color)
        c.drawString(50, y, title)
        c.setFillColor(colors.black)
        y -= 20
        c.setFont("Helvetica", 12)
        text = c.beginText(70, y)
        text.textLines(content)
        c.drawText(text)
        y -= (15 * (content.count('\n') + 2))

    draw_section("Education", education)
    draw_section("Skills", skills)
    draw_section("Experience", experience)

    # Footer line
    c.setStrokeColor(theme_color)
    c.line(50, 50, width - 50, 50)

    c.save()
    messagebox.showinfo("Success", f"Resume generated:\n{file_name}")

# GUI setup
root = tk.Tk()
root.title("Stylish Resume Builder")
root.geometry("520x650")
root.configure(bg="#f9f9f9")

tk.Label(root, text="Name *", bg="#f9f9f9").pack()
entry_name = tk.Entry(root, width=50)
entry_name.pack(pady=5)

tk.Label(root, text="Email *", bg="#f9f9f9").pack()
entry_email = tk.Entry(root, width=50)
entry_email.pack(pady=5)

tk.Label(root, text="Phone *", bg="#f9f9f9").pack()
entry_phone = tk.Entry(root, width=50)
entry_phone.pack(pady=5)

tk.Label(root, text="Education", bg="#f9f9f9").pack()
entry_education = tk.Text(root, height=4, width=50)
entry_education.pack(pady=5)

tk.Label(root, text="Skills", bg="#f9f9f9").pack()
entry_skills = tk.Text(root, height=4, width=50)
entry_skills.pack(pady=5)

tk.Label(root, text="Experience", bg="#f9f9f9").pack()
entry_experience = tk.Text(root, height=4, width=50)
entry_experience.pack(pady=5)

# Color Template Selector
tk.Label(root, text="Choose Template Color", bg="#f9f9f9", font=("Arial", 10, "bold")).pack(pady=5)
color_var = tk.StringVar(value="Blue")
tk.OptionMenu(root, color_var, "Blue", "Green", "Gray").pack(pady=5)

tk.Button(root, text="Generate Stylish Resume", bg="#0078D7", fg="white",
          font=("Arial", 12, "bold"), command=generate_pdf).pack(pady=20)

root.mainloop()
