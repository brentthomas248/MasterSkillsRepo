# Wireframe Generation Prompt Templates

This file contains reusable templates for common screen patterns.

## Login Screen Template

```json
{
  "screenName": "LoginView",
  "feature": "Authentication",
  "layout": {
    "type": "VStack",
    "spacing": ".lg",
    "alignment": "center"
  },
  "components": [
    {
      "type": "Image (Logo)",
      "systemName": "lock.shield.fill",
      "constraints": [
        "size: 80pt",
        "foregroundColor: .blue"
      ]
    },
    {
      "type": "TextField",
      "label": "Email",
      "binding": "email",
      "constraints": [
        "font: .body",
        "minHeight: 44pt",
        "autocapitalization: none",
        "keyboardType: .emailAddress"
      ]
    },
    {
      "type": "SecureField",
      "label": "Password",
      "binding": "password",
      "constraints": [
        "font: .body",
        "minHeight: 44pt"
      ]
    },
    {
      "type": "PrimaryButton",
      "label": "Sign In",
      "action": "viewModel.login()",
      "constraints": [
        "minHeight: 50pt",
        "disabled: !viewModel.isValid"
      ]
    },
    {
      "type": "Button (Secondary)",
      "label": "Forgot Password?",
      "action": "viewModel.showForgotPassword()",
      "constraints": [
        "font: .callout",
        "foregroundColor: .blue"
      ]
    }
  ],
  "viewModel": {
    "state": ["idle", "loading", "success", "error(String)"],
    "properties": ["email: String", "password: String", "isValid: Bool"],
    "methods": ["login() async", "showForgotPassword()"]
  }
}
```

## List/Feed Screen Template

```json
{
  "screenName": "[Feature]ListView",
  "feature": "[FeatureName]",
  "layout": {
    "type": "NavigationStack with List"
  },
  "components": [
    {
      "type": "List",
      "binding": "viewModel.items",
      "rowContent": {
        "type": "HStack",
        "children": [
          {
            "type": "AsyncImage",
            "binding": "item.imageURL",
            "constraints": ["size: 60x60", "cornerRadius: 8"]
          },
          {
            "type": "VStack (alignment: .leading)",
            "children": [
              {
                "type": "Text",
                "content": "item.title",
                "constraints": ["font: .headline"]
              },
              {
                "type": "Text",
                "content": "item.subtitle",
                "constraints": ["font: .subheadline", "foregroundColor: .secondary"]
              }
            ]
          }
        ],
        "constraints": [
          "spacing: .md",
          "minHeight: 76pt"
        ]
      },
      "navigation": {
        "destination": "[Detail]View(item: item)"
      }
    }
  ],
  "viewModel": {
    "state": ["idle", "loading", "content", "error(String)"],
    "properties": ["items: [Item]"],
    "methods": ["loadItems() async", "refreshItems() async"]
  },
  "toolbar": {
    "trailingItems": [
      {
        "type": "Button",
        "label": "Add",
        "systemImage": "plus",
        "action": "viewModel.addItem()"
      }
    ]
  }
}
```

## Detail Screen Template

```json
{
  "screenName": "[Feature]DetailView",
  "feature": "[FeatureName]",
  "layout": {
    "type": "ScrollView with VStack"
  },
  "components": [
    {
      "type": "AsyncImage (Hero)",
      "binding": "item.imageURL",
      "constraints": [
        "aspectRatio: 16:9",
        "maxHeight: 300pt"
      ]
    },
    {
      "type": "VStack (Content Section)",
      "spacing": ".md",
      "children": [
        {
          "type": "Text (Title)",
          "content": "item.title",
          "constraints": ["font: .title", "fontWeight: .bold"]
        },
        {
          "type": "Text (Subtitle)",
          "content": "item.subtitle",
          "constraints": ["font: .callout", "foregroundColor: .secondary"]
        },
        {
          "type": "Divider"
        },
        {
          "type": "Text (Body)",
          "content": "item.description",
          "constraints": ["font: .body", "lineSpacing: 4"]
        }
      ]
    }
  ],
  "viewModel": {
    "state": ["loading", "content", "error(String)"],
    "properties": ["item: Item"],
    "methods": ["loadDetails() async"]
  },
  "toolbar": {
    "trailingItems": [
      {
        "type": "Button",
        "label": "Share",
        "systemImage": "square.and.arrow.up",
        "action": "viewModel.share()"
      }
    ]
  }
}
```

## Form/Settings Screen Template

```json
{
  "screenName": "[Feature]FormView",
  "feature": "[FeatureName]",
  "layout": {
    "type": "Form"
  },
  "sections": [
    {
      "header": "Personal Information",
      "components": [
        {
          "type": "TextField",
          "label": "Full Name",
          "binding": "viewModel.fullName",
          "constraints": ["font: .body"]
        },
        {
          "type": "TextField",
          "label": "Email",
          "binding": "viewModel.email",
          "constraints": ["keyboardType: .emailAddress"]
        }
      ]
    },
    {
      "header": "Preferences",
      "components": [
        {
          "type": "Toggle",
          "label": "Enable Notifications",
          "binding": "viewModel.notificationsEnabled"
        },
        {
          "type": "Picker",
          "label": "Theme",
          "binding": "viewModel.selectedTheme",
          "options": ["Light", "Dark", "System"]
        }
      ]
    },
    {
      "components": [
        {
          "type": "Button",
          "label": "Save Changes",
          "action": "viewModel.save()",
          "constraints": ["disabled: !viewModel.hasChanges"]
        }
      ]
    }
  ],
  "viewModel": {
    "state": ["idle", "saving", "saved", "error(String)"],
    "properties": [
      "fullName: String",
      "email: String",
      "notificationsEnabled: Bool",
      "selectedTheme: String",
      "hasChanges: Bool"
    ],
    "methods": ["save() async"]
  }
}
```

## Empty State Template

```json
{
  "screenName": "[Feature]EmptyStateView",
  "feature": "[FeatureName]",
  "layout": {
    "type": "VStack",
    "spacing": ".lg",
    "alignment": "center"
  },
  "components": [
    {
      "type": "Image",
      "systemName": "tray.fill",
      "constraints": [
        "size: 80pt",
        "foregroundColor: .secondary"
      ]
    },
    {
      "type": "Text (Title)",
      "content": "No Items Yet",
      "constraints": ["font: .title2", "fontWeight: .semibold"]
    },
    {
      "type": "Text (Description)",
      "content": "Get started by adding your first item",
      "constraints": [
        "font: .body",
        "foregroundColor: .secondary",
        "multilineTextAlignment: .center"
      ]
    },
    {
      "type": "PrimaryButton",
      "label": "Add Item",
      "action": "viewModel.addItem()",
      "constraints": ["minHeight: 50pt"]
    }
  ]
}
```

## Usage Instructions

1. **Select Template**: Choose the template that best matches the screen type.
2. **Customize**: Replace `[Feature]`, `[FeatureName]`, and placeholder content with actual values.
3. **Validate**: Run the specification through the HIG constraint checks.
4. **Output**: Present the customized JSON to the user.

## Adding New Templates

When you encounter a new common pattern, document it here following this format:

1. **Template Name**: Clear, descriptive name
2. **Use Case**: When to use this template
3. **JSON Structure**: Complete specification
4. **Notes**: Any specific considerations or variations
