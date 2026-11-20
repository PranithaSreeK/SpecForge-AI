from pydantic import BaseModel
 
 
 
class Requirements(BaseModel):
    business_objective: str
    users: list[str]
    pain_points: list[str]
    functional_requirements: list[str]
    non_functional_requirements: list[str]
    data_sources: list[str]
    integrations: list[str]
    constraints: list[str]
    success_metrics: list[str]
 
 
def mock_llm_extract_requirements(client_brief):
    """Rule-based prototype extractor; not a real LLM."""
    text = client_brief.lower()
 
    objective = ""
    pain_points = []
    functions = []
    users = []
    data_sources = []
    success_metrics = []
 
    if "forecast" in text or "demand" in text:
        objective = "Forecast product demand to improve inventory planning"
        pain_points = ["Demand uncertainty"]
        functions = ["Forecast future product demand"]
        users = ["Inventory planners"]
        data_sources = ["Historical sales data"]
        success_metrics = ["Forecast error"]
 
    
    elif any(word in text for word in [
    "document", "policy", "handbook", "internal procedures",
    "source citations", "cite the source", "employee questions"
]):
        objective = (
            "Help employees find reliable answers from internal policy documents"
        )
        pain_points = [
            "Employees spend too much time searching across policy documents",
            "HR receives repeated questions",
            "Answers need to be supported by approved sources"
        ]
        functions = [
            "Search approved documents and answer employee questions",
            "Cite source documents and relevant sections",
            "Decline to answer when supporting evidence is insufficient",
            "Enforce employee document-access permissions"
        ]
        users = ["Employees", "HR teams"]
        data_sources = ["Internal policy documents and PDF files"]
        success_metrics = [
            "Answer accuracy",
            "Source citation accuracy",
            "Unanswered-question handling",
            "Employee time to find policy information"
        ]
 
 
    elif "ticket" in text or "support" in text:
        objective = "Improve customer support ticket handling"
        pain_points = ["Time-consuming ticket processing"]
        functions = [
            "Categorize support tickets",
            "Prioritize urgent tickets",
            "Route tickets to the appropriate team"
        ]
        users = ["Customer support teams"]
        data_sources = ["Support ticket records"]
        success_metrics = ["Ticket resolution time"]
 
    elif "recommend" in text or "product suggestions" in text:
        objective = "Personalize product recommendations"
        pain_points = ["Generic product suggestions"]
        functions = ["Recommend relevant products"]
        users = ["Customers"]
        data_sources = ["Customer purchase history"]
        success_metrics = ["Recommendation click-through rate"]
 
    elif any(word in text for word in ["dashboard", "kpi", "revenue"]):
        objective = "Improve visibility into business performance"
        pain_points = ["Limited performance visibility"]
        functions = ["Display business KPIs and trends"]
        users = ["Business managers"]
        data_sources = ["Sales and operational data"]
        success_metrics = ["Reporting turnaround time"]
 
        
    elif "invoice" in text:
        objective = "Automate invoice processing and validation"
        pain_points = [
            "Manual invoice processing takes finance staff time",
            "Invoice errors and exceptions require review"
        ]
        functions = [
            "Extract invoice numbers, dates, vendor names, tax amounts, and totals",
            "Validate extracted invoice fields",
            "Flag exceptions for human review"
        ]
        users = ["Finance staff", "Accounts payable teams"]
        data_sources = ["PDF invoices"]
        success_metrics = [
            "Invoice processing time",
            "Invoice extraction accuracy"
        ]
 
    elif any(word in text for word in ["onboarding", "new employee", "employee joins"]):
        objective = "Automate employee onboarding administration"
        pain_points = [
            "Manual coordination of onboarding tasks",
            "Missed tasks and follow-ups"
        ]
        functions = [
            "Trigger onboarding checklists",
            "Assign onboarding tasks",
            "Send reminders",
            "Track task completion"
        ]
        users = ["HR coordinators", "Hiring managers"]
        data_sources = ["Employee onboarding records", "Task records"]
        success_metrics = [
            "Onboarding administration time",
            "Missed onboarding tasks"
        ]
 
    elif "retail" in text or "store" in text or "sales report" in text:
        objective = "Automate retail sales reporting and identify underperforming stores"
        pain_points = [
            "Manual sales reporting takes several hours",
            "Declining store sales are difficult to identify"
        ]
        functions = [
            "Automate sales reporting",
            "Compare performance across stores",
            "Identify stores with declining sales"
        ]
        users = ["Store managers", "Retail operations managers"]
        data_sources = ["Historical store sales data"]
        success_metrics = [
            "Sales reporting preparation time",
            "Identification of underperforming stores"
        ]
 
 
    elif any(phrase in text for phrase in [
        "autonomous agent",
        "agentic workflow",
        "independently plan",
        "plan and execute",
        "coordinate tools autonomously",
        "adapt actions based on results"
    ]):
        objective = "Build an autonomous AI agent for multi-step task execution"
        pain_points = ["Complex tasks require coordinated multi-step actions"]
        functions = [
            "Plan multi-step tasks",
            "Coordinate tools autonomously",
            "Adapt actions based on results"
        ]
        users = ["Business operations teams"]
        data_sources = ["Task and execution records"]
        success_metrics = ["Task completion rate", "Task execution accuracy"]
 
    
        # Extract explicit constraints from the client brief.
    constraints = []

    if any(phrase in text for phrase in [
        "must not expose",
        "must not reveal",
        "unauthorized access",
        "access permissions",
        "access control",
        "restricted information",
    ]):
        constraints.append(
            "Enforce access controls and prevent unauthorized information access"
        )

    if any(phrase in text for phrase in [
        "must comply",
        "compliance requirement",
        "regulatory requirement",
    ]):
        constraints.append(
            "Meet applicable compliance and regulatory requirements"
        )

    if any(phrase in text for phrase in [
        "must use",
        "must support",
        "must integrate",
    ]):
        constraints.append(
            "Meet the client's explicitly stated implementation requirements"
        )

    return Requirements(
        business_objective=objective,
        users=users,
        pain_points=pain_points,
        functional_requirements=functions,
        non_functional_requirements=(
            ["Security and reliability requirements need confirmation"]
            if objective else []
        ),
        data_sources=data_sources,
        integrations=[],
        constraints=constraints,
        success_metrics=success_metrics
    )

def validate_requirements(requirements):
    """Check essential requirement completeness and unresolved decisions."""

    objective = (
        getattr(requirements, "business_objective", "") or ""
    ).strip().lower()

    vague_phrases = [
        "improve our business",
        "use ai to improve",
        "use ai",
        "make things better",
        "improve efficiency"
    ]

    vague = (
        not objective
        or any(phrase in objective for phrase in vague_phrases)
    )

    checks = {
        "business_objective": bool(objective) and not vague,
        "users": bool(requirements.users),
        "pain_points": bool(requirements.pain_points),
        "functional_requirements": bool(
            requirements.functional_requirements
        ),
        "data_sources": bool(requirements.data_sources),
        "success_metrics": bool(requirements.success_metrics)
    }

    missing = [
        field for field, passed in checks.items()
        if not passed
    ]

    checks["missing_essential"] = missing

    # Integrations are tracked separately from essential requirements.
    checks["integrations_identified"] = bool(
        getattr(requirements, "integrations", None)
    )

    # Preserve the existing validation behaviour.
    checks["overall_valid"] = len(missing) == 0

    return checks

 

