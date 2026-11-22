# SpecForge AI

### AI Solution Design & Architecture Assessment Prototype

SpecForge AI is a rule-based prototype designed to support the **early-stage AI consulting and solution-design process**.

It converts an ambiguous client brief into a structured solution blueprint by extracting requirements, identifying missing information, classifying the AI use case, recommending an architecture, defining an MVP, refining requirements through discovery, assessing architecture coverage, identifying gaps, and generating prioritized implementation actions.

> **Current status:** Prototype complete  
> **Implementation:** Rule-based Python workflow with Streamlit interface

---

## 🎯 Problem

AI projects can become difficult to scope when client requirements are incomplete, ambiguous, or disconnected from the proposed technical architecture.

Before development begins, a solution team needs to understand:

- What business problem is being solved?
- What are the actual functional requirements?
- Is AI appropriate for the problem?
- What information is still missing?
- What solution type best fits the use case?
- Does the proposed architecture address the confirmed requirements?
- Where are the architectural gaps?
- What should be resolved before implementation?

SpecForge AI was built to structure this early-stage decision-making process.

---

## 🔄 End-to-End Workflow

```text
Client Brief
     ↓
Requirement Extraction
     ↓
Requirement Validation
     ↓
AI Use-Case Classification
     ↓
Solution Recommendation
     ↓
Architecture Recommendation
     ↓
MVP Scope Definition
     ↓
Client Discovery
     ↓
Discovery Refinement
     ↓
Architecture Coverage Assessment
     ↓
Architecture Gap Analysis
     ↓
Prioritized Implementation Actions
     ↓
Proposal Generation
```

The objective is to move from:

**"Here is what the client wants."**

to:

**"Here is what we understand, what is still unknown, how the solution could be designed, what gaps remain, and what should happen next."**

---

## 🧠 Core Capabilities

### 1. Requirement Analysis

SpecForge extracts structured requirements from a client brief and validates whether enough information is available for solution scoping.

It identifies areas such as:

- Business objectives
- Functional requirements
- AI requirements
- Data requirements
- Integration requirements
- Missing information
- Requirement uncertainty

---

### 2. AI Use-Case Classification

The system classifies potential AI applications into categories such as:

- Agentic AI Workflow
- RAG-based AI Application
- Recommendation System
- Data Analytics / BI
- Workflow Automation
- NLP / LLM
- Predictive Analytics

It then recommends a suitable solution type based on the requirements identified from the brief.

---

### 3. Architecture Recommendation

SpecForge generates a structured architecture blueprint covering:

```text
Frontend
Backend
AI Layer
Data Layer
Integrations
Deployment
```

For example, a RAG-based HR Policy Assistant can be mapped to components such as:

- Streamlit
- Python
- FastAPI
- Pydantic
- LLM
- Embeddings
- Vector Search
- RAG Pipeline
- PostgreSQL
- Docker
- Cloud deployment

The architecture is presented as a **recommendation**, rather than claiming that these components have already been implemented in production.

---

### 4. MVP Scoping

The proposed solution is separated into:

**MVP**

Core functionality required for the initial implementation.

**Phase 2**

Capabilities that can be introduced after the initial solution is validated.

**Out of Scope**

Requirements that should not be committed to until additional information or client decisions are available.

This helps prevent premature scope expansion.

---

### 5. Client Discovery

When requirements are incomplete, SpecForge generates discovery questions to obtain the information needed for solution design.

Example discovery areas include:

- Document storage
- Enterprise integrations
- Document permissions
- Authentication
- Policy update processes
- Citation requirements
- Insufficient-evidence handling
- Evaluation datasets

Client answers can then be incorporated into the refined solution proposal.

---

### 6. Architecture Coverage Assessment

After discovery, confirmed requirements are compared against the proposed architecture.

Each requirement receives an architecture status:

| Status | Meaning |
|---|---|
| **Covered** | The architecture explicitly addresses the requirement |
| **Partial** | Some architectural support exists, but details are missing |
| **Gap** | The requirement is not addressed |
| **Unknown** | The requirement itself has not yet been confirmed |

