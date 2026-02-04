# shin-execute

計画書に基づいて実装を行い、自動検証と外部検査で品質を担保するワークフロー。

## 概要

| 項目 | 内容 |
|------|------|
| 対象ツール | Claude Code / Codex |
| 用途 | テスト作成→実装→自動検証→外部検査 |
| 入力 | 計画書ファイル |
| 出力 | 実装コード（＋テスト） |

## 位置づけ

```
planner-workflow → qa-design-workflow → execute-workflow → summary-workflow
                                                      ↑
                                                    今ここ
```

## ワークフロー

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Plan Reader │ ──▶ │ Test Writer │ ──▶ │ Implementer │ ──▶ │  Verifier   │ ──▶ │  Inspector  │
│ (計画読込)   │     │ (テスト作成) │     │ (実装)       │     │ (自動検証)   │     │ (外部検査)   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘

※ `qa-design.md` がない場合は、先に `/shin-qa-design ./docs/{topic}/plan.md` を実行してから進みます
```

## フェーズ説明

| Phase | 名前 | 内容 |
|-------|------|------|
| 1 | Plan Reader | 計画書読込、qa-design 読込 |
| 2 | Test Writer | テスト作成（qa-design に基づく） |
| 3 | Implementer | 実装 |
| 4 | Verifier | 自動テスト検証 |
| 5 | Inspector | 外部検査（別LLMレビュー） |

## 使用例

```bash
/shin-planner ユーザー認証機能を追加したい
/shin-qa-design ./docs/{topic}/plan.md
/shin-execute ./docs/{topic}/plan.md
/shin-summary ./docs/{topic}/plan.md --all
```

## 動作パターン

```
Plan Reader → Test Writer → Implementer → Verifier → Inspector → 完了
                                 ↑            │
                                 └── 失敗 ────┘ (最大3回)
```

## 出力

```
./docs/{topic}/impl.md  # 検査用実装サマリー
```

## Inspector（外部検査）の注意

- `impl.md` はレビュー入力として使うため、`/shin-*` のスラッシュコマンドは入れない
- 外部検査（codex/claude）はコマンド実行し、出力を `./docs/{topic}/reviews/` に保存して取り込む
