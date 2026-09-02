# Copyright 2026 Google LLC & Gia Bao Huynh (Jun)
# Licensed under the Apache License, Version 2.0

"""Claude Cowork & Model Context Protocol (MCP) Bridge for Google Antigravity."""

from __future__ import annotations

import json
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field


class ClaudeToolDefinition(BaseModel):
    """Definition of an MCP tool exposed to Claude Cowork."""
    name: str = Field(description="Unique name of the tool, e.g. antigravity_run_code")
    description: str = Field(description="Actionable explanation of tool purpose and return schema")
    input_schema: Dict[str, Any] = Field(default_factory=dict, description="JSON Schema for arguments")
    read_only: bool = Field(default=False, description="Whether the tool is read-only")


class ClaudeCoworkBridge:
    """
    Bridge connecting Google Antigravity Agents to Anthropic Claude Cowork.
    Enables Claude to summon Antigravity tools and Antigravity agents to delegate to Claude.
    """

    def __init__(self, agent_name: str = "Antigravity-Research-Copilot"):
        self.agent_name = agent_name
        self.registered_tools: Dict[str, Callable[..., Any]] = {}
        self.tool_definitions: Dict[str, ClaudeToolDefinition] = {}

    def register_tool(
        self,
        name: str,
        description: str,
        input_schema: Optional[Dict[str, Any]] = None,
        read_only: bool = False,
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Decorator to register a function as an MCP tool for Claude."""
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self.registered_tools[name] = func
            self.tool_definitions[name] = ClaudeToolDefinition(
                name=name,
                description=description,
                input_schema=input_schema or {"type": "object", "properties": {}},
                read_only=read_only
            )
            return func
        return decorator

    def list_tools(self) -> List[Dict[str, Any]]:
        """Return the list of tools formatted for Claude Cowork / MCP tools/list."""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.input_schema,
                "annotations": {
                    "readOnlyHint": tool.read_only
                }
            }
            for tool in self.tool_definitions.values()
        ]

    def execute_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a registered tool and format response for Claude."""
        if name not in self.registered_tools:
            return {
                "content": [{"type": "text", "text": f"Error: Tool '{name}' not found."}],
                "isError": True
            }
        try:
            result = self.registered_tools[name](**arguments)
            text_output = json.dumps(result, indent=2) if isinstance(result, (dict, list)) else str(result)
            return {
                "content": [{"type": "text", "text": text_output}],
                "isError": False
            }
        except Exception as e:
            return {
                "content": [{"type": "text", "text": f"Error executing tool '{name}': {str(e)}"}],
                "isError": True
            }
