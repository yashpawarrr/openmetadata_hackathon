# openmetadata_hackathon


Phase 1: MVP Design for the CI/CD Data Contract Validator
The goal is to prevent "breaking changes" from hitting your production data warehouse by validating SQL/dbt changes against OpenMetadata’s lineage.

Architecture of the Action
Trigger: The action runs on pull_request events.

Detection: Use a tool (like a simple Python script using sqlparse) to extract table names/schema changes from the files modified in the PR.

Analysis (The Core):

Query the OpenMetadata REST API for the Lineage of the affected tables.

Compare the proposed changes (e.g., dropping a column, changing a data type) against downstream dependencies (dashboards, other tables).

Reporting: Use an existing GitHub Action (like thollander/actions-comment-pull-request) to post the results back to the PR as a "Governance Check" report.

Core Logic (Pseudo-Python)
Python
# Use the OpenMetadata API to check for downstream impact
def check_impact(table_fqn):
    # API Endpoint: GET /v1/lineage/table/name/{fqn}?upstreamDepth=0&downstreamDepth=3
    response = requests.get(f"{OM_URL}/v1/lineage/table/name/{table_fqn}?downstreamDepth=3", headers=headers)
    lineage = response.json()
    
    # Logic: If 'downstreamNodes' > 0, post a warning comment to the PR
    if lineage['downstreamEdges']:
        return "⚠️ ALERT: This table is used by downstream dashboards! Proceed with caution."
    return "✅ No downstream dependencies detected."
Phase 2: MVP Design for IDE Integration (VS Code Extension)
Developers spend their time in the IDE; bringing metadata to them reduces context switching.

Core Features
Hover Provider: Use the VS Code API registerHoverProvider. When a user hovers over a table name in a .sql file, trigger a request to OpenMetadata to fetch the entity details.

The "Context" View: Use a simple API call to /v1/search/query to find the table's FQN, then fetch details via /v1/tables/name/{fqn}.

Display: Render the Description, Owner, and Tags in a Markdown-formatted hover window.

Phase 3: MVP Design for Automated Data Doc Generator
This ensures documentation never goes stale by syncing your code's reality with OpenMetadata.

Implementation Strategy
Automation: Use a workflow_run trigger in GitHub Actions that fires after a merge to the main branch.

Sync: Fetch the latest schema from OpenMetadata and generate a Markdown table (Data Dictionary).

Update: Automatically commit this file back to your repo’s /docs folder using the stefanzweifel/git-auto-commit-action.

Hackathon Execution Strategy (The "Glue")
To build this successfully in a short period, follow this "Unified Core" strategy:

Create a metadata-client library: Write one small Python package that acts as a wrapper for the OpenMetadata REST API. Your GitHub Action and your IDE extension's backend should both use this.

Standardize on FQN: Always use OpenMetadata's Fully Qualified Name (FQN) as the unique identifier for tables across all three tools.

Focus the Demo: For your hackathon presentation, start by showing the Data Contract Validator. It is the most impressive, as it directly prevents production bugs—the "holy grail" for data teams. Then, show how the IDE Extension would have alerted the dev before they even opened the PR.

Would you like me to provide a template action.yml file to help you structure the GitHub Action, or would you prefer to explore how to set up the authentication (JWT/Bot token) for your OpenMetadata instance?
