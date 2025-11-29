---
name: xlsx
description: "Excel toolkit for marketing data. Import campaign data, create dashboards, analyze performance metrics, export to marketing platforms, for data-driven marketing decisions."
license: Proprietary. LICENSE.txt has complete terms
---

# Excel Processing for Marketing

## Overview

Import campaign data from marketing platforms, create performance dashboards, analyze marketing metrics, and export data for ad platforms using Python. Apply this skill for marketing data analysis, reporting automation, and campaign optimization.

## When to Use

- **Campaign Data Import**: Import data from Google Ads, Facebook Ads, LinkedIn, etc.
- **Performance Dashboards**: Create executive dashboards with KPIs and trends
- **Budget Tracking**: Monitor spend across campaigns and channels
- **Attribution Analysis**: Analyze multi-touch attribution data
- **Bulk Upload Preparation**: Format data for platform bulk uploads
- **Client Reporting**: Generate automated Excel reports for clients
- **A/B Test Analysis**: Analyze test results and statistical significance

## Installation

```bash
# Core Excel libraries
uv pip install openpyxl pandas

# For data analysis
uv pip install numpy scipy

# For chart creation
uv pip install xlsxwriter

# For reading various formats
uv pip install xlrd
```

## Core Capabilities

### 1. Importing Campaign Data from Marketing Platforms

Import and consolidate data from multiple marketing platforms:

```python
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils.dataframe import dataframe_to_rows

def import_campaign_data(sources):
    """Import and combine campaign data from multiple platforms"""

    # Read data from different sources
    google_ads = pd.read_csv('google_ads_export.csv')
    facebook_ads = pd.read_csv('facebook_ads_export.csv')
    linkedin_ads = pd.read_csv('linkedin_ads_export.csv')

    # Standardize column names
    google_ads = google_ads.rename(columns={
        'Campaign': 'campaign_name',
        'Impressions': 'impressions',
        'Clicks': 'clicks',
        'Cost': 'spend'
    })

    facebook_ads = facebook_ads.rename(columns={
        'Campaign Name': 'campaign_name',
        'Impressions': 'impressions',
        'Link Clicks': 'clicks',
        'Amount Spent (USD)': 'spend'
    })

    # Add platform identifier
    google_ads['platform'] = 'Google Ads'
    facebook_ads['platform'] = 'Facebook Ads'
    linkedin_ads['platform'] = 'LinkedIn Ads'

    # Combine all data
    all_campaigns = pd.concat([google_ads, facebook_ads, linkedin_ads], ignore_index=True)

    # Calculate derived metrics
    all_campaigns['ctr'] = (all_campaigns['clicks'] / all_campaigns['impressions'] * 100).round(2)
    all_campaigns['cpc'] = (all_campaigns['spend'] / all_campaigns['clicks']).round(2)

    return all_campaigns

# Create consolidated report
campaign_data = import_campaign_data(None)
campaign_data.to_excel('consolidated_campaigns.xlsx', index=False)
```

### 2. Creating Marketing Dashboards

Build executive dashboards with KPIs and performance metrics:

