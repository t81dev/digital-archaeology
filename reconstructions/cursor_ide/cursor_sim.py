"""
Cursor IDE Substrate & Agentic Workspace Simulator.

A zero-dependency Python reconstruction of Cursor IDE's core abstractions:
1. Context Packet Assembly Pipeline (budgeted prompt packet from open files, diagnostics, vector/keyword indexing, and .cursorrules)
2. Diff-Propose & Apply Trust Boundary (patch generation, line-level diff, speculative application, approval checkpoints)
3. Autonomy Gradient Engine (Completion A0, Inline Edit A1, Chat A2, Supervised Agent Loop A3)
4. Agent Tool Runner (workspace operations: file read/write, terminal execution, diagnostic self-healing)
"""

import re
import difflib
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set


@dataclass
class Diagnostic:
    file_path: str
    line: int
    severity: str  # "error", "warning"
    message: str


@dataclass
class CodeChunk:
    chunk_id: str
    file_path: str
    start_line: int
    end_line: int
    content: str
    symbol_name: str = ""


@dataclass
class ContextPacket:
    system_instructions: str
    project_rules: List[str]
    active_file: Optional[str]
    selection: Optional[str]
    diagnostics: List[Diagnostic]
    retrieved_chunks: List[CodeChunk]
    user_query: str
    token_budget: int
    assembled_prompt: str = ""


class VectorKeywordIndexer:
    """Simulates hybrid (dense embedding + sparse keyword) repository retrieval."""
    def __init__(self):
        self.chunks: List[CodeChunk] = []

    def add_file(self, file_path: str, content: str):
        lines = content.splitlines()
        if not lines:
            return
        # Simple structural chunking by functions/classes or line blocks
        current_chunk_lines = []
        start_line = 1
        current_symbol = "file_scope"

        for i, line in enumerate(lines, start=1):
            if line.strip().startswith(("def ", "class ", "function ", "interface ", "struct ")):
                if current_chunk_lines:
                    chunk_text = "\n".join(current_chunk_lines)
                    chunk_id = f"{file_path}:{start_line}-{i-1}"
                    self.chunks.append(CodeChunk(chunk_id, file_path, start_line, i-1, chunk_text, current_symbol))
                    current_chunk_lines = []
                start_line = i
                current_symbol = line.strip().split("(")[0].split("{")[0]

            current_chunk_lines.append(line)

        if current_chunk_lines:
            chunk_text = "\n".join(current_chunk_lines)
            chunk_id = f"{file_path}:{start_line}-{len(lines)}"
            self.chunks.append(CodeChunk(chunk_id, file_path, start_line, len(lines), chunk_text, current_symbol))

    def search(self, query: str, top_k: int = 3) -> List[CodeChunk]:
        query_terms = set(re.findall(r'\w+', query.lower()))
        scored_chunks: List[Tuple[float, CodeChunk]] = []

        for chunk in self.chunks:
            chunk_terms = set(re.findall(r'\w+', chunk.content.lower()))
            overlap = len(query_terms.intersection(chunk_terms))
            # Hybrid score simulation: term overlap + symbol match bonus
            symbol_bonus = 2.0 if chunk.symbol_name and chunk.symbol_name.lower() in query.lower() else 0.0
            score = float(overlap) + symbol_bonus
            if score > 0:
                scored_chunks.append((score, chunk))

        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        return [chunk for score, chunk in scored_chunks[:top_k]]


class ContextAssembler:
    """Assembles budgeted context packets for LLM inference."""
    def __init__(self, indexer: VectorKeywordIndexer):
        self.indexer = indexer

    def build_packet(
        self,
        user_query: str,
        workspace_files: Dict[str, str],
        active_file: Optional[str] = None,
        selection: Optional[str] = None,
        diagnostics: Optional[List[Diagnostic]] = None,
        project_rules: Optional[List[str]] = None,
        token_budget: int = 2000
    ) -> ContextPacket:
        project_rules = project_rules or []
        diagnostics = diagnostics or []

        # RAG Search over indexed repository
        retrieved_chunks = self.indexer.search(user_query, top_k=3)

        system_instructions = "You are an AI-native coding assistant operating inside Cursor IDE."

        # Assemble prompt text while respecting budget (approximated as 4 chars per token)
        prompt_parts = [f"System: {system_instructions}"]

        if project_rules:
            prompt_parts.append("Project Rules (.cursorrules):")
            for rule in project_rules:
                prompt_parts.append(f"- {rule}")

        if active_file and active_file in workspace_files:
            prompt_parts.append(f"\nActive File ({active_file}):\n```{workspace_files[active_file]}```")

        if selection:
            prompt_parts.append(f"\nSelected Code:\n```{selection}```")

        if diagnostics:
            prompt_parts.append("\nLSP Diagnostics / Linter Errors:")
            for diag in diagnostics:
                prompt_parts.append(f"- [{diag.severity.upper()}] {diag.file_path}:{diag.line} - {diag.message}")

        if retrieved_chunks:
            prompt_parts.append("\nRetrieved Codebase Context:")
            for chunk in retrieved_chunks:
                prompt_parts.append(f"--- Chunk from {chunk.file_path} ({chunk.start_line}-{chunk.end_line}) ---")
                prompt_parts.append(f"```{chunk.content}```")

        prompt_parts.append(f"\nUser Request:\n{user_query}")

        full_prompt = "\n".join(prompt_parts)
        # Budget truncation simulation
        max_chars = token_budget * 4
        if len(full_prompt) > max_chars:
            full_prompt = full_prompt[:max_chars] + "\n...[Truncated due to Context Token Budget]..."

        return ContextPacket(
            system_instructions=system_instructions,
            project_rules=project_rules,
            active_file=active_file,
            selection=selection,
            diagnostics=diagnostics,
            retrieved_chunks=retrieved_chunks,
            user_query=user_query,
            token_budget=token_budget,
            assembled_prompt=full_prompt
        )


