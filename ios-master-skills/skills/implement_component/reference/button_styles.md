# Button Styles Reference

This file contains reference implementations for common button patterns in SwiftUI.

## 1. Primary Button (Call-to-Action)

Use for the main action on a screen (e.g., "Sign In", "Submit", "Continue").

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
                .frame(minHeight: 50)
                .background(Color.blue)
                .cornerRadius(12)
        }
        .buttonStyle(.plain)
        .contentShape(Rectangle())
    }
}
```

**Characteristics:**
- Full width with `.infinity` frame
- 50pt minimum height (exceeds 44pt requirement)
- High contrast (white text on blue background)
- Prominent corner radius (12pt)

## 2. Secondary Button (Alternative Action)

Use for secondary actions (e.g., "Cancel", "Skip", "Learn More").

```swift
struct SecondaryButton: View {
    let title: String
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Text(title)
                .font(.headline)
                .foregroundColor(.blue)
                .frame(maxWidth: .infinity)
                .frame(minHeight: 50)
                .background(Color.clear)
                .overlay(
                    RoundedRectangle(cornerRadius: 12)
                        .stroke(Color.blue, lineWidth: 2)
                )
        }
        .buttonStyle(.plain)
        .contentShape(Rectangle())
    }
}
```

**Characteristics:**
- Full width with border (outline style)
- Same height as primary button for consistency
- Lower visual weight (no fill)
- Uses accent color for border and text

## 3. Destructive Button (Delete/Cancel)

Use for destructive actions (e.g., "Delete Account", "Sign Out").

```swift
struct DestructiveButton: View {
    let title: String
    let action: () -> Void

