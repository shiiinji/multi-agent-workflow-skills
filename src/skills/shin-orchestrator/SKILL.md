---
name: shin-orchestrator
description: タスクを分析し、最適なワークフローを推奨する上位管理ワークフロー。各ワークフローの実行順序と現在のステータスを管理する。This skill should be used as the entry point for any development task to get guidance on which workflow to use.
metadata:
  short-description: Workflow orchestrator
---

# Multi Agent Orchestrator Workflow

タスクを分析し、最適なワークフローを推奨する上位管理ワークフロー。

**このワークフローがすべてのタスクのエントリーポイントとなる。**

## 役割

```
┌─────────────────────────────────────────────────────────────────┐
│                   orchestrator-workflow                         │
│                                                                 │
│  1. タスク分析                                                   │
│  2. 最適なワークフロー推奨                                        │
│  3. 進捗状況の把握                                               │
│  4. 次のステップ提示                                             │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ▼
                     ┌──────────┐
                     │ planner  │
                     └────┬─────┘
                          ▼
                     ┌──────────┐
                     │ qa-design│
                     └────┬─────┘
                          ▼
                     ┌──────────┐
                     │ execute  │
                     └────┬─────┘
                          ▼
                     ┌──────────┐
                     │ summary  │
                     └──────────┘

補助:
  reviewer  ← いつでもレビュー/トラブル対応
```

## 入力

**タスク説明または現在の状態:**
```bash
# 新規タスクの場合
/shin-orchestrator ユーザー認証機能を追加したい

# 進行中のタスクの場合
/shin-orchestrator 計画書を作成しました。次は何をすべき？

# ファイルを指定する場合
/shin-orchestrator ./docs/{topic}/plan.md の次のステップは？

# auto-mode（人の介入を挟まずに最後まで実行）
/shin-orchestrator --auto ユーザー認証機能を追加したい
```

## Mode

| モード | 挙動 |
|------|------|
| デフォルト | 推奨提示のみ（次に実行すべきワークフローとコマンドを出す） |
| `--auto` | planner → qa-design → execute → summary を**このセッションで連続実行**する（途中の人の介入なし） |

### auto-mode のルール

- 途中でユーザー入力を要求しない（不明点は仮定し、`plan.md` の「疑義事項・要確認」に記録する）
- 生成物は `./docs/{topic}/` に出力する（topic が未指定ならタスク名から推定する）
- 外部レビュー（別セッション）が必要な手順は、まず自己レビューで進め、必要なら最後に `/shin-reviewer` を提案する

## Workflow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Analyzer   │ ──▶ │  Selector   │ ──▶ │  Presenter  │
│ (状況分析)   │     │ (WF選択)    │     │ (推奨提示)   │
└─────────────┘     └─────────────┘     └─────────────┘
```

## Phase 1: Analyzer（状況分析）

現在の状況を分析する。

**分析項目:**
1. タスクの種類（新機能/バグ修正/リファクタ/レビュー）
2. 既存の成果物（計画書/テスト設計書/実装）
3. 現在のフェーズ

**状況判定:**
```
新規タスク
└─ planner-workflow

計画書あり → qa-design-workflow
テスト設計書あり → execute-workflow
実装完了 → summary-workflow

レビュー依頼 / 問題発生 → reviewer-workflow
```

## Phase 2: Selector（ワークフロー選択）

状況に応じた最適なワークフローを選択する。

**選択基準:**

| 状況 | 次に実行するワークフロー |
|------|-----------------|
| 何もない状態 | planner-workflow |
| 計画書がある | qa-design-workflow |
| テスト設計書がある | execute-workflow |
| 実装完了後 | summary-workflow |
| レビューしてほしい / 問題が発生した | reviewer-workflow（トラブルシューティング） |

## Phase 3: Presenter（推奨提示）

推奨するワークフローとコマンドを提示する。

**出力形式:**
```markdown
## 現在の状況

| 項目 | ステータス |
|------|-----------|
| 計画書 | ✅ あり / ❌ なし |
| テスト設計書 | ✅ あり / ❌ なし |
| 実装 | ✅ 完了 / 🔄 進行中 / ❌ 未着手 |
| 振り返り（summary） | ✅ 完了 / ❌ 未実施 |

## 推奨: [ワークフロー名]

**理由:** [なぜこのワークフローを推奨するか]

**実行コマンド:**
\`\`\`bash
/multi-agent-xxx-workflow [引数]
\`\`\`

---

## 全体の進捗

\`\`\`
[1] planner    ✅ 完了
[2] qa-design  🔄 次はここ
[3] execute    ⏳ 待機中
[4] summary    ⏳ 待機中
\`\`\`

## 他の選択肢

- `/shin-reviewer` - レビュー/トラブルシューティング
```

## 使用例

### 例1: 新規タスク

```
ユーザー: /shin-orchestrator ユーザー認証機能を追加したい

出力:
## 現在の状況
| 項目 | ステータス |
|------|-----------|
| 計画書 | ❌ なし |

## 推奨: planner-workflow

**理由:** まだ計画がないため、最初に計画を立てる必要があります。

**実行コマンド:**
\`\`\`bash
/shin-planner ユーザー認証機能を追加したい
\`\`\`
```

### 例2: 計画書がある状態

```
ユーザー: /shin-orchestrator ./docs/{topic}/plan.md の次は？

出力:
## 現在の状況
| 項目 | ステータス |
|------|-----------|
| 計画書 | ✅ あり |
| テスト設計書 | ❌ なし |

## 推奨: qa-design-workflow

**理由:** 計画書があります。品質を担保するため、テスト設計を推奨します。

**実行コマンド:**
\`\`\`bash
/shin-qa-design ./docs/{topic}/plan.md
\`\`\`
```

### 例3: 問題発生時

```
ユーザー: /shin-orchestrator テストが通らない

出力:
## 現在の状況
| 項目 | ステータス |
|------|-----------|
| 問題 | テストエラー |

## 推奨: reviewer-workflow

**理由:** テストが失敗している場合、外部レビューでトラブルシューティングが有効です。

**実行コマンド:**
\`\`\`bash
/shin-reviewer "テストが通りません: [エラー内容を貼り付け]"
\`\`\`
```

### 例4: auto-mode

```
ユーザー: /shin-orchestrator --auto ユーザー認証機能を追加したい

出力（要約）:
- plan.md を作成
- qa-design.md を作成
- テスト作成 → 実装 → 自動検証 → 検査
- retrospective.md / learning.md を作成（デフォルト: --all）
```

## ワークフロー一覧（リファレンス）

| ワークフロー | 用途 | 入力 |
|-------------|------|------|
| planner | 計画立案 | タスク説明 |
| qa-design | テスト設計 | 計画書ファイル |
| execute | 実装（テスト+実装+検証+検査） | 計画書ファイル |
| reviewer | レビュー | 任意のコンテンツ |
| summary | 振り返り・学習コンテンツ | 計画書ファイル |

## 典型的なフロー

```
/shin-orchestrator [タスク]
    ↓ 推奨: planner
/shin-planner [タスク]
    ↓
/shin-orchestrator 次は？
    ↓ 推奨: qa-design
/shin-qa-design [plan]
    ↓
/shin-execute [plan]
    ↓
/shin-summary [plan]
    ↓
完了！
```
