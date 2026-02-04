# Multi-Agent Workflow Skills

Claude Code / Codex 向けのマルチエージェントワークフロースキル集。複数のAIエージェントを協調させて、計画から実装、検証、振り返りまで一貫した開発フローを実現します。

## 特徴

- **計画駆動**: 詳細な計画書を作成し、外部レビューを経て実装
- **品質重視**: テスト設計 → 実装 → 自動検証 → 外部検査の多段階フロー
- **3者合議**: 実装者・設計者・品質者の3視点から技術的意思決定
- **学習支援**: コードベース理解と振り返りレポートの自動生成

## インストール

```bash
./install.sh
```

スキルが `~/.claude/skills/` と `~/.codex/skills/` にシンボリックリンクされます。

## ワークフロー全体図

```
orchestrator（エントリーポイント / --auto）
       │
       ▼
   planner（計画書作成）
       │
       ▼
  qa-design（テスト設計）
       │
       ▼
   execute（実装・検証）
       │
       ▼
   summary（振り返り）

補助:
  reviewer  ← 各フェーズからレビュー依頼
  consultant ← 技術的意思決定時に3者合議
  repo-analyzer ← リポジトリ解析（コードベース理解）
```

## スキル一覧

| スキル | 説明 | 使用例 |
|--------|------|--------|
| `/shin-orchestrator` | タスク分析・最適ワークフロー推奨 | `/shin-orchestrator ユーザー認証を追加したい` |
| `/shin-planner` | 計画書作成（外部レビュー付き） | `/shin-planner ユーザー認証を追加したい` |
| `/shin-qa-design` | テスト戦略設計 | `/shin-qa-design ./docs/{topic}/plan.md` |
| `/shin-execute` | 実装・検証・検査 | `/shin-execute ./docs/{topic}/plan.md` |
| `/shin-reviewer` | レビュー・フィードバック | `/shin-reviewer $(cat ./docs/{topic}/plan.md)` |
| `/shin-consultant` | 3者合議による意思決定 | `/shin-consultant "Redux vs Zustand?"` |
| `/shin-repo-analyzer` | リポジトリ解析（コードベース理解） | `/shin-repo-analyzer /path/to/project` |
| `/shin-sequence-diagram` | ユーザー/フロント/バックエンド/DB のフローをシーケンス図（Mermaid）にする | `/shin-sequence-diagram ログインの流れを図にして` |
| `/shin-summary` | 振り返り・学習コンテンツ作成 | `/shin-summary ./docs/{topic}/plan.md --all` |
| `/shin-spec-updater` | 仕様書の更新（最新コード + チャットログから整合） | `/shin-spec-updater ./docs/{topic}/impl.md --thread /path/to/thread.md` |

## 典型的なフロー

### フル品質フロー

```bash
/shin-orchestrator ユーザー認証を追加したい
# → planner を推奨

/shin-planner ユーザー認証を追加したい
# → ./docs/user-auth/plan.md 出力

/shin-qa-design ./docs/user-auth/plan.md
# → ./docs/user-auth/qa-design.md 出力

/shin-execute ./docs/user-auth/plan.md
# → テスト作成 → 実装 → 検証 → 検査

/shin-summary ./docs/user-auth/plan.md --all
# → 振り返りレポート & 学習コンテンツ出力
```

### auto-mode（人の介入なし）

```bash
/shin-orchestrator --auto UIコンポーネントを追加したい
```

### 技術相談

```bash
/shin-consultant "マイクロサービスに分割すべきか？"
# → IMPL/ARCH/QA の3視点で分析 → 多数決で判定
```

### リポジトリ解析（コードベース理解）

```bash
/shin-repo-analyzer /path/to/open-source-project --focus "認証の仕組み"
# → 学習コンテンツ出力
```

## 出力ファイル

各ワークフローは `./docs/{topic}/` 以下にファイルを出力します。

| ファイル | 出力元 |
|----------|--------|
| `plan.md` | planner |
| `qa-design.md` | qa-design |
| `impl.md` | execute |
| `retrospective.md` | summary --retrospective |
| `learning.md` | summary --learning |
| `repo-analyzer.md` | repo-analyzer |

## ディレクトリ構造

```
multi-agent-workflow-skills/
├── install.sh           # インストールスクリプト
├── docs/                # 仕様書
│   ├── overview.md
│   └── shin-*.md
└── src/skills/          # スキル実装
    └── shin-*/
        └── SKILL.md
```

## ライセンス

MIT
