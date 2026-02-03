---
name: shin-summary
description: 実装結果から振り返りレポートや学習コンテンツを作成するワークフロー。--retrospective で振り返り、--learning で学習コンテンツ、--all で両方を出力。This skill should be used after completing implementation to create documentation, learning materials, or retrospective reports.
metadata:
  short-description: Summary & learning content generator
---

# Multi Agent Summary Workflow

実装結果から振り返りレポートや学習コンテンツを作成するワークフロー。

## 役割

```
tdd-workflow / execute-workflow
              │
              │ 実装完了
              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   summary-workflow                              │
│                                                                 │
│  --retrospective: 振り返りレポート                               │
│  --learning: 学習コンテンツ                                      │
│  --all: 両方出力                                                 │
└─────────────────────────────────────────────────────────────────┘
              │
              ▼
         ドキュメント出力
```

## 入力

**計画書ファイル + モード指定:**
```bash
# 振り返りレポート
/shin-summary ./docs/{topic}/plan.md --retrospective

# 学習コンテンツ
/shin-summary ./docs/{topic}/plan.md --learning

# 両方出力
/shin-summary ./docs/{topic}/plan.md --all

# デフォルト（--all と同じ）
/shin-summary ./docs/{topic}/plan.md
```

## Workflow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Collector  │ ──▶ │  Analyzer   │ ──▶ │   Writer    │ ──▶ │   Review    │
│ (情報収集)   │     │ (要点抽出)   │     │ (コンテンツ作成)│     │ (外部レビュー)│
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

## Phase 1: Collector（情報収集）

計画書と実装結果を収集する。

**収集項目:**
1. 計画書の内容（ゴール、スコープ、アーキテクチャ）
2. 実装されたファイル一覧
3. テスト結果（あれば）
4. 変更の差分（git diff）

**実行内容:**
```bash
# 計画書を読み込む
Read: [計画書ファイル]

# 実装されたファイルを確認
git diff --name-only [base branch]

# 変更内容を確認
git diff [base branch]

# テスト結果を確認（あれば）
```

## Phase 2: Analyzer（要点抽出）

収集した情報から要点を抽出する。

**振り返りレポート用:**
- 何を実装したか（What）
- なぜその方法を選んだか（Why）
- どう実装したか（How）
- 課題・困った点
- 改善点・次回への学び

**学習コンテンツ用:**
- 技術的なポイント
- 理解すべき概念
- コードの解説ポイント
- よくある落とし穴
- ベストプラクティス

## Phase 3: Writer（コンテンツ作成）

モードに応じてコンテンツを作成する。

### --retrospective: 振り返りレポート

**出力ファイル:** `./docs/{topic}/retrospective.md`

**フォーマット:**
```markdown
# 振り返りレポート: [タスク名]

## 概要
- **期間:** [開始日] - [完了日]
- **計画書:** [計画書ファイルパス]

## 実装内容

### 何を実装したか
- [実装内容1]
- [実装内容2]

### 変更ファイル一覧
| ファイル | 変更内容 |
|---------|---------|
| src/xxx.ts | 新規作成: XXX機能 |
| src/yyy.ts | 修正: YYY処理 |

## 技術的な決定

### なぜその方法を選んだか
| 決定事項 | 選択肢 | 選んだ理由 |
|---------|-------|-----------|
| [決定1] | A, B, C | [理由] |

## 課題と学び

### 困った点・課題
1. [課題1]
   - 状況: ...
   - 解決方法: ...

### 次回への学び
1. [学び1]
2. [学び2]

## 改善点

### コードの改善点
- [ ] [改善項目1]
- [ ] [改善項目2]

### プロセスの改善点
- [ ] [改善項目1]

## 所感
[自由記述]
```

### --learning: 学習コンテンツ

**出力ファイル:** `./docs/{topic}/learning.md`

**フォーマット:**
```markdown
# 学習コンテンツ: [トピック名]

## はじめに

### この記事で学べること
- [学べること1]
- [学べること2]

### 前提知識
- [前提1]
- [前提2]

## 背景・概要

### 解決したい課題
[課題の説明]

### アプローチ
[採用したアプローチの説明]

## 実装解説

### アーキテクチャ
```
[図やダイアグラム]
```

### コア実装

#### [機能1の名前]

**目的:** [この部分が何をするか]

**コード:**
```typescript
// 重要な部分のコード抜粋
```

**解説:**
- [ポイント1]
- [ポイント2]

#### [機能2の名前]
...

## ポイント・Tips

### 押さえておくべきポイント
1. **[ポイント1]**: [説明]
2. **[ポイント2]**: [説明]

### よくある落とし穴
1. **[落とし穴1]**
   - 問題: [問題の説明]
   - 解決: [解決方法]

### ベストプラクティス
- [ベストプラクティス1]
- [ベストプラクティス2]

## まとめ

### 学んだこと
1. [まとめ1]
2. [まとめ2]

### 次のステップ
- [発展的なトピック1]
- [発展的なトピック2]

## 参考資料
- [リンク1]
- [リンク2]
```

## Phase 4: Review（外部レビュー）

作成したコンテンツを外部レビューに出す。

**レビュー観点:**
- 内容の正確性
- 説明のわかりやすさ
- 抜け漏れのチェック
- 読者目線での改善点

**実行方法（両方に実行）:**
```bash
codex "/shin-reviewer [出力ファイルパス] をレビューして"
claude "/shin-reviewer [出力ファイルパス] をレビューして"
```

## 出力

### --retrospective
```
./docs/{topic}/retrospective.md
```

### --learning
```
./docs/{topic}/learning.md
```

### --all（デフォルト）
```
./docs/{topic}/retrospective.md
./docs/{topic}/learning.md
```

## 使用例

### 例1: 実装後の振り返り

```
ユーザー: /shin-summary ./docs/plan-auth-20240115.md --retrospective

出力:
## Phase 1: Collector
計画書と実装結果を収集中...
- 計画書: ./docs/plan-auth-20240115.md
- 変更ファイル: 12件
- テスト: 全て PASS

## Phase 2: Analyzer
要点を抽出中...
- 実装内容: JWT認証、セッション管理、パスワードリセット
- 技術的決定: 3件
- 課題: 2件

## Phase 3: Writer
振り返りレポートを作成中...

## 出力
./docs/retrospective-20240115-143022.md

## Phase 4: Review
外部レビューを実行しますか？ (y/n)
```

### 例2: 学習コンテンツ作成

```
ユーザー: /shin-summary ./docs/plan-auth-20240115.md --learning

出力:
## Phase 1-2: 収集・分析
...

## Phase 3: Writer
学習コンテンツを作成中...
- トピック: JWT認証の実装方法
- 対象読者: 中級者
- ポイント: 5件

## 出力
./docs/learning-20240115-143522.md
```

## 典型的なフロー

```
/shin-planner [タスク]
    ↓
/shin-execute [plan]
    ↓
/shin-summary [plan] --all
    ↓
振り返りレポート + 学習コンテンツ
```

## ワークフロー全体での位置づけ

```
orchestrator → planner → qa-design → tdd/execute → summary
                                                      │
                                                      ↓
                                              ┌──────────────┐
                                              │ retrospective │
                                              │ learning      │
                                              └──────────────┘
                                                      │
                                              ← reviewer (任意)
```
