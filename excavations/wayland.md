# Wayland: Compositor-Centered Display Protocol & Surface Architecture

> *An archaeological excavation of Wayland as a display protocol and compositor architecture lineage, investigating how replacing the networked, client-drawable X Window System with an asynchronous, surface-oriented protocol re-centered display authority in the compositor, transformed buffer presentation and input security boundaries, and redefined Linux graphical session architecture for a GPU-local era.*

---

## Summary

The Wayland computational lineage is frequently analyzed through simplified desktop-user narratives of "X11 replacement," multi-year distribution migration delays, or driver-path controversies. In digital archaeology, however, **Wayland represents a fundamental structural redefinition of display server architecture**: the collapse of the decoupled display server and compositing window manager into a single authoritative entity—the compositor—and the replacement of server-rendered graphics primitives with client-allocated, surface-committed shared memory and GPU buffers (`DMA-BUF`).

By discarding X11’s legacy core drawing protocol, central font rendering, global input grabs, and ambient cross-client window peeking, Wayland established an asynchronous, object-oriented wire protocol over Unix sockets. Wayland’s core architecture operates on a minimal set of primitives: interface registries, surfaces (`wl_surface`), buffers (`wl_buffer`), outputs (`wl_output`), and seats (`wl_seat`). Desktop-specific window management semantics (such as title bars, window positioning, and surface stacking) were explicitly excluded from the core protocol and delegated to extension families (`xdg-shell`, `wlr-protocols`). Supported by the **XWayland** compatibility bridge for legacy applications and adopted across major desktop compositors (Mutter, KWin, wlroots, Gamescope), Wayland shifted the Linux desktop from an open, ambiently authoritative drawing canvas to a compositor-mediated capability boundary.

---

## Historical Context

The Wayland lineage originated in 2008 when Kristian Høgsberg, a developer working on the X.Org Server and the Compiz compositing window manager, recognized an irreconcilable architectural mismatch in the modern Linux graphics stack.

```
                       The X11 Compositing Indirection Bottleneck

  [ Client App ] ──► ( Render via OpenGL/Cairo ) ──► [ Local Memory / GPU ]
        │                                                    │
        ▼ ( X11 Core Protocol Drawing / Render Requests )     │ ( Send Pixmap Handle )
  [ Xorg Server ] ◄──────────────────────────────────────────┘
        │
        ├─► Intercepted by Composite Extension
        │
        ▼ ( Redirect to Offscreen Pixmap )
  [ Compositing Window Manager ] ──► ( Read Back Frame, Apply Shadow/3D Trans )
        │
        ▼ ( Draw Composite Output Back to Xorg Server )
  [ Hardware Screen / Framebuffer ]
```

In the classic X Window System (X11) architecture, designed in the mid-1980s for networked terminals, the X Server was the authoritative display master. The server owned the screen, managed input devices, rendered fonts, executed 2D drawing requests (lines, arcs, polygons), and maintained window hierarchies. However, by the mid-2000s, three hardware and software shifts had rendered this model inefficient and redundant:
1. **Direct Client Rendering**: Applications no longer asked the X Server to draw 2D primitives. Libraries like GTK, Qt, Cairo, and OpenGL rendered complete pixel frames directly inside client address spaces or GPU vRAM using hardware acceleration (DRI2/DRI3).
2. **Universal Desktop Compositing**: Rather than allowing windows to draw directly to the screen's front buffer (causing tearing and artifacts during dragging), compositing window managers (Compiz, Mutter, KWin) redirected window drawing to offscreen pixmaps, composite all windows into a single scene graph, and presented the final composited frame to the display.
3. **Kernel Graphics Drivers (DRM/KMS/evdev)**: Kernel-level Direct Rendering Manager (DRM), Kernel Mode Setting (KMS), and `evdev` input subsystems moved display mode switching, memory management (GEM/TTM), and hardware device detection directly into the [Linux](linux.md) kernel, rendering the X Server's user-space hardware drivers obsolete.

Under this modern pipeline, the X Server became an unnecessary, high-latency middleman: clients rendered offscreen, sent pixmap handles to Xorg, Xorg notified the compositor, the compositor fetched the pixmap handles from Xorg, composite the scene using OpenGL, and sent the result back to Xorg to display. Høgsberg realized that every frame travelled through the X Server twice, and that the compositing window manager was already doing the real work of a display server. Wayland was designed to eliminate the middleman by turning the compositor itself into the display server, establishing a direct connection between client surface buffers and kernel KMS framebuffers.

---

## Archaeological Scope

To analyze Wayland as an architectural lineage, we decompose the substrate into ten distinct computational layers:

```
                      Wayland System Architecture Topology

 ┌────────────────────────────────────────────────────────────────────────┐
 │ Application / Toolkit Layer (GTK, Qt, SDL, Electron, Native Apps)      │
 └───────────────────┬────────────────────────────────┬───────────────────┘
                     │                                │
                     ▼ (Native Wayland Wire Protocol) │ (X11 Protocol Wire)
 ┌─────────────────────────────────────────┐          │
 │ Core Wayland IPC Protocol (Unix Socket) │          ▼
 │ (wl_surface, wl_buffer, wl_seat, etc.) │ ┌─────────────────────────────┐
 └───────────────────┬─────────────────────┘ │ XWayland Compatibility     │
                     │                       │ Bridge (Nested X Server)     │
                     │                       └──────────────┬──────────────┘
                     ▼                                      │
 ┌──────────────────────────────────────────────────────────┴─────────────┐
 │ Compositor / Display Server Layer (Mutter, KWin, wlroots, Gamescope)   │
 │ - Surface Lifecycle & Commit Engine                                    │
 │ - Output Scene Graph & Composition (EGL/GLES)                         │
 │ - Seat Input Arbitration & Focus Routing                               │
 └───────────────────┬────────────────────────────────────────────────────┘
                     │
                     ▼ (Direct Buffer Sharing / Frame Submission)
 ┌────────────────────────────────────────────────────────────────────────┐
 │ Linux Kernel Subsystems (DRM / KMS, DMA-BUF, evdev, Wayland Socket)    │
 └────────────────────────────────────────────────────────────────────────┘
```

### 1. Protocol Core & Wire IPC
* **Unix Domain Socket IPC**: Asynchronous, stream-oriented binary IPC protocol framing typed requests (client to compositor) and events (compositor to client).
* **Object Registry & Interface Binding**: Dynamic object identification (`wl_registry`), runtime capability discovery, and numerical interface version negotiation.
* **Core Object Primitives**: `wl_display` (core connection handle), `wl_compositor` (surface allocation factory), `wl_surface` (rectangular visual region), `wl_buffer` (pixel storage handle), `wl_output` (physical monitor representation), and `wl_seat` (logical input group).

### 2. Compositor Architectural Model
* **Unified Display Authority**: The compositor functions directly as the display server, controlling DRM/KMS mode setting and managing hardware output planes.
* **Event Loop & Frame Scheduling**: Frame rendering driven by compositor-emitted callbacks (`wl_surface.frame`), synchronizing client rendering loops with physical display VSync.

### 3. Buffer Sharing & Presentation Pipeline
* **Shared Memory (`wl_shm`)**: POSIX shared memory file descriptor exchange (`mmap`) for software-rendered client buffers.
* **Direct Memory Access Buffers (`DMA-BUF`)**: Linux kernel zero-copy memory handles passed via socket file descriptors (`linux-dmabuf` protocol extension), permitting GPU-to-GPU and GPU-to-display engine buffer transfers without CPU copying.
* **Attach/Commit Surface Lifecycle**: Atomic transaction workflow (`attach` buffer $\rightarrow$ set region/damage $\rightarrow$ `commit` surface state) preventing partial or torn frame rendering.

