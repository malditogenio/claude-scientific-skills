---
name: pdf
description: "PDF toolkit for marketing reports. Extract campaign data, create branded reports, merge analytics documents, for marketing report generation and analysis."
license: Proprietary. LICENSE.txt has complete terms
---

# PDF Processing for Marketing

## Overview

Extract text and tables from campaign reports, create branded PDF reports, merge analytics documents, and automate marketing report generation using Python libraries. Apply this skill for programmatic document processing of marketing materials and analytics reports.

## When to Use

- **Campaign Report Generation**: Automatically create PDF reports from campaign performance data
- **Client Deliverables**: Generate branded PDF reports for clients and stakeholders
- **Analytics Export**: Extract data from PDF reports provided by advertising platforms
- **Document Automation**: Merge monthly/quarterly reports into comprehensive documents
- **Data Extraction**: Pull metrics from agency reports and third-party analytics PDFs

## Installation

```bash
# Install core PDF libraries
uv pip install pypdf pdfplumber reportlab

# For table extraction and analysis
uv pip install pandas openpyxl

# For branded report creation
uv pip install pillow

# For OCR on scanned documents (optional)
uv pip install pytesseract pdf2image
```

## Core Capabilities

### 1. Extracting Campaign Data from PDF Reports

Many advertising platforms and agencies provide reports in PDF format. Extract this data for analysis:

```python
import pdfplumber
import pandas as pd

# Extract tables from advertising platform report
with pdfplumber.open("facebook_ads_report.pdf") as pdf:
    all_data = []

    for page in pdf.pages:
        # Extract all tables from the page
        tables = page.extract_tables()

        for table in tables:
            if table and len(table) > 1:
                # Convert to DataFrame (first row as headers)
                df = pd.DataFrame(table[1:], columns=table[0])
                all_data.append(df)

    # Combine all tables
    if all_data:
        campaign_data = pd.concat(all_data, ignore_index=True)
        campaign_data.to_csv("extracted_campaign_data.csv", index=False)
```

### 2. Creating Branded Marketing Reports

Generate professional PDF reports with your brand styling:

```python
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def create_marketing_report(filename, campaign_data):
    """Create a branded marketing performance report"""
    doc = SimpleDocTemplate(filename, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)

    story = []
    styles = getSampleStyleSheet()

    # Custom title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=30,
        alignment=TA_CENTER
    )

    # Add logo (if available)
    # story.append(Image('company_logo.png', width=2*inch, height=1*inch))
    # story.append(Spacer(1, 0.5*inch))

    # Title
    title = Paragraph("Q4 2024 Marketing Campaign Report", title_style)
    story.append(title)
    story.append(Spacer(1, 0.3*inch))

    # Executive Summary
    heading_style = styles['Heading2']
    story.append(Paragraph("Executive Summary", heading_style))
    story.append(Spacer(1, 12))

    summary_text = """
    Our Q4 campaigns achieved a 45% increase in conversions compared to Q3,
    with a 23% reduction in cost per acquisition. Total ad spend was $125,000
    with a ROAS of 4.2x.
    """
    story.append(Paragraph(summary_text, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))

    # Campaign Performance Table
    story.append(Paragraph("Campaign Performance", heading_style))
    story.append(Spacer(1, 12))

    data = [
        ['Campaign', 'Impressions', 'Clicks', 'Conversions', 'Spend', 'ROAS'],
        ['Facebook Brand Awareness', '2.5M', '45,000', '1,200', '$35,000', '4.1x'],
        ['Google Search', '1.2M', '68,000', '2,100', '$52,000', '4.8x'],
        ['Instagram Stories', '1.8M', '32,000', '850', '$28,000', '3.5x'],
        ['LinkedIn B2B', '450K', '12,000', '380', '$10,000', '5.2x'],
    ]

    table = Table(data, colWidths=[2.2*inch, 1.1*inch, 0.9*inch, 1.1*inch, 0.9*inch, 0.8*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))

    story.append(table)
    story.append(Spacer(1, 0.3*inch))

    # Key Insights
    story.append(Paragraph("Key Insights", heading_style))
    story.append(Spacer(1, 12))

    insights = [
        "LinkedIn campaigns showed the highest ROAS at 5.2x",
        "Mobile traffic accounted for 68% of all conversions",
        "Video ads outperformed static images by 34%",
        "Retargeting campaigns had 2.3x higher conversion rates"
    ]

    for insight in insights:
        story.append(Paragraph(f"• {insight}", styles['Normal']))
        story.append(Spacer(1, 6))

    # Build PDF
    doc.build(story)

# Generate report
create_marketing_report("marketing_report.pdf", None)
```

