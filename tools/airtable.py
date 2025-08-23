import httpx
import os
from pydantic import BaseModel
from typing import Optional

AIRTABLE_API_URL = os.getenv("AIRTABLE_API_URL", "")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")

class Lead(BaseModel):
	Name: str
	LinkedIn: str
	Company: str
	Role: str
	Email: Optional[str] = None
	Phone: Optional[str] = None

def update_leads(new_leads: list[Lead]):
	"""
	Update the Airtable leads table with the new leads.
	If append is True, add new leads to existing ones (Airtable will handle duplicates based on your config).
	If append is False, delete all existing leads and add new_leads.
	Returns a JSON string of the updated leads (as returned by Airtable).
	"""
	try:
		headers = {
			"Authorization": f"Bearer {AIRTABLE_API_KEY}",
			"Content-Type": "application/json"
		}
		records = [{"fields": lead.model_dump()} for lead in new_leads]
		response = httpx.patch(
			AIRTABLE_API_URL, 
			headers=headers, 
			json={
				"records": records,
				"performUpsert": {
					"fieldsToMergeOn": ["Name"]
				},
				"typecast": True
			}
		)
		return response.json()
	except Exception as e:
		return f"Error from input:\n\n{str(new_leads)} Error:\n\n{e}"