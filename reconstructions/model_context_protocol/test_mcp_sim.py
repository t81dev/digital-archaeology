#!/usr/bin/env python3
"""
Unit test suite for the Model Context Protocol (MCP) Simulator.
Verifies JSON-RPC protocol framing, initialization state enforcement, capability negotiation,
JSON Schema validation gates, resource reading, prompt fetching, and consent gates.
"""

import json
import pytest
from reconstructions.model_context_protocol.mcp_sim import MCPServer, MCPHost, JSONRPCError


def test_mcp_server_initialization_flow():
    server = MCPServer(name="TestServer", version="1.0.0")
    assert server.state == "UNCONNECTED"

    # Attempt operational method before initialization should fail with -32002
    req_list = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    resp_raw = server.handle_raw_message(req_list)
    assert resp_raw is not None
    resp = json.loads(resp_raw)
    assert "error" in resp
    assert resp["error"]["code"] == -32002

    # Perform initialize
    req_init = json.dumps({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "TestClient", "version": "1.0"}
        }
    })
    resp_raw = server.handle_raw_message(req_init)
    assert resp_raw is not None
    resp = json.loads(resp_raw)
    assert "result" in resp
    assert resp["result"]["serverInfo"]["name"] == "TestServer"
    assert server.state == "INITIALIZING"

    # Send notifications/initialized
    notif = json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"})
    res = server.handle_raw_message(notif)
    assert res is None  # Notifications carry no return response
    assert server.state == "INITIALIZED"

    # Now tools/list should succeed
    resp_raw = server.handle_raw_message(req_list)
    assert resp_raw is not None
    resp = json.loads(resp_raw)
    assert "result" in resp
    assert "tools" in resp["result"]


def test_mcp_schema_validation_gate():
    host = MCPHost()
    server = MCPServer("ValidatorServer")
    host.register_server("srv", server)
    host.initialize_server("srv")

    # Missing required parameter 'query' should raise JSONRPCError (-32602)
    with pytest.raises(JSONRPCError) as exc_info:
        host.call_tool("srv", "execute_sql", {"limit": 10})
    assert exc_info.value.code == -32602
    assert "Missing required parameter" in exc_info.value.message

    # Invalid parameter type (limit as string instead of int)
    with pytest.raises(JSONRPCError) as exc_info:
        host.call_tool("srv", "execute_sql", {"query": "SELECT 1", "limit": "ten"})
    assert exc_info.value.code == -32602
    assert "must be an integer" in exc_info.value.message

    # Valid execution
    res = host.call_tool("srv", "execute_sql", {"query": "SELECT * FROM users", "limit": 5})
    assert res["isError"] is False
    assert "Execution result" in res["content"][0]["text"]


def test_mcp_resources_and_prompts():
    host = MCPHost()
    server = MCPServer("ResourcePromptServer")
    host.register_server("srv", server)
    host.initialize_server("srv")

    # Read Resource
    res = host.read_resource("srv", "db://schema/users")
    assert res["contents"][0]["mimeType"] == "application/json"
    assert "users" in res["contents"][0]["text"]

    # Read non-existent resource
    with pytest.raises(JSONRPCError) as exc_info:
        host.read_resource("srv", "db://schema/nonexistent")
    assert exc_info.value.code == -32602

    # Get Prompt
    prompt = host.get_prompt("srv", "analyze_database", {"table_name": "orders"})
    assert "orders" in prompt["messages"][0]["content"]["text"]


def test_mcp_user_consent_gate():
    host = MCPHost()
    server = MCPServer("ConsentServer")
    host.register_server("srv", server)
    host.initialize_server("srv")

    # Consent gate that rejects every tool call
    def reject_all_consent(server_id, tool_name, args):
        return False

    host.set_consent_callback(reject_all_consent)

    res = host.call_tool("srv", "execute_sql", {"query": "SELECT * FROM users"})
    assert res["isError"] is True
    assert "canceled by user consent" in res["content"][0]["text"]
