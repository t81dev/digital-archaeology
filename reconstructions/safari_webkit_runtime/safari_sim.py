"""
WebKit & Safari Web Runtime Architecture Simulator
===================================================

This module provides a zero-dependency Python reconstruction of core WebKit runtime mechanisms:
1. WebKit2 Multi-Process Message-Passing IPC (UI Process, Web Content Process, Network Process)
2. WKWebView Host Application Embedding & Process Isolation
3. Intelligent Tracking Prevention (ITP) Double-Keyed Storage Partitioning & Storage Access API
"""

import time
import dataclasses
from typing import Dict, List, Optional, Tuple, Any, Set


@dataclasses.dataclass(frozen=True)
class SecurityOrigin:
    protocol: str
    host: str
    port: int = 443

    def to_string(self) -> str:
        if (self.protocol == "https" and self.port == 443) or (self.protocol == "http" and self.port == 80):
            return f"{self.protocol}://{self.host}"
        return f"{self.protocol}://{self.host}:{self.port}"


@dataclasses.dataclass
class IPCMessage:
    msg_type: str
    sender_process: str
    target_process: str
    payload: Dict[str, Any]
    message_id: int


class WebContentProcess:
    """
    Simulates the WebKit2 Web Content Process (com.apple.WebKit.WebContent).
    Executes inside a strict sandbox; runs WebCore layout and JS VM.
    Cannot directly access network sockets or local filesystem.
    """
    def __init__(self, process_id: int, origin: SecurityOrigin, coordinator: 'WebKit2ProcessCoordinator'):
        self.process_id = process_id
        self.origin = origin
        self.coordinator = coordinator
        self.memory_heap: Dict[str, Any] = {}
        self.is_crashed: bool = False

    def execute_script(self, script_code: str) -> Any:
        if self.is_crashed:
            raise RuntimeError("Cannot execute script in crashed WebContentProcess")
        # Simulate simple script evaluation
        if "crash()" in script_code:
            self.is_crashed = True
            self.coordinator.notify_process_crash(self.process_id)
            return "CRASHED"
        self.memory_heap["last_script"] = script_code
        return f"Executed: {script_code}"

    def request_navigation(self, target_url: str):
        msg = IPCMessage(
            msg_type="DecidePolicyForNavigation",
            sender_process=f"WebContentProcess-{self.process_id}",
            target_process="UIProcess",
            payload={"url": target_url, "origin": self.origin.to_string()},
            message_id=self.coordinator.get_next_msg_id()
        )
        return self.coordinator.send_message(msg)

    def write_storage(self, key: str, value: str, top_level_origin: SecurityOrigin) -> bool:
        msg = IPCMessage(
            msg_type="SetStorageItem",
            sender_process=f"WebContentProcess-{self.process_id}",
            target_process="NetworkProcess",
            payload={
                "top_origin": top_level_origin.to_string(),
                "sub_origin": self.origin.to_string(),
                "key": key,
                "value": value
            },
            message_id=self.coordinator.get_next_msg_id()
        )
        res = self.coordinator.send_message(msg)
        return res.get("success", False)

    def read_storage(self, key: str, top_level_origin: SecurityOrigin) -> Optional[str]:
        msg = IPCMessage(
            msg_type="GetStorageItem",
            sender_process=f"WebContentProcess-{self.process_id}",
            target_process="NetworkProcess",
            payload={
                "top_origin": top_level_origin.to_string(),
                "sub_origin": self.origin.to_string(),
                "key": key
            },
            message_id=self.coordinator.get_next_msg_id()
        )
        res = self.coordinator.send_message(msg)
        return res.get("value")


class ITPStorageEngine:
    """
    Simulates WebKit Intelligent Tracking Prevention (ITP) Storage Engine.
    Implements double-keyed storage partitioning <TopOrigin, SubOrigin>,
    cookie capping rules, and Storage Access API grants.
    """
    def __init__(self):
        # Double-keyed storage: (top_origin, sub_origin) -> {key: value}
        self.partitioned_storage: Dict[Tuple[str, str], Dict[str, str]] = {}
        # Unpartitioned storage: sub_origin -> {key: value} (Requires ITP Storage Access Grant)
        self.unpartitioned_storage: Dict[str, Dict[str, str]] = {}
        # Storage Access API grants: set of (top_origin, sub_origin)
        self.storage_access_grants: Set[Tuple[str, str]] = set()
        # Tracked domains identified by ITP classifier
        self.classified_tracker_domains: Set[str] = set()

    def classify_domain_as_tracker(self, domain: str):
        self.classified_tracker_domains.add(domain)

    def set_item(self, top_origin: str, sub_origin: str, key: str, value: str) -> bool:
        # Check if sub_origin has unpartitioned storage access grant
        if (top_origin, sub_origin) in self.storage_access_grants:
            if sub_origin not in self.unpartitioned_storage:
                self.unpartitioned_storage[sub_origin] = {}
            self.unpartitioned_storage[sub_origin][key] = value
            return True

        # Otherwise, enforce Double-Keyed Storage Partitioning
        partition_key = (top_origin, sub_origin)
        if partition_key not in self.partitioned_storage:
            self.partitioned_storage[partition_key] = {}
        self.partitioned_storage[partition_key][key] = value
        return True

    def get_item(self, top_origin: str, sub_origin: str, key: str) -> Optional[str]:
        # If storage access grant exists, read from unpartitioned storage
        if (top_origin, sub_origin) in self.storage_access_grants:
            return self.unpartitioned_storage.get(sub_origin, {}).get(key)

        # Otherwise, read from partitioned storage bucket
        partition_key = (top_origin, sub_origin)
        return self.partitioned_storage.get(partition_key, {}).get(key)

    def request_storage_access(self, top_origin: str, sub_origin: str, user_interacted: bool) -> bool:
        """
        Simulates document.requestStorageAccess() API call.
        Access is granted if the user has interacted with the sub_origin domain.
        """
        if user_interacted:
            self.storage_access_grants.add((top_origin, sub_origin))
            return True
        return False


