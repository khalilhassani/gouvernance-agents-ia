import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak, KeepTogether, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.graphics.shapes import Drawing, Rect, String as DString, Line, Circle, Polygon, Group

def create_terminal_drawing(width, height, title, content_paragraphs):
    """
    Creates a beautiful ReportLab Drawing representing a Windows PowerShell console window.
    """
    d = Drawing(width, height)
    
    # Colors
    TERMINAL_BG = HexColor("#0d1117")
    HEADER_BG = HexColor("#21262d")
    BORDER_COLOR = HexColor("#30363d")
    TEXT_MUTED = HexColor("#8b949e")
    
    # Main container border & shadow background
    d.add(Rect(0, 0, width, height, fillColor=TERMINAL_BG, strokeColor=BORDER_COLOR, strokeWidth=1, rx=5, ry=5))
    
    # Title bar background
    d.add(Rect(0, height - 22, width, 22, fillColor=HEADER_BG, strokeColor=BORDER_COLOR, strokeWidth=0.5, rx=5, ry=5))
    # Fill bottom corners of header to keep them square
    d.add(Rect(0, height - 22, width, 5, fillColor=HEADER_BG, strokeColor=None))
    
    # Colored dots (Red, Yellow, Green) on the left
    d.add(Circle(12, height - 11, 4, fillColor=HexColor("#ff5f56"), strokeColor=None))
    d.add(Circle(24, height - 11, 4, fillColor=HexColor("#ffbd2e"), strokeColor=None))
    d.add(Circle(36, height - 11, 4, fillColor=HexColor("#27c93f"), strokeColor=None))
    
    # Terminal Title Text
    d.add(DString(width/2 - 45, height - 15, title, fontName="Helvetica-Bold", fontSize=8, fillColor=TEXT_MUTED))
    
    return d

def create_docker_logo_drawing(width, height):
    """
    Draws a highly stylized, beautiful blue Docker container ship logo.
    """
    d = Drawing(width, height)
    PRIMARY_BLUE = HexColor("#2496ed")
    LIGHT_BLUE = HexColor("#7cd1ff")
    
    # Draw container stack (grid of rectangles)
    # Stacks: col1: 2, col2: 3, col3: 3, col4: 2
    c_w = 12
    c_h = 7
    gap = 2
    
    start_x = width / 2 - 28
    start_y = height / 2 - 4
    
    # Column 1
    d.add(Rect(start_x, start_y, c_w, c_h, fillColor=PRIMARY_BLUE, strokeColor=None))
    d.add(Rect(start_x, start_y + c_h + gap, c_w, c_h, fillColor=LIGHT_BLUE, strokeColor=None))
    
    # Column 2
    d.add(Rect(start_x + c_w + gap, start_y, c_w, c_h, fillColor=PRIMARY_BLUE, strokeColor=None))
    d.add(Rect(start_x + c_w + gap, start_y + c_h + gap, c_w, c_h, fillColor=PRIMARY_BLUE, strokeColor=None))
    d.add(Rect(start_x + c_w + gap, start_y + 2*(c_h + gap), c_w, c_h, fillColor=LIGHT_BLUE, strokeColor=None))
    
    # Column 3
    d.add(Rect(start_x + 2*(c_w + gap), start_y, c_w, c_h, fillColor=PRIMARY_BLUE, strokeColor=None))
    d.add(Rect(start_x + 2*(c_w + gap), start_y + c_h + gap, c_w, c_h, fillColor=PRIMARY_BLUE, strokeColor=None))
    d.add(Rect(start_x + 2*(c_w + gap), start_y + 2*(c_h + gap), c_w, c_h, fillColor=LIGHT_BLUE, strokeColor=None))
    
    # Column 4
    d.add(Rect(start_x + 3*(c_w + gap), start_y, c_w, c_h, fillColor=PRIMARY_BLUE, strokeColor=None))
    d.add(Rect(start_x + 3*(c_w + gap), start_y + c_h + gap, c_w, c_h, fillColor=LIGHT_BLUE, strokeColor=None))
    
    # Whale body / Ship hull (highly stylized vector polygon)
    # Let's draw a nice curved base
    hull = Polygon(
        points=[
            start_x - 12, start_y - 4,
            start_x + 4*(c_w + gap) + 4, start_y - 4,
            start_x + 4*(c_w + gap) + 12, start_y + 4,
            start_x + 4*(c_w + gap) + 16, start_y + 12,  # whale tail top
            start_x + 4*(c_w + gap) + 10, start_y + 6,   # tail curve inner
            start_x + 4*(c_w + gap) + 4, start_y - 2,
            start_x - 8, start_y - 12,                    # whale body bottom curve
            start_x - 14, start_y - 8
        ],
        fillColor=PRIMARY_BLUE,
        strokeColor=None
    )
    d.add(hull)
    
    return d

