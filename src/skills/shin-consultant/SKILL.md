---
name: shin-consultant
description: 3者合議システム。メイン（実装者）、Claude（設計者）、Codex（品質者）の3つの観点から分析し、多数決で判定する。This skill should be used when you need multiple perspectives on a technical decision, architecture choice, or implementation approach.
metadata:
  short-description: 3-way consultation system
---

# Multi Agent Consultant Workflow

3者合議システム - 異なる観点から分析し多数決で判定する。

## 概要

```
┌─────────────────────────────────────────────────────────────────┐
│                   consultant-workflow                           │
│                   (3者合議システム)                              │
└──────────────────────────┬──────────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │  IMPL    │    │  ARCH    │    │   QA     │
    │ (実装者)  │    │ (設計者)  │    │ (品質者)  │
    │  メイン   │    │  Claude  │    │  Codex   │
    └──────────┘    └──────────┘    └──────────┘
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                    ┌──────────────┐
                    │   COUNCIL    │
                    │  (集約・判定) │
                    └──────────────┘
```

## 3つの観点

| 役割 | コード | 観点 | 実行方法 |
|------|--------|------|----------|
| 実装者 | IMPL | 実装可能性、工数、技術的難易度 | このセッション |
| 設計者 | ARCH | アーキテクチャ、設計パターン、拡張性 | 別 Claude Code |
| 品質者 | QA | テスト容易性、品質、リスク、保守性 | 別 Codex |

## 入力

**相談事項:**
```bash
# 技術的な決定事項
/shin-consultant "Redux vs Zustand どちらを採用すべき？"

# アーキテクチャの相談
/shin-consultant "マイクロサービスに分割すべきか？"

# 実装方針の相談
/shin-consultant "この機能の実装アプローチについて相談したい: [詳細]"
```

## Workflow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    IMPL     │ ──▶ │    ARCH     │ ──▶ │     QA      │ ──▶ │   COUNCIL   │
│ (メイン分析) │     │ (外部Claude) │     │ (外部Codex) │     │ (集約・判定) │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

## Phase 1: IMPL（実装者分析）

このセッションで実装者の観点から分析する。

**分析観点:**
- 実装の難易度
- 必要な工数
- 技術的なリスク
- 既存コードとの整合性
- 依存関係

**出力フォーマット:**
```markdown
## IMPL（実装者）の分析

### 判定
`[IMPL:APPROVE]` / `[IMPL:REJECT]` / `[IMPL:CONDITIONAL]`

### 分析

#### 実装難易度
- [高/中/低]: [理由]

#### 工数見積もり
- [概算]

#### 技術的リスク
- [リスク項目]

#### 既存コードとの整合性
- [整合性の評価]

### 理由
[判定の理由]

### 条件（CONDITIONALの場合）
- [条件1]
- [条件2]
```

## Phase 2: ARCH（設計者分析）

別の Claude Code セッションで設計者の観点から分析を取得する。

**取得方法:**
```markdown
## 外部分析依頼（ARCH）

以下のコマンドで設計者の観点を取得してください:

\`\`\`bash
claude "
あなたは ARCH（設計者）です。以下の相談事項について、アーキテクチャ・設計の観点から分析してください。

## 相談事項
[相談内容]

## IMPL（実装者）の分析
[Phase 1 の出力]

## 分析観点
- アーキテクチャの適切性
- 設計パターン
- 拡張性・柔軟性
- 技術的負債
- ベストプラクティスとの整合性

## 出力ルール（重要）
- セクションごとに必ず内容を書く（空欄禁止）
- 「...」や「TBD」や「[各観点からの分析]」などのプレースホルダ禁止
- 箇条書きは「項目: 内容」形式で、コロンの後に必ず1文以上を書く
- 不明な場合は「不明」と明記し、その理由も1文添える

## 出力フォーマット
### 判定
\`[ARCH:APPROVE]\` / \`[ARCH:REJECT]\` / \`[ARCH:CONDITIONAL]\`

### 分析
- アーキテクチャの適切性:
- 設計パターン:
- 拡張性・柔軟性:
- 技術的負債:
- ベストプラクティスとの整合性:

### 理由
- 主理由:
- 補足:

"
\`\`\`

結果をこのセッションに貼り付けてください。
```

## Phase 3: QA（品質者分析）

別の Codex セッションで品質者の観点から分析を取得する。

