import os
from dotenv import load_dotenv
load_dotenv()
# print("API Key:", os.getenv("TAVILY_API_KEY"))

from core.state import ResearchState
from core.graph import build_graph

#from agents.scout import scout_agent
#from agents.analyst import analyst_agent
#from agents.synthesizer import synthesizer_agent

# Build the pipeline
pipeline = build_graph()

# Run it
state = ResearchState(query="What is OpenAI")
result = pipeline.invoke(state)

'''
# Run Scout
result = scout_agent(state)

# Run Analyst
state = analyst_agent(state)

# Run Synthesizer
state = synthesizer_agent(state)
'''

'''
for r in result.search_results:
    print(f"\n📄 {r.title}")
    print(f"   {r.url}")
    print(f"   Confidence: {r.confidence}")
    print(f"   {r.snippet[:100]}...")


# Print findings of analyst
for finding in state.analyst_findings["findings"]:
    print(f"\n📄 {finding['source_title']}")
    print(f"   Confidence: {finding['confidence']}")
    print(f"   Key facts: {finding['key_facts'][:2]}")
'''

# Print final report
# report = state.final_report

report = result["final_report"]
print("\n" + "═"*45)
print("         RESEARCH REPORT")
print(f"         Query: {state["query"]}")
print("═"*45)

print(f"\n📋 EXECUTIVE SUMMARY")
print(f"   {report['executive_summary']}")

print(f"\n📌 KEY FACTS")
for fact in report['key_facts']:
    print(f"   • {fact}")

print(f"\n⚠️  RISKS")
for risk in report['risks']:
    print(f"   • {risk}")

print(f"\n🚀 OPPORTUNITIES")
for opp in report['opportunities']:
    print(f"   • {opp}")

print(f"\n🎯 OVERALL CONFIDENCE: {report['overall_confidence'].upper()}")
print(f"   Sources used: {report['sources_used']}")
print("═"*45)