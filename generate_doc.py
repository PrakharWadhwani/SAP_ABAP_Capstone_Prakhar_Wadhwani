from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, HRFlowable)
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
from reportlab.platypus.flowables import KeepTogether

PAGE_W, PAGE_H = A4
MARGIN = 2.5 * cm

DARK_BLUE   = HexColor('#1F3864')
MID_BLUE    = HexColor('#2E75B6')
LIGHT_BLUE  = HexColor('#D6E4F7')
ACCENT      = HexColor('#ED7D31')
LIGHT_GRAY  = HexColor('#F5F7FA')
MID_GRAY    = HexColor('#BFBFBF')
TEXT_COLOR  = HexColor('#1A1A2E')

def make_styles():
    base = getSampleStyleSheet()

    heading1 = ParagraphStyle('H1',
        fontName='Helvetica-Bold', fontSize=15,
        textColor=white, alignment=TA_LEFT,
        spaceAfter=4, spaceBefore=10,
        leftIndent=8, leading=20)

    heading2 = ParagraphStyle('H2',
        fontName='Helvetica-Bold', fontSize=14,
        textColor=DARK_BLUE, alignment=TA_LEFT,
        spaceAfter=4, spaceBefore=8, leading=18)

    body = ParagraphStyle('Body',
        fontName='Helvetica', fontSize=12,
        textColor=TEXT_COLOR, alignment=TA_JUSTIFY,
        spaceAfter=6, leading=16)

    code = ParagraphStyle('Code',
        fontName='Courier', fontSize=9,
        textColor=HexColor('#1A1A2E'), alignment=TA_LEFT,
        spaceAfter=4, leading=13,
        backColor=LIGHT_GRAY, leftIndent=10, rightIndent=10,
        borderPad=6)

    label = ParagraphStyle('Label',
        fontName='Helvetica-Bold', fontSize=12,
        textColor=DARK_BLUE, alignment=TA_LEFT,
        spaceAfter=2, leading=15)

    footer_style = ParagraphStyle('Footer',
        fontName='Helvetica', fontSize=9,
        textColor=MID_GRAY, alignment=TA_CENTER)

    return dict(h1=heading1, h2=heading2, body=body,
                code=code, label=label, footer=footer_style)

def section_header(title, styles):
    """Returns a colored section header block."""
    data = [[Paragraph(title, styles['h1'])]]
    tbl = Table(data, colWidths=[PAGE_W - 2*MARGIN])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DARK_BLUE),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
    ]))
    return tbl

def info_table(rows, styles):
    col_w = [(PAGE_W - 2*MARGIN) * 0.35, (PAGE_W - 2*MARGIN) * 0.65]
    data = [[Paragraph(k, styles['label']), Paragraph(v, styles['body'])]
            for k, v in rows]
    tbl = Table(data, colWidths=col_w)
    tbl.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (0,-1), LIGHT_BLUE),
        ('BACKGROUND',    (1,0), (1,-1), white),
        ('GRID',          (0,0), (-1,-1), 0.5, MID_GRAY),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return tbl

