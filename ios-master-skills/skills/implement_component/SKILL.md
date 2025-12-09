---
name: Implement SwiftUI Component
description: Writes production-grade SwiftUI code based on a design specification or user request.
---

# Protocol: Component Implementation

## Context

Before starting, **read these files immediately**:
1. `../../knowledge/swiftui/golden_path.md` — Understand the project structure and MVVM patterns.
2. `../../knowledge/ios_hig/layout.md` — Ensure touch targets and spacing are correct.
3. `../../knowledge/ios_hig/typography.md` — Use semantic text styles.
4. `../../knowledge/ios_hig/colors.md` — Use semantic colors.

## Objective

Convert a design specification (from the `design_screen` skill) or a direct user request into **production-ready SwiftUI code** that:
- Follows the Golden Path architecture.
- Adheres to Apple HIG.
- Passes SwiftLint validation.
- Is fully accessible.

## Steps

### 1. Analyze Input

Determine the input format:

**Option A: JSON Specification** (from `design_screen` skill)
- Parse the JSON structure.
- Extract component types, constraints, and ViewModel requirements.

**Option B: Direct User Request**
- Interpret the request (e.g., "Create a button that submits a form").
- Mentally construct a specification based on HIG knowledge.

### 2. Scaffold View File

Create the view file in the correct location following the Golden Path:

**Path Pattern:**
```
Sources/Features/[FeatureName]/Views/[ViewName].swift
```

**File Structure:**
```swift
import SwiftUI

struct [ViewName]: View {
    @State private var viewModel = [ViewName]ViewModel()

    var body: some View {
        // Implementation
    }
}

#Preview {
    [ViewName]()
}
```

### 3. Apply HIG-Compliant Modifiers

For each component in the specification, apply the appropriate modifiers:

#### Text Elements
```swift
Text("Label")
    .font(.body)              // ✅ Semantic style
    .foregroundColor(.primary) // ✅ Semantic color
```

#### Interactive Elements
```swift
Button("Action") {
    // Action
}
.frame(minHeight: 44)         // ✅ Minimum touch target
.contentShape(Rectangle())    // ✅ Expand hit area for small icons
```

#### Spacing
```swift
VStack(spacing: .md) {        // ✅ Semantic token
    // Content
}
.padding(.horizontal, .lg)    // ✅ Semantic token
```

#### Colors
```swift
.background(Color.secondarySystemBackground)  // ✅ Semantic background
.foregroundColor(.blue)                       // ✅ System accent color
```

### 4. Implement ViewModel (If Needed)

If the component requires state management, create a ViewModel:

**Path Pattern:**
```
Sources/Features/[FeatureName]/ViewModels/[ViewName]ViewModel.swift
```

**ViewModel Template:**
```swift
import SwiftUI

@Observable
final class [ViewName]ViewModel {
    // MARK: - State

    enum State {
        case idle
        case loading
        case content
        case error(String)
    }

    var state: State = .idle

    // MARK: - Properties

    // Add properties here

    // MARK: - Computed Properties

    var isLoading: Bool {
        if case .loading = state { return true }
        return false
    }

    var errorMessage: String {
        if case .error(let message) = state { return message }
        return ""
    }

    // MARK: - Dependencies

    private let service: [Service]Protocol

    // MARK: - Initialization

    init(service: [Service]Protocol = [Service].shared) {
        self.service = service
    }

    // MARK: - Methods

    func performAction() async {
        state = .loading

        do {
            // Perform async work
            state = .content
        } catch {
            state = .error(error.localizedDescription)
        }
    }
}
```

### 5. Add Accessibility

Every interactive element MUST have proper accessibility support:

```swift
Button("Submit") {
    viewModel.submit()
}
.accessibilityLabel("Submit form")
.accessibilityHint("Double tap to submit your information")
```

For custom layouts:
```swift
VStack {
    Image(systemName: "checkmark")
    Text("Success")
}
.accessibilityElement(children: .combine)
.accessibilityLabel("Success indicator")
```

### 6. Self-Correction

Before outputting the code, verify:

**Layout Check:**
- [ ] All buttons have `.frame(minHeight: 44)` or greater.
- [ ] Small icons inside buttons have `.contentShape(Rectangle())`.
- [ ] Spacing uses semantic tokens (`.md`, `.lg`), not hardcoded values.

