import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.colors import HexColor

def create_agent_card_pdf(output_path):
    # Setup document with 0.5 inch margins for max space and modern look
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
    PRIMARY_COLOR = HexColor("#0f172a")    # Very dark slate / Navy
    SECONDARY_COLOR = HexColor("#2563eb")  # Premium Blue
    ACCENT_COLOR = HexColor("#10b981")     # Emerald Green
    BG_LIGHT = HexColor("#f8fafc")         # Light blue-gray for rows
    TEXT_DARK = HexColor("#1e293b")        # Dark slate for text
    TEXT_MUTED = HexColor("#64748b")       # Muted gray for subtitles
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Modify existing styles to avoid conflicts
    styles['Normal'].textColor = TEXT_DARK
    styles['Normal'].fontSize = 9.5
    styles['Normal'].leading = 13
    
    # Create unique custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.white,
        alignment=0 # Left aligned
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=HexColor("#94a3b8"), # Light gray
        alignment=0
    )
    
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=SECONDARY_COLOR,
        spaceBefore=12,
        spaceAfter=6
    )
    
    cell_bold = ParagraphStyle(
        'CellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=PRIMARY_COLOR
    )
    
    cell_normal = ParagraphStyle(
        'CellNormal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=TEXT_DARK
    )
    
    cell_tag = ParagraphStyle(
        'CellTag',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=SECONDARY_COLOR
    )

    # --- HEADER BANNER ---
    # We will put the header in a beautiful dark slate colored table
    header_data = [
        [
            Paragraph("AGENT CARD / FICHE D'IDENTITÉ DE L'AGENT", subtitle_style),
            ""
        ],
        [
            Paragraph("ASSISTANT CITOYEN E-GOV", title_style),
            Paragraph("Version 1.0.0 (Stable)<br/>Statut : <b>CERTIFIÉ CONFORME</b>", ParagraphStyle(
                'HeaderStatus',
                parent=styles['Normal'],
                fontName='Helvetica',
                fontSize=9,
                leading=13,
                textColor=HexColor("#38bdf8"), # Sky blue
                alignment=2 # Right aligned
            ))
        ]
    ]
    
    # Width of the usable page is 612 - 80 = 532
    header_table = Table(header_data, colWidths=[350, 182])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), PRIMARY_COLOR),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('SPAN', (0,0), (1,0)), # Span subtitle across header
        ('PADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,1), (-1,1), 16),
        ('TOPPADDING', (0,0), (-1,0), 16),
    ]))
    
    story.append(header_table)
    story.append(Spacer(1, 15))
    
    # --- METRICS OVERVIEW ---
    # Horizontal summary cards row
    metrics_data = [
        [
            Paragraph("<b>SCORE DE CONFORMITÉ</b><br/><font color='#10b981' size='14'><b>91.25%</b></font><br/><font size='7' color='#64748b'>Seuil exigé : 80%</font>", ParagraphStyle('Card1', parent=styles['Normal'], alignment=1)),
            Paragraph("<b>SUITE DE TESTS (GOLDEN SET)</b><br/><font color='#2563eb' size='14'><b>20 Scénarios</b></font><br/><font size='7' color='#64748b'>Validation continue</font>", ParagraphStyle('Card2', parent=styles['Normal'], alignment=1)),
            Paragraph("<b>TEMPS D'EXÉCUTION CI</b><br/><font color='#7c3aed' size='14'><b>2.82 secondes</b></font><br/><font size='7' color='#64748b'>Mocks déterministes</font>", ParagraphStyle('Card3', parent=styles['Normal'], alignment=1))
        ]
    ]
    metrics_table = Table(metrics_data, colWidths=[177, 177, 178])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor("#f1f5f9")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOX', (0,0), (-1,-1), 1, HexColor("#e2e8f0")),
        ('INNERGRID', (0,0), (-1,-1), 1, HexColor("#e2e8f0")),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    
    story.append(metrics_table)
    story.append(Spacer(1, 15))
    
    # --- SECTION: SPECIFICATIONS GENERALES ---
    story.append(Paragraph("1. Spécifications Générales", section_heading))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY_COLOR, spaceAfter=8))
    
    general_data = [
        [
            Paragraph("Nom de l'agent", cell_bold),
            Paragraph("<b>Assistant Citoyen E-Gov</b> (e-Gov Citizen Assistant)", cell_normal)
        ],
        [
            Paragraph("Description", cell_bold),
            Paragraph("Agent conversationnel intelligent conçu pour orienter les citoyens dans leurs démarches administratives, recueillir leurs réclamations et traiter de manière sécurisée les requêtes sensibles ou politiques.", cell_normal)
        ],
        [
            Paragraph("Modèles de Fondation", cell_bold),
            Paragraph("<b>Production</b> : Gemini 1.5 Flash (API Cloud sécurisée)<br/><b>Validation & CI/CD</b> : Simulateur d'intention hors-ligne déterministe (zéro coût, vitesse maximale)", cell_normal)
        ],
        [
            Paragraph("Cas d'usage cibles", cell_bold),
            Paragraph("• Demandes administratives (État civil, CNI, passeport, permis)<br/>• Réclamations et plaintes d'usagers (factures, retards, bugs)<br/>• Filtrage et signalement sécurisé des alertes éthiques et de corruption", cell_normal)
        ]
    ]
    
    general_table = Table(general_data, colWidths=[130, 402])
    general_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,-2), 0.5, HexColor("#e2e8f0")),
        ('BACKGROUND', (0,0), (0,-1), HexColor("#f8fafc")),
    ]))
    story.append(general_table)
    story.append(Spacer(1, 15))
    
    # --- SECTION: INPUTS / OUTPUTS & DEPENDANCES ---
    story.append(Paragraph("2. Flux de Données & Dépendances", section_heading))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY_COLOR, spaceAfter=8))
    
    flux_data = [
        [
            Paragraph("Format des Entrées (Inputs)", cell_bold),
            Paragraph("Texte brut (saisie libre du citoyen). Longueur typique de 10 à 500 caractères.", cell_normal)
        ],
        [
            Paragraph("Structure des Sorties (Outputs)", cell_bold),
            Paragraph("Objet JSON structuré contenant :<br/>"
                      "• <b>response</b> (str) : Réponse finale rédigée de façon polie et conforme.<br/>"
                      "• <b>intent</b> (str) : Intention classifiée (ex: <i>demande_document</i>, <i>reclamation</i>).<br/>"
                      "• <b>confidence</b> (float) : Score de confiance de l'intention (0.0 à 1.0).<br/>"
                      "• <b>tokens_used</b> (int) : Nombre de tokens consommés lors de la génération.<br/>"
                      "• <b>latency_ms</b> (int) : Latence de réponse de l'agent en millisecondes.", cell_normal)
        ],
        [
            Paragraph("Dépendances Techniques", cell_bold),
            Paragraph("• <b>FastAPI v0.110.0+</b> : Serveur web haute performance.<br/>"
                      "• <b>Uvicorn v0.28.0+</b> : Serveur de production ASGI.<br/>"
                      "• <b>Pydantic v2.0+</b> : Modélisation et validation stricte des structures de données.<br/>"
                      "• <b>Pytest v8.0+</b> : Suite d'évaluation automatique de non-régression.", cell_normal)
        ]
    ]
    
    flux_table = Table(flux_data, colWidths=[130, 402])
    flux_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,-2), 0.5, HexColor("#e2e8f0")),
        ('BACKGROUND', (0,0), (0,-1), HexColor("#f8fafc")),
    ]))
    story.append(flux_table)
    story.append(Spacer(1, 15))
    
    # --- SECTION: LIMITES DE SECURITE ---
    story.append(Paragraph("3. Limites de Sécurité & Guardrails (Gouvernance)", section_heading))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY_COLOR, spaceAfter=8))
    
    security_data = [
        [
            Paragraph("1. Neutralité Politique", cell_bold),
            Paragraph("Interdiction formelle de commenter les élections ou de donner un avis politique. Redirection immédiate de toute question sensible vers l'<b>Instance Nationale de Probité et de Lutte contre la Corruption (INPLC)</b>.", cell_normal)
        ],
        [
            Paragraph("2. Ton Institutionnel (E-Gov)", cell_bold),
            Paragraph("Obligation stricte d'inclure des termes de courtoisie administrative standardisés (ex: <i>Bonjour, Monsieur/Madame, Cher citoyen, Veuillez...</i>). Les réponses sèches ou impolies sont pénalisées par le validateur.", cell_normal)
        ],
        [
            Paragraph("3. Protection des Données (No-Leak)", cell_bold),
            Paragraph("Blocage automatique de toute fuite d'erreur technique interne ou d'exception de base de données (ex: <i>Fatal error, database connection lost, thread dump</i>) pour garantir la sécurité et la réputation de l'infrastructure.", cell_normal)
        ],
        [
            Paragraph("4. Prévention des Hallucinations", cell_bold),
            Paragraph("Interdiction de retourner des gabarits de développement ou variables non interpolées (ex: <i>[placeholder], {variable}</i>). Le score de conformité doit être supérieur à 80% pour autoriser l'affichage.", cell_normal)
        ]
    ]
    
    security_table = Table(security_data, colWidths=[130, 402])
    security_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 7),
        ('LINEBELOW', (0,0), (-1,-2), 0.5, HexColor("#e2e8f0")),
        ('BACKGROUND', (0,0), (0,-1), HexColor("#f8fafc")),
    ]))
    story.append(security_table)
    story.append(Spacer(1, 10))
    
    # --- FOOTER BANNER ---
    footer_text = Paragraph(
        "Ce document fait partie des livrables de conformité réglementaire de la plateforme e-gov. "
        "Dépôt Git associé : <i>gouvernance-agents-ia</i>. Tag de release certifié : <b>v1.0.0</b>.",
        ParagraphStyle('FooterText', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=7.5, textColor=TEXT_MUTED, alignment=1)
    )
    story.append(Spacer(1, 10))
    story.append(footer_text)
    
    # Build Document
    doc.build(story)
    print("PDF successfully generated.")

if __name__ == "__main__":
    create_agent_card_pdf("Agent_Card.pdf")