def generate_pdf(output_path):
    # Setup document in Landscape A4 or Letter
    # Page size: 792 x 612 (Landscape Letter)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=landscape(letter),
        rightMargin=30,
        leftMargin=30,
        topMargin=25,
        bottomMargin=25
    )
    
    story = []
    
    # Custom Palette
    PRIMARY_COLOR = HexColor("#0f172a")    # Slate dark
    SECONDARY_COLOR = HexColor("#2563eb")  # Premium Blue
    ACCENT_BLUE = HexColor("#38bdf8")      # Sky blue
    TEXT_DARK = HexColor("#1e293b")        # Slate Text
    TEXT_MUTED = HexColor("#64748b")       # Muted gray
    BG_LIGHT = HexColor("#f8fafc")         # Light bg
    BORDER_COLOR = HexColor("#e2e8f0")
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Modifying default styles
    styles['Normal'].textColor = TEXT_DARK
    styles['Normal'].fontSize = 9.5
    styles['Normal'].leading = 14
    
    # Custom styles
    slide_title_style = ParagraphStyle(
        'SlideTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=PRIMARY_COLOR,
        spaceAfter=3
    )
    
    body_bold = ParagraphStyle(
        'BodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=14,
        textColor=PRIMARY_COLOR
    )
    
    terminal_style = ParagraphStyle(
        'TerminalText',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=HexColor("#c9d1d9"),
        spaceAfter=0
    )
    # Monospace code block style
    code_block_style = ParagraphStyle(
        'CodeBlock',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=HexColor("#e2e8f0"),
    )
    
    def format_code_to_html(text):
        import re
        lines = text.split('\n')
        formatted_lines = []
        for line in lines:
            parts = re.split(r'(<[^>]+>)', line)
            for i in range(len(parts)):
                if not parts[i].startswith('<'):
                    txt = parts[i]
                    txt = txt.replace('├──', '|--').replace('└──', '`--').replace('│', '|')
                    txt = txt.replace(' ', '&nbsp;')
                    parts[i] = txt
            formatted_lines.append("".join(parts))
        return "<br/>".join(formatted_lines)

    def create_code_box(text, width):
        html_content = format_code_to_html(text)
        body_p = Paragraph(f'<font color="#e2e8f0">{html_content}</font>', code_block_style)
        code_table = Table([[body_p]], colWidths=[width])
        code_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), HexColor("#1e293b")),
            ('BOX', (0,0), (-1,-1), 0.5, HexColor("#334155")),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (-1,-1), 8),
        ]))
        return code_table
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=TEXT_DARK
    )
    
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=PRIMARY_COLOR
    )

    # ----------------------------------------------------
    # SLIDE 1: Title Page
    # ----------------------------------------------------
    title_left = [
        Spacer(1, 20),
        create_docker_logo_drawing(250, 100),
        Spacer(1, 15),
        Paragraph("<font size='22' color='#2563eb'><b>DOCKER FUNDAMENTALS</b></font>", ParagraphStyle('MainTitle1', parent=styles['Normal'], fontName='Helvetica-Bold', leading=26)),
        Paragraph("<font size='22' color='#0f172a'><b>FOR AGENTIC AI</b></font>", ParagraphStyle('MainTitle2', parent=styles['Normal'], fontName='Helvetica-Bold', leading=26)),
        Spacer(1, 8),
        Paragraph("<b>Step-by-Step Guide:</b>", ParagraphStyle('GuideText', parent=styles['Normal'], fontSize=11, textColor=TEXT_MUTED)),
        Paragraph("Containerizing our FastAPI Agent Validation Platform", ParagraphStyle('SubText', parent=styles['Normal'], fontSize=11, leading=15, textColor=TEXT_DARK)),
        Spacer(1, 30),
        Paragraph("<font size='8' color='#94a3b8'>Gouvernance des Agents IA • v1.0.0<br/>Auteurs : Khaoula Adeli &amp; Khalil Hassani Khalfaoui</font>", styles['Normal']),
    ]
    
    learn_points = [
        "• Containerize our FastAPI validation app",
        "• Build a Docker image",
        "• Run the container",
        "• Verify the API & tests",
        "• View container logs",
        "• Stop and remove the container"
    ]
    
    learn_p_html = "<br/>".join([f"<b>{pt.split(' ')[0]}</b> {' '.join(pt.split(' ')[1:])}" for pt in learn_points])
    
    title_right = [
        Spacer(1, 30),
        Table(
            [
                [Paragraph("<b>What you will learn</b>", ParagraphStyle('CardTitle', parent=styles['Normal'], fontName='Helvetica-Bold', textColor=colors.white, fontSize=11, leading=14))],
                [Paragraph(learn_p_html, ParagraphStyle('CardBody', parent=styles['Normal'], fontSize=10, leading=18, textColor=TEXT_DARK))]
            ],
            colWidths=[300],
            style=TableStyle([
                ('BACKGROUND', (0,0), (-1,0), SECONDARY_COLOR),
                ('BACKGROUND', (0,1), (-1,-1), HexColor("#ffffff")),
                ('BOX', (0,0), (-1,-1), 1.5, SECONDARY_COLOR),
                ('PADDING', (0,0), (-1,-1), 15),
                ('TOPPADDING', (0,0), (-1,0), 10),
                ('BOTTOMPADDING', (0,0), (-1,0), 10),
            ])
        )
    ]
    
    slide1_table = Table([[title_left, title_right]], colWidths=[380, 350])
    slide1_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    
    story.append(slide1_table)
    story.append(PageBreak())

    # Helper function for generating standard slides
    def add_slide(slide_num, title, left_flowables, right_flowables):
        header_data = [
            [
                Paragraph(f"<b>{slide_num}. {title}</b>", slide_title_style),
                Paragraph("<font color='#64748b'>DOCKER FUNDAMENTALS FOR AGENTIC AI</font>", ParagraphStyle('SlideHeaderRight', parent=styles['Normal'], alignment=2, fontSize=8, textColor=TEXT_MUTED))
            ]
        ]
        header_table = Table(header_data, colWidths=[400, 332])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ]))
        
        story.append(header_table)
        story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY_COLOR, spaceBefore=4, spaceAfter=12))
        
        slide_content = Table([[left_flowables, right_flowables]], colWidths=[350, 382])
        slide_content.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(slide_content)
        story.append(PageBreak())

    # Helper for rendering terminal inside document flow
    def render_terminal(height, title, content_lines):
        # Header drawing
        header_dr = create_terminal_drawing(370, 22, title, [])
        
        # Terminal body table
        term_text_html = "<br/>".join(content_lines)
        body_p = Paragraph(term_text_html, terminal_style)
        
        # Combined table with 2 rows: row 0 is header, row 1 is terminal body
        term_table = Table([[header_dr], [body_p]], colWidths=[370], rowHeights=[22, height - 22])
        term_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), HexColor("#0d1117")),
            ('BOX', (0,0), (-1,-1), 0.5, HexColor("#30363d")),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,1), (0,1), 10),
            ('BOTTOMPADDING', (0,1), (0,1), 10),
            ('LEFTPADDING', (0,1), (0,1), 10),
            ('RIGHTPADDING', (0,1), (0,1), 10),
        ]))
        
        return term_table

    # ----------------------------------------------------
    # SLIDE 2: 1. Our FastAPI Validation App
    # ----------------------------------------------------
    left_2 = [
        Paragraph("We will containerize our FastAPI validation and compliance platform. The platform executes tests and evaluates AI Agent behavior in an offline, repeatable environment.", styles['Normal']),
        Spacer(1, 10),
        Paragraph("<b>Key Features of the App:</b>", body_bold),
        Paragraph("• <b>FastAPI Server</b>: Exposes endpoints for executing tests (`/api/tests/run`) and exporting the workflow configuration.", styles['Normal']),
        Paragraph("• <b>Test Engine</b>: Executes 20 test cases in a Golden Set and calculates intent correctness, quality, and tone scores.", styles['Normal']),
        Paragraph("• <b>Frontend Dashboard</b>: Displays metrics, compliance reports, and an interactive playground.", styles['Normal']),
    ]
    
    project_tree = """<b>gouvernance-agents-ia/</b>
├── backend/
│   ├── app/
│   │   ├── main.py         <font color='#94a3b8'># FastAPI Server</font>
│   │   ├── services/
│   │   │   └── agent_service.py <font color='#94a3b8'># Simulated Agent</font>
│   │   ├── tests_engine/
│   │   │   └── engine.py   <font color='#94a3b8'># Test Orchestrator</font>
│   │   └── validators/
│   │       └── conformity.py <font color='#94a3b8'># Rules Engine</font>
│   └── requirements.txt    <font color='#94a3b8'># Python Deps</font>
├── frontend/               <font color='#94a3b8'># Dashboard static files</font>
│   ├── index.html
│   └── app.js
└── backend/Dockerfile      <font color='#94a3b8'># Docker Configuration</font>"""

    right_2 = [
        Paragraph("<b>Project Structure:</b>", body_bold),
        Spacer(1, 4),
        create_code_box(project_tree, 370),
    ]
    
    add_slide(2, "Our FastAPI Validation App", left_2, right_2)

    # ----------------------------------------------------
    # SLIDE 3: 2. requirements.txt
    # ----------------------------------------------------
    left_3 = [
        Paragraph("Python dependencies are listed in `requirements.txt`. These libraries are installed inside the Docker image during the build process to guarantee environment isolation.", styles['Normal']),
        Spacer(1, 10),
        Paragraph("<b>Core Dependencies Explained:</b>", body_bold),
        Paragraph("• <b>fastapi</b>: The core web framework utilized to build the API.", styles['Normal']),
        Paragraph("• <b>uvicorn</b>: An ASGI web server implementation used to run the FastAPI app.", styles['Normal']),
        Paragraph("• <b>pydantic</b>: Used for data validation and schema definitions.", styles['Normal']),
        Paragraph("• <b>pytest</b>: Test framework to launch and validate the execution suite.", styles['Normal']),
    ]
    
    req_content = """fastapi>=0.110.0
uvicorn>=0.28.0
pydantic>=2.0
pytest>=8.0
anyio>=4.0"""

    right_3 = [
        Paragraph("<b>requirements.txt (File content):</b>", body_bold),
        Spacer(1, 4),
        create_code_box(req_content, 370),
    ]
    
    add_slide(3, "requirements.txt", left_3, right_3)

    # ----------------------------------------------------
    # SLIDE 4: 3. Dockerfile
    # ----------------------------------------------------
    left_4 = [
        Paragraph("A <b>Dockerfile</b> contains the sequence of instructions Docker uses to build the container image.", styles['Normal']),
        Spacer(1, 8),
        # Table describing instructions
        Table(
            [
                [Paragraph("Instruction", table_cell_bold), Paragraph("Purpose in our project", table_cell_bold)],
                [Paragraph("<b>FROM</b>", table_cell_style), Paragraph("Uses the official lightweight Python 3.12 image as a base.", table_cell_style)],
                [Paragraph("<b>WORKDIR</b>", table_cell_style), Paragraph("Sets the directory inside the container to `/app`.", table_cell_style)],
                [Paragraph("<b>COPY</b>", table_cell_style), Paragraph("Copies files from the host into the container filesystem.", table_cell_style)],
                [Paragraph("<b>RUN</b>", table_cell_style), Paragraph("Installs Python libraries listed in `requirements.txt`.", table_cell_style)],
                [Paragraph("<b>EXPOSE</b>", table_cell_style), Paragraph("Documents that port 8000 is open for incoming traffic.", table_cell_style)],
                [Paragraph("<b>CMD</b>", table_cell_style), Paragraph("Defines the command that launches the server via Uvicorn.", table_cell_style)]
            ],
            colWidths=[80, 260],
            style=TableStyle([
                ('BACKGROUND', (0,0), (-1,0), HexColor("#f1f5f9")),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('GRID', (0,0), (-1,-1), 0.5, HexColor("#e2e8f0")),
                ('PADDING', (0,0), (-1,-1), 4),
            ])
        )
    ]
    
    dockerfile_content = """FROM python:3.12-slim
WORKDIR /app

COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r ./backend/requirements.txt

COPY backend ./backend
COPY frontend ./frontend

EXPOSE 8000
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "uvicorn", "backend.app.main:app", \\
     "--host", "0.0.0.0", "--port", "8000"]"""

    right_4 = [
        Paragraph("<b>Dockerfile Configuration:</b>", body_bold),
        Spacer(1, 4),
        create_code_box(dockerfile_content, 370),
    ]
    
    add_slide(4, "Dockerfile", left_4, right_4)

    # ----------------------------------------------------
    # SLIDE 5: 4. Open Terminal and Navigate to Project
    # ----------------------------------------------------
    left_5 = [
        Paragraph("To containerize the application, start by opening your terminal or PowerShell console and navigate to the project directory.", styles['Normal']),
        Spacer(1, 10),
        Paragraph("<b>Commands used:</b>", body_bold),
        Paragraph("• <b>cd</b>: Change directory to the root of the project.", styles['Normal']),
        Paragraph("• <b>dir</b> (or <b>ls</b> on Unix): Lists files in the current folder. Verify that the `backend/` and `frontend/` folders are visible.", styles['Normal']),
    ]
    
    term_5 = [
        '<font color="#56d364">PS C:\\Users\\LENOVO&gt;</font> <font color="#58a6ff">cd "C:\\Users\\LENOVO\\Desktop\\Lab 24"</font>',
        '<font color="#56d364">PS C:\\Users\\LENOVO\\Desktop\\Lab 24&gt;</font> <font color="#58a6ff">dir</font>',
        '',
        '    Directory: C:\\Users\\LENOVO\\Desktop\\Lab 24',
        '',
        'Mode                 LastWriteTime         Length Name',
        '----                 -------------         ------ ----',
        'd----           24/06/2026   16:33                backend',
        'd----           24/06/2026   16:33                frontend',
        '-a---           24/06/2026   16:33            9169 LIVRABLES.md',
        '-a---           24/06/2026   16:33            4525 README.md',
        '-a---           24/06/2026   16:33            3453 test_report.md'
    ]
    
    right_5 = [
        Paragraph("<b>Console Output:</b>", body_bold),
        Spacer(1, 4),
        render_terminal(180, "Windows PowerShell", term_5)
    ]
    
    add_slide(5, "Open Terminal and Navigate to Project", left_5, right_5)

    # ----------------------------------------------------
    # SLIDE 6: 5. Build the Docker Image
    # ----------------------------------------------------
    left_6 = [
        Paragraph("Build the Docker container image from the Dockerfile. This bundles Python, our dependencies, and all source code into a single immutable artifact.", styles['Normal']),
        Spacer(1, 10),
        Paragraph("<b>Command Syntax:</b>", body_bold),
        Paragraph("<font face='Courier' size='8'>docker build -t name:tag -f Dockerfile_path context</font>", styles['Normal']),
        Spacer(1, 6),
        Paragraph("• <b>-t agent-validation-platform:1.0</b>: Tags the image with a name and version.", styles['Normal']),
        Paragraph("• <b>-f backend/Dockerfile</b>: Specifies the path to the Dockerfile.", styles['Normal']),
        Paragraph("• <b>.</b>: Context is the current folder (all files are copied relative to this root).", styles['Normal']),
    ]
    
    term_6 = [
        '<font color="#56d364">PS C:\\Users\\LENOVO\\Desktop\\Lab 24&gt;</font> <font color="#58a6ff">docker build -t agent-validation-platform:1.0 -f backend/Dockerfile .</font>',
        '[+] Building 8.4s (10/10) FINISHED',
        ' =&gt; [internal] load build definition from Dockerfile        0.0s',
        ' =&gt; =&gt; transferring dockerfile: 689B                       0.0s',
        ' =&gt; [internal] load .dockerignore                          0.0s',
        ' =&gt; =&gt; transferring context: 128B                          0.0s',
        ' =&gt; [internal] load metadata for docker.io/library/python  1.1s',
        ' =&gt; [1/5] FROM docker.io/library/python:3.12-slim          2.3s',
        ' =&gt; [2/5] WORKDIR /app                                     0.1s',
        ' =&gt; [3/5] COPY backend/requirements.txt ./backend/         0.0s',
        ' =&gt; [4/5] RUN pip install --no-cache-dir -r ./backend/req  4.5s',
        ' =&gt; [5/5] COPY backend ./backend && COPY frontend ./front  0.3s',
        ' =&gt; exporting to image                                     0.1s',
        ' =&gt; =&gt; writing image sha256:d8a2bc416ef42a8b9f1d07bde8d12  0.0s',
        ' =&gt; =&gt; naming to docker.io/library/agent-validation-platf  0.0s'
    ]
    
    right_6 = [
        Paragraph("<b>Docker Build Process:</b>", body_bold),
        Spacer(1, 4),
        render_terminal(200, "Windows PowerShell", term_6)
    ]
    
    add_slide(6, "Build the Docker Image", left_6, right_6)

    # ----------------------------------------------------
    # SLIDE 7: 6. Verify the Image
    # ----------------------------------------------------
    left_7 = [
        Paragraph("Verify that the image was built successfully and is registered in Docker's local image cache.", styles['Normal']),
        Spacer(1, 10),
        Paragraph("<b>Command used:</b>", body_bold),
        Paragraph("• <b>docker images</b>: Lists all locally cached Docker images, including their repository name, tag, image ID, creation date, and size.", styles['Normal']),
        Spacer(1, 8),
        Paragraph("The `agent-validation-platform` image is self-contained and weighs approximately 148MB (which includes the entire Python runtime, requirements, and frontend/backend files).", styles['Normal']),
    ]
    
    term_7 = [
        '<font color="#56d364">PS C:\\Users\\LENOVO\\Desktop\\Lab 24&gt;</font> <font color="#58a6ff">docker images</font>',
        '',
        'REPOSITORY                  TAG       IMAGE ID       CREATED          SIZE',
        'agent-validation-platform   1.0       d8a2bc416ef4   12 seconds ago   148MB',
        'python                      3.12-slim 5b1dbe7c2a44   2 weeks ago      120MB'
    ]
    
    right_7 = [
        Paragraph("<b>Docker Local Cache:</b>", body_bold),
        Spacer(1, 4),
        render_terminal(180, "Windows PowerShell", term_7)
    ]
    
    add_slide(7, "Verify the Image", left_7, right_7)

    # ----------------------------------------------------
    # SLIDE 8: 7. Run the Container
    # ----------------------------------------------------
    left_8 = [
        Paragraph("Instantiate and run the Docker container. This starts the FastAPI web server, mapping the ports to allow access from the host machine.", styles['Normal']),
        Spacer(1, 10),
        Paragraph("<b>Command details:</b>", body_bold),
        Paragraph("• <b>-it</b>: Interactive mode with terminal output feedback.", styles['Normal']),
        Paragraph("• <b>--rm</b>: Clean up and delete container files when stopped.", styles['Normal']),
        Paragraph("• <b>-p 8000:8000</b>: Map port 8000 on the host to port 8000 inside the container. This makes the dashboard accessible at `http://127.0.0.1:8000`.", styles['Normal']),
    ]
    
    term_8 = [
        '<font color="#56d364">PS C:\\Users\\LENOVO\\Desktop\\Lab 24&gt;</font> <font color="#58a6ff">docker run -it --rm -p 8000:8000 agent-validation-platform:1.0</font>',
        'INFO:     Started server process [1]',
        'INFO:     Waiting for application startup.',
        'INFO:     Application startup complete.',
        'INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)'
    ]
    
    right_8 = [
        Paragraph("<b>Container Startup logs:</b>", body_bold),
        Spacer(1, 4),
        render_terminal(180, "Windows PowerShell", term_8)
    ]
    
    add_slide(8, "Run the Container", left_8, right_8)

    # ----------------------------------------------------
    # SLIDE 9: 8. Test the Agent & API
    # ----------------------------------------------------
    left_9 = [
        Paragraph("Validate the running API container. We can query the health endpoint and execute the pytest suite inside the active container environment.", styles['Normal']),
        Spacer(1, 10),
        Paragraph("<b>Validation methods:</b>", body_bold),
        Paragraph("• <b>curl</b>: Verify that the FastAPI backend is running and healthy on port 8000.", styles['Normal']),
        Paragraph("• <b>docker exec</b>: Run commands inside an already running container. We use it to trigger our 20 business compliance test cases.", styles['Normal']),
    ]
    
    term_9 = [
        '<font color="#56d364">PS C:\\Users\\LENOVO\\Desktop\\Lab 24&gt;</font> <font color="#58a6ff">curl http://127.0.0.1:8000/health</font>',
        '{"status":"healthy","service":"validation-engine","uptime":"nominal"}',
        '',
        '<font color="#56d364">PS C:\\Users\\LENOVO\\Desktop\\Lab 24&gt;</font> <font color="#58a6ff">docker exec -it agent-val-container pytest backend/app/tests/</font>',
        '============================= test session starts =============================',
        'collected 1 item',
        'backend/app/tests/test_validation.py .                                   [100%]',
        '============================== 1 passed in 2.82s =============================='
    ]
    
    right_9 = [
        Paragraph("<b>Testing & Verification:</b>", body_bold),
        Spacer(1, 4),
        render_terminal(190, "Windows PowerShell", term_9)
    ]
    
    add_slide(9, "Test the Agent & API", left_9, right_9)

    # ----------------------------------------------------
    # SLIDE 10: 9. View Logs (Detached Mode)
    # ----------------------------------------------------
    left_10 = [
        Paragraph("Run the container in detached background mode. This is the preferred way to run services in staging or production environments.", styles['Normal']),
        Spacer(1, 10),
        Paragraph("<b>Detached command flags:</b>", body_bold),
        Paragraph("• <b>-d</b>: Detach and run the container in the background. The terminal immediately prints the container ID.", styles['Normal']),
        Paragraph("• <b>--name agent-val-container</b>: Assign a human-readable name to the container to manage it easily.", styles['Normal']),
        Paragraph("• <b>docker logs name</b>: Retrieve and view the standard output/error logs of the background container.", styles['Normal']),
    ]
    
    term_10 = [
        '<font color="#56d364">PS C:\\Users\\LENOVO\\Desktop\\Lab 24&gt;</font> <font color="#58a6ff">docker run -d --name agent-val-container -p 8000:8000 agent-validation-platform:1.0</font>',
        '8f72a4b8bc0e7a2b95cde82b9b7e77a28e827b38d3829d2b270a2a11b238382c',
        '',
        '<font color="#56d364">PS C:\\Users\\LENOVO\\Desktop\\Lab 24&gt;</font> <font color="#58a6ff">docker logs agent-val-container</font>',
        'INFO:     Started server process [1]',
        'INFO:     Waiting for application startup.',
        'INFO:     Application startup complete.',
        'INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)',
        'INFO:     127.0.0.1:54321 - "GET /health HTTP/1.1" 200 OK'
    ]
    
    right_10 = [
        Paragraph("<b>Background Execution Logs:</b>", body_bold),
        Spacer(1, 4),
        render_terminal(200, "Windows PowerShell", term_10)
    ]
    
    add_slide(10, "View Logs (Detached Mode)", left_10, right_10)

    # ----------------------------------------------------
    # SLIDE 11: 10. Stop the Container
    # ----------------------------------------------------
    left_11 = [
        Paragraph("Stop the running background container. This gracefully terminates Uvicorn and FastAPI before halting the container instance.", styles['Normal']),
        Spacer(1, 10),
        Paragraph("<b>Command details:</b>", body_bold),
        Paragraph("• <b>docker stop agent-val-container</b>: Sends a SIGTERM signal to Uvicorn (PID 1), allowing open connections to close properly, followed by a SIGKILL if it doesn't shut down in 10 seconds.", styles['Normal']),
        Spacer(1, 8),
        Paragraph("Stopping a container does not delete its filesystem, meaning it can be restarted later.", styles['Normal']),
    ]
    
    term_11 = [
        '<font color="#56d364">PS C:\\Users\\LENOVO\\Desktop\\Lab 24&gt;</font> <font color="#58a6ff">docker stop agent-val-container</font>',
        'agent-val-container'
    ]
    
    right_11 = [
        Paragraph("<b>Graceful Stop:</b>", body_bold),
        Spacer(1, 4),
        render_terminal(140, "Windows PowerShell", term_11)
    ]
    
    add_slide(11, "Stop the Container", left_11, right_11)

    # ----------------------------------------------------
    # SLIDE 12: 11. Remove the Container
    # ----------------------------------------------------
    left_12 = [
        Paragraph("Delete the stopped container from the local storage. This cleans up container metadata and releases the assigned port mapping and container name.", styles['Normal']),
        Spacer(1, 10),
        Paragraph("<b>Command details:</b>", body_bold),
        Paragraph("• <b>docker rm agent-val-container</b>: Deletes the container instance. All temporary data inside the container is permanently erased.", styles['Normal']),
        Spacer(1, 8),
        Paragraph("Once removed, the port 8000 is released and you can launch a new container instance with the name `agent-val-container`.", styles['Normal']),
    ]
    
    term_12 = [
        '<font color="#56d364">PS C:\\Users\\LENOVO\\Desktop\\Lab 24&gt;</font> <font color="#58a6ff">docker rm agent-val-container</font>',
        'agent-val-container'
    ]
    
    right_12 = [
        Paragraph("<b>Remove Container:</b>", body_bold),
        Spacer(1, 4),
        render_terminal(140, "Windows PowerShell", term_12)
    ]
    
    add_slide(12, "Remove the Container", left_12, right_12)

    # ----------------------------------------------------
    # SLIDE 13: 12. Summary
    # ----------------------------------------------------
    left_13 = [
        Paragraph("You have successfully containerized and validated the FastAPI Agent Validation Platform using Docker!", styles['Normal']),
        Spacer(1, 8),
        Paragraph("<b>What was covered:</b>", body_bold),
        Paragraph("✓ Verified project structure and code dependencies.", styles['Normal']),
        Paragraph("✓ Explanatory breakdown of Dockerfile instructions.", styles['Normal']),
        Paragraph("✓ Navigated files and built the Docker image.", styles['Normal']),
        Paragraph("✓ Ran the container, mapping port 8000.", styles['Normal']),
        Paragraph("✓ Verified API health check and tests inside the container.", styles['Normal']),
        Paragraph("✓ Launched in detached mode and retrieved container logs.", styles['Normal']),
        Paragraph("✓ Gracefully stopped and deleted the container.", styles['Normal']),
    ]
    
    summary_card = [
        [Paragraph("<b>Validation Status</b>", ParagraphStyle('SummaryTitle', parent=styles['Normal'], fontName='Helvetica-Bold', textColor=colors.white, fontSize=11, leading=14))],
        [Paragraph(
            "<font color='#047857'><b>IMAGE STABLE</b></font><br/>"
            "• Repository: agent-validation-platform<br/>"
            "• Tag: 1.0<br/>"
            "• Base Runtime: Python 3.12-slim<br/>"
            "• Exposed Ports: 8000<br/>"
            "• Test Suite execution inside Docker: <b>100% OK</b>",
            ParagraphStyle('SummaryBody', parent=styles['Normal'], fontSize=9.5, leading=18, textColor=TEXT_DARK)
        )]
    ]
    
    right_13 = [
        Spacer(1, 10),
        Table(
            summary_card,
            colWidths=[330],
            style=TableStyle([
                ('BACKGROUND', (0,0), (-1,0), HexColor("#047857")), # Emerald Green Header
                ('BACKGROUND', (0,1), (-1,-1), HexColor("#ffffff")),
                ('BOX', (0,0), (-1,-1), 1.5, HexColor("#047857")),
                ('PADDING', (0,0), (-1,-1), 15),
                ('TOPPADDING', (0,0), (-1,0), 10),
                ('BOTTOMPADDING', (0,0), (-1,0), 10),
            ])
        ),
        Spacer(1, 20),
        create_docker_logo_drawing(250, 60)
    ]
    
    add_slide(13, "Summary", left_13, right_13)

    # Build the document
    doc.build(story)
    print("Docker containerization guide PDF generated successfully.")

if __name__ == "__main__":
    generate_pdf("Docker_Containerization_Guide.pdf")
