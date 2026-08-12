"""
Stateful Thread & Tool-Use Run Loop Simulator.
This module implements a lightweight, zero-dependency Python reconstruction
of OpenAI's core agentic platform abstractions. Specifically, it models:

1. The ChatML Tokenizer Layer:
   Parses structured, role-based message arrays into boundary-token delimited flat streams,
   ensuring strict separation between system guidelines and user-space prompt injections.

2. The Stateful Thread and Assistant Database:
   Handles server-managed state persistence, and file retrieval (mock RAG indices).

3. The Tool-Execution Run Loop State Machine:
   Maintains a robust state machine transition:
   queued -> in_progress -> requires_action -> completed
   orchestrating multi-turn function call schema resolution and result integration.
"""

import json
from typing import List, Dict, Any, Callable, Optional


class PromptInjectionException(Exception):
    """Raised when an raw user prompt contains malicious system token attempts."""
    pass


class ChatMLTokenizer:
    """
    Simulates a secure ChatML tokenizer that structures role-based messages
    and guards the system instructions from user-space privilege escalations.
    """
    START_TAG = "<|im_start|>"
    END_TAG = "<|im_end|>"

    @classmethod
    def encode(cls, messages: List[Dict[str, str]]) -> str:
        """
        Encodes a structured array of role-based messages into a single ChatML stream.
        Delineates role contexts using unforgeable boundary tags.
        """
        encoded_stream = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            # Guard against unescaped system tokens injected in user input to emulate jailbreaks
            if role == "user" and (cls.START_TAG in content or cls.END_TAG in content):
                raise PromptInjectionException(
                    "Malicious ChatML boundary token detected inside user message payload!"
                )

            encoded_stream.append(f"{cls.START_TAG}{role}\n{content}{cls.END_TAG}")

        return "\n".join(encoded_stream)


class MockVectorStore:
    """
    Simulates a Retrieval-Augmented Generation (RAG) vector database index.
    """
    def __init__(self):
        self.documents = {}

    def upload_file(self, file_id: str, content: str):
        self.documents[file_id] = content

    def semantic_search(self, query: str) -> str:
        """
        Simple keyword-based semantic matching simulation returning matched file content.
        """
        query_words = set(query.lower().split())
        best_match = None
        max_overlap = 0

        for file_id, content in self.documents.items():
            content_lower = content.lower()
            overlap = sum(1 for word in query_words if word in content_lower)
            if overlap > max_overlap:
                max_overlap = overlap
                best_match = content

        return best_match if best_match else "No relevant documents found."


class Assistant:
    """
    Represents a prompt-steered Assistant configuration.
    """
    def __init__(self, assistant_id: str, instructions: str, model: str = "gpt-4o"):
        self.id = assistant_id
        self.instructions = instructions
        self.model = model
        self.tools = {}
        self.file_ids = []

    def register_tool(self, name: str, schema: Dict[str, Any], callback: Callable):
        self.tools[name] = {
            "schema": schema,
            "callback": callback
        }


class Thread:
    """
    Represents a server-managed stateful conversation Thread.
    """
    def __init__(self, thread_id: str):
        self.id = thread_id
        self.messages = []

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})


class Run:
    """
    Represents a thread run state machine.
    States: queued -> in_progress -> requires_action -> completed
    """
    def __init__(self, run_id: str, thread_id: str, assistant_id: str):
        self.id = run_id
        self.thread_id = thread_id
        self.assistant_id = assistant_id
        self.status = "queued"
        self.required_action = None


