# iOS Human Interface Guidelines: Typography

## Dynamic Type System

All text must use semantic text styles that automatically adapt to user accessibility settings.

### Standard Text Styles

| Style | Default Size | Weight | Use Case |
|-------|-------------|--------|----------|
| `.largeTitle` | 34pt | Regular | Page titles (iOS 11+) |
| `.title` | 28pt | Regular | Section headers |
| `.title2` | 22pt | Regular | Secondary headers (iOS 14+) |
| `.title3` | 20pt | Regular | Tertiary headers (iOS 14+) |
| `.headline` | 17pt | Semibold | List item titles, emphasis |
| `.body` | 17pt | Regular | **Default body text** |
| `.callout` | 16pt | Regular | Secondary body text |
| `.subheadline` | 15pt | Regular | Subtitles, captions |
| `.footnote` | 13pt | Regular | Fine print, annotations |
| `.caption` | 12pt | Regular | Timestamps, metadata |
| `.caption2` | 11pt | Regular | Smallest readable text (iOS 14+) |

### Usage Rules

**1. Body is the Default**
- Use `.body` (17pt) as your base text size.
- Only deviate for semantic meaning (headers, captions).

**2. Never Hardcode Font Sizes**
❌ `.font(.system(size: 18))`
✅ `.font(.body)`

**3. Scale with Dynamic Type**
All text automatically scales from `xSmall` to `AX5` accessibility sizes when using semantic styles.

**Example:**
```swift
Text("Welcome")
    .font(.largeTitle)  // ✅ Adapts to user settings

Text("Description")
    .font(.system(size: 14))  // ❌ Fixed size, breaks accessibility
```

### Custom Fonts with Dynamic Type

If using a custom font, you MUST enable Dynamic Type scaling:

```swift
Text("Custom Font")
    .font(.custom("YourFont-Bold", size: 17, relativeTo: .body))
```

### Line Spacing & Readability

- **Body text**: Default line spacing (1.0) is optimal.
- **Long-form content**: Increase to 1.2 for better readability.
- **Headlines**: Tighten to 0.9 for compact impact.

```swift
Text("Long article content...")
    .font(.body)
    .lineSpacing(4)  // Adds breathing room
```

### Text Alignment

- **Left-aligned**: Default for LTR languages (English).
- **Center-aligned**: Titles, short emphasis text.
- **Right-aligned**: Rarely used except for RTL languages or numeric tables.

**Accessibility Rule**: Use `.multilineTextAlignment(.leading)` instead of `.center` for paragraph text to maintain scannability.

### Color & Contrast

**Minimum Contrast Ratios (WCAG AA):**
- Body text (17pt): **4.5:1** against background
- Large text (24pt+): **3:1** against background

**Semantic Colors:**
Always use semantic color tokens that adapt to Light/Dark mode:

```swift
Text("Label")
    .foregroundColor(.primary)   // ✅ High contrast (black/white)

Text("Secondary")
    .foregroundColor(.secondary) // ✅ Lower contrast (gray)

Text("Blue text")
    .foregroundColor(.blue)      // ❌ May fail contrast in Light mode
```

### Font Weights

Use weights sparingly for hierarchy:

| Weight | Use Case |
|--------|----------|
| `.regular` | Default body text |
| `.medium` | Subtle emphasis (iOS 16+) |
| `.semibold` | Buttons, headlines |
| `.bold` | High-priority actions |

**Never use** `.ultraLight` or `.black` — they create accessibility issues.

### Text Truncation

- **Single line**: Use `.lineLimit(1)` with `.truncationMode(.tail)` (default).
- **Multi-line**: Set `.lineLimit(3)` for previews, provide "Read more" expansion.

```swift
Text("Long description...")
    .lineLimit(2)
    .truncationMode(.tail)
```

### Text Fields & Input

**Placeholder text:**
- Use `.secondary` color for placeholders (automatically styled).
- Must be 17pt (`.body` size).

**Input text:**
- Must be `.body` or larger.
- Minimum height: 44pt (includes padding).

## Critical Violations to Avoid

❌ **NEVER DO:**
- `.font(.system(size: 14))` — Bypasses accessibility scaling
- `Text("Important").foregroundColor(.gray)` — Hardcoded color won't adapt to Dark Mode
- `.lineLimit(1)` on long-form content without "Show more" option

✅ **ALWAYS DO:**
- Use semantic text styles (`.body`, `.headline`, etc.)
- Use semantic colors (`.primary`, `.secondary`)
- Test with largest accessibility text size (Settings > Accessibility > Display & Text Size)

## Dynamic Type Testing Checklist

Before shipping, verify:
1. Enable "Larger Text" in Accessibility settings → set to AX3.
2. All text should remain readable (no clipping).
3. Layout should reflow (not fixed heights).
4. Buttons should expand vertically to fit text.
