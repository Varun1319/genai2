
from pydantic import BaseModel
from typing import List, Optional
import wikipedia
import re

class InstitutionDetails(BaseModel):
    name: str
    founder: Optional[str]
    founded_year: Optional[str]
    branches: Optional[List[str]]
    number_of_employees: Optional[str]
    summary: str


def extract_institution_details(institution_name: str) -> InstitutionDetails:
    try:

        page = wikipedia.page(institution_name)
        summary = wikipedia.summary(institution_name, sentences=4)
        content = page.content


        founder = None
        founded_year = None
        branches = []
        employees = None

        lines = content.split("\n")
        for line in lines:
            line_lower = line.lower()
            if "founder" in line_lower and not founder:
                match = re.search(r"(?i)founder(?:s)?\s*[:\-]?\s*(.*)", line)
                if match:
                    possible = match.group(1).strip()

                    if 0 < len(possible.split()) <= 10:
                        founder = possible
            if not founded_year:
                match = re.search(r"\b(?:established|formed)\b[^0-9]{0,20}(\d{4})", line_lower)
                if match:
                    founded_year = match.group(1)
            if re.search(r"(branches|departments)", line_lower) and ":" in line:
                possible_branches = line.split(":", 1)[-1].strip()
                if "," in possible_branches:
                    branches = [b.strip() for b in possible_branches.split(",") if b.strip()]
            if "employees" in line_lower or "staff" in line_lower:
                match = re.search(r"(?i)(?:employees|staff)[^\d]*(\d{1,3}(?:,\d{3})*|\d+)", line)
                if match:
                    employees = match.group(1)

        return InstitutionDetails(
            name=institution_name,
            founder=founder,
            founded_year=founded_year,
            branches=branches if branches else None,
            number_of_employees=employees,
            summary=summary
        )
    except Exception as e:
        return InstitutionDetails(
            name=institution_name,
            founder=None,
            founded_year=None,
            branches=None,
            number_of_employees=None,
            summary=f"Could not fetch summary due to: {str(e)}"
        )


if __name__ == "__main__":
    institution = input("Enter the name of the Institution: ")
    result = extract_institution_details(institution)
    print(result.model_dump_json(indent=4))
