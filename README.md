# NoirAI — Automated Risk Analysis System

NoirAI is a system for automated investigation and risk analysis of digital entities such as domains, companies, and URLs.
It integrates structured data collection, configurable analysis, and transparent reporting.

---

## What NoirAI Does

* **Evidence collection** — WHOIS data, web content, news mentions, and reputation checks
* **Analysis engine** — Heuristics + AI planning to identify risk patterns
* **Risk assessment** — Scores and labels entities as low, medium, high, or critical risk
* **Traceable process** — Step-by-step execution visible to the user
* **Reports** — Exportable investigation summaries

---

## Architecture Overview

* **Planner** — determines the investigation strategy
* **Orchestrator** — runs the plan and manages primitives
* **Primitives** — self-contained modules (whois, scraper, news search, reputation)
* **Risk Engine** — aggregates evidence into a score and label
* **Storage** — local and S3 for evidence and reports

---

## Features

* Real-time trace of system execution
* Multi-source data collection
* Explainable scoring (every verdict tied to evidence)
* Modular primitives (easy to extend)
* AWS-ready (Bedrock, Lambda, ECS, S3)
* Exportable reports for documentation

---

## Stack

* **Backend**: Python, FastAPI, Pydantic
* **Frontend**: Next.js, TypeScript, Tailwind
* **Infra**: AWS Lambda, ECS, S3, API Gateway
* **AI**: Amazon Bedrock (planning and analysis)
* **Storage**: S3 (production), local filesystem (development)

---

## Status

Work in progress. Active development. Expect incomplete features and breaking changes.

---

## License

Apache 2.0. See [LICENSE](LICENSE) for terms.
This project also includes a [NOTICE](NOTICE) file with additional legal and attribution details.
