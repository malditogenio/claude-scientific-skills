---
name: pptx
description: "PowerPoint toolkit for marketing presentations. Create campaign decks, stakeholder presentations, pitch decks, performance reviews, for marketing communications."
license: Proprietary. LICENSE.txt has complete terms
---

# PowerPoint Creation for Marketing

## Overview

Create professional marketing presentations, campaign pitch decks, stakeholder reports, and client deliverables using Python. Apply this skill for automating presentation creation, generating branded decks, and building data-driven slide presentations.

## When to Use

- **Campaign Pitch Decks**: Create presentations for new campaign proposals
- **Client Reports**: Generate monthly/quarterly performance presentations
- **Stakeholder Updates**: Build executive summaries and board presentations
- **Sales Enablement**: Create product marketing and sales pitch decks
- **Event Presentations**: Prepare conference and webinar slides
- **Brand Guidelines**: Document brand standards and style guides
- **Training Materials**: Develop marketing team training decks

## Installation

```bash
# Install python-pptx for presentation creation
uv pip install python-pptx

# For image processing
uv pip install pillow

# For chart generation
uv pip install matplotlib pandas

# Optional: For template extraction
uv pip install markitdown
```

## Core Capabilities

### 1. Creating Campaign Pitch Decks

Build professional campaign proposal presentations:

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

def create_campaign_pitch(campaign_name, output_file):
    """Create a campaign pitch deck"""

    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    # Slide 1: Title Slide
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)

    title = slide.shapes.title
    subtitle = slide.placeholders[1]

    title.text = campaign_name
    subtitle.text = "Campaign Proposal | Q1 2024"

    # Format title
    title.text_frame.paragraphs[0].font.size = Pt(44)
    title.text_frame.paragraphs[0].font.bold = True
    title.text_frame.paragraphs[0].font.color.rgb = RGBColor(44, 62, 80)

    # Slide 2: Campaign Overview
    bullet_slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(bullet_slide_layout)

    title = slide.shapes.title
    body = slide.placeholders[1]

    title.text = "Campaign Overview"

    tf = body.text_frame
    tf.text = "Objective"

    p = tf.add_paragraph()
    p.text = "Increase brand awareness by 40% in target demographic"
    p.level = 1

    p = tf.add_paragraph()
    p.text = "Generate 10,000 qualified leads for sales team"
    p.level = 1

    p = tf.add_paragraph()
    p.text = "Achieve 4.5x ROAS across all channels"
    p.level = 1

    # Slide 3: Target Audience
    slide = prs.slides.add_slide(bullet_slide_layout)
    title = slide.shapes.title
    body = slide.placeholders[1]

    title.text = "Target Audience"

    tf = body.text_frame
    tf.text = "Primary Audience"

    demographics = [
        "Age: 25-45 years old",
        "Income: $75,000+",
        "Location: Urban metros",
        "Interests: Technology, sustainability, innovation"
    ]

    for demo in demographics:
        p = tf.add_paragraph()
        p.text = demo
        p.level = 1

    # Slide 4: Channel Strategy
    slide = prs.slides.add_slide(bullet_slide_layout)
    title = slide.shapes.title
    title.text = "Multi-Channel Strategy"

    # Add table for channel breakdown
    rows, cols = 5, 4
    left = Inches(1.5)
    top = Inches(2.5)
    width = Inches(7)
    height = Inches(3)

    table = slide.shapes.add_table(rows, cols, left, top, width, height).table

    # Table headers
    table.cell(0, 0).text = "Channel"
    table.cell(0, 1).text = "Budget %"
    table.cell(0, 2).text = "Expected Reach"
    table.cell(0, 3).text = "Primary Goal"

    # Style header row
    for col in range(cols):
        cell = table.cell(0, col)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(52, 152, 219)
        cell.text_frame.paragraphs[0].font.bold = True
        cell.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
        cell.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Channel data
    channels = [
        ["Paid Search", "35%", "2.5M", "Lead Generation"],
        ["Social Media", "30%", "5M", "Brand Awareness"],
        ["Display", "20%", "8M", "Retargeting"],
        ["Email", "15%", "500K", "Nurturing"]
    ]

    for row, channel in enumerate(channels, start=1):
        for col, value in enumerate(channel):
            table.cell(row, col).text = value
            table.cell(row, col).text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Slide 5: Budget Overview
    slide = prs.slides.add_slide(prs.slide_layouts[5])  # Blank layout
    title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_shape.text_frame
    title_frame.text = "Budget Allocation"
    title_frame.paragraphs[0].font.size = Pt(32)
    title_frame.paragraphs[0].font.bold = True

    # Budget details
    budget_box = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(8), Inches(4))
    budget_frame = budget_box.text_frame

    budget_items = [
        ("Total Campaign Budget:", "$150,000"),
        ("Media Spend:", "$105,000 (70%)"),
        ("Creative Production:", "$30,000 (20%)"),
        ("Tools & Technology:", "$10,000 (7%)"),
        ("Contingency:", "$5,000 (3%)")
    ]

    for label, value in budget_items:
        p = budget_frame.add_paragraph()
        p.text = f"{label}\t{value}"
        p.font.size = Pt(18)
        p.space_after = Pt(12)

    prs.save(output_file)

