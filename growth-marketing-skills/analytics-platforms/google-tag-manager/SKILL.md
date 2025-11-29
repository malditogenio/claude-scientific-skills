---
name: google-tag-manager
description: "Tag management system. Deploy tracking tags, event tracking, dataLayer management, trigger configuration, GA4/Facebook Pixel integration."
---

# Google Tag Manager

## Overview

Google Tag Manager (GTM) is a tag management system that allows you to deploy and manage marketing tags (tracking codes) on your website or app without modifying code. This skill covers GTM API usage, dataLayer configuration, event tracking setup, and automated tag management.

## When to Use This Skill

- Managing marketing and analytics tags without code deployments
- Implementing event tracking for GA4, Facebook, Google Ads
- Setting up conversion tracking pixels
- Managing dataLayer for enhanced analytics
- A/B testing and personalization integration
- Debugging tracking implementations
- Automated tag container management

## Core Capabilities

### 1. GTM API Setup

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
import json

class GTMAnalytics:
    def __init__(self, service_account_file):
        self.credentials = service_account.Credentials.from_service_account_file(
            service_account_file,
            scopes=['https://www.googleapis.com/auth/tagmanager.readonly']
        )
        self.service = build('tagmanager', 'v2', credentials=self.credentials)

    def list_accounts(self):
        """List all GTM accounts"""
        accounts = self.service.accounts().list().execute()
        return accounts.get('account', [])

    def list_containers(self, account_id):
        """List containers in an account"""
        containers = self.service.accounts().containers().list(
            parent=f'accounts/{account_id}'
        ).execute()
        return containers.get('container', [])

    def get_container(self, path):
        """Get container details"""
        container = self.service.accounts().containers().get(
            path=path
        ).execute()
        return container

    def list_tags(self, workspace_path):
        """List all tags in workspace"""
        tags = self.service.accounts().containers().workspaces().tags().list(
            parent=workspace_path
        ).execute()
        return tags.get('tag', [])

    def list_triggers(self, workspace_path):
        """List all triggers in workspace"""
        triggers = self.service.accounts().containers().workspaces().triggers().list(
            parent=workspace_path
        ).execute()
        return triggers.get('trigger', [])

    def list_variables(self, workspace_path):
        """List all variables in workspace"""
        variables = self.service.accounts().containers().workspaces().variables().list(
            parent=workspace_path
        ).execute()
        return variables.get('variable', [])

# Initialize GTM API
gtm = GTMAnalytics(service_account_file='service-account.json')

# List accounts
accounts = gtm.list_accounts()
print(f"GTM Accounts: {len(accounts)}")

for account in accounts:
    print(f"  {account['name']} (ID: {account['accountId']})")

# List containers
if accounts:
    account_id = accounts[0]['accountId']
    containers = gtm.list_containers(account_id)

    for container in containers:
        print(f"  Container: {container['name']} ({container['publicId']})")
```

### 2. DataLayer Configuration

```python
def generate_datalayer_code(event_name, event_params):
    """
    Generate dataLayer push code for events
    """
    datalayer_code = f"""
// Push event to dataLayer
window.dataLayer = window.dataLayer || [];
dataLayer.push({{
    'event': '{event_name}',
    {', '.join([f"'{k}': '{v}'" for k, v in event_params.items()])}
}});
"""

    return datalayer_code

# E-commerce purchase event
purchase_code = generate_datalayer_code(
    event_name='purchase',
    event_params={
        'transaction_id': 'T12345',
        'value': 99.99,
        'currency': 'USD',
        'items': '[{name: "Product A", price: 99.99}]'
    }
)

print("Purchase Event Code:")
print(purchase_code)

# Marketing event examples
def create_marketing_events():
    """Common marketing event dataLayer examples"""
    events = {
        'form_submit': {
            'event': 'form_submission',
            'form_name': 'contact_form',
            'form_type': 'lead_generation'
        },
        'button_click': {
            'event': 'cta_click',
            'button_text': 'Start Free Trial',
            'button_location': 'hero_section'
        },
        'video_play': {
            'event': 'video_interaction',
            'video_title': 'Product Demo',
            'video_duration': 120,
            'video_percent': 0
        },
        'page_view': {
            'event': 'pageview',
            'page_path': window.location.pathname,
            'page_title': document.title,
            'user_type': 'logged_in'  # or 'anonymous'
        }
    }

    print("\nMarketing Event Examples:")
    for event_name, event_data in events.items():
        print(f"\n{event_name}:")
        print(f"dataLayer.push({json.dumps(event_data, indent=2)})")

    return events