```python
from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from datetime import datetime

def create_marketing_dashboard(campaign_data, output_file):
    """Create an executive marketing dashboard"""

    wb = Workbook()
    ws = wb.active
    ws.title = "Dashboard"

    # Title
    ws['A1'] = 'Marketing Performance Dashboard'
    ws['A1'].font = Font(size=18, bold=True, color='FFFFFF')
    ws['A1'].fill = PatternFill(start_color='2C3E50', end_color='2C3E50', fill_type='solid')
    ws['A1'].alignment = Alignment(horizontal='center')
    ws.merge_cells('A1:F1')

    # Date
    ws['A2'] = f'Generated: {datetime.now().strftime("%Y-%m-%d")}'
    ws['A2'].font = Font(italic=True)

    # KPI Summary Section
    ws['A4'] = 'Key Performance Indicators'
    ws['A4'].font = Font(size=14, bold=True, color='2C3E50')

    kpi_headers = ['Metric', 'This Month', 'Last Month', 'Change', '% Change']
    for col, header in enumerate(kpi_headers, start=1):
        cell = ws.cell(row=5, column=col)
        cell.value = header
        cell.font = Font(bold=True, color='FFFFFF')
        cell.fill = PatternFill(start_color='3498DB', end_color='3498DB', fill_type='solid')
        cell.alignment = Alignment(horizontal='center')

    # KPI Data
    kpis = [
        ['Total Impressions', 2500000, 2100000, '=B6-C6', '=D6/C6'],
        ['Total Clicks', 45000, 38000, '=B7-C7', '=D7/C7'],
        ['Total Conversions', 1200, 950, '=B8-C8', '=D8/C8'],
        ['Total Spend', 125000, 115000, '=B9-C9', '=D9/C9'],
        ['ROAS', 4.2, 3.8, '=B10-C10', '=D10/C10'],
        ['CPA', 104.17, 121.05, '=B11-C11', '=D11/C11'],
    ]

    for row, kpi in enumerate(kpis, start=6):
        ws.cell(row=row, column=1, value=kpi[0])
        ws.cell(row=row, column=2, value=kpi[1])
        ws.cell(row=row, column=3, value=kpi[2])
        ws.cell(row=row, column=4, value=kpi[3])
        ws.cell(row=row, column=5, value=kpi[4])

        # Format numbers
        ws.cell(row=row, column=2).number_format = '#,##0'
        ws.cell(row=row, column=3).number_format = '#,##0'
        ws.cell(row=row, column=4).number_format = '#,##0'
        ws.cell(row=row, column=5).number_format = '0.0%'

    # Campaign Performance by Platform
    ws['A14'] = 'Performance by Platform'
    ws['A14'].font = Font(size=14, bold=True, color='2C3E50')

    platform_headers = ['Platform', 'Impressions', 'Clicks', 'Conversions', 'Spend', 'ROAS']
    for col, header in enumerate(platform_headers, start=1):
        cell = ws.cell(row=15, column=col)
        cell.value = header
        cell.font = Font(bold=True, color='FFFFFF')
        cell.fill = PatternFill(start_color='27AE60', end_color='27AE60', fill_type='solid')
        cell.alignment = Alignment(horizontal='center')

    # Platform data
    platforms = [
        ['Google Ads', 1200000, 28000, 680, 52000, '=E16/D16*100'],
        ['Facebook Ads', 800000, 12000, 350, 35000, '=E17/D17*100'],
        ['LinkedIn Ads', 500000, 5000, 170, 38000, '=E18/D18*100'],
    ]

    for row, platform in enumerate(platforms, start=16):
        for col, value in enumerate(platform, start=1):
            ws.cell(row=row, column=col, value=value)

    # Format platform data
    for row in range(16, 19):
        ws.cell(row=row, column=2).number_format = '#,##0'
        ws.cell(row=row, column=3).number_format = '#,##0'
        ws.cell(row=row, column=4).number_format = '#,##0'
        ws.cell(row=row, column=5).number_format = '$#,##0'
        ws.cell(row=row, column=6).number_format = '0.00'

    # Adjust column widths
    ws.column_dimensions['A'].width = 25
    ws.column_dimensions['B'].width = 15
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 12
    ws.column_dimensions['E'].width = 12
    ws.column_dimensions['F'].width = 12

    wb.save(output_file)

# Create dashboard
create_marketing_dashboard(None, 'marketing_dashboard.xlsx')
```

### 3. Budget Tracking and Pacing

Monitor campaign spend and budget pacing:

```python
import pandas as pd
from datetime import datetime, timedelta

def create_budget_tracker(campaigns_df, monthly_budget):
    """Create budget tracking spreadsheet with pacing alerts"""

    wb = Workbook()
    ws = wb.active
    ws.title = "Budget Tracker"

    # Headers
    headers = ['Campaign', 'Daily Budget', 'Spend Today', 'MTD Spend',
               'Monthly Budget', 'Remaining', 'Days Left', 'Pacing Status']

    for col, header in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True, color='FFFFFF')
        cell.fill = PatternFill(start_color='E74C3C', end_color='E74C3C', fill_type='solid')

    # Calculate days left in month
    today = datetime.now()
    last_day = (today.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    days_left = (last_day - today).days

    # Sample campaign data
    campaigns = [
        ['Google Search', 500, 485, 12500, 15000, '=E2-D2', days_left, '=IF(D2/(30-G2)>B2,"Over Pacing","On Track")'],
        ['Facebook Brand', 350, 365, 8900, 10500, '=E3-D3', days_left, '=IF(D3/(30-G3)>B3,"Over Pacing","On Track")'],
        ['LinkedIn B2B', 200, 195, 5100, 6000, '=E4-D4', days_left, '=IF(D4/(30-G4)>B4,"Over Pacing","On Track")'],
    ]

    for row, campaign in enumerate(campaigns, start=2):
        for col, value in enumerate(campaign, start=1):
            ws.cell(row=row, column=col, value=value)

    # Format currency
    for row in range(2, len(campaigns) + 2):
        for col in [2, 3, 4, 5, 6]:
            ws.cell(row=row, column=col).number_format = '$#,##0.00'

    # Conditional formatting for pacing status
    for row in range(2, len(campaigns) + 2):
        cell = ws.cell(row=row, column=8)
        # Note: Actual conditional formatting would require openpyxl formatting rules

    ws.column_dimensions['A'].width = 20
    for col in ['B', 'C', 'D', 'E', 'F']:
        ws.column_dimensions[col].width = 15

    wb.save('budget_tracker.xlsx')

create_budget_tracker(None, 31500)
```

### 4. A/B Test Analysis

Analyze campaign A/B test results with statistical significance:

```python
import pandas as pd
import numpy as np
from scipy import stats
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

def analyze_ab_test(variant_a, variant_b, output_file):
    """Analyze A/B test results with statistical significance"""

    wb = Workbook()
    ws = wb.active
    ws.title = "AB Test Results"

    # Test data
    ws['A1'] = 'A/B Test Analysis'
    ws['A1'].font = Font(size=16, bold=True)

    headers = ['Variant', 'Impressions', 'Clicks', 'Conversions',
               'CTR %', 'CVR %', 'CPC', 'CPA']

    for col, header in enumerate(headers, start=1):
        cell = ws.cell(row=3, column=col, value=header)
        cell.font = Font(bold=True)
        cell.fill = PatternFill(start_color='D5DBDB', end_color='D5DBDB', fill_type='solid')

    # Variant A
    ws['A4'] = 'Control (A)'
    ws['B4'] = 100000
    ws['C4'] = 2500
    ws['D4'] = 125
    ws['E4'] = '=C4/B4*100'
    ws['F4'] = '=D4/C4*100'
    ws['G4'] = '=IF(C4>0,1000/C4,0)'
    ws['H4'] = '=IF(D4>0,1000/D4,0)'

    # Variant B
    ws['A5'] = 'Test (B)'
    ws['B5'] = 100000
    ws['C5'] = 2800
    ws['D5'] = 156
    ws['E5'] = '=C5/B5*100'
    ws['F5'] = '=D5/C5*100'
    ws['G5'] = '=IF(C5>0,1000/C5,0)'
    ws['H5'] = '=IF(D5>0,1000/D5,0)'

    # Difference
    ws['A6'] = 'Difference'
    ws['A6'].font = Font(bold=True)
    ws['E6'] = '=E5-E4'
    ws['F6'] = '=F5-F4'

    # Statistical significance (simplified)
    ws['A8'] = 'Statistical Analysis'
    ws['A8'].font = Font(size=12, bold=True)

    ws['A9'] = 'Sample Size'
    ws['B9'] = '=B4'
    ws['A10'] = 'Confidence Level'
    ws['B10'] = '95%'
    ws['A11'] = 'Result'

    # Z-test for proportions
    p1 = 2500 / 100000  # Control CTR
    p2 = 2800 / 100000  # Test CTR

    pooled_p = (2500 + 2800) / (100000 + 100000)
    se = np.sqrt(pooled_p * (1 - pooled_p) * (1/100000 + 1/100000))
    z_score = (p2 - p1) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))

    ws['B11'] = 'Significant' if p_value < 0.05 else 'Not Significant'

    # Format numbers
    for row in [4, 5]:
        ws.cell(row=row, column=5).number_format = '0.00%'
        ws.cell(row=row, column=6).number_format = '0.00%'
        ws.cell(row=row, column=7).number_format = '$0.00'
        ws.cell(row=row, column=8).number_format = '$0.00'

    ws.column_dimensions['A'].width = 20
    ws.column_dimensions['B'].width = 12

    wb.save(output_file)

analyze_ab_test(None, None, 'ab_test_analysis.xlsx')
```

