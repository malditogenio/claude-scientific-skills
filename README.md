# Claude Growth Marketing Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.md)
[![Skills](https://img.shields.io/badge/Skills-117+-brightgreen.svg)](#whats-included)

A comprehensive collection of **117+ ready-to-use growth marketing skills** for Claude. Transform Claude into your AI marketing assistant capable of executing complex multi-step marketing workflows across analytics, automation, advertising, and data-driven optimization.

These skills enable Claude to seamlessly work with specialized marketing platforms, analytics tools, and data systems across multiple marketing domains:
- 📊 **Analytics & Tracking** - Google Analytics, Mixpanel, Amplitude, Heap, PostHog, behavior analysis, conversion tracking
- 📧 **Marketing Automation** - HubSpot, Klaviyo, Mailchimp, Braze, Iterable, email campaigns, customer journeys
- 📱 **Advertising Platforms** - Meta Ads, Google Ads, TikTok Ads, LinkedIn Ads, programmatic advertising, ROAS optimization
- 🛒 **E-commerce & Payments** - Shopify, Stripe, WooCommerce, subscription management, revenue optimization
- 🗄️ **CDP & Data Infrastructure** - Segment, mParticle, Snowflake, BigQuery, data pipelines, reverse ETL
- 💼 **CRM & Sales** - Salesforce, Pipedrive, Apollo.io, lead scoring, sales intelligence
- 🔬 **Analysis & Experimentation** - A/B testing, cohort analysis, attribution modeling, churn prediction, LTV optimization
- ✍️ **Content & Strategy** - Copywriting, SEO, content strategy, conversion rate optimization, growth experimentation
- 📱 **Social Media** - Social listening, scheduling, community management, influencer marketing
- 🐍 **Python Analytics** - pandas, scikit-learn, Prophet forecasting, sentiment analysis, marketing ML

**Transform Claude Code into your AI Growth Marketing Expert!**

> ⭐ **If you find this repository useful**, please consider giving it a star! It helps others discover these tools and encourages us to continue maintaining and expanding this collection.

---

## 📦 What's Included

This repository provides **117+ growth marketing skills** organized into the following categories:

- **15 Python Analytics Packages** - pandas, plotly, scikit-learn, Prophet, lifetimes CLV, and more
- **13 Analytics Platforms** - Google Analytics, Mixpanel, Amplitude, Heap, PostHog, Looker, Tableau
- **14 Marketing Automation Tools** - HubSpot, Mailchimp, Klaviyo, Braze, Intercom, and more
- **12 Advertising Platforms** - Meta Ads, Google Ads, TikTok Ads, LinkedIn Ads, programmatic DSP
- **10 E-commerce & Payments** - Shopify, Stripe, WooCommerce, subscription management
- **12 CDP & Data Tools** - Segment, mParticle, Snowflake, BigQuery, Fivetran, Hightouch
- **9 CRM & Sales Tools** - Salesforce, Pipedrive, Apollo.io, Gong, ZoomInfo, Clearbit
- **12 Analysis Methods** - A/B testing, cohort analysis, attribution, churn prediction, LTV
- **10 Communication & Strategy** - Copywriting, SEO, CRO, product-led growth, referral programs
- **7 Social Media Tools** - Buffer, Hootsuite, Sprout Social, social listening
- **4 Document Skills** - PDF, Excel, PowerPoint, CSV data processing

Each skill includes:
- ✅ Comprehensive documentation (`SKILL.md`)
- ✅ Practical code examples
- ✅ Use cases and best practices
- ✅ Integration guides
- ✅ Reference materials

---

## 📋 Table of Contents

- [What's Included](#whats-included)
- [Why Use This?](#why-use-this)
- [Getting Started](#getting-started)
  - [Claude Code](#claude-code-recommended)
  - [Cursor IDE](#cursor-ide)
  - [Any MCP Client](#any-mcp-client)
- [Prerequisites](#prerequisites)
- [Quick Examples](#quick-examples)
- [Use Cases](#use-cases)
- [Available Skills](#available-skills)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Support](#support)
- [License](#license)

---

## 🚀 Why Use This?

### ⚡ **Accelerate Your Marketing**
- **Save Days of Work** - Skip API documentation research and integration setup
- **Production-Ready Code** - Tested, validated examples following marketing best practices
- **Multi-Step Workflows** - Execute complex marketing pipelines with a single prompt

### 🎯 **Comprehensive Coverage**
- **117+ Skills** - Extensive coverage across all major marketing domains
- **15+ Analytics Platforms** - Direct access to Google Analytics, Mixpanel, Amplitude, and more
- **12+ Advertising Platforms** - Meta Ads, Google Ads, TikTok Ads, programmatic DSP

### 🔧 **Easy Integration**
- **One-Click Setup** - Install via Claude Code or MCP server
- **Automatic Discovery** - Claude automatically finds and uses relevant skills
- **Well Documented** - Each skill includes examples, use cases, and best practices

### 🌟 **Data-Driven Marketing**
- **Advanced Analytics** - Cohort analysis, attribution modeling, predictive models
- **ML-Powered Insights** - Churn prediction, LTV optimization, customer segmentation
- **Experimentation Framework** - A/B testing, growth experiments, statistical significance

---

## 🎯 Getting Started

Choose your preferred platform to get started:

### 🖥️ Claude Code (Recommended)

> 📚 **New to Claude Code?** Check out the [Claude Code Quickstart Guide](https://docs.claude.com/en/docs/claude-code/quickstart) to get started.

**Step 1: Install Claude Code**

**macOS:**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows:**
```powershell
irm https://claude.ai/install.ps1 | iex
```

**Step 2: Register the Marketplace**

```bash
/plugin marketplace add your-org/claude-growth-marketing-skills
```

**Step 3: Install Skills**

1. Open Claude Code
2. Select **Browse and install plugins**
3. Choose **claude-growth-marketing-skills**
4. Select **growth-marketing-skills**
5. Click **Install now**

**That's it!** Claude will automatically use the appropriate skills when you describe your marketing tasks. Make sure to keep the skill up to date!

---

### ⌨️ Cursor IDE

One-click installation via our hosted MCP server (coming soon).

---

### 🔌 Any MCP Client

Access all skills via MCP server in any MCP-compatible client (ChatGPT, Google ADK, OpenAI Agent SDK, etc.).

---

## ⚙️ Prerequisites

- **Python**: 3.9+ (3.12+ recommended for best compatibility)
- **uv**: Python package manager (required for installing skill dependencies)
- **Client**: Claude Code, Cursor, or any MCP-compatible client
- **System**: macOS, Linux, or Windows with WSL2
- **Dependencies**: Automatically handled by individual skills (check `SKILL.md` files for specific requirements)

### Installing uv

The skills use `uv` as the package manager for installing Python dependencies. Install it using the instructions for your operating system:

**macOS and Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Alternative (via pip):**
```bash
pip install uv
```

After installation, verify it works by running:
```bash
uv --version
```

---

## 💡 Quick Examples

Once you've installed the skills, you can ask Claude to execute complex multi-step marketing workflows. Here are some example prompts:

### 📊 Full-Funnel Analytics Pipeline
**Goal**: Analyze complete customer journey from acquisition to retention

**Prompt**:
```
Use available skills. Pull data from Google Analytics for traffic sources,
Mixpanel for user behavior events, and Stripe for revenue. Create cohort
analysis for last 6 months, calculate LTV by acquisition channel, identify
drop-off points in the funnel, and build a dashboard with key metrics.
```

**Skills Used**: Google Analytics, Mixpanel, Stripe, Cohort Analysis, LTV Analysis, Funnel Analysis, Plotly Dashboards

---

### 🎯 Campaign Performance Optimization
**Goal**: Optimize ad spend across multiple channels

**Prompt**:
```
Use available skills. Pull campaign data from Meta Ads and Google Ads for
the last 30 days. Analyze ROAS by campaign, audience, and creative. Build
attribution model to understand cross-channel effects. Identify
underperforming segments, calculate optimal budget allocation, and create
recommendations report.
```

**Skills Used**: Meta Ads, Google Ads, Attribution Modeling, statsmodels, Pandas Analytics, Scientific Writing

---

### 🔮 Churn Prediction & Prevention
**Goal**: Identify at-risk customers and create retention campaigns

**Prompt**:
```
Use available skills. Extract customer behavior data from Amplitude,
purchase history from Shopify, and support tickets from Intercom. Build
churn prediction model with scikit-learn, segment high-risk customers,
create personalized retention email flows in Klaviyo, and set up
automated alerts.
```

**Skills Used**: Amplitude, Shopify, Intercom, Churn Prediction, Customer Segmentation, Klaviyo, scikit-learn

---

### 📧 Email Marketing Optimization
**Goal**: Improve email performance through data-driven optimization

**Prompt**:
```
Use available skills. Analyze email campaign data from Mailchimp - open
rates, click rates, conversions by segment and send time. Run sentiment
analysis on subject lines, identify winning patterns, create A/B test
plan for next campaigns, and generate optimized subject line variations.
```

**Skills Used**: Mailchimp, A/B Testing, NLTK Sentiment, Copywriting, Email Marketing

---

### 🛒 E-commerce Revenue Optimization
**Goal**: Increase AOV and conversion rate

**Prompt**:
```
Use available skills. Pull transaction data from Shopify, analyze with
market basket analysis to find product affinities. Calculate price
elasticity, identify upsell opportunities, create customer segments by
RFM, and design personalized recommendation strategy. Generate report
with implementation roadmap.
```

**Skills Used**: Shopify, Market Basket Analysis, Pricing Optimization, Customer Segmentation, RFM Analysis, Pandas Analytics

---

### 📈 Growth Experimentation Framework
**Goal**: Set up systematic experimentation process

**Prompt**:
```
Use available skills. Design A/B testing framework for landing pages
using statistical best practices. Set up tracking with Google Tag Manager,
create experiment documentation template, calculate required sample sizes,
define success metrics, and build automated significance calculator.
```

**Skills Used**: A/B Testing, Google Tag Manager, Growth Experimentation, statsmodels, Conversion Rate Optimization

---

### 🔗 Customer Data Platform Setup
**Goal**: Unify customer data across all touchpoints

**Prompt**:
```
Use available skills. Design Segment implementation to collect events
from web and mobile. Set up identity resolution, create data model for
BigQuery warehouse, configure Hightouch for reverse ETL to ad platforms,
and document data governance policies.
```

**Skills Used**: Segment, BigQuery, Hightouch, Customer Segmentation, Data Architecture

---

> 📖 **Want more examples?** Check out [docs/examples.md](docs/examples.md) for comprehensive workflow examples and detailed use cases across all marketing domains.

---

## 🔬 Use Cases

### 📊 Analytics & Insights
- **Customer Journey Analysis**: Map complete user paths from first touch to conversion
- **Cohort Analysis**: Track retention and LTV by acquisition cohort
- **Funnel Optimization**: Identify and fix conversion bottlenecks
- **Attribution Modeling**: Understand cross-channel marketing impact
- **Predictive Analytics**: Forecast revenue, churn, and growth trends

### 📱 Advertising & Acquisition
- **Campaign Management**: Optimize campaigns across Meta, Google, TikTok, and more
- **Budget Allocation**: Data-driven spend optimization across channels
- **Audience Building**: Create lookalikes and custom audiences from CDP data
- **Creative Analysis**: Identify winning ad creative patterns
- **ROAS Optimization**: Maximize return on ad spend

### 📧 Marketing Automation
- **Email Campaigns**: Design and optimize email marketing flows
- **Customer Journeys**: Build automated lifecycle campaigns
- **Lead Nurturing**: Create sequences that convert leads to customers
- **Personalization**: Deliver targeted content based on behavior
- **Trigger Campaigns**: Set up event-based automated messaging

### 🛒 E-commerce & Revenue
- **Revenue Analytics**: Track and optimize key commerce metrics
- **Subscription Management**: Reduce churn and increase expansion
- **Pricing Strategy**: Test and optimize pricing models
- **Product Recommendations**: Build data-driven recommendation engines
- **Customer Support**: Analyze support data for product insights

### 🔬 Experimentation & Testing
- **A/B Testing**: Design and analyze experiments with statistical rigor
- **Feature Flags**: Roll out features with controlled experiments
- **Multivariate Testing**: Test multiple variables simultaneously
- **Sample Size Calculation**: Ensure experiments have statistical power
- **Sequential Testing**: Enable early stopping with valid inference

### 🗄️ Data Infrastructure
- **Event Tracking**: Implement comprehensive tracking plans
- **Data Warehousing**: Set up modern data stack architecture
- **Reverse ETL**: Sync audiences to ad platforms and tools
- **Data Quality**: Monitor and maintain data accuracy
- **Privacy Compliance**: Implement GDPR/CCPA compliant data practices

---

## 📚 Available Skills

This repository contains **117+ growth marketing skills** organized across multiple domains. Each skill provides comprehensive documentation, code examples, and best practices.

### Skill Categories

#### 🐍 **Python Analytics Packages** (15 skills)
- Data manipulation: pandas, Polars
- Visualization: Plotly, Streamlit dashboards
- Machine learning: scikit-learn, statsmodels
- Forecasting: Prophet, PyMC Bayesian
- Customer analytics: lifetimes (CLV), NetworkX (viral analysis)
- NLP: NLTK sentiment, spaCy
- Automation: Selenium, BeautifulSoup, requests
- Data transforms: dbt

#### 📊 **Analytics Platforms** (13 skills)
- Product analytics: Mixpanel, Amplitude, Heap, PostHog
- Web analytics: Google Analytics, Google Search Console
- Session replay: Hotjar, FullStory
- BI tools: Looker, Tableau, Metabase
- Tag management: Google Tag Manager
- Competitive intel: SimilarWeb

#### 📧 **Marketing Automation** (14 skills)
- All-in-one: HubSpot, Marketo, Pardot, ActiveCampaign
- Email: Mailchimp, SendGrid
- E-commerce focused: Klaviyo
- Mobile & cross-channel: Braze, Iterable, Customer.io
- Conversational: Intercom, Drift
- Workflow automation: Zapier, Make (Integromat)

#### 📱 **Advertising Platforms** (12 skills)
- Social: Meta Ads, TikTok Ads, Twitter Ads, Pinterest Ads, Snapchat Ads
- Search: Google Ads, Apple Search Ads
- Professional: LinkedIn Ads
- E-commerce: Amazon Ads
- Programmatic: DSP platforms, Criteo
- Native: Taboola, Outbrain

#### 🛒 **E-commerce & Payments** (10 skills)
- Platforms: Shopify, WooCommerce, Magento, BigCommerce
- Payments: Stripe, PayPal, Square
- Subscriptions: Recharge
- Support: Gorgias
- Reviews: Yotpo

#### 🗄️ **CDP & Data Infrastructure** (12 skills)
- CDPs: Segment, mParticle, RudderStack
- Warehouses: Snowflake, BigQuery, Redshift, Databricks
- ETL/ELT: Fivetran, Airbyte, Stitch
- Reverse ETL: Census, Hightouch

#### 💼 **CRM & Sales** (9 skills)
- CRM: Salesforce, Pipedrive, Close CRM
- Sales engagement: Apollo.io, Outreach, SalesLoft
- Conversation intelligence: Gong
- Enrichment: Clearbit, ZoomInfo

#### 🔬 **Analysis Methods** (12 skills)
- Experimentation: A/B testing, growth experimentation
- Customer analytics: Cohort analysis, churn prediction, customer segmentation
- Revenue: LTV analysis, CAC optimization, pricing optimization
- Behavior: Funnel analysis, retention analysis, market basket analysis
- Growth: Viral coefficient, attribution modeling

#### ✍️ **Communication & Strategy** (10 skills)
- Content: Copywriting, content strategy, SEO optimization
- Conversion: Landing page optimization, CRO
- Growth: Growth experimentation, product-led growth, referral programs
- Channels: Email marketing, influencer marketing

#### 📱 **Social Media** (7 skills)
- Management: Buffer, Hootsuite, Sprout Social, Later
- Monitoring: Brandwatch, Mention
- Strategy: Social listening

#### 📄 **Document Skills** (4 skills)
- PDF processing
- Excel/XLSX analysis
- PowerPoint/PPTX creation
- CSV data handling

> 📖 **For complete details on all skills**, see [docs/growth-marketing-skills.md](docs/growth-marketing-skills.md)

> 💡 **Looking for practical examples?** Check out [docs/examples.md](docs/examples.md) for comprehensive workflow examples across all marketing domains.

---

## 🤝 Contributing

We welcome contributions to expand and improve this growth marketing skills repository!

### Ways to Contribute

✨ **Add New Skills**
- Create skills for additional marketing platforms or tools
- Add integrations for emerging marketing technologies

📚 **Improve Existing Skills**
- Enhance documentation with more examples and use cases
- Add new workflows and reference materials
- Improve code examples and scripts
- Fix bugs or update outdated information

🐛 **Report Issues**
- Submit bug reports with detailed reproduction steps
- Suggest improvements or new features

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-skill`)
3. **Follow** the existing directory structure and documentation patterns
4. **Ensure** all new skills include comprehensive `SKILL.md` files
5. **Test** your examples and workflows thoroughly
6. **Commit** your changes (`git commit -m 'Add amazing skill'`)
7. **Push** to your branch (`git push origin feature/amazing-skill`)
8. **Submit** a pull request with a clear description of your changes

### Contribution Guidelines

✅ Maintain consistency with existing skill documentation format
✅ Include practical, working examples in all contributions
✅ Ensure all code examples are tested and functional
✅ Follow marketing best practices in examples and workflows
✅ Update relevant documentation when adding new capabilities
✅ Provide clear comments and docstrings in code
✅ Include references to official documentation

---

## 🔧 Troubleshooting

### Common Issues

**Problem: Skills not loading in Claude Code**
- Solution: Ensure you've installed the latest version of Claude Code
- Try reinstalling the plugin

**Problem: Missing Python dependencies**
- Solution: Check the specific `SKILL.md` file for required packages
- Install dependencies: `uv pip install package-name`

**Problem: API rate limits**
- Solution: Many platforms have rate limits. Review the specific platform documentation
- Consider implementing caching or batch requests

**Problem: Authentication errors**
- Solution: Some services require API keys. Check the `SKILL.md` for authentication setup
- Verify your credentials and permissions

**Problem: Outdated examples**
- Solution: Report the issue via GitHub Issues
- Check the official platform documentation for updated syntax

---

## ❓ FAQ

### General Questions

**Q: Is this free to use?**
A: Yes! This project is MIT licensed, allowing free use for any purpose including commercial projects.

**Q: Why are all skills grouped into one plugin?**
A: Modern growth marketing is inherently cross-functional. Bundling all skills makes it easy to combine analytics, advertising, automation, and data infrastructure in unified workflows.

**Q: Can I use this for commercial projects?**
A: Absolutely! The MIT License allows both commercial and noncommercial use without restrictions.

**Q: How often is this updated?**
A: We regularly update skills to reflect the latest versions of platforms and APIs. Major updates are announced in release notes.

### Installation & Setup

**Q: Do I need all the Python packages installed?**
A: No! Only install the packages you need. Each skill specifies its requirements in its `SKILL.md` file.

**Q: What if a skill doesn't work?**
A: First check the [Troubleshooting](#troubleshooting) section. If the issue persists, file an issue on GitHub with detailed reproduction steps.

**Q: Do the skills work offline?**
A: Platform skills require internet access to query APIs. Python package skills work offline once dependencies are installed.

### Contributing

**Q: Can I contribute my own skills?**
A: Absolutely! We welcome contributions. See the [Contributing](#contributing) section for guidelines and best practices.

**Q: How do I report bugs or suggest features?**
A: Open an issue on GitHub with a clear description. For bugs, include reproduction steps and expected vs actual behavior.

---

## 💬 Support

Need help? Here's how to get support:

- 📖 **Documentation**: Check the relevant `SKILL.md` and `references/` folders
- 🐛 **Bug Reports**: Open an issue on GitHub
- 💡 **Feature Requests**: Submit a feature request via GitHub Issues

---

## 📄 License

This project is licensed under the **MIT License**.

### Key Points:
- ✅ **Free for any use** (commercial and noncommercial)
- ✅ **Open source** - modify, distribute, and use freely
- ✅ **Permissive** - minimal restrictions on reuse
- ⚠️ **No warranty** - provided "as is" without warranty of any kind

See [LICENSE.md](LICENSE.md) for full terms.