# Create campaign pitch
create_campaign_pitch("Spring Product Launch Campaign", "campaign_pitch.pptx")
```

### 2. Generating Client Performance Reports

Create automated monthly client reports:

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.dml.color import RGBColor
import pandas as pd

def create_client_report(client_name, performance_data, output_file):
    """Create automated client performance report"""

    prs = Presentation()

    # Title Slide
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    title = slide.shapes.title
    subtitle = slide.placeholders[1]

    title.text = f"{client_name} Performance Report"
    subtitle.text = "November 2024 | Digital Marketing Results"

    # Executive Summary Slide
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title = slide.shapes.title
    body = slide.placeholders[1]

    title.text = "Executive Summary"

    tf = body.text_frame
    tf.text = "Key Highlights"

    highlights = [
        "45% increase in conversions vs. previous month",
        "ROAS improved to 4.2x (target: 3.5x)",
        "Cost per acquisition decreased by 23%",
        "Total revenue generated: $525,000"
    ]

    for highlight in highlights:
        p = tf.add_paragraph()
        p.text = highlight
        p.level = 1
        p.font.size = Pt(18)

    # Performance Metrics Slide with Chart
    slide = prs.slides.add_slide(prs.slide_layouts[5])

    # Add title
    title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_shape.text_frame
    title_frame.text = "Campaign Performance Trends"
    title_frame.paragraphs[0].font.size = Pt(28)
    title_frame.paragraphs[0].font.bold = True

    # Add line chart
    chart_data = CategoryChartData()
    chart_data.categories = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
    chart_data.add_series('Conversions', (250, 285, 310, 340))
    chart_data.add_series('Goal', (300, 300, 300, 300))

    x, y, cx, cy = Inches(1), Inches(2), Inches(8), Inches(4)
    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.LINE, x, y, cx, cy, chart_data
    ).chart

    chart.has_legend = True
    chart.legend.position = XL_CHART_TYPE.BOTTOM

    # Channel Performance Table
    slide = prs.slides.add_slide(prs.slide_layouts[5])

    title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_shape.text_frame
    title_frame.text = "Performance by Channel"
    title_frame.paragraphs[0].font.size = Pt(28)
    title_frame.paragraphs[0].font.bold = True

    # Add table
    rows, cols = 5, 6
    table = slide.shapes.add_table(
        rows, cols, Inches(0.5), Inches(1.5), Inches(9), Inches(3.5)
    ).table

    # Headers
    headers = ['Channel', 'Impressions', 'Clicks', 'Conv.', 'Spend', 'ROAS']
    for col, header in enumerate(headers):
        cell = table.cell(0, col)
        cell.text = header
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(41, 128, 185)
        cell.text_frame.paragraphs[0].font.bold = True
        cell.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)

    # Data
    data = [
        ['Google Ads', '1.2M', '28K', '680', '$52K', '4.8x'],
        ['Facebook', '800K', '12K', '350', '$35K', '3.9x'],
        ['LinkedIn', '500K', '5K', '170', '$38K', '4.1x'],
        ['Total', '2.5M', '45K', '1.2K', '$125K', '4.2x']
    ]

    for row_idx, row_data in enumerate(data, start=1):
        for col_idx, value in enumerate(row_data):
            table.cell(row_idx, col_idx).text = value

    # Next Steps Slide
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title = slide.shapes.title
    body = slide.placeholders[1]

    title.text = "Recommendations & Next Steps"

    tf = body.text_frame
    tf.text = "Optimize Performance"

    recommendations = [
        "Increase budget allocation to Google Ads (highest ROAS)",
        "Test new creative variations for Facebook campaigns",
        "Expand LinkedIn targeting to include lookalike audiences",
        "Implement retargeting campaign for abandoned carts"
    ]

    for rec in recommendations:
        p = tf.add_paragraph()
        p.text = rec
        p.level = 1

    prs.save(output_file)

# Generate report
create_client_report("ACME Corporation", None, "client_report_november.pptx")
```

