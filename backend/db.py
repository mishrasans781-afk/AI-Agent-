import logging

logger = logging.getLogger(__name__)

# Mock DB interaction since no keys were provided
class SupabaseClient:
    def __init__(self):
        self.data = []

    def table(self, table_name):
        return self

    def insert(self, data):
        logger.info(f"[MOCK DB] Inserting into DB: {data}")
        self.data.append(data)
        return self

    def execute(self):
        return {"data": "mock_success", "error": None}

supabase = SupabaseClient()

def save_study_plan(student_data: dict, plan: str):
    return supabase.table("study_plans").insert({
        "student_data": student_data,
        "plan": plan
    }).execute()
