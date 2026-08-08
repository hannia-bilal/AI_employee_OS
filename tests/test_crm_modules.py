import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from CRM.src.modules.activity_timeline.timeline_manager import TimelineManager
from CRM.src.modules.lead_management.lead_manager import LeadManager
from CRM.src.modules.sales_pipeline.pipeline_manager import SalesPipelineManager
from CRM.src.modules.customer_summaries.summary_manager import CustomerSummaryManager


class CRMModuleTests(unittest.TestCase):
    def test_lead_and_pipeline_flow(self):
        lead_manager = LeadManager()
        pipeline_manager = SalesPipelineManager()
        lead = lead_manager.create_lead({
            "name": "Awais Khan",
            "email": "awais@example.com",
            "company": "CodeCelix",
            "phone": "+92-300-0000000",
            "source": "website",
        })

        self.assertEqual(lead.name, "Awais Khan")
        self.assertEqual(lead.pipeline_stage, "new")

        pipeline_manager.add_deal(lead.id, lead.name, 15000, "new")
        pipeline_manager.update_stage(lead.id, "qualified")
        summary = pipeline_manager.get_stage_summary()

        self.assertIn("qualified", summary)
        self.assertGreaterEqual(summary["qualified"], 1)

    def test_timeline_and_summary_generation(self):
        timeline_manager = TimelineManager()
        summary_manager = CustomerSummaryManager()
        activity = timeline_manager.add_activity({
            "lead_id": "LEAD-001",
            "title": "Discovery call",
            "description": "Discussed requirements and budget.",
            "activity_type": "call",
        })

        summary = summary_manager.generate_summary("LEAD-001", [activity])

        self.assertEqual(activity.lead_id, "LEAD-001")
        self.assertIn("Discovery call", summary)
        self.assertIn("requirements", summary)


if __name__ == "__main__":
    unittest.main()
