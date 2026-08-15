"""
Netscape Browser Runtime & Network Client Simulator.

A zero-dependency Python reconstruction modeling Netscape's core computational abstractions:
1. DOM Event-Driven JS Host Environment & Same-Origin Policy (SOP).
2. NPAPI C-ABI Plugin Dispatcher (NPP_ / NPN_ Jump Tables).
3. HTTP Cookie Session State Management & Domain/Path Scoping.
4. SSL/TLS Certificate Trust Evaluation & Security UX Status.
"""

import time
import re
from typing import Dict, List, Optional, Tuple, Any, Callable


# ============================================================================
# 1. HTTP Cookie Session State Engine
# ============================================================================

class CookieRecord:
    """Represents a Netscape-style HTTP Cookie record."""
    def __init__(
        self,
        name: str,
        value: str,
        domain: str,
        path: str = "/",
        expires_timestamp: Optional[float] = None,
        secure: bool = False
    ):
        self.name = name
        self.value = value
        self.domain = domain.lower().lstrip(".")
        self.path = path if path else "/"
        self.expires_timestamp = expires_timestamp
        self.secure = secure

    def is_expired(self, current_time: Optional[float] = None) -> bool:
        if self.expires_timestamp is None:
            return False
        now = current_time if current_time is not None else time.time()
        return now > self.expires_timestamp

    def matches_request(self, scheme: str, host: str, path: str, current_time: Optional[float] = None) -> bool:
        if self.is_expired(current_time):
            return False

        if self.secure and scheme.lower() != "https":
            return False

        req_host = host.lower()
        # Domain matching (domain tail match)
        if not (req_host == self.domain or req_host.endswith("." + self.domain)):
            return False

        # Path matching
        if not path.startswith(self.path):
            return False

        return True


class CookieEngine:
    """Netscape HTTP Cookie Store & Request Header Generator."""
    def __init__(self):
        self.cookies: List[CookieRecord] = []

    def parse_set_cookie(self, set_cookie_str: str, request_host: str, request_path: str = "/") -> Optional[CookieRecord]:
        """Parses a Set-Cookie header string and stores the cookie record."""
        parts = [p.strip() for p in set_cookie_str.split(";")]
        if not parts or "=" not in parts[0]:
            return None

        kv_part = parts[0]
        name, value = kv_part.split("=", 1)
        name = name.strip()
        value = value.strip()

        domain = request_host
        path = request_path
        expires_timestamp = None
        secure = False

        for attr in parts[1:]:
            if "=" in attr:
                attr_name, attr_val = attr.split("=", 1)
                attr_name = attr_name.strip().lower()
                attr_val = attr_val.strip()
                if attr_name == "domain":
                    domain = attr_val.lstrip(".")
                elif attr_name == "path":
                    path = attr_val
                elif attr_name == "expires":
                    # Simple numerical timestamp or delta offset simulation
                    try:
                        expires_timestamp = float(attr_val)
                    except ValueError:
                        expires_timestamp = time.time() + 86400  # Default +24h if string
            else:
                attr_name = attr.strip().lower()
                if attr_name == "secure":
                    secure = True

        record = CookieRecord(
            name=name,
            value=value,
            domain=domain,
            path=path,
            expires_timestamp=expires_timestamp,
            secure=secure
        )
        # Overwrite existing matching cookie or append
        self.cookies = [
            c for c in self.cookies
            if not (c.name == record.name and c.domain == record.domain and c.path == record.path)
        ]
        self.cookies.append(record)
        return record

    def get_cookie_header_for_request(self, url: str, current_time: Optional[float] = None) -> str:
        """Generates the 'Cookie: name=val; name2=val2' request header for a given URL."""
        # Parse URL scheme, host, path
        match = re.match(r'^(https?)://([^/:]+)(?::\d+)?(/.*)?$', url, re.IGNORECASE)
        if not match:
            return ""

        scheme = match.group(1).lower()
        host = match.group(2).lower()
        path = match.group(3) if match.group(3) else "/"

        matching_cookies = [
            c for c in self.cookies
            if c.matches_request(scheme, host, path, current_time)
        ]

        if not matching_cookies:
            return ""

        cookie_pairs = [f"{c.name}={c.value}" for c in matching_cookies]
        return "Cookie: " + "; ".join(cookie_pairs)


# ============================================================================
# 2. SSL/TLS Certificate & Trust Evaluator
# ============================================================================

class X509Certificate:
    """Simulated X.509 Digital Certificate."""
    def __init__(
        self,
        domain_pattern: str,
        issuer: str,
        public_key_rsa: str,
        valid_until_timestamp: float,
        signature_valid: bool = True
    ):
        self.domain_pattern = domain_pattern.lower()
        self.issuer = issuer
        self.public_key_rsa = public_key_rsa
        self.valid_until_timestamp = valid_until_timestamp
        self.signature_valid = signature_valid

    def matches_hostname(self, hostname: str) -> bool:
        host = hostname.lower()
        if self.domain_pattern.startswith("*."):
            suffix = self.domain_pattern[2:]
            return host == suffix or host.endswith("." + suffix)
        return host == self.domain_pattern


