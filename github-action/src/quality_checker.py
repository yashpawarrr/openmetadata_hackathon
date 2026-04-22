from .openmetadata_client import OpenMetadataClient
from typing import Dict

class QualityChecker:
    def __init__(self, client: OpenMetadataClient):
        self.client = client

    def check_quality(self, fqn: str) -> Dict:
        quality = self.client.get_table_quality(fqn)
        if quality.get("qualityScore") and quality["qualityScore"] < 0.7:
            return {
                "warning": True,
                "message": f"Table has low quality score: {quality['qualityScore']}",
                "score": quality["qualityScore"]
            }
        return {"warning": False}