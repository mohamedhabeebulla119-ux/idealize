import json
from agents.compliance_agent import ComplianceAgent
from agents.risk_agent import RiskAgent
from agents.workflow_agent import WorkflowAgent
from agents.agency_recommendation_agent import AgencyRecommendationAgent
from agents.checklist_agent import ChecklistAgent

def run_tests():
    print("Initializing Agents...")
    compliance_agent = ComplianceAgent()
    risk_agent = RiskAgent()
    workflow_agent = WorkflowAgent()
    agency_agent = AgencyRecommendationAgent()
    checklist_agent = ChecklistAgent()

    trade_type = "export"
    product = "Cinnamon (HS Code 0906)"
    country = "Dubai"
    documents = ["Commercial Invoice", "Packing List"]
    approvals = []

    print("\n=============================================")
    print(f"Testing Scenario: {trade_type.capitalize()}ing {product} to {country}")
    print("=============================================\n")

    # 1. Agency Recommendation Agent
    print("--- 1. AgencyRecommendationAgent ---")
    agencies = agency_agent.recommend_agencies(trade_type, product, country)
    print(json.dumps(agencies, indent=2))

    # 2. Compliance Agent
    print("\n--- 2. ComplianceAgent ---")
    compliance = compliance_agent.check_compliance(trade_type, product, country)
    print(json.dumps(compliance, indent=2))

    # 3. Workflow Agent
    print("\n--- 3. WorkflowAgent ---")
    workflow = workflow_agent.generate_workflow(trade_type, product, country)
    print(json.dumps(workflow, indent=2))

    # 4. Risk Agent
    print("\n--- 4. RiskAgent ---")
    risks = risk_agent.analyze_risks(trade_type, product, country, documents, approvals)
    print(json.dumps(risks, indent=2))

    # 5. Checklist Agent
    print("\n--- 5. ChecklistAgent ---")
    checklist = checklist_agent.generate_checklist(trade_type, product, documents, approvals)
    print(json.dumps(checklist, indent=2))

    # --- EDGE CASE TEST ---
    trade_type_edge = "import"
    product_edge = "Fictional Hyper-Drive Core (HS Code 9999)"
    country_edge = "Mars"
    print("\n=============================================")
    print(f"Testing Edge Case: {trade_type_edge.capitalize()}ing {product_edge} from {country_edge}")
    print("=============================================\n")
    
    compliance_edge = compliance_agent.check_compliance(trade_type_edge, product_edge, country_edge)
    print("--- ComplianceAgent (Edge Case) ---")
    print(json.dumps(compliance_edge, indent=2))

if __name__ == "__main__":
    run_tests()
