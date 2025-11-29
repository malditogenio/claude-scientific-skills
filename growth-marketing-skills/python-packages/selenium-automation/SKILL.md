---
name: selenium-automation
description: "Browser automation for marketing tasks. Automated testing, form submission, screenshot capture, dynamic content scraping, social media automation, ad verification."
---

# Selenium for Marketing Automation

## Overview

Selenium enables browser automation for marketing tasks that require JavaScript rendering or user interactions. This skill covers automating repetitive marketing tasks, testing landing pages, capturing screenshots, scraping dynamic content, verifying ad placements, and automating social media workflows.

## When to Use This Skill

- Testing landing pages and conversion funnels
- Automating form submissions and lead generation
- Capturing screenshots of ad placements and campaigns
- Scraping JavaScript-heavy websites (SPAs)
- Automating social media posting and engagement
- Verifying ad placements across different devices
- Monitoring competitor dynamic content
- A/B testing screenshot comparison

## Core Capabilities

### 1. Landing Page Testing and Screenshots

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import os

class LandingPageTester:
    """
    Automated landing page testing and screenshot capture
    """
    def __init__(self, headless=True):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size(1920, 1080)

    def test_page_load(self, url, timeout=10):
        """
        Test page load time and capture metrics
        """
        start_time = datetime.now()
        self.driver.get(url)

        # Wait for page to load
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        load_time = (datetime.now() - start_time).total_seconds()

        return {
            'url': url,
            'load_time': load_time,
            'page_title': self.driver.title,
            'current_url': self.driver.current_url,
            'timestamp': datetime.now()
        }

    def capture_screenshot(self, url, filename=None, full_page=True):
        """
        Capture screenshot of landing page
        """
        self.driver.get(url)

        # Wait for page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"screenshot_{timestamp}.png"

        if full_page:
            # Capture full page
            original_size = self.driver.get_window_size()
            required_width = self.driver.execute_script('return document.body.parentNode.scrollWidth')
            required_height = self.driver.execute_script('return document.body.parentNode.scrollHeight')
            self.driver.set_window_size(required_width, required_height)

        self.driver.save_screenshot(filename)

        print(f"Screenshot saved: {filename}")
        return filename

    def test_conversion_funnel(self, funnel_steps):
        """
        Test complete conversion funnel
        """
        results = []

        for step in funnel_steps:
            try:
                # Navigate to page
                self.driver.get(step['url'])

                # Wait for key element
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, step['key_element']))
                )

                # Check for conversion element
                conversion_element = self.driver.find_element(By.CSS_SELECTOR, step['conversion_element'])
                element_visible = conversion_element.is_displayed()

                results.append({
                    'step': step['name'],
                    'url': step['url'],
                    'status': 'passed' if element_visible else 'failed',
                    'timestamp': datetime.now()
                })

                # Capture screenshot
                self.capture_screenshot(step['url'], f"{step['name']}.png")

            except Exception as e:
                results.append({
                    'step': step['name'],
                    'url': step['url'],
                    'status': 'error',
                    'error': str(e),
                    'timestamp': datetime.now()
                })

        return results

    def close(self):
        self.driver.quit()

# Usage
tester = LandingPageTester(headless=True)

# Test page load
metrics = tester.test_page_load('https://yourlandingpage.com')
print(f"Page load time: {metrics['load_time']:.2f}s")

# Capture screenshots at different viewports
viewports = {
    'desktop': (1920, 1080),
    'tablet': (768, 1024),
    'mobile': (375, 667)
}

for device, (width, height) in viewports.items():
    tester.driver.set_window_size(width, height)
    tester.capture_screenshot('https://yourlandingpage.com', f'landing_{device}.png')

# Test funnel
funnel = [
    {'name': 'homepage', 'url': 'https://example.com', 'key_element': 'h1', 'conversion_element': '.cta-button'},
    {'name': 'signup', 'url': 'https://example.com/signup', 'key_element': 'form', 'conversion_element': '#submit'},
]

