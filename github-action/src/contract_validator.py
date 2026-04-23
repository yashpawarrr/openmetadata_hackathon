from .openmetadata_client import OpenMetadataClient
from typing import Dict

class ContractValidator:
    def __init__(self, client: OpenMetadataClient):
        self.client = client

    def validate_column_change(self, fqn: str, column: str, operation: str) -> Dict:
        contract = self.client.get_contract(fqn)
        if not contract:
            return {"valid": True, "message": "No contract found", "suggested_fix": "Consider defining a contract for this table."}
        for col in contract.get("columns", []):
            if col.get("name") == column:
                constraints = col.get("constraints", [])
                if operation == "DROP" and "required" in constraints:
                    return {
                        "valid": False,
                        "message": f"Column '{column}' is required by contract",
                        "suggested_fix": "Re‑add the column or update the contract before dropping."
                    }
                if operation == "MODIFY" and "immutable" in constraints:
                    return {
                        "valid": False,
                        "message": f"Column '{column}' is immutable per contract",
                        "suggested_fix": "Create a new column instead of modifying."
                    }
        return {"valid": True, "message": "Contract satisfied", "suggested_fix": ""}