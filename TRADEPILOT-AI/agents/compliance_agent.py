class ComplianceAgent:
    def __init__(self):
        self.name = "Compliance Agent"

    def process(self, input_data: str) -> str:
        return f"[{self.name}] Processed output for: {input_data}"
