# shin-spec-updater

実装後に仕様書/計画書/`./docs/{topic}/impl.md`（検査用実装サマリー）などが最新コードと乖離したときに、**最新コード（source of truth）**と、可能なら **チャットログ（llm-threads 等）**から仕様書を更新して整合させるワークフロー。

## 概要

| 項目 | 内容 |
|------|------|
| 対象ツール | Claude Code / Codex |
| 用途 | 仕様ドリフト（spec drift）の解消 |
| 入力 | 仕様書パス +（任意）スレッドログ |
| 出力 | 更新済み仕様書 + 差分一覧 + 要確認 |

## 使いどころ

- 実装後に「追加指示/レビュー指摘」を反映したが、仕様書が更新されていない
- コードが先行して、仕様書が追従できていない
- `plan.md`/`./docs/{topic}/impl.md`/`SKILL.md` など複数のドキュメント間で整合が取れていない

## 使用例

```bash
/shin-spec-updater ./docs/{topic}/impl.md --codebase /path/to/repo --thread /path/to/thread.md
```

## まず確認すること（推奨）

- `./docs/{topic}/` 配下の既存ドキュメント（`plan.md` / `qa-design.md` / `impl.md` / `retrospective.md` / `learning.md` / `spec.md`）を確認して、どこがドリフトしているか当たりを付ける

## チャットログのダイジェスト（任意）

スレッドログから「最新のユーザー指示」「最新の実装サマリ」「参照パス」を抜き出して、仕様更新の材料にする。

```bash
python3 src/skills/shin-spec-updater/scripts/thread_digest.py /path/to/thread.md
python3 src/skills/shin-spec-updater/scripts/thread_digest.py /path/to/thread.md --json
```

## ワークフロー

```
Collector（根拠収集） → Drift Finder（差分特定） → Editor（仕様更新） → Verifier（整合確認）
```
