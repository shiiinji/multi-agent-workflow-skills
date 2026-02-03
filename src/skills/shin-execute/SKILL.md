---
name: shin-execute
description: 計画書を入力として受け取り、テスト作成→実装→自動検証→外部検査のワークフローを実行する。qa-design-workflow でテスト設計がある場合はテストも作成する。This skill should be used after planner-workflow to implement the plan.
metadata:
  short-description: Implementation with testing & inspection
---

# Multi Agent Execute Workflow

計画書に基づいて実装を行い、自動検証と外部検査で品質を担保するワークフロー。

**前提: planner-workflow で作成された計画書を入力として受け取る。**

## 全体フロー

```
┌─────────────────────┐
│  planner-workflow   │
│  (計画書を出力)      │
└──────────┬──────────┘
           │ 計画書ファイル
           ▼
┌─────────────────────┐
│ qa-design-workflow  │ （任意）
│ (テスト設計を出力)   │
└──────────┬──────────┘
           │ テスト設計書ファイル
           ▼
┌─────────────────────┐
│  execute-workflow   │ ← 今ここ
│  (テスト→実装→検証)  │
└─────────────────────┘
```

## 入力

**計画書ファイルパス（必須）:**
```bash
/shin-execute ./docs/{topic}/plan.md
```

計画書がない場合は、先に planner-workflow を実行するよう案内する。

## Workflow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Plan Reader │ ──▶ │ Test Writer │ ──▶ │ Implementer │ ──▶ │  Verifier   │ ──▶ │  Inspector  │
│ (計画読込)   │     │ (テスト作成) │     │ (実装)       │     │ (自動検証)   │     │ (外部検査)   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                          │                    │                   │
                          │ qa-design なし     │ テスト失敗        │ 問題あり
                          │ → スキップ         │ → 再実装          │ → 修正
                          ▼                    ▼                   ▼
                       Phase 3へ          (最大3回)            (最大3回)
```

## Phase 1: Plan Reader（計画読込）

計画書を読み込み、実装対象と qa-design の有無を確認する。

**実行内容:**
1. 計画書ファイルを読み込む
2. qa-design-workflow のテスト設計書があるか確認
3. 実装ステップをリスト化

**確認パターン:**
```
./docs/qa-design-*.md が存在するか？
├─ YES → Phase 2 (Test Writer) へ
└─ NO  → Phase 3 (Implementer) へ（テストなしで実装）
```

**計画書がない場合の案内:**
```markdown
計画書が見つかりません。先に計画を作成してください:

\`\`\`bash
/shin-planner [タスクの説明]
\`\`\`
```

## Phase 2: Test Writer（テスト作成）

**qa-design がある場合のみ実行。**

qa-design-workflow で作成されたテスト設計書に基づいてテストを作成する。

**実行内容:**
1. テスト設計書を読み込む
2. 設計書の各テストケースをコードに変換
3. テストファイルを作成
4. テストが **失敗する** ことを確認（実装がまだないため）

**テストの原則:**
- テスト設計書の内容を網羅
- Unit / Integration / E2E のレイヤーに従う
- 1テスト1アサーション を推奨

**qa-design がない場合:**
```markdown
## テスト設計書なし

qa-design-workflow が実行されていないため、テスト作成をスキップします。
テストを追加したい場合は:

\`\`\`bash
/shin-qa-design ./docs/{topic}/plan.md
\`\`\`

→ Phase 3 (Implementer) に進みます。
```

## Phase 3: Implementer（実装）

計画書に基づいて実装を行う。

**実行内容:**
1. 計画のステップを順番に実行
2. コード編集
3. 必要に応じてコマンド実行（ビルド等）
4. 各ステップ完了後に簡潔な進捗報告

**注意:**
- 計画から逸脱しない
- テストがある場合は、テストが通る最小限の実装を目指す
- 型安全性を確保

## Phase 4: Verifier（自動検証）

テストと型チェックを実行して実装を検証する。

**実行内容:**
```bash
# テスト実行（テストがある場合）
pnpm test -- path/to/__tests__/xxx.test.ts

# 型チェック（TypeScript の場合）
pnpm type:check

# Lint（設定がある場合）
pnpm lint
```

**検証結果による分岐:**
- 全て通過 → Phase 5 (Inspector) へ
- テスト失敗 → Phase 3 に戻り修正（**最大3回まで**）
- 3回失敗 → reviewer-workflow でレビューを依頼

**3回失敗時の案内:**
```markdown
自動検証が3回失敗しました。外部レビューを実行してください（両方）:

\`\`\`bash
codex "/shin-reviewer 実装がテストを通過しません。[エラー内容]"
claude "/shin-reviewer 実装がテストを通過しません。[エラー内容]"
\`\`\`
```

## Phase 5: Inspector（外部検査）

別セッションで実装結果を検査させる。

**実装結果の保存:**
実装完了後、変更内容を一時ファイルに保存（検査用）:
```
./docs/{topic}/impl.md
```

**検査依頼:**
```markdown
## 外部検査依頼

以下のコマンドで外部検査を実行してください（両方）:

\`\`\`bash
codex "/shin-reviewer $(cat ./docs/{topic}/impl.md)"
claude "/shin-reviewer $(cat ./docs/{topic}/impl.md)"
\`\`\`

両方の検査結果をこのセッションに貼り付けてください。
```

**検査項目:**
1. 成功条件がすべて満たされているか
2. コードの品質（可読性、パターン遵守）
3. エッジケースの考慮
4. 型安全性（TypeScript の場合）
5. テストの網羅性（qa-design がある場合）

**検査結果による分岐:**
- 問題なし → 完了報告
- 問題あり → Phase 3 に戻り修正（**最大3回まで**）
- 3回修正後も問題 → ユーザーに判断を委ねる

## 完了報告

すべてのフェーズが完了したら:

```markdown
## 実装完了報告

### 達成したこと
- [実装内容の要約]

### 変更ファイル
| ファイル | 変更内容 |
|---------|---------|
| src/xxx.ts | 新規作成: XXX機能 |
| src/__tests__/xxx.test.ts | テスト追加 |

### 検証結果
- テスト: X件 全て通過
- 型チェック: OK
- 外部検査: OK

### 計画書のステータス
- 完了: Step 1, 2, 3
- スキップ: なし

---

### 次のステップ（任意）

振り返り・学習コンテンツを作成する場合:
\`\`\`bash
/shin-summary ./docs/{topic}/plan.md
\`\`\`
```

## フロー全体図

```
qa-design あり:
  Plan Reader → Test Writer → Implementer → Verifier → Inspector → 完了
                                   ↑            │
                                   └── 失敗 ────┘ (最大3回)

qa-design なし:
  Plan Reader → Implementer → Verifier → Inspector → 完了
                     ↑                       │
                     └────── 問題あり ───────┘ (最大3回)
```