### 3. Creating Visual Brand Presentations

Build branded presentations with consistent styling:

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

def apply_brand_styling(prs, brand_colors):
    """Apply consistent brand styling to presentation"""

    # Define brand colors
    primary_color = RGBColor(*brand_colors['primary'])
    secondary_color = RGBColor(*brand_colors['secondary'])
    accent_color = RGBColor(*brand_colors['accent'])

    return {
        'primary': primary_color,
        'secondary': secondary_color,
        'accent': accent_color
    }

def create_branded_presentation(company_name, brand_colors, output_file):
    """Create a branded marketing presentation"""

    prs = Presentation()
    colors = apply_brand_styling(prs, brand_colors)

    # Cover Slide with Brand Colors
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank

    # Add colored background shape
    background = slide.shapes.add_shape(
        1,  # Rectangle
        Inches(0), Inches(0),
        Inches(10), Inches(7.5)
    )
    background.fill.solid()
    background.fill.fore_color.rgb = colors['primary']
    background.line.fill.background()

    # Add title
    title_box = slide.shapes.add_textbox(Inches(1), Inches(3), Inches(8), Inches(2))
    title_frame = title_box.text_frame
    title_frame.text = company_name
    title_frame.paragraphs[0].font.size = Pt(54)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    title_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Add subtitle
    subtitle_box = slide.shapes.add_textbox(Inches(1), Inches(5), Inches(8), Inches(1))
    subtitle_frame = subtitle_box.text_frame
    subtitle_frame.text = "Marketing Strategy 2024"
    subtitle_frame.paragraphs[0].font.size = Pt(28)
    subtitle_frame.paragraphs[0].font.color.rgb = colors['accent']
    subtitle_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Content Slide with Brand Elements
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Header bar
    header = slide.shapes.add_shape(
        1,  # Rectangle
        Inches(0), Inches(0),
        Inches(10), Inches(1)
    )
    header.fill.solid()
    header.fill.fore_color.rgb = colors['primary']
    header.line.fill.background()

    # Title in header
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(9), Inches(0.6))
    title_frame = title_box.text_frame
    title_frame.text = "Our Marketing Approach"
    title_frame.paragraphs[0].font.size = Pt(32)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)

    # Content boxes
    box_width = 2.5
    box_height = 3.5
    boxes = [
        ("Research", Inches(1), Inches(2)),
        ("Strategy", Inches(3.75), Inches(2)),
        ("Execution", Inches(6.5), Inches(2))
    ]

    for title, left, top in boxes:
        # Box
        box = slide.shapes.add_shape(
            1,  # Rectangle
            left, top,
            Inches(box_width), Inches(box_height)
        )
        box.fill.solid()
        box.fill.fore_color.rgb = colors['secondary']
        box.line.color.rgb = colors['accent']
        box.line.width = Pt(2)

        # Title
        text_box = slide.shapes.add_textbox(left, top + Inches(0.3), Inches(box_width), Inches(0.5))
        text_frame = text_box.text_frame
        text_frame.text = title
        text_frame.paragraphs[0].font.size = Pt(24)
        text_frame.paragraphs[0].font.bold = True
        text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    prs.save(output_file)

# Create branded presentation
brand_colors = {
    'primary': (41, 128, 185),    # Blue
    'secondary': (236, 240, 241),  # Light gray
    'accent': (243, 156, 18)       # Orange
}

create_branded_presentation("TechCorp Marketing", brand_colors, "branded_deck.pptx")
```

### 4. Generating Data-Driven Slides

Create slides with charts and data visualizations:

```python
from pptx import Presentation
from pptx.chart.data import CategoryChartData, ChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches, Pt