def on_page(canvas, doc):
    """Draw header stripe and page number on every page."""
    canvas.saveState()
    # top accent bar
    canvas.setFillColor(DARK_BLUE)
    canvas.rect(0, PAGE_H - 1.1*cm, PAGE_W, 1.1*cm, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont('Helvetica-Bold', 10)
    canvas.drawString(MARGIN, PAGE_H - 0.72*cm,
                      'Capstone Project | Z_VENDOR_INVOICE_REPORT | SAP ABAP')

    # bottom bar with page number (bottom-right as required)
    canvas.setFillColor(LIGHT_GRAY)
    canvas.rect(0, 0, PAGE_W, 1.0*cm, fill=1, stroke=0)
    canvas.setFillColor(MID_GRAY)
    canvas.setFont('Helvetica', 9)
    canvas.drawString(MARGIN, 0.35*cm, '[YOUR NAME] | [ROLL NO] | [BATCH/PROGRAM]')
    canvas.setFillColor(DARK_BLUE)
    canvas.setFont('Helvetica-Bold', 9)
    canvas.drawRightString(PAGE_W - MARGIN, 0.35*cm, f'Page {doc.page}')
    canvas.restoreState()

def build_pdf(output_path):
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            leftMargin=MARGIN, rightMargin=MARGIN,
                            topMargin=1.6*cm, bottomMargin=1.4*cm)
    styles = make_styles()
    story  = []

    # ------------------------------------------------------------------ #
    #  COVER / TITLE BLOCK
    # ------------------------------------------------------------------ #
    story.append(Spacer(1, 1.5*cm))
    cover_data = [[
        Paragraph('CAPSTONE PROJECT', ParagraphStyle('ct',
            fontName='Helvetica-Bold', fontSize=13, textColor=MID_BLUE,
            alignment=TA_CENTER)),
    ],[
        Paragraph('Custom ALV Report for<br/>Vendor Invoice Analysis',
            ParagraphStyle('ct2', fontName='Helvetica-Bold', fontSize=22,
                           textColor=DARK_BLUE, alignment=TA_CENTER, leading=28)),
    ],[
        Paragraph('SAP ABAP | Program: <b>Z_VENDOR_INVOICE_REPORT</b>',
            ParagraphStyle('ct3', fontName='Helvetica', fontSize=12,
                           textColor=MID_BLUE, alignment=TA_CENTER)),
    ]]
    cover_tbl = Table(cover_data, colWidths=[PAGE_W - 2*MARGIN])
    cover_tbl.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), LIGHT_BLUE),
        ('TOPPADDING',    (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LEFTPADDING',   (0,0), (-1,-1), 20),
        ('RIGHTPADDING',  (0,0), (-1,-1), 20),
        ('LINEABOVE',     (0,0), (-1,0),  3, ACCENT),
        ('LINEBELOW',     (0,-1),(-1,-1), 3, ACCENT),
    ]))
    story.append(cover_tbl)
    story.append(Spacer(1, 0.5*cm))

    # Mandatory student details table
    story.append(info_table([
        ('Student Name',    '[YOUR FULL NAME]'),
        ('Roll Number',     '[YOUR ROLL NUMBER]'),
        ('Batch / Program', '[YOUR BATCH / PROGRAM NAME]'),
        ('Submission Date', 'April 21, 2026'),
        ('Program ID',      'Z_VENDOR_INVOICE_REPORT'),
    ], styles))
    story.append(Spacer(1, 0.6*cm))

    # ------------------------------------------------------------------ #
    # 1. TITLE & PROBLEM STATEMENT
    # ------------------------------------------------------------------ #
    story.append(section_header('1.  Title & Problem Statement', styles))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('<b>Project Title:</b> Custom ALV Report for Vendor Invoice Analysis in SAP ABAP', styles['body']))
    story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph(
        'In any SAP-based enterprise, the Accounts Payable (AP) department processes hundreds '
        'of vendor invoices every day. Finance teams require a consolidated, real-time view of '
        'both <i>open</i> (unpaid) and <i>cleared</i> (paid) vendor invoices — including invoice '
        'amounts, posting dates, payment terms, and clearing details — to manage cash flow and '
        'vendor relationships effectively.',
        styles['body']))
    story.append(Paragraph(
        'SAP does not provide a single standard report that combines open items (BSIK) and '
        'cleared items (BSAK) with vendor master data (LFA1) in a flexible, ALV-based output. '
        'Finance controllers must individually check transactions FK10N, FBL1N, and ME23N, '
        'causing manual effort and delays.',
        styles['body']))
    story.append(Paragraph(
        '<b>Problem:</b> There is no unified, filterable, and exportable vendor invoice report in '
        'the standard SAP system that covers both open and cleared invoices with vendor names, '
        'payment status, and subtotals per vendor — accessible to business users without '
        'technical knowledge.',
        styles['body']))
    story.append(Spacer(1, 0.4*cm))

    # ------------------------------------------------------------------ #
    # 2. SOLUTION & FEATURES
    # ------------------------------------------------------------------ #
    story.append(section_header('2.  Solution & Key Features', styles))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph(
        'A custom ABAP report <b>Z_VENDOR_INVOICE_REPORT</b> was developed using the '
        '<b>REUSE_ALV_GRID_DISPLAY</b> function module. The program fetches data from '
        'SAP standard tables, enriches it with vendor master information, and presents a '
        'consolidated, interactive ALV grid output.',
        styles['body']))
    story.append(Spacer(1, 0.2*cm))

    features = [
        ['Feature', 'Description'],
        ['Selection Screen', 'Flexible filters: Company Code, Vendor, Date range, Fiscal Year, Document Type'],
        ['Open + Cleared Items', 'Checkboxes to include BSIK (open) and BSAK (cleared) items independently'],
        ['Vendor Name Enrichment', 'Joins LFA1 master table to display Vendor Name alongside Vendor Number'],
        ['ALV Grid Output', 'Sortable, filterable, color-striped ALV grid with column-width optimization'],
        ['Subtotals & Grand Total', 'Automatic subtotals per Company Code and Vendor; Grand Total row at bottom'],
        ['Payment Status Column', 'Clearly labels each row as "Open" or "Cleared" for instant visibility'],
        ['Double-Click Navigation', 'Double-clicking any row opens the FI document directly in FB03'],
        ['Display Variant', 'Users can save and reload personalized column layouts via ALV variants'],
        ['Export Ready', 'Built-in ALV toolbar allows export to Excel, PDF, and print'],
    ]
    feat_tbl = Table(features, colWidths=[(PAGE_W-2*MARGIN)*0.30, (PAGE_W-2*MARGIN)*0.70])
    feat_tbl.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0),  DARK_BLUE),
        ('TEXTCOLOR',     (0,0), (-1,0),  white),
        ('FONTNAME',      (0,0), (-1,0),  'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (-1,-1), 10),
        ('BACKGROUND',    (0,1), (-1,-1), white),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [white, LIGHT_GRAY]),
        ('GRID',          (0,0), (-1,-1), 0.5, MID_GRAY),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(feat_tbl)
    story.append(Spacer(1, 0.4*cm))

    # ------------------------------------------------------------------ #
    # 3. TECH STACK
    # ------------------------------------------------------------------ #
    story.append(section_header('3.  Tech Stack', styles))
    story.append(Spacer(1, 0.3*cm))

    tech = [
        ['Component', 'Details'],
        ['Language',          'ABAP (Advanced Business Application Programming)'],
        ['SAP Platform',      'SAP ECC 6.0 / SAP S/4HANA'],
        ['Key Tables',        'BSIK (AP Open Items), BSAK (AP Cleared Items), LFA1 (Vendor Master)'],
        ['ALV Function',      'REUSE_ALV_GRID_DISPLAY (SAP List Viewer)'],
        ['Include Library',   'SLIS (SAP List Viewer Utilities)'],
        ['Transaction Used',  'SE38 (ABAP Editor), FB03 (FI Document Display)'],
        ['SAP Module',        'FI-AP (Financial Accounting – Accounts Payable)'],
        ['Development Class', 'ZFIN (Custom Finance Development)'],
    ]
    tech_tbl = Table(tech, colWidths=[(PAGE_W-2*MARGIN)*0.30, (PAGE_W-2*MARGIN)*0.70])
    tech_tbl.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0),  MID_BLUE),
        ('TEXTCOLOR',     (0,0), (-1,0),  white),
        ('FONTNAME',      (0,0), (-1,0),  'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [white, LIGHT_GRAY]),
        ('GRID',          (0,0), (-1,-1), 0.5, MID_GRAY),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(tech_tbl)
    story.append(Spacer(1, 0.4*cm))

    # ------------------------------------------------------------------ #
    # 4. ABAP CODE WALKTHROUGH (Screenshots section)
    # ------------------------------------------------------------------ #
    story.append(section_header('4.  ABAP Code Walkthrough & Screenshots', styles))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('<b>4.1  Program Architecture</b>', styles['h2']))
    story.append(Paragraph(
        'The program follows a modular ABAP design using PERFORM subroutines. The overall '
        'flow is: Selection Screen → Data Retrieval (FORM f_get_data) → Field Catalog Build '
        '(FORM f_build_fieldcat) → Layout & Sort setup → ALV Display.',
        styles['body']))
    story.append(Spacer(1, 0.2*cm))

    arch = [
        ['Event / Form',         'Purpose'],
        ['INITIALIZATION',       'Sets screen title text symbols'],
        ['START-OF-SELECTION',   'Calls all processing FORMs in sequence'],
        ['FORM f_get_data',      'SELECT from BSIK/BSAK; enrich with LFA1 vendor name'],
        ['FORM f_build_fieldcat','Builds column definitions for ALV using DEFINE macro'],
        ['FORM f_set_layout',    'Enables zebra stripes, column optimization, totals'],
        ['FORM f_set_sort',      'Sorts by Company Code and Vendor with subtotals'],
        ['FORM f_display_alv',   'Calls REUSE_ALV_GRID_DISPLAY to render the grid'],
        ['FORM f_user_command',  'Handles double-click: navigates to FB03'],
        ['FORM f_get_variant',   'F4 help for ALV display variants'],
    ]
    arch_tbl = Table(arch, colWidths=[(PAGE_W-2*MARGIN)*0.35, (PAGE_W-2*MARGIN)*0.65])
    arch_tbl.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0),  ACCENT),
        ('TEXTCOLOR',     (0,0), (-1,0),  white),
        ('FONTNAME',      (0,0), (-1,0),  'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [white, LIGHT_GRAY]),
        ('GRID',          (0,0), (-1,-1), 0.5, MID_GRAY),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(arch_tbl)
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('<b>4.2  Key Code Snippet – Data Retrieval</b>', styles['h2']))
    story.append(Paragraph(
        'The data fetch combines open and cleared items via two separate SELECT statements, '
        'then enriches the result with vendor names using FOR ALL ENTRIES:',
        styles['body']))

    code_snippet = (
        "SELECT bukrs lifnr belnr gjahr bldat budat blart dmbtr waers zterm zfbdt\n"
        "  FROM bsik INTO TABLE lt_bsik\n"
        " WHERE bukrs IN s_bukrs AND lifnr IN s_lifnr\n"
        "   AND bldat IN s_bldat AND gjahr IN s_gjahr\n"
        "   AND blart = p_blart.\n\n"
        "SELECT lifnr name1 FROM lfa1 INTO TABLE lt_lfa1\n"
        "   FOR ALL ENTRIES IN gt_vendor_invoice\n"
        " WHERE lifnr = gt_vendor_invoice-lifnr."
    )
    story.append(Paragraph(code_snippet.replace('\n','<br/>'), styles['code']))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('<b>4.3  Screenshot Placeholders</b>', styles['h2']))
    story.append(Paragraph(
        'After executing the program in SAP SE38 / SA38, paste your actual screenshots below. '
        'Replace the placeholder boxes with real screenshots from your SAP system.',
        styles['body']))

    for label_text in ['Selection Screen', 'ALV Output Grid', 'FB03 Navigation (Double-click)']:
        ph_data = [[Paragraph(f'[Screenshot: {label_text}]',
            ParagraphStyle('ph', fontName='Helvetica', fontSize=10,
                           textColor=MID_GRAY, alignment=TA_CENTER))]]
        ph_tbl = Table(ph_data, colWidths=[PAGE_W - 2*MARGIN],
                       rowHeights=[3.5*cm])
        ph_tbl.setStyle(TableStyle([
            ('BOX',           (0,0), (-1,-1), 1, MID_GRAY),
            ('BACKGROUND',    (0,0), (-1,-1), LIGHT_GRAY),
            ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
            ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(ph_tbl)
        story.append(Spacer(1, 0.2*cm))

    story.append(Spacer(1, 0.3*cm))

    # ------------------------------------------------------------------ #
    # 5. UNIQUE POINTS & FUTURE IMPROVEMENTS
    # ------------------------------------------------------------------ #
    story.append(section_header('5.  Unique Points & Future Improvements', styles))
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('<b>5.1  What Makes This Project Unique</b>', styles['h2']))
    unique_pts = [
        ['#', 'Unique Point'],
        ['1', 'Combines BSIK and BSAK in a single output — not available in any standard SAP report'],
        ['2', 'Payment Status column ("Open"/"Cleared") gives instant visual classification'],
        ['3', 'Double-click drill-down to FB03 enables seamless document investigation'],
        ['4', 'DEFINE macro used for field catalog — reduces repetition and improves maintainability'],
        ['5', 'FOR ALL ENTRIES used for efficient vendor name lookup — avoids nested SELECT loops'],
        ['6', 'Subtotals at Company Code and Vendor level with Grand Total row'],
    ]
    u_tbl = Table(unique_pts, colWidths=[(PAGE_W-2*MARGIN)*0.06, (PAGE_W-2*MARGIN)*0.94])
    u_tbl.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0),  DARK_BLUE),
        ('TEXTCOLOR',     (0,0), (-1,0),  white),
        ('FONTNAME',      (0,0), (-1,0),  'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [white, LIGHT_GRAY]),
        ('GRID',          (0,0), (-1,-1), 0.5, MID_GRAY),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN',         (0,0), (0,-1),  'CENTER'),
    ]))
    story.append(u_tbl)
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph('<b>5.2  Future Improvements</b>', styles['h2']))
    future = [
        ['Enhancement', 'Benefit'],
        ['Email Notification',      'Auto-email overdue invoices to AP team using SAP Business Workplace (SBWP)'],
        ['Overdue Highlighting',    'Color-code rows in red where invoice is open beyond payment due date'],
        ['Ageing Analysis',         'Add 0-30, 31-60, 61-90 day buckets to classify outstanding invoices'],
        ['Currency Conversion',     'Add group currency (GBP/USD) alongside local currency amounts'],
        ['OData / Fiori Extension', 'Expose the report as a Fiori tile using SEGW for self-service access'],
        ['BSEG Join',               'Join BSEG for GL account details to support reconciliation use cases'],
    ]
    f_tbl = Table(future, colWidths=[(PAGE_W-2*MARGIN)*0.30, (PAGE_W-2*MARGIN)*0.70])
    f_tbl.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0),  MID_BLUE),
        ('TEXTCOLOR',     (0,0), (-1,0),  white),
        ('FONTNAME',      (0,0), (-1,0),  'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [white, LIGHT_GRAY]),
        ('GRID',          (0,0), (-1,-1), 0.5, MID_GRAY),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(f_tbl)
    story.append(Spacer(1, 0.5*cm))

    # ------------------------------------------------------------------ #
    # CLOSING NOTE
    # ------------------------------------------------------------------ #
    note_data = [[Paragraph(
        '<b>Note:</b> This project was developed individually as a Capstone Project submission. '
        'All ABAP code is original. Replace all bracketed placeholders [YOUR NAME], '
        '[YOUR ROLL NUMBER], [YOUR BATCH/PROGRAM] with your actual details before submission.',
        ParagraphStyle('note', fontName='Helvetica', fontSize=10, textColor=DARK_BLUE,
                       alignment=TA_JUSTIFY, leading=14))]]
    note_tbl = Table(note_data, colWidths=[PAGE_W - 2*MARGIN])
    note_tbl.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), LIGHT_BLUE),
        ('BOX',           (0,0), (-1,-1), 1.5, ACCENT),
        ('TOPPADDING',    (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING',   (0,0), (-1,-1), 12),
    ]))
    story.append(note_tbl)

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF generated: {output_path}")

if __name__ == '__main__':
    build_pdf('/home/claude/sap_abap_project/Project_Documentation.pdf')
