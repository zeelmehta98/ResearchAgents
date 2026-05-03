from anthropic import Anthropic
from core.state import ResearchState
from core.utils import extract_json
import json, os

claude = Anthropic()

def synthesizer_agent(state: ResearchState) -> ResearchState:
    print("📝 Synthesizer agent running...")
    state["current_agent"] = "synthesizer"

    findings = state["analyst_findings"].get("findings", [])

    response = claude.messages.create(
        model="claude-haiku-4-5-20251001",  # TODO: change to claude-sonnet-4-6 before final run
        max_tokens=1500,
        messages=[{
            "role": "user",
            "content": f"""You are a research report writer.
Based on these analyst findings for the query "{state["query"]}", 
write a structured research report.

Findings:
{json.dumps(findings, indent=2)}

Return ONLY a JSON object with this structure:
{{
  "executive_summary": "2-3 sentence overview",
  "key_facts": ["fact1", "fact2", "fact3"],
  "risks": ["risk1", "risk2"],
  "opportunities": ["opp1", "opp2"],
  "overall_confidence": "high/medium/low",
  "sources_used": 5
}}

No other text, just the JSON."""
        }]
    )

    raw_text = response.content[0].text
    try:
        report = json.loads(extract_json(raw_text))
        state["final_report"] = report
        print("✅ Report generated successfully")
    except json.JSONDecodeError:
        print("⚠️ Could not parse report")
        raise

    return state