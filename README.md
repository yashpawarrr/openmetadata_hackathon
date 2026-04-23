<!-- ===================================== -->
<!-- ⚡ DATA NEXUS SUITE - FULL README -->
<!-- ===================================== -->

<!-- <p align="center">
  <img src="https://via.placeholder.com/160x160.png?text=DataNexus" alt="DataNexus Logo" />
</p> -->

<h1 align="center">⚡ DataNexus Suite</h1>

<p align="center">
  <b>The “Shift-Left” Developer Ecosystem for OpenMetadata</b>
</p>

<p align="center">
  Bridging the gap between <b>Data Governance</b> and <b>Software Engineering</b> inside CI/CD + IDEs
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Hackathon-WeMakeDevs-blue?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/OpenMetadata-Integrated-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Status-Prototype-orange?style=for-the-badge"/>
</p>

---

# 📊 OpenMetadata Data Governance Suite

**Enforce, Observe, and Optimize Data Changes Before They Break Production**

A developer-first data governance toolkit that integrates directly into **GitHub CI/CD pipelines** and **VS Code**, powered by OpenMetadata.

It prevents broken pipelines, stale documentation, and expensive query mistakes by turning metadata into real-time developer intelligence.

---

## 🚨 Problem Statement

Modern data teams suffer from:

- ❌ Breaking SQL/dbt changes discovered *after deployment*
- ❌ No governance feedback inside PR workflows
- ❌ Stale documentation that never matches real schema
- ❌ Expensive full-table scans due to missing query awareness
- ❌ Metadata trapped inside dashboards instead of being in the developer workflow

👉 OpenMetadata already stores rich metadata (lineage, quality, contracts). But that metadata remains trapped inside the UI – invisible to the developer writing the code.

**We built the missing bridge.**

---

## 💡 Solution Overview

The **OpenMetadata Data Governance Suite** is a production‑grade toolkit that:

## *Enforce, Observe, and Optimize – Before Merging a Single Line of Code*

- 🔍 **Validates every SQL/dbt change** against OpenMetadata lineage and contracts – directly in your PR.
- 🤖 **Generates human‑readable impact narratives** (not just “violation detected”).
- 💡 **Brings metadata into the IDE** – hover over a table to see description, owner, tags, and quality score.
- ⚡ **Acts as a coding coach** – warns about missing partition filters, full scans, and low‑quality tables.
- 📄 **Auto‑generates data dictionaries** and keeps them in sync with your repository.
- 🧪 **Creates Great Expectations / dbt tests** automatically from OpenMetadata constraints.

All of this runs **inside your GitHub workflows** and **VS Code** – no extra dashboards, no context switching.


> **Stop breaking downstream pipelines. Give every PR an AI-powered governance report, bring lineage into your IDE, and auto-document your data stack.**

---

## 🏗️ Architecture Diagram

┌─────────────────────────────────────────────────────────────────────┐
│                        Developer Workspace                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   VS Code / Cursor Extension                                        │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │ • Hover Provider (Table + Column Docs)                      │   │
│   │ • Inline Optimization Coach                                 │   │
│   │ • Lineage-at-a-Glance View                                  │   │
│   │ • Natural Language Search (OpenMetadata)                    │   │
│   └─────────────────────────────────────────────────────────────┘   │
│                                │                                    │
│                                │ API Calls                          │
│                                ▼                                    │
│                    ┌──────────────────────────┐                     │
│                    │ OpenMetadata API Client  │                     │
│                    │ (Python + TypeScript)    │                     │
│                    └─────────────┬────────────┘                     │
│                                  │                                  │
│                                  │                                  │
│         ┌────────────────────────┼────────────────────────┐         │
│         │                        │                        │         │
│         ▼                        ▼                        ▼         │
│ ┌───────────────┐     ┌────────────────┐     ┌──────────────────┐   │
│ │ Lineage API   │     │ Quality API    │     │ Contract API     │   │
│ └───────────────┘     └────────────────┘     └──────────────────┘   │
│                                                                     │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                         GitHub Repository                           │
│                                                                     │
│  .github/workflows/                                                 │
│  ├── data-contract-validator (CI/CD Governance)                     │ 
│  └── auto-doc-generator (Docs Sync Bot)                             │
│                                                                     │
│  PR Flow:                                                           │
│  SQL Change → Analyzer → OpenMetadata → Impact Engine → PR Comment  │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                        OpenMetadata Server                          │
│                                                                     │
│   ┌────────────┐   ┌────────────┐   ┌────────────┐                  │
│   │  Lineage   │   │  Quality   │   │  Contracts │                  │
│   └────────────┘   └────────────┘   └────────────┘                  │
│                                                                     │
│          ┌──────────────────────────────────────┐                   │
│          │ MySQL (Metadata Store)+Elasticsearch │                   │
│          └──────────────────────────────────────┘                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

---

## ✨ Features

### 1. 🔐 CI/CD Data Contract Validator (GitHub Action)
- Runs on every PR that touches `.sql` or `.yml` files.
- Detects `ALTER`, `DROP`, `CREATE` table changes.
- Queries OpenMetadata for **downstream lineage** (tables, dashboards, reports).
- Validates changes against **data contracts** (e.g. “this column is required, cannot be dropped”).
- Posts an **AI‑powered human explanation** directly as a PR comment.

