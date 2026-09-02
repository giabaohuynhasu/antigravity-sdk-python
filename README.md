# ⚡ Google Antigravity Python SDK (Enhanced v0.2.0)
[![PyPI version](https://img.shields.io/badge/version-0.2.0--enhanced-blue.svg)](https://github.com/giabaohuynhasu/antigravity-sdk-python)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0008--2372--5852-green.svg)](https://orcid.org/0009-0008-2372-5852)
[![PhilPeople](https://img.shields.io/badge/PhilPeople-Gia_Bao_Huynh-0284c7.svg)](https://philpeople.org/profiles/gia-bao-huynh)
[![Academia.edu](https://img.shields.io/badge/Academia.edu-GiaBảoHuỳnh30-red.svg)](https://independent.academia.edu/GiaB%E1%BA%A3oHu%E1%BB%B3nh30)
[![Showcase](https://img.shields.io/badge/Academic_Portal-Live_Showcase-purple.svg)](https://giabaohuynhasu.github.io/research-landing/)

A modern, high-performance Python SDK for designing, executing, and orchestrating **autonomous AI agents**, **Claude Cowork MCP multi-agent bridges**, and **frontier scientific simulations** powered by Google Antigravity.

---

## 🌟 Key Features

1. **🚀 Full Google Antigravity Agent Lifecycle:**
   - Multi-turn conversation sessions, custom persona instructions, and tool calling runners.
   - Built-in capabilities: bash/powershell command execution, file read/write, browser automation, and subagent orchestration.

2. **🔌 Claude Cowork & Model Context Protocol (MCP) Bridge (`google.antigravity.claude`):**
   - Seamlessly expose Antigravity agents as Claude Cowork tools.
   - Run bidirectional multi-agent research workflows between Claude Sonnet and Google Gemini.

3. **📊 Scientific & Queueing Theory Computational Engine (`google.antigravity.science`):**
   - $M/G/1$ Cybernetic Queueing Instability Model with exponential discovery arrivals $\lambda(t) = \lambda_0 e^{\alpha t}$, Pollaczek-Khinchine workload $W(t)$, and critical divergence horizon $t^*$.
   - Gompertz-Makeham Longevity Asymmetry Hazard Simulator (ALRP).
   - Full-population Herfindahl-Hirschman Index ($HHI$) and MITRE decentralization analyzer.

4. **🧠 Native Research Tools (`google.antigravity.tools.research`):**
   - Direct querying of private **Google NotebookLM** research notebooks (`NotebookLMTool`).
   - High-speed in-memory **DuckDB SQL Engine** (`DuckDBSQLTool`).
   - Automated institutional academic email dispatch via **Gemini Spark** (`SparkEmailTool`).

---

## 📦 Installation

```bash
pip install google-antigravity
```

Or install in editable mode for research development:
```bash
git clone https://github.com/giabaohuynhasu/antigravity-sdk-python.git
cd antigravity-sdk-python
pip install -e .
```

---

## ⚡ Quickstart Examples

### 1. Claude Cowork MCP Tool Bridge
```python
from google.antigravity import ClaudeCoworkBridge, QueueingModel

bridge = ClaudeCoworkBridge(agent_name="Antigravity-Research-Copilot")

@bridge.register_tool(
    name="calculate_queueing_instability",
    description="Compute critical divergence horizon t* and workload for M/G/1 queueing models",
    read_only=True
)
def compute_queue(lambda_0: float = 0.015, alpha: float = 0.18, mu: float = 0.052) -> dict:
    qm = QueueingModel(lambda_0=lambda_0, alpha=alpha, mu=mu)
    return {
        "critical_horizon_years": round(qm.critical_horizon(), 2),
        "initial_traffic_intensity": round(qm.traffic_intensity(0.0), 3)
    }

# Export tools to Claude Cowork
tools = bridge.list_tools()
```

### 2. Scientific Queueing & Longevity Simulation
```python
from google.antigravity import QueueingModel, LongevitySimulator

qm = QueueingModel(lambda_0=0.015, alpha=0.18, mu=0.052)
t_star = qm.critical_horizon()
print(f"Critical divergence horizon t*: {t_star:.2f} years")

# Mortality hazard rate at age 80
hazard = LongevitySimulator.hazard_rate(age=80.0)
print(f"Mortality hazard at age 80: {hazard:.6f}")
```

### 3. Native Research Tools (DuckDB & NotebookLM)
```python
from google.antigravity import DuckDBSQLTool, NotebookLMTool

# Query tabular data via DuckDB
sql_tool = DuckDBSQLTool()
res = sql_tool.execute("SELECT 42 AS answer, 'Antigravity' AS engine")
print(res.output)

# Query private Google NotebookLM corpus
nlm = NotebookLMTool()
query_res = nlm.query("Summarize ALRP queueing instability findings")
```

---

## 🧪 Testing

Run test suite with `unittest` or `pytest`:
```bash
python -m unittest discover -s google/antigravity -p "*_test.py"
```

---

## 📜 Citation & Academic Attribution

```bibtex
@software{huynh2026antigravity_sdk,
  author = {Huynh, Gia Bao and Google Antigravity Team},
  title = {Google Antigravity Python SDK: Enhanced Multi-Agent Research Ecosystem},
  url = {https://github.com/giabaohuynhasu/antigravity-sdk-python},
  year = {2026}
}
```
