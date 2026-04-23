#!/usr/bin/env python
import argparse
import sys
import os
import logging
from pathlib import Path
from .openmetadata_client import OpenMetadataClient
from .sql_analyzer import SQLAnalyzer
from .lineage_checker import LineageChecker
from .quality_checker import QualityChecker
from .contract_validator import ContractValidator
from .reporter import generate_report, generate_ai_explanation
from .reporter import generate_report, send_slack_webhook   # <--- add send_slack_webhook
from .lineage_checker import estimate_full_scan_cost        # <--- add this

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def resolve_fqn(table: str, service: str = "default", database: str = "public", schema: str = "") -> str:
    if schema:
        return f"{service}.{database}.{schema}.{table}"
    return f"{service}.{database}.{table}"

def resolve_fqn(table: str, service: str = "default", database: str = "public", schema: str = "") -> str:
    """Build OpenMetadata FQN from components"""
    if schema:
        return f"{service}.{database}.{schema}.{table}"
    return f"{service}.{database}.{table}"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True)
    parser.add_argument("--token", required=True)
    parser.add_argument("--sql-path", default="models/")
    parser.add_argument("--fail-on-violation", default="true")
    parser.add_argument("--service", default="default")
    parser.add_argument("--database", default="public")
    parser.add_argument("--slack-webhook", default="", help="Slack webhook URL for notifications")
    parser.add_argument("--slack-on-violation", action="store_true", help="Only send Slack on violation")
    parser.add_argument("--service", default="default", help="OpenMetadata service name")
    parser.add_argument("--database", default="public", help="Database name for FQN")
    args = parser.parse_args()

    client = OpenMetadataClient(args.host, args.token)
    analyzer = SQLAnalyzer()
    lineage = LineageChecker(client)
    quality = QualityChecker(client)
    contract = ContractValidator(client)

    sql_dir = Path(args.sql_path)
    sql_files = list(sql_dir.rglob("*.sql")) + list(sql_dir.rglob("*.yml"))

    violations = []
    warnings = []
    impacts = []

    for file in sql_files:
        try:
            with open(file) as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Cannot read {file}: {e}")
            continue

        changes = analyzer.detect_changes(content)
        for change in changes:
            table = change['table']
            table_fqn = resolve_fqn(table, args.service, args.database)
            logger.info(f"Checking {change['type']} on {table_fqn}")

            # Lineage impact
            impact = lineage.check_impact(table_fqn)
            if impact["has_downstream"]:
                impacts.append({
                    "table": change['table'],
                    "count": impact['count'],
                    "severity": impact['severity'],
                    "tables": impact.get('tables', []),
                    "dashboards": impact.get('dashboards', [])
                })

            # Contract validation for destructive changes
            if change['operation'] in ('DROP', 'MODIFY'):
                col = change.get('column', '')
                val = contract.validate_column_change(table_fqn, col, change['operation'])
                if not val['valid']:
                    # ai_msg = generate_ai_explanation(
                    #     change_type="ALTER_TABLE",
                    #     table=change['table'],
                    #     column=col,
                    #     operation=change['operation'],
                    #     downstream_tables=impact.get('tables', []),
                    #     downstream_dashboards=impact.get('dashboards', []),
                    #     suggested_fix=val.get('suggested_fix', 'Review downstream dependencies before merging.')
                    # )
                                        # Compute cost estimate for this table
                    table_fqn_for_cost = resolve_fqn(change['table'], args.service, args.database)
                    cost_est = estimate_full_scan_cost(table_fqn_for_cost, client)

                    ai_msg = generate_ai_explanation(
                        change_type="ALTER_TABLE",
                        table=change['table'],
                        column=col,
                        operation=change['operation'],
                        downstream_tables=impact.get('tables', []),
                        downstream_dashboards=impact.get('dashboards', []),
                        suggested_fix=val.get('suggested_fix', 'Review dependencies.'),
                        cost_estimate=cost_est   # 👈 new argument
                    )
                    violations.append({
                        "table": change['table'],
                        "message": val['message'],
                        "ai_explanation": ai_msg,
                        "ai_generated": True
                    })

            # Quality check (non‑breaking)
            qual = quality.check_quality(table_fqn)
            if qual.get('warning'):
                warnings.append({"table": change['table'], "message": qual['message']})

    report = generate_report(violations, warnings, impacts)

    if args.slack_webhook and (args.slack_on_violation and violations):
        send_slack_webhook(report, args.slack_webhook)

    with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
        f.write(f"report<<EOF\n{report}\nEOF\n")
        f.write(f"has-violations={str(len(violations) > 0).lower()}\n")

    print(report)
    if args.fail_on_violation == "true" and violations:
        logger.error("Breaking changes detected – exiting with non‑zero code")
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()