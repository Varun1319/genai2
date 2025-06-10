
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


//////////////////////////////////////////////



from pydantic import BaseModel
from typing import List
import wikipedia
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableSequence
from langchain_cohere import ChatCohere

class InstitutionInfo(BaseModel):
    founder: str
    founded_year: str
    branches: List[str]
    num_employees: str
    summary: str

parser = PydanticOutputParser(pydantic_object=InstitutionInfo)

prompt = PromptTemplate(
    template="""
You are a helpful assistant extracting facts from Wikipedia articles.
Given this article text, extract the following about the institution:

- Founder
- Founded year
- List of current branches
- Approximate number of employees
- A short 4-line summary

Wikipedia Article:
{text}

Use this format:
{format_instructions}
""",
    input_variables=["text"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

llm = ChatCohere(
    cohere_api_key="",  # ⬅️ Replace this with your key
    model="command",
    temperature=0.3
)
chain: RunnableSequence = prompt | llm | parser

institution_name = input("Enter the name of the Institution: ")

try:
    wiki_text = wikipedia.page(institution_name).content
except wikipedia.exceptions.DisambiguationError as e:
    print("Multiple pages found. Suggestions:", e.options)
    exit()
except wikipedia.exceptions.PageError:
    print("Page not found on Wikipedia.")
    exit()

try:
    result: InstitutionInfo = chain.invoke({"text": wiki_text})

    print("\nInstitution Details:\n")
    print(f"Founder: {result.founder}")
    print(f"Founded Year: {result.founded_year}")
    print(f"Branches: {', '.join(result.branches)}")
    print(f"Employees: {result.num_employees}")
    print(f"\nSummary:\n{result.summary}")

except Exception as e:
    print("Error during processing:", e)
