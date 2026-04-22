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
            "tables": impact["tables"],
            "dashboards": impact["dashboards"],
            "severity": "HIGH" if impact["total"] > 0 else "LOW"
        }