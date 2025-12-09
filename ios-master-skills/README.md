# iOS Master Skills Repository

A comprehensive skill library that transforms AI agents into Senior iOS Architects. This repository contains structured knowledge, protocols, and tools for building production-grade SwiftUI applications that strictly adhere to Apple Human Interface Guidelines.

## Overview

This repository follows the "Master Repo Architecture" pattern - a centralized knowledge base that can be linked to any iOS project via Google Antigravity's extension system.

### Key Components

1. **Knowledge Base** (`knowledge/`) - Design laws and architectural standards
2. **Skills** (`skills/`) - Step-by-step protocols for common iOS development tasks
3. **Tools** (`tools/`) - MCP servers and utilities for code analysis

## Structure

```
ios-master-skills/
├── gemini-extension.json          # Manifest (registers with Antigravity)
├── GEMINI.md                      # Router (skill lookup table)
├── knowledge/                     # Static Knowledge Base
│   ├── ios_hig/                   # Apple HIG Guidelines
│   │   ├── layout.md              # Touch targets, safe areas, spacing
│   │   ├── typography.md          # Dynamic Type, semantic styles
│   │   └── colors.md              # Semantic color palettes
│   └── swiftui/                   # SwiftUI Architecture
│       ├── golden_path.md         # Project structure, MVVM patterns
│       └── swiftlint_rules.yml    # Code quality standards
├── skills/                        # Active Capabilities
│   ├── scaffold_new_app/          # Project initialization
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── init_project.sh
│   ├── design_screen/             # UI wireframing
│   │   ├── SKILL.md
│   │   └── prompt_templates/
│   │       └── wireframe_gen.md
│   └── implement_component/       # SwiftUI code generation
│       ├── SKILL.md
│       └── reference/
│           └── button_styles.md
└── tools/                         # Utilities
    └── swift_syntax_analyzer.py   # HIG compliance checker
```

## Setup & Installation

### Prerequisites

- Python 3.7+ (for the Swift analyzer tool)
- Google Antigravity CLI installed
- An iOS project (or the intent to create one)

### Installation Steps

#### Option 1: Link to Existing Project (Recommended)

This method allows live updates - any changes you make to the Master Repo will instantly reflect in all linked projects.

```bash
# Navigate to your iOS project directory
cd ~/MyIosProject

# Link the Master Skills Repo as an extension
gemini extensions link ~/path/to/ios-master-skills

# Verify the link
gemini extensions list
```

#### Option 2: Install as Extension

This creates a static copy in the project.

```bash
cd ~/MyIosProject
gemini extensions install ~/path/to/ios-master-skills
```

### Verification

Open Google Antigravity in your project and ask:

```
List the skills available in the iOS Master Architect extension.
```

The agent should respond with the routing table showing:
- Scaffold New App
- Design Screen
- Implement Component

## Usage

### Skill Activation

The agent automatically routes your requests to the appropriate skill based on intent:

| Your Request | Triggered Skill |
|--------------|----------------|
| "Start a new app", "Init project" | `scaffold_new_app` |
| "Design a screen", "Plan UI" | `design_screen` |
| "Build a button", "Implement view" | `implement_component` |

### Example Workflows

#### 1. Start a New iOS App

```
You: "Initialize a new iOS app called 'TaskMaster' with Authentication and Dashboard features"
```

The agent will:
1. Load `skills/scaffold_new_app/SKILL.md`
2. Run the initialization script
3. Create the Golden Path folder structure
4. Install SwiftLint configuration
5. Scaffold the requested features

#### 2. Design a Screen

```
You: "Design a login screen with email, password, and a sign-in button"
```

The agent will:
1. Load `skills/design_screen/SKILL.md`
2. Reference HIG guidelines (typography, layout, colors)
3. Output a structured JSON specification
4. Validate against HIG constraints

#### 3. Implement a Component

```
You: "Implement the login screen we just designed"
```

The agent will:
1. Load `skills/implement_component/SKILL.md`
2. Generate production SwiftUI code
3. Create the View and ViewModel files
4. Apply HIG-compliant modifiers
5. Add accessibility labels

## Knowledge Base Reference

### iOS Human Interface Guidelines

#### Layout (`knowledge/ios_hig/layout.md`)
- **Touch Targets**: Minimum 44x44pt for all interactive elements
- **Safe Areas**: Bottom 34pt reserved for Home Indicator
- **Spacing System**: 8pt grid (4, 8, 12, 16, 24, 32, 48)
- **Thumb Zone**: Place primary actions in lower 50% of screen

#### Typography (`knowledge/ios_hig/typography.md`)
- **Semantic Styles**: `.body`, `.headline`, `.title`, etc.
- **Dynamic Type**: All text scales with accessibility settings
- **Contrast**: Minimum 4.5:1 for body text (17pt)

#### Colors (`knowledge/ios_hig/colors.md`)
- **Semantic Colors**: `.primary`, `.secondary`, `.systemBackground`
- **Dark Mode**: All colors automatically adapt
- **Contrast**: WCAG AA compliant (4.5:1 for text)

### SwiftUI Architecture