**取得方法:**
```markdown
## 外部分析依頼（QA）

以下のコマンドで品質者の観点を取得してください:

\`\`\`bash
codex "
あなたは QA（品質者）です。以下の相談事項について、品質・テストの観点から分析してください。

## 相談事項
[相談内容]

## これまでの分析
### IMPL（実装者）
[Phase 1 の出力]

### ARCH（設計者）
[Phase 2 の出力]

## 分析観点
- テスト容易性
- 品質リスク
- 保守性
- 運用性
- セキュリティ

## 出力ルール（重要）
- セクションごとに必ず内容を書く（空欄禁止）
- 「...」や「TBD」や「[各観点からの分析]」などのプレースホルダ禁止
- 箇条書きは「項目: 内容」形式で、コロンの後に必ず1文以上を書く
- 不明な場合は「不明」と明記し、その理由も1文添える

## 出力フォーマット
### 判定
\`[QA:APPROVE]\` / \`[QA:REJECT]\` / \`[QA:CONDITIONAL]\`

### 分析
- テスト容易性:
- 品質リスク:
- 保守性:
- 運用性:
- セキュリティ:

### 理由
- 主理由:
- 補足:

"
\`\`\`

結果をこのセッションに貼り付けてください。
```

## Phase 4: COUNCIL（集約・判定）

3者の分析を集約し、最終判定を行う。

**集計ルール:**

| 条件 | 最終判定 |
|------|----------|
| 2票以上 APPROVE | `[COUNCIL:APPROVE]` |
| 2票以上 REJECT | `[COUNCIL:REJECT]` |
| それ以外 | `[COUNCIL:CONDITIONAL]` |

**出力フォーマット:**
```markdown
## 合議結果

### 各者の判定

| 役割 | 判定 | 主な理由 |
|------|------|----------|
| IMPL（実装者） | [判定] | [理由要約] |
| ARCH（設計者） | [判定] | [理由要約] |
| QA（品質者） | [判定] | [理由要約] |

### 最終判定

**`[COUNCIL:APPROVE]`** / **`[COUNCIL:REJECT]`** / **`[COUNCIL:CONDITIONAL]`**

### 判定理由

[3者の意見を総合した判定理由]

### 推奨アクション

1. [アクション1]
2. [アクション2]
3. [アクション3]

### 条件・注意事項（該当する場合）

- [条件1]
- [条件2]

---

### 詳細分析（参照用）

<details>
<summary>IMPL（実装者）の詳細</summary>

[Phase 1 の全文]

</details>

<details>
<summary>ARCH（設計者）の詳細</summary>

[Phase 2 の全文]

</details>

<details>
<summary>QA（品質者）の詳細</summary>

[Phase 3 の全文]

</details>
```

## 使用例

### 例1: 技術選定

```
ユーザー: /shin-consultant "状態管理ライブラリ: Redux vs Zustand vs Jotai"

Phase 1 (IMPL):
[IMPL:CONDITIONAL]
- Zustand が実装難易度は最も低い
- 条件: 複雑な状態遷移がなければ Zustand を推奨

Phase 2 (ARCH):
[ARCH:APPROVE] for Zustand
- シンプルなアーキテクチャ
- 拡張性も十分

Phase 3 (QA):
[QA:APPROVE] for Zustand
- テストが書きやすい
- 学習コストが低い

COUNCIL:
[COUNCIL:APPROVE] - Zustand を採用
```

### 例2: アーキテクチャ決定

```
ユーザー: /shin-consultant "モノリスを維持 vs マイクロサービス化"

Phase 1 (IMPL):
[IMPL:REJECT] for マイクロサービス化
- 現状のチーム規模では運用負荷が高い

Phase 2 (ARCH):
[ARCH:CONDITIONAL]
- 将来的には分割が必要だが、今はモジュラーモノリスを推奨

Phase 3 (QA):
[QA:REJECT] for マイクロサービス化
- テスト環境の複雑化
- 運用コストの増加

COUNCIL:
[COUNCIL:REJECT] - マイクロサービス化は時期尚早
推奨: モジュラーモノリスで境界を明確にする
```

## 判定タグ一覧

| フェーズ | APPROVE | REJECT | CONDITIONAL |
|---------|---------|--------|-------------|
| IMPL | `[IMPL:APPROVE]` | `[IMPL:REJECT]` | `[IMPL:CONDITIONAL]` |
| ARCH | `[ARCH:APPROVE]` | `[ARCH:REJECT]` | `[ARCH:CONDITIONAL]` |
| QA | `[QA:APPROVE]` | `[QA:REJECT]` | `[QA:CONDITIONAL]` |
| COUNCIL | `[COUNCIL:APPROVE]` | `[COUNCIL:REJECT]` | `[COUNCIL:CONDITIONAL]` |

## 典型的なフロー

```
/shin-consultant [相談事項]
    ↓
Phase 1: IMPL（このセッションで分析）
    ↓
Phase 2: ARCH（別 Claude で分析取得）
    ↓ ユーザーが結果を貼り付け
Phase 3: QA（別 Codex で分析取得）
    ↓ ユーザーが結果を貼り付け
Phase 4: COUNCIL（集約・最終判定）
    ↓
完了！
```

## ワークフロー全体での位置づけ

```
orchestrator
    │
    ├─ planner → qa-design → execute → summary
    │
    └─ consultant ← 技術的な意思決定が必要な時に呼び出し
```

計画立案中や実装中に技術的な判断が必要な場合、consultant-workflow を呼び出して3者合議で決定できる。