**Typography Check:**
- [ ] All text uses semantic styles (`.body`, `.headline`), not `.font(.system(size: X))`.
- [ ] Text fields use `.body` or larger.

**Color Check:**
- [ ] All colors use semantic names (`.primary`, `.systemBackground`), not RGB values.
- [ ] No hardcoded hex colors (unless in Asset Catalog).

**Accessibility Check:**
- [ ] All interactive elements have `.accessibilityLabel()`.
- [ ] Images have `.accessibilityHidden(true)` if decorative, or descriptive labels if meaningful.

**Architecture Check:**
- [ ] View is in `Sources/Features/[Feature]/Views/`.
- [ ] ViewModel is in `Sources/Features/[Feature]/ViewModels/`.
- [ ] View has no business logic (only rendering and calling ViewModel methods).
- [ ] ViewModel exposes a `State` enum.

### 7. Output Format

Present the code with clear file paths and explanations:

```
## Implementation: [ComponentName]

**File:** `Sources/Features/[Feature]/Views/[ViewName].swift`

[SwiftUI View Code]

---

**File:** `Sources/Features/[Feature]/ViewModels/[ViewName]ViewModel.swift`

[ViewModel Code]

---

### HIG Compliance Verification
✅ Touch targets: All buttons meet 44pt minimum
✅ Typography: Using Dynamic Type-compatible styles
✅ Colors: Using semantic system colors
✅ Accessibility: All interactive elements have labels

### Next Steps
1. Add this view to your navigation structure.
2. Implement the service layer if network calls are needed.
3. Write unit tests for the ViewModel.
```

## Examples

### Example 1: Primary Button Component

**Input:** "Create a reusable primary button component"

**Output:**

**File:** `Sources/Shared/DesignSystem/Components/Buttons/PrimaryButton.swift`

```swift
import SwiftUI

/// A reusable primary action button that follows Apple HIG.
///
/// Usage:
/// ```swift
/// PrimaryButton("Sign In") {
///     viewModel.login()
/// }
/// .disabled(!viewModel.isValid)
/// ```
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
        .buttonStyle(.plain)
        .contentShape(Rectangle())
    }
}

#Preview {
    VStack(spacing: .md) {
        PrimaryButton("Default Button") {
            print("Tapped")
        }

        PrimaryButton("Disabled Button") {
            print("Tapped")
        }
        .disabled(true)
        .opacity(0.5)
    }
    .padding()
}
```

### Example 2: Login View with ViewModel

**Input:** JSON specification from `design_screen` skill

**Output:**

**File:** `Sources/Features/Authentication/Views/LoginView.swift`

```swift
import SwiftUI

struct LoginView: View {
    @State private var viewModel = LoginViewModel()

    var body: some View {
        NavigationStack {
            VStack(spacing: .lg) {
                // Logo
                Image(systemName: "lock.shield.fill")
                    .font(.system(size: 80))
                    .foregroundColor(.blue)
                    .padding(.bottom, .xl)
                    .accessibilityHidden(true)

                // Email Field
                TextField("Email", text: $viewModel.email)
                    .textInputAutocapitalization(.never)
                    .keyboardType(.emailAddress)
                    .textContentType(.emailAddress)
                    .autocorrectionDisabled()
                    .padding()
                    .background(Color.secondarySystemBackground)
                    .cornerRadius(10)
                    .accessibilityLabel("Email address input field")

                // Password Field
                SecureField("Password", text: $viewModel.password)
                    .textContentType(.password)
                    .padding()
                    .background(Color.secondarySystemBackground)
                    .cornerRadius(10)
                    .accessibilityLabel("Password input field")

                // Sign In Button
                PrimaryButton("Sign In") {
                    Task {
                        await viewModel.login()
                    }
                }
                .disabled(!viewModel.isValid || viewModel.isLoading)
                .opacity(viewModel.isValid ? 1.0 : 0.5)
                .accessibilityLabel("Sign in button")
                .accessibilityHint("Double tap to sign in with your credentials")

                // Forgot Password Link
                Button("Forgot Password?") {
                    viewModel.showForgotPassword()
                }
                .font(.callout)
                .foregroundColor(.blue)
                .frame(minHeight: 44)
                .accessibilityLabel("Forgot password link")
            }
            .padding(.horizontal, .lg)
            .navigationTitle("Sign In")
            .alert("Error", isPresented: $viewModel.showError) {
                Button("OK", role: .cancel) { }
            } message: {
                Text(viewModel.errorMessage)
            }
        }
    }
}