This separates **requirement certainty** from **architecture completeness**, which is important during early solution design.

---

### 7. Architecture Gap Analysis

Architecture gaps are converted into implementation actions.

Each action contains:

- Requirement
- Priority
- Architecture status
- Identified gaps
- Recommended action

For example:

```text
Requirement:
Policy versioning and re-indexing

Priority:
High

Architecture Status:
Partial

Identified Gaps:
- Approved update detection
- Version tracking
- Automatic re-indexing
- Stale document removal

Recommended Action:
Define update detection, re-indexing and stale-content removal.
```

This turns an architecture review into a practical implementation plan.

---

### 8. Proposal Generation

SpecForge can generate a structured solution proposal containing:

- Executive summary
- Business problem
- Proposed solution
- Architecture direction
- MVP scope
- Phase 2 considerations
- Out-of-scope items
- Discovery inputs
- Client-validation considerations

---

# 🖥️ Application Walkthrough

The following screenshots show the prototype from client brief analysis through architecture assessment and gap analysis.

### 1. Client Brief & Analysis

The application starts with a client brief and processes it through the SpecForge workflow.

![SpecForge AI — Client Analysis](screenshots/Screenshot%201.png)

---

### 2. Solution Blueprint

The system produces a structured solution recommendation including the proposed AI solution, architecture direction, MVP scope, and readiness assessment.

![SpecForge AI — Solution Blueprint](screenshots/Screenshot%202.png)

---

### 3. Discovery & Requirement Refinement

When additional information is required, SpecForge identifies unresolved requirements and generates discovery questions for client validation.

![SpecForge AI — Discovery](screenshots/Screenshot%203.png)

---

### 4. Discovery-Aware Proposal

Confirmed discovery inputs can be incorporated into a refined solution proposal, making the recommendation more specific to the client's environment.

![SpecForge AI — Refined Proposal](screenshots/Screenshot%204.png)

---

### 5. Architecture Coverage Overview

The architecture assessment compares the confirmed requirements against the proposed solution architecture.

![SpecForge AI — Coverage Overview](screenshots/Screenshot%205.png)

---

### 6. Requirement Review

Each requirement is reviewed independently based on its discovery status and architecture coverage.

![SpecForge AI — Requirement Review](screenshots/Screenshot%206.png)

---

### 7. Architecture Gap Analysis

Identified gaps are translated into prioritized implementation actions with recommended next steps.

![SpecForge AI — Gap Analysis](screenshots/Screenshot%207.png)

---

## 🏗️ Example Use Case: HR Policy Assistant

One of the demonstrated scenarios is an internal **HR Policy Assistant**.

The system identifies the use case as a:

**RAG-based AI Application**

The discovery workflow can capture requirements including:

- Microsoft SharePoint document storage
- PDF/DOCX support
- Policy versioning
- Document, section, and page citations
- Abstention when evidence is insufficient
- Conflicting-policy escalation
- HR-validated evaluation data
- Permission-aware document retrieval

The architecture assessment can then identify unresolved areas such as:

- SharePoint API integration
- Identity and SSO
- Permission-aware retrieval
- Automatic policy re-indexing
- Citation verification
- Evaluation dataset validation

These gaps are subsequently converted into prioritized implementation actions.

---

## 📊 Example Architecture Assessment

A representative assessment can distinguish between:

```text
Discovery Status
├── Confirmed
└── Unknown

Architecture Status
├── Covered
├── Partial
├── Gap
└── Unknown
```

This allows the system to answer two separate questions:

**"Did the client confirm this requirement?"**

and

**"Does the proposed architecture actually address it?"**

That distinction is central to the project's architecture-review workflow.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| **Python** | Core application and business logic |
| **Streamlit** | Interactive web interface |
| **Pandas** | Data handling and assessment visualization |
| **JSON** | Discovery data and structured outputs |
| **Python unittest** | Automated testing |

