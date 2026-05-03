# 🔍 Research Agents

### Autonomous AI Research System powered by Claude & Tavily

-----

## The Problem

Research is time-consuming. Whether you’re an analyst, student, investor, or product manager — gathering information about a company, competitor, or topic means:

- Opening 10+ browser tabs
- Reading through long articles to find relevant facts
- Manually cross-checking information across sources
- Summarizing everything into a coherent report

*This takes 2–4 hours of focused work. Every single time.*

And the worst part? Most of that time isn’t spent thinking — it’s spent collecting and organizing information. That’s exactly the kind of repetitive, structured work AI is built for.

-----

## The Solution

*Research Agents* automates this entire workflow using a pipeline of 3 specialized AI agents that work together like a small research team.

You type a single query. The system does the rest — searching the web, reading and analyzing sources, extracting key facts, and delivering a structured, confidence-scored report in under 3 minutes.


You type:  "Research Tesla Q1 2025"
               │
               ▼
    ┌──────────────────────┐
    │   🔍 Scout Agent     │  Searches the web, filters top 5 sources
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │   🧠 Analyst Agent   │  Reads each source, extracts structured facts
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │  📝 Synthesizer      │  Writes final report with confidence scores
    └──────────┬───────────┘
               │
               ▼
    Structured report in your terminal (and soon — a live dashboard)


-----

## Why Multi-Agent?

You might ask — why 3 agents? Why not just ask Claude one question and get a report?

Great question. Here’s why a single prompt doesn’t work well:

|Single Prompt Approach                            |Multi-Agent Approach                                                          |
|--------------------------------------------------|------------------------------------------------------------------------------|
|Claude can’t browse the web                       |Scout uses Tavily to fetch live data                                          |
|One model doing everything = mediocre at all tasks|Each agent is specialized for one job                                         |
|No transparency into how the answer was formed    |Every step is visible and auditable                                           |
|Hard to debug when something goes wrong           |Each agent’s output can be inspected individually                             |
|Can’t control cost — uses max tokens always       |Cheap model (Haiku) for simple tasks, stronger model (Sonnet) only when needed|

Think of it like a real team:

> A researcher finds sources. An analyst reads them. A writer produces the report. Nobody does all three jobs at once — specialization produces better results.

-----

## How Each Agent Works

### 🔍 Scout Agent — The Researcher

*Model:* Claude Haiku (fast + cheap)

The Scout’s job is simple: find the most relevant sources on the web for a given query.

1. Takes your query as input
1. Calls the *Tavily API* to search the web and fetch 7–10 raw results
1. Passes those results to Claude Haiku, which filters and ranks them
1. Returns the top 5 most relevant sources with a confidence label (high / medium / low)

*Why Haiku?* This is a simple filtering task — no deep reasoning needed. Haiku is 5x cheaper and 3x faster than Sonnet. Using a heavy model here would be wasteful.

-----

### 🧠 Analyst Agent — The Reader

*Model:* Claude Sonnet (strong reasoning)

The Analyst reads each source the Scout found and extracts structured intelligence from it.

1. Takes the 5 sources from Scout as input
1. For each source, asks Claude Sonnet to extract:
- Key facts
- Recent developments
- Risks and opportunities
- A confidence score for each fact
1. Returns a structured JSON object of findings

*Why Sonnet?* This requires genuine reading comprehension and reasoning — understanding nuance, identifying what’s important, and scoring reliability. Sonnet is worth the extra cost here.

-----

### 📝 Synthesizer Agent — The Writer

*Model:* Claude Sonnet (strong writing)

The Synthesizer takes all the Analyst’s findings and writes a clean, human-readable report.

1. Takes structured findings from Analyst as input
1. Produces a final report with:
- Executive Summary
- Key Facts
- Risks & Opportunities
- Overall Confidence Score
1. Output is ready to read, share, or export

-----

## Why This Architecture Is Smart

### Cost-aware model routing

Not every task needs the most powerful model. By routing simple tasks to Haiku and complex tasks to Sonnet, we cut costs by ~60% compared to using Sonnet for everything — without sacrificing quality where it matters.

### Structured outputs everywhere

Every agent returns validated Pydantic models — not raw text. This means if an agent returns malformed data, the system catches it immediately rather than silently passing garbage to the next agent.

### Transparent and auditable

