# NoirAI — Autonomous Detective Agent 🕵️‍♀️

**An AI-powered investigation system that analyzes companies, domains, and URLs to determine their legitimacy and risk profile.**

NoirAI combines automated data collection, intelligent analysis, and clear reporting to help users make informed decisions about digital entities they encounter online.

---

## What NoirAI Does

NoirAI investigates digital targets through multiple data sources and provides a clear assessment:

- **Automated Evidence Collection** — Gathers WHOIS data, web content, news mentions, and reputation signals
- **Intelligent Analysis** — Uses AI to synthesize findings and identify risk patterns  
- **Clear Risk Assessment** — Delivers actionable verdicts: legitimate, suspicious, or scam
- **Transparent Process** — Shows step-by-step reasoning so users can understand and verify conclusions
- **Exportable Reports** — Generates comprehensive investigation summaries

---

## How It Works

The system uses a modular architecture designed for reliability and transparency:

**Planner** — Determines investigation strategy based on target type and available data sources

**Orchestrator** — Executes the investigation plan, manages data collection, and handles errors gracefully

**Primitives** — Specialized tools for specific tasks (WHOIS lookup, web scraping, news search, reputation checking)

**Storage** — Secure artifact management with support for local development and cloud deployment

**Frontend** — Clean, investigator-themed interface showing real-time progress and final reports

**Risk Engine** — Analyzes collected evidence using configurable heuristics and AI models

---

## Key Features

- **Real-time Investigation Tracking** — Watch as the agent collects and analyzes evidence
- **Multi-source Data Collection** — WHOIS records, website analysis, news mentions, domain reputation
- **Explainable AI Decisions** — Every conclusion is backed by clear evidence and reasoning
- **Modular Architecture** — Easy to extend with new data sources or analysis methods
- **Cloud-Ready Deployment** — Built for AWS with Bedrock AI integration
- **Export-Ready Reports** — Professional investigation summaries for documentation

---

## Technology Stack

**Backend:** Python, FastAPI, Pydantic models, AWS Bedrock
**Frontend:** Next.js, TypeScript, Tailwind CSS
**Infrastructure:** AWS Lambda, ECS, S3, API Gateway
**AI:** Amazon Bedrock for dynamic planning and analysis
**Storage:** S3 for artifacts, local filesystem for development.

---

## Project Status

Under active development.  
Expect breaking changes, unfinished features, and rough edges until closer to the deadline.

---

## License

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

Licensed under the Apache License 2.0. See [LICENSE](LICENSE) for full terms.