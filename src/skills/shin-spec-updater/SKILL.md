---
name: shin-spec-updater
description: 実装後に「仕様書/計画書/./docs/{topic}/impl.md（検査用実装サマリー）/SKILL.md」と最新コードが乖離したときに、最新コード（git diff/実装結果）とチャットログ（llm-threads 等）から仕様書を更新して整合させるワークフロー。Use when the spec needs to be updated to match the latest code and post-implementation decisions captured in chat history.
metadata:
  short-description: Update spec from code + chat
---

# Spec Updater Workflow

実装後に発生しがちな「仕様のドリフト（spec drift）」を、**コードを根拠（source of truth）**として仕様書へ反映し直す。

## 入力

- 更新対象のパス（ファイル/ディレクトリ）
  - 推奨: `./docs/{topic}/`（配下の既存ドキュメントをまとめて整合）
  - 例: `./docs/{topic}/spec.md` / `./docs/{topic}/plan.md` / `./docs/{topic}/impl.md`（検査用実装サマリー）/ `src/skills/{skill}/SKILL.md`
- 対象コードベースのルートパス（省略時: `cwd`）
- （任意）チャットログのパス（例: `~/Documents/llm-threads/.../*.md`）

## パス規約（このリポジトリの標準）

- `./docs/{topic}/plan.md` - 計画書
- `./docs/{topic}/qa-design.md` - テスト設計書
- `./docs/{topic}/impl.md` - 検査用実装サマリー（外部検査/レビュー入力の前提）
- `./docs/{topic}/retrospective.md` - 振り返り
- `./docs/{topic}/learning.md` - 学習コンテンツ

## 出力

- 更新済みの仕様書（最小差分で反映）
- 仕様ドリフトの一覧（「何が」「なぜ」変わったか）
- 未確定事項（要確認リスト）

## 方針（重要）

- **コード優先**: 仕様が曖昧/矛盾する場合は、現行コードの挙動に合わせて spec を更新する（ただし意図が不明なら要確認に落とす）。
- **根拠を残す**: 仕様書に「根拠（どのコード/どのスレッド/どの日時）」を残す。
- **捏造しない**: 推測で仕様を断定しない。判断材料が足りない点は必ず「要確認」に出す。
- **最小差分**: 既存の章立てを尊重し、必要な箇所だけ更新する。

## 使い方（例）

```bash
/shin-spec-updater ./docs/chematels-jsonld-spec/impl.md --codebase /Users/shiiinji/projects/happylogue-jp/chematels --thread /Users/shiiinji/Documents/llm-threads/llms/Codex/chematels/Threads/2026/02/03/chematels-jsonld-spec_*.md
```

## Workflow

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌─────────────┐
│  Collector  │ ──▶ │ Drift Finder │ ──▶ │   Editor    │ ──▶ │  Verifier   │
│ (根拠収集)   │     │ (差分特定)    │     │ (仕様更新)   │     │ (整合確認)   │
└─────────────┘     └──────────────┘     └─────────────┘     └─────────────┘
```

## Phase 1: Collector（根拠収集）

1. `./docs/{topic}/` の既存ドキュメントを確認する（まず「何が存在するか」）
   - `plan.md` / `qa-design.md` / `impl.md` / `retrospective.md` / `learning.md` / `spec.md` など
   - ドキュメント間の整合（同じ用語/前提/出力パス/制約）が崩れていないかを先に見る
2. 更新対象の仕様書を読む（章立て/主張/依存する前提を把握する）
3. コード側の根拠を集める
   - `git status` / `git diff` / `git log -n 20`
   - 関連ファイルの実装（機能の入口、公開 API、設定、型、テスト）
4. チャットログがあれば、意思決定・追加指示を抽出する
   - まず `src/skills/shin-spec-updater/scripts/thread_digest.py` を実行してダイジェストを作る

### チャットログのダイジェスト作成（任意）

```bash
python3 src/skills/shin-spec-updater/scripts/thread_digest.py /path/to/thread.md
python3 src/skills/shin-spec-updater/scripts/thread_digest.py /path/to/thread.md --json
```

## Phase 2: Drift Finder（差分特定）

仕様書と現行コードを突き合わせ、差分を「観測可能な事実」として列挙する。

- 仕様書にあるが、コードに無い（未実装/削除）
- コードにあるが、仕様書に無い（追記漏れ）
- 仕様書とコードの挙動が食い違う（変更/解釈違い）

出力は次の粒度でまとめる:

- 差分（1行）
- 根拠（ファイルパス/関数名/テスト名/スレッド日時）
- 影響範囲（ユーザー影響・互換性・運用影響）
- 対応方針（spec を直す/コードを直す/要確認）

## Phase 3: Editor（仕様更新）

更新は「追記/修正/削除」を最小限に留め、次を必ず含める:

### 仕様書メタ情報（推奨）

仕様書の先頭に以下を追加（既にあれば更新）:

```markdown
## メタ情報
- 最終更新: YYYY-MM-DD HH:MM:SS (TZ)
- 根拠: git commit / 参照スレッド（thread_id など）
```

### 変更サマリ（推奨）

```markdown
## 変更サマリ
- [追加] ...
- [変更] ...
- [削除] ...
```

### 要確認（必須）

不確実な点や仕様決定が必要な点は、必ず残す:

```markdown
## 要確認
- [ ] ...
```

## Phase 4: Verifier（整合確認）

1. 仕様書に書いた内容がコードで再現できることを確認する（README 的に追えるか）
2. 可能ならテスト/型チェックを実行して、仕様更新が「現実（コード）」とズレていないか確認する
3. 仕様更新後に残った差分（意図的な差分）を「要確認」に集約する
