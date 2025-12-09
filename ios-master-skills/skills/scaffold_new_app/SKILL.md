---
name: Scaffold New iOS App
description: Sets up folder structure, strict linting, and Git hygiene for a new SwiftUI project.
---

# Protocol: New App Scaffolding

## Context

Before starting, **read these files immediately**:
1. `../../knowledge/swiftui/golden_path.md` — Understand the mandatory folder structure.
2. `../../knowledge/swiftui/swiftlint_rules.yml` — Understand the linting rules to be installed.

## Objective

Set up a production-ready iOS project with:
- Feature-first folder structure (following Golden Path).
- Strict SwiftLint configuration to prevent crashes and enforce best practices.
- Design System scaffolding for reusable components.
- Git initialization (if requested).

## Steps

### 1. Gather Requirements

Ask the user:
- **App Name**: What is the app called? (e.g., "MyAwesomeApp")
- **Starting Features**: What initial features should be scaffolded? (e.g., "Authentication, Dashboard")
  - If none specified, create a single "Home" feature as a starting point.
- **Git Initialization**: Should we initialize a Git repository? (Default: Yes)

### 2. Execute Structure Script

Run the bundled shell script to create the physical folder structure:

```bash
bash ${extensionPath}/skills/scaffold_new_app/scripts/init_project.sh [AppName]
```

**Expected Output:**
- `Sources/App/` folder created
- `Sources/Features/` folder created
- `Sources/Shared/DesignSystem/` folder created

### 3. Create App Entry Point

Create the main App file at `Sources/App/[AppName]App.swift`:

```swift
import SwiftUI

@main
struct [AppName]App: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

### 4. Create Initial ContentView

Create `Sources/App/ContentView.swift`:

```swift
import SwiftUI

struct ContentView: View {
    var body: some View {
        NavigationStack {
            VStack(spacing: 24) {
                Image(systemName: "checkmark.circle.fill")
                    .font(.system(size: 60))
                    .foregroundColor(.green)

                Text("App Structure Ready")
                    .font(.title)
                    .fontWeight(.semibold)

                Text("Your SwiftUI app is scaffolded and ready for development.")
                    .font(.body)
                    .foregroundColor(.secondary)
                    .multilineTextAlignment(.center)
                    .padding(.horizontal)
            }
            .navigationTitle("Welcome")
        }
    }
}

#Preview {
    ContentView()
}
```

### 5. Scaffold Requested Features

For each feature requested by the user (e.g., "Authentication"):

1. Create feature folder: `Sources/Features/[FeatureName]/`
2. Create subfolders: `Views/`, `ViewModels/`, `Models/`, `Services/`
3. Create a placeholder View file:

**Example: `Sources/Features/Authentication/Views/AuthenticationView.swift`**
```swift
import SwiftUI

struct AuthenticationView: View {
    var body: some View {
        VStack {
            Text("Authentication Feature")
                .font(.title)
        }
    }
}

#Preview {
    AuthenticationView()
}
```

4. Create a placeholder ViewModel:

**Example: `Sources/Features/Authentication/ViewModels/AuthenticationViewModel.swift`**
```swift
import SwiftUI

@Observable
final class AuthenticationViewModel {
    enum State {
        case idle
        case loading
        case success
        case error(String)
    }

    var state: State = .idle

    func authenticate() {
        state = .loading
        // TODO: Implement authentication logic
    }
}
```

### 6. Install SwiftLint Configuration

1. Create `.swiftlint.yml` in the **project root** (not inside Sources/).
2. Copy the **exact content** from `../../knowledge/swiftui/swiftlint_rules.yml` into the new file.

**Critical Rule Highlight:**
```yaml
force_unwrapping:
  severity: error  # This prevents crashes from force unwraps (!)
```

### 7. Create Design System Tokens

Create `Sources/Shared/DesignSystem/Tokens/Spacing.swift`:

```swift
import SwiftUI

extension CGFloat {
    /// 4pt - Icon-to-text spacing
    static let xxs: CGFloat = 4

    /// 8pt - Tight element spacing
    static let xs: CGFloat = 8

    /// 12pt - Related content groups
    static let sm: CGFloat = 12

    /// 16pt - Default padding
    static let md: CGFloat = 16

    /// 24pt - Section separation
    static let lg: CGFloat = 24

    /// 32pt - Major content blocks
    static let xl: CGFloat = 32

    /// 48pt - Screen-level separation
    static let xxl: CGFloat = 48
}
```

Create `Sources/Shared/DesignSystem/Components/Buttons/PrimaryButton.swift`:

```swift
import SwiftUI

struct PrimaryButton: View {
    let title: String
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Text(title)
                .font(.headline)
                .foregroundColor(.white)
                .frame(maxWidth: .infinity)
                .frame(minHeight: 50)
                .background(Color.blue)
                .cornerRadius(12)
        }
        .contentShape(Rectangle())
    }
}

#Preview {
    PrimaryButton(title: "Sign In") {
        print("Tapped")
    }
    .padding()
}
```

### 8. Initialize Git (Optional)

If the user requested Git initialization:

```bash
git init
git add .
git commit -m "Initial project setup with feature structure and SwiftLint

- Created feature-first folder structure
- Added SwiftLint configuration with strict rules
- Scaffolded Design System with spacing tokens
- Created placeholder views for [list features]

🤖 Generated with iOS Master Architect
"
```

### 9. Verify Structure

Run the following to confirm the structure was created correctly:

```bash
ls -R Sources/
```

**Expected Output:**
```
Sources/
├── App/
│   ├── [AppName]App.swift
│   └── ContentView.swift
├── Features/
│   └── [FeatureName]/
│       ├── Views/
│       ├── ViewModels/
│       ├── Models/
│       └── Services/
└── Shared/
    ├── DesignSystem/
    │   ├── Components/
    │   │   └── Buttons/
    │   │       └── PrimaryButton.swift
    │   └── Tokens/
    │       └── Spacing.swift
```

### 10. Final Output

Provide the user with:
1. **Confirmation**: "✅ Project '[AppName]' scaffolded successfully."
2. **Next Steps**:
   - "Run `swiftlint` to verify linting is working."
   - "Open the project in Xcode and build to confirm compilation."
   - "Start implementing your first feature in `Sources/Features/[FeatureName]/`."

## Self-Correction Checklist

Before completing, verify:
- [ ] All folders match the Golden Path structure.
- [ ] `.swiftlint.yml` exists in the project root.
- [ ] `force_unwrapping: error` is present in `.swiftlint.yml`.
- [ ] At least one feature folder exists with Views/ViewModels/Models/Services subfolders.
- [ ] `Spacing.swift` tokens are created.
- [ ] `PrimaryButton.swift` has a `.contentShape(Rectangle())` for hit testing.

## Common Pitfalls

❌ **DON'T:**
- Create files directly in `Sources/` without using feature folders.
- Skip the SwiftLint installation (it prevents production bugs).
- Use hardcoded values in the scaffolded code (always use tokens).

✅ **DO:**
- Follow the exact folder structure from `golden_path.md`.
- Ensure every ViewModels has a `State` enum.
- Use semantic spacing (`.md`, `.lg`) even in placeholder code.