#### Golden Path (`knowledge/swiftui/golden_path.md`)
- **Feature-First Structure**: Organize by feature, not layer
- **MVVM Pattern**: Strict separation (View → ViewModel → Service)
- **State Management**: ViewModels must expose a `State` enum
- **Design System**: Reusable components with semantic tokens

#### SwiftLint Rules (`knowledge/swiftui/swiftlint_rules.yml`)
- **Force Unwrapping**: Error-level (prevents crashes)
- **Custom Rules**: Detect hardcoded sizes, colors, and padding
- **Code Quality**: Enforces clean architecture patterns

## Tools

### Swift Syntax Analyzer

An MCP server that analyzes Swift code for HIG violations.

**Checks:**
- Hardcoded frame sizes
- Hardcoded RGB colors
- Hardcoded font sizes (bypassing Dynamic Type)
- Force unwrapping operators
- Touch targets below 44pt
- Missing ViewModel State enums
- Missing accessibility labels

**Usage:**
```python
# The agent invokes this automatically via MCP
# Manual testing:
echo '{"code": "Button { }.frame(width: 30)"}' | python3 tools/swift_syntax_analyzer.py
```

## Customization

### Adding New Skills

1. Create a new folder in `skills/[SkillName]/`
2. Add a `SKILL.md` file with the protocol
3. Update `GEMINI.md` to add the routing rule:

```markdown
| "Your trigger phrase" | `${extensionPath}/skills/[SkillName]/SKILL.md` |
```

### Updating Knowledge Base

Edit the markdown files in `knowledge/`. Changes are immediately available to all linked projects.

### Extending SwiftLint Rules

Edit `knowledge/swiftui/swiftlint_rules.yml` and add custom rules:

```yaml
custom_rules:
  your_rule_name:
    name: "Your Rule"
    regex: 'pattern'
    message: "Your message"
    severity: warning
```

## Architecture Principles

### 1. Progressive Loading
Only the lightweight `GEMINI.md` is loaded initially. Heavy SKILL.md files are loaded on-demand, keeping the context window clean.

### 2. Decoupled Intelligence
Your project repo contains only app code. The "intelligence" lives in this linked extension.

### 3. Live Updates
Changes to the Master Repo propagate instantly to all linked projects (when using `link` instead of `install`).

### 4. Self-Correction
Every skill includes a verification checklist. The agent validates its work against HIG before delivering.

## Best Practices

### For Users

1. **Trust the Skills**: Let the agent follow the SKILL.md protocols completely before intervening.
2. **Provide Context**: Mention the feature name (e.g., "in the Authentication feature") for accurate file placement.
3. **Iterate in Phases**: Design → Implement → Test (don't skip the design phase).

### For AI Agents

1. **Always Read Context Files**: Load knowledge files before implementing.
2. **Follow Checklists**: Complete all verification steps in SKILL.md.
3. **Use Semantic Tokens**: Never hardcode sizes, colors, or spacing.
4. **Prioritize Accessibility**: Add labels to all interactive elements.

## Troubleshooting

### Agent Doesn't Load Skills

**Issue**: Agent responds generically without referencing SKILL.md files.

**Solution**:
1. Verify the extension is linked: `gemini extensions list`
2. Check that `GEMINI.md` exists and has correct routing table.
3. Re-link the extension: `gemini extensions unlink ios-master-architect && gemini extensions link ~/path/to/ios-master-skills`

### SwiftLint Not Running

**Issue**: Code doesn't pass linting after generation.

**Solution**:
1. Ensure `.swiftlint.yml` is in your project root (not in `Sources/`).
2. Install SwiftLint: `brew install swiftlint`
3. Run manually: `swiftlint lint --strict`

### Script Permissions Error

**Issue**: `init_project.sh` fails with "Permission denied".

**Solution**:
```bash
chmod +x ios-master-skills/skills/scaffold_new_app/scripts/init_project.sh
```

## Contributing

This repository is designed to evolve with iOS best practices.

### Adding New HIG Guidelines

Update the relevant knowledge file:
- Layout changes → `knowledge/ios_hig/layout.md`
- New text styles → `knowledge/ios_hig/typography.md`
- Color updates → `knowledge/ios_hig/colors.md`

### Updating for New iOS Versions

When Apple releases new HIG guidelines:
1. Update knowledge files with new requirements
2. Add new semantic styles/colors if introduced
3. Update SwiftLint rules if needed
4. Test with Xcode beta versions

## Version History

### v1.0.0 (Current)
- Initial release
- Three core skills: Scaffold, Design, Implement
- Complete HIG knowledge base (iOS 17+)
- SwiftUI Golden Path architecture
- Swift syntax analyzer tool

## License

This repository is provided as-is for educational and development purposes. Apple Human Interface Guidelines and SwiftUI are trademarks of Apple Inc.

## Support

For issues, questions, or contributions:
1. Check the troubleshooting section above
2. Review the knowledge files for guidance
3. Consult Apple's official HIG documentation: https://developer.apple.com/design/human-interface-guidelines/

---

**Built with**: Claude Code, structured for Google Antigravity
**Architecture**: Master Repo Pattern with MCP Integration
**Target**: Production-grade SwiftUI development on iOS 17+
