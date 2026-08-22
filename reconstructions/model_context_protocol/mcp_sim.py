#!/usr/bin/env python3
"""
Model Context Protocol (MCP) Simulator.
A zero-dependency Python reconstruction demonstrating the host-server RPC capability bus,
session initialization handshake, capability negotiation, JSON Schema tool validation gates,
URI-addressed resource reading, prompt templates, and multi-server tool multiplexing.
"""

import json
import re
from typing import Any, Dict, List, Optional, Tuple, Callable


class JSONRPCError(Exception):
    def __init__(self, code: int, message: str, data: Optional[Any] = None):
        self.code = code
        self.message = message
        self.data = data
        super().__init__(f"JSON-RPC Error {code}: {message}")


class MCPServer:
    """
    A simulated Model Context Protocol (MCP) Server.
    Encapsulates tools, resources, and prompts behind a JSON-RPC 2.0 interface
    with explicit capability negotiation and state machine enforcement.
    """

    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.state = "UNCONNECTED"  # UNCONNECTED, INITIALIZING, INITIALIZED, TERMINATED
        self.protocol_version = "2024-11-05"

        # Capabilities
        self.capabilities = {
            "tools": {"listChanged": True},
            "resources": {"subscribe": True, "listChanged": True},
            "prompts": {"listChanged": True},
            "logging": {}
        }

        # Internal Primitive Stores
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.resources: Dict[str, Dict[str, Any]] = {}
        self.prompts: Dict[str, Dict[str, Any]] = {}

        # Default sample primitive registrations
        self._register_default_primitives()

    def _register_default_primitives(self):
        """Populate initial set of tools, resources, and prompts for simulation."""
        # Tool: execute_sql
        self.register_tool(
            name="execute_sql",
            description="Executes a read-only SQL query on the target database.",
            input_schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "SQL query string"},
                    "limit": {"type": "integer", "description": "Max rows to return"}
                },
                "required": ["query"]
            },
            handler=self._handle_execute_sql
        )

        # Resource: db://schema/users
        self.register_resource(
            uri="db://schema/users",
            name="Users Database Schema",
            description="Database schema definition for the users table.",
            mime_type="application/json",
            content=json.dumps({
                "table": "users",
                "columns": [
                    {"name": "id", "type": "INTEGER", "primary_key": True},
                    {"name": "username", "type": "VARCHAR(255)"},
                    {"name": "email", "type": "VARCHAR(255)"},
                    {"name": "created_at", "type": "TIMESTAMP"}
                ]
            }, indent=2)
        )

        # Prompt: analyze_database
        self.register_prompt(
            name="analyze_database",
            description="Generates an analysis prompt for database performance and indexing.",
            arguments=[
                {"name": "table_name", "description": "Target table name", "required": True}
            ],
            handler=lambda args: [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Please analyze performance indices and common queries for table '{args.get('table_name')}'. Check schema at db://schema/{args.get('table_name')}."
                    }
                }
            ]
        )

    def register_tool(self, name: str, description: str, input_schema: Dict[str, Any], handler: Callable[[Dict[str, Any]], Dict[str, Any]]):
        self.tools[name] = {
            "name": name,
            "description": description,
            "inputSchema": input_schema,
            "handler": handler
        }

    def register_resource(self, uri: str, name: str, description: str, mime_type: str, content: str):
        self.resources[uri] = {
            "uri": uri,
            "name": name,
            "description": description,
            "mimeType": mime_type,
            "content": content
        }

    def register_prompt(self, name: str, description: str, arguments: List[Dict[str, Any]], handler: Callable[[Dict[str, Any]], List[Dict[str, Any]]]):
        self.prompts[name] = {
            "name": name,
            "description": description,
            "arguments": arguments,
            "handler": handler
        }

    def _handle_execute_sql(self, args: Dict[str, Any]) -> Dict[str, Any]:
        query = args["query"]
        limit = args.get("limit", 10)

        if "DROP" in query.upper() or "DELETE" in query.upper():
            return {
                "content": [{"type": "text", "text": "Error: Mutation queries (DROP/DELETE) are blocked on read-only server."}],
                "isError": True
            }

        return {
            "content": [{
                "type": "text",
                "text": f"Execution result for '{query}' (limit {limit}):\n1 | alice | alice@example.com\n2 | bob | bob@example.com"
            }],
            "isError": False
        }

    def validate_tool_args(self, input_schema: Dict[str, Any], arguments: Dict[str, Any]):
        """Simple JSON Schema validator for tool arguments."""
        if input_schema.get("type") == "object":
            req_fields = input_schema.get("required", [])
            for field in req_fields:
                if field not in arguments:
                    raise JSONRPCError(-32602, f"Missing required parameter: '{field}'")

            props = input_schema.get("properties", {})
            for key, val in arguments.items():
                if key in props:
                    expected_type = props[key].get("type")
                    if expected_type == "string" and not isinstance(val, str):
                        raise JSONRPCError(-32602, f"Parameter '{key}' must be a string")
                    elif expected_type == "integer" and not isinstance(val, int):
                        raise JSONRPCError(-32602, f"Parameter '{key}' must be an integer")
                    elif expected_type == "boolean" and not isinstance(val, bool):
                        raise JSONRPCError(-32602, f"Parameter '{key}' must be a boolean")

    def handle_raw_message(self, raw_json: str) -> Optional[str]:
        """Parse raw JSON-RPC string and handle dispatch."""
        try:
            req = json.loads(raw_json)
        except json.JSONDecodeError:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": "Parse error"}
            })

        req_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})

        # Notifications carry no id
        if req_id is None and method == "notifications/initialized":
            if self.state == "INITIALIZING":
                self.state = "INITIALIZED"
            return None

        try:
            result = self.dispatch_method(method, params)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": result
            })
        except JSONRPCError as err:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": err.code, "message": err.message, "data": err.data}
            })
        except Exception as ex:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32603, "message": f"Internal server error: {str(ex)}"}
            })

    def dispatch_method(self, method: str, params: Dict[str, Any]) -> Any:
        # Pre-initialization check
        if method == "initialize":
            if self.state != "UNCONNECTED":
                raise JSONRPCError(-32600, "Server is already initialized")

            self.state = "INITIALIZING"
            client_proto = params.get("protocolVersion")
            return {
                "protocolVersion": self.protocol_version,
                "capabilities": self.capabilities,
                "serverInfo": {
                    "name": self.name,
                    "version": self.version
                }
            }

        # Enforce initialization state lock
        if self.state != "INITIALIZED":
            raise JSONRPCError(-32002, "Server not initialized. Complete initialize handshake first.")

        # Operational methods
        if method == "tools/list":
            return {
                "tools": [
                    {
                        "name": t["name"],
                        "description": t["description"],
                        "inputSchema": t["inputSchema"]
                    }
                    for t in self.tools.values()
                ]
            }
        elif method == "tools/call":
            tool_name = params.get("name")
            if tool_name not in self.tools:
                raise JSONRPCError(-32601, f"Tool '{tool_name}' not found")

            tool_entry = self.tools[tool_name]
            args = params.get("arguments", {})

            # Validate arguments against JSON schema
            self.validate_tool_args(tool_entry["inputSchema"], args)

            # Execute tool handler
            return tool_entry["handler"](args)

        elif method == "resources/list":
            return {
                "resources": [
                    {
                        "uri": r["uri"],
                        "name": r["name"],
                        "description": r["description"],
                        "mimeType": r["mimeType"]
                    }
                    for r in self.resources.values()
                ]
            }
        elif method == "resources/read":
            uri = params.get("uri")
            if uri not in self.resources:
                raise JSONRPCError(-32602, f"Resource URI '{uri}' not found")

            r = self.resources[uri]
            return {
                "contents": [
                    {
                        "uri": r["uri"],
                        "mimeType": r["mimeType"],
                        "text": r["content"]
                    }
                ]
            }

        elif method == "prompts/list":
            return {
                "prompts": [
                    {
                        "name": p["name"],
                        "description": p["description"],
                        "arguments": p["arguments"]
                    }
                    for p in self.prompts.values()
                ]
            }
        elif method == "prompts/get":
            prompt_name = params.get("name")
            if prompt_name not in self.prompts:
                raise JSONRPCError(-32601, f"Prompt '{prompt_name}' not found")

            p = self.prompts[prompt_name]
            args = params.get("arguments", {})
            messages = p["handler"](args)
            return {
                "description": p["description"],
                "messages": messages
            }
        else:
            raise JSONRPCError(-32601, f"Method '{method}' not recognized")


