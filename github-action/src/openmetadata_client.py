import requests
import os
from typing import Dict, List, Optional, Any

class OpenMetadataClient:
    def __init__(self, host: str, token: str = None):
        self.host = host.rstrip('/')
        self.base_url = f"{self.host}/api/v1"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {token or os.getenv('OPENMETADATA_TOKEN', '')}"
        }

    def get_table_by_fqn(self, fqn: str) -> Optional[Dict]:
        url = f"{self.base_url}/tables/name/{fqn}"
        try:
            resp = requests.get(url, headers=self.headers)
            resp.raise_for_status()
            return resp.json()
        except:
            return None

    def get_lineage(self, fqn: str, downstream_depth: int = 3) -> Dict:
        url = f"{self.base_url}/lineage/table/name/{fqn}"
        params = {"upstreamDepth": 0, "downstreamDepth": downstream_depth}
        try:
            resp = requests.get(url, headers=self.headers, params=params)
            resp.raise_for_status()
            return resp.json()
        except:
            return {"downstreamEdges": [], "nodes": []}

    def get_downstream_impact(self, fqn: str) -> Dict:
        lineage = self.get_lineage(fqn, downstream_depth=5)
        impact = {"tables": [], "dashboards": [], "reports": [], "total": 0}
        for edge in lineage.get("downstreamEdges", []):
            entity = edge.get("toEntity", {})
            type_ = entity.get("type", "")
            name = entity.get("name", "")
            if type_ == "table":
                impact["tables"].append(name)
            elif type_ == "dashboard":
                impact["dashboards"].append(name)
            elif type_ == "report":
                impact["reports"].append(name)
        impact["total"] = len(impact["tables"]) + len(impact["dashboards"]) + len(impact["reports"])
        return impact

    def get_table_quality(self, fqn: str) -> Dict:
        """Get data quality status from OpenMetadata"""
        url = f"{self.base_url}/quality/table/{fqn}"
        try:
            resp = requests.get(url, headers=self.headers)
            resp.raise_for_status()
            return resp.json()
        except:
            return {"qualityScore": None, "tests": []}

    def get_contract(self, fqn: str) -> Dict:
        """Get data contract for a table (OpenMetadata v1.8+)"""
        url = f"{self.base_url}/contracts/table/{fqn}"
        try:
            resp = requests.get(url, headers=self.headers)
            resp.raise_for_status()
            return resp.json()
        except:
            return {"columns": [], "constraints": []}