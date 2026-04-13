#!/bin/bash

# BotFinanzas GitHub Setup Script
# This script initializes a Git repository and pushes to GitHub

echo "🚀 Setting up BotFinanzas GitHub repository..."

# Initialize git repository
git init

# Add all files
git add .

# Initial commit
git commit -m "Initial commit: BotFinanzas v0.1 - Automated Trading Bot with ML"

# Add remote origin (replace with your actual GitHub repository URL)
echo "📝 Please create a repository on GitHub named 'botfinanzas' and then run:"
echo "git remote add origin https://github.com/yourusername/botfinanzas.git"
echo "git branch -M main"
echo "git push -u origin main"

echo ""
echo "✅ Git repository initialized successfully!"
echo ""
echo "Next steps:"
echo "1. Create a new repository on GitHub: https://github.com/new"
echo "2. Name it 'botfinanzas'"
echo "3. Don't initialize with README (we already have one)"
echo "4. Copy the repository URL"
echo "5. Run the commands shown above with your actual repository URL"
echo ""
echo "🔧 Optional: Set up GitHub CLI for easier management:"
echo "brew install gh"
echo "gh auth login"
echo "gh repo create botfinanzas --public --source=. --remote=origin --push"
