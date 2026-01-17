from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.barcode import qr

from datetime import datetime
import os
import random  # For mock grades

# Custom colors for the college theme
COLLEGE_PRIMARY = colors.HexColor('#1a237e')  # Deep blue
COLLEGE_SECONDARY = colors.HexColor('#0d47a1')  # Medium blue
COLLEGE_ACCENT = colors.HexColor('#ffd700')  # Gold
COLLEGE_LIGHT = colors.HexColor('#e8eaf6')  # Light blue
COLLEGE_SUCCESS = colors.HexColor('#2e7d32')  # Green
COLLEGE_DANGER = colors.HexColor('#c62828')  # Red
COLLEGE_WARNING = colors.HexColor('#f57c00')  # Orange

def draw_watermark_and_header(canvas, doc):
    """Draws watermark and static elements on every page"""
    canvas.saveState()
    
    # WATERMARK
    canvas.setFont('Helvetica-Bold', 60)
    canvas.setFillColor(colors.lightgrey, alpha=0.1)
    canvas.translate(A4[0]/2, A4[1]/2)
    canvas.rotate(45)
    canvas.drawCentredString(0, 0, "SETHUPATHY COLLEGE")
    canvas.restoreState()
    
    # FOOTER DECORATION (Static on all pages if needed, but handled in flowables mostly)
    # We can add page numbers here if desired
    canvas.saveState()
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(colors.gray)
    page_num = f"Page {doc.page}"
    canvas.drawRightString(A4[0]-50, 30, page_num)
    canvas.restoreState()

