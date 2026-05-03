'''
from pydantic import BaseModel
from typing import List, Optional

class SearchResult(BaseModel):
    url: str
    title: str
    snippet: str
    confidence: Optional[str] = None

class AnalystFinding(BaseModel):
    source_title: str
    source_url: str
    key_facts: List[str]
    risks: List[str]
    opportunities: List[str]
    confidence: str

class ResearchState(BaseModel):
    query: str
    search_results: List[SearchResult] = []
    analyst_findings: dict = {}
    final_report: dict = {}  # changed from str to dict
    current_agent: str = ""
'''

from typing import List, Optional
from typing_extensions import TypedDict

class SearchResult(TypedDict):
    url: str
    title: str
    snippet: str
    confidence: Optional[str]

class ResearchState(TypedDict):
    query: str
    search_results: List[SearchResult]
    analyst_findings: dict
    final_report: dict
    current_agent: str