class SSLTrustEvaluator:
    """Evaluates SSL 3.0 Handshake, Certificate Validation, and Security UX."""
    def __init__(self):
        self.trusted_root_cas = {"VeriSign Root CA", "RSA Data Security CA", "Thawte Root CA"}

    def perform_handshake(
        self,
        target_url: str,
        cert: X509Certificate,
        current_time: Optional[float] = None
    ) -> Dict[str, Any]:
        now = current_time if current_time is not None else time.time()

        match = re.match(r'^(https?)://([^/:]+)', target_url, re.IGNORECASE)
        if not match:
            return {"status": "INVALID_URL", "secure": False, "lock_icon": "🔓"}

        scheme = match.group(1).lower()
        hostname = match.group(2).lower()

        if scheme != "https":
            return {"status": "PLAINTEXT_HTTP", "secure": False, "lock_icon": "🔓"}

        # Check Root CA Trust
        if cert.issuer not in self.trusted_root_cas:
            return {
                "status": "UNTRUSTED_ISSUER",
                "secure": False,
                "lock_icon": "🔓",
                "warning": f"Certificate issuer '{cert.issuer}' is not in trusted root CA store!"
            }

        # Check Signature Integrity
        if not cert.signature_valid:
            return {
                "status": "BAD_SIGNATURE",
                "secure": False,
                "lock_icon": "🔓",
                "warning": "Certificate signature validation failed!"
            }

        # Check Expiration
        if now > cert.valid_until_timestamp:
            return {
                "status": "EXPIRED_CERTIFICATE",
                "secure": False,
                "lock_icon": "🔓",
                "warning": "Certificate has expired!"
            }

        # Check Hostname Match
        if not cert.matches_hostname(hostname):
            return {
                "status": "HOSTNAME_MISMATCH",
                "secure": False,
                "lock_icon": "🔓",
                "warning": f"Certificate domain '{cert.domain_pattern}' does not match host '{hostname}'!"
            }

        # Handshake Successful
        return {
            "status": "HANDSHAKE_SUCCESSFUL",
            "secure": True,
            "lock_icon": "🔒",
            "cipher_suite": "SSL_RSA_WITH_RC4_128_MD5",
            "issuer": cert.issuer,
            "session_key": "SymmetricKey_RC4_128_" + cert.public_key_rsa[:8]
        }


# ============================================================================
# 3. NPAPI C-ABI Plugin Dispatcher
# ============================================================================

class NPAPINetscapeFuncs:
    """Host Netscape Functions (NPN_) provided to plugins."""
    def __init__(self, host_context: Any):
        self.host_context = host_context
        self.allocated_blocks: List[int] = []

    def NPN_GetURL(self, instance_id: str, url: str) -> str:
        """Requests browser to fetch a URL on behalf of the plugin."""
        return f"HOST_FETCHING[{url}]_FOR_INSTANCE[{instance_id}]"

    def NPN_MemAlloc(self, size: int) -> int:
        """Allocates memory block inside host process space."""
        handle = id(object()) + len(self.allocated_blocks)
        self.allocated_blocks.append(handle)
        return handle

    def NPN_UserAgent(self) -> str:
        return "Mozilla/4.0 (compatible; Netscape 4.78; Windows NT 4.0)"


class NPAPIPluginFuncs:
    """Plugin Exported Functions (NPP_) called by Netscape Host."""
    def __init__(self, mime_type: str, plugin_name: str):
        self.mime_type = mime_type
        self.plugin_name = plugin_name
        self.active_instances: Dict[str, Dict[str, Any]] = {}

    def NPP_New(self, instance_id: str, mode: str) -> bool:
        """Instantiates a new plugin instance for an <embed> element."""
        self.active_instances[instance_id] = {
            "mode": mode,
            "window_handle": None,
            "data_stream": []
        }
        return True

    def NPP_SetWindow(self, instance_id: str, window_handle: str, width: int, height: int) -> bool:
        """Passes native OS window drawing surface handle to plugin."""
        if instance_id in self.active_instances:
            self.active_instances[instance_id]["window_handle"] = window_handle
            self.active_instances[instance_id]["dimensions"] = (width, height)
            return True
        return False

    def NPP_Write(self, instance_id: str, data_bytes: bytes) -> int:
        """Streams network data bytes into the plugin instance."""
        if instance_id in self.active_instances:
            self.active_instances[instance_id]["data_stream"].append(data_bytes)
            return len(data_bytes)
        return 0

    def NPP_Destroy(self, instance_id: str) -> bool:
        """Destroys plugin instance upon page navigation."""
        if instance_id in self.active_instances:
            del self.active_instances[instance_id]
            return True
        return False