results = tester.test_conversion_funnel(funnel)
tester.close()
```

### 2. Form Automation and Lead Generation

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

class FormAutomation:
    """
    Automate form submissions for lead generation testing
    """
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)

    def fill_and_submit_form(self, form_data):
        """
        Fill out and submit a form
        """
        url = form_data['url']
        self.driver.get(url)

        # Wait for form to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "form"))
        )

        # Fill text inputs
        for field in form_data.get('text_fields', []):
            element = self.driver.find_element(By.CSS_SELECTOR, field['selector'])
            element.clear()
            element.send_keys(field['value'])

        # Fill email
        if 'email' in form_data:
            email_elem = self.driver.find_element(By.CSS_SELECTOR, form_data['email']['selector'])
            email_elem.send_keys(form_data['email']['value'])

        # Select dropdowns
        for dropdown in form_data.get('dropdowns', []):
            select = Select(self.driver.find_element(By.CSS_SELECTOR, dropdown['selector']))
            select.select_by_visible_text(dropdown['value'])

        # Checkboxes
        for checkbox in form_data.get('checkboxes', []):
            elem = self.driver.find_element(By.CSS_SELECTOR, checkbox['selector'])
            if checkbox['checked'] and not elem.is_selected():
                elem.click()

        # Submit form
        submit_button = self.driver.find_element(By.CSS_SELECTOR, form_data['submit_button'])
        submit_button.click()

        # Wait for confirmation
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, form_data['confirmation_selector']))
            )
            return {'status': 'success', 'message': 'Form submitted successfully'}
        except:
            return {'status': 'failed', 'message': 'Confirmation not found'}

    def test_form_validation(self, url, test_cases):
        """
        Test form validation with various inputs
        """
        results = []

        for test_case in test_cases:
            self.driver.get(url)

            # Try to submit with test data
            result = self.fill_and_submit_form({
                'url': url,
                **test_case
            })

            results.append({
                'test_name': test_case['name'],
                'expected': test_case['expected_result'],
                'actual': result['status'],
                'passed': result['status'] == test_case['expected_result']
            })

        return pd.DataFrame(results)

    def close(self):
        self.driver.quit()

# Usage
automation = FormAutomation()

# Submit a lead form
form_data = {
    'url': 'https://example.com/contact',
    'text_fields': [
        {'selector': '#name', 'value': 'John Doe'},
        {'selector': '#company', 'value': 'Acme Corp'}
    ],
    'email': {'selector': '#email', 'value': 'john@example.com'},
    'dropdowns': [
        {'selector': '#industry', 'value': 'Technology'}
    ],
    'checkboxes': [
        {'selector': '#newsletter', 'checked': True}
    ],
    'submit_button': '#submit',
    'confirmation_selector': '.success-message'
}

result = automation.fill_and_submit_form(form_data)
print(result)

automation.close()
```

### 3. Dynamic Content Scraping

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

class DynamicContentScraper:
    """
    Scrape JavaScript-rendered content
    """
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome(options=options)

    def scrape_infinite_scroll(self, url, scroll_pause=2, max_scrolls=10):
        """
        Scrape content from infinite scroll pages
        """
        self.driver.get(url)

        # Wait for initial content to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scrolls = 0

        while scrolls < max_scrolls:
            # Scroll to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait for new content to load
            time.sleep(scroll_pause)

            # Calculate new scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height
            scrolls += 1

        # Parse loaded content
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        return soup

    def scrape_ajax_content(self, url, wait_selector, timeout=10):
        """
        Wait for AJAX content to load before scraping
        """
        self.driver.get(url)

        # Wait for specific element that indicates AJAX load complete
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, wait_selector))
        )

        # Additional wait for any animations
        time.sleep(1)

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        return soup

    def scrape_social_media_posts(self, profile_url, post_selector, max_posts=50):
        """
        Scrape social media posts with dynamic loading
        """
        soup = self.scrape_infinite_scroll(profile_url, scroll_pause=2, max_scrolls=10)

        posts = []
        post_elements = soup.select(post_selector)[:max_posts]

        for post in post_elements:
            # Extract post data (adjust selectors based on platform)
            text_elem = post.select_one('.post-text')
            likes_elem = post.select_one('.likes-count')
            date_elem = post.select_one('.post-date')

            posts.append({
                'text': text_elem.text.strip() if text_elem else '',
                'likes': likes_elem.text.strip() if likes_elem else '0',
                'date': date_elem.text.strip() if date_elem else ''
            })

        return pd.DataFrame(posts)

    def close(self):
        self.driver.quit()

# Usage
scraper = DynamicContentScraper()

# Scrape infinite scroll content
soup = scraper.scrape_infinite_scroll('https://example.com/feed')
articles = soup.find_all('article', class_='post')
print(f"Found {len(articles)} articles")

scraper.close()
```

### 4. Ad Verification and Monitoring

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class AdVerification:
    """
    Verify ad placements and capture screenshots
    """
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome(options=options)

    def verify_ad_placement(self, url, ad_selectors):
        """
        Verify ads are displaying correctly
        """
        self.driver.get(url)
        time.sleep(3)  # Wait for ads to load

        results = []

        for ad_name, selector in ad_selectors.items():
            try:
                ad_element = self.driver.find_element(By.CSS_SELECTOR, selector)

                results.append({
                    'ad_name': ad_name,
                    'present': True,
                    'visible': ad_element.is_displayed(),
                    'location': ad_element.location,
                    'size': ad_element.size
                })

                # Screenshot the ad
                ad_element.screenshot(f"{ad_name}_screenshot.png")

            except Exception as e:
                results.append({
                    'ad_name': ad_name,
                    'present': False,
                    'visible': False,
                    'error': str(e)
                })

        return pd.DataFrame(results)

    def check_ad_across_devices(self, url, ad_selector):
        """
        Check ad rendering across different device sizes
        """
        devices = {
            'desktop': (1920, 1080),
            'tablet': (768, 1024),
            'mobile': (375, 667)
        }

        results = []

        for device_name, (width, height) in devices.items():
            self.driver.set_window_size(width, height)
            self.driver.get(url)
            time.sleep(2)

            try:
                ad = self.driver.find_element(By.CSS_SELECTOR, ad_selector)
                visible = ad.is_displayed()

                # Capture screenshot
                self.driver.save_screenshot(f"ad_{device_name}.png")

                results.append({
                    'device': device_name,
                    'resolution': f"{width}x{height}",
                    'ad_visible': visible,
                    'ad_size': ad.size if visible else None
                })

            except Exception as e:
                results.append({
                    'device': device_name,
                    'resolution': f"{width}x{height}",
                    'ad_visible': False,
                    'error': str(e)
                })

        return pd.DataFrame(results)

    def close(self):
        self.driver.quit()

# Usage
verifier = AdVerification()

# Verify multiple ad placements
ad_selectors = {
    'header_banner': '#header-ad',
    'sidebar_ad': '.sidebar-ad',
    'inline_ad': '.inline-ad'
}

results = verifier.verify_ad_placement('https://yoursite.com', ad_selectors)
print(results)

# Check responsive ads
responsive_check = verifier.check_ad_across_devices('https://yoursite.com', '#responsive-ad')
print(responsive_check)

verifier.close()
```

