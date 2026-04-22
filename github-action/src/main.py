#!/usr/bin/env python
import argparse
import sys
import os
from pathlib import Path
from .openmetadata_client import OpenMetadataClient
from .sql_analyzer import SQLAnalyzer
from .lineage_checker import LineageChecker
from .quality_checker import QualityChecker
from .contract_validator import ContractValidator
from .reporter import generate_report, generate_ai_explanation   # <-- added AI function

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True)
    parser.add_argument("--token", required=True)
    parser.add_argument("--sql-path", default="models/")
    parser.add_argument("--fail-on-violation", default="true")
    args = parser.parse_args()

    client = OpenMetadataClient(args.host, args.token)
    analyzer = SQLAnalyzer()
    lineage = LineageChecker(client)
    quality = QualityChecker(client)
    contract = ContractValidator(client)

    sql_dir = Path(args.sql_path)
    sql_files = list(sql_dir.rglob("*.sql")) + list(sql_dir.rglob("*.yml"))

    violations = []   # each will contain 'table', 'message', 'ai_explanation'
    warnings = []
    impacts = []

    for file in sql_files:
        with open(file) as f:
            content = f.read()
        changes = analyzer.detect_changes(content)
        for change in changes:
            table_fqn = f"default.public.{change['table']}"  # Adjust FQN logic
            # Check lineage impact
            impact = lineage.check_impact(table_fqn)
            if impact["has_downstream"]:
                impacts.append({
                    "table": change['table'],
                    "count": impact['count'],
                    "severity": impact['severity'],
                    "tables": impact.get('tables', []),
                    "dashboards": impact.get('dashboards', [])
                })
            # Check contract (breaking changes)
            if change['operation'] in ('DROP', 'MODIFY'):
                col = change.get('column', '')
                val = contract.validate_column_change(table_fqn, col, change['operation'])
                if not val['valid']:
                    # 🔥 Generate AI explanation for this violation
                    ai_msg = generate_ai_explanation(
                        change_type="ALTER_TABLE",
                        table=change['table'],
                        column=col,
                        operation=change['operation'],
                        downstream_tables=impact.get('tables', []),
                        downstream_dashboards=impact.get('dashboards', []),
                        suggested_fix=val.get('suggested_fix', 'Review downstream dependencies before merging.')
                    )
                    violations.append({
                        "table": change['table'],
                        "message": val['message'],          # fallback technical message
                        "ai_explanation": ai_msg,          # new field for AI narrative
                        "ai_generated": True
                    })
            # Quality check (non-breaking)
            qual = quality.check_quality(table_fqn)
            if qual['warning']:
                warnings.append({"table": change['table'], "message": qual['message']})

    report = generate_report(violations, warnings, impacts)

    # Write GitHub output
    with open(os.environ.get('GITHUB_OUTPUT', '/dev/null'), 'a') as f:
        f.write(f"report<<EOF\n{report}\nEOF\n")
        f.write(f"has-violations={str(len(violations) > 0).lower()}\n")

    print(report)
    if args.fail_on_violation == "true" and violations:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()