def create_data_driven_presentation(data, output_file):
    """Create presentation with data visualizations"""

    prs = Presentation()

    # Bar Chart Slide - Channel Performance
    slide = prs.slides.add_slide(prs.slide_layouts[5])

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.6))
    title_frame = title_box.text_frame
    title_frame.text = "Conversions by Channel"
    title_frame.paragraphs[0].font.size = Pt(28)
    title_frame.paragraphs[0].font.bold = True

    # Bar chart
    chart_data = CategoryChartData()
    chart_data.categories = ['Google Ads', 'Facebook', 'LinkedIn', 'Email']
    chart_data.add_series('Conversions', (680, 350, 170, 245))

    x, y, cx, cy = Inches(1), Inches(1.5), Inches(8), Inches(5)
    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data
    ).chart

    # Pie Chart Slide - Budget Allocation
    slide = prs.slides.add_slide(prs.slide_layouts[5])

    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.6))
    title_frame = title_box.text_frame
    title_frame.text = "Budget Distribution"
    title_frame.paragraphs[0].font.size = Pt(28)
    title_frame.paragraphs[0].font.bold = True

    # Pie chart
    chart_data = CategoryChartData()
    chart_data.categories = ['Paid Search', 'Social Media', 'Display', 'Email']
    chart_data.add_series('Budget %', (35, 30, 20, 15))

    x, y, cx, cy = Inches(2), Inches(1.5), Inches(6), Inches(5)
    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.PIE, x, y, cx, cy, chart_data
    ).chart

    chart.has_legend = True
    chart.legend.position = 2  # Right

    # Line Chart Slide - Trend Analysis
    slide = prs.slides.add_slide(prs.slide_layouts[5])

    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.6))
    title_frame = title_box.text_frame
    title_frame.text = "Monthly Conversion Trend"
    title_frame.paragraphs[0].font.size = Pt(28)
    title_frame.paragraphs[0].font.bold = True

    # Line chart
    chart_data = CategoryChartData()
    chart_data.categories = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    chart_data.add_series('2024', (850, 920, 1050, 980, 1120, 1200))
    chart_data.add_series('2023', (720, 780, 810, 850, 890, 920))

    x, y, cx, cy = Inches(1), Inches(1.5), Inches(8), Inches(5)
    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.LINE, x, y, cx, cy, chart_data
    ).chart

    chart.has_legend = True

    prs.save(output_file)

create_data_driven_presentation(None, "data_presentation.pptx")
```

### 5. Creating Automated Report Templates

Build reusable templates for recurring reports:

```python
def create_monthly_template(template_file):
    """Create reusable monthly report template"""

    prs = Presentation()

    # Slide 1: Title
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    title.text = "[CLIENT NAME] - Monthly Report"
    subtitle.text = "[MONTH YEAR]"

    # Slide 2: Key Metrics Summary
    slide = prs.slides.add_slide(prs.slide_layouts[5])

    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.6))
    title_frame = title_box.text_frame
    title_frame.text = "Key Performance Indicators"
    title_frame.paragraphs[0].font.size = Pt(28)
    title_frame.paragraphs[0].font.bold = True

    # KPI boxes
    kpis = [
        ("[IMPRESSIONS]", "Impressions", Inches(1), Inches(2)),
        ("[CLICKS]", "Clicks", Inches(3.5), Inches(2)),
        ("[CONVERSIONS]", "Conversions", Inches(6), Inches(2)),
        ("[ROAS]", "ROAS", Inches(1), Inches(4.5)),
        ("[CPA]", "CPA", Inches(3.5), Inches(4.5)),
        ("[CTR]", "CTR", Inches(6), Inches(4.5))
    ]

    for value, label, left, top in kpis:
        # Value box
        box = slide.shapes.add_shape(1, left, top, Inches(2), Inches(1.5))
        box.fill.solid()
        box.fill.fore_color.rgb = RGBColor(52, 152, 219)

        # Value text
        value_box = slide.shapes.add_textbox(left, top + Inches(0.2), Inches(2), Inches(0.7))
        value_frame = value_box.text_frame
        value_frame.text = value
        value_frame.paragraphs[0].font.size = Pt(36)
        value_frame.paragraphs[0].font.bold = True
        value_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
        value_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

        # Label text
        label_box = slide.shapes.add_textbox(left, top + Inches(0.95), Inches(2), Inches(0.4))
        label_frame = label_box.text_frame
        label_frame.text = label
        label_frame.paragraphs[0].font.size = Pt(14)
        label_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
        label_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Slide 3: Channel Performance (placeholder for table)
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.6))
    title_frame = title_box.text_frame
    title_frame.text = "Performance by Channel"
    title_frame.paragraphs[0].font.size = Pt(28)
    title_frame.paragraphs[0].font.bold = True

    # Slide 4: Insights & Recommendations
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title = slide.shapes.title
    body = slide.placeholders[1]
    title.text = "Key Insights & Recommendations"
    body.text = "[Insert key insights and recommendations here]"

    prs.save(template_file)

