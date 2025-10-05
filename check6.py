import tkinter as tk
from tkinter import messagebox, filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib import colors
import textwrap
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle

import os


def generate_pdf():
    name = entry_name.get()
    title = entry_title.get()
    email = entry_email.get()
    phone = entry_phone.get()
    linkedin = entry_linkedin.get()
    objective = entry_objective.get("1.0", tk.END).strip()
    education = entry_education.get("1.0", tk.END).strip()
    experience = entry_experience.get("1.0", tk.END).strip()

    skills = entry_skills.get("1.0", tk.END).strip()
    projects = entry_projects.get("1.0", tk.END).strip()
    achievements = entry_achievements.get("1.0", tk.END).strip()
    color_choice = color_var.get()
    style_choice = style_var.get()

    if not name or not email or not phone:
        messagebox.showerror("Error", "Please fill all required fields!")
        return

    file_name = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        initialfile=name.replace(" ", "_") + "_Resume.pdf"
    )
    if not file_name:
        return

    # ================= STYLE SETTINGS ================= #
    if style_choice == "Modern Blue":
        theme_color = colors.HexColor("#007ACC")
        header_height = 90
        header_font = "Helvetica-Bold"
        layout_type = "topbar"
    elif style_choice == "Minimalist Gray":
        theme_color = colors.HexColor("#444444")
        header_height = 60
        header_font = "Times-Bold"
        layout_type = "simple"
    elif style_choice == "Bold Gold":
        theme_color = colors.HexColor("#DAA520")
        header_height = 120
        header_font = "Helvetica-Bold"
        layout_type = "sidebar"

    else:
        theme_color = colors.HexColor("#007ACC")
        layout_type = "topbar"

    c = pdf_canvas.Canvas(file_name, pagesize=letter)
    width, height = letter
    y = height - 100


    if style_choice == "Bold Gold":
    # Sidebar layout (Gold)
        sidebar_width = 180
        c.setFillColor(theme_color)
        c.rect(0, 0, sidebar_width, height, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont(header_font, 20)
        c.drawString(25, height - 60, name)
        c.setFont("Helvetica", 12)
        c.drawString(25, height - 80, title)
        c.setFont("Helvetica", 9)
        c.drawString(25, height - 110, f"Email: {email}")
        c.drawString(25, height - 125, f"Phone: {phone}")
        if linkedin:
            c.drawString(25, height - 140, f"LinkedIn:")
            c.drawString(25, height - 152, linkedin)

        # === Paragraph wrapping for right content ===
        content_style = ParagraphStyle(
            name="ContentStyle",
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            textColor=colors.black,
        )

        frame_x = 200
        frame_y = 50
        frame_width = 370
        frame_height = 700

        story = []
        story.append(Paragraph(f"<b>Objective</b><br/>{objective}", content_style))
        story.append(Paragraph(f"<b>Education</b><br/>{education}", content_style))
        story.append(Paragraph(f"<b>Experience</b><br/>{experience}", content_style))
        story.append(Paragraph(f"<b>Skills</b><br/>{skills}", content_style))
        story.append(Paragraph(f"<b>Projects</b><br/>{projects}", content_style))
        story.append(Paragraph(f"<b>Achievements</b><br/>{achievements}", content_style))

        frame = Frame(frame_x, frame_y, frame_width, frame_height, showBoundary=0)
        frame.addFromList(story, c)


    # ================= DRAW HEADER ================= #
    if layout_type == "topbar":
        c.setFillColor(theme_color)
        c.rect(0, height - header_height, width, header_height, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont(header_font, 24)
        c.drawString(50, height - 55, name)
        c.setFont("Helvetica", 14)
        c.drawString(50, height - 75, title)
        c.setFont("Helvetica", 10)
        c.drawRightString(width - 50, height - 55, f"Email: {email}")
        c.drawRightString(width - 50, height - 70, f"Phone: {phone}")
        if linkedin:
            c.drawRightString(width - 50, height - 85, f"LinkedIn: {linkedin}")
        y = height - 130

    elif layout_type == "simple":
        c.setFillColor(theme_color)
        c.setFont(header_font, 26)
        c.drawString(50, height - 80, name)
        c.setFont("Helvetica", 14)
        c.setFillColor(colors.black)
        c.drawString(50, height - 100, title)
        c.setFont("Helvetica", 10)
        c.drawRightString(width - 50, height - 80, f"Email: {email}")
        c.drawRightString(width - 50, height - 95, f"Phone: {phone}")
        if linkedin:
            c.drawRightString(width - 50, height - 110, f"LinkedIn: {linkedin}")
        y = height - 150

    # elif layout_type == "sidebar":
    #     # Sidebar layout
    #     sidebar_width = 180
    #     c.setFillColor(theme_color)
    #     c.rect(0, 0, sidebar_width, height, fill=1, stroke=0)
    #     c.setFillColor(colors.white)
    #     c.setFont(header_font, 20)
    #     c.drawString(25, height - 60, name)
    #     c.setFont("Helvetica", 12)
    #     c.drawString(25, height - 80, title)
    #     c.setFont("Helvetica", 9)
    #     c.drawString(25, height - 110, f"Email: {email}")
    #     c.drawString(25, height - 125, f"Phone: {phone}")
    #     if linkedin:
    #         c.drawString(25, height - 140, f"LinkedIn:")
    #         c.drawString(25, height - 152, linkedin)
    #     y = height - 100
    #     left_margin = sidebar_width + 30
    else:
        left_margin = 70

    # =============== TEXT WRAP HELPER =============== #
    def section(title, content, max_width=80):
        nonlocal y
        if not content.strip():
            return

        if y < 100:  # start new page if needed
            c.showPage()
            y = height - 100

        c.setFillColor(theme_color)
        c.setFont("Helvetica-Bold", 14)

        if layout_type == "sidebar":
            c.drawString(left_margin, y, title)
        else:
            c.drawString(50, y, title)

        y -= 15
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 11)
        text = c.beginText(left_margin if layout_type == "sidebar" else 70, y)

        for line in content.split("\n"):
            if line.strip():
                wrapped_lines = textwrap.wrap(line.strip(), width=max_width)
                for wline in wrapped_lines:
                    text.textLine("• " + wline)
                    y -= 14
        c.drawText(text)
        y -= 10

    # =============== OBJECTIVE SECTION =============== #
    if style_choice != "Bold Gold":
        if objective:
            c.setFillColor(theme_color)
            c.setFont("Helvetica-Bold", 14)
            if layout_type == "sidebar":
                c.drawString(left_margin, y, "Objective")
            else:
                c.drawString(50, y, "Objective")
            y -= 18
            c.setFillColor(colors.black)
            c.setFont("Helvetica", 11)
            text = c.beginText(left_margin if layout_type == "sidebar" else 70, y)
            for line in objective.split("\n"):
                wrapped_lines = textwrap.wrap(line, width=100)
                for wline in wrapped_lines:
                    text.textLine(wline)
                    y -= 14
            c.drawText(text)
            y -= 10

    # =============== OTHER SECTIONS =============== #
    if style_choice != "Bold Gold":
        section("Education", education)
        section("Experience", experience) 
        section("Skills", skills)
        section("Projects", projects)
        section("Achievements", achievements)

    # =============== FOOTER =============== #
    c.setStrokeColor(theme_color)
    c.line(50, 50, width - 50, 50)
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(50, 35, f"Generated by Resume Builder Pro | Style: {style_choice}")

    c.save()
    messagebox.showinfo("Success", f"Your professional resume has been generated:\n{file_name}")


# =============== TKINTER UI =============== #
root = tk.Tk()
root.title("Professional Resume Builder")
root.geometry("800x700")
root.config(bg="#f9f9f9")

canvas_frame = tk.Canvas(root, bg="#f9f9f9")
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas_frame.yview)
scrollable_frame = tk.Frame(canvas_frame, bg="#f9f9f9")

