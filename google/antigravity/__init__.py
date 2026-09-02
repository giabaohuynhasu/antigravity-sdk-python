# Copyright 2026 Google LLC & Gia Bao Huynh (Jun)
# Licensed under the Apache License, Version 2.0

"""Google Antigravity SDK for building AI agents and Multi-Agent Research Ecosystems."""

from google.antigravity.agent import Agent
from google.antigravity.claude import ClaudeCoworkBridge
from google.antigravity.claude import ClaudeToolDefinition
from google.antigravity.connections.connection import AgentConfig
from google.antigravity.connections.local.litert_connection_config import LiteRTAgentConfig
from google.antigravity.connections.local.litert_connection_config import LiteRTBackend
from google.antigravity.connections.local.local_connection_config import LocalAgentConfig
from google.antigravity.connections.local.local_openai_connection_config import LocalOpenAIAgentConfig
from google.antigravity.science import CNACensusAnalytics
from google.antigravity.science import LongevitySimulator
from google.antigravity.science import QueueingModel
from google.antigravity.tools.research import DuckDBSQLTool
from google.antigravity.tools.research import NotebookLMTool
from google.antigravity.tools.research import ResearchToolResult
from google.antigravity.tools.research import SparkEmailTool
from google.antigravity.tools.tool_context import ToolContext
from google.antigravity.types import AgentBehavior
from google.antigravity.types import Audio
from google.antigravity.types import BuiltinTools
from google.antigravity.types import CapabilitiesConfig
from google.antigravity.types import Content
from google.antigravity.types import CustomSystemInstructions
from google.antigravity.types import Document
from google.antigravity.types import GeminiAPIEndpoint
from google.antigravity.types import GeminiModelOptions
from google.antigravity.types import Image
from google.antigravity.types import ModelAPIRetryConfig
from google.antigravity.types import ModelEndpoint
from google.antigravity.types import ModelOutputRetryConfig
from google.antigravity.types import ModelTarget
from google.antigravity.types import ModelType
from google.antigravity.types import RetryConfig
from google.antigravity.types import SystemInstructions
from google.antigravity.types import SystemInstructionSection
from google.antigravity.types import TemplatedSystemInstructions
from google.antigravity.types import ThinkingLevel
from google.antigravity.types import ToolExecutionError
from google.antigravity.types import UsageMetadata
from google.antigravity.types import VertexEndpoint
from google.antigravity.types import Video
from google.antigravity.types import from_bytes
from google.antigravity.types import from_file

__all__ = [
    "Agent",
    "AgentConfig",
    "LocalAgentConfig",
    "LiteRTAgentConfig",
    "LiteRTBackend",
    "LocalOpenAIAgentConfig",
    "ClaudeCoworkBridge",
    "ClaudeToolDefinition",
    "QueueingModel",
    "LongevitySimulator",
    "CNACensusAnalytics",
    "NotebookLMTool",
    "DuckDBSQLTool",
    "SparkEmailTool",
    "ResearchToolResult",
    "ToolContext",
    "AgentBehavior",
    "Audio",
    "BuiltinTools",
    "CapabilitiesConfig",
    "Content",
    "CustomSystemInstructions",
    "Document",
    "GeminiAPIEndpoint",
    "GeminiModelOptions",
    "Image",
    "ModelAPIRetryConfig",
    "ModelEndpoint",
    "ModelOutputRetryConfig",
    "ModelTarget",
    "ModelType",
    "RetryConfig",
    "SystemInstructions",
    "SystemInstructionSection",
    "TemplatedSystemInstructions",
    "ThinkingLevel",
    "UsageMetadata",
    "VertexEndpoint",
    "Video",
    "ToolExecutionError",
    "from_bytes",
    "from_file",
]