The current prototype primarily uses deterministic, rule-based logic for requirement analysis and solution recommendations.

---

## 📁 Project Structure

```text
SpecForge-AI/
│
├── app.py
├── specforge.py
├── test_specforge.py
├── discovery_answers.json
├── requirements.txt
├── README.md
├── .gitignore
│
└── screenshots/
    ├── Screenshot 1.png
    ├── Screenshot 2.png
    ├── Screenshot 3.png
    ├── Screenshot 4.png
    ├── Screenshot 5.png
    ├── Screenshot 6.png
    └── Screenshot 7.png
```

### `app.py`

Streamlit interface responsible for presenting the SpecForge workflow and its outputs.

### `specforge.py`

Core requirement extraction, validation, classification, architecture recommendation, discovery, assessment, gap analysis, and proposal-generation logic.

### `test_specforge.py`

Automated tests for validating the core SpecForge workflow.

### `discovery_answers.json`

Stored discovery inputs used to refine the generated solution.

---

## ▶️ Running the Application

Clone the repository:

```bash
git clone <repository-url>
cd SpecForge-AI
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🧪 Testing

Run the automated tests with:

```bash
python -m unittest test_specforge.py -v
```

The test suite validates key stages of the SpecForge workflow and helps ensure that changes do not break existing functionality.

---

## ⚠️ Current Implementation & Limitations

SpecForge AI is currently a **rule-based prototype**.

It does **not** currently use a live LLM API for requirement extraction or reasoning.

The current implementation uses deterministic Python logic to simulate an early-stage AI solution consulting workflow.

The prototype also does not currently implement:

- Live document ingestion
- Production vector database
- Live SharePoint integration
- Live Microsoft Entra ID authentication
- Production LLM inference
- Production monitoring
- Production deployment

These are intentionally outside the scope of the current prototype.

---

## 🚀 Future Production Evolution

The prototype provides a foundation that could be extended into a production AI-assisted solution-design platform.

### LLM-Powered Requirement Extraction

Replace deterministic extraction rules with an LLM capable of converting complex client briefs into structured requirements.

### RAG-Based Knowledge Layer

Introduce a knowledge base containing:

- Architecture patterns
- Technology capabilities
- Previous solution designs
- Industry-specific requirements
- Implementation patterns

This could allow recommendations to be grounded in reusable organizational knowledge.

### Agentic Workflow

Specialized AI agents could eventually support different stages of the process:

```text
Requirement Analyst
        ↓
AI Solution Architect
        ↓
Discovery Analyst
        ↓
Architecture Reviewer
        ↓
Proposal Generator
```

### Enterprise Integrations

Potential integrations could include:

- Microsoft SharePoint
- Microsoft Entra ID
- Enterprise document repositories
- CRM platforms
- Project management platforms

### Production Architecture

A future implementation could introduce:

```text
Streamlit / Web Frontend
          ↓
      FastAPI
          ↓
   Agent / LLM Layer
          ↓
 RAG + Vector Database
          ↓
     PostgreSQL
          ↓
Enterprise Integrations
```

with Docker, cloud deployment, authentication, monitoring, and evaluation pipelines.

---

## 💡 Why This Project

SpecForge AI focuses on a part of AI implementation that is often overlooked: **what happens before development begins**.

Rather than building only an individual AI model, the project demonstrates a structured approach to:

- Business requirement analysis
- Client discovery
- AI use-case classification
- Solution architecture
- MVP scoping
- Requirement uncertainty
- Architecture coverage
- Technical gap analysis
- Implementation prioritization
- Proposal generation

This makes the project relevant to **AI consulting, business analysis, solution architecture, and AI implementation** environments.

---

## 📌 Project Status

**Prototype Complete — Portfolio Ready**

The current prototype demonstrates an end-to-end solution-design workflow from:

**Client Brief → Requirements → AI Solution → Architecture → Discovery → Coverage Assessment → Gap Analysis → Implementation Actions**

The next stage would be replacing deterministic logic with production AI components and real enterprise integrations.
