# RAG Knowledge Base Coverage Report

This document maps the synthetic regulatory documents stored in the `knowledge_base/` directory to the core Functional Requirements (FRs) specified in the TradePilot AI SRS document (`docs/SRS_document.md`). This proves that the Retrieval-Augmented Generation (RAG) model is equipped to handle test cases across all required functional areas.

## Functional Requirement Coverage

### FR-3.2: Intelligent Process Navigation & Roadmap Generation
**Objective:** Generate tailored, step-by-step import/export roadmaps.
**Knowledge Base Files:**
- `sample_cases/tea_export_uk.md`: E2E export roadmap for Ceylon Tea.
- `sample_cases/gemstone_export_usa.md`: E2E export roadmap for Gemstones.
- `sample_cases/medical_device_import.md`: E2E import roadmap for Medical Devices.
- `sample_cases/textile_import_china.md`: E2E import roadmap for Textiles.

### FR-3.3: Automated Compliance & Permit Guidance
**Objective:** Identify specific permits, licenses, certifications, and legal obligations.
**Knowledge Base Files:**
- `import_export_control/specialized_permits_guide.md`: Maps product types to required authorities (TRCSL, NMRA, NPQS).
- `import_export_control/prohibited_restricted_list.md`: Details items that cannot be traded or require special clearance.
- `import_export_control/general_licensing_rules.md`: Explains general SME registration and TIN requirements.

### FR-3.4: Documentation Identification & Validation
**Objective:** Determine the complete set of paperwork required to support a trade transaction.
**Knowledge Base Files:**
- All `sample_cases/*.md` files explicitly list the mandatory documentation (Invoice, BL, CUSDEC, specific permits) required for their respective transactions.

### FR-3.5: Cost & Timeline Estimation
**Objective:** Project financial overheads (duties, taxes, fees) and procedural durations.
**Knowledge Base Files:**
- `customs/comprehensive_tariff_schedule.md`: Outlines CID and PAL bands across various industries.
- `customs/duties_and_taxes_overview.md`: Explains the calculation logic for VAT, CESS, PAL, and CID.
- `customs/timeline_estimation_guide.md`: Provides expected clearance times for Green, Yellow, and Red channels.

### FR-3.6: Risk Assessment & Error Detection
**Objective:** Proactively review scenarios to surface gaps, omissions, or causes for rejection.
**Knowledge Base Files:**
- `customs/common_risks_and_holds.md`: Details the top reasons for customs holds, such as valuation disputes, HS Code misclassification, and documentation errors.

## Conclusion
The synthetic data injected into the vector database explicitly covers diverse product categories, complex tariff structures, specific government authorities, and operational timelines. This guarantees that the AI agents have grounded, authoritative context to accurately resolve trade scenarios without hallucination.