### 4. Input & Seat Model
* **`wl_seat` Abstraction**: Groups logical input capabilities (pointer, keyboard, touch, tablet) into a unified input seat.
* **Focus & Event Routing**: Compositor-enforced input focus based on surface geometry and window stacking; elimination of global input sniffing or unprivileged event injection.

### 5. Security & Isolation Boundaries
* **Reduced Ambient Authority**: Surfaces cannot inspect, capture, or inject input into sibling surfaces owned by other clients.
* **Privileged Extension Gating**: Screen capture, global keybindings, and window positioning restricted to authorized desktop components or user-mediated portal proxies (`xdg-desktop-portal`).

### 6. Extension Ecosystem & Desktop Shell
* **`xdg-shell` Protocol**: Standardized extension defining desktop window semantics (`xdg_wm_base`, `xdg_surface`, `xdg_toplevel`, `xdg_popup`).
* **Compositor Protocol Families**: Vendor-neutral extension repos (`wayland-protocols`), `wlr-protocols` (wlroots ecosystem), and compositor-private extensions (Mutter, KWin, Weston).

### 7. Compatibility Stack (XWayland)
* **XWayland Server**: A lightweight X.Org Server binary running as an unprivileged Wayland client, translating X11 protocol calls into Wayland surface commits and buffer submissions.
* **Rootless Integration**: X11 client windows seamless integration alongside native Wayland surfaces within the compositor’s unified desktop scene graph.

### 8. Compositor Ecosystem as Architecture Carriers
* **Weston**: Reference compositor demonstrating protocol correctness and minimal DRM/KMS backend implementation.
* **Desktop Compositors**: GNOME Mutter and KDE KWin integrating shell semantics, complex window management, and hardware backends.
* **Modular Infrastructure**: `wlroots` providing reusable, headless C library components for compositors (Sway, Hyprland, River).
* **Specialized Compositors**: Gamescope providing isolated, low-latency gaming surfaces with resolution upscaling and frame pacing.

### 9. Toolkit & Application Adaptation
* **Native Toolkit Backends**: Wayland backends inside GTK (GDK Wayland), Qt (Qt Wayland), SDL2/SDL3, and Chromium/Electron (Ozone platform).
* **Decoration Architectural Debates**: Server-Side Decoration (SSD) versus Client-Side Decoration (CSD) policy split between desktop ecosystems.

### 10. Broader Linux Graphics Ecology
* Integration across Mesa GLES/EGL graphics drivers, `libinput` input device translation, systemd session management, pipewire multimedia streaming, and kernel graphics drivers.

---

## Historical Lineage

The evolution of Wayland is structured by several major transitions that transformed a radical experimental protocol into the default display architecture of modern Linux distributions:

```
                    Wayland Architectural Progression

 2008   Wayland Project Unveiled (Kristian Høgsberg, Weston prototype)
             │
             ▼
 2012   Wayland Core Protocol 1.0 (Stable IPC, wl_surface, wl_shm, wl_seat)
             │
             ▼
 2014   XWayland Merged into X.Org Server (Rootless X11 application compatibility)
             │
             ▼
 2017   xdg-shell Protocol Version 1.0 (Stable desktop window management semantics)
             │
             ▼
 2018   wlroots Library Ecosystem Emergence (Modular Wayland compositor building blocks)
             │
             ▼
 2021   Fedora & Ubuntu Default Sessions Switch to Wayland (Mutter/KWin stabilization)
             │
             ▼
 2022   Gamescope & Steam Deck Launch (Wayland micro-compositor for handheld gaming)
             │
             ▼
 2024+  Advanced Protocol Expansion (HDR, Color Management, Explicit Synchronization)
```

For every major transition, the exact architectural mechanisms shifted:

| Transition | What Changed? | What Survived? | Compatibility Layer | Deliberately Abandoned | Driving Constraint |
|:---|:---|:---|:---|:---|:---|
| **X11 Core $\rightarrow$ Wayland Core** | Merged display server and compositor; replaced server drawing commands with surface buffer commits. | Unix domain socket IPC, client rendering libraries (Mesa, Cairo). | None initially; direct native Wayland client requirement. | Server-side 2D drawing primitives, core fonts, X11 protocol extensions. | Severe latency and double-buffering indirection of composited X11. |
| **Native Native $\rightarrow$ XWayland Bridge** | Added rootless embedded Xorg server acting as a Wayland client. | Entire legacy X11 binary app ecosystem (GIMP, Steam, games). | **XWayland**: Translates X11 draw calls to Wayland buffers & `wl_surface` commits. | Expectation that all legacy apps be rewritten for Wayland natively before migration. | Slow migration of legacy proprietary software and game engines. |
| **Ad-Hoc Shell $\rightarrow$ `xdg-shell` Extension** | Separated core surface geometry from desktop window behaviors (maximized, popup, minimize). | Core protocol primitives (`wl_surface`, `wl_buffer`). | Legacy compositor-specific shell interfaces (`wl_shell`). | Single monolithic protocol specifying both display and desktop UI semantics. | Divergence of window management behaviors across GTK and Qt compositors. |
| **EGLStreams $\rightarrow$ DRM KMS / GBM Consensus** | Unified GPU buffer allocation under generic buffer management (`GBM`) and `DMA-BUF`. | EGL/OpenGL ES client rendering APIs. | Temporary proprietary EGLStreams patches inside Mutter and KWin. | Proprietary driver vendor-specific buffer sharing interfaces. | Driver-path fragmentation and broken compositing on NVIDIA hardware. |
| **Direct Hardware $\rightarrow$ Portal Privileged Proxy** | Moved global desktop actions (screen capture, hotkeys, input injection) to D-Bus Portals. | Native Wayland surface rendering and seat focus. | **`xdg-desktop-portal`**: User-prompted D-Bus authorization boundary. | Unprivileged ambient socket access to screen contents and global keystrokes. | Security vulnerabilities of cross-client keylogging and window peeking. |

---

## Protocol Object Model & Wire IPC

The Wayland protocol is an asynchronous, typed, object-oriented wire protocol executing over a standard Unix domain socket.

### 1. Wire Framing and Message Protocol
All communications between client and compositor consist of 32-bit aligned binary messages. Each message on the wire begins with a mandatory 8-byte header:

```
                       Wayland Wire Message Header Format

  0                   1                   2                   3
  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                          Object ID                            |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |         Opcode / Event ID     |         Message Size          |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                        Arguments ...                          |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

- **Object ID** (32-bit uint): The numeric identifier of the target protocol object receiving the request or firing the event. ID `1` is permanently reserved for the singleton `wl_display` object.
- **Opcode** (16-bit uint): The numeric index of the method/request or event being invoked on the interface.
- **Message Size** (16-bit uint): Total size of the message frame in bytes, including the header and aligned arguments.
- **Arguments**: Strongly typed payload serialized according to XML protocol interface definitions:
  - `i` / `u`: 32-bit signed / unsigned integer.
  - `f`: 24.8 fixed-point number.
  - `s`: UTF-8 string prefixed by length.
  - `o` / `n`: Existing object ID / New object ID created by the call.
  - `a`: Raw byte array prefixed by length.
  - `h`: File descriptor passed via socket out-of-band control messages (`SCM_RIGHTS`).

### 2. Core Protocol Object Primitives
The core `wayland.xml` specification defines a tight hierarchy of computational objects:

```
                        Wayland Core Interface Hierarchy

                                   ┌──────────────┐
                                   │  wl_display  │ (ID 1: Connection Root)
                                   └──────┬───────┘
                                          │
                   ┌──────────────────────┴──────────────────────┐
                   ▼                                             ▼
          ┌─────────────────┐                           ┌─────────────────┐
          │   wl_registry   │                           │   wl_shm        │
          └────────┬────────┘                           └────────┬────────┘
                   │                                             │
      ┌────────────┼────────────┐                                ▼
      ▼            ▼            ▼                       ┌─────────────────┐
