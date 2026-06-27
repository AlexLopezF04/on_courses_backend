import xml.etree.ElementTree as ET
from xml.dom import minidom

def create_svg():
    modules = [
        ("Usuarios", "#E3F2FD", "#1565C0", [
            "User", "StudentProfile", "ProfessorProfile", "AccessLog"
        ]),
        ("Cursos", "#E8F5E9", "#2E7D32", [
            "Category", "Course", "Module", "Lesson", "Resource"
        ]),
        ("Comunidad", "#FFF3E0", "#E65100", [
            "ForumThread", "ForumPost", "Announcement", "LessonComment"
        ]),
        ("Progreso", "#F3E5F5", "#6A1B9A", [
            "Enrollment", "LessonProgress", "QuestionBank",
            "QuestionOption", "Exam", "ExamQuestion",
            "ExamAttempt", "AttemptAnswer", "Certificate"
        ]),
        ("Gamificaci\u00f3n", "#FCE4EC", "#C62828", [
            "Achievement", "UserAchievement", "Review"
        ]),
        ("Comercial", "#E0F7FA", "#00695C", [
            "Cart", "CartItem", "Coupon", "Order",
            "OrderItem", "SupportTicket", "SupportMessage"
        ]),
    ]

    WIDTH, HEIGHT = 1200, 900
    module_w, module_h = 540, 240
    start_x, start_y = 40, 60
    cols = 2
    gap_x, gap_y = 40, 30
    font_family = "monospace, 'Courier New', sans-serif"

    svg = ET.Element("svg", xmlns="http://www.w3.org/2000/svg",
                     width=str(WIDTH), height=str(HEIGHT),
                     viewBox=f"0 0 {WIDTH} {HEIGHT}")
    svg.append(ET.Comment(" ER Diagram - OnCourses Database "))

    # Background
    bg = ET.SubElement(svg, "rect", width="100%", height="100%", fill="#FAFAFA")

    # Title
    title = ET.SubElement(svg, "text", x="600", y="35",
                          **{"text-anchor": "middle", "font-size": "24",
                             "font-weight": "bold", "font-family": font_family,
                             "fill": "#333"})
    title.text = "OnCourses - Diagrama Entidad-Relaci\u00f3n (32 tablas)"

    # Module boxes
    positions = {}
    current_y = {}
    module_boxes = []

    for idx, (name, bg_color, border_color, tables) in enumerate(modules):
        col = idx % cols
        row = idx // cols
        x = start_x + col * (module_w + gap_x)

        max_tables = 9
        table_h = 26
        header_h = 36
        padding = 10
        h = header_h + padding + len(tables) * table_h + padding + 10
        y = start_y + row * (module_h + gap_y)

        # Adjust height for large modules
        if len(tables) > 6:
            h = header_h + padding + len(tables) * table_h + padding + 10

        module_boxes.append((x, y, module_w, h, bg_color, border_color, name, tables, col, row))
        current_y[name] = y + h

    # Calculate total height
    max_y = max(y + h for x, y, w, h, bg, bc, name, tables, col, row in module_boxes)
    svg.set("height", str(max_y + 40))
    svg.set("viewBox", f"0 0 {WIDTH} {max_y + 40}")

    # Draw module boxes and tables
    for x, y, w, h, bg_color, border_color, name, tables, col, row in module_boxes:
        # Module background
        rect = ET.SubElement(svg, "rect", x=str(x), y=str(y),
                             width=str(w), height=str(h),
                             rx="10", ry="10",
                             fill=bg_color, stroke=border_color,
                             **{"stroke-width": "2"})

        # Module header
        ET.SubElement(svg, "rect", x=str(x), y=str(y),
                      width=str(w), height="36", rx="10", ry="10",
                      fill=border_color)

        # Cover top corners
        ET.SubElement(svg, "rect", x=str(x), y=str(y + 20),
                      width=str(w), height="16",
                      fill=border_color)

        # Module name
        t = ET.SubElement(svg, "text", x=str(x + w/2), y=str(y + 24),
                          **{"text-anchor": "middle", "font-size": "14",
                             "font-weight": "bold", "font-family": font_family,
                             "fill": "#FFF"})
        t.text = f"{name} ({len(tables)} tablas)"

        # Table entries
        for i, table in enumerate(tables):
            ty = y + 46 + i * 26
            # Even/odd rows
            if i % 2 == 0:
                ET.SubElement(svg, "rect", x=str(x + 10), y=str(ty),
                              width=str(w - 20), height="24", rx="4", ry="4",
                              fill="#FFFFFF", fill_opacity="0.6")
            t = ET.SubElement(svg, "text", x=str(x + 20), y=str(ty + 16),
                              **{"font-size": "12", "font-family": font_family,
                                 "fill": "#333"})
            t.text = f"\u25c6  {table}"

    # Relationship lines between module boxes
    # Usuarios -> Cursos
    ux, uy, _, uh, _, _, _, _, _, _ = module_boxes[0]
    cx, cy, _, ch, _, _, _, _, _, _ = module_boxes[1]
    # User -> Enrollment
    px, py, _, ph, _, _, _, _, _, _ = module_boxes[3]
    # Cursos -> Progreso
    # Usuarios -> Comercial
    cmx, cmy, _, cmh, _, _, _, _, _, _ = module_boxes[5]

    # Draw cross-module relationship arrows
    def add_arrow(x1, y1, x2, y2, label=""):
        line = ET.SubElement(svg, "line", x1=str(x1), y1=str(y1),
                             x2=str(x2), y2=str(y2),
                             stroke="#666", **{"stroke-width": "1.5",
                                               "stroke-dasharray": "6,3"})
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - 8
            t = ET.SubElement(svg, "text", x=str(mx), y=str(my),
                              **{"text-anchor": "middle", "font-size": "10",
                                 "font-family": font_family, "fill": "#666",
                                 "font-style": "italic"})
            t.text = label

    # User -> Courses (professor)
    add_arrow(ux + module_w, uy + 100, cx, cy + 100, "profesor dicta")

    # User -> Progreso (enrollment)
    add_arrow(ux + module_w, uy + 160, px, py + 40, "se inscribe")

    # Courses -> Progreso
    add_arrow(cx + module_w, cy + 120, px, py + 120, "evaluaci\u00f3n")

    # User -> Comercial
    add_arrow(ux + module_w, uy + 200, cmx, cmy + 60, "compra")

    # Community (module 2, col 1)
    # Courses -> Community
    comx, comy, _, comh, _, _, _, _, _, _ = module_boxes[2]
    add_arrow(cx + module_w, cy + 180, comx, comy + 40, "foros")

    return svg

def prettify(elem):
    rough = ET.tostring(elem, encoding="unicode")
    return minidom.parseString(rough.encode()).toprettyxml(indent="  ")

if __name__ == "__main__":
    svg = create_svg()
    output = prettify(svg)
    with open("docs/er-diagram.svg", "w", encoding="utf-8") as f:
        f.write(output)
    print("Diagrama generado: docs/er-diagram.svg")