def generate_missing_information_report(requirements, validation):
    """Identify missing requirements and generate targeted discovery questions."""

    questions = {
        "business_objective":
            "What specific business outcome should the solution achieve, and what baseline will we use to measure improvement?",
        "users":
            "Who will use the solution, what are their roles, and are there different access levels?",
        "pain_points":
            "Which current processes or problems need to be addressed, and how are they handled today?",
        "functional_requirements":
            "What must the solution do in the first release, and which features can wait until a later phase?",
        "data_sources":
            "What data is available, where is it stored, who owns it, and what is its format and quality?",
        "success_metrics":
            "How will success be measured? Please specify the current baseline, target, measurement method, and evaluation period."
    }

    missing = validation["missing_essential"]
    clarification_questions = [
        questions[field]
        for field in missing
        if field in questions
    ]

    objective = (
        getattr(requirements, "business_objective", "") or ""
    ).lower()

    # Identify the use case from the business objective.
    is_document_assistant = any(
        keyword in objective
        for keyword in [
            "policy", "document", "handbook",
            "employee questions", "internal procedures"
        ]
    )

    is_forecasting = any(
        keyword in objective
        for keyword in [
            "forecast", "forecasting", "demand prediction",
            "sales prediction", "predict future", "predictive"
        ]
    )

    is_analytics = any(
        keyword in objective
        for keyword in [
            "dashboard", "analytics", "reporting",
            "business intelligence", "kpi"
        ]
    )

    is_agentic = any(
        keyword in objective
        for keyword in [
            "agentic", "autonomous agent", "multi-step workflow",
            "automate decisions", "execute actions"
        ]
    )

    # Tailor discovery questions to the identified use case.
    if is_document_assistant:
        clarification_questions.extend([
            "Where are the approved documents stored, and which file formats must be supported?",
            "Who is authorized to view each document, and how should permissions be enforced?",
            "How frequently are documents updated, and who approves new versions?",
            "Should answers cite document names, section headings, page numbers, or all three?",
            "What should the assistant do when documents conflict or evidence is insufficient?",
            "Which identity provider or authentication system should the solution use?",
            "Can the client provide representative questions and verified answers for evaluation?"
        ])

    elif is_forecasting:
        clarification_questions.extend([
            "How far ahead should forecasts be generated, and how frequently should they be refreshed?",
            "Should forecasts be produced by product, store, category, region, or another level?",
            "Are historical inventory, stockout, pricing, and promotion data available alongside sales data?",
            "What forecasting accuracy is acceptable compared with the current planning method or a simple baseline?",
            "How should managers consume forecasts: dashboard, spreadsheet, report, or system integration?",
            "How should forecast performance be monitored as new data becomes available?"
        ])

    elif is_analytics:
        clarification_questions.extend([
            "Which business KPIs should the solution track, and how are they currently calculated?",
            "What reporting frequency and level of detail do users need?",
            "Which systems contain the data, and how frequently is it refreshed?",
            "Who will use the dashboards, and what decisions should they support?",
            "What existing reports or dashboards should be replaced or improved?"
        ])

    elif is_agentic:
        clarification_questions.extend([
            "Which specific workflow should the AI agent complete, from start to finish?",
            "Which tools and systems may the agent access or modify?",
            "Which actions require human approval before execution?",
            "What permissions, spending limits, or other boundaries must the agent follow?",
            "How should failures, uncertain decisions, and unexpected outcomes be handled?",
            "How will task completion, accuracy, and safety be evaluated?"
        ])

    # Use a neutral integration question when the use case is unknown.
    if not validation["integrations_identified"]:
        if is_document_assistant:
            integration_question = (
                "Which document storage, authentication, or HR systems "
                "must integrate with the solution?"
            )
        elif is_forecasting:
            integration_question = (
                "Which sales, inventory, ERP, or reporting systems "
                "must integrate with the solution?"
            )
        elif is_analytics:
            integration_question = (
                "Which databases, business applications, or reporting "
                "platforms must integrate with the solution?"
            )
        elif is_agentic:
            integration_question = (
                "Which business applications and tools may the agent "
                "connect to, and what permissions will it need?"
            )
        else:
            integration_question = (
                "Which existing systems, if any, must integrate with the solution?"
            )

        clarification_questions.append(integration_question)

    clarification_questions = list(
        dict.fromkeys(clarification_questions)
    )

    open_questions = list(missing)

    if not validation["integrations_identified"]:
        open_questions.append("integrations")

    if is_document_assistant:
        open_questions.extend([
            "document_storage",
            "document_permissions",
            "policy_update_process",
            "citation_requirements",
            "insufficient_evidence_handling",
            "authentication",
            "evaluation_dataset"
        ])

    elif is_forecasting:
        open_questions.extend([
            "forecast_horizon",
            "forecast_granularity",
            "inventory_and_promotion_data",
            "forecast_accuracy_target",
            "forecast_delivery_method",
            "forecast_monitoring"
        ])

    elif is_analytics:
        open_questions.extend([
            "kpi_definitions",
            "reporting_frequency",
            "data_refresh_frequency",
            "dashboard_users",
            "decision_requirements"
        ])

    elif is_agentic:
        open_questions.extend([
            "workflow_scope",
            "tool_permissions",
            "human_approval",
            "execution_boundaries",
            "failure_handling",
            "agent_evaluation"
        ])

    open_questions = list(dict.fromkeys(open_questions))

    return {
        "status": (
            "READY FOR SCOPING"
            if validation["overall_valid"]
            else "CLARIFICATION REQUIRED"
        ),
        "missing_fields": missing,
        "clarification_questions": clarification_questions,
        "open_questions": open_questions,
        "has_unresolved_questions": bool(clarification_questions)
    }


def enrich_discovery_questions(report):
    """Add business context and ownership to unresolved client decisions."""

    question_details = {
        "integrations": {
            "why_it_matters": "Determines which systems must exchange data with the solution.",
            "risk": "Unconfirmed integrations may increase delivery time and cost.",
            "owner": "Client IT / Project Sponsor",
        },
        "document_storage": {
            "why_it_matters": "Identifies where approved policies are stored and how they can be accessed.",
            "risk": "The solution may not be able to retrieve the required documents.",
            "owner": "HR / Document Management Owner",
        },
        "document_permissions": {
            "why_it_matters": "Defines which employees can access each policy or document.",
            "risk": "Incorrect permissions could expose restricted information.",
            "owner": "HR / Information Security",
        },
        "policy_update_process": {
            "why_it_matters": "Establishes how new and revised policies are approved and indexed.",
            "risk": "Employees may receive answers based on outdated policies.",
            "owner": "HR Policy Owner",
        },
        "citation_requirements": {
            "why_it_matters": "Defines how answers should reference source documents and sections.",
            "risk": "Employees may be unable to verify answers against official policies.",
            "owner": "HR / Compliance",
        },
        "insufficient_evidence_handling": {
            "why_it_matters": "Defines what the assistant should do when evidence is missing or conflicting.",
            "risk": "The assistant may provide unsupported or misleading answers.",
            "owner": "HR / Project Sponsor",
        },
        "authentication": {
            "why_it_matters": "Determines how employee identities are verified.",
            "risk": "Users may access the system without appropriate identity checks.",
            "owner": "Client IT / Identity Management",
        },
        "evaluation_dataset": {
            "why_it_matters": "Provides representative questions and verified answers for testing.",
            "risk": "Answer quality and citation accuracy may not be reliably measured.",
            "owner": "HR Subject-Matter Experts",
        },
    }

    enriched_questions = []

    for question_id in report.get("open_questions", []):
        details = question_details.get(question_id)

        if details:
            enriched_questions.append({
                "topic": question_id.replace("_", " ").title(),
                "why_it_matters": details["why_it_matters"],
                "risk": details["risk"],
                "owner": details["owner"],
            })

    return enriched_questions

 
def classify_ai_use_case(requirements):
    text = " ".join([
        requirements.business_objective,
        *requirements.pain_points,
        *requirements.functional_requirements,
        *requirements.data_sources,
        *requirements.integrations
    ]).lower()
 
    rules = [
        ("Predictive Machine Learning", [
            "predict", "forecast", "risk", "probability",
            "classification", "prediction", "historical sales",
            "stockout", "seasonality"
        ]),
        ("NLP / LLM", [
            "text", "document", "language", "summarize",
            "chatbot", "natural language", "llm", "answer questions"
        ]),
        ("RAG", [
            "knowledge base", "documents", "company knowledge",
            "retrieve information", "source references", "grounded in"
        ]),
        
        ("Agentic AI", [
            "autonomous agent",
            "agentic workflow",
            "independently plan",
            "plan and execute",
            "multi-step reasoning",
            "dynamically choose actions",
            "coordinate tools autonomously",
            "adapt actions based on results",
            "make decisions and take actions"
        ]),
 
        ("Recommendation System", [
            "recommend", "personalize", "recommendation",
            "product suggestions", "customer preferences"
        ]),
        ("Computer Vision", [
            "image", "video", "object detection", "camera"
        ]),
        ("Data Analytics / BI", [
            "dashboard", "report", "analytics", "insight",
            "kpi", "reporting", "revenue", "costs"
        ]),
        ("Workflow Automation", [
            "manual", "repetitive", "process automation",
            "routing", "ticket processing"
        ])
    ]
 
    categories = [
        category for category, keywords in rules
        if any(keyword in text for keyword in keywords)
    ]
 
    return categories or ["General AI / Software Solution"]
 
 
def recommend_solution_type(categories):
    
    priority = [
        ("RAG", "RAG-based AI Application"),
        ("Predictive Machine Learning", "Predictive ML Solution"),
        ("Recommendation System", "Recommendation System"),
        ("Computer Vision", "Computer Vision Solution"),
        ("NLP / LLM", "LLM / NLP Application"),
        ("Data Analytics / BI", "Analytics / BI Solution"),
        ("Workflow Automation", "Workflow Automation"),
        ("Agentic AI", "Agentic AI Workflow")
    ]
 
 
    for category, solution in priority:
        if category in categories:
            return solution
 
    return "Custom Software / AI Solution"
 
 