class AssistantsEngine:
    """
    The main Assistants API execution orchestrator managing thread run state machines.
    """
    def __init__(self):
        self.assistants = {}
        self.threads = {}
        self.runs = {}
        self.vector_store = MockVectorStore()
        self.run_counter = 0

    def create_assistant(self, assistant_id: str, instructions: str) -> Assistant:
        assistant = Assistant(assistant_id, instructions)
        self.assistants[assistant_id] = assistant
        return assistant

    def create_thread(self, thread_id: str) -> Thread:
        thread = Thread(thread_id)
        self.threads[thread_id] = thread
        return thread

    def create_run(self, thread_id: str, assistant_id: str) -> Run:
        self.run_counter += 1
        run_id = f"run_{self.run_counter}"
        run = Run(run_id, thread_id, assistant_id)
        self.runs[run_id] = run
        return run

    def execute_run_loop(self, run_id: str) -> str:
        """
        Executes the Assistant run loop state machine.
        If a tool invocation is resolved, it halts at 'requires_action' state.
        Otherwise, it retrieves RAG context, compiles ChatML, completes, and goes to 'completed'.
        """
        run = self.runs.get(run_id)
        if not run:
            return "Run not found."

        thread = self.threads[thread_id := run.thread_id]
        assistant = self.assistants[run.assistant_id]

        if run.status == "queued":
            run.status = "in_progress"

        if run.status == "in_progress":
            # 1. Simulate RAG Step: Search files if vector indexes exist
            rag_context = ""
            if assistant.file_ids and thread.messages:
                last_msg = thread.messages[-1]["content"]
                rag_context = self.vector_store.semantic_search(last_msg)

            # 2. Compile ChatML array for execution
            messages_to_compile = [{"role": "system", "content": assistant.instructions}]
            if rag_context:
                messages_to_compile.append({
                    "role": "system",
                    "content": f"Context from uploaded file: {rag_context}"
                })
            messages_to_compile.extend(thread.messages)

            # Strict verification of ChatML compilation safety
            try:
                chatml_payload = ChatMLTokenizer.encode(messages_to_compile)
            except PromptInjectionException as e:
                run.status = "failed"
                raise e

            # 3. Simulate LLM Parsing & Tool invocation detection
            # Check if user query matches any registered tool keywords
            last_user_query = thread.messages[-1]["content"].lower() if thread.messages else ""
            matched_tool_name = None

            for tool_name in assistant.tools:
                if tool_name.replace("_", " ") in last_user_query or tool_name in last_user_query:
                    matched_tool_name = tool_name
                    break

            if matched_tool_name:
                # Transition to 'requires_action' state requesting external output
                run.status = "requires_action"
                # Mock argument generation based on query
                tool_args = {}
                if "path" in last_user_query:
                    # extract simulated file path if any
                    words = last_user_query.split()
                    for word in words:
                        if "/" in word or "." in word:
                            tool_args["path"] = word
                            break
                    if "path" not in tool_args:
                        tool_args["path"] = "root/"

                run.required_action = {
                    "tool_calls": [
                        {
                            "id": f"call_{run_id}",
                            "type": "function",
                            "function": {
                                "name": matched_tool_name,
                                "arguments": json.dumps(tool_args)
                            }
                        }
                    ]
                }
                return f"Run paused. State: {run.status}. Tool Execution Required."

            # If no tools required, complete execution directly
            mock_reply = "Default model response."
            if "hello" in last_user_query:
                mock_reply = "Hello! I am your stateful model-as-platform assistant."
            elif "who are you" in last_user_query:
                mock_reply = f"I am a stateful AI Assistant guided by: {assistant.instructions}"

            thread.add_message("assistant", mock_reply)
            run.status = "completed"
            return f"Run completed. State: {run.status}."

        return f"Run is currently in: {run.status}."

    def submit_tool_outputs(self, run_id: str, tool_outputs: List[Dict[str, Any]]) -> str:
        """
        Submits external tool outputs back to the stateful thread and resumes the run loop.
        """
        run = self.runs.get(run_id)
        if not run or run.status != "requires_action":
            return "Run is not awaiting tool outputs."

        thread = self.threads[run.thread_id]
        assistant = self.assistants[run.assistant_id]

        for output in tool_outputs:
            tool_call_id = output.get("tool_call_id")
            result = output.get("output", "")

            # Append tool output results back to message context
            thread.add_message(
                "system",
                f"Tool result for call {tool_call_id}: {result}"
            )

        # Transition state back to progress and complete the execution
        run.status = "in_progress"
        run.required_action = None

        # Resolve tool-related response completion
        last_query = thread.messages[-2]["content"] if len(thread.messages) >= 2 else ""
        thread.add_message(
            "assistant",
            f"Successfully processed tool output. Result: {tool_outputs[0].get('output')}"
        )
        run.status = "completed"

        return f"Run resumed and completed. State: {run.status}."
