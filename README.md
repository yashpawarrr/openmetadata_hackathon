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

## 🧠 Executive Summary

**DataNexus** is an end-to-end developer suite that brings **data governance directly into the development workflow**.

Instead of treating metadata as a post-production audit layer, DataNexus shifts it left into:

- ⚙️ CI/CD pipelines  
- 💻 IDEs (VS Code / Cursor)  
- 🧪 Local testing environments  

👉 Every query, schema change, and PR becomes **governed, optimized, and documented by default**.

---

## 🚨 The Core Problem

Modern data teams suffer from a silent disconnect:

> Metadata lives in dashboards. Developers live in code.

### This causes:

- 💥 Breaking changes in production tables  
- 🔄 Constant context switching (IDE ↔ metadata tools)  
- 📄 Stale documentation  
- 💸 Inefficient queries with no awareness of scale or partitions  

---

## 🧩 Solution Overview

We transform **OpenMetadata into the Central Nervous System of development**.

---

# 🔧 System Architecture

---

## 1️⃣ CI/CD Data Contract Validator (GitHub Action)

Triggered on every Pull Request.

### Workflow:
- Parses SQL / YAML changes  
- Runs lineage-based impact analysis  
- Validates against data contracts  

### Powered by:
- OpenMetadata **Lineage API**

### 🧨 Example Output:
> ⚠️ Dropping `user_id`  
> → Breaks 3 dashboards + 1 Airflow pipeline  

---

## 2️⃣ IDE Data Context (VS Code / Cursor Plugin)

Brings metadata into the editor.

### Features:
- Hover-based schema insights  
- PII / Sensitive tag alerts  
- Ownership + glossary context  
- Data health indicators  

### Powered by:
- OpenMetadata **Search API**
- Entity + Tag system

👉 Zero context switching. Everything inside the IDE.

---

## 3️⃣ Optimization Intelligence (Coding Coach)

A real-time SQL intelligence layer.

### Detects:
- Full table scans  
- Missing partition filters  
- Expensive queries  

### Powered by:
- Table Profiling API  
- Schema metadata

<!-- ========================================= -->
<!-- ⚡ OPENMETADATA GOVERNANCE SUITE -->
<!-- ========================================= -->

<p align="center">
  <img src="https://via.placeholder.com/160x160.png?text=OGS" alt="OGS Logo"/>
</p>

<h1 align="center">⚡ OpenMetadata Governance Suite</h1>

<p align="center">
  <b>Shift-Left Data Governance for Modern Engineering Teams</b>
</p>

<p align="center">
  From <i>post-production audits</i> → to <b>pre-commit intelligence</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Data%20Governance-Automated-blue?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/OpenMetadata-Native-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/CI%2FCD-Integrated-orange?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/IDE-Enabled-purple?style=for-the-badge"/>
</p>

---

# 🧠 The Big Idea

Modern data systems fail not because of lack of tools —  
but because **governance happens too late**.

> Developers write code in IDEs  
> Data breaks in production  
> Governance reacts after damage is done  

---

## ⚡ We Fix That

**OpenMetadata Governance Suite turns governance into a developer-native workflow.**

We embed intelligence into:

- ⚙️ GitHub PRs (CI/CD layer)
- 💻 VS Code (developer layer)
- 🧪 Automated test generation (quality layer)
- 📚 Standardized documentation (knowledge layer)

👉 Governance is no longer a dashboard.  
👉 It becomes a **background system of truth enforcement**.

---

# 🏗️ Architecture Overview


Developer writes code
↓
VS Code Extension (real-time intelligence)
↓
GitHub PR (data contract validation)
↓
CI/CD pipeline (lineage + impact analysis)
↓
Auto Tester (schema + quality enforcement)
↓
Auto Docs Generator (knowledge sync)
↓
Production-safe deployment 🚀


---

# 📁 Repository Structure Explained

---

## 1️⃣ `.github/workflows/` — Automation Triggers

> 🧩 The nervous system of governance

### What it does:
- Listens to Pull Requests
- Triggers validation pipelines
- Enforces governance before merge

### Components:

- `data-contract-validator.yml`  
  👉 Blocks breaking schema changes before merge

- `auto-doc-generator.yml`  
  👉 Updates documentation automatically after merge

💡 **Key Idea:** Governance starts at commit time, not production time.

---

## 2️⃣ `github-action/` — The Governance Engine

> ⚙️ Your automated data auditor inside CI/CD