def generate_architecture_recommendation(requirements, solution_type):
    ai_layers = {
        "Agentic AI Workflow": [
            "LLM", "LangChain", "Tool Calling", "Agent Workflow"
        ],
        "RAG-based AI Application": [
            "LLM", "Embeddings", "Vector Search", "RAG Pipeline"
        ],
        "Predictive ML Solution": [
            "Scikit-learn", "Feature Engineering", "Model Evaluation"
        ],
        "Recommendation System": [
            "Recommendation Model", "User/Item Features", "Evaluation"
        ],
        "Analytics / BI Solution": [
            "Data Transformation", "KPI Computation", "Visualization"
        ]
    }
 
    return {
        "solution_type": solution_type,
        "frontend": ["Streamlit"],
        "backend": ["Python", "FastAPI", "Pydantic"],
        "ai_layer": ai_layers.get(
            solution_type, ["Application Logic", "Model Integration"]
        ),
        "data_layer": ["PostgreSQL", "Pandas"],
        "integrations": requirements.integrations,
        "deployment": ["Docker", "Cloud deployment", "Git"]
    }
 
 
 

def generate_mvp_scope(requirements, solution_type):
    """Create a use-case-specific MVP plan, risks, and dependencies."""

    objective = requirements.business_objective.lower()
    functions = requirements.functional_requirements

    # Start with the client's actual requirements.
    mvp_features = list(functions)

    phase_2_features = [
        "Additional integrations after requirements confirmation",
        "Monitoring and performance improvements"
    ]

    dependencies = list(requirements.data_sources)
    dependencies.append("Stakeholder feedback")

    assumptions = [
        "Data access and quality need confirmation",
        "Success criteria must be agreed with stakeholders"
    ]

    risks = [
        "Data availability and quality may affect delivery",
        "Integration requirements are not yet confirmed"
    ]

    # Retrieval-augmented generation and document assistants
    if solution_type == "RAG-based AI Application":
        mvp_features.extend([
            "Ingest approved PDF and policy documents",
            "Extract, chunk, and index document content for retrieval",
            "Retrieve relevant passages before generating an answer",
            "Evaluate answer accuracy and citation correctness"
        ])

        phase_2_features.extend([
            "Integrate with the confirmed document storage platform",
            "Integrate with the company's identity and access-management system",
            "Add feedback collection and retrieval-quality monitoring"
        ])

        risks.extend([
            "Poor-quality or outdated policy documents may produce unreliable answers",
            "Incorrect access controls could expose restricted information",
            "Retrieval failures may cause incomplete or unsupported answers"
        ])

    # Invoice processing
    elif "invoice" in objective:
        mvp_features.extend([
            "Extract invoice numbers, dates, vendors, taxes, and totals",
            "Validate extracted fields and flag exceptions",
            "Route exceptions to finance staff for review",
            "Track processing time and extraction accuracy"
        ])

        phase_2_features.extend([
            "Integrate with accounting or ERP systems",
            "Support additional invoice layouts and document formats"
        ])

        risks.extend([
            "Poor-quality scans may reduce extraction accuracy",
            "Incorrectly extracted financial fields require human review"
        ])

    # Employee onboarding
    elif "onboarding" in objective:
        mvp_features.extend([
            "Generate onboarding checklists for new employees",
            "Assign tasks to HR coordinators and hiring managers",
            "Send reminders and track overdue tasks",
            "Measure administration time and missed tasks"
        ])

        phase_2_features.extend([
            "Integrate with HR information systems",
            "Add onboarding progress and bottleneck reporting"
        ])

        risks.extend([
            "Outdated employee records may trigger incorrect tasks",
            "Unclear task ownership may delay onboarding"
        ])

    # Retail analytics
    elif (
        "retail" in objective
        or "store" in objective
        or "sales" in objective
    ):
        mvp_features.extend([
            "Calculate agreed sales KPIs from historical data",
            "Compare sales performance across stores",
            "Identify stores with declining sales",
            "Display sales trends in a dashboard",
            "Measure report preparation time and KPI accuracy"
        ])

        phase_2_features.extend([
            "Add scheduled reports and configurable alerts",
            "Integrate additional retail data sources"
        ])

        risks.extend([
            "Inconsistent KPI definitions may distort comparisons",
            "Incomplete sales history may hide seasonal patterns"
        ])

    # Demand forecasting
    elif (
        "forecast" in objective
        or "demand" in objective
        or "inventory" in objective
    ):
        mvp_features.extend([
            "Prepare historical sales and inventory data",
            "Create product-demand forecasts using historical patterns",
            "Evaluate forecast error against a baseline",
            "Present forecasts to support replenishment planning",
            "Measure forecast error and stockout trends"
        ])

        phase_2_features.extend([
            "Add seasonal features and more advanced forecasting models",
            "Generate replenishment recommendations",
            "Monitor forecast performance as new data arrives"
        ])

        risks.extend([
            "Sparse or unreliable sales history may weaken forecasts",
            "Stockouts can make observed sales differ from true demand",
            "Forecasts should inform, not automatically dictate, purchasing"
        ])

    # Autonomous AI agents
    elif solution_type == "Agentic AI Workflow":
        mvp_features.extend([
            "Plan and execute a bounded multi-step task",
            "Use only explicitly permitted tools",
            "Validate tool inputs and outputs",
            "Require human approval for high-impact actions",
            "Log actions and measure task completion"
        ])

        phase_2_features.extend([
            "Add approved tools and workflows incrementally",
            "Evaluate task success, failure recovery, and operating cost"
        ])

        risks.extend([
            "Incorrect plans or tool outputs may produce bad outcomes",
            "Permissions must prevent unauthorized actions",
            "Human approval and audit logs are required for sensitive actions"
        ])

    # General workflow automation
    elif solution_type == "Workflow Automation":
        mvp_features.extend([
            "Define workflow steps and decision rules",
            "Handle exceptions and route them for human review",
            "Track completion time and workflow failures"
        ])

        phase_2_features.append(
            "Automate additional validated process steps"
        )

        risks.append(
            "Unclear business rules may cause incorrect workflow decisions"
        )

    # General analytics
    elif solution_type == "Analytics / BI Solution":
        mvp_features.extend([
            "Define and calculate agreed business KPIs",
            "Display trends and comparisons in a dashboard",
            "Validate data quality and KPI calculations"
        ])

        phase_2_features.append(
            "Add scheduled reporting and configurable alerts"
        )

        risks.append(
            "Incorrect or inconsistent KPI definitions may mislead users"
        )

    # General predictive ML
    elif solution_type == "Predictive ML Solution":
        mvp_features.extend([
            "Prepare historical data and relevant features",
            "Establish a baseline and evaluate model performance",
            "Present predictions with appropriate limitations"
        ])

        phase_2_features.append(
            "Monitor model performance and data drift"
        )

        risks.append(
            "Model performance may decline when real-world data changes"
        )

    # Other solution types retain a useful general MVP.
    else:
        mvp_features.extend([
            "Provide a basic user interface",
            "Validate inputs and handle errors"
        ])

        risks.append(
            "Technical feasibility must be confirmed during discovery"
        )

    # Avoid duplicate items while preserving their original order.
    mvp_features = list(dict.fromkeys(mvp_features))
    phase_2_features = list(dict.fromkeys(phase_2_features))
    risks = list(dict.fromkeys(risks))

    return {
        "mvp_features": mvp_features,
        "phase_2_features": phase_2_features,
        "out_of_scope": [
            "Custom foundation model training",
            "Unconfirmed integrations"
        ],
        "dependencies": dependencies,
        "assumptions": assumptions,
        "risks": risks
    }

 
 
