# iOS Human Interface Guidelines: Layout

## Inviolable Layout Rules

### Touch Targets

**Minimum tappable area: 44x44 pt**

- If a visual element is smaller (e.g., 24pt icon), use `.contentShape(Rectangle())` on the button frame to expand the hit test area.
- For toolbar icons or compact UI, ensure the entire tappable frame meets the 44pt minimum, even if the icon itself is smaller.

**Example:**
```swift
Button(action: { }) {
    Image(systemName: "heart")
        .font(.system(size: 20))
}
.frame(width: 44, height: 44)
.contentShape(Rectangle())
```

### Safe Areas

**Bottom Safe Area: ~34pt reserved for Home Indicator**
- NEVER place interactive controls in the bottom 34pt on devices with Home Indicator.
- Use `.safeAreaInset()` for floating controls that need to respect this area.
- TabBars automatically handle this spacing.

**Top Safe Area: Dynamic Island/Notch**
- Varies by device (20pt to 59pt).
- Use standard navigation bars or `.safeAreaInset()` for custom headers.
- Never hardcode top padding values.

**Example:**
```swift
VStack {
    // Content
}
.safeAreaInset(edge: .bottom) {
    FloatingButton()
        .padding(.bottom, 16)
}
```

### Touch vs. Sight Hierarchy

**Interactive vs. Content Distinction**
- Interactive elements must be clearly distinguishable from content.
- Use color, size, and elevation (shadows) to indicate interactivity.
- Primary actions should be placed in the lower 50% of the screen for reachability (Thumb Zone).

**Thumb Zone (One-Handed Use):**
- **Easy to reach**: Bottom third of screen
- **Moderate**: Middle third
- **Hard to reach**: Top third (reserve for non-critical actions or back navigation)

### Spacing System

Use a consistent spacing scale based on 8pt grid:

| Token | Value | Use Case |
|-------|-------|----------|
| `.xxs` | 4pt | Icon-to-text spacing |
| `.xs` | 8pt | Tight element spacing |
| `.sm` | 12pt | Related content groups |
| `.md` | 16pt | Default padding |
| `.lg` | 24pt | Section separation |
| `.xl` | 32pt | Major content blocks |
| `.xxl` | 48pt | Screen-level separation |

**Never use arbitrary values** like `padding(13)`. Always use the spacing scale.

### List Item Heights

- **Standard row**: 44pt minimum (text + padding)
- **Subtitle row**: 60pt minimum (two lines + padding)
- **Image thumbnail row**: 76pt minimum (60pt image + 8pt padding each side)

### Modal Presentation

- **Sheet detents**: Use `.medium()` for half-height sheets, `.large()` for full-height.
- **Bottom sheets**: Must have a 20pt grab handle at the top for discoverability.
- **Full screen modals**: Include a close button in the top-right or swipe-down gesture.

## Accessibility Constraints

- All touch targets must scale with Dynamic Type (never fixed sizes).
- Increase spacing between interactive elements when text size > .large.
- Use `.accessibilityElement(children: .combine)` for grouped content.

## Critical Violations to Avoid

❌ **NEVER DO:**
- `Button(...).frame(width: 30, height: 30)` — Too small to tap
- `VStack { }.padding(.top, 50)` — Hardcoded top spacing ignores safe area
- `Text("Tap here").foregroundColor(.blue)` — Looks interactive but isn't a button

✅ **ALWAYS DO:**
- Use `.frame(minHeight: 44)` for all interactive elements
- Use `.safeAreaInset()` or respect `.edgesIgnoringSafeArea()` intentionally
- Wrap text with `Button` if it should be interactive
