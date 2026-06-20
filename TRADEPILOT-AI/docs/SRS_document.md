# Software Requirements Specification

## AI Trade Compliance & Process Navigator
*(Project Codename: TradePilot AI)*

**Domain:** Government & Citizen Services
**Sub-Domain:** Import, Export, and Trade Compliance Services

**Document Version:** 1.0
**Status:** Draft
**Date:** June 20, 2026

---

## Document Control

### Revision History

| Version | Date | Author | Description |
|---|---|---|---|
| 1.0 | 2026-06-20 | Project Team (AI-assisted draft) | Initial Software Requirements Specification, derived from the project README and problem statement. |

### Approval

| Role | Name | Signature | Date |
|---|---|---|---|
| Project Sponsor | | | |
| Technical Lead | | | |
| QA Lead | | | |

This document is a working draft intended to capture functional and non-functional requirements as currently understood. Sections marked as assumptions or open items in Appendix B should be confirmed with project stakeholders prior to formal sign-off.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Overall Description](#2-overall-description)
3. [System Features (Functional Requirements)](#3-system-features-functional-requirements)
4. [External Interface Requirements](#4-external-interface-requirements)
5. [System Architecture Overview](#5-system-architecture-overview)
6. [Non-Functional Requirements](#6-non-functional-requirements)
7. [Data Requirements](#7-data-requirements)
8. [Other Requirements](#8-other-requirements)
- [Appendix A: Illustrative Use-Case Scenarios](#appendix-a-illustrative-use-case-scenarios)
- [Appendix B: Assumptions and Open Items Requiring Stakeholder Confirmation](#appendix-b-assumptions-and-open-items-requiring-stakeholder-confirmation)
- [Appendix C: Document Approval and Maintenance](#appendix-c-document-approval-and-maintenance)

---

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification (SRS) defines the functional and non-functional requirements for the AI Trade Compliance & Process Navigator (project codename "TradePilot AI"), an AI-powered platform designed to guide importers and exporters in Sri Lanka through the end-to-end cross-border trade compliance lifecycle. This document is intended to serve as the authoritative reference for design, development, testing, and stakeholder sign-off throughout the project lifecycle.

### 1.2 Project Scope

The platform accepts natural-language descriptions of a user's trade scenario and, using a Retrieval-Augmented Generation (RAG) pipeline combined with a multi-agent AI architecture, produces a personalized compliance roadmap, identifies required permits and documentation, estimates costs and timelines, flags compliance risks, and generates an actionable, trackable checklist. The system is intended to function as an advisory and process-navigation tool rather than a transaction-execution system.

**In scope (Phase 1 / MVP):** natural-language query intake; AI-generated roadmaps, compliance guidance, documentation checklists, cost and timeline estimates, and risk flags; a curated regulatory knowledge base grounded in Sri Lankan trade authorities; user accounts and saved trade scenarios; a dashboard for tracking readiness.

**Out of scope (Phase 1):** direct electronic submission of forms or permits to government systems on the user's behalf; processing or facilitation of duty/tax payments; real-time integration with Sri Lanka Customs transaction systems; legal representation or formal customs brokerage services. These are noted as candidate items for future phases in Section 2.7.

### 1.3 Intended Audience and Reading Suggestions

This document is intended for the project sponsor and stakeholders, the development and AI engineering team, quality assurance personnel, and any reviewing body evaluating the project (e.g., academic supervisors or government liaison reviewers). Readers seeking a high-level overview should read Sections 1 and 2. Readers responsible for implementation should focus on Sections 3 through 7. Section 8 and the appendices contain supporting reference material, open items, and illustrative scenarios.

### 1.4 Definitions, Acronyms, and Abbreviations

| Term | Definition |
|---|---|
| RAG | Retrieval-Augmented Generation — a technique that grounds AI-generated text in retrieved source documents to improve factual accuracy. |
| LLM | Large Language Model — the underlying AI model (Google Gemini) used to generate natural-language responses. |
| SME | Small and Medium Enterprise. |
| HS Code | Harmonized System Code — an internationally standardized numerical classification for traded products. |
| Knowledge Base | The curated collection of authoritative regulatory documents the platform retrieves from to ground its responses. |
| Roadmap | The personalized, step-by-step sequence of procedures generated for a user's specific trade scenario. |
| Readiness Report | A consolidated summary of a user's progress toward completing all compliance, documentation, and procedural requirements. |
| Agent (AI Agent) | A specialized AI component responsible for a discrete sub-task within the platform's multi-agent architecture. |
| Customs Clearance | The formal process by which goods are authorized to enter or leave a country through customs authorities. |
| Import and Export Control Department | The Sri Lankan government department responsible for regulating and licensing import and export activity. |

### 1.5 References

- Project README: "AI Trade Compliance & Process Navigator" (source document for this specification).
- Sri Lanka Customs official publications and guidelines.
- Sri Lanka Department of Import and Export Control circulars and publications.
- Google Gemini API documentation (for AI generation and reasoning components).
- IEEE Std 830-1998, Recommended Practice for Software Requirements Specifications (structural reference for this document).

### 1.6 Document Overview

Section 2 describes the product at a high level, including its target users, operating environment, and constraints. Section 3 details functional requirements organized by system feature. Section 4 specifies external interface requirements. Section 5 summarizes the proposed system architecture. Section 6 specifies non-functional requirements. Section 7 addresses data requirements, and Section 8 covers remaining cross-cutting requirements. Appendices provide illustrative use-case walkthroughs and a log of assumptions and open items requiring stakeholder confirmation.

---

## 2. Overall Description

### 2.1 Product Perspective

The AI Trade Compliance & Process Navigator is a new, standalone AI-powered platform rather than an extension of an existing system. It is positioned as a personalized trade companion rather than a generic question-answering chatbot: it transforms a free-text description of a trade scenario into a structured, actionable compliance roadmap. The platform depends on two external technical components: a Large Language Model service (Google Gemini) for natural-language understanding and generation, and a curated regulatory knowledge base assembled from authoritative Sri Lankan trade sources, against which all generated guidance is grounded using Retrieval-Augmented Generation.

### 2.2 Product Functions (Summary)

- Intelligent process navigation — generates tailored, step-by-step import/export roadmaps.
- Automated compliance guidance — identifies required permits, approvals, certifications, and documentation.
- Risk assessment — proactively detects missing compliance obligations and likely validation errors.
- Personalized checklist generation — produces actionable task lists and readiness reports.
- Cost and timeline awareness — projects estimated duties, taxes, fees, and procedural durations.

### 2.3 User Classes and Characteristics

| User Class | Category | Key Characteristics |
|---|---|---|
| First-time Importers & Exporters | Primary | Low to moderate familiarity with trade regulations; need step-by-step, plain-language guidance. |
| Small and Medium Enterprises (SMEs) | Primary | Limited in-house compliance expertise; cost- and timeline-sensitive. |
| Startup Founders & Individual Business Owners | Primary | Operate independently without dedicated compliance staff. |
| E-commerce Businesses | Primary | Expanding into cross-border logistics; need scenario-specific guidance per shipment type. |
| Trade Consultants & Customs Clearing Assistants | Secondary | Higher domain expertise; use the platform to verify current regulations. |
| Logistics Coordinators | Secondary | Need to align shipping workflows with compliance timelines. |
| Business Registration Service Providers | Secondary | Advise early-stage enterprises and reference platform output during onboarding. |
| Export Development Support Organizations | Secondary | Use the platform to streamline guidance delivered to local producers. |

### 2.4 Operating Environment

The platform is delivered as a web-based application accessible through modern desktop and mobile browsers, with backend services hosted in a cloud environment. The system requires an active internet connection for both the user-facing interface and backend communication with the Gemini API and the regulatory knowledge base index. No specialized client hardware or local software installation is required.

### 2.5 Design and Implementation Constraints

- The system depends on a third-party LLM provider (Google Gemini); its availability, latency, and rate limits constrain system responsiveness and must be accounted for in the design.
- Generated guidance must be strictly grounded in retrieved regulatory source material; the architecture must prevent ungrounded model output from being presented to users as authoritative compliance guidance, given the legal and financial consequences of incorrect trade advice.
- Government-published source data may be unstructured, inconsistently formatted, or infrequently updated, constraining the completeness and freshness of the knowledge base.
- The platform must clearly communicate that it provides advisory guidance and does not replace licensed customs brokers, trade consultants, or formal legal counsel.
- Phase 1 does not integrate with government e-filing or payment systems; all formal submissions remain the responsibility of the user or their appointed agent.

### 2.6 Assumptions and Dependencies

- Sri Lanka Customs, the Department of Import and Export Control, and other relevant authorities continue to publish regulatory information that is accessible for inclusion in the knowledge base.
- Access to the Google Gemini API remains available under terms suitable for production use.
- Target users have basic digital literacy and access to an internet-connected device.
- Final regulatory decisions and formal submissions remain the responsibility of the user, their customs agent, or relevant licensed professional; the platform's output is advisory.
- The knowledge base will require an ongoing content-maintenance process to remain accurate as regulations change; this is treated as an operational dependency rather than a one-time setup task.

### 2.7 Apportioning of Requirements (Phasing)

The functional requirements in Section 3 represent the Phase 1 (MVP) scope of the platform. The following candidate capabilities are identified as potential future enhancements and are out of scope for the initial release:

- Direct electronic submission/e-filing integration with Sri Lanka Customs or the Department of Import and Export Control systems.
- Integrated payment processing for duties, taxes, and regulatory fees.
- Full multilingual support (Sinhala and Tamil) beyond English-language interaction.
- Native mobile applications (Phase 1 targets responsive web access).
- Predictive analytics for customs delay forecasting based on historical clearance data.

These items should be revisited with stakeholders once Phase 1 is validated; see Appendix B for related open items.

---

## 3. System Features (Functional Requirements)

This section specifies the functional requirements of the platform, organized by system feature. Each feature corresponds to a specialized AI agent or core platform capability described in the system architecture (Section 5). Functional requirement identifiers follow the pattern FR-\<feature\>.\<number\>.

### 3.1 Natural Language Query Intake & Intent Analysis

**Corresponding Agent / Component:** Intent Analysis Agent

Allows a user to describe a trade scenario in plain, conversational language (for example, "I want to export cinnamon to Dubai" or "What approvals do I need to import electronic devices?"). The system parses the request to determine the trade direction, product category, origin and destination markets, and the user's underlying objective before any downstream processing begins.

**Priority:** High

**Functional Requirements:**
- **FR-3.1.1** The system shall accept free-text trade-related queries through a conversational interface.
- **FR-3.1.2** The system shall identify trade direction (import or export) from the user's query.
- **FR-3.1.3** The system shall extract product category, Harmonized System (HS) code candidates, origin country, and destination country from the query where present.
- **FR-3.1.4** The system shall prompt the user for clarification when mandatory scenario details (e.g., product or destination) are missing or ambiguous.
- **FR-3.1.5** The system shall classify the user's intent (e.g., process discovery, documentation check, cost estimate, risk check) to route the request to the relevant downstream agents.

**Inputs:** Free-text user query; optional structured profile data (business type, prior trade history).

**Outputs:** Structured intent object containing trade type, product category, origin/destination markets, and identified sub-intents, passed to the Workflow Planning Agent and other downstream agents.

### 3.2 Intelligent Process Navigation & Roadmap Generation

**Corresponding Agent / Component:** Workflow Planning Agent

Generates a tailored, step-by-step roadmap of the procedures a user must follow to complete their specific import or export scenario, sequencing government approvals, customs steps, and supporting actions in the correct order.

**Priority:** High

**Functional Requirements:**
- **FR-3.2.1** The system shall generate an end-to-end, sequential roadmap of the procedural steps required for the user's specific trade scenario.
- **FR-3.2.2** The system shall tailor the roadmap to the product category, trade direction, and origin/destination markets identified in the user's query.
- **FR-3.2.3** The system shall identify the relevant government agencies and authorities involved at each step of the roadmap.
- **FR-3.2.4** The system shall present the roadmap in a structured, easy-to-follow format suitable for non-specialist users.
- **FR-3.2.5** The system shall allow the user to revise scenario details and regenerate an updated roadmap.

**Inputs:** Structured intent object from the Intent Analysis Agent; retrieved regulatory context from the knowledge base.

**Outputs:** Ordered roadmap of procedural steps, responsible agencies, and dependencies between steps.

### 3.3 Automated Compliance & Permit Guidance

**Corresponding Agent / Component:** Compliance Verification Agent

Identifies and explains the specific permits, licenses, certifications, and legal obligations that apply to the user's declared product and trade route, grounded in authoritative regulatory sources.

**Priority:** High

**Functional Requirements:**
- **FR-3.3.1** The system shall identify all permits, licenses, and certifications applicable to the declared product category and trade route.
- **FR-3.3.2** The system shall map each identified requirement to the specific regulatory source or circular that mandates it.
- **FR-3.3.3** The system shall flag product categories that are restricted, prohibited, or subject to special licensing conditions.
- **FR-3.3.4** The system shall indicate which compliance obligations are mandatory versus conditional (e.g., dependent on quantity, value, or destination country).
- **FR-3.3.5** The system shall clearly indicate when a compliance requirement could not be verified against the knowledge base, rather than presenting an unverified answer as fact.

**Inputs:** Structured intent object; retrieved regulatory passages from the knowledge base.

**Outputs:** List of applicable permits/certifications with source attribution and mandatory/conditional status.

### 3.4 Documentation Identification & Validation

**Corresponding Agent / Component:** Documentation Agent

Determines the complete set of paperwork required to support a trade transaction and helps the user assess whether their documentation is likely to be complete before formal submission.

**Priority:** High

**Functional Requirements:**
- **FR-3.4.1** The system shall generate a list of mandatory documents required for the user's specific trade scenario.
- **FR-3.4.2** The system shall describe the purpose and issuing authority of each required document.
- **FR-3.4.3** The system shall allow the user to mark documents as prepared, in progress, or not started.
- **FR-3.4.4** The system shall identify commonly occurring documentation errors associated with the relevant product category or trade route.
- **FR-3.4.5** The system shall highlight missing mandatory documents prior to a user marking their checklist as complete.

**Inputs:** Roadmap and compliance output from upstream agents; user-reported document status.

**Outputs:** Document checklist with status tracking and completeness indicators.

### 3.5 Cost & Timeline Estimation

**Corresponding Agent / Component:** Cost Estimation Agent

Projects the likely financial overheads and procedural durations associated with a trade scenario, helping users plan their operations and cash flow with greater confidence.

**Priority:** Medium

**Functional Requirements:**
- **FR-3.5.1** The system shall provide an estimated breakdown of customs duties, taxes, port charges, and regulatory fees applicable to the scenario.
- **FR-3.5.2** The system shall provide an estimated timeline for each major stage of the roadmap (e.g., permit approval, customs clearance, inspection).
- **FR-3.5.3** The system shall clearly label all cost and timeline figures as estimates and indicate the regulatory basis or assumptions used to generate them.
- **FR-3.5.4** The system shall allow the user to adjust scenario parameters (e.g., declared value, quantity) and receive an updated estimate.
- **FR-3.5.5** The system shall flag when insufficient information is available to produce a reliable cost or timeline estimate.

**Inputs:** Roadmap and compliance output; user-supplied transaction parameters (declared value, quantity, mode of transport).

**Outputs:** Itemized cost estimate and stage-by-stage timeline projection.

### 3.6 Risk Assessment & Error Detection

**Corresponding Agent / Component:** Risk Assessment Agent

Proactively reviews a user's scenario and declared readiness to surface gaps, omissions, or likely causes of rejection, delay, or regulatory audit before the user proceeds with formal submission.

**Priority:** High

**Functional Requirements:**
- **FR-3.6.1** The system shall identify missing compliance obligations or documentation gaps based on the user's declared scenario and checklist status.
- **FR-3.6.2** The system shall highlight conditions that commonly cause customs holds, shipment delay, or formal compliance investigation for the relevant product or route.
- **FR-3.6.3** The system shall assign a relative risk indicator (e.g., low/medium/high) to flagged issues to help the user prioritize remediation.
- **FR-3.6.4** The system shall provide a recommended corrective action for each flagged risk where applicable.

**Inputs:** Outputs from the Workflow Planning, Compliance Verification, and Documentation agents; user checklist status.

**Outputs:** List of flagged risks with severity indicators and recommended remediation actions.

### 3.7 Checklist & Readiness Report Generation

**Corresponding Agent / Component:** Checklist Generation Agent

Consolidates the outputs of the other agents into a single, actionable checklist and a readiness report that gives the user a consolidated view of their progress toward a compliant, well-documented trade transaction.

**Priority:** High

**Functional Requirements:**
- **FR-3.7.1** The system shall consolidate roadmap steps, compliance requirements, and documentation items into a single interactive checklist.
- **FR-3.7.2** The system shall calculate and display an overall readiness score or status based on completed versus outstanding checklist items.
- **FR-3.7.3** The system shall allow the user to export or save the checklist and readiness report.
- **FR-3.7.4** The system shall update the readiness report automatically as the user updates checklist item status.

**Inputs:** Outputs from the Workflow Planning, Compliance Verification, Documentation, Cost Estimation, and Risk Assessment agents.

**Outputs:** Consolidated, trackable checklist and a readiness summary report.

### 3.8 RAG Knowledge Retrieval & Grounding Engine

**Corresponding Agent / Component:** Retrieval-Augmented Generation pipeline

Underpins every agent in the platform by retrieving relevant passages from an authoritative knowledge base and injecting them into the language model's context, ensuring that generated guidance is grounded in verifiable regulatory sources rather than the model's unguided output.

**Priority:** High

**Functional Requirements:**
- **FR-3.8.1** The system shall retrieve relevant regulatory passages from the authoritative knowledge base for each user query before generating a response.
- **FR-3.8.2** The system shall inject retrieved passages into the language model context as the evidentiary basis for generated responses.
- **FR-3.8.3** The system shall attribute generated guidance to its supporting source document(s) wherever the knowledge base provides a match.
- **FR-3.8.4** The system shall maintain a knowledge base sourced from Sri Lanka Customs guidelines, Import and Export Control Department publications, government circulars and trade regulations, product-specific compliance manuals, and customs documentation frameworks.
- **FR-3.8.5** The system shall support periodic re-ingestion of updated regulatory source material into the knowledge base.

**Inputs:** User query/intent; the curated regulatory knowledge base.

**Outputs:** Retrieved, contextualized regulatory passages supplied to the relevant agent(s) prior to response generation.

### 3.9 User Account, Profile & Trade Scenario Management

**Corresponding Agent / Component:** Platform / Account services

Allows users to register, manage a basic business profile, and save trade scenarios so that roadmaps, checklists, and reports can be revisited and updated over time rather than regenerated from scratch.

**Priority:** Medium

**Functional Requirements:**
- **FR-3.9.1** The system shall allow a user to create and authenticate an account.
- **FR-3.9.2** The system shall allow a user to maintain a basic business profile (e.g., business type, primary trade activity).
- **FR-3.9.3** The system shall allow a user to save a trade scenario and its associated roadmap, checklist, and reports for later access.
- **FR-3.9.4** The system shall allow a user to manage multiple saved trade scenarios independently.

**Inputs:** User registration and profile data; saved scenario data.

**Outputs:** Persisted user accounts, profiles, and trade scenarios.

### 3.10 Query History & Roadmap Tracking Dashboard

**Corresponding Agent / Component:** Platform / Dashboard services

Provides users with a consolidated dashboard view of their past queries, generated roadmaps, and checklist progress, supporting ongoing operational planning across multiple trade transactions.

**Priority:** Medium

**Functional Requirements:**
- **FR-3.10.1** The system shall display a history of a user's previous queries and generated roadmaps.
- **FR-3.10.2** The system shall display the current readiness status of each saved trade scenario.
- **FR-3.10.3** The system shall allow a user to resume work on a previously saved scenario from the dashboard.
- **FR-3.10.4** The system shall allow a user to delete saved scenarios and associated history.

**Inputs:** Saved user scenario, checklist, and history data.

**Outputs:** Dashboard view summarizing scenario status and history.

---

## 4. External Interface Requirements

### 4.1 User Interfaces

- The system shall provide a conversational, chat-style interface for natural-language query entry.
- The system shall provide a structured dashboard view presenting the generated roadmap, checklist, cost/timeline estimate, and risk flags for a given trade scenario.
- The user interface shall be responsive and usable on both desktop and mobile browser viewports.
- The user interface shall present generated guidance in plain, non-technical language suitable for first-time traders, while still providing access to underlying source citations for users who want them.
- The user interface shall target WCAG 2.1 Level AA accessibility guidelines as a baseline design objective.

### 4.2 Hardware Interfaces

The system has no dependency on specialized hardware. It is accessed via standard client devices (desktop, laptop, tablet, or smartphone) capable of running a modern web browser.

### 4.3 Software Interfaces

| Interface | Purpose |
|---|---|
| Google Gemini API | Provides natural-language understanding, reasoning, and generation for all AI agents. |
| Regulatory Knowledge Base / Vector Index | Stores embedded representations of authoritative regulatory source documents for retrieval during RAG processing. |
| Knowledge Base Ingestion Pipeline | Periodically ingests updated government circulars, customs guidelines, and compliance manuals into the knowledge base. |
| Authentication Service | Manages user registration, login, and session management. |
| Application Database | Persists user profiles, saved trade scenarios, checklists, and query history. |

### 4.4 Communications Interfaces

- All communication between the client application and backend services shall use HTTPS.
- All communication between backend services and the Gemini API shall be encrypted in transit.
- The system shall implement timeout and retry handling for external API calls to the LLM provider.

---

## 5. System Architecture Overview

The platform combines two architectural patterns: a Retrieval-Augmented Generation (RAG) pipeline that grounds all generated content in authoritative sources, and a multi-agent AI architecture in which specialized agents collaborate to resolve the distinct facets of a trade compliance scenario.

### 5.1 Retrieval-Augmented Generation (RAG) Workflow

- **Step 1 — User Request:** the user submits an import/export query in natural language.
- **Step 2 — Information Retrieval:** the system queries the authoritative regulatory knowledge base for relevant passages.
- **Step 3 — Contextualization:** retrieved regulatory documents are parsed and injected into the model context as evidentiary grounding.
- **Step 4 — Response Generation:** the Google Gemini model synthesizes a roadmap and supporting guidance strictly based on the injected regulatory evidence.

This pipeline exists specifically to minimize hallucinated or unsupported regulatory claims, which carry meaningful legal and financial risk for end users.

### 5.2 Multi-Agent Architecture

Specialized agents operate in coordination to resolve the multiple facets of a trade compliance request. Each agent corresponds to one of the system features specified in Section 3.

| Agent | Core Responsibility |
|---|---|
| Intent Analysis Agent | Identifies the user's objective, trade type, product category, and target/origin markets. |
| Workflow Planning Agent | Generates the tailored, sequential end-to-end trade process roadmap. |
| Compliance Verification Agent | Evaluates and isolates the specific permits, certifications, and legal obligations required. |
| Documentation Agent | Identifies mandatory paperwork and validates documentation completeness. |
| Cost Estimation Agent | Provides granular, calculated estimates for duties, taxes, tariffs, and related fees. |
| Risk Assessment Agent | Pinpoints potential causes of rejection, shipment delay, or regulatory audit. |
| Checklist Generation Agent | Outlines actionable checklists and structured readiness reports. |

### 5.3 Orchestration Flow

At a high level, a user query is first processed by the Intent Analysis Agent to establish trade direction, product category, and origin/destination markets. This structured intent, together with retrieved knowledge base context, is then distributed to the Workflow Planning, Compliance Verification, Documentation, Cost Estimation, and Risk Assessment agents, which operate on the shared context to produce their respective outputs. The Checklist Generation Agent consolidates these outputs into a unified roadmap, checklist, and readiness report that is returned to the user through the dashboard interface.

---

## 6. Non-Functional Requirements

The quantitative targets in this section are proposed working targets for design and testing purposes. They should be validated and, where necessary, revised with project stakeholders during detailed design, as they are not derived from a measured production baseline.

### 6.1 Performance Requirements

- The system should return an initial roadmap response for a well-formed query within a target of 10–15 seconds under normal load, acknowledging that multi-agent orchestration and LLM inference introduce inherent latency.
- The system should provide visible progress indication to the user while a multi-agent response is being generated.
- The knowledge base retrieval step should complete within a target of 2 seconds per query under normal load.

### 6.2 Accuracy and Reliability of Guidance

- Generated compliance guidance shall be grounded in retrieved knowledge base content rather than unsupported model output.
- Where the knowledge base does not contain sufficient information to answer a query reliably, the system shall explicitly communicate this limitation to the user rather than presenting a best-guess answer as authoritative.
- The system shall attribute compliance claims to their supporting source document or circular wherever available.

### 6.3 Security Requirements

- User data shall be encrypted in transit (TLS) and at rest.
- User authentication credentials shall be stored using industry-standard hashing and salting practices.
- API keys and credentials for third-party services (including the Gemini API) shall be stored in a secure secrets management mechanism and never exposed to the client.
- The system shall apply role-based access control where administrative functions (e.g., knowledge base content management) are distinct from end-user functions.
- Business-sensitive information entered by users (e.g., declared trade values, product details) shall be accessible only to the originating account unless explicitly shared.

### 6.4 Usability

- Generated guidance shall be written in plain language appropriate for users without specialized trade or legal training.
- The interface shall be navigable by a first-time user without requiring external training material, supported by in-app onboarding guidance.
- The system shall support responsive layouts for both desktop and mobile browser access.

### 6.5 Availability and Reliability

- The platform should target a production availability objective of 99.5% uptime, excluding scheduled maintenance windows.
- The system shall degrade gracefully and present a clear status message to the user when the LLM provider or knowledge base service is unavailable, rather than failing silently.

### 6.6 Scalability

- The multi-agent architecture shall be designed to allow individual agents to be scaled independently based on observed load.
- The system shall be designed to accommodate growth in concurrent users and query volume without requiring architectural redesign for at least an initial target of low-to-moderate production traffic, to be refined with usage data.

### 6.7 Maintainability

- The regulatory knowledge base shall be updatable through a content ingestion process that does not require a full application redeployment.
- Knowledge base source documents shall be versioned with an effective date to support traceability of which regulatory version informed a given response.

### 6.8 Portability

As a browser-based application, the platform shall be accessible from any modern, standards-compliant web browser without requiring platform-specific client software.

### 6.9 Legal, Compliance, and Disclaimer Requirements

- The system shall display a clear disclaimer that the platform provides informational and advisory guidance and does not constitute formal legal, tax, or customs brokerage advice.
- The system shall recommend that users verify critical compliance determinations with a licensed customs agent or relevant government authority before formal submission.
- The system shall comply with applicable Sri Lankan data protection requirements regarding the collection, storage, and processing of user and business data.

---

## 7. Data Requirements

### 7.1 Input Data

- Free-text trade query submitted by the user.
- Structured scenario parameters: trade direction, product category, origin and destination markets, declared value, quantity, and mode of transport (where provided).
- Optional business profile data: business type and prior trade history.
- User-reported document and checklist status.

### 7.2 Knowledge Base Data Sources

- Sri Lanka Customs guidelines.
- Import and Export Control Department publications.
- Government circulars and explicit trade regulations.
- Product-specific compliance manuals and permit requirements.
- Customs procedures and documentation frameworks.

### 7.3 Data Storage and Retention

- User accounts, profiles, and saved trade scenarios shall be persisted in the application database.
- Generated roadmaps, checklists, and readiness reports shall be persisted and associated with the originating user account.
- An audit record shall be retained linking each generated compliance claim to the regulatory source(s) used to ground it, to support traceability and review.
- Data retention periods for user-generated content shall be defined in consultation with legal/compliance stakeholders (see Appendix B).

### 7.4 Data Privacy

- The system shall collect only the personal and business data necessary to provide the platform's core functionality.
- The system shall obtain user consent prior to storing account and scenario data.
- The system shall provide users with the ability to view and delete their saved scenario data.

---

## 8. Other Requirements

### 8.1 Localization

Phase 1 of the platform operates in English. Given Sri Lanka's multilingual SME base, Sinhala and Tamil language support is identified as a high-value candidate for a future phase (see Section 2.7) and should be evaluated for prioritization based on user research.

### 8.2 Regulatory Update Process

Because trade regulations change over time, the platform requires an operational process — not only a technical one — for periodically reviewing and re-ingesting updated government circulars and customs guidelines into the knowledge base. Ownership of this process should be assigned during project planning.

### 8.3 Training and Support Materials

In-app onboarding content should be provided to help first-time users understand how to phrase queries, interpret generated roadmaps, and use the checklist and readiness report features.

---

## Appendix A: Illustrative Use-Case Scenarios

The following scenarios illustrate how the platform's features apply to representative user queries. These are illustrative only and do not represent verified regulatory outcomes.

**Scenario 1: Cinnamon Export to Dubai**

A user submits the query "I want to export cinnamon to Dubai." The Intent Analysis Agent identifies the trade direction (export), product category (cinnamon — a spice/agricultural product), and destination market (United Arab Emirates). The Workflow Planning Agent generates a roadmap covering relevant export procedures; the Compliance Verification Agent identifies applicable phytosanitary or agricultural export certifications; the Documentation Agent lists required export paperwork; the Cost Estimation Agent projects associated fees; the Risk Assessment Agent flags any product-specific risk factors; and the Checklist Generation Agent consolidates these into a trackable readiness report.

**Scenario 2: Electronic Device Imports**

A user submits the query "What approvals do I need to import electronic devices?" The platform identifies the trade direction (import) and product category (electronics), then surfaces applicable import licensing, standards compliance, and certification requirements, along with the documentation and cost implications specific to electronic goods.

---

## Appendix B: Assumptions and Open Items Requiring Stakeholder Confirmation

This document was produced from the available project README and problem statement. The following items are explicitly flagged as assumptions or gaps that should be confirmed or resolved with project stakeholders before this SRS is finalized for sign-off:

- Specific hosting/cloud infrastructure provider and deployment environment have not been specified and are assumed to be a standard cloud platform.
- Exact performance SLAs (response time, uptime) are proposed targets pending stakeholder validation; no measured baseline currently exists.
- Scope and timeline for multilingual (Sinhala/Tamil) support has not been defined and is listed as a future-phase candidate only.
- Whether the platform will pursue formal integration or partnership discussions with Sri Lanka Customs or the Department of Import and Export Control has not been confirmed.
- Data retention periods and formal data protection compliance obligations require review with legal/compliance stakeholders.
- Pricing/monetization model (free, subscription, per-query, government-funded) has not been defined and is outside the scope of this SRS.
- The specific scope of "customs procedures and documentation frameworks" as a knowledge base source should be itemized in detail during knowledge base design.

---

## Appendix C: Document Approval and Maintenance

This SRS should be treated as a living document during the design and development phases. Material changes to scope, features, or non-functional targets should be reflected through a new entry in the Revision History table (Document Control) rather than silent edits, to preserve traceability for all project stakeholders.