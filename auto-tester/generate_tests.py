import os
import json
import requests
from pathlib import Path

def generate_data_dictionary():
    host = os.getenv("OPENMETADATA_HOST", "http://localhost:8585")
    token = os.getenv("OPENMETADATA_TOKEN", "")
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{host}/api/v1/tables?limit=100", headers=headers)
    tables = resp.json().get("data", [])
    md = ["# 📚 Data Dictionary\n\n"]
    for t in tables:
        md.append(f"## {t['name']}\n")
        md.append(f"**Description:** {t.get('description', 'No description')}\n")
        md.append(f"**Owner:** {t.get('owner', {}).get('name', 'Unknown')}\n")
        md.append(f"**Tags:** {', '.join([tag['tagFQN'] for tag in t.get('tags', [])])}\n\n")
        md.append("| Column | Type | Description |\n|--------|------|-------------|\n")
        for col in t.get("columns", []):
            md.append(f"| {col['name']} | {col['dataType']} | {col.get('description', '-')} |\n")
        md.append("\n---\n\n")
    Path("docs/data-dictionary.md").write_text("".join(md))
    print("✅ Data dictionary generated")

if __name__ == "__main__":
    generate_data_dictionary()


# //

def generate_great_expectations_tests():
    """Generate Great Expectations tests from OpenMetadata constraints"""
    host = os.getenv("OPENMETADATA_HOST")
    token = os.getenv("OPENMETADATA_TOKEN")
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{host}/api/v1/tables?limit=100", headers=headers)
    tables = resp.json().get("data", [])

    expectations = []
    for t in tables:
        fqn = t['fullyQualifiedName']
        for col in t.get("columns", []):
            if not col.get("nullable", True):
                expectations.append(f"expect_column_values_to_not_be_null('{col['name']}')")
            if col.get("dataType") == "numeric":
                expectations.append(f"expect_column_values_to_be_in_type_list('{col['name']}', ['int', 'float'])")
    # Write to file for Great Expectations
    Path("great_expectations/expectations.json").write_text(json.dumps(expectations, indent=2))
    print(f"✅ Generated {len(expectations)} expectations")