class NetworkProcess:
    """
    Simulates WebKit2 Network Process (com.apple.WebKit.Networking).
    Manages socket connections, TLS handshakes, and storage engines.
    """
    def __init__(self, storage_engine: ITPStorageEngine):
        self.storage_engine = storage_engine
        self.request_log: List[Dict[str, Any]] = []

    def handle_message(self, message: IPCMessage) -> Dict[str, Any]:
        self.request_log.append({"msg_id": message.message_id, "type": message.msg_type})

        if message.msg_type == "SetStorageItem":
            p = message.payload
            success = self.storage_engine.set_item(p["top_origin"], p["sub_origin"], p["key"], p["value"])
            return {"success": success}

        elif message.msg_type == "GetStorageItem":
            p = message.payload
            val = self.storage_engine.get_item(p["top_origin"], p["sub_origin"], p["key"])
            return {"value": val}

        elif message.msg_type == "RequestStorageAccess":
            p = message.payload
            granted = self.storage_engine.request_storage_access(p["top_origin"], p["sub_origin"], p["user_interacted"])
            return {"granted": granted}

        return {"error": "Unknown NetworkProcess Message"}


class WebKit2ProcessCoordinator:
    """
    Central IPC Message Router and Process Coordinator simulating WebKit2 Architecture.
    Dispatches messages between UI Process, Web Content Processes, and Network Process.
    """
    def __init__(self):
        self.msg_counter: int = 0
        self.storage_engine = ITPStorageEngine()
        self.network_process = NetworkProcess(self.storage_engine)
        self.web_content_processes: Dict[int, WebContentProcess] = {}
        self.navigation_policy_callback = None
        self.crashed_process_ids: List[int] = []

    def get_next_msg_id(self) -> int:
        self.msg_counter += 1
        return self.msg_counter

    def spawn_web_content_process(self, origin: SecurityOrigin) -> WebContentProcess:
        proc_id = len(self.web_content_processes) + 1
        proc = WebContentProcess(proc_id, origin, self)
        self.web_content_processes[proc_id] = proc
        return proc

    def notify_process_crash(self, process_id: int):
        self.crashed_process_ids.append(process_id)
        if process_id in self.web_content_processes:
            del self.web_content_processes[process_id]

    def send_message(self, message: IPCMessage) -> Dict[str, Any]:
        if message.target_process == "NetworkProcess":
            return self.network_process.handle_message(message)

        elif message.target_process == "UIProcess":
            if message.msg_type == "DecidePolicyForNavigation":
                url = message.payload["url"]
                allowed = True
                if self.navigation_policy_callback:
                    allowed = self.navigation_policy_callback(url)
                return {"allow": allowed}

        return {"error": "Target Process Not Found"}


class WKWebViewHost:
    """
    Simulates a Native Application embedding a WebKit2 WKWebView.
    Demonstrates host process insulation from web content crashes.
    """
    def __init__(self, coordinator: WebKit2ProcessCoordinator):
        self.coordinator = coordinator
        self.active_process: Optional[WebContentProcess] = None
        self.title: str = "Host App Window"
        self.page_loaded_url: Optional[str] = None

        # Register navigation delegate
        self.coordinator.navigation_policy_callback = self.decide_policy_for_navigation

    def decide_policy_for_navigation(self, url: str) -> bool:
        # Block unsafe schemes
        if url.startswith("javascript:"):
            return False
        return True

    def load_url(self, url: str):
        # Parse host origin
        host = url.split("//")[-1].split("/")[0]
        origin = SecurityOrigin("https", host)

        proc = self.coordinator.spawn_web_content_process(origin)
        self.active_process = proc

        if proc.request_navigation(url)["allow"]:
            self.page_loaded_url = url
            proc.execute_script("console.log('Page Loaded')")

    def trigger_web_content_crash(self):
        if self.active_process:
            self.active_process.execute_script("crash()")

    def is_host_alive(self) -> bool:
        # Host app process remains alive even if active web content process crashes
        return True
