# iOS Human Interface Guidelines: Colors

## Semantic Color System

iOS uses a semantic color system that automatically adapts to Light Mode, Dark Mode, and accessibility settings. **Never hardcode hex colors** unless defining custom brand colors in an Asset Catalog.

### System Colors (Adaptive)

#### Label Colors (Text)
These colors are designed for text and maintain proper contrast in all modes.

| Color | Light Mode | Dark Mode | Use Case |
|-------|-----------|-----------|----------|
| `.primary` | Black (opacity 1.0) | White (opacity 1.0) | Primary text, body copy |
| `.secondary` | Black (opacity 0.6) | White (opacity 0.6) | Secondary labels, subtitles |
| `.tertiary` | Black (opacity 0.3) | White (opacity 0.3) | Disabled text, placeholders |
| `.quaternary` | Black (opacity 0.18) | White (opacity 0.16) | Watermarks, very subtle text |

**Example:**
```swift
Text("Heading")
    .foregroundColor(.primary)

Text("Subtitle")
    .foregroundColor(.secondary)
```

#### Fill Colors (Backgrounds)
Used for UI element backgrounds (buttons, cards, input fields).

| Color | Use Case |
|-------|----------|
| `.systemFill` | Primary fill for controls |
| `.secondarySystemFill` | Secondary elements (cards) |
| `.tertiarySystemFill` | Tertiary elements (disabled states) |
| `.quaternarySystemFill` | Subtle backgrounds |

#### Background Colors
Used for screen-level backgrounds.

| Color | Use Case |
|-------|----------|
| `.systemBackground` | Primary background (screens, modals) |
| `.secondarySystemBackground` | Grouped content backgrounds (table cells) |
| `.tertiarySystemBackground` | Nested grouped content |

**Example:**
```swift
VStack {
    // Content
}
.background(Color.secondarySystemBackground)
```

### Accent Colors (Interactive)

These colors indicate interactivity and should be used sparingly.

| Color | Use Case |
|-------|----------|
| `.blue` | Default interactive elements (links, buttons) |
| `.green` | Success states |
| `.red` | Destructive actions, errors |
| `.orange` | Warnings |
| `.yellow` | Caution (use sparingly, low contrast) |
| `.purple`, `.pink`, `.indigo` | Brand accents, creative UI |

**Tint Color:**
Use `.tint()` modifier to apply app-wide accent color:

```swift
NavigationView {
    // Content
}
.tint(.purple)  // All buttons, links, and controls use purple
```

### Custom Brand Colors

If you need brand-specific colors:

**1. Define in Asset Catalog**
- Create color set in `Assets.xcassets`.
- Define separate appearances for Light and Dark modes.
- Name semantically (e.g., "BrandPrimary", not "Blue500").

**2. Use in Code**
```swift
Color("BrandPrimary")  // Automatically adapts to Light/Dark mode
```

**3. Ensure WCAG Contrast**
- Light mode: Minimum 4.5:1 for text, 3:1 for UI elements.
- Dark mode: Test with both pure black (#000000) and elevated backgrounds (#1C1C1E).

### Gradients

Use gradients sparingly for visual interest, not for functional UI.

**Linear Gradient:**
```swift
LinearGradient(
    colors: [.blue, .purple],
    startPoint: .topLeading,
    endPoint: .bottomTrailing
)
```

**Radial Gradient:**
```swift
RadialGradient(
    colors: [.white, .blue],
    center: .center,
    startRadius: 0,
    endRadius: 200
)
```

**Rule:** Gradients should never be used on text or interactive elements that need to maintain accessibility contrast.

### Opacity & Transparency

Use opacity intentionally:

| Opacity | Use Case |
|---------|----------|
| `1.0` | Default (fully opaque) |
| `0.8` | Slight de-emphasis |
| `0.5` | Disabled states, overlays |
| `0.0` | Hidden elements (use `.hidden()` instead) |

**Example:**
```swift
Button("Disabled") { }
    .disabled(true)
    .opacity(0.5)
```

### Material Backgrounds (Blur Effects)

Use for overlays and floating UI (sheets, popovers).

```swift
.background(.ultraThinMaterial)  // Subtle blur
.background(.thinMaterial)       // Standard blur
.background(.regularMaterial)    // Default picker style
.background(.thickMaterial)      // Strong blur
.background(.ultraThickMaterial) // Maximum blur
```

**Use Case:** Floating toolbars, overlays, modal sheets.

## Color Usage Rules

### Rule 1: Semantic Over Specific
❌ `.foregroundColor(.black)`
✅ `.foregroundColor(.primary)`

### Rule 2: Test in Both Modes
Always verify your UI in both Light and Dark modes (use Xcode Environment Overrides or device settings).

### Rule 3: Contrast is Non-Negotiable
Use Xcode's Accessibility Inspector to verify contrast ratios. Minimum 4.5:1 for body text.

### Rule 4: Use Tint for App Identity
Set a global tint color in your `App` struct:

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .tint(.indigo)  // App-wide accent color
        }
    }
}
```

### Rule 5: Limited Palette
Use no more than 3-4 colors in your UI:
1. Primary color (brand)
2. Secondary color (accent)
3. Semantic colors (success/error)
4. Neutral colors (text/backgrounds)

## Critical Violations to Avoid

❌ **NEVER DO:**
- `Color(red: 0.2, green: 0.4, blue: 0.8)` — Hardcoded RGB won't adapt to Dark Mode
- `.foregroundColor(.white)` on a button — May be invisible in Dark Mode
- Using yellow for important text — Fails contrast requirements

✅ **ALWAYS DO:**
- Use semantic colors (`.primary`, `.secondary`, `.systemBackground`)
- Define custom colors in Asset Catalog with Light/Dark variants
- Test with Accessibility Inspector for contrast
- Use `.tint()` for consistent interactive color

## Dark Mode Testing Checklist

Before shipping, verify:
1. Switch to Dark Mode (Settings > Display > Dark).
2. All text remains readable (no white text on light backgrounds).
3. Custom colors defined in Asset Catalog have Dark variants.
4. Check contrast with Accessibility Inspector (Xcode > Accessibility Inspector > Audit).
