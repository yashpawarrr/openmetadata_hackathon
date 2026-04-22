import sqlparse
import re
from pathlib import Path
from typing import Set, List, Dict

class SQLAnalyzer:
    def __init__(self):
        self.table_pattern = re.compile(r'(?:FROM|JOIN|INTO|UPDATE|TABLE)\s+([`"\']?([a-zA-Z0-9_\.]+)[`"\']?)', re.IGNORECASE)
        self.alter_pattern = re.compile(r'ALTER\s+TABLE\s+([^\s]+)\s+(ADD|DROP|MODIFY|CHANGE)\s+([^\s]+)', re.IGNORECASE)

    def extract_tables(self, sql: str) -> Set[str]:
        tables = set()
        for stmt in sqlparse.parse(sql):
            stmt_str = str(stmt).lower()
            for match in self.table_pattern.findall(stmt_str):
                name = match[1].strip('`"\'')
                if name and not name.startswith('('):
                    tables.add(name)
        return tables

    def detect_changes(self, sql: str) -> List[Dict]:
        changes = []
        for stmt in sqlparse.parse(sql):
            stmt_str = str(stmt).upper()
            match = self.alter_pattern.search(stmt_str)
            if match:
                changes.append({
                    "type": "ALTER_TABLE",
                    "table": match.group(1),
                    "operation": match.group(2),
                    "column": match.group(3),
                    "sql": str(stmt)
                })
            if "CREATE TABLE" in stmt_str:
                parts = stmt_str.split("CREATE TABLE")
                if len(parts) > 1:
                    table = parts[1].strip().split()[0]
                    changes.append({"type": "CREATE_TABLE", "table": table, "operation": "CREATE"})
            if "DROP TABLE" in stmt_str:
                parts = stmt_str.split("DROP TABLE")
                if len(parts) > 1:
                    table = parts[1].strip().split()[0]
                    changes.append({"type": "DROP_TABLE", "table": table, "operation": "DROP"})
        return changes

    def check_description_presence(self, sql: str) -> List[Dict]:
        """Check if new columns have descriptions (COMMENT clause)"""
        issues = []
        # Simple regex to find column definitions without COMMENT
        col_pattern = re.compile(r'(\w+)\s+[\w\(\)]+\s*(?:,|$)', re.IGNORECASE)
        for match in col_pattern.findall(sql):
            if "COMMENT" not in sql.upper():
                issues.append({"column": match, "issue": "Missing description"})
        return issues