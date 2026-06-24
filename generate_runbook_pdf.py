import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.graphics.shapes import Drawing, Rect, String as DString, Line, Circle
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.legends import Legend

def create_runbook_pdf(output_path):
    # Setup document with 40pt margins for a clean, professional grid
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    story = []
    
    # Custom Color Palette
    PRIMARY_COLOR = HexColor("#0f172a")    # Slate Dark
    SECONDARY_COLOR = HexColor("#b91c1c")  # Incident Red
    ACCENT_BLUE = HexColor("#1d4ed8")      # Deep Blue
    ACCENT_GREEN = HexColor("#047857")     # Success Green
    BG_LIGHT = HexColor("#f8fafc")         # Slate Light
    TEXT_DARK = HexColor("#1e293b")        # Dark slate for text
    TEXT_MUTED = HexColor("#64748b")       # Muted gray
    
    styles = getSampleStyleSheet()
    
    # Modify base style
    styles['Normal'].textColor = TEXT_DARK
    styles['Normal'].fontSize = 9
    styles['Normal'].leading = 12.5
    
    # Custom Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.white,
        alignment=0
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=HexColor("#cbd5e1"),
        alignment=0
    )
    
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=HexColor("#0f172a"),
        spaceBefore=12,
        spaceAfter=6
    )
    
    sub_section_heading = ParagraphStyle(
        'SubSectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=ACCENT_BLUE,
        spaceBefore=8,
        spaceAfter=4
    )
    
    cell_bold = ParagraphStyle(
        'CellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=PRIMARY_COLOR
    )
    
    cell_normal = ParagraphStyle(
        'CellNormal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=TEXT_DARK
    )
    
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=HexColor("#0f172a"),
        backColor=HexColor("#f1f5f9"),
        borderColor=HexColor("#cbd5e1"),
        borderWidth=0.5,
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=4
    )

    # --- HEADER BANNER ---
    header_data = [
        [
            Paragraph("RUNBOOK OPÉRATIONNEL DE PRODUCTION &nbsp; | &nbsp; Auteurs : Khaoula Adeli &amp; Khalil Hassani Khalfaoui", subtitle_style),
            ""
        ],
        [
            Paragraph("PROCÉDURES D'URGENCE & GESTION DES INCIDENTS", title_style),
            Paragraph("Version : 1.0.0<br/>Classification : <b>INTERNE</b>", ParagraphStyle(
                'HeaderStatus',
                parent=styles['Normal'],
                fontName='Helvetica',
                fontSize=8.5,
                leading=12,
                textColor=HexColor("#fca5a5"), # Light red
                alignment=2
            ))
        ]
    ]
    
    header_table = Table(header_data, colWidths=[380, 152])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor("#7f1d1d")), # Dark red background for incident runbook
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('SPAN', (0,0), (1,0)),
        ('PADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,1), (-1,1), 16),
        ('TOPPADDING', (0,0), (-1,0), 16),
    ]))
    
    story.append(header_table)
    story.append(Spacer(1, 12))
    
    # --- INTRODUCTION ---
    intro_p = Paragraph(
        "Ce document d'exploitation définit les procédures strictes de supervision, d'isolement (Kill-Switch) "
        "et de retour arrière (Rollback) pour l'<b>Assistant Citoyen E-Gov</b>. Il garantit la continuité opérationnelle "
        "et la conformité réglementaire de la plateforme face aux dérives techniques ou linguistiques de l'agent.",
        styles['Normal']
    )
    story.append(intro_p)
    story.append(Spacer(1, 10))
    
    # --- SECTION 1: GESTION DES INCIDENTS ---
    story.append(Paragraph("1. Procédure de Détection et de Triage", section_heading))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#7f1d1d"), spaceAfter=8))
    
    story.append(Paragraph("A. Indicateurs de Performance et de Qualité (SLIs)", sub_section_heading))
    story.append(Paragraph(
        "La supervision s'appuie sur quatre indicateurs majeurs mis à jour en continu par la suite de tests "
        "et l'analyse des logs d'API.",
        styles['Normal']
    ))
    story.append(Spacer(1, 5))
    
    # SLI Table
    sli_data = [
        [Paragraph("Métrique (SLI)", cell_bold), Paragraph("Seuil Nominal", cell_bold), Paragraph("Seuil Alerte", cell_bold), Paragraph("Méthode de Mesure", cell_bold)],
        [Paragraph("Taux d'Erreur (HTTP 5xx)", cell_normal), Paragraph("&lt; 0.5%", cell_normal), Paragraph("&gt; 1.0% (Alerte)", cell_normal), Paragraph("Logs API FastAPI / Nginx", cell_normal)],
        [Paragraph("Latence Moyenne (p95)", cell_normal), Paragraph("&lt; 300 ms", cell_normal), Paragraph("&gt; 500 ms (Alerte)", cell_normal), Paragraph("Temps calculé par <i>agent_service.py</i>", cell_normal)],
        [Paragraph("Score de Conformité", cell_normal), Paragraph("&gt; 90.0%", cell_normal), Paragraph("&lt; 80.0% (Critique)", cell_normal), Paragraph("Moteur de règles <i>conformity.py</i>", cell_normal)],
        [Paragraph("Taux d'Hallucinations", cell_normal), Paragraph("0.0%", cell_normal), Paragraph("&gt; 0.0% (Bloquant)", cell_normal), Paragraph("Détection regex sur outputs réels", cell_normal)]
    ]
    sli_table = Table(sli_data, colWidths=[120, 100, 112, 200])
    sli_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor("#cbd5e1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, HexColor("#f8fafc")]),
    ]))
    story.append(sli_table)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("B. Matrice de Triage et Priorisation", sub_section_heading))
    
    # Chart for visual presentation of compliance results (Pie Chart of recent test execution)
    d = Drawing(400, 110)
    # Background for chart area
    d.add(Rect(0, 0, 400, 110, fillColor=HexColor("#f8fafc"), strokeColor=HexColor("#e2e8f0"), strokeWidth=1))
    
    # Add Pie Chart
    pc = Pie()
    pc.x = 20
    pc.y = 15
    pc.width = 80
    pc.height = 80
    pc.data = [85, 15] # 85% Conforme, 15% Défaillant
    pc.labels = []
    pc.sideLabels = False
    
    # Custom colors for slices
    pc.slices[0].fillColor = HexColor("#10b981") # Green
    pc.slices[1].fillColor = HexColor("#ef4444") # Red
    d.add(pc)
    
    # Add Legend
    legend = Legend()
    legend.x = 120
    legend.y = 90
    legend.dx = 8
    legend.dy = 8
    legend.fontName = 'Helvetica'
    legend.fontSize = 8.5
    legend.boxAnchor = 'nw'
    legend.columnMaximum = 2
    legend.colorNamePairs = [(HexColor("#10b981"), 'Conforme (85% success rate)'), (HexColor("#ef4444"), 'Défaillant / Alerte (15%)')]
    d.add(legend)
    
    # Title/Explanation inside chart
    d.add(DString(120, 60, "RÉSULTAT DE LA DERNIÈRE SUITE DE TESTS MÉTIERS (GOLDEN SET)", fontName="Helvetica-Bold", fontSize=8.5, fillColor=PRIMARY_COLOR))
    d.add(DString(120, 45, "• 17 Tests validés (greetings conformes, intentions correctes)", fontName="Helvetica", fontSize=8, fillColor=TEXT_DARK))
    d.add(DString(120, 32, "• 3 Échecs critiques (2 fuites système 'Fatal error', 1 hallucination)", fontName="Helvetica", fontSize=8, fillColor=TEXT_DARK))
    
    story.append(d)
    story.append(Spacer(1, 12))
    
    # --- SECTION 2: KILL-SWITCH ---
    story.append(Paragraph("2. Procédure de \"Kill-Switch\" (Arrêt d'Urgence)", section_heading))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#7f1d1d"), spaceAfter=8))
    
    story.append(Paragraph(
        "En cas d'anomalie critique (ex: génération de propos inappropriés, fuite massive d'erreurs "
        "système), la coupure immédiate de l'agent est requise.",
        styles['Normal']
    ))
    story.append(Spacer(1, 6))
    
    # Visual Flowchart representation in drawing
    flow = Drawing(532, 45)
    flow.add(Rect(0, 0, 532, 45, fillColor=HexColor("#fef2f2"), strokeColor=HexColor("#fca5a5"), strokeWidth=1))
    # Box 1
    flow.add(Rect(10, 10, 110, 25, fillColor=HexColor("#fee2e2"), strokeColor=SECONDARY_COLOR, strokeWidth=1, rx=3, ry=3))
    flow.add(DString(20, 18, "1. DÉTECTION P1", fontName="Helvetica-Bold", fontSize=8, fillColor=SECONDARY_COLOR))
    # Arrow 1
    flow.add(Line(120, 22, 140, 22, strokeColor=TEXT_MUTED, strokeWidth=1.5))
    # Box 2
    flow.add(Rect(140, 10, 140, 25, fillColor=HexColor("#eff6ff"), strokeColor=ACCENT_BLUE, strokeWidth=1, rx=3, ry=3))
    flow.add(DString(150, 18, "2. INJECTION VARIABLE", fontName="Helvetica-Bold", fontSize=8, fillColor=ACCENT_BLUE))
    # Arrow 2
    flow.add(Line(280, 22, 300, 22, strokeColor=TEXT_MUTED, strokeWidth=1.5))
    # Box 3
    flow.add(Rect(300, 10, 100, 25, fillColor=HexColor("#faf5ff"), strokeColor=HexColor("#7c3aed"), strokeWidth=1, rx=3, ry=3))
    flow.add(DString(310, 18, "3. REDÉMARRAGE", fontName="Helvetica-Bold", fontSize=8, fillColor=HexColor("#7c3aed")))
    # Arrow 3
    flow.add(Line(400, 22, 420, 22, strokeColor=TEXT_MUTED, strokeWidth=1.5))
    # Box 4
    flow.add(Rect(420, 10, 102, 25, fillColor=HexColor("#ecfdf5"), strokeColor=ACCENT_GREEN, strokeWidth=1, rx=3, ry=3))
    flow.add(DString(428, 18, "4. STATUT PALLIATIF", fontName="Helvetica-Bold", fontSize=8, fillColor=ACCENT_GREEN))
    
    story.append(flow)
    story.append(Spacer(1, 8))
    
    # Detailed Steps KeepTogether to avoid break in bad places
    steps_story = []
    steps_story.append(Paragraph("<b>Étape 1 : Modification de la Variable Applicative</b>", sub_section_heading))
    steps_story.append(Paragraph(
        "Définir la variable d'environnement `AGENT_STATUS` à `maintenance` sur le serveur hébergeant l'API.",
        styles['Normal']
    ))
    steps_story.append(Paragraph(
        "# Sous Windows PowerShell :<br/>"
        "<b>[System.Environment]::SetEnvironmentVariable(\"AGENT_STATUS\", \"maintenance\", \"Machine\")</b><br/>"
        "# Sous Linux / Bash :<br/>"
        "<b>export AGENT_STATUS=\"maintenance\"</b>",
        code_style
    ))
    
    steps_story.append(Paragraph("<b>Étape 2 : Relance du Serveur pour Prise en Compte</b>", sub_section_heading))
    steps_story.append(Paragraph(
        "Forcer le redémarrage du processus FastAPI pour charger la nouvelle variable.",
        styles['Normal']
    ))
    steps_story.append(Paragraph(
        "# Relancer le service Systemd (Linux) :<br/>"
        "<b>sudo systemctl restart e-gov-backend.service</b><br/>"
        "# Si lancé manuellement sous Windows :<br/>"
        "<b>Stop-Process -Name \"python\" -Force ; python -m uvicorn backend.app.main:app</b>",
        code_style
    ))
    
    steps_story.append(Paragraph("<b>Étape 3 : Comportement Palliatif de Secours</b>", sub_section_heading))
    steps_story.append(Paragraph(
        "Une fois activé, l'agent court-circuite le modèle génératif et renvoie instantanément :",
        styles['Normal']
    ))
    steps_story.append(Paragraph(
        "<i>« Notre assistant en ligne fait actuellement l'objet d'une maintenance technique. "
        "Pour toute urgence, veuillez nous contacter par téléphone au 3737. »</i>",
        ParagraphStyle('FallbackText', parent=styles['Normal'], fontName='Helvetica-Oblique', backColor=HexColor("#fef2f2"), borderPadding=6, borderWidth=0.5, borderColor=HexColor("#fca5a5"))
    ))
    
    story.append(KeepTogether(steps_story))
    story.append(Spacer(1, 15))
    
    # --- SECTION 3: ROLLBACK ---
    story.append(Paragraph("3. Procédure de \"Rollback\" (Retour Arrière)", section_heading))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#7f1d1d"), spaceAfter=8))
    
    rollback_story = []
    rollback_story.append(Paragraph(
        "Si le déploiement d'une nouvelle configuration ou version de prompt échoue aux tests "
        "ou provoque une baisse de conformité, restaurer immédiatement l'état stable certifié `v1.0.0`.",
        styles['Normal']
    ))
    
    rollback_story.append(Paragraph("<b>A. Commutation Git (Restauration du Code)</b>", sub_section_heading))
    rollback_story.append(Paragraph(
        "# Récupérer les tags du dépôt distant :<br/>"
        "<b>git fetch --tags</b><br/>"
        "# Basculer sur le tag certifié v1.0.0 :<br/>"
        "<b>git checkout tags/v1.0.0</b><br/>"
        "# Créer une branche de correction à partir de ce point stable :<br/>"
        "<b>git checkout -b rollback-release-v1.0.0</b>",
        code_style
    ))
    
    rollback_story.append(Paragraph("<b>B. Reconstruction & Lancement</b>", sub_section_heading))
    rollback_story.append(Paragraph(
        "# Relancer le serveur backend avec le code restauré :<br/>"
        "<b>python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000</b>",
        code_style
    ))
    
    rollback_story.append(Paragraph("<b>C. Validation Après Restauration</b>", sub_section_heading))
    rollback_story.append(Paragraph(
        "L'équipe DevOps doit impérativement exécuter la suite de validation pour certifier le retour à la normale :",
        styles['Normal']
    ))
    rollback_story.append(Paragraph(
        "# 1. Exécution des tests métiers (doit passer au vert) :<br/>"
        "<b>python -m pytest backend/app/tests/</b><br/>"
        "# 2. Interrogation de l'API de santé système :<br/>"
        "<b>curl -I http://127.0.0.1:8000/health</b>",
        code_style
    ))
    
    story.append(KeepTogether(rollback_story))
    
    # Build Document
    doc.build(story)
    print("Runbook PDF successfully generated.")

if __name__ == "__main__":
    create_runbook_pdf("Operational_Runbook.pdf")
