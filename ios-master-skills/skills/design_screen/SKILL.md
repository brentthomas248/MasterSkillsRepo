---
name: Design SwiftUI Screen
description: Converts a user prompt into a HIG-compliant wireframe specification before implementation.
---

# Protocol: UI Wireframing

## Context

Before starting, **read these files immediately**:
1. `../../knowledge/ios_hig/typography.md` — Understand semantic text styles and Dynamic Type.
2. `../../knowledge/ios_hig/layout.md` — Understand touch targets, safe areas, and spacing.
3. `../../knowledge/ios_hig/colors.md` — Understand semantic color usage.
4. `../../knowledge/templates/FEATURE_SPEC.md` — Use this standard format when interpreting user requirements.

## Objective

Transform a high-level user request (e.g., "Create a login screen") into a **structured design specification** that can be handed off to the implementation skill.

**Critical Rule:** DO NOT write SwiftUI code in this skill. This skill outputs a JSON specification only.

## Steps

### 1. Semantic Analysis

Break down the user's request into functional requirements.

**Example Request:** "Design a login screen"

**Analysis:**
- **Inputs**: Email field, password field
- **Actions**: Login button, forgot password link
- **Feedback**: Loading indicator, error message display
- **Navigation**: Link to sign-up screen

### 2. Constraint Check

Verify the design meets HIG requirements by checking the knowledge base:

#### Typography Check
- **Body text**: Are we using `.body` (17pt) as the base?
- **Headlines**: Are section titles using `.headline` (17pt semibold)?
- **Text fields**: Are inputs at least `.body` size?

**Reference:** `../../knowledge/ios_hig/typography.md`

#### Layout Check
- **Touch targets**: Are all buttons at least 44x44 pt?
- **Spacing**: Are we using semantic tokens (`.md`, `.lg`) instead of hardcoded values?
- **Safe areas**: Is the keyboard-aware layout respecting the bottom safe area?

**Reference:** `../../knowledge/ios_hig/layout.md`

#### Color Check
- **Semantic colors**: Are we using `.primary`, `.secondary`, `.systemBackground`?
- **Contrast**: Will text have 4.5:1 contrast in both Light and Dark modes?

**Reference:** `../../knowledge/ios_hig/colors.md`

### 3. Generate Specification

Output a **JSON block** defining the screen hierarchy with constraints.

**Template:**
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
      "type": "TextField",
      "label": "Email",
      "binding": "email",
      "constraints": [
        "font: .body",
        "minHeight: 44pt",
        "autocapitalization: none",
        "keyboardType: .emailAddress"
      ],
      "accessibility": "label: 'Email address input field'"
    },
    {
      "type": "SecureField",
      "label": "Password",
      "binding": "password",
      "constraints": [
        "font: .body",
        "minHeight: 44pt"
      ],
      "accessibility": "label: 'Password input field'"
    },
    {
      "type": "PrimaryButton",
      "label": "Sign In",
      "action": "viewModel.login()",
      "constraints": [
        "minHeight: 50pt",
        "frame: .infinity (full width)",
        "disabled: !viewModel.isValid"
      ],
      "accessibility": "label: 'Sign in button', hint: 'Double tap to sign in'"
    },
    {
      "type": "Button",
      "label": "Forgot Password?",
      "action": "viewModel.showForgotPassword()",
      "constraints": [
        "font: .callout",
        "foregroundColor: .blue",
        "minHeight: 44pt"
      ],
      "accessibility": "label: 'Forgot password button'"
    }
  ],
  "viewModel": {
    "name": "LoginViewModel",
    "state": {
      "cases": ["idle", "loading", "success", "error(String)"]
    },
    "properties": [
      "email: String",
      "password: String",
      "isValid: Bool (computed)"
    ],
    "methods": [
      "login() async",
      "showForgotPassword()"
    ]
  },
  "navigation": {
    "backButton": true,
    "navigationTitle": "Sign In"
  },
  "alerts": [
    {
      "trigger": "viewModel.state == .error",
      "title": "Error",
      "message": "viewModel.errorMessage",
      "actions": ["OK (dismiss)"]
    }
  ]
}
```

### 4. Validate Against HIG

Before outputting, perform a self-check:

**Validation Checklist:**
- [ ] All buttons have `minHeight: 44pt` (or 50pt for primary actions).
- [ ] Text styles use semantic names (`.body`, `.headline`), not hardcoded sizes.
- [ ] Spacing uses tokens (`.md`, `.lg`), not numeric values.
- [ ] Colors use semantic names (`.primary`, `.blue`), not RGB values.
- [ ] All interactive elements have accessibility labels.
- [ ] ViewModel has a `State` enum defined.

If any check fails, add a **warning** to the output:

```json
{
  "warnings": [
    "Button 'Forgot Password' is using a hardcoded color. Consider using .secondary or .tint()."
  ]
}
```

### 5. Output Format

Present the specification to the user in a code block with clear formatting:

```
## Screen Design: [ScreenName]