scrollable_frame.bind("<Configure>", lambda e: canvas_frame.configure(scrollregion=canvas_frame.bbox("all")))
canvas_frame.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas_frame.configure(yscrollcommand=scrollbar.set)
canvas_frame.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

root = scrollable_frame

# ===== UI ELEMENTS ===== #
def label(text):
    tk.Label(root, text=text, bg="#f9f9f9", font=("Arial", 10, "bold")).pack(anchor="w", padx=20, pady=2)

def textbox(height=3):
    box = tk.Text(root, height=height, width=70)
    box.pack(pady=3)
    return box

label("Full Name *")
entry_name = tk.Entry(root, width=70); entry_name.pack()

label("Job Title (e.g., Software Engineer)")
entry_title = tk.Entry(root, width=70); entry_title.pack()

label("Email *")
entry_email = tk.Entry(root, width=70); entry_email.pack()

label("Phone *")
entry_phone = tk.Entry(root, width=70); entry_phone.pack()

label("LinkedIn (optional)")
entry_linkedin = tk.Entry(root, width=70); entry_linkedin.pack()

label("Objective")
entry_objective = textbox(4)

label("Education")
entry_education = textbox(4)

label("Experience")
entry_experience = textbox(4)


label("Skills (each skill in new line)")
entry_skills = textbox(4)

label("Projects")
entry_projects = textbox(4)

label("Achievements")
entry_achievements = textbox(4)

label("Choose Template Theme")
color_var = tk.StringVar(value="Blue")
tk.OptionMenu(root, color_var, "Blue", "Teal", "Gray", "Gold").pack(pady=5)

label("Choose Resume Style")
style_var = tk.StringVar(value="Modern Blue")
tk.OptionMenu(root, style_var, "Modern Blue", "Minimalist Gray", "Bold Gold").pack(pady=5)

tk.Button(root, text="Generate Professional Resume", bg="#007ACC", fg="white",
          font=("Arial", 12, "bold"), command=generate_pdf).pack(pady=20)

# Allow mousewheel scrolling
def _on_mousewheel(event):
    canvas_frame.yview_scroll(int(-1*(event.delta/120)), "units")

canvas_frame.bind_all("<MouseWheel>", _on_mousewheel)

root.mainloop()