### 2. 💡 IDE Integration (VS Code / Cursor)
- **Hover over any table name** → instantly shows description, owner, tags, quality score, column list.
- **Inline Coach** – warns when you query a large table without a `WHERE` clause or partition filter.
- **Lineage‑at‑a‑glance** – shows upstream and downstream dependencies in a sidebar.
- **Natural language search** – ask *“What is the primary key for the user table?”* inside the IDE.

### 3. 📄 Automated “Data Doc” Generator
- Triggers on merge to `main`.
- Fetches latest schema and descriptions from OpenMetadata.
- Generates a beautiful **Markdown data dictionary** (`docs/data-dictionary.md`).
- Commits it back to the repository automatically.

### 4. 🧪 Data Scout – Auto‑Test Generator
- Reads column constraints (`is_nullable`, `min_value`, `data_type`) from OpenMetadata.
- Generates **Great Expectations expectations** or **dbt tests** automatically.
- Saves hours of manual test writing.

### 5. ⚡ Optimization Intelligence – The Coding Coach
- Parses SQL in real time inside the IDE.
- Recognises `SELECT * FROM huge_table` without `WHERE`.
- Fetches table size and partition info from OpenMetadata.
- Shows a **lightbulb warning** with a concrete fix: *“This table is 500 GB and partitioned by `created_at`. Add a filter on `created_at`.”*

---

## 🛠️ Tech Stack

| Layer          | Technologies |
|----------------|--------------|
| **CI/CD**      | GitHub Actions, Docker, Python 3.11 |
| **IDE**        | VS Code Extension API, TypeScript, Axios |
| **Metadata**   | OpenMetadata REST API (v1.2+) |
| **SQL Parsing**| `sqlparse` (Python), custom regex |
| **AI **        | OpenAI API / Ollama (local) for narrative generation |
| **Testing**    | Great Expectations (auto‑generated) |
| **Docs**       | Markdown + `git-auto-commit-action` |

---

## 🔄 Workflow

1. **Developer opens a PR** that modifies a SQL model.
2. GitHub Action triggers the **Data Contract Validator**.
3. The action:
   - Parses the changed files to detect schema modifications.
   - Calls OpenMetadata APIs to fetch downstream lineage and contracts.
   - Sends the structured impact data to an LLM (or fallback template).
   - Generates a human‑readable warning message.
   - Posts the message as a comment on the PR.
4. **Developer sees the comment** – for example:  
   *“⚠️ You are dropping `user_id` from `orders`. This will break 3 downstream tables and 2 dashboards. Please update `user_activity` model.”*
5. While coding, the **VS Code extension** shows hover cards and performance warnings in real time.
6. After merge, the **Auto‑Doc Generator** updates the data dictionary automatically.

---

## 📸 Example Outputs

### 🔹 PR Comment (with AI explanation)

> ## 📋 OpenMetadata Governance Report
>
> ### ❌ Breaking Changes
>
> ⚠️ **You are trying to DROP column `user_id` from table `orders`.**
>
> **Impact:**
> - 🔻 Breaks **3 downstream tables**: `user_activity`, `revenue_summary`, `customer_360`
> - 📊 Affects **2 dashboards**: `Revenue Dashboard`, `User Funnel Dashboard`
>
> **Suggested fix:** Update joins in `user_activity` model before merging.
>
> ---
> *Report generated by OpenMetadata Data Contract Validator*

### 🔹 VS Code Hover Card


📊 orders
Contains all customer orders.

Owner: @data-team
Tags: pii finance
Quality score: 0.92

Column	Type	Description
order_id	int	Unique order ID
user_id	int	FK to users
amount	decimal	Order total
text

### 🔹 Inline Coach Warning

> ⚠️ **`users_large`** (size: 500 GB) has no `WHERE` clause.  
> This will cause a full table scan.  
> 💡 *Hint: this table is partitioned by `created_at`. Add a filter on `created_at`.*

---

## 💥 Why This Project Is Impactful

- **Prevents production incidents** before they happen.
- **Reduces mean time to resolution (MTTR)** by giving developers actionable fixes, not just error codes.
- **Brings OpenMetadata into the developer’s natural workflow** – no more switching tabs.
- **Automates documentation** – docs that never go stale.
- **Shifts governance from “policing” to “enabling”** – the AI coach helps developers write better queries, not just blocks them.



> *“A single breaking change that goes undetected can cost a data team hours of firefighting. This suite catches those changes in the PR stage – when fixing them costs minutes.”*


---

## 🧪 Getting Started (Quick Links)

- **GitHub Action** – add to your `.github/workflows/`  
  [Example workflow](.github/workflows/data-contract-validator.yml)
- **VS Code Extension** – install from [marketplace link] or run locally  
  `npm install && npm run compile`
- **OpenMetadata Setup** – [Docker quickstart](https://docs.open-metadata.org/deployment)

---

## 👥 Contributors

Built with ❤️ for the OpenMetadata Hackathon.

*We believe metadata should work for developers – not the other way around.*

---

**License:** MIT  


🔮🔮🔮
<p align="center"> <b>Built for developers. Powered by metadata. Designed for scale.</b> </p>
