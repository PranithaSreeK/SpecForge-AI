import streamlit as st
import specforge
import json
import html
from pathlib import Path
from specforge import run_specforge_pipeline

def render_architecture_coverage_chart(architecture_counts):
    """Render a simple visual summary of architecture coverage."""
    import pandas as pd

    coverage_df = pd.DataFrame({
        "Status": ["Covered", "Partial", "Gap", "Unknown"],
        "Count": [
            architecture_counts["Covered"],
            architecture_counts["Partial"],
            architecture_counts["Gap"],
            architecture_counts["Unknown"]
        ]
    })

    st.bar_chart(
        coverage_df,
        x="Status",
        y="Count",
        height=280
    )

DISCOVERY_FILE = Path("discovery_answers.json")

st.set_page_config(
    page_title="SpecForge AI",
    page_icon="🧠",
    layout="wide"
)

st.title("SpecForge AI")
st.subheader("From Client Brief to AI Solution Blueprint")

st.write(
    "Turn a business request into an initial AI solution recommendation, "
    "architecture, MVP scope, and clarification report."
)

client_brief = st.text_area(
    "Client brief",
    height=200,
    placeholder="Describe the client's business problem..."
)

if st.button("Analyze Brief", type="primary"):
    if not client_brief.strip():
        st.warning("Please enter a client brief.")
    else:
        result = run_specforge_pipeline(client_brief)
        st.write("Debug pipeline status:", result["status"])
        st.session_state["specforge_result"] = result
        st.session_state["specforge_brief"] = client_brief

