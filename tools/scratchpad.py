import os
import pandas as pd
from pydantic import BaseModel
from typing import Optional


class Lead(BaseModel):
    name: str
    linkedin_url: str
    company: str
    role: str
    email: Optional[str] = None
    phone: Optional[str] = None

def update_leads(new_leads: list[Lead], append: bool = False):
    """
    Update the leads.csv file with the new leads.
    If append is True, add new leads to existing ones (avoiding duplicates).
    If append is False, overwrite with new_leads.
    Returns a JSON string of the updated leads.
    """
    path = 'files/leads.csv'
    columns = [field for field in Lead.model_fields]
    # Try to read the file, handle empty file or missing file gracefully
    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            # If the file is empty, create an empty DataFrame with correct columns
            if df.empty and len(df.columns) == 0:
                df = pd.DataFrame(columns=columns)
        except pd.errors.EmptyDataError:
            df = pd.DataFrame(columns=columns)
    else:
        df = pd.DataFrame(columns=columns)
    if append:
        df = pd.concat([df, pd.DataFrame([lead.model_dump() for lead in new_leads])], ignore_index=True)
    else:
        df = pd.DataFrame([lead.model_dump() for lead in new_leads], columns=columns)
    df.to_csv(path, index=False)
    return df.to_json(orient="records")