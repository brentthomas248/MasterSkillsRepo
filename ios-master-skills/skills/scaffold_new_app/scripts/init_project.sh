#!/bin/bash
#
# iOS Project Structure Initialization Script
# Usage: bash init_project.sh [AppName]
#
# This script creates the "Golden Path" folder structure for a new iOS app.

set -e  # Exit on error

APP_NAME="$1"

if [ -z "$APP_NAME" ]; then
    echo "Error: App name is required."
    echo "Usage: bash init_project.sh [AppName]"
    exit 1
fi

echo "🚀 Scaffolding iOS project: $APP_NAME"
echo ""

# Create root directory (optional, usually run inside existing project)
# mkdir -p "$APP_NAME"
# cd "$APP_NAME"

# Create App folder
echo "📁 Creating Sources/App..."
mkdir -p "Sources/App"

# Create Features folder
echo "📁 Creating Sources/Features..."
mkdir -p "Sources/Features"

# Create Shared/DesignSystem structure
echo "📁 Creating Sources/Shared/DesignSystem..."
mkdir -p "Sources/Shared/DesignSystem/Components/Buttons"
mkdir -p "Sources/Shared/DesignSystem/Components/Cards"
mkdir -p "Sources/Shared/DesignSystem/Components/TextFields"
mkdir -p "Sources/Shared/DesignSystem/Tokens"
mkdir -p "Sources/Shared/Extensions"
mkdir -p "Sources/Shared/Utilities"
mkdir -p "Sources/Shared/Resources"

echo ""
echo "✅ Project structure created successfully!"
echo ""
echo "📂 Structure:"
echo "   Sources/"
echo "   ├── App/"
echo "   ├── Features/"
echo "   └── Shared/"
echo "       ├── DesignSystem/"
echo "       │   ├── Components/"
echo "       │   │   ├── Buttons/"
echo "       │   │   ├── Cards/"
echo "       │   │   └── TextFields/"
echo "       │   └── Tokens/"
echo "       ├── Extensions/"
echo "       ├── Utilities/"
echo "       └── Resources/"
echo ""
echo "🎯 Next steps:"
echo "   1. Add your app entry point to Sources/App/"
echo "   2. Create feature folders in Sources/Features/"
echo "   3. Install SwiftLint configuration"
echo ""
