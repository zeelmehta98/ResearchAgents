from anthropic import Anthropic
from core.state import ResearchState
from core.utils import extract_json
import json, os

claude = Anthropic()

def analyst_agent(state: ResearchState) -> ResearchState:
    print("🧠 Analyst agent running...")
    state["current_agent"] = "analyst"

    findings = []

    for source in state["search_results"]:
        response = claude.messages.create(
            # model="claude-sonnet-4-6", -- ideally
            model="claude-haiku-4-5-20251001",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": f"""You are a research analyst.
Analyze this source about "{state["query"]}" and extract structured findings.

Source title: {source["title"]}
Source URL: {source["url"]}
Content: {source["snippet"]}

Return ONLY a JSON object with these fields:
{{
  "key_facts": ["fact1", "fact2"],
  "risks": ["risk1", "risk2"],
  "opportunities": ["opp1", "opp2"],
  "confidence": "high/medium/low"
}}

No other text, just the JSON."""
            }]
        )

        raw_text = response.content[0].text
        try:
            parsed = json.loads(extract_json(raw_text))
            parsed["source_title"] = source["title"]
            parsed["source_url"] = source["url"]
            findings.append(parsed)
        except json.JSONDecodeError:
            print(f"⚠️ Could not parse findings for: {source["title"]}")
            continue

    state["analyst_findings"] = {"findings": findings}
    print(f"✅ Analyst extracted findings from {len(findings)} sources")
    return state