marketing_events = create_marketing_events()
```

### 3. Tag Configuration Examples

```python
def create_ga4_event_tag(gtm, workspace_path, tag_name, event_name,
                        trigger_name, measurement_id):
    """
    Create GA4 event tag programmatically
    """
    tag_data = {
        'name': tag_name,
        'type': 'gaawc',  # GA4 Event tag
        'parameter': [
            {
                'type': 'template',
                'key': 'measurementId',
                'value': measurement_id
            },
            {
                'type': 'template',
                'key': 'eventName',
                'value': event_name
            }
        ],
        'firingTriggerId': [trigger_name],
        'tagFiringOption': 'oncePerEvent'
    }

    # Note: This requires write permissions
    # tag = gtm.service.accounts().containers().workspaces().tags().create(
    #     parent=workspace_path,
    #     body=tag_data
    # ).execute()

    print(f"GA4 Event Tag Configuration:")
    print(json.dumps(tag_data, indent=2))

    return tag_data

# Create purchase tracking tag
# ga4_purchase_tag = create_ga4_event_tag(
#     gtm,
#     workspace_path='accounts/123/containers/456/workspaces/789',
#     tag_name='GA4 - Purchase Event',
#     event_name='purchase',
#     trigger_name='purchase_trigger_id',
#     measurement_id='G-XXXXXXXXXX'
# )

def create_facebook_pixel_tag(pixel_id, event_name):
    """Facebook Pixel event tag configuration"""
    tag_config = {
        'name': f'Facebook - {event_name}',
        'type': 'html',
        'parameter': [
            {
                'type': 'template',
                'key': 'html',
                'value': f"""
<script>
fbq('track', '{event_name}', {{
    value: {{{{Event Value}}}},
    currency: 'USD',
    content_type: 'product'
}});
</script>
                """
            }
        ]
    }

    print(f"Facebook Pixel Tag for {event_name}:")
    print(json.dumps(tag_config, indent=2))

    return tag_config

# Facebook conversion tracking
fb_purchase = create_facebook_pixel_tag('PIXEL_ID', 'Purchase')
```

### 4. Trigger Configuration

```python
def analyze_triggers(gtm, workspace_path):
    """
    Analyze all triggers in workspace
    """
    triggers = gtm.list_triggers(workspace_path)

    trigger_data = []
    for trigger in triggers:
        trigger_data.append({
            'name': trigger.get('name'),
            'type': trigger.get('type'),
            'filter': trigger.get('filter', [])
        })

    triggers_df = pd.DataFrame(trigger_data)

    print("\nTrigger Analysis:")
    print(f"Total triggers: {len(triggers_df)}")
    print("\nTrigger Types:")
    print(triggers_df['type'].value_counts())

    return triggers_df

# Analyze triggers
# triggers_df = analyze_triggers(
#     gtm,
#     workspace_path='accounts/123/containers/456/workspaces/789'
# )

def create_trigger_examples():
    """Common trigger configurations"""
    triggers = {
        'page_view': {
            'name': 'All Pages',
            'type': 'pageview',
            'filter': []
        },
        'button_click': {
            'name': 'CTA Button Click',
            'type': 'click',
            'filter': [
                {
                    'type': 'cssSelector',
                    'parameter': [
                        {'key': 'selector', 'value': '.cta-button'}
                    ]
                }
            ]
        },
        'form_submit': {
            'name': 'Contact Form Submit',
            'type': 'formSubmission',
            'filter': [
                {
                    'type': 'cssSelector',
                    'parameter': [
                        {'key': 'selector', 'value': '#contact-form'}
                    ]
                }
            ]
        },
        'scroll_depth': {
            'name': '50% Scroll Depth',
            'type': 'scrollDepth',
            'filter': [
                {
                    'type': 'scrollDepthThreshold',
                    'parameter': [
                        {'key': 'threshold', 'value': '50'}
                    ]
                }
            ]
        },
        'custom_event': {
            'name': 'Purchase Complete',
            'type': 'customEvent',
            'filter': [
                {
                    'type': 'eventName',
                    'parameter': [
                        {'key': 'eventName', 'value': 'purchase'}
                    ]
                }
            ]
        }
    }

    print("\nCommon Trigger Configurations:")
    for name, config in triggers.items():
        print(f"\n{name}:")
        print(json.dumps(config, indent=2))

    return triggers