┌───────────┐ ┌───────────┐ ┌───────────┐               │   wl_shm_pool   │
│wl_compos- │ │  wl_seat  │ │ wl_output │               └────────┬────────┘
│   itor    │ └─────┬─────┘ └───────────┘                        │
└─────┬─────┘       │                                            ▼
      │             ├───────────────┬──────────────┐    ┌─────────────────┐
      ▼             ▼               ▼              ▼    │    wl_buffer    │
┌───────────┐ ┌───────────┐   ┌───────────┐  ┌──────────┤ (Pixel Data Ref)│
│wl_surface │ │wl_pointer │   │wl_keyboard│  │ wl_touch │ └────────┬────────┘
└─────┬─────┘ └───────────┘   └───────────┘  └──────────┘          │
      │                                                            │
      └───────────────────── Attach Buffer ────────────────────────┘
```

* **`wl_display`**: The core global context handle. Manages client event queues, error reporting (`wl_display.error`), and socket flushing (`wl_display.flush`).
* **`wl_registry`**: The capability discovery mechanism. When a client binds to the registry, the compositor emits a stream of `global` events advertising available interfaces, numeric object IDs, and supported interface versions.
* **`wl_compositor`**: The surface factory interface. Used by clients to instantiate `wl_surface` objects and `wl_region` clipping boundaries.
* **`wl_surface`**: The fundamental visual building block. Represents a rectangular area on screen that receives pixel buffers (`attach`), accepts region updates (`damage`), and executes atomic updates (`commit`).
* **`wl_buffer`**: A wrapper handle providing raw pixel data to a `wl_surface`. Created either via shared memory (`wl_shm_pool`) or GPU memory handles (`zwp_linux_dmabuf_v1`).
* **`wl_output`**: Advertises physical or virtual display monitor attributes (resolution, subpixel geometry, refresh rate, scale factor, transform rotation).
* **`wl_seat`**: Represents a collection of input devices assigned to a single user. Allocates `wl_pointer`, `wl_keyboard`, and `wl_touch` interfaces on demand.

### 3. Object Creation and Interface Versioning
Wayland object creation is asynchronous and client-driven. When a request allocates a new object (e.g., `wl_compositor.create_surface`), the client allocates a local 32-bit ID from its client-assigned ID space and passes it immediately in the `n` argument. There is no synchronous round-trip blocking call asking the server "please allocate an ID."

Interface versioning follows explicit backwards-compatibility contracts:
- Every global interface advertised by `wl_registry` carries a numeric version integer.
- The client passes its desired interface version during `wl_registry.bind`. The bound version must be less than or equal to the server's advertised version.
- Requests and events added in newer versions are never emitted or accepted unless the client explicitly bound to that version.

---

## Compositor-Centered Architecture

In the Wayland architectural paradigm, **the compositor is the authoritative display server**. It does not delegate screen output, window hierarchy, or input mediation to an external supervisor daemon.

```
                   Compositor Architecture and Driver Bounds

  ┌──────────────────────────────────────────────────────────────────────┐
  │                    Wayland Compositor (Userspace)                     │
  │                                                                      │
  │  ┌──────────────────┐  ┌──────────────────┐  ┌────────────────────┐  │
  │  │ Wayland Socket   │  │ Scene Graph &    │  │ Seat Focus & Input │  │
  │  │ Wire IPC Server  │  │ Render Engine    │  │ Arbitrator         │  │
  │  └────────┬─────────┘  └────────┬─────────┘  └─────────┬──────────┘  │
  │           │                     │                      │             │
  │           ▼                     ▼                      ▼             │
  │  ┌────────────────────────────────────────────────────────────────┐  │
  │  │ Backend Hardware Drivers (EGL / GLES / GBM / libinput)          │  │
  │  └──────────────────────────────┬─────────────────────────────────┘  │
  └─────────────────────────────────┼────────────────────────────────────┘
                                    │ (Direct Device Node Control)
                                    ▼
  ┌──────────────────────────────────────────────────────────────────────┐
  │                        Linux Kernel Subsystems                       │
  │  ┌──────────────────────────┐         ┌───────────────────────────┐  │
  │  │ DRM / KMS Subsystem      │         │ evdev Subsystem           │  │
  │  │ (/dev/dri/card0)         │         │ (/dev/input/event*)       │  │
  │  └──────────────────────────┘         └───────────────────────────┘  │
  └──────────────────────────────────────────────────────────────────────┘
```

### 1. Kernel Interface Mapping (DRM/KMS & libinput)
The compositor opens Linux kernel graphics device nodes (`/dev/dri/card0`) directly using Direct Rendering Manager (DRM) and Kernel Mode Setting (KMS) APIs:
- **KMS Plane Control**: The compositor configures primary hardware planes, overlay planes, and hardware cursor planes directly via KMS ioctls (`drmModePageFlip`, `drmModeAtomicCommit`).
- **Input Hardware Access**: The compositor opens raw kernel input event nodes (`/dev/input/event*`) managed via `libinput`. `libinput` handles raw touchpad gesture processing, palm rejection, pointer acceleration curves, and keymap translation (`xkbcommon`).

### 2. Redraw Loop & VSync Synchronization
Wayland completely eliminates the tearing and asynchronous presentation artifacts characteristic of legacy X11 through its compositor-controlled frame pacing loop:

```
                      Wayland Frame Callback Lifecycle

   Client                                                      Compositor
     │                                                             │
     ├─── wl_surface.attach(buffer) ─────────────────────────────► │
     ├─── wl_surface.damage_buffer(x, y, w, h) ───────────────────► │
     ├─── callback_id = wl_surface.frame() ──────────────────────► │ (Queue Frame Callback)
     ├─── wl_surface.commit() ───────────────────────────────────► │ (State Applied Atomically)
     │                                                             │
     │                                 [ Compositor Renders Frame ]│
     │                                 [ Executes KMS Page Flip   ]│
     │                                 [ Waits for Hardware VSync ]│
     │                                                             │
     │ ◄─ wl_callback.done(timestamp) ────────────────────────────┼─ (Hardware VSync Fired)
     │                                                             │
   [ Renders NEXT Frame ]                                          │
