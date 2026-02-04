#!/bin/bash

# Mood Board Generator - Quick Start Script
# 快速启动脚本

echo "🎨 Mood Board Generator - Starting..."
echo "=================================="
echo ""

# 检查是否在正确的目录
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found!"
    echo "Please run this script from the mood_board_generator directory"
    exit 1
fi

# 检查依赖
echo "📦 Checking dependencies..."
if ! python3 -c "import gradio" 2>/dev/null; then
    echo "⚠️  Gradio not found. Installing dependencies..."
    pip3 install -r requirements.txt
else
    echo "✅ Dependencies OK"
fi

echo ""
echo "🚀 Starting Gradio app..."
echo "=================================="
echo ""
echo "📱 Open your browser to: http://localhost:7860"
echo "⌨️  Press Ctrl+C to stop the server"
echo ""

# 启动应用
python3 app.py
