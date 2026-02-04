---
name: shin-repo-analyzer
description: リポジトリ（コードベース）を解析して深く理解するためのワークフロー。構造分析→設計理解→概念解説→学習パス作成の4段階で、オープンソースやプロジェクトを「使う」だけでなく「理解する」ための解析・学習コンテンツを生成する。This skill should be used when you want to deeply analyze and understand a repository/codebase, not just use it.
metadata:
  short-description: Repository analysis & understanding
---

# Multi Agent Repo Analyzer Workflow

リポジトリ（コードベース）を解析して深く理解するためのワークフロー。

**目的: 「使う」だけでなく「理解する」**

## 概要

```
┌─────────────────────────────────────────────────────────────────┐
│                 repo-analyzer-workflow                           │
│                 (リポジトリ解析/理解)                            │
└──────────────────────────┬──────────────────────────────────────┘
                           │
    ┌──────────────────────┼──────────────────────────────────────┐
    ▼                      ▼                      ▼               ▼
┌─────────┐          ┌─────────┐          ┌─────────┐      ┌─────────┐
│Explorer │    →     │Architect│    →     │Educator │  →   │  Guide  │
│(構造分析)│          │(設計理解)│          │(概念解説)│      │(学習パス)│
└─────────┘          └─────────┘          └─────────┘      └─────────┘
```

## 入力

**プロジェクトパス:**
```bash
# ローカルプロジェクト
/shin-repo-analyzer /Users/shiiinji/code/example-repo

# 特定のモジュールに絞る
/shin-repo-analyzer /Users/shiiinji/code/example-repo/src/workflows

# 解析目的を指定
/shin-repo-analyzer /Users/shiiinji/code/example-repo --focus "ワークフローエンジンの仕組み"
```

## Workflow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Explorer   │ ──▶ │  Architect  │ ──▶ │  Educator   │ ──▶ │    Guide    │
│ (構造分析)   │     │ (設計理解)   │     │ (概念解説)   │     │ (学習パス)   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
      │                   │                   │                   │
      ▼                   ▼                   ▼                   ▼
  構造マップ          設計解説          学習コンテンツ        学習ガイド
```

## Phase 1: Explorer（構造分析）

プロジェクトの全体構造を把握する。

**分析項目:**
1. ディレクトリ構造
2. 主要ファイル・モジュール
3. 設定ファイル（package.json, tsconfig.json など）
4. エントリーポイント
5. 依存関係

**実行内容:**
```bash
# ディレクトリ構造を確認
tree -L 3 [project_path]

# 設定ファイルを読む
cat package.json
cat tsconfig.json
cat README.md

# 主要なファイルタイプを確認
find . -name "*.ts" | head -20
```

**出力形式:**
```markdown
## 構造マップ

### プロジェクト概要
- **名前:** [プロジェクト名]
- **種類:** [CLI / Web App / Library / etc.]
- **言語:** [TypeScript / JavaScript / etc.]
- **フレームワーク:** [Next.js / NestJS / etc.]

### ディレクトリ構造
\`\`\`
project/
├── src/           # ← ソースコード
│   ├── core/      # ← コアロジック
│   ├── utils/     # ← ユーティリティ
│   └── index.ts   # ← エントリーポイント
├── tests/         # ← テスト
└── package.json   # ← 設定
\`\`\`

### 主要ファイル
| ファイル | 役割 | 重要度 |
|---------|------|--------|
| src/index.ts | エントリーポイント | ⭐⭐⭐ |
| src/core/engine.ts | コアエンジン | ⭐⭐⭐ |

### 依存関係
| パッケージ | 用途 |
|-----------|------|
| typescript | 型システム |
| vitest | テスト |

### 初見での気づき
- [気づき1]
- [気づき2]
```

## Phase 2: Architect（設計理解）

アーキテクチャと設計パターンを理解する。

**分析項目:**
1. アーキテクチャパターン（MVC, Clean Architecture, etc.）
2. 設計パターン（Factory, Strategy, Observer, etc.）
3. データフロー
4. モジュール間の依存関係
5. 抽象化のレイヤー

**実行内容:**
- 主要なクラス/関数の定義を読む
- import/export の関係を追跡
- インターフェース/型定義を確認
- テストコードから意図を読み取る

**出力形式:**
```markdown
## 設計解説

### アーキテクチャ
\`\`\`
┌─────────────────────────────────────────┐
│              Application                │
├─────────────────────────────────────────┤
│   ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│   │ Module A│  │ Module B│  │ Module C│ │
│   └────┬────┘  └────┬────┘  └────┬────┘ │
│        │            │            │      │
│        └────────────┼────────────┘      │
│                     ▼                   │
│              ┌──────────┐               │
│              │   Core   │               │
│              └──────────┘               │
└─────────────────────────────────────────┘
\`\`\`

### 採用パターン
| パターン | 適用箇所 | 目的 |
|---------|---------|------|
| Factory | src/factory/ | オブジェクト生成の抽象化 |
| Strategy | src/strategies/ | アルゴリズムの切り替え |

### データフロー
\`\`\`
User Input → Parser → Validator → Processor → Output
\`\`\`

### レイヤー構成
1. **Presentation**: UI/CLI
2. **Application**: ユースケース
3. **Domain**: ビジネスロジック
4. **Infrastructure**: 外部連携

### 設計の意図（Why）
- [なぜこの構造なのか]
- [どんな問題を解決しているか]
```

## Phase 3: Educator（概念解説）

主要な概念とコアロジックを解説する。

**解説項目:**
1. コア概念の説明
2. 主要な処理フローの解説
3. 重要なコードの詳細解説
4. 「なぜそう書いているか」の解説