**Feature:** [FeatureName]
**Complexity:** [Simple/Medium/Complex]

### Visual Hierarchy
[JSON specification from step 3]

### HIG Compliance
✅ Touch targets: All interactive elements meet 44pt minimum
✅ Typography: Using Dynamic Type-compatible styles
✅ Colors: Using semantic system colors
⚠️  Warnings: [List any warnings from step 4]

### Next Steps
Use the "Implement Component" skill to generate SwiftUI code from this specification.
```

## Examples

### Example 1: Simple Profile Screen

**User Request:** "Design a profile screen showing user name, email, and a logout button"

**Output:**
```json
{
  "screenName": "ProfileView",
  "feature": "Profile",
  "layout": {
    "type": "VStack",
    "spacing": ".xl",
    "alignment": "center"
  },
  "components": [
    {
      "type": "AsyncImage",
      "binding": "viewModel.user.avatarURL",
      "constraints": [
        "frame: 100x100",
        "cornerRadius: 50",
        "placeholder: Image(systemName: 'person.circle.fill')"
      ],
      "accessibility": "label: 'Profile picture'"
    },
    {
      "type": "Text",
      "content": "viewModel.user.displayName",
      "constraints": [
        "font: .title",
        "foregroundColor: .primary"
      ]
    },
    {
      "type": "Text",
      "content": "viewModel.user.email",
      "constraints": [
        "font: .callout",
        "foregroundColor: .secondary"
      ]
    },
    {
      "type": "Button",
      "label": "Sign Out",
      "action": "viewModel.logout()",
      "constraints": [
        "font: .headline",
        "foregroundColor: .red",
        "minHeight: 50pt",
        "frame: .infinity"
      ]
    }
  ],
  "viewModel": {
    "name": "ProfileViewModel",
    "state": {
      "cases": ["idle", "loading", "loggedOut"]
    },
    "properties": [
      "user: User"
    ],
    "methods": [
      "logout() async"
    ]
  }
}
```

### Example 2: Complex Dashboard Screen

**User Request:** "Design a dashboard with user stats, recent activity list, and quick action buttons"

**Output:**
```json
{
  "screenName": "DashboardView",
  "feature": "Dashboard",
  "layout": {
    "type": "ScrollView",
    "content": "VStack with spacing: .lg"
  },
  "components": [
    {
      "type": "HStack (Stats Cards)",
      "children": [
        {
          "type": "StatCard",
          "title": "Total Views",
          "value": "viewModel.totalViews",
          "icon": "eye.fill"
        },
        {
          "type": "StatCard",
          "title": "Followers",
          "value": "viewModel.followersCount",
          "icon": "person.2.fill"
        }
      ],
      "constraints": [
        "spacing: .md",
        "height: 100pt"
      ]
    },
    {
      "type": "VStack (Quick Actions)",
      "children": [
        {
          "type": "PrimaryButton",
          "label": "New Post",
          "action": "viewModel.createPost()"
        },
        {
          "type": "SecondaryButton",
          "label": "View Analytics",
          "action": "viewModel.showAnalytics()"
        }
      ],
      "constraints": [
        "spacing: .sm"
      ]
    },
    {
      "type": "List (Recent Activity)",
      "binding": "viewModel.recentActivity",
      "rowContent": {
        "type": "ActivityRow",
        "title": "activity.title",
        "timestamp": "activity.createdAt",
        "icon": "activity.icon"
      },
      "constraints": [
        "listStyle: .plain",
        "minRowHeight: 60pt"
      ]
    }
  ],
  "viewModel": {
    "name": "DashboardViewModel",
    "state": {
      "cases": ["idle", "loading", "content", "error(String)"]
    },
    "properties": [
      "totalViews: Int",
      "followersCount: Int",
      "recentActivity: [Activity]"
    ],
    "methods": [
      "loadDashboard() async",
      "createPost()",
      "showAnalytics()"
    ]
  }
}
```

## Prompt Templates

Reference template file for common screen patterns:
`./prompt_templates/wireframe_gen.md`

## Self-Correction Checklist

Before outputting, verify:
- [ ] All text styles use semantic names (not font sizes).
- [ ] All spacing uses tokens (not numeric values).
- [ ] All colors use semantic names (not hex/RGB).
- [ ] All interactive elements meet 44pt minimum touch target.
- [ ] ViewModel includes a `State` enum.
- [ ] Accessibility labels are provided for all interactive elements.

## Common Pitfalls

❌ **DON'T:**
- Write SwiftUI code in this skill (that's the implementation skill's job).
- Use hardcoded values in the specification (always use tokens/semantic names).
- Skip the constraint check step.

✅ **DO:**
- Output a clear JSON specification.
- Reference the HIG knowledge files for validation.
- Include warnings if the design might violate HIG.
- Provide clear next steps for the user.
