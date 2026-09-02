# Copyright 2026 Google LLC & Gia Bao Huynh (Jun)
# Licensed under the Apache License, Version 2.0

"""Native Research Tools (NotebookLM, DuckDB SQL, Gemini Spark Email) for Google Antigravity."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class ResearchToolResult(BaseModel):
    """Result returned by native research tools."""
    output: str
    success: bool = True
    error: Optional[str] = None


class NotebookLMTool:
    """Tool for querying the user's private Google NotebookLM research notebooks."""

    def __init__(self, default_notebook_id: str = "24fb3456-0d1a-4e3d-864b-952523aa982f"):
        self.default_notebook_id = default_notebook_id
        self.nlm_path = Path("C:/Users/nswcl/.local/bin/nlm.exe")

    def query(self, prompt: str, notebook_id: Optional[str] = None) -> ResearchToolResult:
        """Query a Google NotebookLM notebook."""
        nid = notebook_id or self.default_notebook_id
        if not self.nlm_path.exists():
            return ResearchToolResult(
                output="",
                success=False,
                error="nlm.exe not found at C:/Users/nswcl/.local/bin/nlm.exe"
            )
        try:
            cmd = f'& "{self.nlm_path}" query "{nid}" "{prompt}"'
            proc = subprocess.run(
                ["powershell.exe", "-NoProfile", "-Command", cmd],
                capture_output=True,
                text=True,
                timeout=60
            )
            out = proc.stdout.strip() if proc.stdout else proc.stderr.strip()
            return ResearchToolResult(output=out, success=proc.returncode == 0)
        except Exception as e:
            return ResearchToolResult(output="", success=False, error=str(e))


class DuckDBSQLTool:
    """Tool for executing high-speed SQL queries directly against memory or CSV/Parquet files."""

    def execute(self, sql_query: str) -> ResearchToolResult:
        """Execute a DuckDB SQL query and return tabular markdown string."""
        try:
            import duckdb
            con = duckdb.connect()
            df = con.execute(sql_query).df()
            out = df.to_markdown(index=False) if hasattr(df, "to_markdown") else df.to_string(index=False)
            return ResearchToolResult(output=out, success=True)
        except Exception as e:
            return ResearchToolResult(output="", success=False, error=str(e))


class SparkEmailTool:
    """Tool for sending automated academic reports to ASU institutional email via SMTP."""

    def send(
        self,
        subject: str,
        body: str,
        recipient: str = "huynhbao@asu.edu",
        sender_email: str = "thuaquan228@gmail.com",
        app_password: str = "tftgqgjmfifdmtzz"
    ) -> ResearchToolResult:
        """Send an email report via Gmail TLS Relay."""
        import smtplib
        from email.mime.text import MIMEText
        from email.utils import formataddr

        try:
            msg = MIMEText(body, "plain", "utf-8")
            msg["From"] = formataddr(("Antigravity Research OS", sender_email))
            msg["To"] = formataddr(("Gia Bao Huynh (Jun)", recipient))
            msg["Subject"] = subject

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, app_password)
                server.send_message(msg)
            return ResearchToolResult(output=f"[✓ Email successfully sent to {recipient}]", success=True)
        except Exception as e:
            return ResearchToolResult(output="", success=False, error=str(e))
