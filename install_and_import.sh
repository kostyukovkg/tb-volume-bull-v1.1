#!/bin/bash

# Transfer logs to bot.log
exec > >(tee -a logs/bot.log) 2>&1

# Check python version
PYTHON_CMD=python3.10

if ! command -v $PYTHON_CMD &> /dev/null
then
    echo "❌ Python is not installed"
    exit 1
fi

# Create venv, if does not exist
if [ ! -d "venv" ]; then
    echo "🔧 Create venv..."
    $PYTHON_CMD -m venv venv
fi

# Activate venv
source venv/bin/activate || { echo "❌ Could not activate venv"; exit 1; }

# Install requirements, if not yet
if [ ! -f "venv/.requirements_installed" ]; then
    echo "📦 Installing requirements..."
    pip install --upgrade pip
    pip install -r requirements.txt
    touch venv/.requirements_installed
fi

# Check .env
if [ ! -f ".env" ]; then
    echo "⚠️ File .env not found."
    echo "Create .env based on .env.example"
    cp .env.example .env
    echo "✅ Template .env created. Type your API keys!"
    exit 1
fi

# Start bot
echo "🚀 Start bot..."
$PYTHON_CMD main.py