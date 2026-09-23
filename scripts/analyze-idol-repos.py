#!/usr/bin/env python3
"""Generate a conservative, evidence-based inventory report from repos.jsonl."""
from __future__ import annotations
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "repos.jsonl"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

if not DATA.exists():
    raise SystemExit("data/repos.jsonl not found; run scripts/collect-idol-repos.sh first")

repos = [json.loads(line) for line in DATA.read_text().splitlines() if line.strip()]
now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

def classify(repo):
    text = f"{repo.get('name','')} {repo.get('description','')} {repo.get('readme','')}".lower()
    rules = [
        ("canonical data / API", r"idol-db|canonical|schema|crawler|api|provenance"),
        ("theory / ontology / research", r"民俗|ontology|研究|research|理論|文化"),
        ("live / event discovery", r"live|ライブ|event|イベント"),
        ("production / business simulation", r"produce|producer|経営|投資|ゲーム|game"),
        ("conversation / agent", r"talk|会話|agent|conversation"),
        ("map / playlist / discovery", r"map|playlist|音楽|地域|年代"),
    ]
    for label, pattern in rules:
        if re.search(pattern, text):
            return label
    return "unclassified"

for repo in repos:
    repo["inferred_domain"] = classify(repo)

languages = Counter((r.get("language") or "unknown") for r in repos)
private_count = sum(bool(r.get("private") or r.get("isPrivate")) for r in repos)
all_files = [(r["name"], f) for r in repos for f in r.get("files", [])]

lines = [
    "# idol-p-agent 現状把握レポート",
    "",
    f"> 生成日時: {now}。この文書は GitHub の取得結果から生成した観測レポートです。README由来の記述と推論を混同しません。",
    "",
    "## 1. Executive summary",
    "",
    f"`bonsai` 配下で発見された対象は **{len(repos)} リポジトリ**です。言語情報は {', '.join(f'{k}: {v}' for k, v in languages.most_common())}。公開範囲は取得権限の範囲で private {private_count} 件です。",
    "",
    "初期仮説として、`idol-lab` が理論・オントロジー・基礎データ、`idol-research` が実証分析、`idol-live`・`idol-map`・`idol-talk`・`idol-produce` 系が応用プロダクトという層構造が確認できます。これはREADMEとファイルツリーに基づく仮説であり、依存関係の正式な契約として固定する前に各repoのデータ出典を照合すべきです。",
    "",
    "## 2. Inventory table",
    "",
    "| Repository | Visibility | Updated | Inferred domain | Description |",
    "|---|---|---:|---|---|",
]
for r in sorted(repos, key=lambda x: x.get("name", "")):
    desc = (r.get("description") or "").replace("|", "\\|").replace("\n", " ")
    visibility = "private" if r.get("private") or r.get("isPrivate") else "public"
    lines.append(f"| [`{r['name']}`]({r.get('html_url', r.get('url',''))}) | {visibility} | {r.get('updated_at', r.get('updatedAt',''))[:10]} | {r['inferred_domain']} | {desc[:180]} |")

lines += ["", "## 3. Domain / data / dependency map", "", "| Layer | Evidence | Interpretation |", "|---|---|---|", "| Theory and source data | `idol-lab` README describes research, ontology, and structured data; it also records `idol-quiz` integration | Candidate source-of-truth layer |", "| Empirical research | `idol-research` README describes data collection, DB, marketing, data science, and hypothesis testing | Analysis and validation layer |", "| Live / events | `idol-live` README specifies event normalization, source URL, and fetched timestamp | Operational event-data layer |", "| Discovery / context | `idol-map` README describes region × decade navigation and reuse of quiz context | Experience layer using historical/context data |", "| Relationship / conversation | `idol-talk` README models idol × fan interaction and next-interest suggestions | Interaction model layer |", "| Production / simulation | `idol-produce` and `idol-produce-or` describe fan trust, investment, and visible/invisible value | Experimentation and productization layer |", "", "## 4. Evidence and gaps", "", "### Observed signals", ""]
for r in sorted(repos, key=lambda x: x.get("name", "")):
    files = r.get("files", [])
    signals = []
    for key in ("README.md", "data.json", "data.jsonl", "ontology.json", "package.json", "index.html", "src", "api", "schema"):
        if any(key in f for f in files): signals.append(key)
    lines.append(f"- **{r['name']}**: {r['inferred_domain']}; representative files: {', '.join(signals) if signals else 'not detected in first 200 files'}." )
lines += ["", "### Gaps requiring validation", "", "- Repository references are not yet a formal dependency graph. Extract and validate links in README, source, and package manifests before consolidating data.", "- Data provenance appears important (`source_url`, `fetched_at`, and source repo references), but field-level schemas should be compared and versioned.", "- Product status cannot be inferred from README alone. Add commit activity, deployment status, test presence, and last meaningful change to the next snapshot.", "- Future proposals below are hypotheses, not forecasts; validate each with a small cross-repo experiment.", "", "## 5. Prioritized proposals", "", "| Priority | Proposal | Rationale | First validation |", "|---|---|---|---|", "| P0 | Establish a shared provenance contract | Multiple projects reuse cultural/context/event data; source URL and acquisition time are critical for trust | Compare schemas in `idol-lab`, `idol-research`, and `idol-live`; write one minimal JSON Schema |", "| P0 | Generate a machine-readable dependency map | README-level links already indicate data flow between lab, research, quiz, and map | Parse repository URLs and local import paths; review false positives in one report |", "| P1 | Create a cross-product insight loop | Research hypotheses can be tested against live/event and relationship/product signals | Define 3 metrics and run one historical or synthetic backtest |", "| P1 | Add a canonical capability/status matrix | The portfolio spans theory, data, interaction, discovery, and simulation; status is currently fragmented | Record implementation state, owner, evidence, and next action per repo |", "| P2 | Build a unified idol domain ontology adapter | `idol-lab` has ontology assets while product repos need domain-specific views | Map one entity (`idol`, `event`, or `fan relationship`) end-to-end without rewriting source data |", "", "## 6. Risks and validation plan", "", """The main risks are **data drift**, **duplicate source-of-truth**, **private/public boundary leakage**, and overconfident future claims. Every subsequent run should preserve the raw snapshot, show changes since the previous run, and cite the exact repository and file supporting each material claim. Reports must redact credentials and avoid copying private content into public artifacts.""", "", "## 7. Next run checklist", "", """1. Run `./scripts/collect-idol-repos.sh`.
2. Run `python3 scripts/analyze-idol-repos.py`.
3. Review added/removed repositories and README changes.
4. Verify dependency links and provenance fields.
5. Promote only validated proposals to implementation issues.""", ""]
(REPORTS / "latest.md").write_text("\n".join(lines), encoding="utf-8")
print(f"wrote {REPORTS / 'latest.md'}")