### 5. Bulk Upload Preparation

Format data for platform bulk uploads (Google Ads, Facebook Ads):

```python
def prepare_google_ads_upload(campaign_data):
    """Prepare campaign data for Google Ads bulk upload"""

    # Google Ads Editor format
    upload_data = pd.DataFrame({
        'Campaign': campaign_data['campaign_name'],
        'Ad Group': campaign_data['ad_group'],
        'Keyword': campaign_data['keyword'],
        'Match Type': 'Exact',  # or from data
        'Max CPC': campaign_data['bid'],
        'Final URL': campaign_data['landing_page'],
        'Status': 'Enabled'
    })

    # Apply required formatting
    upload_data['Max CPC'] = upload_data['Max CPC'].apply(lambda x: f"{x:.2f}")

    # Save in required format
    upload_data.to_csv('google_ads_upload.csv', index=False)

    return upload_data

def prepare_facebook_ads_upload(campaign_data):
    """Prepare campaign data for Facebook Ads bulk upload"""

    upload_data = pd.DataFrame({
        'Campaign Name': campaign_data['campaign_name'],
        'Ad Set Name': campaign_data['ad_set'],
        'Ad Name': campaign_data['ad_name'],
        'Status': 'ACTIVE',
        'Daily Budget': campaign_data['daily_budget'],
        'Start Date': campaign_data['start_date'],
        'End Date': campaign_data['end_date'],
        'Optimization Goal': 'CONVERSIONS',
        'Bid Strategy': 'LOWEST_COST_WITH_BID_CAP',
        'Bid Amount': campaign_data['bid']
    })

    # Save
    upload_data.to_csv('facebook_ads_upload.csv', index=False)

    return upload_data
```

### 6. Attribution Analysis

Analyze multi-touch attribution data:

```python
def create_attribution_report(touchpoint_data):
    """Create attribution analysis report"""

    wb = Workbook()
    ws = wb.active
    ws.title = "Attribution Analysis"

    # Title
    ws['A1'] = 'Multi-Touch Attribution Report'
    ws['A1'].font = Font(size=16, bold=True)
    ws.merge_cells('A1:E1')

    # Attribution models comparison
    headers = ['Channel', 'First Touch', 'Last Touch', 'Linear', 'Time Decay']

    for col, header in enumerate(headers, start=1):
        cell = ws.cell(row=3, column=col, value=header)
        cell.font = Font(bold=True, color='FFFFFF')
        cell.fill = PatternFill(start_color='8E44AD', end_color='8E44AD', fill_type='solid')

    # Sample attribution data
    channels = [
        ['Paid Search', 120, 85, 95, 98],
        ['Social Media', 45, 92, 78, 82],
        ['Email', 28, 156, 98, 125],
        ['Display', 67, 34, 52, 45],
        ['Direct', 15, 108, 52, 75],
    ]

    for row, channel in enumerate(channels, start=4):
        for col, value in enumerate(channel, start=1):
            ws.cell(row=row, column=col, value=value)

    # Total row
    ws['A9'] = 'Total Conversions'
    ws['A9'].font = Font(bold=True)
    for col in range(2, 6):
        ws.cell(row=9, column=col, value=f'=SUM({chr(64+col)}4:{chr(64+col)}8)')
        ws.cell(row=9, column=col).font = Font(bold=True)

    # Format as numbers
    for row in range(4, 10):
        for col in range(2, 6):
            ws.cell(row=row, column=col).number_format = '#,##0'

    ws.column_dimensions['A'].width = 18
    for col in ['B', 'C', 'D', 'E']:
        ws.column_dimensions[col].width = 14

    wb.save('attribution_analysis.xlsx')

create_attribution_report(None)
```

