# SwiftUI Project Structure: The Golden Path

This document defines the mandatory folder structure and architectural patterns for all iOS projects in this system.

## 1. Hierarchy Rules

All new features must follow this strict **"Feature-First"** directory structure:

```
/Sources/
├── App/
│   ├── [AppName]App.swift          # App entry point
│   └── AppDelegate.swift           # iOS lifecycle hooks (if needed)
├── Features/
│   ├── [FeatureName]/              # e.g., Authentication, Dashboard, Profile
│   │   ├── Views/
│   │   │   ├── [Feature]View.swift
│   │   │   └── Components/
│   │   │       └── [SubView].swift
│   │   ├── ViewModels/
│   │   │   └── [Feature]ViewModel.swift
│   │   ├── Models/
│   │   │   └── [Feature]Model.swift
│   │   └── Services/
│   │       └── [Feature]Service.swift
│   └── [NextFeature]/
│       └── (same structure)
└── Shared/
    ├── DesignSystem/
    │   ├── Components/
    │   │   ├── Buttons/
    │   │   │   ├── PrimaryButton.swift
    │   │   │   └── SecondaryButton.swift
    │   │   ├── Cards/
    │   │   └── TextFields/
    │   ├── Tokens/
    │   │   ├── Spacing.swift
    │   │   └── Typography.swift
    │   └── Theme.swift
    ├── Extensions/
    │   ├── View+Extensions.swift
    │   └── Color+Extensions.swift
    ├── Utilities/
    │   ├── NetworkClient.swift
    │   └── Logger.swift
    └── Resources/
        └── Assets.xcassets
```

### Why Feature-First?

- **Scalability**: Each feature is self-contained. Adding a new feature doesn't pollute the existing structure.
- **Collaboration**: Multiple developers can work on separate features without conflicts.
- **Testability**: Each feature can be tested in isolation.
- **Discoverability**: Finding code related to a feature is deterministic (no hunting across scattered files).

### Naming Conventions

- **Features**: Use singular noun (e.g., `Authentication`, not `Auth` or `Authentications`).
- **Views**: Suffix with `View` (e.g., `LoginView`, not `LoginScreen`).
- **ViewModels**: Suffix with `ViewModel` (e.g., `LoginViewModel`).
- **Services**: Suffix with `Service` (e.g., `AuthenticationService`).

## 2. MVVM Architecture

### The Contract

Every feature must follow the **MVVM (Model-View-ViewModel)** pattern:

#### Views
- **Purely declarative**: No business logic, no network calls, no data transformations.
- **Responsibilities**:
  - Render UI based on ViewModel state.
  - Handle user interactions by calling ViewModel methods.
  - Apply Design System components.

**Example:**
```swift
struct LoginView: View {
    @State private var viewModel = LoginViewModel()

    var body: some View {
        VStack(spacing: .md) {
            TextField("Email", text: $viewModel.email)
            SecureField("Password", text: $viewModel.password)

            PrimaryButton("Sign In") {
                viewModel.login()
            }
            .disabled(!viewModel.isValid)
        }
        .padding()
        .alert("Error", isPresented: $viewModel.showError) {
            Button("OK", role: .cancel) {}
        } message: {
            Text(viewModel.errorMessage)
        }
    }
}
```

#### ViewModels
- **Observable**: Must use `@Observable` (iOS 17+) or `ObservableObject` (iOS 16 and below).
- **State Management**: Expose a `State` enum (`Idle`, `Loading`, `Content`, `Error`).
- **Business Logic**: Handle data transformations, validation, and orchestration.

**Example:**
```swift
@Observable
final class LoginViewModel {
    enum State {
        case idle
        case loading
        case success
        case error(String)
    }

    var state: State = .idle
    var email = ""
    var password = ""

    var isValid: Bool {
        !email.isEmpty && password.count >= 8
    }

    var showError: Bool {
        if case .error = state { return true }
        return false
    }

    var errorMessage: String {
        if case .error(let message) = state { return message }
        return ""
    }

    private let authService: AuthenticationService

    init(authService: AuthenticationService = .shared) {
        self.authService = authService
    }

    func login() {
        state = .loading

        Task {
            do {
                try await authService.login(email: email, password: password)
                state = .success
            } catch {
                state = .error(error.localizedDescription)
            }
        }
    }
}
```

#### Models
- **Data structures**: Plain Swift structs or classes (prefer `struct` for value semantics).
- **Codable**: Implement `Codable` for API responses.
- **No logic**: Models are dumb data containers.

**Example:**
```swift
struct User: Codable, Identifiable {
    let id: String
    let email: String
    let displayName: String
    let avatarURL: URL?
}
```

