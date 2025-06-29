#!/bin/bash

echo "🔧 TorTrack Environment Setup"
echo "============================"
echo ""

# Check if .env already exists
if [ -f ".env" ]; then
    echo "⚠️  .env file already exists in root directory."
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Keeping existing .env file."
    else
        cp env.example .env
        echo "✅ Created new .env from template"
    fi
else
    cp env.example .env
    echo "✅ Created .env from template"
fi

# Check backend .env
if [ -f "backend/.env" ]; then
    echo "⚠️  .env file already exists in backend directory."
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Keeping existing backend/.env file."
    else
        cp backend/env.example backend/.env
        echo "✅ Created new backend/.env from template"
    fi
else
    cp backend/env.example backend/.env
    echo "✅ Created backend/.env from template"
fi

echo ""
echo "📝 Next steps:"
echo "1. Edit .env and add your API keys"
echo "2. Edit backend/.env for local development"
echo "3. See API_KEYS.md for instructions on getting API keys"
echo ""
echo "🚀 Then run: docker-compose up -d" 