@dataclass
class SpeculativePatch:
    file_path: str
    original_content: str
    proposed_content: str
    diff_unified: str
    approved: Optional[bool] = None


class DiffApplyEngine:
    """Simulates speculative patch generation, diff rendering, and trust checkpoint approval."""

    @staticmethod
    def create_patch(file_path: str, original_content: str, proposed_content: str) -> SpeculativePatch:
        orig_lines = original_content.splitlines(keepends=True)
        prop_lines = proposed_content.splitlines(keepends=True)

        diff = "".join(difflib.unified_diff(
            orig_lines, prop_lines,
            fromfile=f"a/{file_path}", tofile=f"b/{file_path}"
        ))

        return SpeculativePatch(
            file_path=file_path,
            original_content=original_content,
            proposed_content=proposed_content,
            diff_unified=diff
        )

    @staticmethod
    def apply_patch(patch: SpeculativePatch, workspace: Dict[str, str], user_accepts: bool) -> bool:
        patch.approved = user_accepts
        if user_accepts:
            workspace[patch.file_path] = patch.proposed_content
            return True
        return False


class CursorWorkspaceAgent:
    """Simulates a supervised workspace agent executing tool calls and self-correcting loops."""
    def __init__(self, workspace: Dict[str, str], project_rules: Optional[List[str]] = None):
        self.workspace: Dict[str, str] = workspace
        self.project_rules: List[str] = project_rules or []
        self.indexer = VectorKeywordIndexer()
        self.refresh_index()
        self.context_assembler = ContextAssembler(self.indexer)
        self.execution_log: List[str] = []
        self.terminal_output_buffer: List[str] = []

    def refresh_index(self):
        self.indexer = VectorKeywordIndexer()
        for path, content in self.workspace.items():
            self.indexer.add_file(path, content)

    def read_file(self, path: str) -> str:
        self.execution_log.append(f"TOOL: read_file({path})")
        return self.workspace.get(path, f"Error: File '{path}' not found.")

    def run_terminal_command(self, cmd: str, require_approval: bool = True, approved: bool = True) -> str:
        self.execution_log.append(f"TOOL: run_terminal_command('{cmd}')")
        if require_approval and not approved:
            output = "Command Execution Rejected by User."
            self.terminal_output_buffer.append(output)
            return output

        # Simulating terminal command behaviors
        if "pytest" in cmd or "test" in cmd:
            # Check for simulated errors in workspace code
            errors = self.get_linter_errors()
            if errors:
                output = f"FAIL: Tests failed due to linter error in {errors[0].file_path}:{errors[0].line}"
            else:
                output = "SUCCESS: 100% tests passed."
        else:
            output = f"Executed: {cmd} (Exit Code 0)"

        self.terminal_output_buffer.append(output)
        return output

    def get_linter_errors(self) -> List[Diagnostic]:
        self.execution_log.append("TOOL: get_linter_errors()")
        diagnostics = []
        for path, content in self.workspace.items():
            lines = content.splitlines()
            for idx, line in enumerate(lines, start=1):
                if "SYNTAX_ERROR" in line or "UNDEFINED_VARIABLE" in line:
                    diagnostics.append(Diagnostic(path, idx, "error", f"Syntax/Type error found: '{line.strip()}'"))
        return diagnostics

    def execute_agent_goal(self, goal: str, max_steps: int = 5) -> Dict[str, str]:
        """
        Executes a supervised agent loop A3:
        1. Context assembly
        2. Tool inspection / edit proposal
        3. Diff application
        4. Test run & self-correction loop
        """
        self.execution_log.append(f"AGENT GOAL STARTED: {goal}")
        step = 0

        while step < max_steps:
            step += 1
            self.execution_log.append(f"--- Step {step} ---")

            # Check diagnostics
            errors = self.get_linter_errors()

            # Assemble context
            packet = self.context_assembler.build_packet(
                user_query=goal,
                workspace_files=self.workspace,
                diagnostics=errors,
                project_rules=self.project_rules
            )

            if not errors:
                # Run tests to verify
                test_result = self.run_terminal_command("pytest", require_approval=False)
                if "SUCCESS" in test_result:
                    self.execution_log.append("AGENT GOAL ACHIEVED: Tests passed cleanly.")
                    break

            # If errors exist, self-correct by editing file
            if errors:
                err = errors[0]
                content = self.workspace[err.file_path]
                fixed_content = content.replace("SYNTAX_ERROR", "FIXED_CODE").replace("UNDEFINED_VARIABLE", "VALID_VARIABLE")

                patch = DiffApplyEngine.create_patch(err.file_path, content, fixed_content)
                self.execution_log.append(f"AGENT PROPOSED PATCH for {err.file_path}:\n{patch.diff_unified}")

                # Apply patch
                DiffApplyEngine.apply_patch(patch, self.workspace, user_accepts=True)
                self.refresh_index()
                self.execution_log.append(f"PATCH APPLIED to {err.file_path}")

        return self.workspace