### 3. Merging Multiple Campaign Reports

Combine individual campaign reports into a single comprehensive document:

```python
from pypdf import PdfWriter, PdfReader

def merge_campaign_reports(output_filename, report_files):
    """Merge multiple campaign PDFs into one document"""
    writer = PdfWriter()

    for pdf_file in report_files:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            writer.add_page(page)

    with open(output_filename, "wb") as output:
        writer.write(output)

# Merge monthly reports
monthly_reports = [
    "october_campaign_report.pdf",
    "november_campaign_report.pdf",
    "december_campaign_report.pdf"
]

merge_campaign_reports("q4_complete_report.pdf", monthly_reports)
```

### 4. Extracting Marketing Metrics from PDFs

Extract specific metrics from standardized marketing reports:

```python
import pdfplumber
import re

def extract_marketing_metrics(pdf_path):
    """Extract key marketing metrics from PDF report"""
    metrics = {}

    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text()

        # Extract common marketing metrics using regex
        patterns = {
            'impressions': r'Impressions[:\s]+([0-9,]+)',
            'clicks': r'Clicks[:\s]+([0-9,]+)',
            'ctr': r'CTR[:\s]+([0-9.]+)%',
            'cpc': r'CPC[:\s]+\$([0-9.]+)',
            'conversions': r'Conversions[:\s]+([0-9,]+)',
            'roas': r'ROAS[:\s]+([0-9.]+)x',
            'spend': r'Total Spend[:\s]+\$([0-9,]+)'
        }

        for metric, pattern in patterns.items():
            match = re.search(pattern, full_text, re.IGNORECASE)
            if match:
                value = match.group(1).replace(',', '')
                metrics[metric] = float(value)

    return metrics

# Extract metrics
metrics = extract_marketing_metrics("google_ads_report.pdf")
print(f"Campaign Performance:")
print(f"  Impressions: {metrics.get('impressions', 'N/A'):,.0f}")
print(f"  Clicks: {metrics.get('clicks', 'N/A'):,.0f}")
print(f"  CTR: {metrics.get('ctr', 'N/A')}%")
print(f"  ROAS: {metrics.get('roas', 'N/A')}x")
```

### 5. Adding Branding to Existing Reports

Add watermarks or headers to PDFs for client distribution:

```python
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
import io

def add_branded_footer(input_pdf, output_pdf, company_name):
    """Add branded footer to each page"""
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for page_num, page in enumerate(reader.pages):
        # Create footer
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)

        # Add footer text
        can.setFont("Helvetica", 8)
        can.setFillColor(HexColor('#666666'))
        footer_text = f"{company_name} | Confidential Marketing Report | Page {page_num + 1}"
        can.drawCentredString(letter[0]/2, 30, footer_text)
        can.save()

        # Merge footer with page
        packet.seek(0)
        footer_pdf = PdfReader(packet)
        page.merge_page(footer_pdf.pages[0])
        writer.add_page(page)

    with open(output_pdf, "wb") as output:
        writer.write(output)

# Add branding
add_branded_footer("campaign_report.pdf", "branded_report.pdf", "ACME Marketing Agency")
```

### 6. Extracting Text for Content Analysis

Extract text from content marketing PDFs for analysis:

```python
from pypdf import PdfReader

def extract_pdf_text(pdf_path):
    """Extract all text from PDF"""
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text

def analyze_content_keywords(pdf_path):
    """Basic keyword frequency analysis"""
    from collections import Counter
    import re

    text = extract_pdf_text(pdf_path).lower()

    # Remove common words
    common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}

    # Extract words
    words = re.findall(r'\b[a-z]{3,}\b', text)
    words = [w for w in words if w not in common_words]

    # Get top keywords
    keyword_counts = Counter(words)
    top_keywords = keyword_counts.most_common(20)

    return top_keywords

# Analyze white paper
keywords = analyze_content_keywords("marketing_whitepaper.pdf")
print("Top Keywords:")
for keyword, count in keywords:
    print(f"  {keyword}: {count}")
```

