# idol-p-agent

`bonsai` 配下の `idol` / `idol-*` リポジトリを横断して把握し、既存データと実装を根拠に、次の研究・開発・統合候補を提案するプロジェクト・インテリジェンス用エージェントです。

## 役割

- GitHub上の対象リポジトリを毎回再発見
- README、メタデータ、コミット、ファイルツリーを共通形式で収集
- 理論・データ・イベント・会話・発見・プロデュースの層を整理
- データの出典、依存関係、重複、未充足領域を分析
- 短期・中期・長期の提案を、根拠・コスト・リスク・検証方法付きで提示

## 実行

GitHub CLI (`gh`) の認証済み環境で次を実行します。

```bash
./scripts/collect-idol-repos.sh
python3 scripts/analyze-idol-repos.py
```

出力は次の通りです。

- `data/repos.jsonl`: 収集スナップショット。1行1リポジトリ。
- `reports/latest.md`: 最新の棚卸し・分析・提案。
- `.github/agents/idol-p-agent.agent.md`: GitHub向けエージェント定義。

## 初回の観測

現時点では、`idol-lab` が理論・オントロジー・構造化データ、`idol-research` が実証研究・データサイエンス、`idol-live` がイベント収集、`idol-map` が地域×年代の発見、`idol-talk` が関係・会話モデル、`idol-produce` / `idol-produce-or` がファン関係と事業シミュレーションを担う構造が見えています。

この構造は初期仮説です。正式な依存関係やSingle Source of Truthとして扱う前に、フィールド単位のスキーマ・出典・更新責任を照合します。

## 設計上の境界

このエージェントは、依頼がない限り Issue/PR の作成、コードのpush、外部公開、破壊的変更を行いません。privateリポジトリは認証された範囲だけを読み、秘密情報や個人情報をレポートへコピーしません。将来予測は断定せず、観測事実・仮説・信頼度・次の検証を分けて記録します。

## エコシステム定義

既存リポジトリの役割分担を借用し、次の流れを初期のエコシステムとして扱います。

```text
Public Data / External Sources
          ↓ collect / normalize
idol-research ── research design / observation / analysis
          ↓ canonicalize
idol-db ──────── canonical public data / schema / API / feeds
          ↓ consume
idol-live ────── event discovery and scheduling
idol-map ─────── region × decade discovery
idol-playlist ── music and ranking experiences
idol-talk ────── relationship and conversation models
idol-produce ─── business / fan-trust simulation
          ↓ evaluate
Research Results / Product Proposals
```

`idol-lab` は理論・民俗学・概念・解釈・ontologyを保持し、`idol-research` は研究設計と検証、`idol-db` は公開データのcanonical layerとインターフェースを担当する、という境界を優先します。プロダクトrepoはcanonical dataを直接複製せず、出典付きのAPIまたはfixtureを介して利用することを提案します。

### 共通データ契約

収集・正規化・分析で扱うデータには、可能な限り `source`、`source_url`、`accessed_at`、`retrieved_at`、`license`、`confidence` を保持します。`idol-live` のイベントでは、`fetched_at`、無料条件、ドリンク代、予約条件を分離します。raw dataの再販売ではなく、継続観測・集計・比較・特徴量化・モデル化による分析結果を価値の中心に置きます。
