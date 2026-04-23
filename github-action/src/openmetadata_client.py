import requests
import os
import logging
from typing import Dict, List, Optional, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenMetadataClient:
    def __init__(self, host: str, token: str = None):
        self.host = host.rstrip('/')
        self.base_url = f"{self.host}/api/v1"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {token or os.getenv('OPENMETADATA_TOKEN', '')}"
        }
        self.timeout = 10

    def _request(self, method: str, path: str, params: dict = None) -> Optional[Dict]:
        url = f"{self.base_url}{path}"
        try:
            resp = requests.request(method, url, headers=self.headers, params=params, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"OpenMetadata API error: {e}")
            return None

    def get_table_by_fqn(self, fqn: str) -> Optional[Dict]:
        return self._request("GET", f"/tables/name/{fqn}")

    def get_lineage(self, fqn: str, downstream_depth: int = 3) -> Dict:
        data = self._request("GET", f"/lineage/table/name/{fqn}", params={"upstreamDepth": 0, "downstreamDepth": downstream_depth})
        return data if data else {"downstreamEdges": [], "nodes": []}

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
        data = self._request("GET", f"/quality/table/{fqn}")
        return data if data else {"qualityScore": None, "tests": []}

    def get_contract(self, fqn: str) -> Dict:
        data = self._request("GET", f"/contracts/table/{fqn}")
        return data if data else {"columns": [], "constraints": []}