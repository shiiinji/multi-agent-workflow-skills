#!/bin/bash

# Shin Workflow Skills Installer
# Creates symlinks to Claude Code and Codex skill directories

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="$SCRIPT_DIR/src/skills"

CLAUDE_SKILLS_DIR="$HOME/.claude/skills"
CODEX_SKILLS_DIR="$HOME/.codex/skills"

SKILLS=(
    "shin-orchestrator"
    "shin-planner"
    "shin-qa-design"
    "shin-execute"
    "shin-reviewer"
    "shin-summary"
    "shin-spec-updater"
    "shin-consultant"
    "shin-repo-analyzer"
    "shin-sequence-diagram"
)

# Old skills to remove
OLD_SKILLS=(
    "multi-agent-orchestrator-workflow"
    "multi-agent-planner-workflow"
    "multi-agent-qa-design-workflow"
    "multi-agent-tdd-workflow"
    "multi-agent-execute-workflow"
    "multi-agent-reviewer-workflow"
    "multi-agent-summary-workflow"
    "multi-agent-consultant-workflow"
    "multi-agent-learner-workflow"
    "shin-learner"
)

echo "🚀 Installing Shin Workflow Skills..."
echo ""

# Create skill directories if they don't exist
mkdir -p "$CLAUDE_SKILLS_DIR"
mkdir -p "$CODEX_SKILLS_DIR"

# Remove old symlinks
echo "🧹 Cleaning up old symlinks..."
for old_skill in "${OLD_SKILLS[@]}"; do
    if [ -L "$CLAUDE_SKILLS_DIR/$old_skill" ]; then
        rm "$CLAUDE_SKILLS_DIR/$old_skill"
        echo "   Removed: $CLAUDE_SKILLS_DIR/$old_skill"
    fi
    if [ -L "$CODEX_SKILLS_DIR/$old_skill" ]; then
        rm "$CODEX_SKILLS_DIR/$old_skill"
        echo "   Removed: $CODEX_SKILLS_DIR/$old_skill"
    fi
done
echo ""

for skill in "${SKILLS[@]}"; do
    echo "📦 Installing $skill..."

    # Claude Code
    if [ -L "$CLAUDE_SKILLS_DIR/$skill" ]; then
        echo "   Removing existing symlink: $CLAUDE_SKILLS_DIR/$skill"
        rm "$CLAUDE_SKILLS_DIR/$skill"
    elif [ -d "$CLAUDE_SKILLS_DIR/$skill" ]; then
        echo "   ⚠️  Directory exists (not a symlink): $CLAUDE_SKILLS_DIR/$skill"
        echo "   Backing up to $CLAUDE_SKILLS_DIR/$skill.bak"
        mv "$CLAUDE_SKILLS_DIR/$skill" "$CLAUDE_SKILLS_DIR/$skill.bak"
    fi
    ln -s "$SKILLS_SRC/$skill" "$CLAUDE_SKILLS_DIR/$skill"
    echo "   ✅ Claude Code: $CLAUDE_SKILLS_DIR/$skill -> $SKILLS_SRC/$skill"

    # Codex
    if [ -L "$CODEX_SKILLS_DIR/$skill" ]; then
        echo "   Removing existing symlink: $CODEX_SKILLS_DIR/$skill"
        rm "$CODEX_SKILLS_DIR/$skill"
    elif [ -d "$CODEX_SKILLS_DIR/$skill" ]; then
        echo "   ⚠️  Directory exists (not a symlink): $CODEX_SKILLS_DIR/$skill"
        echo "   Backing up to $CODEX_SKILLS_DIR/$skill.bak"
        mv "$CODEX_SKILLS_DIR/$skill" "$CODEX_SKILLS_DIR/$skill.bak"
    fi
    ln -s "$SKILLS_SRC/$skill" "$CODEX_SKILLS_DIR/$skill"
    echo "   ✅ Codex: $CODEX_SKILLS_DIR/$skill -> $SKILLS_SRC/$skill"

    echo ""
done

echo "✅ Installation complete!"
echo ""
echo "Usage:"
echo "  Claude Code / Codex:"
echo ""
echo "  エントリーポイント:"
echo "    /shin-orchestrator <task>    # 最適なワークフローを推奨"
echo ""
echo "  個別ワークフロー:"
echo "    /shin-planner <task>         # 計画立案"
echo "    /shin-qa-design <plan>       # QAテスト設計"
echo "    /shin-execute <plan>         # 実装（テスト+実装+検証+検査）"
echo "    /shin-reviewer <content>     # レビュー"
echo "    /shin-summary <plan>         # 振り返り・学習コンテンツ"
echo "    /shin-spec-updater <spec>    # 仕様書更新（コード + チャットログ）"
echo "    /shin-consultant <topic>     # 3者合議（技術相談）"
echo "    /shin-repo-analyzer <path>   # リポジトリ解析（コードベース理解）"
echo "    /shin-sequence-diagram <flow> # シーケンス図（User/FE/BE/DB）"
