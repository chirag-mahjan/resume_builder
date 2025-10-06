import tkinter as tk
from tkinter import messagebox, filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib import colors
import textwrap
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
import tempfile
import webbrowser



import os
import json
root = tk.Tk()


def save_settings():
    data = {
        "name": entry_name.get(),
        "title": entry_title.get(),
        "email": entry_email.get(),
        "phone": entry_phone.get()
    }
    with open("resume_data.json", "w") as f:
        json.dump(data, f)

def load_settings():
    if os.path.exists("resume_data.json"):
        with open("resume_data.json") as f:
            data = json.load(f)
            entry_name.insert(0, data.get("name", ""))
            entry_title.insert(0, data.get("title", ""))
            entry_email.insert(0, data.get("email", ""))
            entry_phone.insert(0, data.get("phone", ""))



def generate_pdf(preview_mode=False):
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
    # === Color and Theme Setup ===
    color_map = {
        "Blue": "#007ACC",
        "Teal": "#008B8B",
        "Gray": "#444444",
        "Gold": "#DAA520"
    }
    theme_color = colors.HexColor(color_map.get(color_choice, "#007ACC"))

    style_choice = style_var.get()

    if not name or not email or not phone:
        messagebox.showerror("Error", "Please fill all required fields!")
        return

    if not preview_mode:
        file_name = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=name.replace(" ", "_") + "_Resume.pdf"
        )
        if not file_name:
            return
    else:
        file_name = preview_mode  # passed from preview function

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
    # === Add Profile Photo (Optional) ===
    global photo_path
    if photo_path:
        try:
            c.drawImage(photo_path, 50, height - 130, width=80, height=80, mask='auto')
        except Exception:
            messagebox.showwarning("Image Error", "Couldn't add photo. Try smaller image or .jpg format.")

    


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
        # === Add Custom Sections ===
        for sec_name, box in custom_sections:
            content = box.get("1.0", tk.END).strip()
            if content:
                section(sec_name, content)


    # =============== FOOTER =============== #
    c.setStrokeColor(theme_color)
    c.line(50, 50, width - 50, 50)
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(50, 35, f"Generated by Resume Builder Pro | Style: {style_choice}")

    c.save()
    messagebox.showinfo("Success", f"Your professional resume has been generated:\n{file_name}")


def _generate_pdf_internal(file_path, preview_mode=False):
    """Internal helper to reuse generate_pdf() for preview"""
    global preview_mode_flag
    preview_mode_flag = preview_mode
    generate_pdf(preview_mode=file_path)


def preview_pdf():
    """Generate a temporary preview of the resume"""
    import tempfile
    import webbrowser

    # Save to a temporary file
    temp_file = os.path.join(tempfile.gettempdir(), "resume_preview.pdf")

    # Temporarily ask the main function to use this path
    name = entry_name.get()
    if not name.strip():
        messagebox.showerror("Error", "Please enter your name before previewing.")
        return

    # Use same generation logic, but skip dialog
    color_choice = color_var.get()
    style_choice = style_var.get()

    # Generate PDF silently with existing function
    # We'll reuse generate_pdf but modify it slightly below 👇
    _generate_pdf_internal(temp_file, preview_mode=True)

    # Open the PDF file for preview
    webbrowser.open(temp_file)