```

1. **Client Request**: The client updates its buffer, issues a `wl_surface.frame` request to obtain a `wl_callback` object, and commits the surface.
2. **State Application**: The compositor marks the surface as dirty but does **not** force an immediate draw.
3. **Composite & Flip**: At the optimal point in the display's refresh cycle, the compositor composite all dirty surfaces into the display scene graph and submits the composited frame to KMS via an atomic page flip.
4. **VSync Event**: When the display hardware completes the page flip, the kernel emits a VSync interrupt.
5. **Frame Release**: The compositor fires the `wl_callback.done` event with the current hardware timestamp, signaling to the client that it is now safe to render its next frame.

This protocol loop guarantees that clients never render faster than the physical display can refresh, preventing frame waste and eliminating screen tearing by construction.

---

## Surface, Buffer & Presentation Path

Graphics presentation in Wayland operates on explicit separation between **pixel storage handles** (`wl_buffer`) and **visual placement abstractions** (`wl_surface`).

### 1. Dual Buffer Storage Paths: SHM vs DMA-BUF
Wayland supports two primary memory paths for passing pixel content from clients to the compositor:

```
                        Wayland Memory Buffer Architecture

 [ Software Client (CPU Rendering) ]        [ Hardware Client (GPU Rendering) ]
                 │                                           │
                 ▼                                           ▼
   ┌───────────────────────────┐               ┌───────────────────────────┐
   │ Shared Memory Pool        │               │ GPU vRAM Allocation       │
   │ (POSIX shm_open / mmap)   │               │ (Mesa / EGL / Vulkan)     │
   └─────────────┬─────────────┘               └─────────────┬─────────────┘
                 │                                           │
                 ▼ (Pass shm FD)                             ▼ (Pass DMA-BUF FD)
   ┌───────────────────────────┐               ┌───────────────────────────┐
   │ wl_shm_pool / wl_buffer   │               │ linux_dmabuf_v1           │
   └─────────────┬─────────────┘               └─────────────┬─────────────┘
                 │                                           │
                 ▼                                           ▼
   ┌───────────────────────────┐               ┌───────────────────────────┐
   │ Compositor CPU/RAM Read   │               │ Zero-Copy GPU Scanout     │
   │ (Cairo / Pixman Fallback) │               │ (KMS Direct Plane / EGL)  │
   └───────────────────────────┘               └───────────────────────────┘
```

* **Software Shared Memory (`wl_shm`)**: Intended for CPU-rendered applications. The client creates a POSIX shared memory file descriptor (`shm_open`), truncates it to the required size, maps it via `mmap`, and passes the file descriptor to the compositor via socket file descriptor passing. The compositor creates a `wl_shm_pool` and extracts individual `wl_buffer` objects referencing offsets inside the shared memory segment.
* **Direct Memory Access Buffers (`linux-dmabuf-unstable-v1`)**: Intended for hardware-accelerated GPU applications. The client allocates GPU memory via Mesa (EGL/Vulkan) and exports the underlying kernel memory allocation as a `DMA-BUF` file descriptor. The file descriptor, along with stride, offset, pixel format (DRM format codes), and modifier flags, is passed to the compositor.

### 2. Zero-Copy Scanout Bypass
When a client application (such as a full-screen video player or 3D game) occupies an entire physical monitor output, the compositor can bypass the composition step completely. Using `DMA-BUF` handles, the compositor assigns the client's buffer directly to a hardware KMS overlay or primary plane (`direct scanout`). The GPU does not composite the frame; the display controller reads pixel data directly from the client's GPU memory allocation, achieving zero-copy presentation with absolute minimum latency.

### 3. The Double-Buffered State Machine (Attach & Commit)
A `wl_surface` maintains two distinct state structures inside the compositor: **pending state** and **current state**.

```
                   wl_surface Double-Buffered State Machine

  Client Requests (attach, damage, set_scale, set_buffer_transform)
                               │
                               ▼
            ┌────────────────────────────────────┐
            │   Compositor PENDING State         │
            │   (Accumulates unapplied changes)  │
            └──────────────────┬─────────────────┘
                               │
                               │  Client Issues wl_surface.commit()
                               ▼
            ┌────────────────────────────────────┐
            │   Compositor CURRENT State         │
            │   (Atomic Swap; Passed to Renderer)│
            └────────────────────────────────────┘
```

Requests like `attach` (binding a buffer), `damage` (invalidating a region), `set_buffer_scale`, or `set_buffer_transform` modify **only** the pending state. The compositor takes no visual action when these requests arrive. Only when the client explicitly issues a `wl_surface.commit()` request does the compositor atomically swap the pending state into current state. This guarantees that complex surface reconfigurations (such as resizing a window, attaching a new buffer, and updating damage regions) occur atomically in a single frame update.

---

## Input / Seat Model

In classic X11, any client connected to the X server socket could inspect all input devices, install global keyloggers, sniff pointer coordinates across other applications, or inject synthetic events into arbitrary windows. Wayland completely re-architects input handling around **strict compositor-mediated focus isolation**.

### 1. `wl_seat` Grouping & Capability Discovery
An input seat (`wl_seat`) represents a logical grouping of input devices assigned to a user context. A seat advertises dynamic capabilities via the `wl_seat.capabilities` bitmask event:
- `POINTER` (`1`): Mouse, trackball, or touchpad pointer device present.
- `KEYBOARD` (`2`): Physical or virtual keyboard present.
- `TOUCH` (`4`): Multi-touch touchscreen surface present.

Clients bind to the seat and allocate individual device handles (`wl_seat.get_pointer`, `wl_seat.get_keyboard`, `wl_seat.get_touch`) based on advertised capabilities.

### 2. Spatial Focus & Event Routing
Input events are delivered **only** to the client surface that currently holds seat focus:
* **Pointer Events**: Pointer coordinates (`wl_pointer.enter`, `motion`, `button`, `leave`) are relative to the top-left corner of the target surface. A client has zero knowledge of the absolute pointer coordinates on the physical screen monitor.
* **Keyboard Events**: Keypress events (`wl_keyboard.key`) are dispatched exclusively to the surface that currently holds keyboard focus (determined by compositor window management policy).
* **Isolation from Non-Focused Surfaces**: An application running in the background receives zero pointer motion events, zero keystroke events, and zero touch signals while unfocused.

### 3. Elimination of Global Grabs
In X11, applications could execute `XGrabKeyboard` or `XGrabPointer` to intercept all system input globally. Wayland explicitly omits unprivileged global grabs from the core protocol. Popups, context menus, and dropdowns operate via specialized shell child surfaces (`xdg_popup`) managed by compositor focus rules rather than raw client input hijacking.

---

## Security & Isolation Boundaries

Wayland’s primary architectural departure from X11 is its **elimination of ambient cross-client authority**.

```
                        X11 vs Wayland Security Boundaries

   [ Classic X11 Open Namespace ]           [ Wayland Isolated Capability Model ]

  Client A          Client B               Client A               Client B
     │                 │                      │                      │
     ▼                 ▼                      ▼                      ▼
 ┌──────────────────────────┐           ┌──────────┐           ┌──────────┐
 │      Xorg Server         │           │Surface A │           │Surface B │
 │ - Global Window Tree     │           └────┬─────┘           └────┬─────┘
 │ - Open Input Event Sniff │                │                      │
 │ - Arbitrary Screen Peek  │                ▼                      ▼
 └──────────────────────────┘           ┌─────────────────────────────────┐
                                        │ Wayland Compositor (Isolation)  │
                                        │ - Strict Surface Separation     │
                                        │ - Mediated Portal Security      │
                                        └─────────────────────────────────┘
