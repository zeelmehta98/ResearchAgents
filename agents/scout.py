from tavily import TavilyClient
from anthropic import Anthropic
from core.state import ResearchState, SearchResult
from core.utils import extract_json
import json, os

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
claude = Anthropic()

def scout_agent(state: ResearchState) -> ResearchState:
    print("🔍 Scout agent running...")
    state["current_agent"] = "scout"

    # Step 1: Tavily searches the web
    raw_results = tavily.search(
        query=state["query"],
        max_results=7,
        search_depth="advanced"
    )

    # Step 2: Haiku filters and ranks them
    response = claude.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": f"""You are a research scout. 
Given these search results for the query "{state["query"]}", 
pick the 5 most relevant and return them as JSON array.

Each item must have: url, title, snippet, confidence (high/medium/low)

Search results:
{json.dumps(raw_results['results'], indent=2)}

Respond ONLY with valid JSON array, no commentary."""
        }]
    )

    # Step 3: Parse and store
    raw_text = response.content[0].text.strip()
    if not raw_text:
        raise ValueError("Claude returned empty response")

    try:
        filtered = json.loads(extract_json(raw_text))
    except json.JSONDecodeError:
        print("⚠️ Claude did not return valid JSON. Raw output:")
        print(raw_text)
        raise
        #start = raw_text.find("[")
        #end = raw_text.rfind("]")
        #if start != -1 and end != -1:
        #    filtered = json.loads(raw_text[start:end+1])
        #else:
        #    raise

    state["search_results"] = [SearchResult(**r) for r in filtered]

    print(f"✅ Scout found {len(state["search_results"])} sources")
    return state