create_monthly_template("monthly_report_template.pptx")
```

## Quick Start

### Create Basic Presentation

```python
from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation()

# Title slide
slide = prs.slides.add_slide(prs.slide_layouts[0])
title = slide.shapes.title
subtitle = slide.placeholders[1]

title.text = "Q4 Marketing Review"
subtitle.text = "Campaign Performance Summary"

# Content slide
slide = prs.slides.add_slide(prs.slide_layouts[1])
title = slide.shapes.title
body = slide.placeholders[1]

title.text = "Campaign Highlights"
tf = body.text_frame
tf.text = "45% increase in conversions"

p = tf.add_paragraph()
p.text = "ROAS improved to 4.2x"
p.level = 0

prs.save("marketing_review.pptx")
```

### Add Charts

```python
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

# Create chart data
chart_data = CategoryChartData()
chart_data.categories = ['Q1', 'Q2', 'Q3', 'Q4']
chart_data.add_series('Revenue', (50000, 65000, 72000, 85000))

# Add chart to slide
slide = prs.slides.add_slide(prs.slide_layouts[5])
chart = slide.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED,
    Inches(1), Inches(1.5), Inches(8), Inches(5),
    chart_data
).chart
```

### Add Tables

```python
# Add table
slide = prs.slides.add_slide(prs.slide_layouts[5])
rows, cols = 4, 3
table = slide.shapes.add_table(
    rows, cols, Inches(2), Inches(2), Inches(6), Inches(3)
).table

# Populate table
table.cell(0, 0).text = "Channel"
table.cell(0, 1).text = "Spend"
table.cell(0, 2).text = "ROAS"
```

## Best Practices

### Design Principles

1. **Consistent Branding**: Use brand colors and fonts throughout
2. **One Message Per Slide**: Keep slides focused on single concepts
3. **Visual Hierarchy**: Use size and color to emphasize important information
4. **White Space**: Don't overcrowd slides
5. **Data Visualization**: Use charts instead of tables when possible

### Content Guidelines

1. **Executive Summaries**: Start with key takeaways
2. **Data Context**: Always provide comparison points (vs. last month, vs. goal)
3. **Actionable Insights**: End with clear recommendations
4. **Concise Text**: Use bullet points, not paragraphs
5. **Supporting Details**: Put detailed data in appendix slides

### Automation Tips

```python
# Use functions for repetitive slide creation
def add_metric_slide(prs, title, metric, value):
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = title
    # ... add metric visualization
    return slide

# Loop through data to create multiple slides
for metric in metrics_list:
    add_metric_slide(prs, metric['title'], metric['name'], metric['value'])
```

## References

### Libraries

- **python-pptx**: PowerPoint creation library
  - [Documentation](https://python-pptx.readthedocs.io/)
  - Create and modify presentations programmatically

- **pillow**: Image processing
  - [Documentation](https://pillow.readthedocs.io/)
  - Resize and format images for slides

- **matplotlib**: Chart generation
  - [Documentation](https://matplotlib.org/)
  - Create charts to embed in presentations

### Marketing Presentation Types

1. **Campaign Pitch Decks**: Proposal presentations for new campaigns
2. **Client Reports**: Regular performance updates
3. **Strategy Presentations**: Long-term planning and roadmaps
4. **Stakeholder Updates**: Executive summaries and board presentations
5. **Training Materials**: Educational content for teams
6. **Sales Enablement**: Product marketing and sales support

### Common Slide Structures

```python
# Cover Slide
layouts[0]  # Title and subtitle

# Content Slide with Bullets
layouts[1]  # Title and content

# Section Header
layouts[2]  # Section header

# Two Content Areas
layouts[3]  # Title and two content areas

# Comparison
layouts[4]  # Title and comparison

# Blank
layouts[5]  # Title only

# Completely Blank
layouts[6]  # No placeholders
```

### File Naming Conventions

- Use descriptive names: `client-name_report-type_YYYY-MM.pptx`
- Version control: Include v1, v2, or final in filename
- Examples:
  - `acme_monthly-report_2024-11.pptx`
  - `q4-campaign_pitch-deck_final.pptx`
  - `stakeholder-update_2024-q4_v2.pptx`
