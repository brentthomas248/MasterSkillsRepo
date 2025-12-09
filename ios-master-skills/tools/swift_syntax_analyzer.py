#!/usr/bin/env python3
"""
Swift Syntax Analyzer - MCP Server
Analyzes Swift code for common HIG violations and architecture issues.

This tool is invoked by Google Antigravity via the MCP protocol.
"""

import sys
import json
import re
from typing import List, Dict, Any


class SwiftAnalyzer:
    """Analyzes Swift code for HIG compliance and architecture issues."""

    def __init__(self, code: str):
        self.code = code
        self.violations = []

    def analyze(self) -> List[Dict[str, Any]]:
        """Run all analysis checks and return violations."""
        self.check_hardcoded_frame_sizes()
        self.check_hardcoded_colors()
        self.check_hardcoded_fonts()
        self.check_force_unwrapping()
        self.check_touch_target_sizes()
        self.check_viewmodel_state_enum()
        self.check_accessibility_labels()
        return self.violations

    def add_violation(self, severity: str, rule: str, message: str, line: int = None):
        """Add a violation to the list."""
        violation = {
            "severity": severity,
            "rule": rule,
            "message": message,
        }
        if line is not None:
            violation["line"] = line
        self.violations.append(violation)

    def check_hardcoded_frame_sizes(self):
        """Check for hardcoded frame sizes instead of semantic tokens."""
        # Match .frame(width: 100) or .frame(height: 50) patterns
        patterns = [
            (r'\.frame\(width:\s*(\d+)\)', "Hardcoded frame width"),
            (r'\.frame\(height:\s*(\d+)\)', "Hardcoded frame height"),
        ]

        for pattern, description in patterns:
            matches = re.finditer(pattern, self.code)
            for match in matches:
                size = match.group(1)
                line_num = self.code[:match.start()].count('\n') + 1
                self.add_violation(
                    severity="warning",
                    rule="hardcoded_frame_size",
                    message=f"{description}: {size}pt. Consider using minWidth/minHeight or semantic tokens.",
                    line=line_num
                )

    def check_hardcoded_colors(self):
        """Check for hardcoded RGB colors instead of semantic colors."""
        # Match Color(red:, Color(.sRGB, red:, etc.
        patterns = [
            r'Color\(red:\s*[\d.]+',
            r'Color\(\.sRGB,\s*red:',
            r'Color\(hue:\s*[\d.]+',
            r'UIColor\(red:\s*[\d.]+',
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, self.code)
            for match in matches:
                line_num = self.code[:match.start()].count('\n') + 1
                self.add_violation(
                    severity="warning",
                    rule="hardcoded_color",
                    message="Hardcoded RGB/HSB color. Use semantic colors (e.g., .primary, .systemBackground) or Asset Catalog colors.",
                    line=line_num
                )

    def check_hardcoded_fonts(self):
        """Check for hardcoded font sizes instead of semantic text styles."""
        # Match .font(.system(size: 18)) patterns
        pattern = r'\.font\(\.system\(size:\s*(\d+)\)'
        matches = re.finditer(pattern, self.code)

        for match in matches:
            size = match.group(1)
            line_num = self.code[:match.start()].count('\n') + 1
            self.add_violation(
                severity="warning",
                rule="hardcoded_font_size",
                message=f"Hardcoded font size: {size}pt. Use semantic text styles (e.g., .body, .headline) for Dynamic Type support.",
                line=line_num
            )

    def check_force_unwrapping(self):
        """Check for force unwrapping operators."""
        # Match force unwrap (!) but not force try (try!)
        pattern = r'(?<!try)!\s*(?![=])'
        matches = re.finditer(pattern, self.code)

        for match in matches:
            # Skip if it's part of a comment
            line_start = self.code.rfind('\n', 0, match.start()) + 1
            line_end = self.code.find('\n', match.start())
            line = self.code[line_start:line_end] if line_end != -1 else self.code[line_start:]

            if '//' in line and line.index('//') < (match.start() - line_start):
                continue  # It's in a comment

            line_num = self.code[:match.start()].count('\n') + 1
            self.add_violation(
                severity="error",
                rule="force_unwrapping",
                message="Force unwrapping (!) can cause crashes. Use optional binding (if let, guard let) or nil coalescing (??) instead.",
                line=line_num
            )

    def check_touch_target_sizes(self):
        """Check for buttons/interactive elements that might be too small."""
        # Look for buttons with explicit frame sizes less than 44pt
        pattern = r'Button\(.*?\)\s*\{[\s\S]*?\}[\s\S]*?\.frame\(.*?(?:width|height):\s*(\d+)\)'
        matches = re.finditer(pattern, self.code, re.MULTILINE)

        for match in matches:
            size = int(match.group(1))
            if size < 44:
                line_num = self.code[:match.start()].count('\n') + 1
                self.add_violation(
                    severity="error",
                    rule="touch_target_too_small",
                    message=f"Touch target size is {size}pt, which is below the minimum 44pt. Use .frame(minWidth: 44, minHeight: 44) or add .contentShape(Rectangle()).",
                    line=line_num
                )

    def check_viewmodel_state_enum(self):
        """Check if ViewModels have a State enum defined."""
        # Check if this is a ViewModel class
        viewmodel_pattern = r'class\s+\w+ViewModel'
        if not re.search(viewmodel_pattern, self.code):
            return  # Not a ViewModel file

        # Check for State enum
        state_enum_pattern = r'enum\s+State\s*\{'
        if not re.search(state_enum_pattern, self.code):
            self.add_violation(
                severity="warning",
                rule="missing_viewmodel_state",
                message="ViewModel should expose a State enum (e.g., idle, loading, content, error) for state management.",
            )

    def check_accessibility_labels(self):
        """Check if interactive elements have accessibility labels."""
        # Look for Buttons without .accessibilityLabel
        button_pattern = r'Button\([^)]*\)\s*\{[\s\S]*?\}(?![\s\S]*?\.accessibilityLabel)'

        # Find all Button declarations
        button_matches = list(re.finditer(r'Button\(', self.code))

        for match in button_matches:
            # Find the closing brace for this button
            start = match.start()
            brace_count = 0
            in_button = False
            button_end = start

            for i in range(start, len(self.code)):
                if self.code[i] == '{':
                    brace_count += 1
                    in_button = True
                elif self.code[i] == '}':
                    brace_count -= 1
                    if in_button and brace_count == 0:
                        button_end = i
                        break

            # Check if there's an accessibility label within the next 200 characters
            snippet = self.code[start:min(button_end + 200, len(self.code))]

            # Skip if button has text label (Image-only buttons need labels)
            if 'Image(' in snippet and '.accessibilityLabel' not in snippet:
                line_num = self.code[:match.start()].count('\n') + 1
                self.add_violation(
                    severity="warning",
                    rule="missing_accessibility_label",
                    message="Image-only button should have .accessibilityLabel() for VoiceOver support.",
                    line=line_num
                )


def analyze_swift_code(code: str) -> Dict[str, Any]:
    """Main entry point for Swift code analysis."""
    analyzer = SwiftAnalyzer(code)
    violations = analyzer.analyze()

    return {
        "status": "success",
        "violations": violations,
        "summary": {
            "total": len(violations),
            "errors": len([v for v in violations if v["severity"] == "error"]),
            "warnings": len([v for v in violations if v["severity"] == "warning"]),
        }
    }


def main():
    """MCP Server main entry point."""
    # Read input from stdin (MCP protocol)
    try:
        input_data = sys.stdin.read()
        request = json.loads(input_data)

        # Extract Swift code from request
        code = request.get("code", "")

        if not code:
            result = {
                "status": "error",
                "message": "No Swift code provided for analysis."
            }
        else:
            result = analyze_swift_code(code)

        # Output result as JSON (MCP protocol)
        print(json.dumps(result, indent=2))

    except json.JSONDecodeError as e:
        error_result = {
            "status": "error",
            "message": f"Invalid JSON input: {str(e)}"
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)

    except Exception as e:
        error_result = {
            "status": "error",
            "message": f"Analysis failed: {str(e)}"
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