trigger_examples = create_trigger_examples()
```

### 5. Variable Configuration

```python
def analyze_variables(gtm, workspace_path):
    """
    Analyze all variables in workspace
    """
    variables = gtm.list_variables(workspace_path)

    var_data = []
    for var in variables:
        var_data.append({
            'name': var.get('name'),
            'type': var.get('type'),
            'format': var.get('formatValue', {}).get('convertUndefinedToNull')
        })

    vars_df = pd.DataFrame(var_data)

    print("\nVariable Analysis:")
    print(f"Total variables: {len(vars_df)}")
    print("\nVariable Types:")
    print(vars_df['type'].value_counts())

    return vars_df

# Analyze variables
# vars_df = analyze_variables(
#     gtm,
#     workspace_path='accounts/123/containers/456/workspaces/789'
# )

def create_variable_examples():
    """Common variable configurations"""
    variables = {
        'datalayer_variable': {
            'name': 'DL - Event Value',
            'type': 'dataLayer',
            'parameter': [
                {'key': 'dataLayerVersion', 'value': '2'},
                {'key': 'name', 'value': 'event_value'}
            ]
        },
        'javascript_variable': {
            'name': 'JS - User ID',
            'type': 'jsm',
            'parameter': [
                {'key': 'javascript', 'value': 'function() { return window.userId; }'}
            ]
        },
        'url_variable': {
            'name': 'URL - Path',
            'type': 'url',
            'parameter': [
                {'key': 'component', 'value': 'PATH'}
            ]
        },
        'custom_javascript': {
            'name': 'CJS - Product Category',
            'type': 'jsm',
            'parameter': [
                {
                    'key': 'javascript',
                    'value': '''
                    function() {
                        return document.querySelector('[data-category]')?.dataset.category || 'unknown';
                    }
                    '''
                }
            ]
        },
        'regex_table': {
            'name': 'Regex - Channel Grouping',
            'type': 'smm',  # Regex table
            'parameter': [
                {
                    'key': 'input',
                    'value': '{{Page URL}}'
                },
                {
                    'key': 'map',
                    'list': [
                        {'map': [
                            {'key': 'input', 'value': '.*utm_source=google.*'},
                            {'key': 'output', 'value': 'Google'}
                        ]},
                        {'map': [
                            {'key': 'input', 'value': '.*utm_source=facebook.*'},
                            {'key': 'output', 'value': 'Facebook'}
                        ]}
                    ]
                }
            ]
        }
    }

    print("\nCommon Variable Configurations:")
    for name, config in variables.items():
        print(f"\n{name}:")
        print(json.dumps(config, indent=2))

    return variables

variable_examples = create_variable_examples()
```

### 6. Container Version Management

```python
def list_container_versions(gtm, container_path):
    """List all published versions"""
    versions = gtm.service.accounts().containers().versions().list(
        parent=container_path
    ).execute()

    version_data = []
    for version in versions.get('containerVersion', []):
        version_data.append({
            'version_id': version.get('containerVersionId'),
            'name': version.get('name'),
            'description': version.get('description'),
            'fingerprint': version.get('fingerprint')
        })

    versions_df = pd.DataFrame(version_data)

    print("\nContainer Versions:")
    print(versions_df)

    return versions_df

def export_container_version(gtm, version_path, filename):
    """
    Export container version to JSON
    """
    version = gtm.service.accounts().containers().versions().get(
        path=version_path
    ).execute()

    # Save to file
    with open(filename, 'w') as f:
        json.dump(version, f, indent=2)

    print(f"Container version exported to {filename}")

    # Analyze contents
    print(f"\nContainer Contents:")
    print(f"  Tags: {len(version.get('tag', []))}")
    print(f"  Triggers: {len(version.get('trigger', []))}")
    print(f"  Variables: {len(version.get('variable', []))}")

    return version

# Export current container
# container_version = export_container_version(
#     gtm,
#     version_path='accounts/123/containers/456/versions/789',
#     filename='gtm_container_backup.json'
# )
```

### 7. Preview and Debug Mode

```python
def generate_debug_script():
    """
    Generate JavaScript for GTM debugging
    """
    debug_script = """
// GTM Debug Helper
(function() {
    // Log all dataLayer pushes
    var originalPush = window.dataLayer.push;
    window.dataLayer.push = function() {
        console.log('dataLayer.push:', arguments);
        return originalPush.apply(window.dataLayer, arguments);
    };

    // Monitor GTM events
    window.addEventListener('gtm.js', function(event) {
        console.log('GTM Event:', event);
    });

    // Check if GTM is loaded
    if (window.google_tag_manager) {
        console.log('GTM Loaded:', Object.keys(window.google_tag_manager));
    }

    // Helper to view current dataLayer
    window.viewDataLayer = function() {
        console.table(window.dataLayer);
    };

    console.log('GTM Debug Mode Active');
    console.log('Use viewDataLayer() to see current state');
})();
"""

    print("GTM Debug Script:")
    print(debug_script)

    return debug_script