**出力形式:**
```markdown
## 学習コンテンツ

### コア概念

#### 概念1: [概念名]

**一言で:** [簡潔な説明]

**詳細:**
[詳しい説明]

**コード例:**
\`\`\`typescript
// このコードが何をしているか
function example() {
  // ポイント1: ...
  // ポイント2: ...
}
\`\`\`

**なぜこうなっているか:**
- [理由1]
- [理由2]

---

#### 概念2: [概念名]
...

### 処理フロー詳解

#### [フロー名]

\`\`\`
Step 1: [処理内容]
    ↓
Step 2: [処理内容]
    ↓
Step 3: [処理内容]
\`\`\`

**各ステップの解説:**

1. **Step 1**: [詳細解説]
   - ファイル: `src/xxx.ts:42`
   - 関数: `processInput()`

2. **Step 2**: ...

### 重要なコード解説

#### [ファイル名]: [関数/クラス名]

**役割:** [何をするコードか]

\`\`\`typescript
// 元のコード（簡略化）
export class Engine {
  // 1. 初期化処理
  constructor(config: Config) {
    this.config = config;  // ← 設定を保持
  }

  // 2. メイン処理
  async run(input: Input): Promise<Output> {
    const validated = this.validate(input);  // ← 入力検証
    const processed = this.process(validated);  // ← 処理実行
    return this.format(processed);  // ← 出力整形
  }
}
\`\`\`

**ポイント:**
- `validate()`: [何をしているか]
- `process()`: [何をしているか]
- `format()`: [何をしているか]

**学びのポイント:**
- [このコードから学べること]
```

## Phase 4: Guide（学習パス）

効率的な学習パスと深掘りポイントを提示する。

**出力形式:**
```markdown
## 学習ガイド

### 推奨学習パス

```
Level 1: 概要理解 (30分)
├─ README.md を読む
├─ ディレクトリ構造を把握
└─ エントリーポイントを確認

Level 2: 基本フロー理解 (1-2時間)
├─ メイン処理の流れを追う
├─ 主要なクラス/関数を読む
└─ サンプルコードを実行

Level 3: 詳細理解 (3-5時間)
├─ 各モジュールの役割を理解
├─ 設計パターンを把握
└─ テストコードを読む

Level 4: 応用 (継続的)
├─ 実際に使ってみる
├─ カスタマイズしてみる
└─ 貢献してみる
```

### 読むべきファイル（優先順）

| 順番 | ファイル | 理由 | 所要時間 |
|------|---------|------|----------|
| 1 | README.md | 全体像の把握 | 10分 |
| 2 | src/index.ts | エントリーポイント | 15分 |
| 3 | src/core/engine.ts | コアロジック | 30分 |
| 4 | src/types/index.ts | 型定義 | 20分 |
| 5 | tests/engine.test.ts | 使い方の例 | 20分 |

### 深掘りポイント

#### 理解を深めるための質問
1. **[質問1]**
   - 関連ファイル: `src/xxx.ts`
   - 調査方法: [具体的な調査手順]

2. **[質問2]**
   - 関連ファイル: `src/yyy.ts`
   - 調査方法: [具体的な調査手順]

#### 実験してみよう
1. **[実験1]**: [やってみること]
   ```bash
   # 実行コマンド
   ```

2. **[実験2]**: [やってみること]

### 関連技術・前提知識

| 技術 | 必要度 | 学習リソース |
|------|--------|-------------|
| TypeScript | 必須 | [リンク] |
| Node.js | 必須 | [リンク] |
| [パターン名] | 推奨 | [リンク] |

### よくある疑問と回答

**Q: [よくある質問1]**
A: [回答]

**Q: [よくある質問2]**
A: [回答]

---

### 次のステップ

学習完了後の推奨アクション:
1. [ ] 実際にプロジェクトを動かしてみる
2. [ ] 小さな変更を加えてみる
3. [ ] テストを追加してみる
4. [ ] ドキュメントを読み直す
```

## 出力ファイル

**保存先:**
```
./docs/{topic}/learning.md
```

**ルール（必須）**
- 出力は必ず上記パスに書き込む（チャット本文だけで終えない）
- `{topic}` はデフォルトで `basename(<project_path>)`（例: `/Users/.../example-repo` → `example-repo`）
- 書き込みできない場合は、勝手に別パス（例: `/tmp`）に出力せず、理由を説明してユーザーに確認する

**完了条件（Definition of Done）**
- `./docs/{topic}/learning.md` が存在し、最新の学習コンテンツが入っている
- 最終レスポンスに出力ファイルパスを明記する

## 使用例

### 例1: オープンソースプロジェクトの学習

```
ユーザー: /shin-repo-analyzer /Users/shiiinji/code/example-repo

Phase 1 (Explorer):
- YAML ベースのワークフローエンジン
- TypeScript で実装
- CLI + プログラマティック API

Phase 2 (Architect):
- Step-based architecture
- Agent pattern for LLM integration
- Plugin system for extensibility

Phase 3 (Educator):
- Workflow: ステップの集合
- Step: 個別の処理単位
- Agent: LLM とのインターフェース

Phase 4 (Guide):
1. README.md → 全体像
2. src/workflow.ts → コア処理
3. examples/ → 使用例
```

### 例2: 特定モジュールの深掘り

```
ユーザー: /shin-repo-analyzer /Users/shiiinji/code/example-repo/src/agents --focus "エージェントの仕組み"

→ エージェントモジュールに特化した学習コンテンツを生成
```

## ワークフロー全体での位置づけ

```
orchestrator
    │
    ├─ planner → execute → summary
    │
    ├─ reviewer
    │
    ├─ consultant
    │
    └─ repo-analyzer ← 既存コードを理解したい時
```

**使い分け:**
- 新規実装: planner → execute
- 既存コード理解: **repo-analyzer**
- 技術相談: consultant
- レビュー: reviewer