def generate_student_report_pdf(student, output_dir='static/reports', host_url='http://127.0.0.1:5000/'):
    """
    Generate a comprehensive PDF report for a student including:
    - Personal information
    - Attendance summary and visualization
    - Subject enrollment and academic performance
    - QR Verification with Photo
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'student_report_{student.umis}_{timestamp}.pdf'
    filepath = os.path.join(output_dir, filename)
    
    # Create PDF document with custom page template
    doc = SimpleDocTemplate(
        filepath, 
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )
    elements = []
    styles = getSampleStyleSheet()
    
    # ===== CUSTOM STYLES =====
    
    # College name style
    college_name_style = ParagraphStyle(
        'CollegeName',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=COLLEGE_PRIMARY,
        spaceAfter=4,
        alignment=TA_LEFT, # Changed to Left for layout with photo
        fontName='Helvetica-Bold',
        leading=22
    )
    
    # College subtitle style
    college_subtitle_style = ParagraphStyle(
        'CollegeSubtitle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=COLLEGE_SECONDARY,
        spaceAfter=8,
        alignment=TA_LEFT,
        fontName='Helvetica',
        leading=11
    )
    
    # Report title style
    report_title_style = ParagraphStyle(
        'ReportTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.white,
        spaceAfter=20,
        spaceBefore=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        leading=20
    )
    
    # Section heading style
    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=COLLEGE_PRIMARY,
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold',
        borderWidth=0,
        borderColor=COLLEGE_ACCENT,
        borderPadding=5,
        leftIndent=0,
        leading=16
    )
    
    # ===== HEADER SECTION (Refined UI & Fix QR) =====
    
    # 1. Student Photo Handling
    photo_path = os.path.join('static', 'student_photos', f'{student.umis}.jpg')
    if not os.path.exists(photo_path):
        photo_path = os.path.join('static', 'student_photos', f'{student.umis}.png')
         
    if os.path.exists(photo_path):
        # Resize maintaining aspect ratio? ReportLab Image simply stretches to w/h
        student_photo = Image(photo_path, 1.1*inch, 1.1*inch)
    else:
        student_photo = Paragraph("<br/><br/><b>NO PHOTO</b>", ParagraphStyle('NoPhoto', parent=styles['Normal'], alignment=TA_CENTER, fontSize=8))

    # 2. QR Code Generation (Linked to Verification URL)
    verify_url = f"{host_url}verify/{student.umis}"
    qr_code = qr.QrCodeWidget(verify_url)
    qr_code.barWidth = 1.5
    qr_code.barHeight = 1.5
    qr_code.qrVersion = 2 
    # Ensure it's scannable
    
    d_qr = Drawing(60, 60) 
    d_qr.add(qr_code)
    
    # 3. Header Layout Table: [Photo | College Details | QR Code]
    # We use a white background for Photo and QR slots so they pop out, 
    # and Blue for the center text.
    header_content = [
        [
            student_photo,
            [
                Paragraph('<b>SETHUPATHY GOVERNMENT ARTS COLLEGE</b>', ParagraphStyle('H_Title', parent=college_name_style, textColor=colors.white)),
                Paragraph('<i>(Autonomous) | Affiliated to Madurai Kamaraj University</i><br/>Ramanathapuram - 623 501, Tamil Nadu', ParagraphStyle('H_Sub', parent=college_subtitle_style, textColor=colors.HexColor('#e0e0e0')))
            ],
            d_qr
        ]
    ]
    
    header_table = Table(header_content, colWidths=[1.3*inch, 4.0*inch, 1.3*inch])
    header_table.setStyle(TableStyle([
        # Center Column (Text): Deep Blue
        ('BACKGROUND', (1, 0), (1, 0), COLLEGE_PRIMARY),
        
        # Side Columns (Photo & QR): White for contrast
        ('BACKGROUND', (0, 0), (0, 0), colors.white),
        ('BACKGROUND', (2, 0), (2, 0), colors.white),
        
        # Alignment
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'), # All content centered horizontally in cells
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        
        # Padding
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        
        # Borders: Box around the whole thing?
        ('BOX', (0, 0), (-1, -1), 2, COLLEGE_PRIMARY),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey), # Inner grid
    ]))
    elements.append(header_table)
    
    # Decorative line
    line_data = [['']]
    line_table = Table(line_data, colWidths=[6.5*inch])
    line_table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 3, COLLEGE_ACCENT),
        ('LINEBELOW', (0, 0), (-1, 0), 1, COLLEGE_SECONDARY),
    ]))
    elements.append(line_table)
    elements.append(Spacer(1, 0.15*inch))
    
    # Report title banner
    report_title_data = [[
        Paragraph('STUDENT ACADEMIC REPORT', report_title_style)
    ]]
    
    report_title_table = Table(report_title_data, colWidths=[6.5*inch])
    report_title_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLLEGE_SECONDARY),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('ROUNDEDCORNERS', [5, 5, 5, 5]),
    ]))
    elements.append(report_title_table)
    elements.append(Spacer(1, 0.25*inch))
    
    # Student Information Section
    section_header = Paragraph("📋 STUDENT INFORMATION", heading_style)
    elements.append(section_header)
    
    student_data = [
        ['UMIS Number:', student.umis],
        ['Full Name:', student.name],
        ['Email Address:', student.email or 'Not Provided'],
        ['Phone Number:', student.phone or 'Not Provided'],
        ['Department:', student.department.name if student.department else 'Not Assigned'],
        ['Current Year:', f'Year {student.current_year}' if student.current_year else 'Not Specified'],
        ['Parent/Guardian Contact:', student.parents_num or 'Not Provided']
    ]
    
    student_table = Table(student_data, colWidths=[2.2*inch, 4.3*inch])
    student_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), COLLEGE_LIGHT),
        ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (0, -1), COLLEGE_PRIMARY),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#b0bec5')),
        ('BOX', (0, 0), (-1, -1), 2, COLLEGE_SECONDARY),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(student_table)
    elements.append(Spacer(1, 0.35*inch))
    
    # Attendance Summary & Visual Charts
    from models import Attendance
    attendance_records = Attendance.query.filter_by(student_umis=student.umis).order_by(Attendance.date.desc()).all()
    
    total_days = len(attendance_records)
    present_count = sum(1 for a in attendance_records if a.status == 'Present')
    absent_count = sum(1 for a in attendance_records if a.status == 'Absent')
    leave_count = sum(1 for a in attendance_records if a.status == 'Leave')
    attendance_pct = (present_count / total_days * 100) if total_days > 0 else 0
    
    # Determine attendance status color
    if attendance_pct >= 75:
        pct_color = COLLEGE_SUCCESS
        status_text = "Excellent"
    elif attendance_pct >= 60:
        pct_color = COLLEGE_WARNING
        status_text = "Satisfactory"
    else:
        pct_color = COLLEGE_DANGER
        status_text = "Needs Improvement"
    
    elements.append(Paragraph("📊 ATTENDANCE SUMMARY & TRENDS", heading_style))
    
    # --- Pie Chart Drawing ---
    if total_days > 0:
        d_pie = Drawing(200, 100)
        pc = Pie()
        pc.x = 50
        pc.y = 10
        pc.width = 80
        pc.height = 80
        pc.data = [present_count, absent_count, leave_count]
        pc.labels = ['Present', 'Absent', 'Leave']
        
        # Colors: Present=Green, Absent=Red, Leave=Orange
        pc.slices.strokeWidth = 0.5
        pc.slices[0].fillColor = COLLEGE_SUCCESS
        pc.slices[1].fillColor = COLLEGE_DANGER
        pc.slices[2].fillColor = COLLEGE_WARNING
        
        d_pie.add(pc)
    else:
        d_pie = Paragraph("(No data for visual chart)", styles['Normal'])

    # Attendance statistics table
    summary_data = [
        ['Total Days', 'Present', 'Absent', 'Leave', 'Percentage', 'Status'],
        [
            str(total_days), 
            str(present_count), 
            str(absent_count), 
            str(leave_count), 
            f'{attendance_pct:.1f}%',
            status_text
        ]
    ]
    
    summary_table = Table(summary_data, colWidths=[1.05*inch]*6)
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLLEGE_PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 1), (0, 1), colors.HexColor('#e3f2fd')),
        ('BACKGROUND', (1, 1), (1, 1), colors.HexColor('#e8f5e9')),
        ('BACKGROUND', (2, 1), (2, 1), colors.HexColor('#ffebee')),
        ('BACKGROUND', (3, 1), (3, 1), colors.HexColor('#fff3e0')),
        ('BACKGROUND', (4, 1), (4, 1), pct_color),
        ('BACKGROUND', (5, 1), (5, 1), pct_color),
        ('TEXTCOLOR', (0, 1), (3, 1), colors.black),
        ('TEXTCOLOR', (4, 1), (5, 1), colors.white),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1.5, colors.white),
        ('BOX', (0, 0), (-1, -1), 2, COLLEGE_SECONDARY),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))

    # Arrange Table and Chart side by side (roughly)
    # We can just append them sequentially for simplicity in layout, or use a Table to hold them
    elements.append(summary_table)
    elements.append(Spacer(1, 0.1*inch))
    
    if total_days > 0:
        # Chart legend/container
        chart_table = Table([[d_pie, Paragraph("<b>Visual Representation</b><br/>Attendance Distribution", styles['Normal'])]], colWidths=[3*inch, 3*inch])
        chart_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(chart_table)

    elements.append(Spacer(1, 0.35*inch))
    
    # ===== ACADEMIC SUBJECTS & MARKS SECTION =====
    elements.append(Paragraph("📚 ACADEMIC SUBJECTS & PERFORMANCE", heading_style))
    
    from models import Subject
    # Fetch subjects (Mocking semester logic if not explicit)
    enrolled_subjects = []
    if student.department_id and student.current_year:
        # Assuming student takes all subjects for their year
        enrolled_subjects = Subject.query.filter_by(
            department_id=student.department_id, 
            year=student.current_year
        ).all()
        
    if enrolled_subjects:
        # Table Header
        acad_data = [['Subject Code', 'Subject Name', 'Credits', 'Grade', 'Remarks']]
        
        # Populate with subjects and MOCK grades
        total_credits = 0
        total_points = 0
        
        grades = ['O', 'D+', 'D', 'A+', 'A', 'B', 'U'] # Outstanding to Unsatisfactory
        
        for subj in enrolled_subjects:
            # Mock Data Generation
            mock_credits = random.choice([3, 4])
            mock_grade = random.choice(grades)
            remarks = "Completed" if mock_grade != 'U' else "Re-appear"
            
            acad_data.append([
                subj.code,
                subj.name,
                str(mock_credits),
                mock_grade,
                remarks
            ])
            
        acad_table = Table(acad_data, colWidths=[1.2*inch, 2.8*inch, 0.8*inch, 0.8*inch, 1.2*inch])
        acad_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), COLLEGE_SECONDARY),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'), # Subject Name Left Aligned
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#eeeeee')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('BOX', (0, 0), (-1, -1), 1, COLLEGE_SECONDARY),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(acad_table)
    else:
        elements.append(Paragraph("No subject enrollment records found for this academic year.", styles['Italic']))

    elements.append(Spacer(1, 0.35*inch))

    # Day-by-Day Attendance Records (Simplified for brevity if we have charts, but keeping as requested)
    if attendance_records:
        elements.append(Paragraph("📅 DETAILED ATTENDANCE LOG", heading_style))
        
        records_to_show = attendance_records[:20] # reduced count to fit new sections
        attendance_data = [['S.No', 'Date', 'Day', 'Status']]
        
        for idx, record in enumerate(records_to_show, 1):
            date_str = record.date.strftime('%d-%b-%Y')
            day_str = record.date.strftime('%A')
            attendance_data.append([str(idx), date_str, day_str, record.status])
        
        attendance_table = Table(attendance_data, colWidths=[0.6*inch, 1.8*inch, 1.6*inch, 1.5*inch])
        
        # Build style list dynamically
        table_style = [
            ('BACKGROUND', (0, 0), (-1, 0), COLLEGE_PRIMARY),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#b0bec5')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
            ('BOX', (0, 0), (-1, -1), 2, COLLEGE_SECONDARY),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
        ]
        
        for idx, record in enumerate(records_to_show, 1):
            if record.status == 'Present':
                table_style.append(('TEXTCOLOR', (3, idx), (3, idx), COLLEGE_SUCCESS))
            elif record.status == 'Absent':
                table_style.append(('TEXTCOLOR', (3, idx), (3, idx), COLLEGE_DANGER))
            elif record.status == 'Leave':
                table_style.append(('TEXTCOLOR', (3, idx), (3, idx), COLLEGE_WARNING))
        
        attendance_table.setStyle(TableStyle(table_style))
        elements.append(attendance_table)
        
        if len(attendance_records) > 20:
            elements.append(Paragraph(f"...and {len(attendance_records)-20} more records available online.", styles['Italic']))
    
    # Footer Section
    elements.append(Spacer(1, 0.5*inch))
    
    # Decorative line before footer
    footer_line_data = [['']]
    footer_line_table = Table(footer_line_data, colWidths=[6.5*inch])
    footer_line_table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 2, COLLEGE_ACCENT),
    ]))
    elements.append(footer_line_table)
    elements.append(Spacer(1, 0.15*inch))
    
    # Footer text with disclaimer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#546e7a'),
        alignment=TA_CENTER,
        leading=10
    )
    
    footer_text = f"""
    <b>Report Generated:</b> {datetime.now().strftime('%d %B %Y at %I:%M %p')} | <b>Verification ID:</b> {student.umis}-{random.randint(1000,9999)}<br/>
    <b>Sethupathy Government Arts College</b> (Autonomous) | Ramanathapuram<br/>
    <i>Scan the QR Code to verify authenticity online. | Student Management System v2.0</i><br/>
    This is a computer-generated document and does not require a signature.
    """
    footer = Paragraph(footer_text, footer_style)
    elements.append(footer)
    
    # Build PDF with Watermark and Header callbacks
    doc.build(elements, onFirstPage=draw_watermark_and_header, onLaterPages=draw_watermark_and_header)
    
    return filepath


def generate_batch_report_pdf(students_data, output_path='static/reports/batch_report.pdf', 
                              report_title=None, hod_sign=True, principal_sign=False):
    """
    Generate a PDF report for multiple students with college header.
    students_data: list of dicts with student info, attendance %, and marks.
    report_title: Custom title for the report (optional).
    hod_sign: Include HOD signature block.
    principal_sign: Include Principal signature block.
    """
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    import os
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    doc = SimpleDocTemplate(output_path, pagesize=landscape(A4), rightMargin=30, leftMargin=30, topMargin=40, bottomMargin=30)
    elements = []
    styles = getSampleStyleSheet()
    
    # --- HEADER ---
    header_style = ParagraphStyle('Header', parent=styles['Heading1'], fontSize=16, textColor=COLLEGE_PRIMARY, alignment=TA_CENTER, spaceAfter=4)
    sub_header_style = ParagraphStyle('SubHeader', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#555555'), alignment=TA_CENTER, spaceAfter=15)
    
    elements.append(Paragraph("<b>SETHUPATHY GOVERNMENT ARTS COLLEGE</b>", header_style))
    elements.append(Paragraph("Ramanathapuram - 623501 | (Autonomous)", sub_header_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Custom or default title
    title_text = report_title if report_title else "STUDENT BATCH REPORT"
    elements.append(Paragraph(f"<b>{title_text.upper()}</b>", ParagraphStyle('Title', parent=styles['Heading2'], alignment=TA_CENTER, textColor=COLLEGE_SECONDARY)))
    elements.append(Spacer(1, 0.3*inch))
    
    # --- TABLE ---
    table_data = [['S.No', 'Roll No', 'Name', 'Email', 'Department', 'Year', 'Attendance %', 'Marks Summary']]
    
    for idx, s in enumerate(students_data, 1):
        marks_str = ', '.join([f"{m['subject']}: {m['marks']}" for m in s.get('marks', [])]) or '-'
        table_data.append([
            str(idx),
            s.get('roll_number', 'N/A'),
            s.get('name', ''),
            s.get('email', ''),
            s.get('department', ''),
            s.get('year', ''),
            f"{s.get('attendance_pct', 0):.1f}%",
            marks_str[:50] + ('...' if len(marks_str) > 50 else '')
        ])
    
    col_widths = [0.4*inch, 0.9*inch, 1.8*inch, 2.2*inch, 1.5*inch, 0.5*inch, 0.9*inch, 2.5*inch]
    
    batch_table = Table(table_data, colWidths=col_widths, repeatRows=1)
    batch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLLEGE_PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (2, 1), (3, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
        ('BOX', (0, 0), (-1, -1), 1.5, COLLEGE_SECONDARY),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(batch_table)
    
    # --- SIGNATURE BLOCKS ---
    elements.append(Spacer(1, 0.6*inch))
    
    sign_style_left = ParagraphStyle('SignLeft', parent=styles['Normal'], fontSize=10, alignment=TA_LEFT)
    sign_style_right = ParagraphStyle('SignRight', parent=styles['Normal'], fontSize=10, alignment=TA_RIGHT)
    
    sign_row = []
    if hod_sign:
        sign_row.append(Paragraph("<br/><br/>_____________________<br/><b>Head of Department</b>", sign_style_left))
    else:
        sign_row.append(Paragraph("", sign_style_left))
        
    if principal_sign:
        sign_row.append(Paragraph("<br/><br/>_____________________<br/><b>Principal</b>", sign_style_right))
    else:
        sign_row.append(Paragraph("", sign_style_right))
    
    if hod_sign or principal_sign:
        sign_table = Table([sign_row], colWidths=[5*inch, 5*inch])
        sign_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        elements.append(sign_table)
    
    # --- FOOTER ---
    elements.append(Spacer(1, 0.4*inch))
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.gray, alignment=TA_CENTER)
    elements.append(Paragraph(f"Generated on {datetime.now().strftime('%d %B %Y at %I:%M %p')} | Student Management System", footer_style))
    
    doc.build(elements)
    return output_path

