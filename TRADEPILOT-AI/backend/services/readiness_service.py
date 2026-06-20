class ReadinessService:
    def calculate_score(self, checklist_state: dict) -> float:
        total = len(checklist_state)
        if total == 0:
            return 100.0
        completed = sum(1 for v in checklist_state.values() if v)
        return round((completed / total) * 100, 2)

readiness_service = ReadinessService()
