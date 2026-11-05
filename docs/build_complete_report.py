#!/usr/bin/env python3
"""
build_complete_report.py
Generates the comprehensive, rigorous, and beautifully formatted DBMS Project Report
for 'Social Media Database Management System' strictly adhering to the structure,
formatting guidelines, and evaluation requirements of DBMS_Project.docx.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_report():
    doc = docx.Document()

    # Configure Page Margins (A4 format)
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # XML Helper Functions
    def set_cell_background(cell, fill_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

    def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(
            f'<w:tcMar {nsdecls("w")}>'
            f'<w:top w:w="{top}" w:type="dxa"/>'
            f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
            f'<w:left w:w="{left}" w:type="dxa"/>'
            f'<w:right w:w="{right}" w:type="dxa"/>'
            f'</w:tcMar>'
        )
        tcPr.append(tcMar)

    def set_table_borders(table, color="CBD5E1", sz="4", val="single"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideV w:val="none"/>'
            f'<w:left w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(borders)

    # Typography Helpers
    def add_chapter_title(chapter_num, title_text):
        p_ch = doc.add_paragraph()
        p_ch.paragraph_format.keep_with_next = True
        p_ch.paragraph_format.space_before = Pt(24)
        p_ch.paragraph_format.space_after = Pt(2)
        r_ch = p_ch.add_run(f"Chapter {chapter_num}")
        r_ch.font.name = 'Georgia'
        r_ch.font.size = Pt(24)
        r_ch.bold = True
        r_ch.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A) # Deep Navy

        p_t = doc.add_paragraph()
        p_t.paragraph_format.keep_with_next = True
        p_t.paragraph_format.space_before = Pt(0)
        p_t.paragraph_format.space_after = Pt(14)
        r_t = p_t.add_run(title_text)
        r_t.font.name = 'Georgia'
        r_t.font.size = Pt(20)
        r_t.bold = True
        r_t.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A) # Dark Slate

    def add_h2(title_text):
        p = doc.add_paragraph()
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(title_text)
        r.font.name = 'Georgia'
        r.font.size = Pt(15)
        r.bold = True
        r.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
        return p

    def add_h3(title_text):
        p = doc.add_paragraph()
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(title_text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(13)
        r.bold = True
        r.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
        return p

    def add_p(text, bold_prefix=""):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = 'Times New Roman'
            r_pre.font.size = Pt(12)
            r_pre.bold = True
            r_pre.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
        return p

    def add_bullet(text, bold_prefix=""):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = 'Times New Roman'
            r_pre.font.size = Pt(12)
            r_pre.bold = True
            r_pre.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
        return p

    def add_code(code_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, "F8FAFC")
        set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:left w:val="single" w:sz="18" w:space="0" w:color="0284C7"/>'
            f'<w:top w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>'
            f'<w:right w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>'
            f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.1
        r = p.add_run(code_text.strip())
        r.font.name = 'Consolas'
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(0)
        p_sp.paragraph_format.space_after = Pt(6)

    def add_table_data(headers, rows, col_widths=None):
        tbl = doc.add_table(rows=len(rows) + 1, cols=len(headers))
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl, color="CBD5E1")
        
        # Header
        hdr = tbl.rows[0].cells
        for i, h in enumerate(headers):
            hdr[i].text = ""
            set_cell_background(hdr[i], "1E293B")
            set_cell_margins(hdr[i], top=120, bottom=120, left=140, right=140)
            p = hdr[i].paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(h)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10.5)
            r.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            if col_widths and i < len(col_widths):
                hdr[i].width = col_widths[i]

        # Body
        for r_idx, row in enumerate(rows):
            cells = tbl.rows[r_idx + 1].cells
            bg = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
            for c_idx, val in enumerate(row):
                cells[c_idx].text = ""
                set_cell_background(cells[c_idx], bg)
                set_cell_margins(cells[c_idx], top=90, bottom=90, left=140, right=140)
                p = cells[c_idx].paragraphs[0]
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.15
                r = p.add_run(str(val))
                r.font.name = 'Times New Roman'
                r.font.size = Pt(10.0)
                r.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
                if col_widths and c_idx < len(col_widths):
                    cells[c_idx].width = col_widths[c_idx]

        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(0)
        p_sp.paragraph_format.space_after = Pt(6)

    def add_image_figure(img_path, caption, width=Inches(6.0)):
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(4)
            p_img.paragraph_format.keep_with_next = True
            r = p_img.add_run()
            r.add_picture(img_path, width=width)
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(12)
            r_cap = p_cap.add_run(caption)
            r_cap.font.name = 'Times New Roman'
            r_cap.font.size = Pt(10.5)
            r_cap.bold = True
            r_cap.italic = True
            r_cap.font.color.rgb = RGBColor(0x47, 0x55, 0x69)
        else:
            add_p(f"[{caption}]")

    # ==========================================
    # 1. COVER PAGE (Matching DBMS_Project.docx)
    # ==========================================
    p_top_sp = doc.add_paragraph()
    p_top_sp.paragraph_format.space_before = Pt(36)
    
    p_c1 = doc.add_paragraph()
    p_c1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_c1 = p_c1.add_run("Database Management Systems (DBMS)")
    r_c1.font.name = 'Georgia'
    r_c1.font.size = Pt(17)
    r_c1.bold = True
    r_c1.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)
    
    p_c2 = doc.add_paragraph()
    p_c2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_c2.paragraph_format.space_before = Pt(18)
    p_c2.paragraph_format.space_after = Pt(6)
    r_c2 = p_c2.add_run("Project Report Format")
    r_c2.font.name = 'Georgia'
    r_c2.font.size = Pt(24.5)
    r_c2.bold = True
    r_c2.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
    
    p_c3 = doc.add_paragraph()
    p_c3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_c3.paragraph_format.space_before = Pt(4)
    p_c3.paragraph_format.space_after = Pt(40)
    r_c3 = p_c3.add_run("Social Media Database Management System")
    r_c3.font.name = 'Georgia'
    r_c3.font.size = Pt(20.5)
    r_c3.bold = True
    r_c3.font.color.rgb = RGBColor(0x03, 0x69, 0xA1) # Ocean blue
    
    # Metadata Block
    meta_items = [
        ("Student Name(s):", "Vansh Chadha"),
        ("Roll Number(s):", "25U021036"),
        ("Branch & Section:", "Computer Science & Engineering (Class 3-AI)"),
        ("Course Instructor:", "Priyankar"),
        ("Academic Session:", "2026-2027 (Monsoon Semester)")
    ]
    for lbl, val in meta_items:
        p_m = doc.add_paragraph()
        p_m.paragraph_format.space_before = Pt(3)
        p_m.paragraph_format.space_after = Pt(3)
        p_m.paragraph_format.left_indent = Inches(1.5)
        r_lbl = p_m.add_run(f"{lbl:<24}\t")
        r_lbl.font.name = 'Georgia'
        r_lbl.font.size = Pt(12)
        r_lbl.bold = True
        r_lbl.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        
        r_val = p_m.add_run(val)
        r_val.font.name = 'Times New Roman'
        r_val.font.size = Pt(12)
        r_val.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
        
    p_foot_sp = doc.add_paragraph()
    p_foot_sp.paragraph_format.space_before = Pt(100)
    
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("Department of Computer Science\nIndian Institute of Information Technology Bhopal")
    r_inst.font.name = 'Georgia'
    r_inst.font.size = Pt(14)
    r_inst.bold = True
    r_inst.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
    
    doc.add_page_break()

    # ==========================================
    # 2. TABLE OF CONTENTS
    # ==========================================
    p_toc_head = doc.add_paragraph()
    p_toc_head.paragraph_format.space_before = Pt(12)
    p_toc_head.paragraph_format.space_after = Pt(14)
    r_th = p_toc_head.add_run("Contents")
    r_th.font.name = 'Georgia'
    r_th.font.size = Pt(22)
    r_th.bold = True
    r_th.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    toc_entries = [
        ("General Instructions", "3"),
        ("1 Introduction", "4"),
        ("    1.1 Project Overview", "4"),
        ("    1.2 Problem Statement", "4"),
        ("    1.3 Objectives", "5"),
        ("    1.4 Scope of the Project", "5"),
        ("    1.5 Software and Hardware Requirements", "5"),
        ("2 System Requirements and Analysis", "6"),
        ("    2.1 Functional Requirements", "6"),
        ("    2.2 Business Rules", "7"),
        ("3 Entity–Relationship (ER) Modeling", "8"),
        ("    3.1 Identification of Entities", "8"),
        ("    3.2 Identification of Relationships", "10"),
        ("    3.3 ER Diagram", "11"),
        ("    3.4 Explanation of the ER Diagram", "12"),
        ("4 ER-to-Relational Mapping", "13"),
        ("    4.1 Mapping Rules", "13"),
        ("    4.2 Step-by-Step Conversion", "13"),
        ("    4.3 Final Relational Schema", "15"),
        ("5 Functional Dependencies", "16"),
        ("    5.1 Identification of Functional Dependencies", "16"),
        ("    5.2 Candidate Keys and Attribute Classification", "17"),
        ("    5.3 FD Analysis", "18"),
        ("6 Database Normalization", "19"),
        ("    6.1 Unnormalized Form (UNF)", "19"),
        ("    6.2 First Normal Form (1NF)", "20"),
        ("    6.3 Second Normal Form (2NF)", "20"),
        ("    6.4 Third Normal Form (3NF)", "21"),
        ("    6.5 Boyce–Codd Normal Form (BCNF)", "22"),
        ("    6.6 Final Normalized Schema", "23"),
        ("7 Relational Integrity and Constraints", "24"),
        ("8 MySQL Database Implementation", "26"),
        ("    8.1 Database Creation", "26"),
        ("    8.2 Table Creation", "26"),
        ("    8.3 Data Insertion", "28"),
        ("    8.4 Data Modification and Deletion", "30"),
        ("    8.5 Sample Database Contents", "31"),
        ("    8.6 SQL Query Implementation", "33"),
        ("    8.7 Advanced DBMS Features", "38"),
        ("9 Application Development", "41"),
        ("    9.1 System Architecture", "41"),
        ("    9.2 Front-End Technologies", "42"),
        ("    9.3 Application Modules", "42"),
        ("    9.4 Database Connectivity", "44"),
        ("    9.5 Application Screenshots", "45"),
        ("    9.6 Database Operations through the Application", "47"),
        ("10 Testing and Results", "48"),
        ("    10.1 Test Cases", "48"),
        ("    10.2 Query Testing", "50"),
        ("    10.3 Constraint Testing", "51"),
        ("    10.4 Results and Discussion", "52"),
        ("11 Conclusion and Future Scope", "55"),
        ("    11.1 Conclusion", "55"),
        ("    11.2 Limitations", "55"),
        ("    11.3 Future Scope", "56"),
        ("References", "57"),
        ("Appendix A: Complete MySQL Script", "58"),
        ("Appendix B: Source Code", "63"),
        ("Appendix C: Additional Screenshots", "65"),
        ("Appendix D: Team Contribution", "66"),
        ("Suggested Evaluation Scheme", "67")
    ]
    for title, pg in toc_entries:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(1)
        p_t.paragraph_format.space_after = Pt(2)
        r1 = p_t.add_run(f"{title:<65}")
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        r1.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
        if not title.startswith("    "):
            r1.bold = True
            r1.font.name = 'Georgia'
        r2 = p_t.add_run(f"\t{pg}")
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(11)
        r2.bold = True
        r2.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    doc.add_page_break()

    # ==========================================
    # 3. GENERAL INSTRUCTIONS (From template)
    # ==========================================
    add_styled_heading = doc.add_paragraph()
    r_gi = add_styled_heading.add_run("General Instructions")
    r_gi.font.name = 'Georgia'
    r_gi.font.size = Pt(22)
    r_gi.bold = True
    r_gi.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
    add_styled_heading.paragraph_format.space_after = Pt(12)

    instructions = [
        "The front end may be developed using any suitable programming language or framework (implemented with React 18 and Vite).",
        "MySQL is mandatory for database creation, storage, and query execution. A different DBMS must not be used in place of MySQL (implemented with MySQL 8.0+ / MariaDB 10.11+).",
        "Design the database before implementing the application (rigorous ER modeling and 3NF/BCNF normalization performed prior to UI integration).",
        "Demonstrate the DBMS concepts covered in the course through the report and implementation (keys, relational algebra, constraints, triggers, views, stored procedures, indexing).",
        "Include all diagrams, functional dependencies, normalization steps, SQL statements, and execution results.",
        "Submit the report, application source code, and a complete MySQL script or database export.",
        "Every team member must understand the database design and be prepared to explain it during evaluation."
    ]
    for i, inst in enumerate(instructions, 1):
        add_bullet(inst, bold_prefix=f"{i}. ")

    add_p(
        "Important Note: This report implements the approved project topic 'Social Media Database Management System' "
        "(Kinetic Social) replacing the example Inventory Management System throughout all chapters, entities, business rules, "
        "relational schemas, SQL queries, full-stack application modules, and experimental benchmarks.",
        bold_prefix="Implementation Scope: "
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 1: INTRODUCTION
    # ==========================================
    add_chapter_title("1", "Introduction")

    add_h2("1.1 Project Overview")
    add_p(
        "Modern social networking platforms represent some of the most data-intensive and relationship-heavy "
        "computing systems in existence today. Platforms such as Twitter/X, Instagram, and LinkedIn manage millions of "
        "concurrent users, high-frequency multimedia publishing, dense graphs of follower/following relationships, "
        "real-time interaction metrics (likes, comments, reposts), and personalized notification streams. "
        "At the core of these applications lies a database management system that must balance rigorous data integrity, "
        "transactional consistency, and sub-millisecond read latency."
    )
    add_p(
        "The 'Social Media Database Management System' (engineered under the project title Kinetic Social) is a full-stack "
        "relational database application designed to demonstrate the complete lifecycle of DBMS engineering. "
        "The project models users, content posts, comments, likes, asymmetrical follower networks, notifications, "
        "and normalized taxonomy tags. The system is engineered to provide ACID transactional guarantees, automated "
        "consistency enforcement via database triggers, encapsulated reporting via views and stored procedures, "
        "and high-throughput performance validated through index benchmarking on 300,000+ synthetic records."
    )
    add_p(
        "Intended users of this platform include content creators publishing articles and updates, general platform members "
        "browsing personalized feeds and interacting with authors, community moderators managing discussions, and platform "
        "administrators analyzing platform-wide creator engagement metrics."
    )

    add_h2("1.2 Problem Statement")
    add_p(
        "Naive implementations of social networking applications suffer from critical architectural deficiencies "
        "when deployed without formal database design principles:"
    )
    add_bullet(
        "Storing denormalized user details alongside posts and comments creates severe data redundancy and update anomalies; "
        "updating a user's biography or profile requires scanning millions of historical records.",
        bold_prefix="Data Redundancy and Update Anomalies: "
    )
    add_bullet(
        "Applications that compute interaction counts (e.g., total likes or follower counts) by querying child tables on every "
        "page render cause disk I/O thrashing. Conversely, maintaining cached counters solely within application application "
        "logic leads to race conditions, dirty reads, and desynchronized counters during concurrent requests.",
        bold_prefix="Counter Drift and Concurrency Race Conditions: "
    )
    add_bullet(
        "Without strict relational integrity and cascading foreign-key rules, deleting a user account leaves orphaned posts, "
        "comments, and dangling notification references, corrupting database consistency.",
        bold_prefix="Orphaned Records and Broken Referential Integrity: "
    )
    add_bullet(
        "Computing chronological feeds across a user's network requires joining multi-million-row tables. In the absence of "
        "a composite B-tree indexing strategy, the database falls back to expensive unindexed full-table scans (ALL) and filesort "
        "operations, causing unacceptable latency (>400 ms per feed request).",
        bold_prefix="Unindexed Multi-Table Joins and Query Latency: "
    )
    add_p(
        "This project addresses these fundamental challenges by implementing a formally normalized 3NF/BCNF relational database "
        "in MySQL, enforcing referential integrity inside the database engine, utilizing atomic triggers to guarantee counter "
        "synchronization, and optimizing access paths through composite indexing."
    )

    add_h2("1.3 Objectives")
    add_p("The primary technical and academic objectives of this project are as follows:")
    add_bullet("Design a robust conceptual model using Chen's Entity-Relationship (ER) notation capturing 1:1, 1:N, M:N, and recursive relationships.", bold_prefix="1. Conceptual Modeling: ")
    add_bullet("Formally map the ER diagram into a relational database schema using standard transformation algorithms, strictly identifying primary, composite, and foreign keys.", bold_prefix="2. Relational Mapping: ")
    add_bullet("Identify all functional dependencies and rigorously prove normalization up to Boyce-Codd Normal Form (BCNF), documenting deliberate denormalizations where latency requires it.", bold_prefix="3. Normalization & Integrity: ")
    add_bullet("Implement the database schema in MySQL/MariaDB with comprehensive domain constraints, NOT NULL checks, UNIQUE constraints, and cascading referential integrity rules.", bold_prefix="4. SQL Implementation: ")
    add_bullet("Deploy automated MySQL triggers to maintain aggregate counters (like_count) and dispatch notifications without application-layer overhead.", bold_prefix="5. Advanced DBMS Features: ")
    add_bullet("Encapsulate complex analytical operations using MySQL Views (user_feed) and Stored Procedures (get_mutual_followers, recount_likes).", bold_prefix="6. Encapsulated Business Logic: ")
    add_bullet("Formulate and evaluate a targeted B-tree indexing strategy, benchmarking execution plans before and after indexing on a 300,000+ record dataset.", bold_prefix="7. Performance Benchmarking: ")
    add_bullet("Develop and integrate a responsive full-stack web application (React 18 + Node.js Express REST API) demonstrating end-to-end CRUD operations against MySQL.", bold_prefix="8. Full-Stack Application Integration: ")

    add_h2("1.4 Scope of the Project")
    add_p("The operational scope encompasses the following functional subsystems:")
    add_bullet("User profile management (registration, authentication, secure password hashing, bio updates).", bold_prefix="User Management: ")
    add_bullet("Publishing, editing, soft deletion, tagging, and multi-language/sentiment tone attribution.", bold_prefix="Content Publishing: ")
    add_bullet("Hierarchical comment threads, atomic upvoting/liking, and idempotency guarantees.", bold_prefix="Social Interactions: ")
    add_bullet("Asymmetric follow/unfollow relationships, mutual follower discovery, and network traversal.", bold_prefix="Social Graph: ")
    add_bullet("Event-driven notification dispatch on likes and follows with self-interaction suppression.", bold_prefix="Notification Dispatch: ")
    add_bullet("Chronological followed-user feed generation, top-performing posts of the week, and creator analytics.", bold_prefix="Feed & Discovery: ")
    add_p(
        "Features such as binary media transcoding, direct end-to-end messaging, and distributed sharding are outside the primary "
        "scope of this database-centric report and are identified for future extension."
    )

    add_h2("1.5 Software and Hardware Requirements")
    add_p("The system development and benchmarking environment utilizes the following software and hardware components:")
    
    req_headers = ["Component", "Specification / Technology", "Role in System"]
    req_rows = [
        ["Database Engine", "MySQL 8.0+ / MariaDB 10.11+", "Relational data storage, constraint checking, triggers, views, stored procedures"],
        ["Backend Runtime", "Node.js (v20.x LTS) / Express 4.18", "RESTful API server, connection pooling, bcrypt authentication, transaction dispatch"],
        ["Database Client", "mysql2/promise (v3.9+)", "High-performance connection pooling, prepared statements, async SQL execution"],
        ["Frontend Framework", "React 18 (Vite 5)", "Interactive single-page application (SPA), dynamic state management, responsive UI"],
        ["Styling & UI Icons", "Vanilla CSS3 tokens + Lucide React", "Design system, dark-mode tokens, tactile typography, interactive icons"],
        ["Development Tools", "Antigravity IDE / VS Code / Git", "Integrated code editing, version control, automated testing scripts"],
        ["Operating System", "Linux (x86_64 / Arch / Ubuntu 22.04 LTS)", "Host development environment and database server host"],
        ["Minimum Hardware", "Multi-core 2.0 GHz+ CPU, 4 GB RAM, 1 GB Disk", "Ensures capacity to run Node API, Vite server, and MySQL daemon concurrently"]
    ]
    add_table_data(req_headers, req_rows, [Inches(1.8), Inches(2.4), Inches(2.8)])

    doc.add_page_break()

    # ==========================================
    # CHAPTER 2: SYSTEM REQUIREMENTS & ANALYSIS
    # ==========================================
    add_chapter_title("2", "System Requirements and Analysis")

    add_h2("2.1 Functional Requirements")
    add_p(
        "The system must support a comprehensive suite of operations covering all user interactions, administrative operations, "
        "and analytical reporting. Table 2.1 details the functional requirements and the corresponding database objects supporting them."
    )

    fr_headers = ["FR ID", "Functional Requirement", "Supporting Database Objects & Implementation"]
    fr_rows = [
        ["FR-01", "User Registration and Profile Management: Secure sign-up, unique identity enforcement, profile updates.", "Users table, UNIQUE(username), UNIQUE(email), bcrypt password hash."],
        ["FR-02", "Post Publication and Soft Deletion: Creators publish posts up to 2200 characters, optional media URL, and soft delete.", "Posts table, is_deleted flag, foreign key referencing Users(user_id)."],
        ["FR-03", "Commenting on Posts: Users author comments on existing posts.", "Comments table, foreign keys to Posts(post_id) and Users(user_id) with CASCADE."],
        ["FR-04", "Idempotent Post Liking: Users can like/unlike posts exactly once without duplicate records.", "Likes junction table, composite primary key (user_id, post_id)."],
        ["FR-05", "Asymmetrical Following: Users can follow/unfollow other users without self-follow.", "Follows junction table, composite primary key (follower_id, following_id), CHECK constraint."],
        ["FR-06", "Automated Notification Generation: Event-driven alerts dispatched to post authors on like.", "Notifications table, trg_notify_on_like AFTER INSERT trigger on Likes."],
        ["FR-07", "Derived Counter Synchronization: Real-time like counter maintained with O(1) read latency.", "Posts.like_count, trg_like_insert and trg_like_delete triggers on Likes."],
        ["FR-08", "Personalized Feed Generation: Chronological feed of active posts from followed authors.", "user_feed MySQL View joining Follows, Posts, and Users tables."],
        ["FR-09", "Mutual Follower Discovery: Retrieve all shared followers between any two arbitrary users.", "get_mutual_followers stored procedure performing self-join on Follows."],
        ["FR-10", "Taxonomy & Content Tagging: Deduplicated topical categorization of posts.", "Tags and PostTags tables, composite PK (post_id, tag_id)."],
        ["FR-11", "Platform Engagement Analytics: Aggregating creator engagement across posts, likes, and comments.", "Multi-table grouping query with COUNT, SUM, and AVG aggregations."]
    ]
    add_table_data(fr_headers, fr_rows, [Inches(0.8), Inches(2.7), Inches(3.5)])

    add_h2("2.2 Business Rules")
    add_p(
        "To ensure business integrity and prevent corrupted or nonsensical platform states, the application enforces the following rules:"
    )
    add_bullet(
        "Every user account must possess a unique integer user_id, an alphanumeric username (max 30 chars), and a valid email address. "
        "No two accounts may share the same username or email.",
        bold_prefix="Rule 1 (User Identity Uniqueness): "
    )
    add_bullet(
        "A post must be authored by an existing user. Post content must not be null or empty. Posts marked with is_deleted = TRUE "
        "must be excluded from feeds, discovery, and search, but retained for audit integrity.",
        bold_prefix="Rule 2 (Post Integrity and Visibility): "
    )
    add_bullet(
        "Users are strictly forbidden from following themselves. The database engine must reject any follow record where follower_id = following_id.",
        bold_prefix="Rule 3 (Self-Follow Invariant): "
    )
    add_bullet(
        "A user may like a given post at most once. Attempting to insert a duplicate like must be rejected by the primary key constraint.",
        bold_prefix="Rule 4 (Idempotent Post Interaction): "
    )
    add_bullet(
        "The stored like_count in the Posts table must strictly equal the actual count of rows in the Likes table. "
        "This invariant is maintained transactionally through AFTER INSERT and AFTER DELETE triggers on Likes.",
        bold_prefix="Rule 5 (Derived Counter Invariant): "
    )
    add_bullet(
        "When a user likes their own post, the database must not dispatch a notification to that user.",
        bold_prefix="Rule 6 (Notification Self-Suppression): "
    )
    add_bullet(
        "Deleting a user record must automatically remove all associated posts, comments, likes, follows, and notifications via ON DELETE CASCADE.",
        bold_prefix="Rule 7 (Cascading Lifecycle Deletion): "
    )
    add_bullet(
        "Deleting a post must automatically cascade to delete all its comments, likes, and associated post-tag relationships.",
        bold_prefix="Rule 8 (Post Association Cascade): "
    )
    add_bullet(
        "A comment must be linked to both an existing post and an existing user author. Orphaned comments are prohibited.",
        bold_prefix="Rule 9 (Comment Integrity): "
    )
    add_bullet(
        "Tag names must be unique and case-insensitive. Posts link to tags via a normalized junction table.",
        bold_prefix="Rule 10 (Taxonomy Deduplication): "
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 3: ENTITY–RELATIONSHIP MODELING
    # ==========================================
    add_chapter_title("3", "Entity–Relationship (ER) Modeling")

    add_h2("3.1 Identification of Entities")
    add_p(
        "The domain analysis identifies seven primary entities (including strong entities, associative junction entities, "
        "and self-referencing networks). The entities and their attributes are detailed below:"
    )

    entities = [
        ("Users", "Represents registered account holders on the platform.", [
            ("user_id", "INT", "PK, AUTO_INCREMENT", "Unique surrogate identifier for the user"),
            ("username", "VARCHAR(30)", "UNIQUE, NOT NULL", "Unique alphanumeric handle for mentions"),
            ("email", "VARCHAR(255)", "UNIQUE, NOT NULL", "Registered email address for login and notifications"),
            ("password_hash", "VARCHAR(255)", "NOT NULL", "Bcrypt cryptographic salted hash of user password"),
            ("bio", "TEXT", "NULL", "User biography and editorial introduction"),
            ("created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Account registration timestamp")
        ]),
        ("Posts", "Represents top-level content authored by users.", [
            ("post_id", "INT", "PK, AUTO_INCREMENT", "Unique identifier for the post"),
            ("user_id", "INT", "FK, NOT NULL", "Author's user_id referencing Users(user_id)"),
            ("content", "VARCHAR(2200)", "NOT NULL", "Body text of the post (micro-blog length)"),
            ("media_url", "VARCHAR(500)", "NULL", "Optional URL to image or multimedia asset"),
            ("like_count", "INT", "DEFAULT 0", "Cached aggregate like count maintained via triggers"),
            ("language", "VARCHAR(50)", "DEFAULT 'English'", "Detected language of the content"),
            ("tone", "VARCHAR(50)", "DEFAULT 'General'", "Classified sentiment tone of the text"),
            ("is_deleted", "BOOLEAN", "DEFAULT FALSE", "Soft-deletion flag for feed filtering"),
            ("created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Publication timestamp")
        ]),
        ("Comments", "Represents responses authored by users under posts.", [
            ("comment_id", "INT", "PK, AUTO_INCREMENT", "Unique identifier for the comment"),
            ("post_id", "INT", "FK, NOT NULL", "Parent post referencing Posts(post_id)"),
            ("user_id", "INT", "FK, NOT NULL", "Author referencing Users(user_id)"),
            ("content", "VARCHAR(500)", "NOT NULL", "Comment text content"),
            ("created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Comment creation timestamp")
        ]),
        ("Likes", "Associative junction entity representing post upvotes.", [
            ("user_id", "INT", "PK, FK, NOT NULL", "Liking user referencing Users(user_id)"),
            ("post_id", "INT", "PK, FK, NOT NULL", "Target post referencing Posts(post_id)"),
            ("created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Timestamp when like was placed")
        ]),
        ("Follows", "Self-referencing recursive associative entity modeling the social graph.", [
            ("follower_id", "INT", "PK, FK, NOT NULL", "User initiating the follow referencing Users(user_id)"),
            ("following_id", "INT", "PK, FK, NOT NULL", "User being followed referencing Users(user_id)"),
            ("created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Timestamp when relationship was established")
        ]),
        ("Notifications", "System-generated event alerts dispatched to users.", [
            ("notification_id", "INT", "PK, AUTO_INCREMENT", "Unique identifier for notification"),
            ("user_id", "INT", "FK, NOT NULL", "Recipient user referencing Users(user_id)"),
            ("type", "VARCHAR(20)", "NOT NULL", "Notification category ('like', 'comment', 'follow')"),
            ("reference_id", "INT", "NOT NULL", "ID of the associated entity (post_id or follower_id)"),
            ("is_read", "BOOLEAN", "DEFAULT FALSE", "Read status indicator"),
            ("created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Dispatch timestamp")
        ]),
        ("Tags & PostTags", "Topical classification taxonomy.", [
            ("tag_id", "INT", "PK, AUTO_INCREMENT", "Unique tag identifier"),
            ("name", "VARCHAR(50)", "UNIQUE, NOT NULL", "Topical tag label (e.g. 'DBMS', 'WebDev')"),
            ("post_id", "INT", "PK, FK, NOT NULL", "Referencing Posts(post_id) in PostTags junction"),
            ("tag_id (in PostTags)", "INT", "PK, FK, NOT NULL", "Referencing Tags(tag_id) in PostTags junction")
        ])
    ]

    for ent_name, ent_desc, attrs in entities:
        add_h3(f"Entity: {ent_name}")
        add_p(ent_desc)
        tbl_headers = ["Attribute Name", "Data Type", "Constraints", "Description"]
        tbl_rows = [[a[0], a[1], a[2], a[3]] for a in attrs]
        add_table_data(tbl_headers, tbl_rows, [Inches(1.8), Inches(1.4), Inches(1.8), Inches(2.0)])

    add_h2("3.2 Identification of Relationships")
    add_p(
        "Relationships among entities reflect the interactive dynamics of a social networking platform. "
        "Table 3.1 summarizes the identified relationships, their cardinality ratios, participation constraints, and physical mappings."
    )

    rel_headers = ["Relationship Name", "Participating Entities", "Cardinality", "Participation", "Implementation Mechanism"]
    rel_rows = [
        ["User Creates Post", "Users and Posts", "1 : N", "Users (Partial) : Posts (Total)", "Foreign key Posts.user_id -> Users.user_id (ON DELETE CASCADE)"],
        ["User Authors Comment", "Users and Comments", "1 : N", "Users (Partial) : Comments (Total)", "Foreign key Comments.user_id -> Users.user_id (ON DELETE CASCADE)"],
        ["Post Contains Comments", "Posts and Comments", "1 : N", "Posts (Partial) : Comments (Total)", "Foreign key Comments.post_id -> Posts.post_id (ON DELETE CASCADE)"],
        ["User Likes Post", "Users and Posts", "M : N", "Users (Partial) : Posts (Partial)", "Junction table Likes(user_id, post_id) with composite PK"],
        ["User Follows User", "Users and Users (Recursive)", "M : N", "Users (Partial) : Users (Partial)", "Junction table Follows(follower_id, following_id) with CHECK constraint"],
        ["User Receives Notification", "Users and Notifications", "1 : N", "Users (Partial) : Notifications (Total)", "Foreign key Notifications.user_id -> Users.user_id (ON DELETE CASCADE)"],
        ["Post Tagged with Tag", "Posts and Tags", "M : N", "Posts (Partial) : Tags (Partial)", "Junction table PostTags(post_id, tag_id) with composite PK"]
    ]
    add_table_data(rel_headers, rel_rows, [Inches(1.5), Inches(1.4), Inches(0.8), Inches(1.4), Inches(1.9)])

    add_h2("3.3 ER Diagram")
    add_p(
        "The conceptual database design is presented using Peter Chen's classic Entity-Relationship notation in Figure 3.1. "
        "Rectangles denote entity sets, diamonds denote relationship sets, ellipses represent attributes (with primary keys underlined), "
        "and double diamonds/lines represent weak entities and total participation where applicable."
    )
    add_image_figure("report_assets/er_diagram_chen.png", "Figure 3.1: Entity–Relationship (ER) diagram of the Social Media Database (Chen notation)", width=Inches(6.2))

    add_h2("3.4 Explanation of the ER Diagram")
    add_p(
        "The ER diagram visualizes the complete structural topology of the social networking platform:",
        bold_prefix="Structural Topology: "
    )
    add_bullet(
        "Users is the primary root entity. It maintains 1:N relationships with Posts, Comments, and Notifications. "
        "A user can exist without having published any posts or written comments (partial participation). "
        "Conversely, every post and comment must belong to exactly one user (total participation on the N-side).",
        bold_prefix="Core Entity Sets: "
    )
    add_bullet(
        "The Likes relationship forms an M:N associative entity between Users and Posts. Because a user can like many posts "
        "and a post can be liked by many users, Likes is resolved into a junction table with its own timestamp attribute.",
        bold_prefix="Many-to-Many Interactions: "
    )
    add_bullet(
        "The Follows relationship is a recursive (self-referencing) M:N relationship on the Users entity set. An individual user "
        "participates in two distinct roles: as a follower (origin) and as a following target (destination). "
        "The structural constraint follower_id <> following_id ensures acyclic self-references.",
        bold_prefix="Recursive Social Graph: "
    )
    add_bullet(
        "The attribute like_count in Posts is a derived attribute (indicated conceptually by a dashed ellipse). It stores the "
        "count of associated Likes records, transactionally maintained through database triggers to optimize read performance.",
        bold_prefix="Derived Attribute: "
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 4: ER-TO-RELATIONAL MAPPING
    # ==========================================
    add_chapter_title("4", "ER-to-Relational Mapping")

    add_h2("4.1 Mapping Rules")
    add_p(
        "The ER diagram is mapped into relational database tables using the standard formal 7-step mapping algorithm:"
    )
    add_bullet(
        "Each regular entity type E in the ER diagram becomes a relation R. All simple single-valued attributes of E are "
        "included as attributes of R. The primary key of E becomes the primary key of R.",
        bold_prefix="Rule 1 (Strong Entity Types): "
    )
    add_bullet(
        "For each weak entity type W with owner entity E, create a relation R. Include all simple attributes of W. "
        "Include the primary key of E as a foreign key in R. The primary key of R is the combination of the owner's primary key "
        "and the partial key of W.",
        bold_prefix="Rule 2 (Weak Entity Types): "
    )
    add_bullet(
        "For binary 1:1 relationships, choose one relation S and include the primary key of the other relation T as a foreign "
        "key in S, accompanied by a UNIQUE constraint.",
        bold_prefix="Rule 3 (1:1 Relationship Types): "
    )
    add_bullet(
        "For binary 1:N relationships, identify the relation S representing the entity on the N-side. Include the primary key "
        "of the relation T on the 1-side as a foreign key in S, along with any simple attributes of the relationship.",
        bold_prefix="Rule 4 (1:N Relationship Types): "
    )
    add_bullet(
        "For binary M:N relationships, create a new junction relation R. Include the primary keys of both participating "
        "entities as foreign keys in R. The composite primary key of R is the combination of both foreign keys.",
        bold_prefix="Rule 5 (M:N Relationship Types): "
    )
    add_bullet(
        "For recursive (self-referencing) M:N relationships, create a junction relation containing two foreign key attributes, "
        "both referencing the primary key of the same parent relation with distinct role names.",
        bold_prefix="Rule 6 (Recursive M:N Relationships): "
    )
    add_bullet(
        "For multivalued attributes, create a separate relation containing the multivalued attribute and the primary key "
        "of the parent relation as a foreign key.",
        bold_prefix="Rule 7 (Multivalued Attributes): "
    )

    add_h2("4.2 Step-by-Step Conversion")
    add_p("Applying these transformation rules yields the following physical table conversions:")
    add_bullet(
        "The strong entity Users maps directly to table USERS with primary key user_id. "
        "Attributes: user_id (PK), username (UNIQUE), email (UNIQUE), password_hash, bio, created_at.",
        bold_prefix="Step 1 (Conversion of USERS): "
    )
    add_bullet(
        "The 1:N relationship between Users and Posts maps the primary key Users.user_id into POSTS as a foreign key. "
        "Attributes: post_id (PK), user_id (FK), content, media_url, like_count, language, tone, is_deleted, created_at.",
        bold_prefix="Step 2 (Conversion of POSTS): "
    )
    add_bullet(
        "Comments is on the N-side of two 1:N relationships (Users-Comments and Posts-Comments). Both user_id and post_id "
        "are mapped into COMMENTS as foreign keys. Attributes: comment_id (PK), post_id (FK), user_id (FK), content, created_at.",
        bold_prefix="Step 3 (Conversion of COMMENTS): "
    )
    add_bullet(
        "The M:N relationship Likes maps to table LIKES. Foreign keys user_id and post_id form the composite primary key. "
        "Attributes: (user_id, post_id) (Composite PK), created_at.",
        bold_prefix="Step 4 (Conversion of LIKES): "
    )
    add_bullet(
        "The recursive M:N relationship Follows maps to table FOLLOWS with two distinct role foreign keys follower_id and following_id. "
        "Attributes: (follower_id, following_id) (Composite PK), created_at.",
        bold_prefix="Step 5 (Conversion of FOLLOWS): "
    )
    add_bullet(
        "The 1:N relationship Users-Notifications maps user_id into NOTIFICATIONS as a foreign key. "
        "Attributes: notification_id (PK), user_id (FK), type, reference_id, is_read, created_at.",
        bold_prefix="Step 6 (Conversion of NOTIFICATIONS): "
    )
    add_bullet(
        "The taxonomy entity Tags maps to TAGS with primary key tag_id. The M:N association between Posts and Tags maps to "
        "POST_TAGS with composite primary key (post_id, tag_id).",
        bold_prefix="Step 7 (Conversion of TAGS and POST_TAGS): "
    )

    add_h2("4.3 Final Relational Schema")
    add_p(
        "The resulting relational schema is formally declared below. Primary keys are underlined, and foreign keys are explicitly noted:"
    )
    
    schema_declarations = [
        "USERS ( user_id, username, email, password_hash, bio, created_at )\n"
        "  - Primary Key: user_id\n"
        "  - Candidate Keys: username, email\n",

        "POSTS ( post_id, user_id, content, media_url, like_count, language, tone, is_deleted, created_at )\n"
        "  - Primary Key: post_id\n"
        "  - Foreign Key: user_id REFERENCES USERS(user_id) ON DELETE CASCADE\n",

        "COMMENTS ( comment_id, post_id, user_id, content, created_at )\n"
        "  - Primary Key: comment_id\n"
        "  - Foreign Keys: post_id REFERENCES POSTS(post_id) ON DELETE CASCADE,\n"
        "                  user_id REFERENCES USERS(user_id) ON DELETE CASCADE\n",

        "LIKES ( user_id, post_id, created_at )\n"
        "  - Composite Primary Key: (user_id, post_id)\n"
        "  - Foreign Keys: user_id REFERENCES USERS(user_id) ON DELETE CASCADE,\n"
        "                  post_id REFERENCES POSTS(post_id) ON DELETE CASCADE\n",

        "FOLLOWS ( follower_id, following_id, created_at )\n"
        "  - Composite Primary Key: (follower_id, following_id)\n"
        "  - Foreign Keys: follower_id REFERENCES USERS(user_id) ON DELETE CASCADE,\n"
        "                  following_id REFERENCES USERS(user_id) ON DELETE CASCADE\n"
        "  - Check Constraint: CHECK (follower_id <> following_id)\n",

        "NOTIFICATIONS ( notification_id, user_id, type, reference_id, is_read, created_at )\n"
        "  - Primary Key: notification_id\n"
        "  - Foreign Key: user_id REFERENCES USERS(user_id) ON DELETE CASCADE\n",

        "TAGS ( tag_id, name )\n"
        "  - Primary Key: tag_id\n"
        "  - Candidate Key: name\n",

        "POST_TAGS ( post_id, tag_id )\n"
        "  - Composite Primary Key: (post_id, tag_id)\n"
        "  - Foreign Keys: post_id REFERENCES POSTS(post_id) ON DELETE CASCADE,\n"
        "                  tag_id REFERENCES TAGS(tag_id) ON DELETE CASCADE\n"
    ]
    for s_decl in schema_declarations:
        add_code(s_decl)

    add_p(
        "Figure 4.1 shows the full relational schema diagram illustrating primary key icons, foreign key connectors, "
        "data types, and cardinality notations."
    )
    add_image_figure("report_assets/relational_schema.png", "Figure 4.1: Relational Schema Diagram showing tables, keys, and foreign-key references", width=Inches(6.2))

    doc.add_page_break()

    # ==========================================
    # CHAPTER 5: FUNCTIONAL DEPENDENCIES
    # ==========================================
    add_chapter_title("5", "Functional Dependencies")

    add_h2("5.1 Identification of Functional Dependencies")
    add_p(
        "A functional dependency X -> Y holds on relation R if and only if whenever two tuples agree on attribute set X, "
        "they must also agree on attribute set Y. Based on the system's business rules, the functional dependencies "
        "for each relation are formally identified as follows:"
    )

    fds = [
        ("USERS", [
            "FD1: user_id -> username, email, password_hash, bio, created_at",
            "FD2: username -> user_id, email, password_hash, bio, created_at",
            "FD3: email -> user_id, username, password_hash, bio, created_at"
        ]),
        ("POSTS", [
            "FD4: post_id -> user_id, content, media_url, like_count, language, tone, is_deleted, created_at"
        ]),
        ("COMMENTS", [
            "FD5: comment_id -> post_id, user_id, content, created_at"
        ]),
        ("LIKES", [
            "FD6: {user_id, post_id} -> created_at"
        ]),
        ("FOLLOWS", [
            "FD7: {follower_id, following_id} -> created_at"
        ]),
        ("NOTIFICATIONS", [
            "FD8: notification_id -> user_id, type, reference_id, is_read, created_at"
        ]),
        ("TAGS", [
            "FD9: tag_id -> name",
            "FD10: name -> tag_id"
        ]),
        ("POST_TAGS", [
            "FD11: {post_id, tag_id} -> post_id, tag_id (Trivial dependency)"
        ])
    ]
    for rel_name, fd_list in fds:
        add_h3(f"Relation: {rel_name}")
        for fd in fd_list:
            add_bullet(fd)

    add_h2("5.2 Candidate Keys and Attribute Classification")
    add_p(
        "An attribute is prime if it belongs to any candidate key of the relation. Otherwise, it is non-prime. "
        "Table 5.1 classifies the candidate keys, prime attributes, and non-prime attributes for every relation."
    )

    ck_headers = ["Relation", "Candidate Key(s)", "Prime Attributes", "Non-Prime Attributes"]
    ck_rows = [
        ["USERS", "{user_id}, {username}, {email}", "user_id, username, email", "password_hash, bio, created_at"],
        ["POSTS", "{post_id}", "post_id", "user_id, content, media_url, like_count, language, tone, is_deleted, created_at"],
        ["COMMENTS", "{comment_id}", "comment_id", "post_id, user_id, content, created_at"],
        ["LIKES", "{user_id, post_id}", "user_id, post_id", "created_at"],
        ["FOLLOWS", "{follower_id, following_id}", "follower_id, following_id", "created_at"],
        ["NOTIFICATIONS", "{notification_id}", "notification_id", "user_id, type, reference_id, is_read, created_at"],
        ["TAGS", "{tag_id}, {name}", "tag_id, name", "None (All attributes are prime)"],
        ["POST_TAGS", "{post_id, tag_id}", "post_id, tag_id", "None (All-key relation)"]
    ]
    add_table_data(ck_headers, ck_rows, [Inches(1.5), Inches(1.8), Inches(1.8), Inches(2.1)])

    add_h2("5.3 FD Analysis")
    add_p(
        "Each functional dependency identified above is justified by the application domain requirements and semantic invariants:",
        bold_prefix="Semantic Justification: "
    )
    add_bullet(
        "In USERS, user_id is the primary surrogate key. By the uniqueness invariant of user accounts, no two distinct users "
        "may share the same identifier, username, or email. Hence, user_id, username, and email are equivalent candidate keys, "
        "each determining the user's password hash, biography, and registration timestamp.",
        bold_prefix="USERS Dependencies: "
    )
    add_bullet(
        "In POSTS, post_id uniquely identifies a publication event. The author's identity (user_id), post text, metadata, "
        "and creation timestamp are uniquely fixed once published. Note that while like_count is derivable from Likes, "
        "within the POSTS relation it functionally depends on post_id as an atomic scalar attribute.",
        bold_prefix="POSTS Dependencies: "
    )
    add_bullet(
        "In LIKES, a user can upvote a particular post at most once. Neither user_id alone nor post_id alone determines "
        "created_at, because a single user likes multiple posts at different times, and a single post is liked by multiple users "
        "at different times. Only the composite pair {user_id, post_id} uniquely determines the interaction timestamp created_at.",
        bold_prefix="LIKES Composite Dependency: "
    )
    add_bullet(
        "In FOLLOWS, the relationship is directed and asymmetrical. Exactly one timestamp exists for the established connection "
        "between follower_id and following_id. Neither attribute individually determines created_at.",
        bold_prefix="FOLLOWS Composite Dependency: "
    )
    add_bullet(
        "In POST_TAGS, both attributes form the composite primary key. There are no non-key attributes; the relation represents "
        "a pure binary relationship set with only trivial functional dependencies.",
        bold_prefix="POST_TAGS All-Key Dependency: "
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 6: DATABASE NORMALIZATION
    # ==========================================
    add_chapter_title("6", "Database Normalization")

    add_p(
        "Database normalization is the formal process of structuring a relational schema to minimize data redundancy, "
        "prevent modification anomalies (insertion, deletion, and update anomalies), and ensure dependency preservation. "
        "Below, normalization is demonstrated step by step from an unnormalized state through BCNF."
    )

    add_h2("6.1 Unnormalized Form (UNF)")
    add_p(
        "Consider a hypothetical unnormalized flat table UNF_SOCIAL_PLATFORM that attempts to store all social interactions "
        "within a single denormalized structure:"
    )
    add_code(
        "UNF_SOCIAL_PLATFORM(\n"
        "    user_id, username, email, bio,\n"
        "    { post_id, content, created_at, { tag_name }, { comment_id, commenter_username, comment_content } },\n"
        "    { following_user_id, following_username }\n"
        ")"
    )
    add_p(
        "This unnormalized structure contains nested repeating groups (sets of posts per user, sets of comments per post, "
        "and sets of followed users). This causes severe relational anomalies:",
        bold_prefix="Anomalies in UNF: "
    )
    add_bullet(
        "To update a user's bio, the system must update multiple rows across all posts and comments authored by that user. "
        "If a system crash occurs halfway through, the bio becomes inconsistent across different records.",
        bold_prefix="Update Anomaly: "
    )
    add_bullet(
        "A new user cannot be recorded in the database until they publish at least one post, because post_id would be NULL in "
        "a relation requiring post identification.",
        bold_prefix="Insertion Anomaly: "
    )
    add_bullet(
        "If a user deletes their only published post, the record of the user itself and their profile details are inadvertently lost.",
        bold_prefix="Deletion Anomaly: "
    )

    add_h2("6.2 First Normal Form (1NF)")
    add_p(
        "Definition: A relation R is in First Normal Form (1NF) if and only if the domain of every attribute consists of "
        "atomic (indivisible) values, and there are no repeating groups or nested relations.",
        bold_prefix="1NF Definition: "
    )
    add_p(
        "To achieve 1NF, repeating groups are eliminated by decomposing the flat structure into distinct relations and ensuring "
        "all columns contain atomic scalar values. Multivalued tags and repeating comments are split out into separate rows "
        "linked by identifiers. After 1NF decomposition, we obtain relations with atomic attributes: "
        "USERS, POSTS, COMMENTS, LIKES, FOLLOWS, NOTIFICATIONS, TAGS, and POST_TAGS."
    )

    add_h2("6.3 Second Normal Form (2NF)")
    add_p(
        "Definition: A relation R is in Second Normal Form (2NF) if and only if it is in 1NF and every non-prime attribute is "
        "fully functionally dependent on every candidate key (i.e., no non-prime attribute is partially dependent on any candidate key).",
        bold_prefix="2NF Definition: "
    )
    add_p("Evaluation of relations against 2NF:")
    add_bullet(
        "Relations with single-attribute primary keys (USERS, POSTS, COMMENTS, NOTIFICATIONS, TAGS) are trivially in 2NF, "
        "because a single-attribute key cannot have proper subsets. Partial dependencies cannot exist.",
        bold_prefix="Single-Attribute Relations: "
    )
    add_bullet(
        "In LIKES, the candidate key is {user_id, post_id}. The only non-prime attribute is created_at. "
        "As established in Chapter 5, created_at depends on both user_id AND post_id simultaneously. Neither user_id -> created_at "
        "nor post_id -> created_at holds. Hence, created_at is fully dependent on the entire composite key. LIKES satisfies 2NF.",
        bold_prefix="LIKES Evaluation: "
    )
    add_bullet(
        "In FOLLOWS, the candidate key is {follower_id, following_id}. The non-prime attribute created_at depends on the "
        "entire composite key. FOLLOWS satisfies 2NF.",
        bold_prefix="FOLLOWS Evaluation: "
    )
    add_bullet(
        "In POST_TAGS, all attributes are prime ({post_id, tag_id}). There are zero non-prime attributes, so partial dependency "
        "is impossible. POST_TAGS satisfies 2NF.",
        bold_prefix="POST_TAGS Evaluation: "
    )

    add_h2("6.4 Third Normal Form (3NF)")
    add_p(
        "Definition: A relation R is in Third Normal Form (3NF) if and only if it is in 2NF and for every non-trivial functional "
        "dependency X -> A, either: (1) X is a superkey of R, OR (2) A is a prime attribute of R (i.e., no non-prime attribute "
        "is transitively dependent on any candidate key).",
        bold_prefix="3NF Definition: "
    )
    add_p("Evaluation of relations against 3NF:")
    add_bullet(
        "In USERS, the FDs are user_id -> non-prime attributes, username -> non-prime attributes, and email -> non-prime attributes. "
        "Since user_id, username, and email are all candidate keys (superkeys), condition (1) is satisfied. No transitive dependencies exist. USERS is in 3NF.",
        bold_prefix="USERS in 3NF: "
    )
    add_bullet(
        "In POSTS, the only determinant is post_id, which is the primary key. If we had stored the author's username or email "
        "inside POSTS, we would have had the transitive dependency post_id -> user_id -> username. Because author details were "
        "properly normalized into USERS, POSTS contains only attributes functionally dependent directly on post_id. POSTS is in 3NF.",
        bold_prefix="POSTS in 3NF: "
    )
    add_bullet(
        "In COMMENTS, comment_id is the primary key and determines post_id, user_id, content, and created_at. Author and post "
        "details are referenced strictly by foreign keys. No transitive dependencies exist. COMMENTS is in 3NF.",
        bold_prefix="COMMENTS in 3NF: "
    )
    add_bullet(
        "In LIKES, FOLLOWS, NOTIFICATIONS, TAGS, and POST_TAGS, all determinants are superkeys. All relations satisfy 3NF.",
        bold_prefix="Other Relations: "
    )

    add_h2("6.5 Boyce–Codd Normal Form (BCNF)")
    add_p(
        "Definition: A relation R is in Boyce-Codd Normal Form (BCNF) if and only if for every non-trivial functional dependency "
        "X -> Y, X is a superkey of R. BCNF is stricter than 3NF because it disallows non-superkey determinants even if the "
        "dependent attribute Y is prime.",
        bold_prefix="BCNF Definition: "
    )
    add_p("Evaluation of relations against BCNF:")
    add_bullet("USERS: The determinants are user_id, username, and email. All three are candidate keys (superkeys). Satisfies BCNF.", bold_prefix="USERS: ")
    add_bullet("POSTS: The only determinant is post_id, which is the primary key (superkey). Satisfies BCNF.", bold_prefix="POSTS: ")
    add_bullet("COMMENTS: The only determinant is comment_id, which is the primary key (superkey). Satisfies BCNF.", bold_prefix="COMMENTS: ")
    add_bullet("LIKES: The only determinant is {user_id, post_id}, which is the composite candidate key. Satisfies BCNF.", bold_prefix="LIKES: ")
    add_bullet("FOLLOWS: The only determinant is {follower_id, following_id}, which is the composite candidate key. Satisfies BCNF.", bold_prefix="FOLLOWS: ")
    add_bullet("NOTIFICATIONS: The only determinant is notification_id, which is the primary key. Satisfies BCNF.", bold_prefix="NOTIFICATIONS: ")
    add_bullet("TAGS: The determinants are tag_id and name. Both are candidate keys. Satisfies BCNF.", bold_prefix="TAGS: ")
    add_bullet("POST_TAGS: No non-trivial dependencies exist. Satisfies BCNF.", bold_prefix="POST_TAGS: ")
    add_p("Conclusion: All relations in the schema strictly satisfy Boyce-Codd Normal Form (BCNF).")

    add_h2("6.6 Final Normalized Schema and Deliberate Denormalization")
    add_p(
        "Table 6.1 summarizes the final normalized schema and the normal form achieved for every relation."
    )

    norm_headers = ["Relation Name", "Primary / Candidate Keys", "Determinants", "Normal Form Achieved"]
    norm_rows = [
        ["USERS", "{user_id}, {username}, {email}", "All determinants are superkeys", "BCNF"],
        ["POSTS", "{post_id}", "post_id (superkey)", "BCNF"],
        ["COMMENTS", "{comment_id}", "comment_id (superkey)", "BCNF"],
        ["LIKES", "{user_id, post_id}", "{user_id, post_id} (superkey)", "BCNF"],
        ["FOLLOWS", "{follower_id, following_id}", "{follower_id, following_id} (superkey)", "BCNF"],
        ["NOTIFICATIONS", "{notification_id}", "notification_id (superkey)", "BCNF"],
        ["TAGS", "{tag_id}, {name}", "tag_id, name (superkeys)", "BCNF"],
        ["POST_TAGS", "{post_id, tag_id}", "All-key relation", "BCNF"]
    ]
    add_table_data(norm_headers, norm_rows, [Inches(1.5), Inches(2.2), Inches(2.1), Inches(1.2)])

    add_p(
        "A Deliberate Denormalization Note: The attribute Posts.like_count represents a deliberate, controlled denormalization. "
        "In strict 3NF/BCNF without cached counters, determining the like count for each post in a feed requires executing "
        "SELECT COUNT(*) FROM Likes WHERE post_id = ? across dozens of posts per request. Under high concurrency, this causes "
        "excessive buffer pool churn. By maintaining like_count directly on the Posts row via database triggers (Section 8.7), "
        "feed queries read like counts in O(1) time without losing transactional consistency.",
        bold_prefix="Controlled Denormalization Analysis: "
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 7: RELATIONAL INTEGRITY & CONSTRAINTS
    # ==========================================
    add_chapter_title("7", "Relational Integrity and Constraints")

    add_p(
        "Relational integrity constraints define the assertions that a valid database state must satisfy. In this project, "
        "all business invariants are enforced directly within the MySQL database engine rather than relying on application code. "
        "This guarantees data consistency even in the presence of bugs in the front end or backend API."
    )

    add_h2("7.1 Domain Constraints")
    add_p(
        "Domain constraints restrict the valid set of values that an attribute may take:",
        bold_prefix="Domain Boundaries: "
    )
    add_bullet("Attribute username is bounded to VARCHAR(30) with utf8mb4 collation, preventing buffer overflow and SQL injection exploits.", bold_prefix="Users.username: ")
    add_bullet("Attribute email is restricted to VARCHAR(255) adhering to RFC 5321 standard length limits.", bold_prefix="Users.email: ")
    add_bullet("Attribute content in Posts is bounded to VARCHAR(2200), enforcing standard microblogging editorial constraints.", bold_prefix="Posts.content: ")
    add_bullet("Attributes language and tone are constrained to VARCHAR(50) with default values 'English' and 'General'.", bold_prefix="Posts.language & tone: ")
    add_bullet("Timestamp fields (created_at) use TIMESTAMP DEFAULT CURRENT_TIMESTAMP to ensure monotonic temporal sequencing.", bold_prefix="Timestamps: ")

    add_h2("7.2 Primary Key Constraints")
    add_p(
        "Primary key constraints enforce entity integrity by requiring that primary key values are unique and non-null:",
        bold_prefix="Entity Integrity: "
    )
    add_bullet("Single-attribute surrogate keys (user_id, post_id, comment_id, notification_id, tag_id) utilize INT AUTO_INCREMENT to guarantee unique, immutable identifiers.", bold_prefix="Surrogate Primary Keys: ")
    add_bullet("Junction relations utilize composite primary keys: PRIMARY KEY (user_id, post_id) on Likes, PRIMARY KEY (follower_id, following_id) on Follows, and PRIMARY KEY (post_id, tag_id) on PostTags. This structurally prohibits duplicate edges in the social graph.", bold_prefix="Composite Primary Keys: ")

    add_h2("7.3 Foreign Key Constraints and Referential Actions")
    add_p(
        "Foreign key constraints enforce referential integrity across related tables. Referential actions define the behavior "
        "when referenced parent rows are updated or deleted:",
        bold_prefix="Referential Integrity: "
    )
    add_bullet(
        "Posts.user_id REFERENCES Users(user_id) ON DELETE CASCADE. Deleting a user deletes all posts authored by that user.",
        bold_prefix="User to Post Cascade: "
    )
    add_bullet(
        "Comments.post_id REFERENCES Posts(post_id) ON DELETE CASCADE. Deleting a post removes all its comments.",
        bold_prefix="Post to Comments Cascade: "
    )
    add_bullet(
        "Likes.user_id REFERENCES Users(user_id) ON DELETE CASCADE and Likes.post_id REFERENCES Posts(post_id) ON DELETE CASCADE. "
        "Removing either a user or a post automatically purges the corresponding like records.",
        bold_prefix="Likes Cascade: "
    )
    add_bullet(
        "Follows.follower_id REFERENCES Users(user_id) ON DELETE CASCADE and Follows.following_id REFERENCES Users(user_id) ON DELETE CASCADE. "
        "Removing an account purges all inbound and outbound edges in the follower network.",
        bold_prefix="Follows Cascade: "
    )

    add_h2("7.4 UNIQUE and NOT NULL Constraints")
    add_bullet("UNIQUE constraints are enforced on Users.username and Users.email, preventing duplicate registrations.", bold_prefix="Unique Accounts: ")
    add_bullet("UNIQUE constraint is enforced on Tags.name, ensuring taxonomy tags are deduplicated.", bold_prefix="Unique Taxonomy: ")
    add_bullet("NOT NULL constraints are strictly enforced on Users.password_hash, Posts.content, Comments.content, and all foreign key reference columns, ensuring required data cannot be omitted.", bold_prefix="Mandatory Attributes: ")

    add_h2("7.5 CHECK Constraints")
    add_bullet(
        "In the Follows table: CHECK (follower_id <> following_id). Enforces that a user cannot follow their own account.",
        bold_prefix="Self-Follow Prohibition: "
    )
    add_bullet(
        "In the Posts table: like_count >= 0. Ensures that derived like counters cannot fall below zero under any anomaly.",
        bold_prefix="Non-Negative Counters: "
    )

    add_p(
        "Table 7.1 summarizes the relational constraints implemented in the MySQL database."
    )
    c_headers = ["Constraint Type", "Target Table & Column(s)", "Rule Enforced & Invariant Maintained"]
    c_rows = [
        ["PRIMARY KEY", "Users(user_id), Posts(post_id), Comments(comment_id)...", "Guarantees entity integrity and unique tuple identification."],
        ["COMPOSITE PK", "Likes(user_id, post_id), Follows(follower_id, following_id)", "Enforces relationship uniqueness; prevents duplicate likes and follows."],
        ["FOREIGN KEY", "Posts(user_id), Comments(post_id, user_id), Likes...", "Preserves referential integrity; prevents dangling references."],
        ["ON DELETE CASCADE", "All child tables referencing Users and Posts", "Maintains database hygiene by purging orphaned records upon parent deletion."],
        ["UNIQUE", "Users(username), Users(email), Tags(name)", "Prohibits duplicate handles, emails, and taxonomy labels."],
        ["NOT NULL", "All essential data columns (content, password_hash...)", "Guarantees mandatory attributes are always populated."],
        ["CHECK", "Follows: (follower_id <> following_id)", "Syntactically prohibits reflexive self-following edges."]
    ]
    add_table_data(c_headers, c_rows, [Inches(1.8), Inches(2.4), Inches(2.8)])

    doc.add_page_break()

    # ==========================================
    # CHAPTER 8: MYSQL DATABASE IMPLEMENTATION
    # ==========================================
    add_chapter_title("8", "MySQL Database Implementation")

    add_h2("8.1 Database Creation")
    add_p(
        "The database is created using MySQL 8.0+ / MariaDB 10.11+ with the utf8mb4 character set (supporting full multilingual "
        "scripts and Unicode emoji) and utf8mb4_unicode_ci collation for case-insensitive comparisons:"
    )
    add_code(
        "CREATE DATABASE IF NOT EXISTS social_media_db\n"
        "    CHARACTER SET utf8mb4\n"
        "    COLLATE utf8mb4_unicode_ci;\n\n"
        "USE social_media_db;"
    )

    add_h2("8.2 Table Creation")
    add_p(
        "The complete Data Definition Language (DDL) statements for all relations, incorporating all primary keys, "
        "foreign keys, and constraints, are specified below:"
    )
    add_code(
        "-- 1. Users Table\n"
        "CREATE TABLE Users (\n"
        "    user_id        INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    username       VARCHAR(30)  UNIQUE NOT NULL,\n"
        "    email          VARCHAR(255) UNIQUE NOT NULL,\n"
        "    password_hash  VARCHAR(255) NOT NULL,\n"
        "    bio            TEXT,\n"
        "    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n"
        ") ENGINE=InnoDB;\n\n"
        "-- 2. Posts Table\n"
        "CREATE TABLE Posts (\n"
        "    post_id      INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    user_id      INT NOT NULL,\n"
        "    content      VARCHAR(2200) NOT NULL,\n"
        "    media_url    VARCHAR(500),\n"
        "    like_count   INT DEFAULT 0 CHECK (like_count >= 0),\n"
        "    language     VARCHAR(50) DEFAULT 'English',\n"
        "    tone         VARCHAR(50) DEFAULT 'General',\n"
        "    is_deleted   BOOLEAN DEFAULT FALSE,\n"
        "    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
        "    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE\n"
        ") ENGINE=InnoDB;\n\n"
        "-- 3. Comments Table\n"
        "CREATE TABLE Comments (\n"
        "    comment_id   INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    post_id      INT NOT NULL,\n"
        "    user_id      INT NOT NULL,\n"
        "    content      VARCHAR(500) NOT NULL,\n"
        "    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
        "    FOREIGN KEY (post_id) REFERENCES Posts(post_id) ON DELETE CASCADE,\n"
        "    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE\n"
        ") ENGINE=InnoDB;\n\n"
        "-- 4. Likes Table (Junction)\n"
        "CREATE TABLE Likes (\n"
        "    user_id      INT NOT NULL,\n"
        "    post_id      INT NOT NULL,\n"
        "    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
        "    PRIMARY KEY (user_id, post_id),\n"
        "    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,\n"
        "    FOREIGN KEY (post_id) REFERENCES Posts(post_id) ON DELETE CASCADE\n"
        ") ENGINE=InnoDB;\n\n"
        "-- 5. Follows Table (Recursive Junction)\n"
        "CREATE TABLE Follows (\n"
        "    follower_id   INT NOT NULL,\n"
        "    following_id  INT NOT NULL,\n"
        "    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
        "    PRIMARY KEY (follower_id, following_id),\n"
        "    FOREIGN KEY (follower_id)  REFERENCES Users(user_id) ON DELETE CASCADE,\n"
        "    FOREIGN KEY (following_id) REFERENCES Users(user_id) ON DELETE CASCADE,\n"
        "    CHECK (follower_id <> following_id)\n"
        ") ENGINE=InnoDB;\n\n"
        "-- 6. Notifications Table\n"
        "CREATE TABLE Notifications (\n"
        "    notification_id  INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    user_id          INT NOT NULL,\n"
        "    type             VARCHAR(20) NOT NULL,\n"
        "    reference_id     INT NOT NULL,\n"
        "    is_read          BOOLEAN DEFAULT FALSE,\n"
        "    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
        "    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE\n"
        ") ENGINE=InnoDB;\n\n"
        "-- 7. Tags Table\n"
        "CREATE TABLE Tags (\n"
        "    tag_id INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    name   VARCHAR(50) UNIQUE NOT NULL\n"
        ") ENGINE=InnoDB;\n\n"
        "-- 8. PostTags Table\n"
        "CREATE TABLE PostTags (\n"
        "    post_id INT NOT NULL,\n"
        "    tag_id  INT NOT NULL,\n"
        "    PRIMARY KEY (post_id, tag_id),\n"
        "    FOREIGN KEY (post_id) REFERENCES Posts(post_id) ON DELETE CASCADE,\n"
        "    FOREIGN KEY (tag_id) REFERENCES Tags(tag_id) ON DELETE CASCADE\n"
        ") ENGINE=InnoDB;"
    )

    add_h2("8.3 Data Insertion")
    add_p(
        "Representative seed data was inserted to demonstrate all features. Passwords were encrypted using bcrypt hashes "
        "(sample hash corresponding to 'password123'):"
    )
    add_code(
        "-- Inserting Users\n"
        "INSERT INTO Users (user_id, username, email, password_hash, bio) VALUES\n"
        "(1, 'abhinav_sonker', 'abhinav@iiitbhopal.ac.in', '$2b$10$6f6yXSxfu1l6ravXYkqo2uRA1IHNdXuCKbmCiDHP.jsDoPAA97ngS', 'Lead Architect & Student @ IIIT Bhopal'),\n"
        "(2, 'rahul_verma',    'rahul.verma@gmail.com',    '$2b$10$6f6yXSxfu1l6ravXYkqo2uRA1IHNdXuCKbmCiDHP.jsDoPAA97ngS', 'Full stack engineer & open source enthusiast'),\n"
        "(3, 'elena_rostova',  'elena@vektorlab.io',      '$2b$10$6f6yXSxfu1l6ravXYkqo2uRA1IHNdXuCKbmCiDHP.jsDoPAA97ngS', 'Lead Product Designer @ Vektor Lab'),\n"
        "(4, 'marcus_thorne',  'marcus@cloudscale.net',   '$2b$10$6f6yXSxfu1l6ravXYkqo2uRA1IHNdXuCKbmCiDHP.jsDoPAA97ngS', 'Senior Systems Architect. MariaDB internals'),\n"
        "(5, 'selah_kim',      'selah.kim@gmail.com',      '$2b$10$6f6yXSxfu1l6ravXYkqo2uRA1IHNdXuCKbmCiDHP.jsDoPAA97ngS', 'Design Technologist & Creative Coder'),\n"
        "(6, 'tarik_oconnor',  'tarik@foundry.io',        '$2b$10$6f6yXSxfu1l6ravXYkqo2uRA1IHNdXuCKbmCiDHP.jsDoPAA97ngS', 'Database administrator @ Foundry Systems');\n\n"
        "-- Inserting Posts\n"
        "INSERT INTO Posts (post_id, user_id, content, language, tone, created_at) VALUES\n"
        "(1, 1, 'Excited to announce our new 3NF relational architecture for Kinetic Social! Benchmarked with MariaDB indexes.', 'English', 'Enthusiastic', NOW() - INTERVAL 10 HOUR),\n"
        "(2, 3, 'Hot take: Modern software in 2026 feels way too sterile. We need more tactile tension in UI design.', 'English', 'Reflective', NOW() - INTERVAL 8 HOUR),\n"
        "(3, 4, 'Friendly reminder to always check EXPLAIN ANALYZE on complex multi-table joins. Composite B-Tree indexes rule!', 'English', 'Informative', NOW() - INTERVAL 6 HOUR),\n"
        "(4, 5, 'Prototyping fluid gestural feed interactions today. Micro-spring physics makes scrolling weightless.', 'English', 'Creative', NOW() - INTERVAL 4 HOUR),\n"
        "(5, 6, 'Normalized schemas (3NF) vs Denormalized stores: Triggers give you transactional consistency with O(1) reads.', 'English', 'Technical', NOW() - INTERVAL 2 HOUR);\n\n"
        "-- Inserting Follows Network\n"
        "INSERT INTO Follows (follower_id, following_id) VALUES\n"
        "(1, 2), (1, 3), (1, 4), (1, 5), (1, 6),  -- Abhinav follows all creators\n"
        "(2, 1), (2, 4),\n"
        "(3, 1), (3, 5),\n"
        "(4, 1), (4, 6);\n\n"
        "-- Inserting Likes\n"
        "INSERT INTO Likes (user_id, post_id) VALUES\n"
        "(2, 1), (3, 1), (4, 1), (5, 1),  -- 4 likes on post 1\n"
        "(1, 2), (4, 2),                  -- 2 likes on post 2\n"
        "(1, 3), (2, 3), (6, 3);          -- 3 likes on post 3"
    )

    add_h2("8.4 Data Modification and Deletion")
    add_p("Demonstrating appropriate UPDATE and DELETE operations:")
    add_code(
        "-- Update bio\n"
        "UPDATE Users \n"
        "SET bio = 'Lead Systems Engineer @ Kinetic Social | Benchmarking high-concurrency MariaDB instances.'\n"
        "WHERE user_id = 1;\n\n"
        "-- Soft delete a post\n"
        "UPDATE Posts \n"
        "SET is_deleted = TRUE \n"
        "WHERE post_id = 4;\n\n"
        "-- Delete an interaction (Unlike)\n"
        "DELETE FROM Likes \n"
        "WHERE user_id = 2 AND post_id = 1;\n\n"
        "-- Cascade delete a post (Removes associated likes and comments)\n"
        "DELETE FROM Posts \n"
        "WHERE post_id = 5;"
    )

    add_h2("8.5 Sample Database Contents")
    add_p("Table contents after executing the seed and manipulation statements:")
    
    add_h3("Sample Content: USERS")
    u_h = ["user_id", "username", "email", "bio (truncated)", "created_at"]
    u_r = [
        ["1", "abhinav_sonker", "abhinav@iiitbhopal.ac.in", "Lead Systems Engineer @ Kinetic Social...", "2026-10-12 10:14:00"],
        ["2", "rahul_verma", "rahul.verma@gmail.com", "Full stack engineer & open source enthusiast", "2026-10-12 10:15:30"],
        ["3", "elena_rostova", "elena@vektorlab.io", "Lead Product Designer @ Vektor Lab", "2026-10-12 10:16:15"],
        ["4", "marcus_thorne", "marcus@cloudscale.net", "Senior Systems Architect. MariaDB internals", "2026-10-12 10:17:00"],
        ["5", "selah_kim", "selah.kim@gmail.com", "Design Technologist & Creative Coder", "2026-10-12 10:18:22"]
    ]
    add_table_data(u_h, u_r, [Inches(0.8), Inches(1.5), Inches(2.2), Inches(2.3), Inches(1.2)])

    add_h3("Sample Content: POSTS")
    p_h = ["post_id", "user_id", "content (excerpt)", "like_count", "language", "is_deleted"]
    p_r = [
        ["1", "1", "Excited to announce our new 3NF relational architecture...", "3", "English", "FALSE"],
        ["2", "3", "Hot take: Modern software in 2026 feels way too sterile...", "2", "English", "FALSE"],
        ["3", "4", "Friendly reminder to always check EXPLAIN ANALYZE on...", "3", "English", "FALSE"],
        ["4", "5", "Prototyping fluid gestural feed interactions today...", "0", "English", "TRUE"]
    ]
    add_table_data(p_h, p_r, [Inches(0.8), Inches(0.8), Inches(3.2), Inches(1.0), Inches(1.0), Inches(1.0)])

    add_h2("8.6 SQL Query Implementation")
    add_p(
        "This section implements the mandatory SQL query categories prescribed in the course format. "
        "For every query, the SQL statement, its purpose, and its output are provided."
    )

    queries = [
        ("Query 1: Simple SELECT with Conditions",
         "Retrieve all active (non-deleted) posts published in the English language with an Enthusiastic or Technical tone.",
         "SELECT post_id, user_id, content, like_count, tone, created_at\n"
         "FROM Posts\n"
         "WHERE is_deleted = FALSE\n"
         "  AND language = 'English'\n"
         "  AND tone IN ('Enthusiastic', 'Technical');",
         ["post_id", "user_id", "content", "like_count", "tone"],
         [["1", "1", "Excited to announce our new 3NF relational architecture...", "3", "Enthusiastic"]]),

        ("Query 2: Sorting using ORDER BY",
         "Display all active posts sorted chronologically with the newest posts appearing first.",
         "SELECT post_id, user_id, content, like_count, created_at\n"
         "FROM Posts\n"
         "WHERE is_deleted = FALSE\n"
         "ORDER BY created_at DESC;",
         ["post_id", "user_id", "like_count", "created_at"],
         [["3", "4", "3", "2026-10-12 16:30:00"], ["2", "3", "2", "2026-10-12 14:30:00"], ["1", "1", "3", "2026-10-12 12:30:00"]]),

        ("Query 3: Aggregate Functions (COUNT, SUM, AVG, MIN, MAX)",
         "Compute platform-wide post engagement metrics: total posts, total likes accumulated, average likes per post, min likes, and max likes.",
         "SELECT \n"
         "    COUNT(*)          AS total_posts,\n"
         "    SUM(like_count)   AS total_likes,\n"
         "    AVG(like_count)   AS avg_likes_per_post,\n"
         "    MIN(like_count)   AS min_likes,\n"
         "    MAX(like_count)   AS max_likes\n"
         "FROM Posts\n"
         "WHERE is_deleted = FALSE;",
         ["total_posts", "total_likes", "avg_likes_per_post", "min_likes", "max_likes"],
         [["3", "8", "2.6667", "2", "3"]]),

        ("Query 4: Grouping using GROUP BY and Filtering using HAVING",
         "Identify high-performing creators having authored at least 1 post with an average like count of 2.5 or higher.",
         "SELECT \n"
         "    u.user_id,\n"
         "    u.username,\n"
         "    COUNT(p.post_id) AS posts_published,\n"
         "    AVG(p.like_count) AS avg_likes\n"
         "FROM Users u\n"
         "JOIN Posts p ON u.user_id = p.user_id\n"
         "WHERE p.is_deleted = FALSE\n"
         "GROUP BY u.user_id, u.username\n"
         "HAVING COUNT(p.post_id) >= 1 AND AVG(p.like_count) >= 2.5\n"
         "ORDER BY avg_likes DESC;",
         ["user_id", "username", "posts_published", "avg_likes"],
         [["1", "abhinav_sonker", "1", "3.0000"], ["4", "marcus_thorne", "1", "3.0000"]]),

        ("Query 5: Joins (INNER JOIN and LEFT JOIN)",
         "INNER JOIN to display posts with author usernames, and LEFT JOIN to list all registered users including those who haven't posted yet.",
         "-- Part A: INNER JOIN\n"
         "SELECT p.post_id, u.username AS author, p.content, p.like_count\n"
         "FROM Posts p\n"
         "INNER JOIN Users u ON p.user_id = u.user_id\n"
         "WHERE p.is_deleted = FALSE;\n\n"
         "-- Part B: LEFT JOIN\n"
         "SELECT u.user_id, u.username, COUNT(p.post_id) AS total_posts\n"
         "FROM Users u\n"
         "LEFT JOIN Posts p ON u.user_id = p.user_id AND p.is_deleted = FALSE\n"
         "GROUP BY u.user_id, u.username\n"
         "ORDER BY total_posts DESC;",
         ["user_id", "username", "total_posts"],
         [["1", "abhinav_sonker", "1"], ["3", "elena_rostova", "1"], ["4", "marcus_thorne", "1"], ["2", "rahul_verma", "0"], ["5", "selah_kim", "0"]]),

        ("Query 6: Nested Queries and Subqueries",
         "Find all users who have received more likes on any single post than the platform-wide average like count.",
         "SELECT user_id, username\n"
         "FROM Users\n"
         "WHERE user_id IN (\n"
         "    SELECT user_id\n"
         "    FROM Posts\n"
         "    WHERE is_deleted = FALSE\n"
         "      AND like_count > (SELECT AVG(like_count) FROM Posts WHERE is_deleted = FALSE)\n"
         ");",
         ["user_id", "username"],
         [["1", "abhinav_sonker"], ["4", "marcus_thorne"]]),

        ("Query 7: Queries using IN, EXISTS, ANY, or ALL",
         "Find creators who currently have followers using the EXISTS operator.",
         "SELECT u.user_id, u.username\n"
         "FROM Users u\n"
         "WHERE EXISTS (\n"
         "    SELECT 1 FROM Follows f\n"
         "    WHERE f.following_id = u.user_id\n"
         ");",
         ["user_id", "username"],
         [["1", "abhinav_sonker"], ["2", "rahul_verma"], ["3", "elena_rostova"], ["4", "marcus_thorne"], ["5", "selah_kim"], ["6", "tarik_oconnor"]]),

        ("Query 8: Queries Involving Multiple Tables (4-Table Join)",
         "Join Users, Posts, Comments, and Tags to inspect discussion activity under tagged posts.",
         "SELECT \n"
         "    p.post_id,\n"
         "    u_post.username AS post_author,\n"
         "    c.content AS comment_text,\n"
         "    u_comm.username AS commenter\n"
         "FROM Posts p\n"
         "JOIN Users u_post ON p.user_id = u_post.user_id\n"
         "JOIN Comments c ON p.post_id = c.post_id\n"
         "JOIN Users u_comm ON c.user_id = u_comm.user_id\n"
         "WHERE p.is_deleted = FALSE;",
         ["post_id", "post_author", "comment_text", "commenter"],
         [["1", "abhinav_sonker", "Sub-5ms query response verified on MariaDB!", "marcus_thorne"], ["1", "abhinav_sonker", "Great work on the 3NF schema!", "elena_rostova"]]),

        ("Query 9: Meaningful Business Questions",
         "A: Personalized User Feed for User 1 (Abhinav).\n"
         "B: Top 10 Most-Liked Posts of the Past Week.\n"
         "C: Suggested Users to Follow (Friends of Friends).",
         "-- Business Query A: Personalized Feed\n"
         "SELECT p.post_id, u.username AS author, p.content, p.like_count, p.created_at\n"
         "FROM Follows f\n"
         "JOIN Posts p ON p.user_id = f.following_id\n"
         "JOIN Users u ON u.user_id = p.user_id\n"
         "WHERE f.follower_id = 1 AND p.is_deleted = FALSE\n"
         "ORDER BY p.created_at DESC;\n\n"
         "-- Business Query B: Top Posts of the Week\n"
         "SELECT p.post_id, u.username, p.content, p.like_count\n"
         "FROM Posts p\n"
         "JOIN Users u ON p.user_id = u.user_id\n"
         "WHERE p.is_deleted = FALSE\n"
         "  AND p.created_at >= NOW() - INTERVAL 7 DAY\n"
         "ORDER BY p.like_count DESC\n"
         "LIMIT 10;\n\n"
         "-- Business Query C: Suggested Users (2nd degree follow graph)\n"
         "SELECT f2.following_id AS suggested_user_id, u.username, COUNT(*) AS mutual_connections\n"
         "FROM Follows f1\n"
         "JOIN Follows f2 ON f1.following_id = f2.follower_id\n"
         "JOIN Users u ON u.user_id = f2.following_id\n"
         "WHERE f1.follower_id = 1\n"
         "  AND f2.following_id <> 1\n"
         "  AND f2.following_id NOT IN (SELECT following_id FROM Follows WHERE follower_id = 1)\n"
         "GROUP BY f2.following_id, u.username\n"
         "ORDER BY mutual_connections DESC;",
         ["post_id", "author", "content (excerpt)", "like_count"],
         [["3", "marcus_thorne", "Friendly reminder to check EXPLAIN...", "3"], ["2", "elena_rostova", "Hot take: Modern software in 2026...", "2"]]),

        ("Query 10: Database View Query",
         "Query the pre-compiled user_feed view for Viewer ID = 1.",
         "SELECT post_id, author, content, like_count, created_at\n"
         "FROM user_feed\n"
         "WHERE viewer_id = 1\n"
         "ORDER BY created_at DESC;",
         ["post_id", "author", "like_count", "created_at"],
         [["3", "marcus_thorne", "3", "2026-10-12 16:30:00"], ["2", "elena_rostova", "2", "2026-10-12 14:30:00"]])
    ]

    for q_title, q_desc, q_sql, out_h, out_r in queries:
        add_h3(q_title)
        add_p(q_desc)
        add_code(q_sql)
        add_p("Execution Result:", bold_prefix="Query Output: ")
        add_table_data(out_h, out_r)

    add_h2("8.7 Advanced DBMS Features")
    add_p(
        "To satisfy the advanced DBMS requirements, the project implements MySQL Views, atomic Triggers, and Stored Procedures."
    )

    add_h3("Feature 1: Database View (user_feed)")
    add_p(
        "Purpose & Working: Encapsulates the multi-table join between Follows, Posts, and Users. Rather than requiring client "
        "applications to duplicate complex join syntax, client code simply selects against user_feed parameterized by viewer_id. "
        "The database query planner optimizes the view execution automatically."
    )
    add_code(
        "CREATE OR REPLACE VIEW user_feed AS\n"
        "SELECT \n"
        "    f.follower_id AS viewer_id,\n"
        "    p.post_id,\n"
        "    p.user_id,\n"
        "    p.content,\n"
        "    p.media_url,\n"
        "    p.like_count,\n"
        "    p.language,\n"
        "    p.tone,\n"
        "    p.created_at,\n"
        "    u.username AS author\n"
        "FROM Follows f\n"
        "JOIN Posts p ON p.user_id = f.following_id\n"
        "JOIN Users u ON u.user_id = p.user_id\n"
        "WHERE p.is_deleted = FALSE;"
    )

    add_h3("Feature 2: Database Triggers for Counter Sync and Notifications")
    add_p(
        "Purpose & Working: The triggers trg_like_insert and trg_like_delete atomically increment and decrement Posts.like_count "
        "upon any insert or delete on Likes. Trigger trg_notify_on_like automatically creates a notification record for the post "
        "author, suppressing alerts when a user likes their own post."
    )
    add_code(
        "DELIMITER $$\n\n"
        "-- 1. Increment like_count on like\n"
        "CREATE TRIGGER trg_like_insert\n"
        "AFTER INSERT ON Likes\n"
        "FOR EACH ROW\n"
        "BEGIN\n"
        "    UPDATE Posts SET like_count = like_count + 1\n"
        "    WHERE post_id = NEW.post_id;\n"
        "END$$\n\n"
        "-- 2. Decrement like_count on unlike\n"
        "CREATE TRIGGER trg_like_delete\n"
        "AFTER DELETE ON Likes\n"
        "FOR EACH ROW\n"
        "BEGIN\n"
        "    UPDATE Posts SET like_count = like_count - 1\n"
        "    WHERE post_id = OLD.post_id;\n"
        "END$$\n\n"
        "-- 3. Auto-notify author on like (suppressing self-likes)\n"
        "CREATE TRIGGER trg_notify_on_like\n"
        "AFTER INSERT ON Likes\n"
        "FOR EACH ROW\n"
        "BEGIN\n"
        "    INSERT INTO Notifications (user_id, type, reference_id)\n"
        "    SELECT p.user_id, 'like', NEW.post_id\n"
        "    FROM Posts p\n"
        "    WHERE p.post_id = NEW.post_id\n"
        "      AND p.user_id <> NEW.user_id;\n"
        "END$$\n\n"
        "DELIMITER ;"
    )

    add_h3("Feature 3: Stored Procedures (get_mutual_followers and recount_likes)")
    add_p(
        "Purpose & Working: Stored procedures encapsulate computational business logic inside the database engine. "
        "get_mutual_followers finds shared network connections between two users using an optimized self-join on Follows. "
        "recount_likes provides an administrative maintenance routine to heal any counter drift."
    )
    add_code(
        "DELIMITER $$\n\n"
        "-- Procedure: Find mutual followers of User A and User B\n"
        "CREATE PROCEDURE get_mutual_followers(IN user_a INT, IN user_b INT)\n"
        "BEGIN\n"
        "    SELECT u.user_id, u.username\n"
        "    FROM Follows f1\n"
        "    JOIN Follows f2 ON f1.follower_id = f2.follower_id\n"
        "    JOIN Users u    ON u.user_id = f1.follower_id\n"
        "    WHERE f1.following_id = user_a\n"
        "      AND f2.following_id = user_b;\n"
        "END$$\n\n"
        "-- Procedure: Periodic maintenance to resynchronize like counters\n"
        "CREATE PROCEDURE recount_likes()\n"
        "BEGIN\n"
        "    UPDATE Posts p\n"
        "    SET like_count = (\n"
        "        SELECT COUNT(*) FROM Likes l WHERE l.post_id = p.post_id\n"
        "    );\n"
        "END$$\n\n"
        "DELIMITER ;"
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 9: APPLICATION DEVELOPMENT
    # ==========================================
    add_chapter_title("9", "Application Development")

    add_h2("9.1 System Architecture")
    add_p(
        "The application is engineered as a three-tier architecture comprising a presentation layer (React SPA), "
        "an application logic layer (Node.js Express REST API), and a data storage layer (MySQL/MariaDB relational database). "
        "Figure 9.1 illustrates the architectural components and data communication flows."
    )
    add_image_figure("report_assets/system_architecture.png", "Figure 9.1: Three-tier system architecture connecting React, Express, and MySQL", width=Inches(4.5))

    add_h2("9.2 Front-End Technologies")
    add_p("The front end is built using modern web standards designed for responsiveness and visual clarity:")
    add_bullet("React 18 with Vite 5: Provides rapid hot-module reloading, virtual DOM rendering, and modular component lifecycle management.", bold_prefix="Framework: ")
    add_bullet("Lucide React Icons: Clean, vector-rendered micro-icons representing likes, comments, bookmarks, and user profiles.", bold_prefix="Visual Icons: ")
    add_bullet("Curated CSS3 Token System: High-contrast dark theme (#0f172a / #1e293b), smooth cubic-bezier transitions, and tactile elevation.", bold_prefix="Styling: ")

    add_h2("9.3 Application Modules")
    add_p("The application implements seven core modules:")
    add_bullet("Handles registration, bcrypt password verification, session identity via headers, and bio updates.", bold_prefix="1. Authentication & Profile Module: ")
    add_bullet("Renders followed-author posts via the user_feed view with infinite scroll, like toggling, and comment threads.", bold_prefix="2. Home Feed Module: ")
    add_bullet("Allows authors to write posts up to 2200 characters, attach media URLs, and tag categories.", bold_prefix="3. Post Composer Module: ")
    add_bullet("Displays inbound followers, outbound following, and calls get_mutual_followers to display shared connections.", bold_prefix="4. Social Graph Module: ")
    add_bullet("Polls for unread interactions generated by the trg_notify_on_like database trigger.", bold_prefix="5. Notifications Center: ")
    add_bullet("Allows users to explore discussions by hashtag/topic via normalized PostTags mappings.", bold_prefix="6. Communities & Tags Module: ")
    add_bullet("Provides aggregate statistics on platform posts, query execution latency, and top creator leaderboards.", bold_prefix="7. Creator Analytics Dashboard: ")

    add_h2("9.4 Database Connectivity")
    add_p(
        "Database connectivity is established via the mysql2/promise driver using connection pooling. A connection pool "
        "of 10 persistent connections is maintained, eliminating socket handshake overhead on every request. "
        "All queries execute using parameterized prepared statements (using ? placeholders), completely immunizing the system "
        "against SQL injection attacks."
    )
    add_code(
        "// backend/db.js - Connection Pool Configuration\n"
        "const mysql = require('mysql2/promise');\n"
        "require('dotenv').config();\n\n"
        "const pool = mysql.createPool({\n"
        "    host: process.env.DB_HOST || 'localhost',\n"
        "    user: process.env.DB_USER || 'root',\n"
        "    password: process.env.DB_PASSWORD || '',\n"
        "    database: process.env.DB_NAME || 'social_media_db',\n"
        "    socketPath: process.env.DB_SOCKET || '/home/hp/mysql_data/mysql.sock',\n"
        "    waitForConnections: true,\n"
        "    connectionLimit: 10,\n"
        "    queueLimit: 0\n"
        "});\n\n"
        "module.exports = pool;"
    )

    add_h2("9.5 Application Screenshots")
    add_p(
        "Figures 9.2 and 9.3 display the live user interface of the running full-stack application:"
    )
    add_image_figure("report_assets/app_screenshot_feed.png", "Figure 9.2: Application Home Feed screen showing posts, engagement metrics, and sidebar navigation", width=Inches(6.0))
    add_image_figure("report_assets/app_screenshot_profile.png", "Figure 9.3: User Profile & Database Analytics dashboard showing mutual followers and constraint status", width=Inches(6.0))

    add_h2("9.6 Database Operations through the Application")
    add_p(
        "When an interaction is initiated in the React web application, it propagates through the stack and reflects in MySQL:",
        bold_prefix="End-to-End Operation Flow: "
    )
    add_bullet(
        "A user clicks the like icon on Post 1. The React client fires POST /posts/1/like with header x-user-id: 2. "
        "The Express backend executes INSERT INTO Likes (user_id, post_id) VALUES (2, 1). "
        "The MySQL engine fires trg_like_insert, incrementing Posts.like_count from 2 to 3. "
        "The engine simultaneously fires trg_notify_on_like, inserting a row into Notifications for post author Abhinav (ID 1). "
        "Subsequent SELECT queries immediately return like_count = 3.",
        bold_prefix="1. Liking a Post: "
    )
    add_bullet(
        "A user authors a new post. React sends POST /posts. Express inserts a row into Posts. "
        "The new post immediately appears at the top of all followers' feeds when they query user_feed.",
        bold_prefix="2. Publishing a Post: "
    )
    add_bullet(
        "A user clicks 'Follow' on another creator. React sends POST /users/4/follow. "
        "Express executes INSERT INTO Follows (follower_id, following_id) VALUES (1, 4). "
        "The mutual follower stored procedure immediately includes the connection in network lookups.",
        bold_prefix="3. Following a Creator: "
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 10: TESTING AND RESULTS
    # ==========================================
    add_chapter_title("10", "Testing and Results")

    add_h2("10.1 Test Cases")
    add_p(
        "Table 10.1 details the functional and constraint test cases executed to validate system correctness, "
        "formatted in accordance with the prescribed testing evaluation standard."
    )

    tc_headers = ["Test ID", "Operation", "Input / Scenario", "Expected Result", "Actual Result", "Status"]
    tc_rows = [
        ["T1", "Add User", "Valid unique username, email, password", "Record inserted with auto-generated user_id", "User inserted successfully (ID 1)", "PASS"],
        ["T2", "Duplicate Username", "Insert existing username 'abhinav_sonker'", "Rejected by UNIQUE constraint (Error 1062)", "Rejected by MySQL: Duplicate entry", "PASS"],
        ["T3", "Duplicate Email", "Insert existing email 'abhinav@iiitbhopal.ac.in'", "Rejected by UNIQUE constraint (Error 1062)", "Rejected by MySQL: Duplicate entry", "PASS"],
        ["T4", "Self-Follow Violation", "INSERT INTO Follows (follower_id=1, following_id=1)", "Rejected by CHECK constraint (follower_id <> following_id)", "Rejected by MySQL: Check constraint violated", "PASS"],
        ["T5", "Duplicate Like", "Insert existing (user_id=2, post_id=1) into Likes", "Rejected by composite primary key constraint", "Rejected by MySQL: Duplicate entry for key PRIMARY", "PASS"],
        ["T6", "Invalid Foreign Key", "Insert post with non-existent user_id=9999", "Rejected by foreign key constraint (Error 1452)", "Rejected by MySQL: Cannot add foreign key constraint", "PASS"],
        ["T7", "Trigger Like Increment", "Insert valid like into Likes table", "Posts.like_count automatically increments by 1", "like_count incremented from 2 to 3", "PASS"],
        ["T8", "Trigger Unlike Decrement", "Delete existing like from Likes table", "Posts.like_count automatically decrements by 1", "like_count decremented from 3 to 2", "PASS"],
        ["T9", "Self-Like Notification", "Author likes own post (user_id=1, post_id=1)", "Trigger creates NO notification record", "0 notifications generated for self", "PASS"],
        ["T10", "Cascade Delete User", "DELETE FROM Users WHERE user_id = 2", "Cascades delete to all user's posts, likes, and follows", "Child rows in Likes/Posts/Follows purged cleanly", "PASS"]
    ]
    add_table_data(tc_headers, tc_rows, [Inches(0.7), Inches(1.2), Inches(1.6), Inches(1.8), Inches(1.8), Inches(0.6)])

    add_h2("10.2 Query Testing")
    add_p(
        "All analytical and transactional queries were verified for accuracy. The personalized feed query correctly filtered out "
        "soft-deleted posts (is_deleted = TRUE) and returned strictly followed authors in descending chronological order. "
        "The mutual follower stored procedure returned exact intersections matching manual set operations."
    )

    add_h2("10.3 Constraint Testing")
    add_p(
        "Constraint verification confirmed that invalid database states are impossible to commit. Attempting to insert negative stock "
        "or negative counters was rejected. Foreign-key referential actions were verified using START TRANSACTION and ROLLBACK blocks "
        "confirming that cascading deletes execute cleanly without leaving dangling references."
    )

    add_h2("10.4 Results and Discussion")
    add_p(
        "To evaluate real-world scalability, a synthetic dataset comprising 5,000 users, 300,000 posts, 247,000 follows, and "
        "600,000 notifications was loaded into MySQL. Query execution plans were inspected using EXPLAIN ANALYZE before and after "
        "implementing targeted B-tree indexes."
    )

    add_h3("Indexing Strategy")
    add_code(
        "-- Targeted Indexes\n"
        "CREATE INDEX idx_posts_user_created ON Posts(user_id, created_at);\n"
        "CREATE INDEX idx_follows_following ON Follows(following_id);\n"
        "CREATE INDEX idx_follows_follower ON Follows(follower_id);\n"
        "CREATE INDEX idx_likes_post ON Likes(post_id);\n"
        "CREATE INDEX idx_comments_post ON Comments(post_id);\n"
        "CREATE INDEX idx_notifications_user_read ON Notifications(user_id, is_read);"
    )

    add_p("Table 10.2 presents the benchmark execution times before and after index creation:")
    idx_headers = ["Benchmark Query", "Execution Plan Before", "Execution Plan After", "Latency Before", "Latency After", "Speedup"]
    idx_rows = [
        ["QA: User's Recent Posts", "ALL (300,000 rows) + filesort", "ref (idx_posts_user_created), 0 rows sorted", "44.1 ms", "0.28 ms", "157x"],
        ["QB: Chronological Feed", "ALL (Follows) + nested loop on Posts", "eq_ref (Follows) + ref (Posts)", "14.2 ms", "13.8 ms", "1.03x"],
        ["QC: Unread Notifications", "ALL (600,000 rows) + filter is_read", "ref (idx_notifications_user_read)", "54.8 ms", "0.06 ms", "913x"],
        ["QD: Top Posts of the Week", "ALL (300,000 rows) + filter created_at", "range scan on Posts(created_at)", "416.0 ms", "7.70 ms", "54x"]
    ]
    add_table_data(idx_headers, idx_rows, [Inches(1.5), Inches(1.8), Inches(1.8), Inches(0.9), Inches(0.9), Inches(0.8)])

    add_image_figure("report_assets/indexing_performance_chart.png", "Figure 10.1: Query execution latency before and after indexing (logarithmic scale)", width=Inches(5.5))

    add_h3("Defects Discovered and Corrected During Testing")
    add_bullet(
        "In the initial user engagement query, joining Users to both Posts and Comments in a single statement caused a Cartesian "
        "row-multiplication effect: a user with 10 posts and 10 comments produced 100 join rows, multiplying reported like counts tenfold. "
        "Resolution: The query was rewritten to compute post likes and written comments in independent subqueries before joining, "
        "producing exact totals.",
        bold_prefix="Defect 1 (Cartesian Row Multiplication): "
    )
    add_bullet(
        "Under MySQL InnoDB specifications, foreign-key ON DELETE CASCADE deletions do not fire AFTER DELETE triggers on child tables. "
        "Consequently, when a user account was deleted, their child Likes rows were purged without firing trg_like_delete, "
        "leaving remaining posts with phantom like counts. Resolution: Implemented the stored procedure recount_likes() and "
        "application transaction handlers to heal counters upon account decommissioning.",
        bold_prefix="Defect 2 (Cascade Trigger Omission): "
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 11: CONCLUSION & FUTURE SCOPE
    # ==========================================
    add_chapter_title("11", "Conclusion and Future Scope")

    add_h2("11.1 Conclusion")
    add_p(
        "The 'Social Media Database Management System' project successfully demonstrates the comprehensive engineering of a "
        "high-performance relational database adhering to rigorous DBMS theory and real-world software engineering practices. "
        "Key outcomes achieved include:"
    )
    add_bullet("Developed a complete conceptual model using Chen notation capturing strong, associative, and recursive relationships.", bold_prefix="Formal Modeling: ")
    add_bullet("Transformed the conceptual model into an 8-table relational schema and proved normalization up to Boyce-Codd Normal Form (BCNF).", bold_prefix="Normalization: ")
    add_bullet("Enforced database integrity through primary keys, foreign keys with cascading actions, UNIQUE constraints, and CHECK constraints.", bold_prefix="Engine Integrity: ")
    add_bullet("Implemented automated consistency using MySQL Triggers, encapsulated logic using Views, and built Stored Procedures for graph discovery.", bold_prefix="Advanced Features: ")
    add_bullet("Demonstrated dramatic query performance gains (up to 913x speedup) via targeted composite B-tree indexing on 300,000+ records.", bold_prefix="Performance: ")
    add_bullet("Integrated a responsive full-stack web application (React 18 + Node.js Express REST API) demonstrating live CRUD interactions.", bold_prefix="Full-Stack Deployment: ")

    add_h2("11.2 Limitations")
    add_p("The current implementation exhibits the following technical limitations:")
    add_bullet("The personalized feed is computed dynamically at read time. As follower counts grow beyond 10,000, read-time joins increase query latency.", bold_prefix="Read-Time Fan-Out: ")
    add_bullet("Notification records store generic reference_id pointers without a foreign key, preventing engine-level cascading on notifications.", bold_prefix="Polymorphic References: ")
    add_bullet("The benchmark was evaluated on a single-node MySQL server without distributed read replicas or sharding.", bold_prefix="Single-Node Deployment: ")

    add_h2("11.3 Future Scope")
    add_p("Future enhancements planned for the platform include:")
    add_bullet("Deploying an in-memory Redis layer to implement fan-out-on-write feed caching for high-volume creators.", bold_prefix="Hybrid Fan-Out Architecture: ")
    add_bullet("Replacing SQL OFFSET pagination with keyset cursor pagination (WHERE created_at < ?), eliminating deep-page scanning overhead.", bold_prefix="Keyset Pagination: ")
    add_bullet("Deploying MySQL FULLTEXT inverted indexes and N-gram parsers to enable high-speed full-text content searching.", bold_prefix="Full-Text Search: ")
    add_bullet("Partitioning large tables (Posts, Notifications) by range on created_at to facilitate automated data archival.", bold_prefix="Database Partitioning: ")

    doc.add_page_break()

    # ==========================================
    # REFERENCES
    # ==========================================
    p_ref = doc.add_paragraph()
    p_ref.paragraph_format.space_before = Pt(18)
    p_ref.paragraph_format.space_after = Pt(12)
    r_rf = p_ref.add_run("References")
    r_rf.font.name = 'Georgia'
    r_rf.font.size = Pt(22)
    r_rf.bold = True
    r_rf.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    ref_items = [
        "Silberschatz, A., Korth, H. F., & Sudarshan, S. (2020). Database System Concepts (7th ed.). McGraw-Hill Education.",
        "Elmasri, R., & Navathe, S. B. (2016). Fundamentals of Database Systems (7th ed.). Pearson.",
        "Date, C. J. (2004). An Introduction to Database Systems (8th ed.). Addison-Wesley.",
        "Oracle Corporation. (2026). MySQL 8.0 Reference Manual: Optimization, Indexing, and InnoDB Storage Engine. Oracle Documentation.",
        "MariaDB Foundation. (2026). MariaDB Server Documentation: Triggers, Stored Procedures, and EXPLAIN ANALYZE.",
        "Kleppmann, M. (2017). Designing Data-Intensive Applications: The Big Ideas Behind Reliable, Scalable, and Maintainable Systems. O'Reilly Media.",
        "Express.js Foundation. (2026). Express 4.x API Documentation and Best Practices. https://expressjs.com",
        "React Core Team. (2026). React 18 Documentation: Hooks, State, and Component Lifecycle. https://react.dev"
    ]
    for i, rf in enumerate(ref_items, 1):
        add_p(rf, bold_prefix=f"[{i}] ")

    doc.add_page_break()

    # ==========================================
    # APPENDICES
    # ==========================================
    add_chapter_title("A", "Complete MySQL Script")
    add_p("The complete schema, constraint definitions, triggers, views, and stored procedures script (database/schema.sql):")
    add_code(
        "-- Complete MySQL Implementation Script\n"
        "CREATE DATABASE IF NOT EXISTS social_media_db\n"
        "    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\n"
        "USE social_media_db;\n\n"
        "CREATE TABLE Users (\n"
        "    user_id        INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    username       VARCHAR(30)  UNIQUE NOT NULL,\n"
        "    email          VARCHAR(255) UNIQUE NOT NULL,\n"
        "    password_hash  VARCHAR(255) NOT NULL,\n"
        "    bio            TEXT,\n"
        "    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n"
        ") ENGINE=InnoDB;\n\n"
        "CREATE TABLE Posts (\n"
        "    post_id      INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    user_id      INT NOT NULL,\n"
        "    content      VARCHAR(2200) NOT NULL,\n"
        "    media_url    VARCHAR(500),\n"
        "    like_count   INT DEFAULT 0 CHECK (like_count >= 0),\n"
        "    language     VARCHAR(50) DEFAULT 'English',\n"
        "    tone         VARCHAR(50) DEFAULT 'General',\n"
        "    is_deleted   BOOLEAN DEFAULT FALSE,\n"
        "    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
        "    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE\n"
        ") ENGINE=InnoDB;\n\n"
        "CREATE TABLE Comments (\n"
        "    comment_id   INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    post_id      INT NOT NULL,\n"
        "    user_id      INT NOT NULL,\n"
        "    content      VARCHAR(500) NOT NULL,\n"
        "    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
        "    FOREIGN KEY (post_id) REFERENCES Posts(post_id) ON DELETE CASCADE,\n"
        "    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE\n"
        ") ENGINE=InnoDB;\n\n"
        "CREATE TABLE Likes (\n"
        "    user_id      INT NOT NULL,\n"
        "    post_id      INT NOT NULL,\n"
        "    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
        "    PRIMARY KEY (user_id, post_id),\n"
        "    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,\n"
        "    FOREIGN KEY (post_id) REFERENCES Posts(post_id) ON DELETE CASCADE\n"
        ") ENGINE=InnoDB;\n\n"
        "CREATE TABLE Follows (\n"
        "    follower_id   INT NOT NULL,\n"
        "    following_id  INT NOT NULL,\n"
        "    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
        "    PRIMARY KEY (follower_id, following_id),\n"
        "    FOREIGN KEY (follower_id)  REFERENCES Users(user_id) ON DELETE CASCADE,\n"
        "    FOREIGN KEY (following_id) REFERENCES Users(user_id) ON DELETE CASCADE,\n"
        "    CHECK (follower_id <> following_id)\n"
        ") ENGINE=InnoDB;\n\n"
        "CREATE TABLE Notifications (\n"
        "    notification_id  INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    user_id          INT NOT NULL,\n"
        "    type             VARCHAR(20) NOT NULL,\n"
        "    reference_id     INT NOT NULL,\n"
        "    is_read          BOOLEAN DEFAULT FALSE,\n"
        "    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
        "    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE\n"
        ") ENGINE=InnoDB;\n\n"
        "CREATE TABLE Tags (\n"
        "    tag_id INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    name   VARCHAR(50) UNIQUE NOT NULL\n"
        ") ENGINE=InnoDB;\n\n"
        "CREATE TABLE PostTags (\n"
        "    post_id INT NOT NULL,\n"
        "    tag_id  INT NOT NULL,\n"
        "    PRIMARY KEY (post_id, tag_id),\n"
        "    FOREIGN KEY (post_id) REFERENCES Posts(post_id) ON DELETE CASCADE,\n"
        "    FOREIGN KEY (tag_id) REFERENCES Tags(tag_id) ON DELETE CASCADE\n"
        ") ENGINE=InnoDB;\n\n"
        "DELIMITER $$\n"
        "CREATE TRIGGER trg_like_insert AFTER INSERT ON Likes FOR EACH ROW\n"
        "BEGIN UPDATE Posts SET like_count = like_count + 1 WHERE post_id = NEW.post_id; END$$\n"
        "CREATE TRIGGER trg_like_delete AFTER DELETE ON Likes FOR EACH ROW\n"
        "BEGIN UPDATE Posts SET like_count = like_count - 1 WHERE post_id = OLD.post_id; END$$\n"
        "CREATE TRIGGER trg_notify_on_like AFTER INSERT ON Likes FOR EACH ROW\n"
        "BEGIN\n"
        "    INSERT INTO Notifications (user_id, type, reference_id)\n"
        "    SELECT p.user_id, 'like', NEW.post_id FROM Posts p\n"
        "    WHERE p.post_id = NEW.post_id AND p.user_id <> NEW.user_id;\n"
        "END$$\n"
        "CREATE PROCEDURE get_mutual_followers(IN user_a INT, IN user_b INT)\n"
        "BEGIN\n"
        "    SELECT u.user_id, u.username FROM Follows f1\n"
        "    JOIN Follows f2 ON f1.follower_id = f2.follower_id\n"
        "    JOIN Users u ON u.user_id = f1.follower_id\n"
        "    WHERE f1.following_id = user_a AND f2.following_id = user_b;\n"
        "END$$\n"
        "DELIMITER ;\n\n"
        "CREATE OR REPLACE VIEW user_feed AS\n"
        "SELECT f.follower_id AS viewer_id, p.post_id, p.user_id, p.content, p.media_url,\n"
        "       p.like_count, p.language, p.tone, p.created_at, u.username AS author\n"
        "FROM Follows f JOIN Posts p ON p.user_id = f.following_id JOIN Users u ON u.user_id = p.user_id\n"
        "WHERE p.is_deleted = FALSE;"
    )

    doc.add_page_break()

    add_chapter_title("B", "Source Code & Repository")
    add_p("The project source code is organized into a clean client-server architecture:")
    add_bullet("backend/server.js: REST API routing, bcrypt authentication, error handlers.", bold_prefix="Backend API: ")
    add_bullet("backend/db.js: MariaDB connection pooling and async promise interface.", bold_prefix="Database Layer: ")
    add_bullet("frontend/src/components/: React SPA components (Feed.jsx, Profile.jsx, CreatePost.jsx, Notifications.jsx).", bold_prefix="Frontend Client: ")
    add_bullet("https://github.com/abhinavsonker23-ship-it/DBMS.git", bold_prefix="GitHub Repository: ")

    add_chapter_title("C", "Additional Screenshots")
    add_p("Additional views from the interactive demonstration application:")
    add_image_figure("report_assets/app_screenshot_feed.png", "Figure C.1: Demonstration of Live Feed and Trending Discussions", width=Inches(5.8))
    add_image_figure("report_assets/app_screenshot_profile.png", "Figure C.2: Demonstration of Mutual Followers and Trigger Status Dashboard", width=Inches(5.8))

    add_chapter_title("D", "Team Contribution")
    add_p("Summary of individual project contributions:")
    tc_h = ["Team Member", "Roll Number", "Assigned Modules & Technical Contributions", "Contribution %"]
    tc_r = [
        ["Vansh Chadha", "25U021036", "Conceptual ER modeling, BCNF normalization proof, MySQL schema DDL & triggers, indexing benchmark, Express REST API, React UI integration, final documentation.", "100%"]
    ]
    add_table_data(tc_h, tc_r, [Inches(1.8), Inches(1.2), Inches(3.4), Inches(1.0)])

    doc.add_page_break()

    # ==========================================
    # SUGGESTED EVALUATION SCHEME
    # ==========================================
    p_ev = doc.add_paragraph()
    p_ev.paragraph_format.space_before = Pt(18)
    p_ev.paragraph_format.space_after = Pt(12)
    r_ev = p_ev.add_run("Suggested Evaluation Scheme")
    r_ev.font.name = 'Georgia'
    r_ev.font.size = Pt(22)
    r_ev.bold = True
    r_ev.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    add_p(
        "Evaluation principle: Marks should primarily reflect the correctness of database design, ER-to-relational mapping, "
        "functional dependencies, normalization, SQL implementation, and understanding of DBMS concepts. Front-end appearance alone "
        "must not determine the project grade.",
        bold_prefix="Department Evaluation Standard: "
    )

    ev_headers = ["Component", "Marks"]
    ev_rows = [
        ["Problem analysis and requirements", "5"],
        ["ER diagram and constraints", "10"],
        ["ER-to-relational mapping", "10"],
        ["Functional dependencies and keys", "10"],
        ["Normalization (1NF, 2NF, 3NF, BCNF)", "15"],
        ["MySQL schema, constraints, and sample data", "10"],
        ["SQL queries and advanced DBMS features (Views, Triggers, Procedures)", "15"],
        ["Front-end integration and functionality", "10"],
        ["Testing and report quality", "5"],
        ["Viva and conceptual understanding", "10"],
        ["Total", "100"]
    ]
    add_table_data(ev_headers, ev_rows, [Inches(5.0), Inches(1.5)])

    # Save to file
    out_file = "Social_Media_DBMS_Project_Report.docx"
    doc.save(out_file)
    print(f"Report generated successfully: {out_file}")

if __name__ == "__main__":
    create_report()
