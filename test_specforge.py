import unittest

from specforge import (
    mock_llm_extract_requirements,
    validate_requirements,
    run_specforge_pipeline,
    classify_ai_use_case,
    recommend_solution_type,
)


RETAIL_BRIEF = (
    "We're a retail company with 200 stores. Managers spend several "
    "hours every week preparing sales reports manually. We want an AI "
    "solution that automates reporting and identifies stores with "
    "declining sales."
)

FORECAST_BRIEF = (
    "We need demand forecasting to predict future product demand."
)

DOCUMENT_BRIEF = (
    "We want a document assistant that answers questions about company policies."
)

VAGUE_BRIEF = (
    "We want to use AI to improve our business."
)


INVOICE_BRIEF = (
    "We want to automate invoice processing. Extract invoice numbers, "
    "dates, vendor names, tax amounts, and totals from PDF invoices. "
    "Validate fields and flag exceptions for finance staff."
)

ONBOARDING_BRIEF = (
    "We want to automate employee onboarding. Trigger checklists for "
    "new hires, assign tasks to HR coordinators and hiring managers, "
    "send reminders, and track task completion."
)



class TestSpecForge(unittest.TestCase):

    def test_retail_requirements_are_extracted(self):
        requirements = mock_llm_extract_requirements(RETAIL_BRIEF)
        validation = validate_requirements(requirements)

        self.assertTrue(validation["overall_valid"])
        self.assertEqual(validation["missing_essential"], [])
        self.assertTrue(requirements.business_objective)
        self.assertTrue(requirements.functional_requirements)
        self.assertTrue(requirements.data_sources)
        self.assertTrue(requirements.success_metrics)

    def test_forecasting_brief_is_supported(self):
        requirements = mock_llm_extract_requirements(FORECAST_BRIEF)
        validation = validate_requirements(requirements)

        self.assertTrue(validation["overall_valid"])

    def test_document_brief_is_supported(self):
        requirements = mock_llm_extract_requirements(DOCUMENT_BRIEF)
        validation = validate_requirements(requirements)

        self.assertTrue(validation["overall_valid"])

    def test_vague_brief_triggers_clarification(self):
        result = run_specforge_pipeline(VAGUE_BRIEF)

        self.assertEqual(result["status"], "CLARIFICATION REQUIRED")
        self.assertIn("clarification_report", result)

    def test_retail_pipeline_generates_blueprint(self):
        result = run_specforge_pipeline(RETAIL_BRIEF)

        self.assertEqual(result["status"], "BLUEPRINT GENERATED")
        self.assertIn("blueprint", result)
        self.assertIn("proposal", result)

        blueprint = result["blueprint"]
        self.assertIn("solution_type", blueprint)
        self.assertIn("architecture", blueprint)
        self.assertIn("mvp_scope", blueprint)

    def test_invoice_requirements_are_extracted(self):
        requirements = mock_llm_extract_requirements(INVOICE_BRIEF)
        validation = validate_requirements(requirements)

        self.assertTrue(validation["overall_valid"])
        self.assertIn("invoice", requirements.business_objective.lower())
        self.assertTrue(requirements.functional_requirements)
        self.assertTrue(requirements.data_sources)

    def test_onboarding_requirements_are_extracted(self):
        requirements = mock_llm_extract_requirements(ONBOARDING_BRIEF)
        validation = validate_requirements(requirements)

        self.assertTrue(validation["overall_valid"])
        self.assertIn("onboarding", requirements.business_objective.lower())
        self.assertTrue(requirements.functional_requirements)
        self.assertTrue(requirements.data_sources)

    def test_invoice_proposal_is_business_specific(self):
        result = run_specforge_pipeline(INVOICE_BRIEF)

        self.assertEqual(result["status"], "BLUEPRINT GENERATED")
        proposal = result["proposal"]["proposed_solution"].lower()

        self.assertIn("invoice-processing workflow", proposal)
        self.assertIn("finance staff", proposal)
        self.assertIn("extraction accuracy", proposal)

    def test_onboarding_proposal_is_business_specific(self):
        result = run_specforge_pipeline(ONBOARDING_BRIEF)

        self.assertEqual(result["status"], "BLUEPRINT GENERATED")
        proposal = result["proposal"]["proposed_solution"].lower()

        self.assertIn("employee-onboarding workflow", proposal)
        self.assertIn("checklists", proposal)
        self.assertIn("reminders", proposal)
        self.assertIn("completion", proposal)

    def test_invoice_and_onboarding_recommend_workflow_automation(self):
        briefs = [
            "We want to automate invoice processing.",
            "We want to automate employee onboarding."
        ]

        for brief in briefs:
            with self.subTest(brief=brief):
                requirements = mock_llm_extract_requirements(brief)
                categories = classify_ai_use_case(requirements)
                solution = recommend_solution_type(categories)

                self.assertEqual(solution, "Workflow Automation")


    def test_autonomous_agent_recommends_agentic_ai(self):
        brief = (
            "We need an autonomous agent that independently plans "
            "multi-step tasks, coordinates tools autonomously, and "
            "adapts actions based on results."
        )

        requirements = mock_llm_extract_requirements(brief)
        categories = classify_ai_use_case(requirements)
        solution = recommend_solution_type(categories)

        self.assertIn("Agentic AI", categories)
        self.assertEqual(solution, "Agentic AI Workflow")

if __name__ == "__main__":
    unittest.main(verbosity=2)
