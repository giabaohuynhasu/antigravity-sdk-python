"""
Example: Claude Cowork MCP Bridge with Google Antigravity SDK
Demonstrates how to register custom tools and export them to Claude Cowork.
"""

from google.antigravity import ClaudeCoworkBridge, QueueingModel

# 1. Initialize Claude Bridge
bridge = ClaudeCoworkBridge(agent_name="Antigravity-Research-Copilot")

# 2. Register a Scientific Tool for Claude
@bridge.register_tool(
    name="calculate_queueing_instability",
    description="Compute critical divergence horizon t* and workload for M/G/1 queueing models",
    input_schema={
        "type": "object",
        "properties": {
            "lambda_0": {"type": "number", "description": "Initial arrival rate"},
            "alpha": {"type": "number", "description": "Compounding acceleration rate"},
            "mu": {"type": "number", "description": "Remediation capacity rate"}
        },
        "required": ["lambda_0", "alpha", "mu"]
    },
    read_only=True
)
def compute_queue(lambda_0: float, alpha: float, mu: float) -> dict:
    qm = QueueingModel(lambda_0=lambda_0, alpha=alpha, mu=mu)
    return {
        "critical_horizon_years": round(qm.critical_horizon(), 2),
        "initial_traffic_intensity": round(qm.traffic_intensity(0.0), 3)
    }

# 3. List tools formatted for Claude Cowork
tools = bridge.list_tools()
print(f"Exported {len(tools)} tools for Claude Cowork:")
for t in tools:
    print(f" - {t['name']}: {t['description']}")

# 4. Simulate Claude summoning the tool
res = bridge.execute_tool("calculate_queueing_instability", {
    "lambda_0": 0.015,
    "alpha": 0.18,
    "mu": 0.052
})
print("\nClaude Tool Execution Output:")
print(res["content"][0]["text"])