```

### 1. Threat Model & Ambient Authority Reduction
In X11, connecting to the X11 Unix socket granted ambient authority over the entire graphical session. Any background utility could:
- Query the global window tree and read raw pixel contents of sibling windows (screen scraping / credential spying).
- Intercept global keystrokes across all applications (keylogging).
- Synthesize pointer and keyboard events to drive other applications (unauthorized command injection).

Wayland treats the socket connection as a **capability-restricted channel**. The native Wayland protocol provides no request methods to:
1. List other clients or surfaces connected to the compositor.
2. Read pixel data from surfaces owned by other applications.
3. Inject input events into non-owned surfaces.
4. Obtain absolute desktop window coordinates.

### 2. Privileged Operations via D-Bus Desktop Portals
Because legitimate desktop workflows (screen sharing, screenshot capture, accessibility tools, global hotkeys) require capabilities beyond isolated surface rendering, Wayland delegates these privileged operations to an external authority: **`xdg-desktop-portal`**.

```
                     Screen Capture via xdg-desktop-portal

  [ Application ] ──► ( D-Bus Request ) ──► [ xdg-desktop-portal ]
                                                     │
                                                     ▼
                                            [ System Security UI ]
                                            ( Prompt User Consent )
                                                     │
                                                     ▼ ( User Approves )
  [ Application ] ◄── ( PipeWire Stream FD ) ◄───────┘
         │
         ▼
  [ Reads Screen Video Stream via PipeWire Buffer Handles ]