def generate_success_metrics(requirements, solution_type):
    """Return use-case-specific metrics for proposal evaluation."""
 
    objective = requirements.business_objective.lower()
 
    # Retrieval-augmented generation and document assistants
    if solution_type == "RAG-based AI Application":
        return [
            {
                "metric": "Answer accuracy",
                "measurement": "Percentage of evaluated answers judged correct against approved policy documents",
                "purpose": "Check the reliability of employee-facing answers"
            },
            {
                "metric": "Source citation accuracy",
                "measurement": "Percentage of citations that correctly support the associated answer",
                "purpose": "Ensure answers are traceable to relevant policy sections"
            },
            {
                "metric": "Evidence-based abstention",
                "measurement": "Percentage of unanswerable test questions correctly declined",
                "purpose": "Reduce unsupported or fabricated answers"
            },
            {
                "metric": "Employee information retrieval time",
                "measurement": "Average time to find an answer, compared with the existing process",
                "purpose": "Evaluate improvements in employee productivity"
            },
            {
                "metric": "Access-control compliance",
                "measurement": "Percentage of access-control test cases that correctly prevent unauthorized retrieval",
                "purpose": "Check that restricted documents remain protected"
            }
        ]
 
 
    # Invoice processing
    if "invoice" in objective:
        return [
            {
                "metric": "Invoice extraction accuracy",
                "measurement": "Percentage of extracted fields matching verified values",
                "purpose": "Assess the accuracy of invoice data extraction"
            },
            {
                "metric": "Invoice processing time",
                "measurement": "Average time required to process one invoice",
                "purpose": "Evaluate operational efficiency"
            },
            {
                "metric": "Manual correction rate",
                "measurement": "Percentage of invoices requiring manual correction",
                "purpose": "Identify extraction and validation gaps"
            }
        ]
 
    # Employee onboarding
    elif "onboarding" in objective:
        return [
            {
                "metric": "Onboarding completion rate",
                "measurement": "Percentage of required onboarding tasks completed",
                "purpose": "Track completion of onboarding activities"
            },
            {
                "metric": "Overdue task rate",
                "measurement": "Percentage of onboarding tasks completed after their due date",
                "purpose": "Identify delays in onboarding"
            },
            {
                "metric": "Administration time per hire",
                "measurement": "Average HR administration hours per new employee",
                "purpose": "Evaluate administrative workload"
            }
        ]
 
    # Retail analytics
    elif any(word in objective for word in ["retail", "store", "sales"]):
        return [
            {
                "metric": "Reporting preparation time",
                "measurement": "Time required to produce a sales report",
                "purpose": "Evaluate reporting efficiency"
            },
            {
                "metric": "KPI calculation accuracy",
                "measurement": "Agreement between dashboard calculations and verified results",
                "purpose": "Validate reporting reliability"
            },
            {
                "metric": "Underperforming store identification",
                "measurement": "Agreement between flagged stores and agreed business criteria",
                "purpose": "Assess the usefulness of performance monitoring"
            }
        ]
 
    # Demand forecasting
    elif any(word in objective for word in ["forecast", "demand", "inventory"]):
        return [
            {
                "metric": "Forecast error",
                "measurement": "MAE or WAPE on held-out historical periods",
                "purpose": "Evaluate demand prediction accuracy"
            },
            {
                "metric": "Stockout rate",
                "measurement": "Percentage of tracked products or periods experiencing stockouts",
                "purpose": "Monitor product availability"
            },
            {
                "metric": "Excess inventory",
                "measurement": "Inventory above an agreed target or policy threshold",
                "purpose": "Monitor potential overstocking"
            }
        ]
 
    # Agentic AI
    elif solution_type == "Agentic AI Workflow":
        return [
            {
                "metric": "Task completion rate",
                "measurement": "Percentage of assigned tasks completed successfully",
                "purpose": "Evaluate end-to-end task execution"
            },
            {
                "metric": "Tool execution success rate",
                "measurement": "Percentage of tool calls completed successfully",
                "purpose": "Assess tool-use reliability"
            },
            {
                "metric": "Human intervention rate",
                "measurement": "Percentage of tasks requiring human intervention",
                "purpose": "Understand oversight requirements"
            }
        ]
 
    # General fallback: preserve the metrics extracted from the brief.
    return [
        {
            "metric": metric,
            "measurement": "Define the calculation and baseline with stakeholders",
            "purpose": "Evaluate progress toward the stated business objective"
        }
        for metric in requirements.success_metrics
    ]
 
 
def calculate_ai_readiness(requirements):
    checks = {
        "Business Objective": bool(requirements.business_objective.strip()),
        "Users Identified": bool(requirements.users),
        "Pain Points Identified": bool(requirements.pain_points),
        "Functional Requirements": bool(requirements.functional_requirements),
        "Data Sources": bool(requirements.data_sources),
        "Success Metrics": bool(requirements.success_metrics)
    }
 
    score = round(sum(checks.values()) / len(checks) * 100, 1)
    level = "High" if score >= 85 else (
        "Medium" if score >= 60 else "Low"
    )
 
    return {"score": score, "readiness": level, "checks": checks}
 
 