class NPAPIDispatcher:
    """Host Dispatcher managing NPAPI Shared Libraries and Jump Tables."""
    def __init__(self):
        self.registered_plugins: Dict[str, NPAPIPluginFuncs] = {}
        self.npn_funcs = NPAPINetscapeFuncs(self)

    def register_plugin(self, plugin: NPAPIPluginFuncs):
        self.registered_plugins[plugin.mime_type] = plugin

    def embed_element(self, mime_type: str, instance_id: str, window_handle: str, width: int, height: int) -> Optional[NPAPIPluginFuncs]:
        if mime_type not in self.registered_plugins:
            return None

        plugin = self.registered_plugins[mime_type]
        success = plugin.NPP_New(instance_id, mode="EMBED")
        if success:
            plugin.NPP_SetWindow(instance_id, window_handle, width, height)
            return plugin
        return None


# ============================================================================
# 4. DOM Host Environment, Event Dispatcher & Same-Origin Policy (SOP)
# ============================================================================

class Origin:
    """Netscape Same-Origin Tuple <Scheme, Host, Port>."""
    def __init__(self, scheme: str, host: str, port: int):
        self.scheme = scheme.lower()
        self.host = host.lower()
        self.port = port

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Origin):
            return False
        return self.scheme == other.scheme and self.host == other.host and self.port == other.port

    def __str__(self) -> str:
        return f"{self.scheme}://{self.host}:{self.port}"


class DOMElement:
    """Simplified DOM Level 0 Element."""
    def __init__(self, tag: str, name: str = "", attributes: Optional[Dict[str, str]] = None):
        self.tag = tag
        self.name = name
        self.attributes = attributes if attributes else {}
        self.value: str = self.attributes.get("value", "")
        self.event_handlers: Dict[str, Callable[..., bool]] = {}

    def attach_event_listener(self, event_type: str, handler: Callable[..., bool]):
        self.event_handlers[event_type.lower()] = handler

    def dispatch_event(self, event_type: str, *args, **kwargs) -> bool:
        handler = self.event_handlers.get(event_type.lower())
        if handler:
            return handler(*args, **kwargs)
        return True  # Default proceed


class DOMDocument:
    """DOM Level 0 Document Representation."""
    def __init__(self, origin: Origin, url: str):
        self.origin = origin
        self.url = url
        self.forms: List[DOMElement] = []
        self.elements: Dict[str, DOMElement] = {}
        self.cookie_store: CookieEngine = CookieEngine()

    def add_form(self, name: str) -> DOMElement:
        form = DOMElement(tag="form", name=name)
        self.forms.append(form)
        self.elements[name] = form
        return form


class NetscapeDOMHost:
    """Browser Window & JavaScript Host Execution Engine."""
    def __init__(self):
        self.documents: Dict[str, DOMDocument] = {}
        self.npapi_dispatcher = NPAPIDispatcher()
        self.ssl_evaluator = SSLTrustEvaluator()

    def parse_origin(self, url: str) -> Origin:
        match = re.match(r'^(https?)://([^/:]+)(?::(\d+))?', url, re.IGNORECASE)
        if not match:
            return Origin("http", "localhost", 80)
        scheme = match.group(1).lower()
        host = match.group(2).lower()
        default_port = 443 if scheme == "https" else 80
        port = int(match.group(3)) if match.group(3) else default_port
        return Origin(scheme, host, port)

    def create_document(self, window_name: str, url: str) -> DOMDocument:
        origin = self.parse_origin(url)
        doc = DOMDocument(origin, url)
        self.documents[window_name] = doc
        return doc

    def check_same_origin_access(self, source_window: str, target_window: str) -> bool:
        """Enforces Netscape Navigator 2.02 Same-Origin Policy (SOP)."""
        if source_window not in self.documents or target_window not in self.documents:
            return False

        src_origin = self.documents[source_window].origin
        tgt_origin = self.documents[target_window].origin
        return src_origin == tgt_origin

    def execute_script_cross_frame_access(
        self,
        source_window: str,
        target_window: str,
        property_name: str
    ) -> Tuple[bool, Any]:
        """Attempts to read target window property subject to Same-Origin Policy."""
        if not self.check_same_origin_access(source_window, target_window):
            return False, "SecurityException: Blocked cross-origin frame access!"

        tgt_doc = self.documents[target_window]
        if property_name == "url":
            return True, tgt_doc.url
        elif property_name == "forms":
            return True, tgt_doc.forms
        elif property_name in tgt_doc.elements:
            return True, tgt_doc.elements[property_name].value
        return False, "PropertyNotFound"
