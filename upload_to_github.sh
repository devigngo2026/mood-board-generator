#!/bin/bash

# GitHub 上传脚本
# 使用方法: ./upload_to_github.sh YOUR_GITHUB_USERNAME

echo "🚀 Mood Board Generator - GitHub 上传脚本"
echo "=========================================="
echo ""

# 检查是否提供了用户名
if [ -z "$1" ]; then
    echo "❌ 错误：请提供你的 GitHub 用户名"
    echo ""
    echo "使用方法："
    echo "  ./upload_to_github.sh YOUR_GITHUB_USERNAME"
    echo ""
    echo "例如："
    echo "  ./upload_to_github.sh moyinleung"
    echo ""
    exit 1
fi

GITHUB_USERNAME=$1
REPO_NAME="mood-board-generator"

echo "📝 配置信息："
echo "  GitHub 用户名: $GITHUB_USERNAME"
echo "  仓库名称: $REPO_NAME"
echo ""

# 检查是否在正确的目录
if [ ! -f "app.py" ]; then
    echo "❌ 错误：请在项目根目录运行此脚本"
    exit 1
fi

# 检查是否已经有远程仓库
if git remote get-url origin > /dev/null 2>&1; then
    echo "⚠️  警告：已存在远程仓库"
    echo "当前远程仓库: $(git remote get-url origin)"
    echo ""
    read -p "是否要更新远程仓库地址？(y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git remote set-url origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
        echo "✅ 远程仓库地址已更新"
    fi
else
    # 添加远程仓库
    echo "📡 添加远程仓库..."
    git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    echo "✅ 远程仓库已添加"
fi

echo ""
echo "🔍 检查 Git 状态..."
git status

echo ""
echo "📤 准备推送到 GitHub..."
echo ""
echo "⚠️  重要提示："
echo "  1. 请确保你已在 GitHub 上创建了仓库："
echo "     https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo ""
echo "  2. 推送时需要输入："
echo "     - Username: $GITHUB_USERNAME"
echo "     - Password: Personal Access Token (不是密码！)"
echo ""
echo "  3. 如何获取 Personal Access Token："
echo "     访问: https://github.com/settings/tokens"
echo "     点击 'Generate new token (classic)'"
echo "     勾选 'repo' 权限"
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
        echo "  2. 添加 Topics 和描述"
        echo "  3. 部署到 Hugging Face Spaces"
        echo ""
    else
        echo ""
        echo "=========================================="
        echo "❌ 推送失败"
        echo "=========================================="
        echo ""
        echo "可能的原因："
        echo "  1. 仓库未在 GitHub 上创建"
        echo "  2. Personal Access Token 错误"
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