def calculate_complexity(solution_type, requirements, architecture):
    """Estimate implementation complexity using transparent scoring rules."""

    solution_points = {
        "Workflow Automation": 1,
        "Analytics / BI Solution": 1,
        "Recommendation System": 2,
        "Predictive ML Solution": 2,
        "LLM / NLP Application": 2,
        "RAG-based AI Application": 3,
        "Agentic AI Workflow": 4,
        "Computer Vision Solution": 3,
    }

    score = solution_points.get(solution_type, 2)
    reasons = [
        f"{solution_type} has a base complexity score of {score}."
    ]

    # 1. Confirmed integrations
    integrations = getattr(requirements, "integrations", []) or []
    integration_count = len(integrations)
    integration_points = min(integration_count, 4)
    score += integration_points

    reasons.append(
        f"{integration_count} confirmed integration(s) add "
        f"{integration_points} point(s), capped at 4."
    )


    # 3. Data readiness
    data_sources = getattr(requirements, "data_sources", []) or []

    # 3. Data readiness
    data_sources = getattr(requirements, "data_sources", []) or []
    constraints = getattr(requirements, "constraints", []) or []
    data_text = " ".join(str(item).lower() for item in data_sources)

    data_uncertain = any(
        phrase in data_text
        for phrase in [
            "unknown",
            "not confirmed",
            "not finalized",
            "unavailable",
            "to be determined",
        ]
    )

    if not data_sources:
        score += 2
        reasons.append(
            "Data sources are unspecified; discovery adds 2 points."
        )
    elif data_uncertain:
        score += 1
        reasons.append(
            "Data-source availability is uncertain; preparation adds 1 point."
        )
    else:
        reasons.append(
            f"{len(data_sources)} data source(s) identified; "
            "no data-discovery points applied."
        )

    # 4. Functional scope
    functional_requirements = (
        getattr(requirements, "functional_requirements", []) or []
    )
    functional_count = len(functional_requirements)
    functional_points = min(functional_count // 3, 3)
    score += functional_points

    reasons.append(
        f"{functional_count} functional requirement(s) add "
        f"{functional_points} point(s), capped at 3."
    )

    # 5. Constraints, with extra weight for security-sensitive work
    constraint_points = min(len(constraints), 2)
    score += constraint_points

    reasons.append(
        f"{len(constraints)} constraint(s) add "
        f"{constraint_points} point(s), capped at 2."
    )

    security_terms = [
        "access control",
        "access permission",
        "unauthorized",
        "authentication",
        "security",
        "confidential",
    ]

    security_sensitive = any(
        term in str(constraint).lower()
        for constraint in constraints
        for term in security_terms
    )

    if security_sensitive:
        score += 1
        reasons.append(
            "Security-sensitive requirements add 1 point "
            "for authorization and security testing."
        )

    # 6. Specialized evaluation
    if solution_type in {
        "Predictive ML Solution",
        "Recommendation System",
        "Computer Vision Solution",
    }:
        score += 1
        reasons.append(
            "Model evaluation and validation add 1 point."
        )

    if solution_type in {
        "RAG-based AI Application",
        "Agentic AI Workflow",
    }:
        score += 1
        reasons.append(
            "Retrieval or agent-workflow testing adds 1 point."
        )

    # 7. Deployment complexity
    deployment = architecture.get("deployment", [])
    if isinstance(deployment, str):
        deployment = [deployment] if deployment.strip() else []

    deployment_count = len(deployment)
    deployment_points = 1 if deployment_count > 1 else 0
    score += deployment_points

    reasons.append(
        f"{deployment_count} deployment component(s) add "
        f"{deployment_points} operational-complexity point(s)."
    )

    # 8. Complexity band
    level = (
        "Low" if score <= 4
        else "Medium" if score <= 8
        else "High"
    )

    reasons.append(
        f"Final score: {score}. Complexity level: {level} "
        "(Low: 0–4, Medium: 5–8, High: 9+)."
    )

    return {
        "score": score,
        "level": level,
        "reasons": reasons,
    }


def calculate_requirements_uncertainty(requirements, report):
    """Assess uncertainty caused by unresolved client decisions."""

    open_questions = report.get("open_questions", [])

    uncertainty_rules = {
        "integrations": "Integration requirements are unresolved.",
        "document_storage": "Document storage requirements are unresolved.",
        "document_permissions": "Document permissions are unresolved.",
        "policy_update_process": "Policy update processes are unresolved.",
        "citation_requirements": "Citation requirements are unresolved.",
        "insufficient_evidence_handling": (
            "Insufficient-evidence handling is unresolved."
        ),
        "authentication": "Authentication requirements are unresolved.",
        "evaluation_dataset": "The evaluation dataset is unresolved.",
    }

    unresolved = [
        question
        for question in uncertainty_rules
        if question in open_questions
    ]

    uncertainty_count = len(unresolved)

    if uncertainty_count <= 2:
        level = "Low"
    elif uncertainty_count <= 5:
        level = "Medium"
    else:
        level = "High"

    reasons = [
        uncertainty_rules[question]
        for question in unresolved
    ]

    reasons.append(
        f"{uncertainty_count} unresolved decision(s) identified."
    )

    return {
        "score": uncertainty_count,
        "level": level,
        "unresolved_items": unresolved,
        "reasons": reasons,
    }


    
def generate_proposal(blueprint, discovery_answers=None):
    """Generate a business-specific proposal from the solution blueprint."""
 
    requirements = blueprint["requirements"]
    solution_type = blueprint["solution_type"]
    objective = requirements.business_objective
    objective_text = objective.lower()
    functions = requirements.functional_requirements
    scope = blueprint["mvp_scope"]
    success_metrics = generate_success_metrics(requirements, solution_type)
 
    # Sensible defaults for other supported use cases.
    executive_summary = (
        f"Proposed {solution_type} to address the business objective: "
        f"{objective}."
    )
    problem = objective
    proposed_solution = (
        f"Implement a {solution_type} tailored to the objective: "
        f"{objective}. Confirm data access, scope, and success criteria "
        "before implementation."
    )
 
    # 0. Retrieval-augmented generation and document assistants
    if solution_type == "RAG-based AI Application":
        executive_summary = (
            "Reduce time spent searching HR policies by providing "
            "document-grounded answers with citations and permission-aware "
            "retrieval."
        )
        problem = (
            "Employees spend too much time searching across internal "
            "documents, while HR handles repeated questions. Answers must "
            "be traceable to approved sources and respect access permissions."
        )
        proposed_solution = (
            "Build a retrieval-augmented question-answering assistant "
            "that indexes approved policy PDFs, retrieves relevant passages, "
            "and generates answers with source-document and section citations. "
            "The assistant should abstain when sufficient evidence is not "
            "available and enforce employee permissions before retrieving "
            "restricted content. Confirm the document platform, identity "
            "integration, and access rules during discovery."
        )
 
    # 1. Invoice processing
    elif "invoice" in objective_text:
        executive_summary = (
            "Reduce manual invoice-processing effort through automated "
            "field extraction, validation, exception routing, and "
            "processing-performance tracking."
        )
        problem = (
            "Manual invoice handling consumes finance-team time, while "
            "missing or incorrect fields create additional review work."
        )
        proposed_solution = (
            "Build an invoice-processing workflow that extracts invoice "
            "numbers, dates, vendor names, tax amounts, and totals from "
            "PDF invoices. Validate required fields, flag missing or "
            "inconsistent values, and route exceptions to finance staff. "
            "Measure processing time, field-level extraction accuracy, "
            "and the proportion of invoices requiring manual correction."
        )
 
    # 2. Employee onboarding
    elif "onboarding" in objective_text:
        executive_summary = (
            "Streamline employee onboarding through coordinated checklists, "
            "task ownership, reminders, and completion tracking."
        )
        problem = (
            "Manual onboarding coordination can consume administrative "
            "time and result in missed or delayed tasks."
        )
        proposed_solution = (
           "Build an employee-onboarding workflow that creates checklists for new "
            "hires, assigns tasks to HR coordinators and hiring managers, "
            "sends reminders, and tracks completion. Measure onboarding "
            "administration time, overdue tasks, and missed activities."
        )
 
    # 3. Retail sales analytics
    elif (
        solution_type == "Analytics / BI Solution"
        and any(word in objective_text
                for word in ["retail", "store", "sales"])
    ):
        executive_summary = (
            "Help retail managers compare store performance using "
            "consistent sales KPIs, trend analysis, and underperformance "
            "indicators."
        )
        problem = (
            "Manual reporting and inconsistent KPI definitions can delay "
            "the identification of declining store performance."
        )
        proposed_solution = (
            "Build a retail sales dashboard using historical store data. "
            "Calculate agreed KPIs, compare performance across stores, "
            "visualize sales trends, and flag locations with declining "
            "sales against agreed thresholds. Validate data quality and "
            "KPI definitions before rollout. Measure reporting time, "
            "KPI accuracy, and time to identify underperforming stores."
        )
 
    # 4. Demand forecasting
    elif (
        solution_type == "Predictive ML Solution"
        and any(word in objective_text
                for word in ["forecast", "demand", "inventory"])
    ):
        executive_summary = (
            "Improve inventory planning by forecasting product demand "
            "from historical sales and evaluating forecast quality "
            "before using predictions to inform replenishment decisions."
        )
        problem = (
            "Stockouts and excess inventory can occur when purchasing "
            "decisions do not adequately reflect changes in demand."
        )
        proposed_solution = (
            "Prepare historical sales and inventory data, investigate "
            "seasonal patterns, and build product-demand forecasts using "
            "an appropriate baseline and predictive model. Evaluate "
            "forecast errors on held-out historical periods before "
            "presenting results to the purchasing team. Use forecasts "
            "to support replenishment planning while keeping purchasing "
            "decisions under human control. Measure forecast error and "
            "track stockout and excess-inventory trends where suitable "
            "data is available."
        )
 
    # 5. Controlled agentic AI
    elif solution_type == "Agentic AI Workflow":
        executive_summary = (
            "Support business operations with a controlled agent workflow "
            "that plans multi-step tasks and uses approved tools."
        )
        problem = (
            "Multi-step operational tasks can require repeated coordination, "
            "while unrestricted automated actions introduce operational risk."
        )
        proposed_solution = (
            "Design an agent workflow that breaks tasks into steps, uses "
            "explicitly permitted tools, validates tool inputs and outputs, "
            "and records its actions. Require human approval before high-impact "
            "operations. Evaluate task completion rate, tool-execution success, "
            "error rate, and frequency of human intervention."
        )
 
    # 6. General workflow automation
    elif solution_type == "Workflow Automation":
        executive_summary = (
            "Reduce repetitive operational work through standardized "
            "process steps, input validation, and exception handling."
        )
        proposed_solution = (
            "Automate the agreed business process using defined rules, "
            "input validation, exception routing, and human review where "
            "needed. Initial workflow coverage: "
            + "; ".join(functions) + "."
        )
 
    # 7. General analytics
    elif solution_type == "Analytics / BI Solution":
        executive_summary = (
            "Improve business visibility through consistent KPI reporting, "
            "trend analysis, and performance comparisons."
        )
        proposed_solution = (
            "Prepare the agreed business data, calculate validated KPIs, "
            "and present trends and comparisons in a dashboard. Confirm "
            "KPI definitions and data availability before implementation."
        )
 
    # 8. General predictive machine learning
    elif solution_type == "Predictive ML Solution":
        executive_summary = (
            "Use historical data to develop and evaluate predictions "
            "that support a defined business decision."
        )
        proposed_solution = (
            "Prepare historical data, establish a baseline, engineer "
            "relevant features, and evaluate a predictive model on "
            "held-out data. Agree on evaluation metrics and acceptable "
            "performance before deployment."
        )

 
    # Discovery-driven proposal refinement.
    # Recorded answers are assumptions until validated by the client.
    discovery_answers = discovery_answers or {}

    if solution_type == "RAG-based AI Application" and discovery_answers:
        discovery_context = []

        discovery_fields = [
            ("integrations", "System integrations"),
            ("document_storage", "Document storage"),
            ("document_permissions", "Document permissions"),
            ("policy_update_process", "Policy update process"),
            ("citation_requirements", "Citation requirements"),
            ("insufficient_evidence_handling", "Insufficient evidence handling"),
            ("authentication", "Authentication"),
            ("evaluation_dataset", "Evaluation dataset"),
        ]

        for key, label in discovery_fields:
            answer = str(discovery_answers.get(key, "")).strip()
            if answer:
                discovery_context.append(f"- {label}: {answer}")

        if discovery_context:
            proposed_solution += (
                "\n\nDiscovery inputs to validate before implementation:\n"
                + "\n".join(discovery_context)
            )

            proposed_solution += (
                "\n\nClient validation note: The discovery inputs above "
                "are recorded assumptions until confirmed by the client. "
                "Validate access permissions, identity integration, "
                "document versioning, citation behavior, and evaluation "
                "criteria before finalizing the implementation design."
            )

    architecture = blueprint["architecture"]
 
    return {
        "executive_summary": executive_summary,
        "problem": problem,
        "proposed_solution": proposed_solution,
        "success_metrics": success_metrics,
        "technology_stack": (
            architecture["backend"]
            + architecture["ai_layer"]
            + architecture["data_layer"]
        ),
        "mvp": scope["mvp_features"],
        "phase_2": scope["phase_2_features"],
        "risks": scope["risks"],
        "complexity": blueprint["implementation_complexity"]["level"]
    }
 
 
def run_specforge_pipeline(client_brief):
    requirements = mock_llm_extract_requirements(client_brief)
    validation = validate_requirements(requirements)
    report = generate_missing_information_report(requirements, validation)
 
    result = {
        "client_brief": client_brief,
        "requirements": requirements,
        "validation": validation,
        "clarification_report": report
    }
 
    if not validation["overall_valid"]:
        result["status"] = "CLARIFICATION REQUIRED"
        return result
 
    categories = classify_ai_use_case(requirements)
    solution = recommend_solution_type(categories)
    architecture = generate_architecture_recommendation(
        requirements, solution
    )
    scope = generate_mvp_scope(requirements, solution)
    readiness = calculate_ai_readiness(requirements)
    complexity = calculate_complexity(solution, requirements, architecture)
    uncertainty = calculate_requirements_uncertainty(
        requirements,
        report
    )
 
    blueprint = {
        "solution_type": solution,
        "ai_categories": categories,
        "architecture": architecture,
        "mvp_scope": scope,
        "ai_readiness": readiness,
        "implementation_complexity": complexity,
        "requirements_uncertainty": uncertainty,
        "requirements": requirements
    }
 
    result.update({
        "status": "BLUEPRINT GENERATED",
        "blueprint": blueprint,
        "proposal": generate_proposal(blueprint)
    })
 
    return result

def update_discovery_answers(report, answers):
    """
    Update discovery status based on client answers.

    answers should be a dictionary mapping each open question
    to the client's answer.
    """

    open_questions = report.get("open_questions", [])

    answered_items = []
    unresolved_items = []

    for question in open_questions:
        answer = answers.get(question, "")

        if isinstance(answer, str) and answer.strip():
            answered_items.append(question)
        else:
            unresolved_items.append(question)

    total_questions = len(open_questions)
    answered_count = len(answered_items)

    uncertainty_score = (
        round((len(unresolved_items) / total_questions) * 10)
        if total_questions
        else 0
    )

    if uncertainty_score >= 7:
        uncertainty_level = "High"
    elif uncertainty_score >= 4:
        uncertainty_level = "Medium"
    else:
        uncertainty_level = "Low"

    return {
        "total_questions": total_questions,
        "answered_count": answered_count,
        "unanswered_count": len(unresolved_items),
        "answered_items": answered_items,
        "unresolved_items": unresolved_items,
        "uncertainty_score": uncertainty_score,
        "uncertainty_level": uncertainty_level,
        "status": (
            "DISCOVERY COMPLETE"
            if not unresolved_items
            else "DISCOVERY IN PROGRESS"
        )
    }


def generate_discovery_refinement(discovery_answers):
    """
    Summarize discovery answers and flag missing decisions.
    This is rule-based; it does not call a live LLM.
    """

    question_labels = {
        "integrations": "System integrations",
        "document_storage": "Document storage",
        "document_permissions": "Document permissions",
        "policy_update_process": "Policy update process",
        "citation_requirements": "Citation requirements",
        "insufficient_evidence_handling": "Insufficient evidence handling",
        "authentication": "Authentication",
        "evaluation_dataset": "Evaluation dataset",
    }

    answered = {}
    unanswered = []

    for key, label in question_labels.items():
        answer = str(discovery_answers.get(key, "")).strip()

        if answer:
            answered[label] = answer
        else:
            unanswered.append(label)

    return {
        "status": (
            "READY FOR REVIEW"
            if not unanswered
            else "DISCOVERY INCOMPLETE"
        ),
        "answered_count": len(answered),
        "total_questions": len(question_labels),
        "unanswered_questions": unanswered,
        "discovery_answers": answered,
        "review_note": (
            "Answers are recorded inputs, not automatically verified "
            "client requirements. Obtain client confirmation before "
            "finalizing the solution blueprint."
        ),
    }
def generate_requirements_architecture_review(blueprint, discovery_answers):
    """
    Compare recorded discovery answers against the current blueprint.
    This is a rule-based review, not an automated architecture validator.
    """

    requirements = [
        {
            "key": "integrations",
            "requirement": "Microsoft SharePoint integration",
            "current_coverage": "Document platform integration must be confirmed",
            "gap": "SharePoint is recorded in discovery, but implementation details are not explicit in the blueprint.",
            "recommended_action": "Specify SharePoint connectivity, document retrieval, permissions, and API requirements.",
            "status": "Gap",
        },
        {
            "key": "authentication",
            "requirement": "Microsoft Entra ID authentication and SSO",
            "current_coverage": "Identity integration requires confirmation",
            "gap": "SSO and identity-based authorization are not explicitly defined.",
            "recommended_action": "Define Entra ID SSO, user identity propagation, and authorization checks before retrieval.",
            "status": "Gap",
        },
        {
            "key": "document_storage",
            "requirement": "PDF and DOCX document ingestion",
            "current_coverage": "PDF and policy-document ingestion is mentioned",
            "gap": "DOCX support is not explicit in the current MVP scope.",
            "recommended_action": "Explicitly include PDF and DOCX parsing, validation, and ingestion tests.",
            "status": "Partial",
        },
        {
            "key": "policy_update_process",
            "requirement": "Approved policy versioning and re-indexing",
            "current_coverage": "Document indexing is included",
            "gap": "Automatic detection of approved updates and removal of outdated indexed content are not explicit.",
            "recommended_action": "Define update detection, approval checks, re-indexing, and stale-content handling.",
            "status": "Gap",
        },
        {
            "key": "citation_requirements",
            "requirement": "Document, section, and page citations",
            "current_coverage": "Source-document and section citations are included",
            "gap": "Page-number availability and citation verification are not explicitly specified.",
            "recommended_action": "Preserve document, section, and page metadata and test whether each citation supports its answer.",
            "status": "Partial",
        },
        {
            "key": "insufficient_evidence_handling",
            "requirement": "Abstention and conflicting-policy handling",
            "current_coverage": "Abstention for insufficient evidence is included",
            "gap": "Explicit conflict detection and escalation to HR are not fully specified.",
            "recommended_action": "Add conflict detection, conflicting-source citations, and HR escalation rules.",
            "status": "Partial",
        },
        {
            "key": "evaluation_dataset",
            "requirement": "Verified HR evaluation dataset",
            "current_coverage": "Answer accuracy and citation correctness are listed as evaluation goals",
            "gap": "A reviewed test dataset covering ambiguity, insufficient evidence, and conflicting policies is not explicit.",
            "recommended_action": "Create HR-reviewed test cases with expected answers, approved sources, and section/page references.",
            "status": "Partial",
        },
        {
            "key": "document_permissions",
            "requirement": "Permission-aware document retrieval",
            "current_coverage": "Permission-aware retrieval is stated as a requirement",
            "gap": "Enforcement of source-system permissions during retrieval needs a defined design and security tests.",
            "recommended_action": "Specify permission filtering before content reaches the model and test unauthorized-access scenarios.",
            "status": "Partial",
        },
    ]

    # Report missing discovery answers separately from architecture gaps.
    for item in requirements:
        answer = discovery_answers.get(item["key"], "")
        item["discovery_answer_recorded"] = bool(
            isinstance(answer, str) and answer.strip()
        )

        if not item["discovery_answer_recorded"]:
            item["gap"] += " Discovery answer is also missing."
            item["status"] = "Gap"

    status_counts = {
        "Covered": sum(item["status"] == "Covered" for item in requirements),
        "Partial": sum(item["status"] == "Partial" for item in requirements),
        "Gap": sum(item["status"] == "Gap" for item in requirements),
    }

    return {
        "review_title": "Requirements-to-Architecture Review",
        "review_type": "Rule-based preliminary review",
        "total_requirements": len(requirements),
        "status_counts": status_counts,
        "items": requirements,
        "limitations": (
            "Statuses are preliminary rule-based assessments. "
            "They must be reviewed against the actual architecture and "
            "confirmed client requirements before implementation."
        ),
    }


def generate_architecture_action_plan(review):
    """
    Convert architecture review findings into a prioritized action plan.
    Priorities are rule-based recommendations, not validated risk scores.
    """

    priority_rules = {
        "Microsoft SharePoint integration": {
            "priority": "High",
            "reason": "The solution needs a defined way to access approved policy documents.",
            "action": "Define SharePoint connectivity, API requirements, document retrieval, and permission handling.",
            "sequence": 2,
        },
        "Microsoft Entra ID authentication and SSO": {
            "priority": "Critical",
            "reason": "Incorrect authorization could expose confidential HR information.",
            "action": "Specify Entra ID SSO, identity propagation, and authorization checks before document retrieval.",
            "sequence": 1,
        },
        "PDF and DOCX document ingestion": {
            "priority": "Medium",
            "reason": "Unsupported formats could prevent relevant policy content from being indexed.",
            "action": "Specify PDF and DOCX parsing, validation, and ingestion tests.",
            "sequence": 5,
        },
        "Approved policy versioning and re-indexing": {
            "priority": "High",
            "reason": "Outdated policies could produce incorrect employee guidance.",
            "action": "Define approved-update detection, re-indexing, and stale-content removal.",
            "sequence": 3,
        },
        "Document, section, and page citations": {
            "priority": "Medium",
            "reason": "Employees need to verify answers against approved policy sources.",
            "action": "Preserve document, section, and page metadata and test citation correctness.",
            "sequence": 6,
        },
        "Abstention and conflicting-policy handling": {
            "priority": "High",
            "reason": "Unsupported or contradictory answers could mislead employees.",
            "action": "Define abstention thresholds, conflict detection, source citations, and HR escalation.",
            "sequence": 4,
        },
        "Verified HR evaluation dataset": {
            "priority": "Medium",
            "reason": "The team needs reliable tests for answer quality and safe behavior.",
            "action": "Build an HR-reviewed dataset covering normal, ambiguous, unanswerable, and conflicting-policy questions.",
            "sequence": 7,
        },
        "Permission-aware document retrieval": {
            "priority": "Critical",
            "reason": "Document permissions must be enforced before restricted content reaches the model.",
            "action": "Define source-permission filtering and test unauthorized-access scenarios.",
            "sequence": 1,
        },
    }

    action_items = []

    for item in review.get("items", []):
        requirement = item.get("requirement", "")
        rule = priority_rules.get(requirement)

        if rule is None:
            continue

        action_items.append({
            "requirement": requirement,
            "review_status": item.get("status", "Unknown"),
            "priority": rule["priority"],
            "sequence": rule["sequence"],
            "reason": rule["reason"],
            "recommended_action": rule["action"],
            "discovery_answer_recorded": item.get(
                "discovery_answer_recorded", False
            ),
        })

    priority_order = {
        "Critical": 1,
        "High": 2,
        "Medium": 3,
        "Low": 4,
    }

    action_items.sort(
        key=lambda item: (
            priority_order.get(item["priority"], 99),
            item["sequence"],
        )
    )

    for index, item in enumerate(action_items, start=1):
        item["action_number"] = index

    return {
        "plan_title": "Prioritized Architecture Action Plan",
        "total_actions": len(action_items),
        "priority_counts": {
            priority: sum(
                item["priority"] == priority for item in action_items
            )
            for priority in ["Critical", "High", "Medium", "Low"]
        },
        "actions": action_items,
        "limitations": (
            "Priorities are preliminary rule-based recommendations. "
            "Confirm them with stakeholders using business impact, "
            "security requirements, dependencies, and implementation effort."
        ),
    }

def assess_architecture_coverage(blueprint, discovery_answers):
    """
    Assess architecture coverage using blueprint evidence
    and recorded client discovery answers.

    This is a transparent rule-based assessment.
    """

    architecture = blueprint.get("architecture", {})
    mvp = blueprint.get("mvp_scope", {})
    requirements = blueprint.get("requirements")

    # Collect explicit blueprint evidence.
    evidence = []

    for section in [
        architecture.get("frontend", []),
        architecture.get("backend", []),
        architecture.get("ai_layer", []),
        architecture.get("data_layer", []),
        architecture.get("integrations", []),
        architecture.get("deployment", []),
        mvp.get("mvp_features", []),
    ]:
        evidence.extend(str(item).lower() for item in section)

    blueprint_text = " ".join(evidence)

    # Discovery answers are recorded assumptions until validated.
    def get_answer(key):
        value = discovery_answers.get(key, "")
        return value.strip() if isinstance(value, str) else ""

    def assess(key, requirement, keywords, recommendation):
        answer = get_answer(key)

        if not answer:
            return {
                "key": key,
                "requirement": requirement,
                "status": "Unknown",
                "discovery_answer": "",
                "blueprint_evidence": [],
                "gap": "Client discovery information is missing.",
                "recommended_action": (
                    "Obtain client confirmation before finalizing "
                    "the architecture."
                ),
            }

        matched = [
            word for word in keywords
            if word.lower() in blueprint_text
        ]

        if len(matched) >= len(keywords):
            status = "Covered"
            gap = "Required capabilities are explicitly represented."
        elif matched:
            status = "Partial"
            gap = "Some capabilities are represented, but details are missing."
        else:
            status = "Gap"
            gap = "The confirmed requirement is not explicitly addressed."

        return {
            "key": key,
            "requirement": requirement,
            "status": status,
            "discovery_answer": answer,
            "blueprint_evidence": matched,
            "gap": gap,
            "recommended_action": recommendation,
        }

    assessments = [
        assess(
            "integrations",
            "Document platform integration",
            ["integrations"],
            "Specify the document platform API, connectivity and retrieval design.",
        ),
        assess(
            "authentication",
            "Identity integration and SSO",
            ["authentication"],
            "Define identity provider, SSO and user identity propagation.",
        ),
        assess(
            "document_storage",
            "PDF and DOCX ingestion",
            ["ingest", "pdf"],
            "Specify PDF and DOCX parsing, validation and ingestion.",
        ),
        assess(
            "policy_update_process",
            "Policy versioning and re-indexing",
            ["index"],
            "Define approved-update detection, re-indexing and stale-content removal.",
        ),
        assess(
            "citation_requirements",
            "Document, section and page citations",
            ["cite", "source"],
            "Preserve document, section and page metadata and validate citations.",
        ),
        assess(
            "insufficient_evidence_handling",
            "Abstention and conflicting-policy handling",
            ["decline", "insufficient"],
            "Define abstention, conflict detection and HR escalation.",
        ),
        assess(
            "evaluation_dataset",
            "Verified HR evaluation dataset",
            ["evaluate"],
            "Create an HR-reviewed dataset with verified answers and sources.",
        ),
        assess(
            "document_permissions",
            "Permission-aware document retrieval",
            ["permissions"],
            "Define permission filtering before retrieved content reaches the model.",
        ),
    ]

    counts = {
        status: sum(
            item["status"] == status for item in assessments
        )
        for status in ["Covered", "Partial", "Gap", "Unknown"]
    }

    return {
        "review_title": "Discovery-Aware Architecture Assessment",
        "review_type": "Rule-based evidence assessment",
        "total_requirements": len(assessments),
        "status_counts": counts,
        "items": assessments,
        "limitations": (
            "This assessment uses keyword-based evidence matching. "
            "A keyword match does not prove that an implementation exists. "
            "Discovery answers are recorded assumptions pending client "
            "validation. Technical design and security review are required."
        ),
    }

def assess_architecture_coverage_v2(blueprint, discovery_answers):
    """
    Assess discovery completeness separately from architecture coverage.

    Rule-based preliminary assessment. Keyword evidence does not prove
    that a technical implementation exists.
    """

    architecture = blueprint.get("architecture", {})
    mvp = blueprint.get("mvp_scope", {})
    requirements = blueprint.get("requirements")

    def answer_for(key):
        value = discovery_answers.get(key, "")
        return value.strip() if isinstance(value, str) else ""

    def contains_all(text, terms):
        text = text.lower()
        return all(term.lower() in text for term in terms)

    def assess(key, name, required_answer, evidence_rules,
               recommendation, unknown_means):
        answer = answer_for(key)

        if not answer:
            discovery_status = "Unknown"
            architecture_status = "Unknown"
            evidence_found = []
            gap = "Client confirmation is still required."

        else:
            discovery_status = "Confirmed"

            evidence_found = []

            for label, check in evidence_rules:
                if check():
                    evidence_found.append(label)

            if len(evidence_found) == len(evidence_rules):
                architecture_status = "Covered"
                gap = "All defined evidence checks are satisfied."
            elif evidence_found:
                architecture_status = "Partial"
                gap = "Some architectural evidence exists, but details are missing."
            else:
                architecture_status = "Gap"
                gap = "The blueprint does not explicitly address this requirement."

        return {
            "key": key,
            "requirement": name,
            "discovery_status": discovery_status,
            "architecture_status": architecture_status,
            "discovery_answer": answer,
            "blueprint_evidence": evidence_found,
            "gap": gap,
            "recommended_action": (
                "Obtain client confirmation before finalizing the design."
                if discovery_status == "Unknown"
                else recommendation
            ),
        }

    # Architecture evidence is evaluated from explicit architecture
    # components and MVP features, not from discovery answers.

    ai_layer = architecture.get("ai_layer", [])
    backend = architecture.get("backend", [])
    integrations = architecture.get("integrations", [])
    data_layer = architecture.get("data_layer", [])
    mvp_features = mvp.get("mvp_features", [])

    architecture_text = " ".join(
        str(item).lower()
        for section in [
            ai_layer, backend, integrations, data_layer, mvp_features
        ]
        for item in section
    )

    checks = [
        assess(
            "integrations",
            "Document platform integration",
            True,
            [
                ("Named document platform integration",
                 lambda: bool(integrations)),
                ("SharePoint connectivity explicitly specified",
                 lambda: contains_all(architecture_text, ["sharepoint", "api"])),
            ],
            "Specify SharePoint API connectivity, document retrieval and permissions.",
            "Document platform is not confirmed."
        ),
        assess(
            "authentication",
            "Identity integration and SSO",
            True,
            [
                ("Identity provider specified",
                 lambda: "microsoft entra id" in architecture_text),
                ("Authentication mechanism specified",
                 lambda: any(x in architecture_text for x in ["sso", "oauth", "openid connect"])),
            ],
            "Define Entra ID SSO, identity propagation and authorization.",
            "Identity requirements are unknown."
        ),
        assess(
            "document_storage",
            "PDF and DOCX ingestion",
            True,
            [
                ("PDF ingestion in MVP",
                 lambda: contains_all(architecture_text, ["pdf", "ingest"])),
                ("DOCX ingestion explicitly specified",
                 lambda: "docx" in architecture_text),
            ],
            "Specify PDF and DOCX parsing, validation and ingestion.",
            "Document formats need confirmation."
        ),
        assess(
            "policy_update_process",
            "Policy versioning and re-indexing",
            True,
            [
                ("Indexing capability",
                 lambda: "index" in architecture_text),
                ("Approved update detection",
                 lambda: any(x in architecture_text for x in ["update detection", "version detection"])),
                ("Stale content handling",
                 lambda: any(x in architecture_text for x in ["stale content", "outdated content", "remove old versions"])),
            ],
            "Define update detection, re-indexing and stale-content removal.",
            "Policy update process is unknown."
        ),
        assess(
            "citation_requirements",
            "Document, section and page citations",
            True,
            [
                ("Source citation capability",
                 lambda: any(x in architecture_text for x in ["cite", "citation"])),
                ("Section metadata",
                 lambda: "section" in architecture_text),
                ("Page metadata",
                 lambda: "page number" in architecture_text or "page metadata" in architecture_text),
            ],
            "Preserve document, section and page metadata and validate citations.",
            "Citation requirements are unknown."
        ),
        assess(
            "insufficient_evidence_handling",
            "Abstention and conflicting-policy handling",
            True,
            [
                ("Insufficient evidence handling",
                 lambda: "insufficient" in architecture_text or "decline to answer" in architecture_text),
                ("Conflict detection",
                 lambda: "conflict detection" in architecture_text or "conflicting policies" in architecture_text),
                ("HR escalation",
                 lambda: "hr escalation" in architecture_text),
            ],
            "Specify abstention, conflict detection and HR escalation.",
            "Insufficient-evidence behavior is unknown."
        ),
        assess(
            "evaluation_dataset",
            "Verified HR evaluation dataset",
            True,
            [
                ("Evaluation capability",
                 lambda: "evaluate" in architecture_text),
                ("Verified expected answers",
                 lambda: "verified expected answers" in architecture_text),
                ("HR-reviewed dataset",
                 lambda: "hr-reviewed dataset" in architecture_text),
            ],
            "Create an HR-reviewed dataset with verified answers and sources.",
            "Evaluation requirements are unknown."
        ),
        assess(
            "document_permissions",
            "Permission-aware document retrieval",
            True,
            [
                ("Permission enforcement in MVP",
                 lambda: "permissions" in architecture_text),
                ("Authorization before retrieval",
                 lambda: "before retrieval" in architecture_text or "permission filtering" in architecture_text),
            ],
            "Define permission filtering before retrieved content reaches the model.",
            "Document permissions are unknown."
        ),
    ]

    discovery_counts = {
        status: sum(
            item["discovery_status"] == status for item in checks
        )
        for status in ["Confirmed", "Unknown"]
    }

    architecture_counts = {
        status: sum(
            item["architecture_status"] == status for item in checks
        )
        for status in ["Covered", "Partial", "Gap", "Unknown"]
    }

    return {
        "review_title": "Discovery-Aware Architecture Assessment",
        "review_type": "Rule-based evidence assessment V2",
        "total_requirements": len(checks),
        "discovery_counts": discovery_counts,
        "architecture_counts": architecture_counts,
        "items": checks,
        "limitations": (
            "This is a preliminary keyword-based assessment. "
            "Discovery answers indicate recorded client requirements, "
            "not independently verified facts. Keyword matches do not "
            "prove implementation. Technical design and security review "
            "are required before implementation."
        ),
    }

def generate_architecture_gap_analysis(assessment):
    """
    Convert V2 architecture assessments into actionable,
    traceable implementation gaps.

    Priorities are preliminary rule-based recommendations.
    """

    gap_rules = {
        "integrations": {
            "missing": [
                "SharePoint API connectivity",
                "Document retrieval mechanism",
                "Integration authentication",
                "Permission propagation"
            ],
            "priority": "High"
        },
        "authentication": {
            "missing": [
                "Identity provider configuration",
                "SSO protocol",
                "User identity propagation",
                "Authentication testing"
            ],
            "priority": "Critical"
        },
        "document_storage": {
            "missing": [
                "DOCX parsing",
                "File validation",
                "Document extraction error handling"
            ],
            "priority": "Medium"
        },
        "policy_update_process": {
            "missing": [
                "Approved update detection",
                "Version tracking",
                "Automatic re-indexing",
                "Stale document removal"
            ],
            "priority": "High"
        },
        "citation_requirements": {
            "missing": [
                "Page-level metadata",
                "Citation verification",
                "Source traceability testing"
            ],
            "priority": "Medium"
        },
        "insufficient_evidence_handling": {
            "missing": [
                "Conflict detection",
                "Conflicting-source identification",
                "HR escalation workflow"
            ],
            "priority": "High"
        },
        "evaluation_dataset": {
            "missing": [
                "HR-reviewed evaluation dataset",
                "Verified expected answers",
                "Ambiguous and unanswerable test cases"
            ],
            "priority": "Medium"
        },
        "document_permissions": {
            "missing": [
                "Permission filtering before retrieval",
                "User-level authorization",
                "Unauthorized-access testing"
            ],
            "priority": "Critical"
        }
    }

    priority_order = {
        "Critical": 1,
        "High": 2,
        "Medium": 3,
        "Low": 4
    }

    actions = []

    for item in assessment.get("items", []):

        key = item["key"]
        status = item["architecture_status"]

        if status == "Covered":
            continue

        rule = gap_rules.get(key)

        if rule is None:
            continue

        # Unknown requirements need clarification first.
        if item["discovery_status"] == "Unknown":
            missing = [
                "Obtain and document client confirmation",
                "Validate the requirement before architecture design"
            ]
            priority = "High"
        else:
            missing = rule["missing"]
            priority = rule["priority"]

        actions.append({
            "requirement_key": key,
            "requirement": item["requirement"],
            "discovery_status": item["discovery_status"],
            "architecture_status": status,
            "existing_evidence": item["blueprint_evidence"],
            "identified_gaps": missing,
            "recommended_action": item["recommended_action"],
            "priority": priority
        })

    actions.sort(
        key=lambda item: priority_order[item["priority"]]
    )

    for number, action in enumerate(actions, start=1):
        action["action_number"] = number

    return {
        "title": "Architecture Gap Analysis and Action Plan",
        "total_actions": len(actions),
        "priority_counts": {
            priority: sum(
                item["priority"] == priority
                for item in actions
            )
            for priority in ["Critical", "High", "Medium", "Low"]
        },
        "actions": actions,
        "limitations": (
            "This is a preliminary rule-based action plan. "
            "Identified gaps and priorities must be validated by "
            "technical architects and client stakeholders."
        )
    }



