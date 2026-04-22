from .openmetadata_client import OpenMetadataClient
from typing import Dict

class ContractValidator:
    def __init__(self, client: OpenMetadataClient):
        self.client = client

    def validate_column_change(self, fqn: str, column: str, operation: str) -> Dict:
        contract = self.client.get_contract(fqn)
        if not contract:
            return {"valid": True, "message": "No contract found"}

        for col in contract.get("columns", []):
            if col.get("name") == column:
                constraints = col.get("constraints", [])
                if operation == "DROP" and "required" in constraints:
                    return {"valid": False, "message": f"Column '{column}' is required by contract"}
                if operation == "MODIFY" and "immutable" in constraints:
                    return {"valid": False, "message": f"Column '{column}' is immutable per contract"}
        return {"valid": True, "message": "Contract satisfied"}