if "specforge_result" in st.session_state:
    result = st.session_state["specforge_result"]

    st.divider()
    st.header("Analysis Results")
    st.write("**Status:**", result["status"])

    if result["status"] == "BLUEPRINT GENERATED":
        blueprint = result["blueprint"]
        proposal = result["proposal"]
       
        requirements = result["requirements"]
        
        complexity = blueprint["implementation_complexity"]
        uncertainty = blueprint["requirements_uncertainty"]

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Implementation Complexity",
                complexity["level"],
                help=(
                    "Estimates the effort involved in building the solution "
                    "based on its technical and operational requirements."
                )
            )
            st.caption(f"Complexity score: {complexity['score']}")

        with col2:
            st.metric(
                "Requirements Uncertainty",
                uncertainty["level"],
                help=(
                    "Measures unresolved client decisions that need "
                    "clarification before implementation."
                )
            )
            st.caption(
                f"Unresolved decisions: {uncertainty['score']}"
            )

        with st.expander("Why was this complexity level assigned?"):
            for reason in complexity.get("reasons", []):
                st.write(f"- {reason}")

        with st.expander("Why is requirements uncertainty at this level?"):
            for reason in uncertainty.get("reasons", []):
                st.write(f"- {reason}")

            st.caption(f"Debug module path: {specforge.__file__}")

        st.subheader("Recommended Solution")
        st.write(blueprint["solution_type"])

        st.subheader("Detected AI Capabilities")
        st.write(", ".join(blueprint["ai_categories"]))

        st.subheader("Proposed Architecture")

        for layer, components in blueprint["architecture"].items():
            st.markdown(f"**{layer.replace('_', ' ').title()}**")

            if isinstance(components, list):
                if components:
                    st.write(", ".join(components))
                else:
                    st.write("To be confirmed with the client.")
            elif components:
                st.write(components)
            else:
                st.write("To be confirmed with the client.")

        st.caption(
            "These are preliminary recommendations. "
            "Technologies and integrations require client confirmation."
        )


        st.subheader("MVP Scope")
        for feature in blueprint["mvp_scope"]["mvp_features"]:
            st.write(f"- {feature}")

        st.subheader("Client Proposal")
        st.markdown(f"**Executive summary:** {proposal['executive_summary']}")
        st.markdown(f"**Business problem:** {proposal['problem']}")
        st.markdown(f"**Proposed solution:** {proposal['proposed_solution']}")


        st.subheader("Success Metrics")

        for metric in proposal.get("success_metrics", []):
            st.markdown(f"**{metric['metric']}**")
            st.write(f"Measurement: {metric['measurement']}")
            st.write(f"Purpose: {metric['purpose']}")


        st.markdown("**Technology stack**")
        for item in proposal["technology_stack"]:
            st.write(f"- {item}")

        st.markdown("**Phase 2**")
        for item in proposal["phase_2"]:
            st.write(f"- {item}")

        st.markdown("**Risks**")
        for item in proposal["risks"]:
            st.write(f"- {item}")

        # Build a downloadable Markdown proposal.
        architecture = blueprint["architecture"]
        scope = blueprint["mvp_scope"]

        proposal_markdown = f"""# SpecForge AI — Solution Proposal

## 1. Executive Summary
{proposal['executive_summary']}

## 2. Client Brief
{st.session_state['specforge_brief']}

## 3. Business Problem
{proposal['problem']}


## 4. Success Metrics
{chr(10).join(
    '- **' + item['metric'] + '**' + chr(10)
    + '  - Measurement: ' + item['measurement'] + chr(10)
    + '  - Purpose: ' + item['purpose']
    for item in proposal.get('success_metrics', [])
)}


## 5. Recommended Solution
{blueprint['solution_type']}

## 6. Detected AI Capabilities
{chr(10).join('- ' + item for item in blueprint['ai_categories'])}

## 7. Proposed Architecture
{chr(10).join('### ' + key.replace('_', ' ').title() + chr(10) +
chr(10).join('- ' + str(item) for item in value)
for key, value in architecture.items())}

## 8. MVP Scope
{chr(10).join('- ' + item for item in scope['mvp_features'])}

## 9. Phase 2
{chr(10).join('- ' + item for item in scope['phase_2_features'])}

## 10. Technology Stack
{chr(10).join('- ' + item for item in proposal['technology_stack'])}

## 11. Risks
{chr(10).join('- ' + item for item in proposal['risks'])}

## 12. Readiness and Complexity
- Requirement completeness score: {blueprint['ai_readiness']['score']}%
- Readiness level: {blueprint['ai_readiness']['readiness']}
- Estimated implementation complexity: {blueprint['implementation_complexity']['level']}
- Requirements uncertainty: {blueprint['requirements_uncertainty']['level']}
- Unresolved client decisions: {blueprint['requirements_uncertainty']['score']}

## Important Note
This proposal is a preliminary, rule-based prototype output.
Architecture, effort, data availability, integrations, and success
criteria require confirmation with the client before implementation.
"""

        st.download_button(
            label="Download Solution Proposal (.md)",
            data=proposal_markdown,
            file_name="SpecForge_Solution_Proposal.md",
            mime="text/markdown"
        )
        # Display discovery questions at the end of the blueprint.
        report = result.get("clarification_report")

        if report:
            st.divider()
            st.header("Client Discovery Report")

            if report.get("missing_fields"):
                st.subheader("Missing Information")
                for field in report["missing_fields"]:
                    st.write(f"- {field.replace('_', ' ').title()}")

            if report.get("clarification_questions"):
                st.subheader("Clarification Questions")
                for question in report["clarification_questions"]:
                    st.write(f"- {question}")


            
            
            if report.get("open_questions"):
                st.subheader("Client Discovery Action Plan")

                questions = specforge.enrich_discovery_questions(report)

                # Store client answers during the current Streamlit session.
                
                if "discovery_answers" not in st.session_state:
                    if DISCOVERY_FILE.exists():
                        try:
                            st.session_state.discovery_answers = (
                                json.loads(
                                    DISCOVERY_FILE.read_text(
                                        encoding="utf-8"
                                    )
                                )
                            )
                        except (json.JSONDecodeError, OSError):
                            st.session_state.discovery_answers = {}
                            st.warning(
                                "Could not load saved discovery answers. "
                                "Starting with an empty response set."
                            )
                    else:
                        st.session_state.discovery_answers = {}


                for item in questions:
                    topic = item["topic"]
                    question_key = next(
                        (
                            key for key in report["open_questions"]
                            if key.replace("_", " ").lower() == topic.lower()
                        ),
                        topic.lower().replace(" ", "_")
                    )

                    st.markdown(f"### {topic}")
                    st.markdown(
                        f"**Why it matters:** {item['why_it_matters']}"
                    )
                    st.markdown(
                        f"**Risk if unresolved:** {item['risk']}"
                    )
                    st.markdown(
                        f"**Suggested stakeholder:** {item['owner']}"
                    )

                    answer = st.text_area(
                        "Client answer",
                        key=f"discovery_answer_{question_key}",
                        value=st.session_state.discovery_answers.get(
                            question_key, ""
                        ),
                        placeholder="Record the client's answer here...",
                    )

                    st.session_state.discovery_answers[question_key] = answer
                    st.divider()

                discovery = specforge.update_discovery_answers(
                    report,
                    st.session_state.discovery_answers
                )

                st.subheader("Discovery Progress")

                col1, col2, col3 = st.columns(3)
                col1.metric(
                    "Questions Answered",
                    f"{discovery['answered_count']}/{discovery['total_questions']}"
                )
                col2.metric(
                    "Unanswered",
                    discovery["unanswered_count"]
                )
                col3.metric(
                    "Uncertainty",
                    f"{discovery['uncertainty_score']}/10"
                )

                st.progress(
                    discovery["answered_count"]
                    / max(discovery["total_questions"], 1)
                )

                st.write(f"**Discovery Status:** {discovery['status']}")
                st.write(
                    f"**Discovery Uncertainty:** "
                    f"{discovery['uncertainty_score']}/10 "
                    f"({discovery['uncertainty_level']})"
                )

                if st.button("Save Discovery Answers"):
                    try:
                        DISCOVERY_FILE.write_text(
                            json.dumps(
                                st.session_state.discovery_answers,
                                indent=4,
                                ensure_ascii=False
                            ),
                            encoding="utf-8"
                        )
                        st.success("Discovery answers saved successfully.")
                    except OSError as error:
                        st.error(f"Could not save answers: {error}")


                st.subheader("Discovery-Driven Refinement")

                refinement = specforge.generate_discovery_refinement(
                    st.session_state.discovery_answers
                )
                refined_proposal = specforge.generate_proposal(
                    result["blueprint"],
                    discovery_answers=st.session_state.discovery_answers
                )
                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Discovery Answers Recorded",
                        f"{refinement['answered_count']}/{refinement['total_questions']}"
                    )

                with col2:
                    st.write("**Refinement Status**")
                    st.write(refinement["status"])

                st.info(refinement["review_note"])

                if refinement["unanswered_questions"]:
                    st.warning("Some discovery questions remain unanswered:")
                    for question in refinement["unanswered_questions"]:
                        st.write(f"- {question}")
                else:
                    st.success(
                        "All discovery fields are populated. "
                        "Review and confirm the answers before finalizing requirements."
                    )

                with st.expander("Review Discovery Answers"):
                    if refinement["discovery_answers"]:
                        for topic, answer in refinement["discovery_answers"].items():
                            st.markdown(f"**{topic}**")
                            st.write(answer)
                            st.divider()
                    else:
                        st.info("No discovery answers are available to display.")

                st.subheader("Discovery-Aware Proposal")

                st.markdown(
                    f"**Executive Summary:** "
                    f"{refined_proposal['executive_summary']}"
                )

                st.markdown(
                    f"**Business Problem:** "
                    f"{refined_proposal['problem']}"
                )

                st.markdown(
                    f"**Proposed Solution:** "
                    f"{refined_proposal['proposed_solution']}"
                )

                st.info(
                    "This proposal incorporates recorded discovery answers. "
                    "All answers remain pending client validation."
                )
                
                
                st.divider()
                st.header("Discovery-Aware Architecture Assessment")

                assessment = specforge.assess_architecture_coverage_v2(
                    blueprint=result["blueprint"],
                    discovery_answers=st.session_state.discovery_answers
                )

                st.caption(
                    "Separates confirmed client requirements from "
                    "preliminary architecture coverage."
                )

                # Discovery metrics
                st.subheader("Discovery Completeness")

                col1, col2 = st.columns(2)

                col1.metric(
                    "Confirmed Requirements",
                    assessment["discovery_counts"]["Confirmed"]
                )

                col2.metric(
                    "Unknown Requirements",
                    assessment["discovery_counts"]["Unknown"]
                )

                # Architecture metrics
                st.subheader("Architecture Coverage")

                col1, col2, col3, col4 = st.columns(4)

                col1.metric(
                    "Covered",
                    assessment["architecture_counts"]["Covered"]
                )

                col2.metric(
                    "Partial",
                    assessment["architecture_counts"]["Partial"]
                )

                col3.metric(
                    "Gaps",
                    assessment["architecture_counts"]["Gap"]
                )

                col4.metric(
                    "Unknown",
                    assessment["architecture_counts"]["Unknown"]
                )

                st.markdown("#### Coverage Overview")
                render_architecture_coverage_chart(
                    assessment["architecture_counts"]
                )

                # Requirements review table
                review_rows = [
                    {
                        "Requirement": item["requirement"],
                        "Discovery Status": item["discovery_status"],
                        "Architecture Status": item["architecture_status"],
                        "Blueprint Evidence": ", ".join(item["blueprint_evidence"]),
                        "Identified Gap": item["gap"],
                        "Recommended Action": item["recommended_action"]
                    }
                    for item in assessment["items"]
                ]

                st.dataframe(
                    review_rows,
                    use_container_width=True,
                    hide_index=True,
                    height=420
                )

                # Download assessment
                st.download_button(
                    label="Download Architecture Assessment (JSON)",
                    data=json.dumps(
                        assessment,
                        indent=4,
                        ensure_ascii=False
                    ),
                    file_name="specforge_architecture_assessment.json",
                    mime="application/json"
                )

                with st.expander("Assessment methodology and limitations"):
                    st.write(assessment["limitations"])

                # V3 dynamic gap analysis
                st.divider()
                st.subheader("Architecture Gap Analysis")

                gap_analysis = specforge.generate_architecture_gap_analysis(
                    assessment
                )

                st.write(
                    "Implementation actions generated from the identified "
                    "architecture gaps and unresolved client decisions."
                )

                col1, col2 = st.columns(2)

                col1.metric(
                    "Total Actions",
                    gap_analysis["total_actions"]
                )

                col2.metric(
                    "Critical Actions",
                    gap_analysis["priority_counts"]["Critical"]
                )

                # Display each architecture action as an expandable card.
                for item in gap_analysis["actions"]:
                    priority = item["priority"]
                    status = item["architecture_status"]

                    with st.expander(
                        f"Action {item['action_number']} — {item['requirement']}"
                    ):
                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown(f"**Priority:** {priority}")

                        with col2:
                            st.markdown(f"**Architecture Status:** {status}")

                        st.markdown("**Identified Gaps**")
                        for gap in item["identified_gaps"]:
                            st.write(f"- {gap}")

                        st.markdown("**Recommended Action**")
                        st.write(item["recommended_action"])

                st.download_button(
                    label="Download Architecture Gap Analysis (JSON)",
                    data=json.dumps(
                        gap_analysis,
                        indent=4,
                        ensure_ascii=False
                    ),
                    file_name="specforge_architecture_gap_analysis.json",
                    mime="application/json"
                )

                with st.expander("Gap analysis methodology and limitations"):
                    st.write(gap_analysis["limitations"])

                
                # --------------------------------------------------
                st.subheader("Download Refined Proposal")

                proposal_markdown = f"""# SpecForge AI — Discovery-Aware Proposal

## Executive Summary
{refined_proposal['executive_summary']}

## Business Problem
{refined_proposal['problem']}

## Proposed Solution
{refined_proposal['proposed_solution']}

## Success Metrics
{chr(10).join('- ' + str(metric) for metric in refined_proposal['success_metrics'])}

## MVP Scope
{chr(10).join('- ' + str(item) for item in refined_proposal['mvp'])}

## Phase 2
{chr(10).join('- ' + str(item) for item in refined_proposal['phase_2'])}

## Technology Stack
{chr(10).join('- ' + str(item) for item in refined_proposal['technology_stack'])}

## Implementation Complexity
{refined_proposal['complexity']}

## Client Validation Notice
This proposal incorporates recorded discovery answers. These inputs
are assumptions until confirmed by the client. Validate requirements,
document permissions, identity integration, versioning, and evaluation
criteria before finalizing the implementation design.
                """

                st.download_button(
                label="Download Refined Proposal (Markdown)",
                data=proposal_markdown,
                file_name="specforge_refined_proposal.md",
                mime="text/markdown"
                )
       
                st.subheader("Export Discovery Report")

                discovery_report = {
                    "client_brief": result.get("client_brief", ""),
                    "recommended_solution": result.get(
                        "blueprint", {}
                    ).get("solution_type", "Not specified"),
                    "implementation_complexity": result.get(
                        "blueprint", {}
                    ).get("implementation_complexity", {}),
                    "blueprint_requirements_uncertainty": result.get(
                        "blueprint", {}
                    ).get("requirements_uncertainty", {}),
                    "discovery_status": discovery["status"],
                    "discovery_progress": {
                        "total_questions": discovery["total_questions"],
                        "answered_count": discovery["answered_count"],
                        "unanswered_count": discovery["unanswered_count"],
                        "uncertainty_score": discovery["uncertainty_score"],
                        "uncertainty_level": discovery["uncertainty_level"]
                    },
                    "client_answers": st.session_state.discovery_answers,
                    "unresolved_decisions": discovery["unresolved_items"],
                    "discovery_questions": questions
                }

                st.download_button(
                label="Download Discovery Report (JSON)",
                data=json.dumps(
                discovery_report,
                indent=4,
                ensure_ascii=False
                ),
                file_name="specforge_discovery_report.json",
                mime="application/json"
                )
    else:
        report = result["clarification_report"]
        st.warning("More information is needed before scoping.")

        st.subheader("Missing Information")
        for field in report["missing_fields"]:
            st.write(f"- {field.replace('_', ' ').title()}")

        st.subheader("Questions for the Client")
        for question in report["clarification_questions"]:
            st.write(f"- {question}")

st.caption(
    "Prototype: rule-based extraction and recommendations; "
    "not yet powered by a live LLM."
)