### 5. Competitor Page Monitoring

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
import hashlib
from datetime import datetime
import json

class CompetitorMonitor:
    """
    Monitor competitor pages for changes
    """
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)

    def capture_page_state(self, url, key_selectors):
        """
        Capture current state of competitor page
        """
        self.driver.get(url)
        time.sleep(3)

        page_state = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'page_title': self.driver.title,
            'elements': {}
        }

        for element_name, selector in key_selectors.items():
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                text = element.text.strip()
                html = element.get_attribute('outerHTML')

                page_state['elements'][element_name] = {
                    'text': text,
                    'html_hash': hashlib.md5(html.encode()).hexdigest(),
                    'present': True
                }
            except:
                page_state['elements'][element_name] = {
                    'present': False
                }

        # Screenshot
        screenshot_file = f"competitor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        self.driver.save_screenshot(screenshot_file)
        page_state['screenshot'] = screenshot_file

        return page_state

    def detect_changes(self, current_state, previous_state):
        """
        Detect changes between page states
        """
        changes = []

        for element_name in current_state['elements']:
            curr = current_state['elements'][element_name]
            prev = previous_state['elements'].get(element_name, {})

            if not prev:
                changes.append({
                    'element': element_name,
                    'change_type': 'new_element'
                })
            elif curr.get('html_hash') != prev.get('html_hash'):
                changes.append({
                    'element': element_name,
                    'change_type': 'content_modified',
                    'old_text': prev.get('text', ''),
                    'new_text': curr.get('text', '')
                })

        return changes

    def close(self):
        self.driver.quit()

# Usage
monitor = CompetitorMonitor()

key_elements = {
    'pricing': '.pricing-section',
    'hero_cta': '.hero-cta',
    'features': '.features-list'
}

# Capture current state
current = monitor.capture_page_state('https://competitor.com', key_elements)

# Save state
with open('competitor_state.json', 'w') as f:
    json.dump(current, f, indent=2)

monitor.close()
```

### 6. Social Media Automation

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class SocialMediaAutomation:
    """
    Automate social media tasks (use responsibly!)
    """
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome(options=options)

    def login(self, platform, username, password):
        """
        Login to social media platform
        """
        if platform == 'twitter':
            self.driver.get('https://twitter.com/login')
            time.sleep(2)

            username_field = self.driver.find_element(By.NAME, 'text')
            username_field.send_keys(username)
            username_field.send_keys(Keys.RETURN)
            time.sleep(2)

            password_field = self.driver.find_element(By.NAME, 'password')
            password_field.send_keys(password)
            password_field.send_keys(Keys.RETURN)
            time.sleep(3)

    def schedule_post(self, platform, content, media_path=None):
        """
        Create a social media post
        """
        # Platform-specific implementation
        pass

    def close(self):
        self.driver.quit()
```

## Installation

```bash
# Install Selenium
uv pip install selenium pandas beautifulsoup4

# Install ChromeDriver (or use webdriver-manager)
uv pip install webdriver-manager

# Alternative: Auto-manage drivers
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
```

## Quick Start

```python
from selenium import webdriver

# Create browser instance
driver = webdriver.Chrome()

# Navigate to page
driver.get('https://example.com')

# Find element and interact
button = driver.find_element(By.ID, 'submit-button')
button.click()

# Close browser
driver.quit()
```

## Best Practices

1. **Use headless mode** - Faster and uses less resources
2. **Explicit waits** - Use WebDriverWait instead of time.sleep()
3. **Handle exceptions** - Always wrap in try/except blocks
4. **Clean up resources** - Always call driver.quit()
5. **Anti-detection** - Remove automation indicators for scraping
6. **Respect rate limits** - Add appropriate delays between actions
7. **Screenshots for debugging** - Capture screenshots on errors

## References

- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Selenium Python Bindings](https://selenium-python.readthedocs.io/)
- [WebDriver Manager](https://github.com/SergeyPirogov/webdriver_manager)
