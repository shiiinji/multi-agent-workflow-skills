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
planner-workflow → qa-design-workflow（任意） → execute-workflow → summary-workflow
                                                      ↑
                                                    今ここ
```

## ワークフロー

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Plan Reader │ ──▶ │ Test Writer │ ──▶ │ Implementer │ ──▶ │  Verifier   │ ──▶ │  Inspector  │
│ (計画読込)   │     │ (テスト作成) │     │ (実装)       │     │ (自動検証)   │     │ (外部検査)   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                          │
                    qa-design なし
                          │
                          ▼
                       スキップ
```

## フェーズ説明

| Phase | 名前 | 内容 |
|-------|------|------|
| 1 | Plan Reader | 計画書読込、qa-design 有無確認 |
| 2 | Test Writer | テスト作成（qa-design があれば） |
| 3 | Implementer | 実装 |
| 4 | Verifier | 自動テスト検証 |
| 5 | Inspector | 外部検査（別LLMレビュー） |

## 使用例

```bash
# qa-design ありの場合（テスト込み）
/shin-planner ユーザー認証機能を追加したい
/shin-qa-design ./docs/{topic}/plan.md
/shin-execute ./docs/{topic}/plan.md

# qa-design なしの場合（テストなし）
/shin-planner UIコンポーネントを追加したい
/shin-execute ./docs/{topic}/plan.md
```

## 動作パターン

### qa-design あり

```
Plan Reader → Test Writer → Implementer → Verifier → Inspector → 完了
                                 ↑            │
                                 └── 失敗 ────┘ (最大3回)
```

### qa-design なし

```
Plan Reader → Implementer → Verifier → Inspector → 完了
                   ↑                       │
                   └────── 問題あり ───────┘ (最大3回)
```

## 出力

```
./docs/{topic}/impl.md  # 検査用実装サマリー
```