# =============== TKINTER UI =============== #
# =============== MAIN APP =============== #
def open_resume_builder():
    """Show the resume builder UI"""
    for widget in root.winfo_children():
        widget.destroy()  # clear main menu

    root.title("Professional Resume Builder")
    root.config(bg="#f9f9f9")
    global canvas_frame
    canvas_frame = tk.Canvas(root, bg="#f9f9f9")
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas_frame.yview)
    canvas_frame.bind_all("<MouseWheel>", _on_mousewheel)

    scrollable_frame = tk.Frame(canvas_frame, bg="#f9f9f9")

    scrollable_frame.bind("<Configure>", lambda e: canvas_frame.configure(scrollregion=canvas_frame.bbox("all")))
    canvas_frame.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas_frame.configure(yscrollcommand=scrollbar.set)
    canvas_frame.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    builder_root = scrollable_frame  # reuse existing widgets under this frame

    # ===== UI ELEMENTS ===== #
    def label(text):
        tk.Label(builder_root, text=text, bg="#f9f9f9", font=("Arial", 10, "bold")).pack(anchor="w", padx=20, pady=2)

    def textbox(height=3):
        box = tk.Text(builder_root, height=height, width=70)
        box.pack(pady=3)
        return box

    # === all your existing input fields (copy from your code here) ===
    global entry_name, entry_title, entry_email, entry_phone, entry_linkedin
    global entry_objective, entry_education, entry_experience
    global entry_skills, entry_projects, entry_achievements
    global color_var, style_var, custom_sections, photo_path

    label("Full Name *")
    entry_name = tk.Entry(builder_root, width=70); entry_name.pack()

    label("Job Title (e.g., Software Engineer)")
    entry_title = tk.Entry(builder_root, width=70); entry_title.pack()

    label("Email *")
    entry_email = tk.Entry(builder_root, width=70); entry_email.pack()

    label("Phone *")
    entry_phone = tk.Entry(builder_root, width=70); entry_phone.pack()

    # ========== PHOTO UPLOAD ==========
    photo_path = None
    def choose_photo():
        global photo_path
        photo_path = filedialog.askopenfilename(
            title="Choose Profile Photo",
            filetypes=[("Image files", "*.jpg;*.png;*.jpeg")]
        )
        if photo_path:
            messagebox.showinfo("Photo Added", "Profile photo selected successfully!")

    tk.Button(builder_root, text="Add Profile Photo", command=choose_photo, bg="#007ACC", fg="white").pack(pady=4)

    label("LinkedIn (optional)")
    entry_linkedin = tk.Entry(builder_root, width=70); entry_linkedin.pack()

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
    tk.OptionMenu(builder_root, color_var, "Blue", "Teal", "Gray", "Gold").pack(pady=5)

    label("Choose Resume Style")
    style_var = tk.StringVar(value="Modern Blue")
    tk.OptionMenu(builder_root, style_var, "Modern Blue", "Minimalist Gray", "Bold Gold").pack(pady=5)

    tk.Button(builder_root, text="Generate Professional Resume", bg="#007ACC", fg="white",
              font=("Arial", 12, "bold"), command=generate_pdf).pack(pady=20)

    tk.Button(builder_root, text="👁 Preview Resume", bg="#005fa3", fg="white",
              font=("Arial", 11, "bold"), command=preview_pdf).pack(pady=5)

    tk.Button(builder_root, text="💾 Save Info", command=save_settings, bg="#444", fg="white").pack(pady=3)

    custom_sections = []
    def add_section():
        sec_name = tk.simpledialog.askstring("New Section", "Enter section name:")
        if sec_name:
            lbl = tk.Label(builder_root, text=sec_name, font=("Arial", 10, "bold"), bg="#f9f9f9")
            lbl.pack(anchor="w", padx=20)
            box = tk.Text(builder_root, width=70, height=3, wrap="word")
            box.pack(pady=3)
            custom_sections.append((sec_name, box))

    tk.Button(builder_root, text="➕ Add Custom Section", command=add_section, bg="#444", fg="white").pack(pady=4)

    load_settings()


def open_ats_checker():
    """Simple ATS score calculator"""
    for widget in root.winfo_children():
        widget.destroy()  # clear main menu

    label = tk.Label(root, text="Upload your resume PDF to check ATS score", font=("Arial", 14, "bold"))
    label.pack(pady=30)

    def check_score():
        file_path = filedialog.askopenfilename(
            title="Select Resume PDF",
            filetypes=[("PDF files", "*.pdf")]
        )
        if not file_path:
            return

        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(file_path)
            text = "\n".join([page.extract_text() or "" for page in reader.pages])
        except Exception:
            messagebox.showerror("Error", "Could not read PDF. Please upload a valid file.")
            return

        # === Simple ATS Scoring Logic ===
        score = 0
        total = 7
        checks = {
            "Name": bool(text.strip()),
            "Email": "@" in text,
            "Phone": any(ch.isdigit() for ch in text),
            "Skills": "skill" in text.lower(),
            "Experience": "experience" in text.lower(),
            "Education": "education" in text.lower(),
            "Projects": "project" in text.lower(),
        }
        score = sum(checks.values())
        percent = int((score / total) * 100)

        messagebox.showinfo("ATS Score", f"✅ Your ATS Compatibility Score: {percent}%")

    tk.Button(root, text="📄 Upload Resume", command=check_score, bg="#007ACC", fg="white",
              font=("Arial", 12, "bold")).pack(pady=20)

    tk.Button(root, text="⬅ Back", command=show_main_menu, bg="#444", fg="white").pack(pady=10)
def show_main_menu():
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Resume Builder App")
    tk.Label(root, text="Welcome!", font=("Arial", 20, "bold")).pack(pady=30)
    tk.Label(root, text="What would you like to do?", font=("Arial", 12)).pack(pady=10)

    tk.Button(root, text="🧾 Build Your Resume", command=open_resume_builder,
              bg="#007ACC", fg="white", font=("Arial", 13, "bold"), width=25).pack(pady=15)

    tk.Button(root, text="📊 Check ATS Score", command=open_ats_checker,
              bg="#005fa3", fg="white", font=("Arial", 13, "bold"), width=25).pack(pady=15)

# Allow mousewheel scrolling
def _on_mousewheel(event):
    canvas_frame.yview_scroll(int(-1*(event.delta/120)), "units")


def on_enter(e): e.widget.config(bg="#005fa3")
def on_leave(e): e.widget.config(bg="#007ACC")

for btn in root.winfo_children():
    if isinstance(btn, tk.Button):
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

if __name__ == "__main__":
    show_main_menu()
    root.mainloop()