### Core Responsibilities:
- SQL parsing  
- Lineage impact analysis  
- Schema validation  
- PR commenting with insights  

### Inside:

- `action.yml` → GitHub entry contract  
- `Dockerfile` → reproducible execution environment  
- `src/main.py` → pipeline orchestrator  
- `openmetadata_client.py` → API bridge  
- `lineage_checker.py` → downstream impact detection  
- `contract_validator.py` → breaking change prevention  
- `reporter.py` → PR feedback system  

🔥 This is where **OpenMetadata becomes enforcement logic**

---

## 3️⃣ `vscode-extension/` — Developer Intelligence Layer

> 💻 Governance inside the IDE (Shift-Left in action)

### Features:
- Hover-based metadata context  
- Inline SQL optimization suggestions  
- Real-time lineage exploration  
- AI-powered dataset search  

### Core Modules:

- `hoverProvider.ts` → schema insights on hover  
- `inlineCoach.ts` → query optimization warnings  
- `lineageView.ts` → dependency visualization  
- `aiSearch.ts` → natural language dataset search  

💡 **Key Idea:** Developers never leave the IDE to understand data.

---

## 4️⃣ `auto-tester/` — Quality Enforcement Engine

> 🧪 Turning metadata into test cases automatically

### What it does:
- Reads OpenMetadata constraints  
- Generates dbt / Great Expectations tests  
- Ensures schema rules are enforced locally  

### File:
- `generate_tests.py` → converts metadata → test suites  

💡 **Key Idea:**  
Production rules become local tests automatically.

---

## 5️⃣ `docs/` — Knowledge Standardization Layer

> 📚 Single source of truth for all data systems

### Purpose:
- Standardized data dictionary format  
- AI-friendly documentation structure  
- Consistent metadata onboarding  

### File:
- `data-dictionary-template.md`

💡 **Key Idea:** Documentation is not manual anymore — it is structured and enforced.

---

# 🚀 Why This Project Matters

## ❌ Before (Traditional Stack)
- Broken dashboards in production  
- Late detection of schema issues  
- Manual documentation debt  
- No visibility inside IDE  

---

## ✅ After (DataNexus Stack)
- Errors blocked in PR stage  
- Real-time IDE intelligence  
- Auto-generated tests  
- Auto-updated documentation  
- Full lineage-aware development  

---

# 🎬 Demo Flow (VERY IMPORTANT)

1. Developer changes SQL schema  
2. VS Code warns instantly ⚠️  
3. PR is opened  
4. GitHub Action runs lineage check  
5. ❌ PR gets blocked with explanation  
6. Auto-doc updates in background  

👉 Judges instantly see real-world impact

---

# 🧭 Final Vision

> “Governance should not be a meeting.  
It should be a system that runs before humans make mistakes.”

---

# ⚡ Outcome

This suite ensures:

- Safer pipelines  
- Smarter developers  
- Faster delivery  
- Zero governance debt  

---

<p align="center">
  <b>Built for engineers who ship fast — without breaking things.</b>
</p>
```








### Example:

```sql
SELECT * FROM events;

🔴 Issue:

5TB table scan detected
No partition filter

✅ Fix:

SELECT * FROM events WHERE event_date >= CURRENT_DATE;
4️⃣ Data Scout (Auto-Test Engine)

Keeps local development aligned with production.

What it does:
Reads OpenMetadata test definitions
Generates dbt / Great Expectations tests

👉 Ensures dev ≈ production always

📊 Feature Matrix
Feature	OpenMetadata Component	Value
Impact Analysis	Lineage API	Prevents outages
Context Awareness	Entity API	Zero switching
Schema Drift Detection	Versioning API	Safe changes
Auto Documentation	Export APIs	No doc debt
Optimization Alerts	Profiler API	Lower cost queries

DataNexus transforms OpenMetadata from:

📦 System of Record
to
🧠 System of Intelligence

🎬 Hackathon Demo Moment (IMPORTANT)

Show this live:

Developer opens Pull Request
Schema change detected
Lineage impact analysis runs
❌ PR gets blocked automatically


🧭 Conclusion

DataNexus is not just a tool.

It is a developer-first governance layer that ensures:

Cleaner code
Safer pipelines
Smarter queries
Lower costs

All without leaving the IDE.

🔮🔮🔮
<p align="center"> <b>Built for developers. Powered by metadata. Designed for scale.</b> </p>
