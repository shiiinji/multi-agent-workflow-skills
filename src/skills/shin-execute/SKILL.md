---
name: shin-execute
description: 計画書を入力として受け取り、テスト作成→実装→自動検証→外部検査のワークフローを実行する。qa-design-workflow のテスト設計書に基づいてテストも作成する。This skill should be used after planner-workflow to implement the plan.
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
│ qa-design-workflow  │
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
                                              │                   │
                                              │ テスト失敗        │ 問題あり
                                              │ → 再実装          │ → 修正
                                              ▼                   ▼
                                          (最大3回)            (最大3回)
```

## Phase 1: Plan Reader（計画読込）

計画書を読み込み、実装対象と qa-design を確認する。

**実行内容:**
1. 計画書ファイルを読み込む
2. 計画書と同じディレクトリの `qa-design.md` があるか確認
3. 実装ステップをリスト化

**確認パターン:**
```
qa-design.md が存在するか？
├─ YES → Phase 2 (Test Writer) へ
└─ NO  → 先に qa-design-workflow を実行して中断
```

**計画書がない場合の案内:**
```markdown
計画書が見つかりません。先に計画を作成してください:

\`\`\`bash
/shin-planner [タスクの説明]
\`\`\`
```

## Phase 2: Test Writer（テスト作成）

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

qa-design.md が見つかりません。先にテスト設計を作成してください:

\`\`\`bash
/shin-qa-design ./docs/{topic}/plan.md
\`\`\`

完了後、もう一度 `/shin-execute` を実行してください。
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
# テスト実行
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

外部LLM（codex/claude）に実装結果をレビューさせ、指摘を取り込んで仕上げる。

**実装結果の保存:**
実装完了後、変更内容を一時ファイルに保存（検査用）:
```
./docs/{topic}/impl.md
```

**impl.md の注意:**
- このファイルは **レビュー入力** として使うため、`/shin-*` のスラッシュコマンドは書かない（外部検査コマンドはこのセッション側に置く）
- 「何を・なぜ・どう変えたか」「どう検証したか」を短くまとめる（貼り付けやすさ優先）

**impl.md の最小テンプレ（例）:**
```markdown
# 実装サマリー

## 達成したこと
- ...

## レビューで見てほしい点
- ...
```

**外部検査の実行（ファイルに保存）:**
```bash
mkdir -p ./docs/{topic}/reviews

codex "/shin-reviewer $(cat ./docs/{topic}/impl.md)" > ./docs/{topic}/reviews/codex.md
claude "/shin-reviewer $(cat ./docs/{topic}/impl.md)" > ./docs/{topic}/reviews/claude.md
```

このフェーズでは **上記コマンドを実際に実行** し、`./docs/{topic}/reviews/*.md` を **このセッションで読み込み**、指摘を反映する（省略しない）。

**完了条件（Inspector）:**
- `./docs/{topic}/reviews/codex.md` が存在する
- `./docs/{topic}/reviews/claude.md` が存在する
- 上記 2ファイルを読み込み、指摘対応が完了している

**検査項目:**
1. 成功条件がすべて満たされているか
2. コードの品質（可読性、パターン遵守）
3. エッジケースの考慮
4. 型安全性（TypeScript の場合）
5. テストの網羅性

**検査結果による分岐:**
- codex/claude の指摘に問題あり → Phase 3 に戻り修正（**最大3回まで**）
- 両方OK → 完了報告
- 3回修正後も問題 → ユーザーに判断を委ねる

## 完了報告

すべてのフェーズが完了したら:

```markdown
## 実装完了報告

### 達成したこと
- [実装内容の要約]

### 外部検査
- codex: OK（`./docs/{topic}/reviews/codex.md`）
- claude: OK（`./docs/{topic}/reviews/claude.md`）

### 計画書のステータス
- 完了: Step 1, 2, 3
- スキップ: なし

---

### 次のステップ

振り返り・学習コンテンツを作成する:
\`\`\`bash
/shin-summary ./docs/{topic}/plan.md
\`\`\`
```

## フロー全体図

```
Plan Reader → Test Writer → Implementer → Verifier → Inspector → 完了
                                   ↑            │
                                   └── 失敗 ────┘ (最大3回)
```