class MCPHost:
    """
    Simulated Model Context Protocol (MCP) Client Host.
    Manages session lifecycle, capability negotiation, human approval consent gates,
    and multi-server tool invocation routing.
    """

    def __init__(self, name: str = "HostApplication", version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.msg_id_counter = 1
        self.servers: Dict[str, MCPServer] = {}
        self.consent_callback: Optional[Callable[[str, str, Dict[str, Any]], bool]] = None

    def register_server(self, server_id: str, server: MCPServer):
        self.servers[server_id] = server

    def set_consent_callback(self, callback: Callable[[str, str, Dict[str, Any]], bool]):
        """Set human approval consent gate callback (server_id, tool_name, args) -> bool."""
        self.consent_callback = callback

    def initialize_server(self, server_id: str) -> Dict[str, Any]:
        """Perform the complete initialize handshake sequence with target server."""
        if server_id not in self.servers:
            raise ValueError(f"Server '{server_id}' not registered in host.")

        server = self.servers[server_id]

        # 1. Send initialize request
        req_id = self.msg_id_counter
        self.msg_id_counter += 1

        init_req = json.dumps({
            "jsonrpc": "2.0",
            "id": req_id,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "roots": {"listChanged": True},
                    "sampling": {}
                },
                "clientInfo": {
                    "name": self.name,
                    "version": self.version
                }
            }
        })

        resp_raw = server.handle_raw_message(init_req)
        assert resp_raw is not None
        resp = json.loads(resp_raw)

        if "error" in resp:
            raise RuntimeError(f"Initialization failed: {resp['error']}")

        # 2. Send notifications/initialized notification
        notif_raw = json.dumps({
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        })
        server.handle_raw_message(notif_raw)

        return resp["result"]

    def list_tools(self, server_id: str) -> List[Dict[str, Any]]:
        server = self.servers[server_id]
        req_id = self.msg_id_counter
        self.msg_id_counter += 1

        req = json.dumps({
            "jsonrpc": "2.0",
            "id": req_id,
            "method": "tools/list"
        })

        resp_raw = server.handle_raw_message(req)
        assert resp_raw is not None
        resp = json.loads(resp_raw)

        if "error" in resp:
            raise JSONRPCError(resp["error"]["code"], resp["error"]["message"])

        return resp["result"]["tools"]

    def call_tool(self, server_id: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke tool on specified server with optional human-in-the-loop approval gate."""
        if self.consent_callback is not None:
            approved = self.consent_callback(server_id, tool_name, arguments)
            if not approved:
                return {
                    "content": [{"type": "text", "text": "Operation canceled by user consent policy."}],
                    "isError": True
                }

        server = self.servers[server_id]
        req_id = self.msg_id_counter
        self.msg_id_counter += 1

        req = json.dumps({
            "jsonrpc": "2.0",
            "id": req_id,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        })

        resp_raw = server.handle_raw_message(req)
        assert resp_raw is not None
        resp = json.loads(resp_raw)

        if "error" in resp:
            raise JSONRPCError(resp["error"]["code"], resp["error"]["message"])

        return resp["result"]

    def read_resource(self, server_id: str, uri: str) -> Dict[str, Any]:
        server = self.servers[server_id]
        req_id = self.msg_id_counter
        self.msg_id_counter += 1

        req = json.dumps({
            "jsonrpc": "2.0",
            "id": req_id,
            "method": "resources/read",
            "params": {"uri": uri}
        })

        resp_raw = server.handle_raw_message(req)
        assert resp_raw is not None
        resp = json.loads(resp_raw)

        if "error" in resp:
            raise JSONRPCError(resp["error"]["code"], resp["error"]["message"])

        return resp["result"]

    def get_prompt(self, server_id: str, prompt_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        server = self.servers[server_id]
        req_id = self.msg_id_counter
        self.msg_id_counter += 1

        req = json.dumps({
            "jsonrpc": "2.0",
            "id": req_id,
            "method": "prompts/get",
            "params": {
                "name": prompt_name,
                "arguments": arguments
            }
        })

        resp_raw = server.handle_raw_message(req)
        assert resp_raw is not None
        resp = json.loads(resp_raw)

        if "error" in resp:
            raise JSONRPCError(resp["error"]["code"], resp["error"]["message"])

        return resp["result"]


def main():
    print("=== Model Context Protocol (MCP) Interactive Simulator ===")

    # Create host and two distinct servers
    host = MCPHost(name="CursorIDE", version="0.45.0")
    db_server = MCPServer(name="Postgres-MCP-Server", version="1.0.0")

    # Build second server: Filesystem server
    fs_server = MCPServer(name="Filesystem-MCP-Server", version="1.0.0")
    fs_server.register_tool(
        name="read_file",
        description="Reads plain text file from workspace.",
        input_schema={
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Path to file"}
            },
            "required": ["filepath"]
        },
        handler=lambda args: {
            "content": [{"type": "text", "text": f"Contents of {args['filepath']}:\nfn main() {{ println!(\"Hello MCP!\"); }}"}],
            "isError": False
        }
    )

    host.register_server("db", db_server)
    host.register_server("fs", fs_server)

    # Set consent approval callback
    def user_consent_gate(server_id: str, tool_name: str, args: Dict[str, Any]) -> bool:
        print(f"\n[Consent UI] Approving tool '{tool_name}' on server '{server_id}' with args: {args}")
        return True  # Auto-approve for demo

    host.set_consent_callback(user_consent_gate)

    # 1. Initialize sessions
    print("\n1. Initializing sessions with 'db' and 'fs' servers...")
    init_db_res = host.initialize_server("db")
    print(f"  ✓ DB Server Initialized: {init_db_res['serverInfo']['name']} (Capabilities: {list(init_db_res['capabilities'].keys())})")

    init_fs_res = host.initialize_server("fs")
    print(f"  ✓ FS Server Initialized: {init_fs_res['serverInfo']['name']}")

    # 2. Discover Tools
    print("\n2. Discovering tools across servers...")
    db_tools = host.list_tools("db")
    fs_tools = host.list_tools("fs")
    print(f"  - DB Server Tools: {[t['name'] for t in db_tools]}")
    print(f"  - FS Server Tools: {[t['name'] for t in fs_tools]}")

    # 3. Read Resource
    print("\n3. Reading context resource 'db://schema/users'...")
    res = host.read_resource("db", "db://schema/users")
    print(f"  - Resource Payload:\n{res['contents'][0]['text']}")

    # 4. Invoke Tool
    print("\n4. Calling tool 'execute_sql' with JSON Schema validation gate...")
    tool_res = host.call_tool("db", "execute_sql", {"query": "SELECT * FROM users;", "limit": 5})
    print(f"  - Tool Result:\n{tool_res['content'][0]['text']}")

    # 5. Get Prompt Template
    print("\n5. Retrieving prompt template 'analyze_database'...")
    prompt_res = host.get_prompt("db", "analyze_database", {"table_name": "users"})
    print(f"  - Prompt Message Turn:\n  Role: {prompt_res['messages'][0]['role']}\n  Content: {prompt_res['messages'][0]['content']['text']}")

    print("\n✓ MCP Simulation execution complete.")


if __name__ == "__main__":
    main()
