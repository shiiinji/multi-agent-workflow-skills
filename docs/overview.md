# Multi-Agent Workflow Skills

マルチエージェントワークフローを実現するスキル群。Claude Code と Codex の両方で使用可能。

## 概要

複数のAIエージェントを協調させて、タスクを確実に遂行するためのスキルセット。

## クイックスタート

**迷ったらこれ:**
```bash
/shin-orchestrator [やりたいこと]
```

オーケストレーターが状況を分析し、最適なワークフローを推奨します。

## 全体フロー

```
┌─────────────────────────────────────────────────────────────────┐
│                   orchestrator-workflow                         │
│                   (エントリーポイント・推奨提示)                  │
└──────────────────────────┬──────────────────────────────────────┘
                           │ 推奨
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                   planner-workflow                              │
│                   (計画書を出力)                                 │
└──────────────────────────┬──────────────────────────────────────┘
                           │ 計画書ファイル
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                   qa-design-workflow（任意）                     │
│                   (テスト設計書を出力)                           │
└──────────────────────────┬──────────────────────────────────────┘
                           │ テスト設計書ファイル
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                   execute-workflow                              │
│                   (テスト→実装→自動検証→外部検査)                │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                   summary-workflow（任意）                       │
│                   (振り返りレポート・学習コンテンツ)              │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                         完了                                    │
└─────────────────────────────────────────────────────────────────┘

         ┌─────────────────────────────────────┐
         │         reviewer-workflow           │
         │         (随時呼び出し)               │
         │                                     │
         │  ← 全ワークフローから呼び出し可能    │
         │  ← 人から直接呼び出し可能            │
         └─────────────────────────────────────┘

         ┌─────────────────────────────────────┐
         │        consultant-workflow          │
         │        (3者合議システム)             │
         │                                     │
         │  IMPL(実装者) + ARCH(設計者) + QA   │
         │  ← 技術的な意思決定が必要な時       │
         └─────────────────────────────────────┘

         ┌─────────────────────────────────────┐
         │         learner-workflow            │
         │        (コードベース学習)            │
         │                                     │
         │  Explorer → Architect → Educator   │
         │  ← 既存コードを理解したい時         │
         └─────────────────────────────────────┘
```

## スキル一覧

| スキル名 | 役割 | 入力 | 出力 |
|---------|------|------|------|
| **orchestrator** | **上位管理・推奨提示** | タスク/状況 | 推奨ワークフロー |
| planner | 計画立案 | タスク説明 | 計画書ファイル |
| qa-design | テスト設計 | 計画書ファイル | テスト設計書ファイル |
| execute | 実装（テスト+実装+検証+検査） | 計画書ファイル | 実装 |
| reviewer | レビュー | 計画書/設計書/実装/エラー | フィードバック |
| summary | 振り返り・学習コンテンツ | 計画書ファイル | レポート/コンテンツ |
| **consultant** | **3者合議（技術相談）** | 相談事項 | 合議判定・推奨 |
| **learner** | **コードベース学習** | プロジェクトパス | 学習コンテンツ |
| sequence-diagram | シーケンス図生成（User/Frontend/Backend/DB） | フロー説明/API仕様 | Mermaid シーケンス図 |

## 典型的なフロー

### パターン A: オーケストレーター主導（推奨）

```bash
# 1. タスクを投げる
/shin-orchestrator ユーザー認証機能を追加したい
# → planner を推奨

# 2. 推奨に従う
/shin-planner ユーザー認証機能を追加したい

# 3. 次を確認
/shin-orchestrator 次は？
# → qa-design or execute を推奨

# 4. 推奨に従う
/shin-qa-design ./docs/{topic}/plan.md

# ...繰り返し
```

### パターン B: フル QA フロー

```bash
/shin-planner ユーザー認証機能を追加したい
/shin-qa-design ./docs/{topic}/plan.md
/shin-execute ./docs/{topic}/plan.md
```

### パターン C: シンプルフロー（テストなし）

```bash
/shin-planner UIコンポーネントを追加したい
/shin-execute ./docs/{topic}/plan.md
```

### パターン D: 振り返り・学習コンテンツ作成

```bash
/shin-planner ユーザー認証機能を追加したい
/shin-execute ./docs/{topic}/plan.md
/shin-summary ./docs/{topic}/plan.md --all
```

### パターン E: レビューのみ

```bash
/shin-reviewer "このコードをレビューして: src/auth.ts"
```

### パターン F: 技術相談（3者合議）

```bash
/shin-consultant "Redux vs Zustand どちらを採用すべき？"
```

### パターン G: コードベース学習

```bash
/shin-learner /Users/shiiinji/code/example-repo
```

## インストール

```bash
./install.sh
```

これにより、`~/.claude/skills/` と `~/.codex/skills/` にシンボリックリンクが作成されます。

## 詳細ドキュメント

- [shin-orchestrator](./shin-orchestrator.md) - 上位管理（エントリーポイント）
- [shin-planner](./shin-planner.md) - 計画立案
- [shin-qa-design](./shin-qa-design.md) - テスト設計
- [shin-execute](./shin-execute.md) - 実装
- [shin-reviewer](./shin-reviewer.md) - レビュー
- [shin-summary](./shin-summary.md) - 振り返り・学習コンテンツ
- [shin-consultant](./shin-consultant.md) - 3者合議（技術相談）
- [shin-learner](./shin-learner.md) - コードベース学習

## ディレクトリ構造

```
multi-agent-workflow-skills/
├── docs/                              # 仕様書
│   ├── overview.md
│   ├── shin-orchestrator.md
│   ├── shin-planner.md
│   ├── shin-qa-design.md
│   ├── shin-execute.md
│   ├── shin-reviewer.md
│   ├── shin-summary.md
│   ├── shin-consultant.md
│   └── shin-learner.md
├── src/
│   └── skills/                        # 共通スキル（実装）
│       ├── shin-orchestrator/
│       │   └── SKILL.md
│       ├── shin-planner/
│       │   └── SKILL.md
│       ├── shin-qa-design/
│       │   └── SKILL.md
│       ├── shin-execute/
│       │   └── SKILL.md
│       ├── shin-reviewer/
│       │   └── SKILL.md
│       ├── shin-summary/
│       │   └── SKILL.md
│       ├── shin-consultant/
│       │   └── SKILL.md
│       └── shin-learner/
│           └── SKILL.md
└── install.sh                         # インストールスクリプト
```
