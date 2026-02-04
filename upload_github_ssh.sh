#!/bin/bash

# GitHub SSH 上传脚本
# 使用方法: ./upload_github_ssh.sh

echo "🚀 Mood Board Generator - GitHub SSH 上传"
echo "=========================================="
echo ""

# 从 SSH 测试中获取 GitHub 用户名
GITHUB_USERNAME="devigngo2026"
REPO_NAME="mood-board-generator"

echo "📝 配置信息："
echo "  GitHub 用户名: $GITHUB_USERNAME"
echo "  仓库名称: $REPO_NAME"
echo "  认证方式: SSH Key ✅"
echo ""

# 检查是否在正确的目录
if [ ! -f "app.py" ]; then
    echo "❌ 错误：请在项目根目录运行此脚本"
    exit 1
fi

# 测试 SSH 连接
echo "🔐 测试 SSH 连接到 GitHub..."
if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
    echo "✅ SSH 连接成功！"
else
    echo "❌ SSH 连接失败"
    echo ""
    echo "请确保："
    echo "  1. SSH Key 已添加到 GitHub"
    echo "  2. 访问 https://github.com/settings/keys 检查"
    echo ""
    exit 1
fi

echo ""

# 检查是否已经有远程仓库
if git remote get-url origin > /dev/null 2>&1; then
    CURRENT_URL=$(git remote get-url origin)
    echo "⚠️  已存在远程仓库: $CURRENT_URL"
    echo ""
    read -p "是否要更新为 SSH URL？(y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git remote set-url origin "git@github.com:$GITHUB_USERNAME/$REPO_NAME.git"
        echo "✅ 远程仓库已更新为 SSH URL"
    fi
else
    # 添加远程仓库（SSH URL）
    echo "📡 添加远程仓库（SSH）..."
    git remote add origin "git@github.com:$GITHUB_USERNAME/$REPO_NAME.git"
    echo "✅ 远程仓库已添加"
fi

echo ""
echo "🔍 当前远程仓库："
git remote -v

echo ""
echo "📤 准备推送到 GitHub..."
echo ""
echo "⚠️  重要提示："
echo "  1. 请确保你已在 GitHub 上创建了仓库："
echo "     https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo ""
echo "  2. 使用 SSH 认证，无需输入密码！"
echo ""

read -p "是否继续推送？(y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🚀 推送到 GitHub..."
    git branch -M main
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "=========================================="
        echo "✅ 成功上传到 GitHub！"
        echo "=========================================="
        echo ""
        echo "📍 仓库地址："
        echo "  https://github.com/$GITHUB_USERNAME/$REPO_NAME"
        echo ""
        echo "🎯 下一步："
        echo "  1. 访问你的 GitHub 仓库"
        echo "  2. 添加 Topics: gradio, ai, mood-board, python"
        echo "  3. 设置仓库描述"
        echo "  4. 部署到 Hugging Face Spaces"
        echo ""
        echo "🔗 快速链接："
        echo "  仓库: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
        echo "  设置: https://github.com/$GITHUB_USERNAME/$REPO_NAME/settings"
        echo ""
    else
        echo ""
        echo "=========================================="
        echo "❌ 推送失败"
        echo "=========================================="
        echo ""
        echo "可能的原因："
        echo "  1. 仓库未在 GitHub 上创建"
        echo "  2. 仓库名称不匹配"
        echo "  3. 网络连接问题"
        echo ""
        echo "请检查错误信息并重试"
        echo ""
    fi
else
    echo ""
    echo "❌ 已取消推送"
    echo ""
    echo "你可以稍后手动推送："
    echo "  git push -u origin main"
    echo ""
fi
