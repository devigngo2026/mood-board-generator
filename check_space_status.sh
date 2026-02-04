#!/bin/bash

# Hugging Face Space 状态检查脚本

SPACE_URL="https://huggingface.co/spaces/alanie/mbg"

echo "🔍 检查 Hugging Face Space 状态"
echo "=================================="
echo ""
echo "Space: alanie/mbg"
echo "URL: $SPACE_URL"
echo ""

# 检查 Space 是否可访问
echo "📡 检查连接..."
if curl -s --head "$SPACE_URL" | head -n 1 | grep "200" > /dev/null; then
    echo "✅ Space 可访问"
else
    echo "❌ Space 无法访问"
fi

echo ""
echo "🌐 请在浏览器中打开以下链接："
echo ""
echo "1. Space 主页:"
echo "   $SPACE_URL"
echo ""
echo "2. 查看日志:"
echo "   点击页面右上角 ⋮ → View logs"
echo ""
echo "3. Space 设置:"
echo "   $SPACE_URL/settings"
echo ""

# 检查状态的提示
echo "📊 检查状态指示器:"
echo ""
echo "  🟢 Running    = 应用正常运行 ✅"
echo "  🟡 Building   = 正在构建 ⏳"
echo "  🔴 Error      = 运行错误 ❌"
echo "  ⚪ Sleeping   = 休眠中 💤"
echo ""

echo "🎯 如果看到错误，请："
echo "  1. 点击 ⋮ → View logs"
echo "  2. 复制错误信息"
echo "  3. 告诉我具体的错误"
echo ""

# 提供获取日志的命令
echo "💻 使用 API 获取日志（需要 Token）:"
echo ""
echo "# 1. 获取 Token:"
echo "   https://huggingface.co/settings/tokens"
echo ""
echo "# 2. 设置 Token:"
echo "   export HF_TOKEN='your_token_here'"
echo ""
echo "# 3. 查看运行日志:"
echo "   curl -N -H \"Authorization: Bearer \$HF_TOKEN\" \\"
echo "     \"https://huggingface.co/api/spaces/alanie/mbg/logs/run\""
echo ""
echo "# 4. 查看构建日志:"
echo "   curl -N -H \"Authorization: Bearer \$HF_TOKEN\" \\"
echo "     \"https://huggingface.co/api/spaces/alanie/mbg/logs/build\""
echo ""

echo "=================================="
echo "✨ 打开浏览器查看 Space 状态吧！"
echo "=================================="