    var body: some View {
        Button(role: .destructive, action: action) {
            Text(title)
                .font(.headline)
                .foregroundColor(.white)
                .frame(maxWidth: .infinity)
                .frame(minHeight: 50)
                .background(Color.red)
                .cornerRadius(12)
        }
        .buttonStyle(.plain)
        .contentShape(Rectangle())
    }
}
```

**Characteristics:**
- Uses `.destructive` role for semantic meaning
- Red background (system red, adapts to Dark Mode)
- Same size as primary button
- Should be used sparingly and with confirmation dialogs

## 4. Text Button (Low Priority Action)

Use for low-priority actions (e.g., "Skip", "Not Now", "Forgot Password?").

```swift
struct TextButton: View {
    let title: String
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Text(title)
                .font(.callout)
                .foregroundColor(.blue)
                .frame(minHeight: 44)
        }
        .buttonStyle(.plain)
        .contentShape(Rectangle())
    }
}
```

**Characteristics:**
- No background or border
- Smaller font size (`.callout` = 16pt)
- 44pt minimum height (meets touch target requirement)
- Uses accent color

## 5. Icon Button (Toolbar/Navigation)

Use for toolbar actions or icon-only buttons.

```swift
struct IconButton: View {
    let systemName: String
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Image(systemName: systemName)
                .font(.system(size: 20))
                .foregroundColor(.primary)
                .frame(width: 44, height: 44)
        }
        .buttonStyle(.plain)
        .contentShape(Rectangle())
    }
}
```

**Characteristics:**
- Fixed 44x44pt frame (touch target requirement)
- Icon is smaller (20pt) but hit area is expanded
- `.contentShape(Rectangle())` ensures full frame is tappable
- Uses `.primary` color for adaptability

## 6. Floating Action Button (FAB)

Use for primary screen-level actions (e.g., "Add New Item").

```swift
struct FloatingActionButton: View {
    let systemName: String
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Image(systemName: systemName)
                .font(.title2)
                .foregroundColor(.white)
                .frame(width: 60, height: 60)
                .background(Color.blue)
                .clipShape(Circle())
                .shadow(color: .black.opacity(0.2), radius: 8, x: 0, y: 4)
        }
        .buttonStyle(.plain)
        .contentShape(Circle())
    }
}
```

**Characteristics:**
- Circular shape with 60pt diameter (exceeds 44pt requirement)
- Elevated appearance with shadow
- Used as an overlay (e.g., bottom-trailing corner)
- High visual prominence

**Usage Example:**
```swift
VStack {
    // Main content
}
.overlay(alignment: .bottomTrailing) {
    FloatingActionButton(systemName: "plus") {
        viewModel.addItem()
    }
    .padding(.trailing, .lg)
    .padding(.bottom, .lg)
}
```

## 7. Pill Button (Tag/Filter)

Use for tags, filters, or selection chips.

```swift
struct PillButton: View {
    let title: String
    let isSelected: Bool
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Text(title)
                .font(.subheadline)
                .foregroundColor(isSelected ? .white : .primary)
                .padding(.horizontal, .md)
                .padding(.vertical, .xs)
                .frame(minHeight: 36)
                .background(isSelected ? Color.blue : Color.secondarySystemBackground)
                .cornerRadius(18)
        }
        .buttonStyle(.plain)
        .contentShape(RoundedRectangle(cornerRadius: 18))
    }
}
```

**Characteristics:**
- Capsule shape (height / 2 corner radius)
- Toggleable appearance (selected vs. unselected)
- Compact size (36pt height is acceptable for secondary actions)
- Often used in horizontal scrolling collections

**Usage Example:**
```swift
ScrollView(.horizontal, showsIndicators: false) {
    HStack(spacing: .sm) {
        PillButton(title: "All", isSelected: viewModel.filter == .all) {
            viewModel.filter = .all
        }
        PillButton(title: "Active", isSelected: viewModel.filter == .active) {
            viewModel.filter = .active
        }
        PillButton(title: "Completed", isSelected: viewModel.filter == .completed) {
            viewModel.filter = .completed
        }
    }
    .padding(.horizontal, .lg)
}
```

## 8. Loading Button (Async Action Indicator)

Use for buttons that trigger async operations.

```swift
struct LoadingButton: View {
    let title: String
    let isLoading: Bool
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            ZStack {
                Text(title)
                    .font(.headline)
                    .foregroundColor(.white)
                    .opacity(isLoading ? 0 : 1)

                if isLoading {
                    ProgressView()
                        .tint(.white)
                }
            }
            .frame(maxWidth: .infinity)
            .frame(minHeight: 50)
            .background(Color.blue)
            .cornerRadius(12)
        }
        .disabled(isLoading)
        .buttonStyle(.plain)
        .contentShape(Rectangle())
    }
}
```

**Characteristics:**
- Shows loading spinner when action is in progress
- Disables interaction during loading
- Maintains button size (doesn't collapse)
- Hides text label during loading for clarity

## Usage Guidelines

### Button Hierarchy

In a single screen, follow this priority order:
1. **One Primary Button**: The main action
2. **Optional Secondary Button**: Alternative action
3. **Text Buttons**: Low-priority actions
4. **Icon Buttons**: Utility actions (share, close, etc.)

### Button Placement

- **Primary actions**: Bottom of the screen or form (thumb zone).
- **Destructive actions**: Never as the default action; always require confirmation.
- **Cancel/Back**: Top-left (standard iOS convention).
- **Floating Action Button**: Bottom-trailing corner with padding.

### Accessibility

Always add accessibility labels to icon-only buttons:

```swift
IconButton(systemName: "magnifyingglass") {
    viewModel.search()
}
.accessibilityLabel("Search")
.accessibilityHint("Double tap to open search")
```

### State Management

Buttons should reflect state visually:

```swift
PrimaryButton("Submit") {
    viewModel.submit()
}
.disabled(!viewModel.isValid)
.opacity(viewModel.isValid ? 1.0 : 0.5)
```

### Dark Mode Consideration

All these button styles use semantic colors that automatically adapt:
- `Color.blue` → System blue (adapts to Dark Mode)
- `Color.white` → Always white (use for text on colored backgrounds)
- `Color.primary` → Black in Light Mode, White in Dark Mode

## Testing Checklist

Before shipping button implementations:
- [ ] All buttons meet 44pt minimum touch target (or justify smaller size for secondary actions).
- [ ] `.contentShape()` is applied for small icons.
- [ ] Colors use semantic system colors.
- [ ] Buttons have accessibility labels (especially icon-only buttons).
- [ ] Disabled states are visually distinct.
- [ ] Buttons are tested in both Light and Dark modes.
- [ ] Buttons scale properly with Dynamic Type.