debug_script = generate_debug_script()
```

### 8. Tag Testing and Validation

```python
def validate_tag_implementation(expected_events):
    """
    Generate validation checklist for tag implementation
    """
    validation_script = """
// Tag Implementation Validation
const validationResults = {
    gtmLoaded: !!window.google_tag_manager,
    dataLayerExists: !!window.dataLayer,
    events: {}
};

// Check for expected events in dataLayer
const expectedEvents = %s;

expectedEvents.forEach(eventName => {
    const found = window.dataLayer.some(item =>
        item.event === eventName
    );
    validationResults.events[eventName] = found;
});

console.log('Validation Results:', validationResults);
""" % json.dumps(expected_events)

    print("Tag Validation Script:")
    print(validation_script)

    return validation_script

# Validate e-commerce implementation
validation = validate_tag_implementation([
    'view_item',
    'add_to_cart',
    'begin_checkout',
    'purchase'
])

def create_qa_checklist():
    """QA checklist for GTM implementation"""
    checklist = {
        'Setup': [
            'GTM container installed on all pages',
            'dataLayer initialized before GTM snippet',
            'GTM container ID matches configuration'
        ],
        'Tags': [
            'GA4 config tag fires on all pages',
            'Conversion tags fire on correct events',
            'All tags have appropriate triggers',
            'No duplicate tags firing'
        ],
        'Triggers': [
            'Custom events defined in dataLayer',
            'Form submit triggers configured',
            'Click triggers use proper selectors',
            'Trigger conditions are specific enough'
        ],
        'Variables': [
            'DataLayer variables defined for all events',
            'Custom JavaScript variables tested',
            'URL variables configured correctly',
            'User-defined variables have fallbacks'
        ],
        'Testing': [
            'Preview mode tested all scenarios',
            'Tag Assistant shows tags firing',
            'No JavaScript errors in console',
            'Events appear in GA4 DebugView'
        ]
    }

    print("\nGTM QA Checklist:")
    for category, items in checklist.items():
        print(f"\n{category}:")
        for item in items:
            print(f"  [ ] {item}")

    return checklist

qa_checklist = create_qa_checklist()
```

## Installation

```bash
uv pip install google-api-python-client google-auth pandas
```

GTM Container Snippet (add to website):

```html
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-XXXXXX');</script>
<!-- End Google Tag Manager -->

<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-XXXXXX"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
```

## Authentication

1. Create a service account in Google Cloud Console
2. Enable the Tag Manager API
3. Grant the service account access to your GTM containers
4. Download the service account JSON key

## Quick Start

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Authenticate
credentials = service_account.Credentials.from_service_account_file(
    'service-account.json',
    scopes=['https://www.googleapis.com/auth/tagmanager.readonly']
)

service = build('tagmanager', 'v2', credentials=credentials)

# List accounts
accounts = service.accounts().list().execute()
print(f"GTM Accounts: {accounts}")

# List containers
if accounts.get('account'):
    account_id = accounts['account'][0]['accountId']
    containers = service.accounts().containers().list(
        parent=f'accounts/{account_id}'
    ).execute()
    print(f"Containers: {containers}")
```

## Key Features

- **Tag Management**: Deploy tags without code changes
- **DataLayer**: Structured data collection
- **Triggers**: Event-based tag firing
- **Variables**: Dynamic values and conditions
- **Version Control**: Container versioning and rollback
- **Preview Mode**: Test before publishing
- **Built-in Templates**: GA4, Google Ads, Facebook Pixel

## References

- [Google Tag Manager API](https://developers.google.com/tag-platform/tag-manager/api/v2)
- [DataLayer Documentation](https://developers.google.com/tag-platform/tag-manager/datalayer)
- [GTM Templates](https://developers.google.com/tag-platform/tag-manager/templates)
- [Tag Manager Best Practices](https://developers.google.com/tag-platform/tag-manager/best-practices)