## Quick Start

### Extract Campaign Data

```python
import pdfplumber
import pandas as pd

# Extract tables from marketing report
with pdfplumber.open("campaign_report.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        if tables:
            df = pd.DataFrame(tables[0][1:], columns=tables[0][0])
            print(df)
```

### Create Simple Report

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("campaign_summary.pdf", pagesize=letter)
width, height = letter

# Title
c.setFont("Helvetica-Bold", 18)
c.drawString(100, height - 100, "Campaign Performance Report")

# Metrics
c.setFont("Helvetica", 12)
c.drawString(100, height - 150, "Impressions: 2,500,000")
c.drawString(100, height - 170, "Clicks: 45,000")
c.drawString(100, height - 190, "Conversions: 1,200")
c.drawString(100, height - 210, "ROAS: 4.2x")

c.save()
```

### Merge Reports

```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()

for month in ["jan", "feb", "mar"]:
    reader = PdfReader(f"{month}_report.pdf")
    for page in reader.pages:
        writer.add_page(page)

with open("q1_report.pdf", "wb") as output:
    writer.write(output)
```

## Common Marketing Workflows

### Agency Report Automation

```python
def generate_client_report(client_name, campaign_data):
    """Generate monthly client report"""
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
    from reportlab.lib.styles import getSampleStyleSheet

    filename = f"{client_name}_monthly_report.pdf"
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title = Paragraph(f"{client_name} - Monthly Report", styles['Title'])
    story.append(title)

    # Performance table
    table_data = [['Metric', 'This Month', 'Last Month', 'Change']]
    table_data.extend(campaign_data)

    table = Table(table_data)
    story.append(table)

    doc.build(story)
    return filename
```

### Multi-Platform Report Consolidation

```python
def consolidate_platform_reports(platforms):
    """Merge reports from different marketing platforms"""
    all_metrics = {}

    for platform, pdf_path in platforms.items():
        metrics = extract_marketing_metrics(pdf_path)
        all_metrics[platform] = metrics

    # Create consolidated report
    create_consolidated_report(all_metrics)
```

## References

### Python Libraries

- **pypdf**: Modern PDF manipulation library
  - [Documentation](https://pypdf.readthedocs.io/)
  - Merge, split, rotate, encrypt PDFs

- **pdfplumber**: Advanced text and table extraction
  - [Documentation](https://github.com/jsvine/pdfplumber)
  - Best for extracting structured data

- **reportlab**: Professional PDF creation
  - [Documentation](https://www.reportlab.com/docs/reportlab-userguide.pdf)
  - Full layout control, tables, charts

- **pandas**: Data analysis and manipulation
  - [Documentation](https://pandas.pydata.org/docs/)
  - Essential for working with extracted data

### Command-Line Tools

```bash
# Install poppler-utils for CLI tools
sudo apt-get install poppler-utils

# Extract text
pdftotext marketing_report.pdf

# Convert PDF to images
pdftoppm -jpeg -r 150 report.pdf page

# Merge PDFs with qpdf
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf
```

### Best Practices

1. **Data Validation**: Always validate extracted data for completeness
2. **Brand Consistency**: Use templates for consistent branded reports
3. **Automation**: Script repetitive report generation tasks
4. **Version Control**: Include date stamps and version numbers in reports
5. **File Naming**: Use consistent naming conventions (client_platform_date.pdf)
6. **Quality Check**: Review generated PDFs before client distribution
7. **Performance**: Use `read_only=True` for large PDFs when only reading data

### Marketing-Specific Tips

- **Campaign Reports**: Standardize table formats for easier extraction
- **Client Deliverables**: Include executive summaries at the beginning
- **Data Visualization**: Consider creating charts in Python first, then embedding in PDF
- **Compliance**: Add disclaimers and date stamps to all reports
- **Archiving**: Maintain PDF archives of all campaign reports for historical analysis
