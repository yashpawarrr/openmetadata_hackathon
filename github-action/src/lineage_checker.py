from .openmetadata_client import OpenMetadataClient
from typing import Dict

class LineageChecker:
    def __init__(self, client: OpenMetadataClient):
        self.client = client

    def check_impact(self, fqn: str) -> Dict:
        impact = self.client.get_downstream_impact(fqn)
        return {
            "has_downstream": impact["total"] > 0,
            "count": impact["total"],
            "tables": impact.get("tables", []),
            "dashboards": impact.get("dashboards", []),
            "severity": "HIGH" if impact["total"] > 0 else "LOW"
        }
    
    def estimate_full_scan_cost(table_fqn: str, client) -> str:
        """
        Returns human-readable cost estimate (e.g., "$2.50") based on table size.
        Assumes OpenMetadata stores 'tableSize' in bytes.
        """
        table = client.get_table_by_fqn(table_fqn)
        if not table:
            return "unknown (table metadata missing)"
        size_bytes = table.get("tableSize", 0)
        if size_bytes <= 0:
            return "negligible (table size unknown)"
        # Convert to terabytes (BigQuery: ~$5/TB scanned)
        size_tb = size_bytes / (1024 ** 4)
        cost = size_tb * 5.0
        if cost < 0.01:
            return "negligible (<$0.01)"
        return f"${cost:.2f}"