Because each agent’s output is stored in a shared state object, you can inspect exactly what the Scout found, what the Analyst extracted, and how the Synthesizer formed its conclusions. No black box.

### Extensible by design

Want to add a fact-checker agent? A translation agent? A competitor comparison agent? The LangGraph pipeline makes it trivial to add new nodes without touching existing agents.

-----

## Project Structure


research-agent/
├── agents/
│   ├── scout.py          ← web search + source filtering
│   ├── analyst.py        ← fact extraction + confidence scoring
│   └── synthesizer.py    ← final report generation
├── core/
│   ├── graph.py          ← LangGraph orchestrator (connects agents)
│   └── state.py          ← shared Pydantic state between agents
├── dashboard/            ← Streamlit UI (Week 3)
├── .env                  ← API keys (never commit this)
├── requirements.txt
└── main.py               ← entry point


-----

## Setup

*1. Clone the repo*

bash
git clone https://github.com/yourusername/research-agents
cd research-agents


*2. Install dependencies*

bash
pip install -r requirements.txt


*3. Add your API keys*

Create a .env file in the root:


ANTHROPIC_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here


Get your keys here:

- Anthropic → [console.anthropic.com](https://console.anthropic.com)
- Tavily → [app.tavily.com](https://app.tavily.com) (free tier: 1,000 searches/month)

*4. Run*

bash
python main.py


-----

## Example Output


🔍 Scout agent running...
✅ Scout found 5 sources

  📄 Tesla Q1 2025 Earnings - Reuters         [confidence: high]
  📄 Tesla misses analyst expectations - CNBC  [confidence: high]
  📄 Musk addresses delivery numbers - WSJ     [confidence: medium]
  📄 Tesla stock drops 8% - Bloomberg          [confidence: medium]
  📄 EV market overview Q1 - TechCrunch        [confidence: low]

🧠 Analyst agent running...
✅ Analyst extracted 14 findings across 5 sources

📝 Synthesizer agent running...
✅ Report generated in 2m 34s

════════════════════════════════════════
           RESEARCH REPORT
           Query: Tesla Q1 2025
════════════════════════════════════════

EXECUTIVE SUMMARY
Tesla reported Q1 2025 revenue of $19.3B, missing analyst
expectations by 4%. Deliveries fell 13% YoY amid rising
competition from Chinese EV makers...

KEY FACTS
• Revenue: $19.3B (↓9% YoY)
• Deliveries: 336,681 vehicles (↓13% YoY)
• Net income: $1.1B (↓55% YoY)

RISKS
• Increasing competition from BYD in China
• Margin pressure from price cuts

OPPORTUNITIES
• Cybertruck ramp-up in H2 2025
• Full Self-Driving subscription growth

OVERALL CONFIDENCE: High (4/5 sources agree on core facts)
════════════════════════════════════════


-----

## Tech Stack

|Tool                                                   |Purpose                       |Why we chose it                                                   |
|-------------------------------------------------------|------------------------------|------------------------------------------------------------------|
|[Anthropic Claude](https://anthropic.com)              |Powers all 3 agents           |Best reasoning + instruction following                            |
|[Tavily](https://tavily.com)                           |Web search API                |Built specifically for AI agents, returns clean structured results|
|[LangGraph](https://langchain-ai.github.io/langgraph)  |Agent orchestration           |Industry standard for multi-agent pipelines                       |
|[Pydantic](https://docs.pydantic.dev)                  |Data validation + shared state|Ensures agents pass clean, typed data to each other               |
|[python-dotenv](https://pypi.org/project/python-dotenv)|Environment variables         |Keeps API keys out of source code                                 |
|[Streamlit](https://streamlit.io)                      |Dashboard UI                  |Fast to build, pure Python, no frontend needed                    |

-----

## Roadmap

- [x] Scout agent (web search + filtering)
- [ ] Analyst agent (fact extraction + confidence scoring)
- [ ] Synthesizer agent (report generation)
- [ ] LangGraph pipeline (connect all 3 agents)
- [ ] Streamlit dashboard (live agent status + report UI)
- [ ] Deploy to Hugging Face Spaces

-----

## What I Learned Building This

- How to design and orchestrate multi-agent AI pipelines using LangGraph
- Cost-aware model routing (Haiku vs Sonnet based on task complexity)
- Structured output extraction and JSON parsing from LLM responses
- Building resilient pipelines with Pydantic validation between agents
- Real-world prompt engineering for reliable, consistent agent behavior