#### Services
- **API Clients**: Handle network requests, local storage, or third-party SDKs.
- **Protocol-based**: Define protocols for testability.
- **Singleton or Dependency Injection**: Use `.shared` singleton or inject via initializer.

**Example:**
```swift
protocol AuthenticationServiceProtocol {
    func login(email: String, password: String) async throws
    func logout() async throws
}

final class AuthenticationService: AuthenticationServiceProtocol {
    static let shared = AuthenticationService()

    func login(email: String, password: String) async throws {
        // Network call
    }

    func logout() async throws {
        // Clear session
    }
}
```

## 3. Design System

The `Shared/DesignSystem/` folder contains reusable UI components. This is the **single source of truth** for app styling.

### Components

Every visual element should be abstracted into a reusable component:

**Example: PrimaryButton.swift**
```swift
struct PrimaryButton: View {
    let title: String
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Text(title)
                .font(.headline)
                .foregroundColor(.white)
                .frame(maxWidth: .infinity)
                .frame(height: 50)
                .background(Color.blue)
                .cornerRadius(12)
        }
        .buttonStyle(.plain)
    }
}
```

### Tokens

Use semantic tokens for spacing, typography, and colors instead of hardcoded values.

**Example: Spacing.swift**
```swift
extension CGFloat {
    static let xxs: CGFloat = 4
    static let xs: CGFloat = 8
    static let sm: CGFloat = 12
    static let md: CGFloat = 16
    static let lg: CGFloat = 24
    static let xl: CGFloat = 32
    static let xxl: CGFloat = 48
}

// Usage
VStack(spacing: .md) {
    // Content
}
.padding(.horizontal, .lg)
```

## 4. State Management Rules

### Local State
Use `@State` for view-specific state (e.g., text field input, toggle state).

### Shared State
Use `@Environment` or a shared `@Observable` object for cross-feature state (e.g., user session, theme).

**Example:**
```swift
@Observable
final class AppState {
    var currentUser: User?
    var isAuthenticated: Bool { currentUser != nil }
}

@main
struct MyApp: App {
    @State private var appState = AppState()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(appState)
        }
    }
}

// Usage in a view
struct ProfileView: View {
    @Environment(AppState.self) private var appState

    var body: some View {
        if let user = appState.currentUser {
            Text("Welcome, \(user.displayName)")
        }
    }
}
```

## 5. Navigation

Use the modern `NavigationStack` (iOS 16+) with type-safe routes.

**Example:**
```swift
enum Route: Hashable {
    case login
    case dashboard
    case profile(userId: String)
}

struct ContentView: View {
    @State private var path: [Route] = []

    var body: some View {
        NavigationStack(path: $path) {
            LoginView()
                .navigationDestination(for: Route.self) { route in
                    switch route {
                    case .login:
                        LoginView()
                    case .dashboard:
                        DashboardView()
                    case .profile(let userId):
                        ProfileView(userId: userId)
                    }
                }
        }
    }
}
```

## 6. Testing Structure

Mirror the source structure in your test folder:

```
/Tests/
├── FeaturesTests/
│   ├── AuthenticationTests/
│   │   ├── LoginViewModelTests.swift
│   │   └── AuthenticationServiceTests.swift
│   └── DashboardTests/
└── SharedTests/
    └── DesignSystemTests/
```

## 7. Critical Rules

✅ **ALWAYS DO:**
- Create a new folder in `Features/` for each major feature.
- Use MVVM separation (View → ViewModel → Service).
- Expose a `State` enum in ViewModels.
- Use Design System components (never inline styling).
- Use semantic tokens (`.md`, `.lg`) for spacing.

❌ **NEVER DO:**
- Put business logic in Views.
- Create a "Helpers" or "Utils" dumping ground.
- Hardcode colors or spacing (use tokens).
- Mix feature code (e.g., Login logic in Dashboard folder).

## 8. Migration Checklist

If adding this structure to an existing project:

1. Create the `Features/` and `Shared/DesignSystem/` folders.
2. Move existing views into feature folders.
3. Extract ViewModels from Views (if they have business logic).
4. Create a `DesignSystem/Components/` folder and migrate one button/card at a time.
5. Create `Spacing.swift` and replace hardcoded padding values.

## 9. Code Review Checklist

Before submitting code, verify:

- [ ] Feature is in correct `Features/[Name]/` folder.
- [ ] View has no business logic (only `body` and `@State` for UI).
- [ ] ViewModel exposes a `State` enum.
- [ ] No hardcoded spacing/colors (uses tokens).
- [ ] Reusable components are in `DesignSystem/`.
- [ ] No force unwraps (`!`) in production code.