## Quick Start

### Import Platform Data

```python
import pandas as pd

# Read CSV export from Google Ads
google_data = pd.read_csv('google_ads_export.csv')

# Process and save to Excel
google_data['CTR'] = google_data['Clicks'] / google_data['Impressions']
google_data.to_excel('processed_campaigns.xlsx', index=False)
```

### Create Simple Dashboard

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active

# Add headers
ws['A1'] = 'Campaign'
ws['B1'] = 'Spend'
ws['C1'] = 'Conversions'
ws['D1'] = 'CPA'

# Add data
ws['A2'] = 'Google Search'
ws['B2'] = 5000
ws['C2'] = 125
ws['D2'] = '=B2/C2'

ws['B2'].number_format = '$#,##0'
ws['D2'].number_format = '$#,##0.00'

wb.save('campaign_summary.xlsx')
```

### Read and Analyze Data

```python
import pandas as pd

# Read Excel file
df = pd.read_excel('campaign_data.xlsx')

# Calculate metrics
df['CTR'] = (df['Clicks'] / df['Impressions'] * 100).round(2)
df['ROAS'] = (df['Revenue'] / df['Spend']).round(2)

# Get top performers
top_campaigns = df.nlargest(10, 'ROAS')
print(top_campaigns[['Campaign', 'Spend', 'Revenue', 'ROAS']])
```

## Best Practices

### Data Organization

1. **Use Consistent Column Names**: Standardize across all exports
2. **Date Formatting**: Use YYYY-MM-DD format
3. **Sheet Naming**: Descriptive names (Summary, Raw_Data, Charts)
4. **Data Validation**: Add dropdowns for consistent entries

### Formula Best Practices

1. **Use Cell References**: `=B2/C2` not `=5000/125`
2. **Named Ranges**: Name important ranges for clarity
3. **Error Handling**: `=IFERROR(B2/C2, 0)`
4. **Absolute References**: Use `$` for fixed cells

### Performance Optimization

```python
# For large datasets, use efficient methods
import pandas as pd

# Read only needed columns
df = pd.read_excel('large_file.xlsx', usecols=['Campaign', 'Spend', 'Conversions'])

# Use chunks for very large files
chunk_size = 10000
for chunk in pd.read_excel('huge_file.xlsx', chunksize=chunk_size):
    process_chunk(chunk)
```

## References

### Libraries

- **openpyxl**: Excel file creation and editing
  - [Documentation](https://openpyxl.readthedocs.io/)
  - Supports formulas, formatting, charts

- **pandas**: Data analysis and manipulation
  - [Documentation](https://pandas.pydata.org/)
  - Essential for working with campaign data

- **xlsxwriter**: Alternative for creating Excel files
  - [Documentation](https://xlsxwriter.readthedocs.io/)
  - Good for write-heavy operations

- **scipy**: Statistical analysis
  - [Documentation](https://scipy.org/)
  - For A/B test significance calculations

### Marketing-Specific Tips

1. **Campaign Naming Conventions**: Use consistent formats across platforms
2. **UTM Parameters**: Include in spreadsheets for tracking
3. **Conversion Windows**: Note attribution windows in reports
4. **Currency**: Always specify currency in headers
5. **Time Zones**: Document timezone for date/time fields
6. **Archived Campaigns**: Keep separate sheet for historical data
7. **Version Control**: Date-stamp files (report_2024-01-15.xlsx)

### Common Formulas for Marketing

```excel
# CTR (Click-Through Rate)
=Clicks/Impressions*100

# CPC (Cost Per Click)
=Spend/Clicks

# CPA (Cost Per Acquisition)
=Spend/Conversions

# ROAS (Return on Ad Spend)
=Revenue/Spend

# Conversion Rate
=Conversions/Clicks*100

# CPM (Cost Per Thousand Impressions)
=Spend/Impressions*1000
```