#Preview {
    LoginView()
}
```

**File:** `Sources/Features/Authentication/ViewModels/LoginViewModel.swift`

```swift
import SwiftUI

@Observable
final class LoginViewModel {
    // MARK: - State

    enum State {
        case idle
        case loading
        case success
        case error(String)
    }

    var state: State = .idle

    // MARK: - Properties

    var email = ""
    var password = ""

    // MARK: - Computed Properties

    var isValid: Bool {
        !email.isEmpty && password.count >= 8
    }

    var isLoading: Bool {
        if case .loading = state { return true }
        return false
    }

    var showError: Bool {
        if case .error = state { return true }
        return false
    }

    var errorMessage: String {
        if case .error(let message) = state { return message }
        return ""
    }

    // MARK: - Dependencies

    private let authService: AuthenticationServiceProtocol

    // MARK: - Initialization

    init(authService: AuthenticationServiceProtocol = AuthenticationService.shared) {
        self.authService = authService
    }

    // MARK: - Methods

    func login() async {
        state = .loading

        do {
            try await authService.login(email: email, password: password)
            state = .success
        } catch {
            state = .error(error.localizedDescription)
        }
    }

    func showForgotPassword() {
        // TODO: Navigate to forgot password flow
    }
}
```

### Example 3: List Row Component

**Input:** "Create a list row component for displaying user profiles"

**Output:**

**File:** `Sources/Features/Profile/Views/Components/ProfileRowView.swift`

```swift
import SwiftUI

struct ProfileRowView: View {
    let user: User

    var body: some View {
        HStack(spacing: .md) {
            // Avatar
            AsyncImage(url: user.avatarURL) { image in
                image
                    .resizable()
                    .aspectRatio(contentMode: .fill)
            } placeholder: {
                Image(systemName: "person.circle.fill")
                    .resizable()
                    .foregroundColor(.secondary)
            }
            .frame(width: 60, height: 60)
            .clipShape(Circle())
            .accessibilityLabel("\(user.displayName)'s profile picture")

            // User Info
            VStack(alignment: .leading, spacing: 4) {
                Text(user.displayName)
                    .font(.headline)
                    .foregroundColor(.primary)

                Text(user.email)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }

            Spacer()

            // Chevron
            Image(systemName: "chevron.right")
                .font(.caption)
                .foregroundColor(.secondary)
                .accessibilityHidden(true)
        }
        .padding(.vertical, .xs)
        .frame(minHeight: 76)  // 60pt image + 8pt padding each side
        .contentShape(Rectangle())
        .accessibilityElement(children: .combine)
        .accessibilityLabel("Profile row for \(user.displayName)")
        .accessibilityHint("Double tap to view profile details")
    }
}

#Preview {
    List {
        ProfileRowView(user: User.preview)
        ProfileRowView(user: User.preview2)
    }
}
```

## Reference Files

Consult these files for common component implementations:
- `./reference/button_styles.md` — Button variants and styles
- `./reference/form_fields.md` — Text fields, pickers, toggles (TODO)
- `./reference/lists.md` — List styles and row components (TODO)

## Self-Correction Checklist

Before completing, verify:
- [ ] File is in correct `Features/[Feature]/` folder.
- [ ] View has no business logic.
- [ ] ViewModel exposes a `State` enum (if applicable).
- [ ] All buttons have `minHeight: 44pt` or greater.
- [ ] All text uses semantic styles (`.body`, `.headline`).
- [ ] All colors use semantic names (`.primary`, `.systemBackground`).
- [ ] All spacing uses tokens (`.md`, `.lg`).
- [ ] All interactive elements have accessibility labels.
- [ ] Preview is included at the bottom of the file.

## Common Pitfalls

❌ **DON'T:**
- Put business logic in the View.
- Use hardcoded sizes, colors, or spacing.
- Skip accessibility labels.
- Forget the `#Preview` block.

✅ **DO:**
- Follow MVVM separation strictly.
- Use semantic tokens for all styling.
- Test with Dynamic Type (large text sizes).
- Include clear documentation comments for reusable components.
