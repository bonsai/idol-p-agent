# idol-p-agent 現状把握レポート

> 生成日時: 2026-09-23 08:48 UTC。この文書は GitHub の取得結果から生成した観測レポートです。README由来の記述と推論を混同しません。

## 1. Executive summary

`bonsai` 配下で発見された対象は **15 リポジトリ**です。言語情報は unknown: 5, HTML: 5, Python: 3, JavaScript: 1, TypeScript: 1。公開範囲は取得権限の範囲で private 5 件です。

初期仮説として、`idol-lab` が理論・オントロジー・基礎データ、`idol-research` が実証分析、`idol-live`・`idol-map`・`idol-talk`・`idol-produce` 系が応用プロダクトという層構造が確認できます。これはREADMEとファイルツリーに基づく仮説であり、依存関係の正式な契約として固定する前に各repoのデータ出典を照合すべきです。

## 2. Inventory table

| Repository | Visibility | Updated | Inferred domain | Description |
|---|---|---:|---|---|
| [`idol-banduke`](https://github.com/bonsai/idol-banduke) | private | 2026-09-10 | unclassified |  |
| [`idol-db`](https://github.com/bonsai/idol-db) | public | 2026-09-23 | canonical data / API |  |
| [`idol-fansite`](https://github.com/bonsai/idol-fansite) | public | 2026-09-11 | unclassified |  |
| [`idol-lab`](https://github.com/bonsai/idol-lab) | private | 2026-09-20 | theory / ontology / research | アイドル民俗学プロジェクト（論文・概念ラボ）。現代の奇祭としての「推す」という行為。md/ttl を GitHub で閲覧可能。 |
| [`idol-live`](https://github.com/bonsai/idol-live) | public | 2026-09-23 | canonical data / API |  |
| [`idol-map`](https://github.com/bonsai/idol-map) | public | 2026-09-14 | theory / ontology / research | Radiooooo ミミック：日本の御当地アイドルを「地方 × 年代」で選び、音楽へアクセス。年代コンテンツは idol-quiz のアイドル民俗学データを使用。 |
| [`idol-oshare`](https://github.com/bonsai/idol-oshare) | private | 2026-08-27 | unclassified |  |
| [`idol-p-agent`](https://github.com/bonsai/idol-p-agent) | public | 2026-09-23 | conversation / agent |  |
| [`idol-playlist`](https://github.com/bonsai/idol-playlist) | public | 2026-09-21 | map / playlist / discovery |  |
| [`idol-portal`](https://github.com/bonsai/idol-portal) | public | 2026-09-14 | theory / ontology / research | アイドル民俗学プロジェクト 統合ポータル。idol-quiz/idol-lab/idol-oshare を横断し、共有オントロジーの可視化成果物（SQLite/グラフ/DOT）をまとめる。 |
| [`idol-produce`](https://github.com/bonsai/idol-produce) | private | 2026-09-03 | production / business simulation |  |
| [`idol-produce-or`](https://github.com/bonsai/idol-produce-or) | public | 2026-09-18 | canonical data / API |  |
| [`idol-quiz`](https://github.com/bonsai/idol-quiz) | private | 2026-09-11 | theory / ontology / research | アイドル民俗学クイズ（別repo）。アイドル民俗学検定 全21問＋年代別年表。 |
| [`idol-research`](https://github.com/bonsai/idol-research) | public | 2026-09-19 | canonical data / API |  |
| [`idol-talk`](https://github.com/bonsai/idol-talk) | public | 2026-09-18 | production / business simulation |  |

## 3. Domain / data / dependency map

| Layer | Evidence | Interpretation |
|---|---|---|
| Theory and source data | `idol-lab` README describes research, ontology, and structured data; it also records `idol-quiz` integration | Candidate source-of-truth layer |
| Empirical research | `idol-research` README describes data collection, DB, marketing, data science, and hypothesis testing | Analysis and validation layer |
| Live / events | `idol-live` README specifies event normalization, source URL, and fetched timestamp | Operational event-data layer |
| Discovery / context | `idol-map` README describes region × decade navigation and reuse of quiz context | Experience layer using historical/context data |
| Relationship / conversation | `idol-talk` README models idol × fan interaction and next-interest suggestions | Interaction model layer |
| Production / simulation | `idol-produce` and `idol-produce-or` describe fan trust, investment, and visible/invisible value | Experimentation and productization layer |

## 4. Evidence and gaps

### Observed signals

- **idol-banduke**: unclassified; representative files: not detected in first 200 files.
- **idol-db**: canonical data / API; representative files: README.md, data.json, data.jsonl, ontology.json, index.html, api, schema.
- **idol-fansite**: unclassified; representative files: data.json, index.html.
- **idol-lab**: theory / ontology / research; representative files: not detected in first 200 files.
- **idol-live**: canonical data / API; representative files: README.md, package.json, index.html, src, schema.
- **idol-map**: theory / ontology / research; representative files: README.md, index.html.
- **idol-oshare**: unclassified; representative files: not detected in first 200 files.
- **idol-p-agent**: conversation / agent; representative files: not detected in first 200 files.
- **idol-playlist**: map / playlist / discovery; representative files: index.html.
- **idol-portal**: theory / ontology / research; representative files: README.md, index.html, api, schema.
- **idol-produce**: production / business simulation; representative files: not detected in first 200 files.
- **idol-produce-or**: canonical data / API; representative files: README.md.
- **idol-quiz**: theory / ontology / research; representative files: not detected in first 200 files.
- **idol-research**: canonical data / API; representative files: README.md, schema.
- **idol-talk**: production / business simulation; representative files: README.md.

### Gaps requiring validation

- Repository references are not yet a formal dependency graph. Extract and validate links in README, source, and package manifests before consolidating data.
- Data provenance appears important (`source_url`, `fetched_at`, and source repo references), but field-level schemas should be compared and versioned.
- Product status cannot be inferred from README alone. Add commit activity, deployment status, test presence, and last meaningful change to the next snapshot.
- Future proposals below are hypotheses, not forecasts; validate each with a small cross-repo experiment.

## 5. Prioritized proposals

| Priority | Proposal | Rationale | First validation |
|---|---|---|---|
| P0 | Establish a shared provenance contract | Multiple projects reuse cultural/context/event data; source URL and acquisition time are critical for trust | Compare schemas in `idol-lab`, `idol-research`, and `idol-live`; write one minimal JSON Schema |
| P0 | Generate a machine-readable dependency map | README-level links already indicate data flow between lab, research, quiz, and map | Parse repository URLs and local import paths; review false positives in one report |
| P1 | Create a cross-product insight loop | Research hypotheses can be tested against live/event and relationship/product signals | Define 3 metrics and run one historical or synthetic backtest |
| P1 | Add a canonical capability/status matrix | The portfolio spans theory, data, interaction, discovery, and simulation; status is currently fragmented | Record implementation state, owner, evidence, and next action per repo |
| P2 | Build a unified idol domain ontology adapter | `idol-lab` has ontology assets while product repos need domain-specific views | Map one entity (`idol`, `event`, or `fan relationship`) end-to-end without rewriting source data |

## 6. Risks and validation plan

The main risks are **data drift**, **duplicate source-of-truth**, **private/public boundary leakage**, and overconfident future claims. Every subsequent run should preserve the raw snapshot, show changes since the previous run, and cite the exact repository and file supporting each material claim. Reports must redact credentials and avoid copying private content into public artifacts.

## 7. Next run checklist

1. Run `./scripts/collect-idol-repos.sh`.
2. Run `python3 scripts/analyze-idol-repos.py`.
3. Review added/removed repositories and README changes.
4. Verify dependency links and provenance fields.
5. Promote only validated proposals to implementation issues.