```

1. **Request Delegation**: Instead of asking the display server directly for screen pixels, the application issues a D-Bus IPC request to `org.freedesktop.portal.ScreenCast`.
2. **User Consent Gate**: The portal daemon invokes a native compositor dialog asking the user to explicitly select which screen, output, or window to share.
3. **PipeWire Stream Delivery**: Upon user approval, the portal daemon returns a PipeWire media stream file descriptor to the application. Screen pixels flow securely over PipeWire buffer handles without granting the application persistent access to the display server's global state.

---

## Extension Ecosystem & Desktop Semantics

The core `wayland.xml` specification is intentionally incomplete: it defines surfaces, buffers, and seats, but completely omits desktop window management concepts like title bars, minimization, maximizing, popups, or window positioning. These higher-level semantics are defined via **Protocol Extensions**.

### 1. `xdg-shell` Protocol Standard
`xdg-shell` is the universal protocol extension that defines desktop window behavior across toolkits (GTK, Qt) and compositors (Mutter, KWin, wlroots):

```
                       xdg-shell Interface Structure

                                ┌──────────────┐
                                │ xdg_wm_base  │ (Global Desktop Factory)
                                └──────┬───────┘
                                       │
                                       ▼
                                ┌──────────────┐
                                │ xdg_surface  │ (Binds to wl_surface)
                                └──────┬───────┘
                                       │
                   ┌───────────────────┴───────────────────┐
                   ▼                                       ▼
          ┌─────────────────┐                     ┌─────────────────┐
          │  xdg_toplevel   │                     │    xdg_popup    │
          │ (Main Windows)  │                     │ (Menus, Tooltips│
          └─────────────────┘                     └─────────────────┘
```

* **`xdg_wm_base`**: The global desktop management factory. Responds to compositor ping requests (`ping`/`pong`) to monitor client responsiveness.
* **`xdg_surface`**: Assigns desktop roles to a base `wl_surface`.
* **`xdg_toplevel`**: Represents a top-level desktop application window. Handles window resizing, maximization (`set_maximized`), minimization (`set_minimized`), fullscreen toggles (`set_fullscreen`), and window title/app-id metadata.
* **`xdg_popup`**: Represents transient popups, dropdown menus, and tooltips, positioned relative to a parent `xdg_surface` using explicit grab policies.

### 2. Extension Governance: `wayland-protocols`
Extension protocols are categorized into standardized governance tiers within the `wayland-protocols` repository:
- **Stable**: Fully locked, backwards-compatible protocols (`xdg-shell`, `presentation-time`, `viewporter`).
- **Staging**: Protocols undergoing real-world validation prior to final stabilization (`fractional-scale-v1`, `cursor-shape-v1`, `tearing-control-v1`, `explicit-synchronization-v1`).
- **Unstable / Legacy**: Experimental protocols prefixed with `z` and versioned explicitly (e.g., `zwp_linux_dmabuf_v1`).

---

## XWayland Compatibility Strategy

To enable seamless transition from X11 to Wayland without breaking decades of legacy software, the Wayland ecosystem engineered **XWayland**—a specialized compatibility bridge.

```
                      XWayland Bridge Architecture

  ┌──────────────────────────────────────────────────────────────────────┐
  │ Legacy X11 Application (GIMP, Steam Game, Xterm)                     │
  └──────────────────────────────────┬───────────────────────────────────┘
                                     │ (X11 Protocol Wire / DISPLAY=:0)
                                     ▼
  ┌──────────────────────────────────────────────────────────────────────┐
  │ XWayland Server (Unprivileged Nested X.Org Server Process)           │
  │ - Translates X11 Window Creation ──► wl_surface Allocation           │
  │ - Translates X11 Pixmaps          ──► wl_buffer / DMA-BUF Submissions │
  │ - Translates X11 Damage Events   ──► wl_surface.damage Operations     │
  └──────────────────────────────────┬───────────────────────────────────┘
                                     │ (Native Wayland IPC Wire)
                                     ▼
  ┌──────────────────────────────────────────────────────────────────────┐
  │ Host Wayland Compositor (Mutter / KWin / wlroots)                    │
  │ - Composites XWayland Surfaces Alongside Native Wayland Surfaces     │
  └──────────────────────────────────────────────────────────────────────┘
```

### 1. Rootless Embedded Architecture
XWayland is a complete X.Org Server binary compiled without hardware driver backends. Instead of driving graphics cards or input devices directly, XWayland runs as an unprivileged Wayland client connected to the host compositor:
- **Window Mapping**: When an X11 application creates a top-level X11 window, XWayland instantiates a corresponding native `wl_surface` and `xdg_toplevel` object inside the host Wayland compositor.
- **Buffer Forwarding**: X11 drawing operations update offscreen pixmaps inside XWayland. XWayland wraps these pixmaps in `wl_buffer` handles (via `DMA-BUF` or shared memory) and commits them to the host Wayland compositor.
- **Input Forwarding**: Pointer and keyboard events received by XWayland from the host compositor are translated into standard X11 input events (`KeyPress`, `MotionNotify`) and routed to target X11 windows.

### 2. Compatibility Cost and Isolation Bounds
While XWayland allows unmodified legacy binaries to execute, it introduces explicit architectural trade-offs:
- **Shared X11 Namespace**: X11 applications running inside XWayland share a common X11 server namespace, meaning X11 applications can still spy on or inject input into *other X11 applications* running inside the same XWayland instance. However, they **cannot** inspect native Wayland surfaces or bypass the host compositor's security boundaries.
- **Scaling and Fractional DPI Overhead**: Translating legacy X11 coordinate spaces to modern HiDPI or fractional scaling Wayland outputs requires bitmap scaling or compositor viewport transforms (`wp_viewporter`), occasionally introducing visual blurriness on unadapted X11 applications.

---

## Compositor Ecosystem

Unlike X11, where a single reference display server binary (`Xorg`) dominated all desktop environments, the Wayland specification mandates that **compositors implement display server behavior**. This produced a diverse, competitive compositor ecosystem:

```
                      Wayland Compositor Ecosystem

                       ┌─────────────────────────┐
                       │  Wayland Protocol Specs │
                       └────────────┬────────────┘
                                    │
    ┌───────────────────┬───────────┴───────────┬───────────────────┐
    ▼                   ▼                       ▼                   ▼
┌───────┐           ┌────────┐             ┌────────┐          ┌──────────┐
│Weston │           │ Mutter │             │  KWin  │          │ wlroots  │
└───────┘           └────────┘             └────────┘          └────┬─────┘
(Reference)          (GNOME)                 (KDE)                  │
                                                   ┌────────────────┴────────┐
                                                   ▼                         ▼
                                             ┌──────────┐              ┌──────────┐
                                             │   Sway   │              │ Gamescope│
                                             └──────────┘              └──────────┘
                                              (Tiling)                   (Gaming)
```

### 1. Weston (Reference Implementation)
Maintained by the core Wayland project, Weston serves as the definitive reference implementation of protocol correctness. It demonstrates minimal DRM/KMS backend initialization, `wl_shm` / `DMA-BUF` composition, and reference shell logic without desktop environment dependencies.

### 2. Desktop Compositors (Mutter & KWin)
* **GNOME Mutter**: Integrates Wayland display server logic directly into the GNOME Shell rendering pipeline. Prioritizes Client-Side Decoration (CSD), strict `xdg-shell` compliance, and desktop shell integration.
* **KDE KWin**: Implements Wayland compositing for KDE Plasma. Supports both Client-Side Decoration and Server-Side Decoration (SSD) via `zxdg_decoration_manager_v1`, offering extensive window management scripting.

### 3. `wlroots` and the Modular Compositor Architecture
Created by Drew DeVault and the Sway development team, `wlroots` revolutionized Wayland compositor development by providing a modular, unopinionated C library implementing core compositor infrastructure. `wlroots` abstracts DRM/KMS page flips, EGL context initialization, `libinput` device handling, and protocol extension state machines. It powers tiling compositors (Sway, River), dynamic desktop compositors (Hyprland), and specialized embedded compositors.

### 4. Gamescope (Specialized Gaming Micro-Compositor)
Developed by Valve Corporation for [SteamOS](steamos.md) and the Steam Deck, `Gamescope` is a specialized Wayland micro-compositor. It executes as a nested Wayland server or direct DRM compositor, isolating individual game rendering surfaces, enforcing precise frame pacing, applying hardware-accelerated upscaling (AMD FSR, NIS), and compositing system overlays without window manager overhead.

---

## Toolkit & Application Layer

The transition of applications to Wayland was mediated primarily through major GUI toolkits:

```
                    Toolkit Wayland Integration Topology

  [ GTK Application ]     [ Qt Application ]     [ SDL3 Game Engine ]     [ Electron App ]
          │                        │                      │                      │
          ▼                        ▼                      ▼                      ▼
  ┌───────────────┐        ┌───────────────┐      ┌───────────────┐      ┌───────────────┐
  │  GDK Wayland  │        │  Qt Wayland   │      │ SDL Wayland   │      │ Ozone Platform│
  │    Backend    │        │    Plugin     │      │    Backend    │      │ (Chromium)    │
  └───────┬───────┘        └───────┬───────┘      └───────┬───────┘      └───────┬───────┘
          │                        │                      │                      │
          └────────────────────────┴──────────┬───────────┴──────────────────────┘
                                              │
                                              ▼
                           [ Native Wayland Protocol Requests ]
```

### 1. Native Toolkit Backends
* **GTK (GDK Wayland Backend)**: Full native Wayland support introduced in GTK 3.x and perfected in GTK 4. Standardized Client-Side Decoration (CSD), rendering window title bars, close buttons, and header bars directly inside application buffers.
* **Qt (Qt Wayland Plugin)**: Modular platform plugin (`-platform wayland`) enabling Qt applications to execute natively. Supports both CSD and Server-Side Decoration (SSD) negotiation.
* **SDL2 / SDL3**: Simple DirectMedia Layer added native Wayland surface support, enabling cross-platform C++ game engines to allocate native Wayland EGL swapchains without X11 overhead.
* **Electron / Chromium (Ozone Platform)**: The Ozone abstraction layer enabled Chromium and Electron applications (VS Code, Slack, Discord) to toggle between native X11 and native Wayland backends seamlessly.

### 2. The Decoration Policy Split: CSD vs SSD
A major architectural debate in the Wayland ecosystem emerged around window decoration responsibility:
- **Client-Side Decoration (CSD)**: The application renders its own window borders, title bars, and window control buttons directly inside its pixel buffer. Favored by GNOME and GTK, CSD allows applications to embed search bars, tab strips, and custom UI controls into the title bar space.
- **Server-Side Decoration (SSD)**: The compositor draws window frames and title bars around client surfaces. Favored by KDE and `wlroots` compositors, SSD guarantees consistent window frame appearance and behavior across all applications, regardless of toolkit.
- **Reconciliation (`zxdg_decoration_manager_v1`)**: The decoration negotiation extension allows clients and compositors to negotiate decoration authority at runtime.

---

## Ecosystem Lock-In & Socio-Technical Persistence

Wayland’s transition from experimental proposal to dominant Linux infrastructure was governed by powerful socio-technical feedback loops and friction surfaces:

```
                    Wayland Ecosystem Reinforcement Loops

  ┌──────────────────────────────────────────────────────────────────────┐
  │ Distribution Defaults (Fedora, Ubuntu, RHEL, Arch Session Defaults)  │
  └──────────────────────────────────┬───────────────────────────────────┘
                                     │
                                     ▼
  ┌──────────────────────────────────────────────────────────────────────┐
  │ Major Toolkit Backends Target Native Wayland (GTK4, Qt6, SDL3)       │
  └──────────────────────────────────┬───────────────────────────────────┘
                                     │
                                     ▼
  ┌──────────────────────────────────────────────────────────────────────┐
  │ Application Migration Pressure (Chromium Ozone, Electron, Gamescope) │
  └──────────────────────────────────┬───────────────────────────────────┘
                                     │
                                     ▼
  ┌──────────────────────────────────────────────────────────────────────┐
  │ Portal API Standardization (xdg-desktop-portal, PipeWire)            │
  └──────────────────────────────────┬───────────────────────────────────┘
                                     │
                                     ▼
  ┌──────────────────────────────────────────────────────────────────────┐
  │ Hardware & Driver Vendor Alignment (Mesa GBM, NVIDIA DRM KMS/GBM)    │
  └──────────────────────────────────────────────────────────────────────┘
```

### 1. Self-Reinforcing Adoption Drivers
1. **Distribution Session Defaults**: Major distributions switching their default desktop sessions to Wayland (Fedora 25 in 2016, Ubuntu 21.04 in 2021) forced software developers, hardware vendors, and toolkit maintainers to prioritize Wayland bug fixes and performance optimizations.
2. **Toolkit Deprecation Cycles**: GTK4 and Qt6 built their primary rendering pipelines around modern surface compositing, making legacy X11 backends secondary maintenance targets.
3. **Gaming & Handheld Integration**: Valve selecting Wayland (`Gamescope`) for the Steam Deck cemented Wayland as the default display architecture for modern PC gaming and low-latency display pacing.

### 2. Migration Constraints and Friction Surfaces
* **Proprietary NVIDIA Driver Paths**: For over a decade, NVIDIA resisted the open Linux graphics ecosystem standard (Generic Buffer Management - `GBM`), attempting to force its proprietary `EGLStreams` API. Because compositors refused to maintain separate vendor-specific buffer sharing paths, NVIDIA users experienced severe rendering glitches and lack of hardware acceleration until NVIDIA eventually adopted `GBM` support in 2021.
* **Advanced Desktop Feature Gaps**: Certain specialized desktop workflows that relied on X11 ambient authority—such as global hotkey daemons, screen color pickers, automated window manipulation scripts, dynamic screen recording, and advanced color management/HDR—required multi-year protocol extension development and portal plumbing before matching X11 feature parity.

---

## Constraint Migration

The evolution of display server architectures demonstrates how computational abstractions shift as physical, hardware, and security constraints migrate:

```
                            Constraint Migration

 Remote Network Graphics (1980s X11 Era) ──► Server 2D Drawing Primitives & Core Fonts
                                                               │
                                                               ▼
 Local GPU Acceleration (2000s) ───────────► Offscreen Client Rendering & Compositors
                                                               │
                                                               ▼
 Ambience & Security Vulnerabilities ──────► Protocol Isolation & Surface Capability Bounds
                                                               │
                                                               ▼
 Multi-Vendor Ecosystem Fragmentation ─────► Standardized Extensions (xdg-shell, DMA-BUF)
                                                               │
                                                               ▼
 Low-Latency & Mobile Handheld Limits ─────► Zero-Copy Scanout & VSync Frame Pacing
```

1. **Networked Terminal Constraint $\rightarrow$ Local Acceleration**: X11 was optimized for thin network terminals executing drawing commands on a remote mainframe. As GPUs digitized local framebuffers, server-side 2D drawing became an obsolete bottleneck, driving Wayland's direct client buffer submission architecture.
2. **Ambient Access Risk $\rightarrow$ Capability Isolation**: The open X11 namespace permitted arbitrary window peeking and keylogging. As desktop operating systems faced untrusted applications and web browsers, display authority migrated from open client access to strict compositor capability gates.
3. **Display Latency & Tearing $\rightarrow$ VSync Pacing**: Monolithic display presentation without compositor coordination produced tearing and frame jitter. Wayland migrated display timing to hardware VSync callbacks (`wl_surface.frame`), ensuring tear-free presentation by construction.

---

## Recurring Ideas & Heterogeneous Survival

Wayland’s architectural primitives reflect recurring concepts across systems history:

* **Compositor as Display Server $\rightarrow$ Microkernel Graphics Executive**: Collapsing display server, window manager, and input arbitrator into a single authority mirrors the integration seen in macOS `WindowServer` and Android `SurfaceFlinger`.
* **Explicit Buffer State Machines $\rightarrow$ Modern Graphics APIs**: Wayland’s `attach`/`damage`/`commit` surface lifecycle directly mirrors explicit command list recording and queue submission in modern low-level graphics APIs (Vulkan, Direct3D 12, [Apple Metal](apple-metal.md)).
* **Capability Boundaries via IPC Proxies**: Delegating privileged screen capture to `xdg-desktop-portal` over D-Bus revives classic capability-based object security ([Capability Systems](capability-systems.md), [KeyKOS](keykos-nanokernel-capabilities.md)), replacing ambient socket rights with explicit user consent tokens.

---

## Historical Counterfactuals

1. **What if X11 had been incrementally hardened instead of replaced?**
   If the X.Org community had successfully stripped legacy 2D drawing code, stabilized XACE security extensions, and integrated compositing directly into Xorg, the Linux ecosystem might have avoided a decade-long display server transition. However, maintaining backwards compatibility with 30 years of X11 wire protocol specs would have left severe architectural debt, high context-switch latency, and complex state synchronization bottlenecks intact.

2. **What if Wayland had mandated a single reference desktop compositor?**
   If the Wayland project had required all desktop environments to run on a single mandatory compositor binary (e.g., forcing GNOME, KDE, and Sway to use Weston), protocol fragmentation would have been eliminated. However, desktop environments would have lost operational autonomy, suppressing innovations like `wlroots` and `Gamescope`.

3. **What if XWayland had not been developed?**
   Without XWayland, Linux desktop migration to Wayland would have stalled indefinitely. Legacy proprietary software, Steam game catalogs, and unmaintained desktop applications would have broken completely, trapping users on legacy X11 sessions.

---

## Compare Wayland with Other Computational Lineages

| Dimension | Wayland Protocol | X Window System (X11) | macOS WindowServer | Windows DWM (Desktop Window Mgr) | Android SurfaceFlinger |
|:---|:---|:---|:---|:---|:---|
| **Authority Model** | **Compositor-Centric**: Compositor is display server & input master. | **Server-Centric**: Xorg Server owns screen; WM is secondary client. | **Unified Server**: Monolithic WindowServer process owns display & compositing. | **Executive Layer**: DWM composites surface buffers generated by Win32/DirectX. | **System Service**: SurfaceFlinger composites system & app surface layers. |
| **Drawing & Presentation** | **Client-Allocated Buffers**: Shared memory or GPU `DMA-BUF` handles. | **Server Primitive Drawing**: Server draws lines/fonts or receives pixmaps. | **Client Surface Buffers**: Quartz / Metal surface buffer handles. | **Client Direct Composition**: DirectComposition / DirectX swapchains. | **Client Buffer Queues**: Gralloc GPU buffers submitted to Hardware Composer. |
| **Network Transparency** | **Local Socket Default**: Protocol decoupled; network via RDP/VNC proxies. | **Built-in Network IPC**: Core drawing commands transmitted over TCP/IP. | **Local Execution**: Surface buffers bound to local display hardware. | **Local Execution**: Remote display offloaded to RDP video streaming. | **Local Execution**: Surface buffers bound to mobile SoC hardware. |
| **Security & Isolation** | **Strict Capability Isolation**: No cross-client surface peeking or input sniffing. | **Open Ambient Namespace**: Any client can spy on windows and capture global keys. | **Enclave Isolation**: App Sandbox & Accessibility permission gates. | **Session Isolation**: UIPI (User Interface Privilege Isolation) boundaries. | **Binder Sandbox**: UID separation & SELinux surface access controls. |
| **Extension Architecture** | **Modular XML Protocols**: `xdg-shell`, `wayland-protocols` extension repos. | **Server Extensions**: XRENDER, SHM, Composite, RANDR, XINPUT. | **Proprietary Frameworks**: Private System frameworks & AppKit/UIKit. | **Proprietary Frameworks**: Win32 / DWM private composition APIs. | **Android HAL / Binder**: Hardware Composer (HWC) HAL interfaces. |
| **Compatibility Strategy** | **XWayland Bridge**: Rootless embedded Xorg server client. | **Monolithic Back-Compat**: Multi-decade protocol wire stability. | **Quartz / Carbon Layers**: Transitory emulation layers during OS shifts. | **Win32 Back-Compat**: Multi-decade Win32/DirectX binary stability. | **Android NDK / HAL**: Dynamic HAL translation across Android versions. |
| **Compositor Role** | **Mandatory Engine**: Compositor manages KMS mode setting & input. | **Optional Client**: Compositing WM operates as an external X11 client. | **Mandatory Engine**: Core Quartz Compositor engine. | **Mandatory Engine**: DWM manages composition scene graph. | **Mandatory Engine**: SurfaceFlinger + Hardware Composer (HWC). |
| **Application Assumptions** | **Surface Commit Loop**: Asynchronous frame callbacks (`wl_surface.frame`). | **Synchronous Request Loop**: Blocking X11 event requests and replies. | **Display Link Loop**: CADisplayLink / Metal frame pacing loops. | **DXGI Swapchain**: DXGI Present calls synchronized to VSync. | **Choreographer Loop**: VSync-aligned Choreographer frame callbacks. |
| **Long-Term Persistence** | **Linux Standard**: Ubiquitous display protocol for desktop, gaming, embedded. | **Legacy Maintenance**: Deprecated baseline reserved for legacy Unix software. | **Proprietary Standard**: Core display substrate across macOS, iOS, visionOS. | **Proprietary Standard**: Core display substrate across Windows desktop & Xbox. | **Mobile Standard**: Core display substrate across billions of Android devices. |

---

## Modern Relevance

Wayland’s architectural footprint extends across the modern computing spectrum:

### 1. Ubiquitous Linux Desktop Infrastructure
Wayland is the default display architecture across major enterprise and community Linux distributions (Fedora, Red Hat Enterprise Linux, Ubuntu, Debian, Arch Linux, SUSE). Desktop environments (GNOME 40+, KDE Plasma 6) treat Wayland as their primary development target.

### 2. Gaming Compositors & Handheld Stacks
Valve’s `Gamescope` micro-compositor proved that Wayland’s surface-oriented model offers superior low-latency frame pacing, resolution upscaling, and overlay compositing for handheld gaming consoles (Steam Deck) and custom home theater gaming PCs.

### 3. Automotive, Embedded & Smart Systems
Wayland’s minimal core footprint and decoupling of shell semantics made it the default display substrate for Automotive Grade Linux (AGL), embedded IVI (In-Vehicle Infotainment) systems, smart TVs (webOS, Tizen), and industrial touch panels, where full desktop window managers are unnecessary.

### 4. Advanced Display Features (HDR & Explicit Sync)
Modern display innovations on Linux—such as High Dynamic Range (HDR) color management, Wide Color Gamut (WCG), Variable Refresh Rate (VRR / FreeSync / G-Sync), and Explicit GPU Synchronization (`linux-drm-syncobj-v1`)—are implemented natively as Wayland protocol extensions, defining the future of high-performance Linux graphics.

---

## Reconstruction Proposal: Wayland Surface Protocol & Frame Loop Simulator

To expose the core mechanisms of **Wayland wire protocol framing, `wl_surface` double-buffered state commits, and VSync frame callback pacing**, we propose an interactive, zero-dependency Python simulator located in `reconstructions/wayland_surface_protocol/wayland_sim.py`.

### Key Architectural Components
1. **Wire Message Encoder/Decoder**: Simulates 32-bit aligned Wayland wire message serialisation, header parsing (Object ID, Opcode, Length), and dynamic object creation (`wl_registry.bind`).
2. **Double-Buffered State Machine**: Implements `wl_surface` pending versus current state mechanics, demonstrating how `attach`, `damage`, and `commit` operations achieve atomic frame updates.
3. **Compositor Scene Graph & VSync Pacing Loop**: Simulates a multi-surface scene graph executing a KMS page flip loop, firing `wl_callback.done` frame events only on hardware VSync ticks.
4. **Seat Input Focus Router**: Simulates a `wl_seat` distributing pointer and keyboard events exclusively to focused surfaces while enforcing input isolation for background surfaces.

---

## Knowledge-Graph Relationships

```json
[
  {
    "source": "wayland",
    "target": "x11",
    "relationship": "replaces_architecture_of"
  },
  {
    "source": "wayland",
    "target": "compositor",
    "relationship": "centers_display_authority_in"
  },
  {
    "source": "wayland",
    "target": "wl_surface",
    "relationship": "defines_core_primitive"
  },
  {
    "source": "wayland",
    "target": "xdg_shell",
    "relationship": "uses_extension_for_desktop_semantics"
  },
  {
    "source": "xwayland",
    "target": "wayland",
    "relationship": "bridges_x11_clients_to"
  },
  {
    "source": "gamescope",
    "target": "wayland",
    "relationship": "implements_micro_compositor_protocol"
  },
  {
    "source": "mutter",
    "target": "wayland",
    "relationship": "implements_compositor_server"
  },
  {
    "source": "kwin",
    "target": "wayland",
    "relationship": "implements_compositor_server"
  },
  {
    "source": "wlroots",
    "target": "wayland",
    "relationship": "provides_composable_library_for"
  },
  {
    "source": "wayland",
    "target": "linux",
    "relationship": "executes_on_kernel_drm_kms"
  }
]
```

---

## Research Questions

1. **Will Client-Side Decoration (CSD) and Server-Side Decoration (SSD) ever achieve architectural unification?** Will cross-toolkit decoration extensions permanently eliminate visual inconsistency across GTK, Qt, and custom application title bars?
2. **Can D-Bus portals completely replace legacy X11 IPC capabilities without introducing permission fatigue?** As applications request granular portal access for hotkeys, screenshots, and window positioning, how do desktop environments prevent user prompt exhaustion?
3. **How does explicit GPU synchronization alter Wayland compositor rendering architecture?** Will `linux-drm-syncobj-v1` eliminate out-of-order frame presentation and GPU driver stall hazards across heterogeneous multi-GPU systems?

---

## Limitations and Uncertainties

* **Implementation Divergence across Compositors**: Because Wayland is a protocol specification rather than a single server executable, individual compositor implementations (Mutter, KWin, Sway, Hyprland) may exhibit minor differences in extension support, timing heuristics, and window management policies.
* **Rapid Extension Lifecycle**: Advanced protocol extensions (HDR, color management, explicit sync) evolve rapidly within `wayland-protocols`, requiring analysis to distinguish stable baseline protocols from active staging specifications.

---

## Excavation Scorecard

| Category | Rating | Rationale |
| :--- | :--- | :--- |
| Historical Importance | ★★★★★ | Re-architected Linux graphical session display architecture, replacing 30 years of legacy X11 display server conventions. |
| Technical Innovation | ★★★★★ | Engineered asynchronous wire IPC, double-buffered surface commits, DMA-BUF zero-copy presentation, and seat input isolation. |
| Commercial Success | ★★★★★ | Standard default display engine across major Linux distributions, Steam Deck handheld devices, and automotive infotainment systems. |
| Modern Potential | ★★★★★ | Foundational display substrate for modern Linux desktop environments, low-latency gaming compositors, and HDR display pipelines. |
| AI Synergy | ★★☆☆☆ | Indirect synergy via GPU buffer sharing and display compositing for multi-modal AI UI interfaces. |
| Difficulty to Recreate | ★★★★☆ | Implementing a complete Wayland compositor requires orchestrating DRM/KMS, EGL/GLES, libinput, and complex protocol extension state machines. |

---

## Bibliography

1. Høgsberg, K. (2008–2012). *The Wayland Display Server Protocol Specification and Architecture Notes*. Wayland Project / freedesktop.org.
2. Wayland Project. (2012–2024). *wayland.xml: Wayland Core Protocol Specification*. freedesktop.org.
3. freedesktop.org. (2017–2024). *xdg-shell Protocol Specification & wayland-protocols Extensions Repository*. freedesktop.org.
4. Packard, K. (2013). *XWayland: Integrating X11 and Wayland Architecture*. X.Org Foundation Proceedings.
5. DeVault, D., et al. (2018–2024). *wlroots: Modular Wayland Compositor Library Documentation*. ddevault.com / swaywm.org.
6. Valve Corporation. (2022–2024). *Gamescope: Embedded Wayland Gaming Compositor Architecture*. GitHub Repository.
7. Stone, D. (2013). *The Realities of Display Server Engineering: Wayland vs X11*. Linux.conf.au Keynote Presentation.

---

*Cross-links: [Linux: The Ubiquitous Substrate](linux.md), [SteamOS: Gaming-Session Substrate](steamos.md), [Ecosystem Lock-In](../patterns/ecosystem-lockin.md), [Constraint Migration](../patterns/constraint-migration.md), [Capability Systems](../excavations/capability-systems.md), [Qt](../excavations/qt.md).*

---

**Last updated**: August 26, 2026
