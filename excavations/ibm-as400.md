# IBM AS/400: Layered Technology-Independent Substrate & Single-Level Store

> A layered, object-based machine architecture decoupling application semantics from physical hardware via the Technology Independent Machine Interface (TIMI) and a single-level store, enabling unprecedented decades-long software persistence across radical CPU microarchitecture shifts.

---

## Historical Context

In June 1988, IBM introduced the **Application System/400 (AS/400)** (system code name *Silverlake*). To commercial markets, it was presented as the successor to IBM’s midrange business computing lines—primarily the System/36 and System/38. However, from a computational archaeology perspective, the AS/400 was not merely a commercially packaged midrange server; it represented the architectural maturation of a radical computing paradigm originally conceived in the early 1970s under IBM's Future System (FS) project and first commercialized in 1978 as the IBM System/38.

During the late 1970s and 1980s, the software industry faced a growing crisis: **hardware architectural volatility**. Rapid advances in semiconductor technology meant that processor instruction set architectures (ISAs) were changing every 3 to 5 years. For enterprise businesses, re-compiling, re-testing, or rewriting complex business logic (written in RPG or COBOL) for each new hardware platform imposed unsustainable financial costs and operational risks.

Traditional operating systems (such as Unix, VM/CMS, or MS-DOS) exposed the underlying physical memory model, register files, and CPU instruction sets directly to compilers and system utilities. When the underlying hardware changed, application binaries broke.

Under the leadership of Chief Architect Frank Soltis at IBM Rochester, Minnesota, the engineering team designed the AS/400 to invert this relationship. Rather than forcing applications to adapt to hardware, they constructed an integrated, layered substrate where:
1. **Hardware was completely abstracted** behind an intermediate high-level interface.
2. **Volatile main memory and persistent disk storage were merged** into a single, flat, 64-bit (and later 128-bit capability-aware) virtual address space.
3. **Operating system resources were encapsulated as strongly-typed objects** rather than raw byte-stream files or process tables.
4. **Database management was integrated directly into the OS kernel** rather than hosted as external application middleware.

The AS/400 was designed to solve a fundamental business constraint: *how to allow enterprise software logic to outlive the physical silicon on which it executes.*

---

## Archaeological Scope

The AS/400 ecosystem is not a single monolith or hardware box, but a vertically integrated computational stack spanning hardware, microcode, virtual machine interface, operating system, integrated database, and application runtime contracts.

```
+-------------------------------------------------------------------+
|                  High-Level Business Applications                 |
|                   (RPG III/IV, COBOL, CL, C, SQL)                 |
+-------------------------------------------------------------------+
|                 OS/400 Integrated Service Substrate               |
|  +---------------------+ +------------------+ +-----------------+ |
|  | Typed Object System | | DB2 for OS/400   | | Work Management | |
|  | (Libraries/User Pfs)| | (Physical/Logical| | (Subsystems/Jobs| |
|  |                     | |  File Catalog)   | |  & Queues)      | |
|  +---------------------+ +------------------+ +-----------------+ |
+-------------------------------------------------------------------+
|               Technology Independent Machine Interface             |
|                                (TIMI)                             |
|       [High-level instructions, abstract registers, typed pointers] |
+-------------------------------------------------------------------+
|                 System Licensed Internal Code (SLIC)               |
|      (Vertical Microcode, Page Fault Managers, Hardware Drivers,  |
|       TIMI-to-Native Translators, Single-Level Store Allocator)    |
+-------------------------------------------------------------------+
|                 Physical Microarchitecture & Hardware             |
|    (Original 48-bit CISC IMPI -> 64-bit Amazon POWER RISC ->      |
|                      Modern POWER10 Processors)                   |
+-------------------------------------------------------------------+
```

### 1. Hardware Implementation Layer
The physical hardware substrate. Historically evolved across three distinct silicon eras:
* **CISC Custom Processors (1988–1995)**: Multi-chip 48-bit CISC architectures based on the Instruction Micro Processor Interface (IMPI).
* **PowerPC AS RISC Processors (1995–2001)**: 64-bit RISC implementations (A10, A30, "Muskie", "Pulsar") extending PowerPC with tags for single-level store address tracking and capability security.
* **Unified POWER Processors (2001–Present)**: Convergence onto standard IBM POWER ISAs (POWER4 through POWER10) running IBM i in LPAR virtualized partitions.

### 2. System Licensed Internal Code (SLIC) / Vertical Microcode
The trusted microcode layer executing below TIMI. Written in C++ and assembly, SLIC implements physical hardware device drivers, virtual memory management, process/thread context switching, page fault routing for the Single-Level Store, and the dynamic translation engine that compiles TIMI intermediate code into native CPU instruction streams.

### 3. Technology Independent Machine Interface (TIMI)
The formal mathematical and architectural contract dividing application/OS code from physical hardware. TIMI is an abstract, machine-independent instruction set that operates on typed references, abstract registers, and high-level primitive operations.

### 4. OS/400 (IBM i) Kernel & Subsystems
The operating system running above TIMI. Provides work management (jobs, subsystems, job queues), security governance, library-based object namespaces, and native system utilities.

### 5. Integrated Database Facilities (DB2 for OS/400 / IBM i)
The native relational database engine built directly into the operating system kernel and TIMI abstractions. Provides Physical Files (table structures) and Logical Files (index/projection views) using Data Description Specifications (DDS) or SQL.

---

## Historical Lineage

The evolution of the AS/400 lineage demonstrates remarkable architectural continuity across more than four decades, despite major rebrandings and complete hardware replacements.

```
System/38 (1978)
  |  (Inherited TIMI concept, 48-bit Single-Level Store, Object Model)
  v
AS/400 Launch (1988) [B-Series, C-Series]
  |  (CISC 48-bit IMPI CPU, OS/400 v1r1, RPG III, Physical/Logical Files)
  v
CISC-to-RISC Transition (1995) [OS/400 V3R6]
  |  (TIMI retranslation engine converts all binaries to 64-bit PowerPC AS without source code)
  v
iSeries & eServer iSeries (2000) [V5R1]
  |  (LPAR hardware virtualization, PASE AIX binary execution environment, DB2 SQL integration)
  v
System i & IBM i (2008–Present) [IBM i 6.1 -> 7.5]
  |  (Running on POWER8/9/10 hardware, 128-bit capability addresses, containerized work environments)
```

### Architectural Continuity Checks across Lineage Eras

| Era / Brand | Engine / Hardware | TIMI Boundary Preserved? | Storage Model | Object Continuity |
| :--- | :--- | :--- | :--- | :--- |
| **System/38 (1978)** | Custom CISC (48-bit addressing) | System Vector / Machine Interface | 48-bit Single-Level Store | Native System Objects (`.OBJ`) |
| **AS/400 CISC (1988)** | Custom IMPI CISC | 48-bit TIMI Boundary | 48-bit Single-Level Store | OS/400 Object Architecture |
| **AS/400 RISC (1995)** | 64-bit PowerPC AS (A10/A30) | 64-bit TIMI Retranslation | 64-bit Single-Level Store | Direct Binary Object Retranslation |
| **iSeries (2000)** | POWER4 / SMR RISC | 64-bit TIMI + PASE Environment | 64-bit Single-Level Store | 100% Binary Application Compatibility |
| **IBM i on POWER (2008–Present)** | POWER8 / POWER9 / POWER10 | 64-bit TIMI (ILE & EPM Runtimes) | 64-bit Single-Level Store | Decades-Old Binaries Execute Natively |

**Lineage Finding**: Rebrandings (iSeries, System i, IBM i) were primarily marketing responses to open-system trends. Architecturally, the platform represents a continuous single lineage. Programs compiled to TIMI on an AS/400 B10 in 1988 can be restored onto a 2024 POWER10 server running IBM i 7.5 and executed after automatic TIMI-to-POWER10 retranslation.

---

## Architectural Artifacts

The platform relies on concrete object formats and binary structures that enforce isolation and hardware independence:

### 1. Program Objects (`*PGM`)
In OS/400, executables are not raw ELF/PE binary files, but structured system objects (`*PGM`). A `*PGM` object encapsulates:
* **Header & Metadata**: Authority settings, creation flags, compiler origin.
* **TIMI Intermediate Code (Template)**: The hardware-independent instruction stream generated by the compiler.
* **Associated Space**: Storage containing program variables, static data, and heap references.
* **Translated Native Executable Code**: The physical hardware instructions generated by SLIC for the current host CPU.

When the system detects that a `*PGM` object is being executed on a new CPU architecture (e.g., during a CISC-to-RISC migration), the SLIC translator reads the embedded TIMI intermediate representation, compiles it into new native instructions, updates the native executable segment inside the object, and executes it seamlessly.

### 2. User Profiles (`*USRPRF`)
Identity and capability enforcement are embedded into system objects (`*USRPRF`). Every process and job executes under the explicit context of a `*USRPRF`, which grants object-level authority pointers.

### 3. Data Description Specifications (DDS)
Before SQL became the dominant query interface, AS/400 data structures were defined using DDS source artifacts. DDS defines:
* **Physical Files (`*FILE PF`)**: Record layout, field types, primary keys, and fixed-length storage formats.
* **Logical Files (`*FILE LF`)**: OMIT/FORMAT specifications providing alternate access paths, filtered record views, and multi-file join structures without duplicating physical data.

---

## Extracted Abstractions

The AS/400 created six fundamental computational abstractions that achieved ecosystem-scale persistence:

1. **Technology Independent Machine Interface (TIMI)**: Decoupling application semantics and OS code from physical instruction set architectures through intermediate representations and automatic retranslation.
2. **Single-Level Store (SLS)**: Unifying main memory (RAM) and secondary storage (HDD/NVMe) into a single, flat, persistent virtual address space addressed by tagged 64-bit pointers.
3. **Typed Object Operating System**: Replacing untyped byte streams and Unix-style raw file paths with strongly-typed, system-encapsulated objects organized into library namespaces with capability-based security access control.
4. **Kernel-Integrated Relational Database**: Treating database tables, indices, and views as native OS primitives rather than user-space application middleware.
5. **Integrated Work Management & Subsystems**: Decoupling job scheduling, memory allocation pools, and batch execution queues into isolated, declaratively-managed execution environments (Subsystems).
6. **Tag-Protected Pointers & Capability-Style Security**: Hardware- and microcode-enforced memory tags that prevent address spoofing, buffer overflows, and unauthorized pointer manipulation at the physical register level.

---

## Layered Machine Architecture

The AS/400 layered machine model enforces a strict computational hierarchy where higher layers are isolated from lower-layer implementation details.

```text
[ User & Business Logic ]  -> RPG IV, COBOL, SQL, Command Language (CL)
          |
          v
[ OS/400 High-Level Substrate ] -> Libraries, Objects, DB2 Engine, Security
          |
          v
===================================================================
             TECHNOLOGY INDEPENDENT MACHINE INTERFACE (TIMI)
===================================================================
          |
          v
[ System Licensed Internal Code ] -> Virtual Memory, Translator, Drivers
          |
          v
[ Hardware Abstraction / Hypervisor ] -> PowerVM, LPAR, Microcode
          |
          v
[ Physical Processor & Memory ] -> POWER10 Cores, Main RAM, Disk/NVMe Arrays
```

### Separation of Responsibilities

* **Above TIMI**: Software developers write code in RPG, COBOL, C, or CL. Compilers generate TIMI intermediate instructions and OS/400 object templates. Software above TIMI has **zero visibility** into physical CPU registers, stack pointers, cache lines, page tables, or I/O addresses.
* **At TIMI**: The interface presents an abstract machine model with an infinite supply of typed variables, high-level mathematical operations, structured object handles, and database cursor primitives.
* **Below TIMI**: SLIC manages physical CPU allocation, memory management units (MMUs), page fault resolution, device driver interrupts, and JIT/AOT retranslation of TIMI code into host CPU microcode/ISA.

This architecture ensures that physical silicon can be completely replaced—switching from CISC to RISC, or expanding from 48-bit to 64-bit address spaces—without modifying a single byte of code above TIMI.

---

## TIMI & Compatibility Regime

### Mechanics of TIMI

TIMI is often compared to modern virtual machines such as the Java Virtual Machine (JVM) or Microsoft Common Language Runtime (CLR). However, TIMI differs in two critical ways:
1. **Operating System Integration**: TIMI is not an application-level runtime; the entire operating system (OS/400) and all user-space applications execute *above* TIMI.
2. **Ahead-Of-Time (AOT) Retranslation**: TIMI code is typically compiled into native host machine code at installation time or upon first execution, rather than being continuously interpreted.

TIMI instructions operate on abstract typed operands rather than physical register indices. For example, a TIMI arithmetic instruction does not specify `ADD R1, R2, R3`; instead, it specifies:

$$\text{ADDN}\quad (\text{TargetOperand}),\quad (\text{SourceOperand1}),\quad (\text{SourceOperand2})$$

where the operands refer to declared entry slots in the program's type dictionary (e.g., Packed Decimal, Zoned Decimal, Binary Float).

### The CISC-to-RISC Retranslation Event (1995)

The ultimate test of TIMI occurred in 1995 with the release of OS/400 V3R6 and the transition from 48-bit custom CISC processors to 64-bit PowerPC AS RISC processors.

```
+-----------------------------------------------------------------+
|                    Existing Program Object                      |
|  +-----------------------------------------------------------+  |
|  | Metadata & Associated Space                               |  |
|  +-----------------------------------------------------------+  |
|  | TIMI Intermediate Representation (Abstract Instructions)   |  |
|  +-----------------------------------------------------------+  |
|  | [OLD] 48-bit CISC Native Binaries (Obsolete)             |  |
|  +-----------------------------------------------------------+  |
+-----------------------------------------------------------------+
                                |
                                v
               [ SLIC Retranslation Engine (V3R6) ]
                                |
                                v
+-----------------------------------------------------------------+
|                    Updated Program Object                       |
|  +-----------------------------------------------------------+  |
|  | Metadata & Associated Space                               |  |
|  +-----------------------------------------------------------+  |
|  | TIMI Intermediate Representation (Preserved Unchanged)    |  |
|  +-----------------------------------------------------------+  |
|  | [NEW] 64-bit PowerPC RISC Native Binaries (Generated)    |  |
|  +-----------------------------------------------------------+  |
+-----------------------------------------------------------------+
```

During this migration:
1. Customers restored backup tapes containing CISC program objects onto new RISC hardware.
2. The SLIC operating system detected that the embedded native executable section matched the 48-bit CISC architecture, whereas the host CPU was 64-bit RISC.
3. SLIC automatically invoked the internal optimizer/translator, parsed the embedded TIMI intermediate stream, compiled brand-new 64-bit PowerPC assembly, optimized register allocation for the RISC pipeline, and updated the program object.
4. **Result**: Millions of enterprise applications migrated across instruction sets without source code availability, re-compilation, or manual intervention.

---

## Object Model, Libraries & Authority

Unlike Unix-like operating systems where "everything is a file" (a stream of uninterpreted bytes), in OS/400 **everything is a typed object**.

### Object Architecture

Every entity in the system is represented by a structured system object identified by a name, a type, and a library container:

$$\text{Object Reference} = \text{Library} \quad / \quad \text{Object Name} \quad (\text{Object Type})$$

Common system object types include:
* `*PGM`: Executable Program
* `*FILE`: Database Physical/Logical File, Printer File, or Device File
* `*LIB`: Library (Namespace container)
* `*USRPRF`: User Profile (Security identity)
* `*JOBD`: Job Description (Work execution parameters)
* `*SBSD`: Subsystem Description (Execution environment definition)
* `*MSGQ`: Message Queue

### Library Namespace vs. Hierarchical Directory

In the classic OS/400 object domain, namespaces are flat two-level hierarchies: `LIBRARY / OBJECT`.
* Libraries (`*LIB`) act as object catalogues.
* The system searches for objects using a library list (`*LIBL`), analogous to a system `PATH`, but applying to all system object references (programs, database files, panels).
* (Note: In later releases, the Integrated File System (IFS) added POSIX hierarchical pathing `/home/user/file.txt`, but native OS/400 operations remain strictly object- and library-centric.)

### Security & Authority Model

OS/400 enforces object-centric security. Objects cannot be modified via arbitrary pointer access or raw byte writes. Only system microcode (SLIC) can mutate object structures.

Users are granted explicit authorities to objects:
* `*READ`: Read data/attributes
* `*ADD`: Insert records or objects
* `*UPD`: Update existing data
* `*DLT`: Delete data
* `*EXECUTE`: Execute program objects
* `*ALL`: Full ownership authority

Capability security is enforced at the pointer level: pointers on the system contain hidden 1-bit tag flags in physical hardware RAM. If a user program attempts to construct or tamper with a memory address pointer in user memory, the hardware clears the tag bit, causing a hardware capability fault upon access.

---

## Single-Level Store

The **Single-Level Store (SLS)** is arguably the AS/400's most distinctive storage abstraction. Designed by Frank Soltis and the System/38 engineering team, SLS eliminates the traditional operating system distinction between main memory (RAM) and disk storage.

```
Traditional Operating System (Unix / Windows / Linux)
+------------------------------------+  +------------------------------------+
| Main Memory (RAM)                  |  | Secondary Storage (Disk / NVMe)    |
| - Virtual Address Space (32/64-bit)|  | - File System Hierarchy            |
| - Volatile Pointers & Heaps        |  | - File Handles, Inodes, Blocks     |
+------------------------------------+  +------------------------------------+
                   \                    /
                    Explicit I/O Operations (read(), write(), fread())

==================================================================================

AS/400 Single-Level Store Architecture
+--------------------------------------------------------------------------------+
| Single Flat Virtual Address Space (64-bit / 128-bit Capability Pointers)       |
|                                                                                |
|  [ Object A ]      [ Database Page B ]      [ Program C ]     [ User Buffer D] |
+--------------------------------------------------------------------------------+
                                       |
                   SLIC Virtual Memory & Page Fault Engine
                                       |
     +---------------------------------+---------------------------------+
     |                                                                   |
     v                                                                   v
+-----------------------+                               +------------------------+
| Physical RAM (Cache)  | <---- Transparent Paging ---> | Physical Disks / NVMe  |
+-----------------------+                               +------------------------+
```

### Architectural Principles of Single-Level Store

1. **Unified Address Space**: Every object, program, database record, and variable resides at a unique, permanent virtual address within a monolithic 64-bit (and structurally 128-bit) address space.
2. **Elimination of Explicit File I/O**: Applications do not issue `open()`, `read()`, `write()`, or `close()` system calls to manipulate disk files. Programs simply reference the memory address of an object or record. If the target page is in physical RAM, access is instantaneous. If the page resides on physical disk, the hardware and SLIC generate a page fault, retrieve the 4KB/64KB block from disk, map it into RAM, and resume execution transparently.
3. **Object Persistence**: Storage allocation is permanent by default. An object created at virtual address `0x0000 7FFF 8000 1234` retains that address across system reboots, disk migrations, and hardware upgrades.
4. **Physical Storage Agnosticism**: Disk drives are treated merely as non-volatile paging space for the single-level store. Adding new disk drives to an AS/400 automatically expands the global virtual address space pool without requiring drive formatting, volume mounting, or partition resizing.

---

## Integrated Database & Work Management

### DB2 for OS/400 / IBM i

Unlike general-purpose operating systems where relational database systems (Oracle, DB2, PostgreSQL) are installed as separate software applications, the AS/400 database is integrated into the operating system and TIMI interface.

* **Physical Files (`*FILE PF`)**: Represent raw relational data tables containing field-level definitions and physical record rows.
* **Logical Files (`*FILE LF`)**: Represent indexed views, multi-table joins, or filtered subsets of physical files. Indices (Access Paths) are maintained automatically by SLIC microcode in real time upon record modification.
* **Record-Level Access (RLA)**: RPG and COBOL programs access database records directly via native language verbs (`CHAIN`, `READ`, `READE`, `WRITE`, `UPDATE`), bypassing SQL parser overhead for high-throughput batch transaction processing.

### Work Management & Subsystems

OS/400 abandons flat process management in favor of structured Work Management:
* **Jobs**: The basic unit of execution (similar to a process/thread context).
* **Subsystems (`*SBSD`)**: Independent operating environments that manage job memory pools, concurrency limits, and processing priorities. Examples:
  * `QINTER`: Manages interactive display terminal sessions.
  * `QBATCH`: Manages background transaction batch jobs.
  * `QSERVER`: Manages database client/server connections and network API requests.
* **Job Queues (`*JOBQ`)**: Buffer batch workloads before dispatching them into subsystems.

---

## Languages, Program Objects & Runtimes

### Platform Language Hierarchy

The primary programming environments on AS/400 are deeply tied to platform contracts:

1. **RPG (Report Program Generator - RPG III, RPG IV / ILE RPG)**: The standard language for business logic. RPG IV incorporates free-format syntax, strong typing, and direct integration with database record structures.
2. **COBOL (ANSI 85 / ILE COBOL)**: Enterprise financial and transaction processing.
3. **Control Language (CL)**: The command/scripting language used to control system operations, manage objects, invoke programs, and manipulate job queues.
4. **C/C++ & Java**: Supported in modern releases via the Integrated Language Environment (ILE).

### Program Architecture: EPM vs. ILE

* **Original Program Model (EPM)**: Monolithic program objects where each program contained its own imports, exports, and call stacks.
* **Integrated Language Environment (ILE) (1994)**: Introduced modular compilation. Source code compiles into Modules (`*MODULE`), which are bound into Program Objects (`*PGM`) or Service Programs (`*SRVPGM`, the OS/400 equivalent of DLLs/shared libraries). ILE enables language interoperability—an RPG IV module can call a C module or COBOL module within the same execution stack.

---

## Hardware Transitions (incl. CISC→RISC)

The hardware history of the AS/400 is characterized by radical instruction set transformations executed underneath a completely stable TIMI interface.

```
       1988                     1995                    2001                   2024
+-----------------+      +-----------------+      +---------------+      +---------------+
| Custom 48-bit   |      | 64-bit PowerPC  |      | IBM POWER4    |      | IBM POWER10   |
| IMPI CISC CPUs  | ---> | AS RISC (A10)   | ---> | Convergence   | ---> | High-Density  |
| Multi-Chip Board|      | Monolithic Die  |      | Dual-Core SMP |      | Multi-Threaded|
+-----------------+      +-----------------+      +---------------+      +---------------+
         |                        |                       |                      |
         +------------------------+-----------------------+----------------------+
                                  |
            Decoupled via Technology Independent Machine Interface (TIMI)
```

### Key Hardware Architectural Milestones

1. **Custom 48-Bit IMPI CISC Era (1988–1995)**:
   * Architecture derived from System/38.
   * Utilized custom IBM multi-chip CPU modules.
   * Internal registers were 48 bits wide to natively support 48-bit single-level store pointers.

2. **PowerPC AS 64-Bit RISC Era (1995–2001)**:
   * Joint development between IBM Rochester and IBM Austin.
   * Extended standard PowerPC RISC instruction sets with 64-bit address tagging and capability checking registers.
   * Code-named "Muskie" (A10) and "Pulsar" (A30).

3. **POWER Microprocessor Convergence (2001–Present)**:
   * IBM consolidated its server lines (pSeries/AIX and iSeries/OS/400) onto a single physical processor family: IBM POWER processors.
   * Hardware virtualization (PowerVM / LPAR) allowed IBM i, AIX, and Linux to execute concurrently on the same physical silicon.

---

## Ecosystem Lock-In

The AS/400 created one of the most powerful and durable ecosystem lock-in mechanisms in computing history.

```text
       TIMI & Object OS Contracts
                   |
                   v
   Application Written in RPG/COBOL/CL
                   |
                   v
  Deep Integration with Physical/Logical Files
                   |
                   v
 Operational Dependencies (Subsystems, Job Queues, *USRPRF)
                   |
                   v
 Absolute Zero Rewrite Cost on Platform UPGRADES
                   |
                   v
 High Migration Cost to Unix/Windows/Linux (Require 100% Code Rewrite)
                   |
                   v
 Extreme Enterprise Persistence (Decades-Long Platform Lock-In)
```

### Mechanics of Platform Gravity

1. **Zero Migration Cost Upstream**: Upgrading from an AS/400 B10 to an iSeries to a POWER10 server required zero code rewrites or application re-architecting. Applications compiled in 1989 continued to run with improved performance on each new processor generation.
2. **Infinite Migration Cost Cross-Platform**: Porting an AS/400 application stack to Unix, Linux, or Windows required rewriting:
   * The database access layer (converting native Record Level Access to SQL).
   * The user interface (converting 5250 green-screen datastreams to GUI/Web).
   * The job execution framework (converting CL scripts and subsystems to shell scripts or systemd).
3. **Integrated Skills Investment**: IT operations staff and business developers specialized in RPG, CL, DDS, and DB2 for OS/400, creating deeply entrenched organizational capabilities centered around the platform.

---

## Limits, Market Niche & Persistence

### Technical & Market Limitations

Despite its architectural brilliance, the AS/400 platform encountered structural boundaries that restricted its expansion beyond enterprise business processing:

1. **Proprietary Hardware/Software Coupling**: For decades, OS/400 executed exclusively on proprietary IBM hardware. Customers could not license OS/400 to run on commodity x86 hardware, limiting its market footprint compared to Unix and Linux.
2. **5250 Terminal UI Paradigm**: The platform's user interaction model was built around the IBM 5250 block-mode terminal protocol. As web interfaces and rich client-server GUIs emerged in the 1990s, AS/400 applications were perceived as antiquated "green-screen" legacy systems.
3. **Record-Oriented Programming Bias**: RPG and RLA were optimized for structured, tabular business records. The platform struggled to gain adoption for scientific computing, un-structured text processing, or real-time graphic workloads.
4. **Talent Pipeline Contraction**: Educational institutions shifted computer science curricula to C, C++, Java, and Unix. RPG and OS/400 administration became specialized niche disciplines, creating a workforce aging constraint for enterprise deployment.

---

## Constraint Migration

The evolution of design constraints across the AS/400 lineage highlights how computational trade-offs shifted over four decades:

```
1970s / 1980s Constraints                  2000s / 2020s Constraints
+------------------------------------+      +------------------------------------+
| - High Cost of Memory (RAM)        |      | - Open-Systems Interoperability    |
| - Rapid CPU Hardware Obsolescence  | ---> | - Web API / REST Integration       |
| - Manual Software Migration Cost   |      | - Cloud Virtualization & LPARs     |
| - Separate File & Database Tooling |      | - Developer Talent & Skill Pipeline|
+------------------------------------+      +------------------------------------+
                 |                                             |
                 v                                             v
  AS/400 Solution (1988)                         IBM i Evolution (2024)
  - Single-Level Store                           - Native Java, Node.js, Python Runtimes
  - TIMI Intermediate Representation             - Open Source Package Ecosystem (Yum/RPM)
  - Kernel-Integrated DB2                        - SQL / REST / Web Service Interfaces
  - RPG III / DDS Record Access                  - PowerVM Cloud Partitions
```

---

## Recurring Ideas

The architectural principles pioneered by the AS/400 lineage continue to resurface in modern computing frameworks:

1. **Virtual Machine Intermediate Code**: TIMI laid the conceptual groundwork for modern managed runtimes. WebAssembly (Wasm), Java Bytecode (JVM), and Microsoft CIL (.NET) all reflect the TIMI principle of decoupling high-level application code from host CPU microarchitectures.
2. **Persistent Memory & CXL Addressing**: Modern Compute Express Link (CXL) hardware architectures and Non-Volatile Dual In-line Memory Modules (NVDIMMs) are reviving interest in Single-Level Store models, seeking to unify system RAM and persistent storage into a single address space.
3. **Capability-Based Hardware Security**: ARM Morello and CHERI (Capability Hardware Enhanced RISC Instructions) introduce tagged architecture memory pointers to enforce spatial and temporal memory safety at the CPU register level—a direct physical continuation of the tagged memory architecture used in System/38 and PowerPC AS.

---

## Comparative Analysis

| Dimension | IBM AS/400 (IBM i) | Unix / Linux | IBM System/370 / Mainframe | Intel x86 Protected Mode |
| :--- | :--- | :--- | :--- | :--- |
| **Machine Interface** | TIMI (High-Level Intermediate Representation) | Physical CPU ISA (x86_64, ARM, RISC-V) | System/370 / z/Architecture ISA | Physical x86 Machine Code |
| **Storage Model** | Single-Level Store (64/128-bit) | Two-Level Store (RAM vs. File System) | Disk Datasets (MVS) / Files | Two-Level Store (Paged Virtual RAM + Files) |
| **Resource Model** | Strongly-Typed System Objects (`*PGM`, `*LIB`) | Untyped Byte-Stream Files & Process IDs | Datasets, PDS, JCL Execution | Raw Files, Pointers, Process Handles |
| **Database Integration**| Native DB2 Kernel Substrate | User-Space Middleware (PostgreSQL, MySQL) | User-Space Subsystems (IMS, DB2 for z/OS) | External Application Middleware |
| **Compatibility Strategy**| Automatic TIMI Retranslation across ISAs | Source Code Recompilation or Emulation | Strict Binary Microcode ISA Back-Compatibility | Hardware Microcode Back-Compatibility |
| **Security Architecture**| Pointer Tagging + Object Authority Checks | POSIX Permissions / ACLs / SELinux | RACF / System Storage Keys | Page Ring Protection (Ring 0-3) |

---

## Modern Relevance

Today, the AS/400 lineage lives on as **IBM i** executing on IBM POWER10 hardware inside global enterprises.

* **Core Enterprise Infrastructure**: Thousands of global banks, logistics corporations, retail giants, and manufacturing firms continue to run core transaction backbones on IBM i.
* **Hybrid Runtime Architecture**: Modern IBM i partitions support dual execution environments:
  1. **Native Object Domain**: Running traditional RPG IV, CL, DB2, and TIMI-translated application objects.
  2. **PASE (Portable Application Solutions Environment)**: An AIX runtime environment within IBM i executing native IBM POWER ELF binaries, enabling Python, Node.js, C++, and open-source tooling to run directly alongside traditional DB2 business objects.

---

## Reconstruction Proposal

To demonstrate the foundational principles of the AS/400 architecture, we specify a zero-dependency Python simulator located in `reconstructions/ibm_as400_timi/as400_sim.py` with an accompanying test suite in `reconstructions/ibm_as400_timi/test_as400_sim.py`.

### Simulator Architectural Requirements

1. **TIMI Code Representation & Compiler**:
   * Models an abstract TIMI intermediate instruction set with typed arithmetic, database cursor operations, and object references.
   * Compiles abstract TIMI instructions into two native backends: **CISC 48-bit IMPI Assembly** and **RISC 64-bit PowerPC Assembly**.
2. **Automatic Retranslation Engine**:
   * Simulates host hardware processor shifts.
   * When a program compiled for CISC executes on a simulated RISC host, the SLIC retranslation engine automatically compiles the TIMI intermediate template into RISC instructions without modifying application logic.
3. **Single-Level Store (SLS) Memory Engine**:
   * Implements a 64-bit flat virtual memory address space.
   * Automatically handles page faulting between simulated volatile RAM and persistent backing disk storage.
4. **Typed Object System & Authority Control**:
   * Encapsulates system entities as typed objects (`*PGM`, `*LIB`, `*FILE`, `*USRPRF`).
   * Enforces object authority security checks during library resolution and program invocation.
5. **Integrated Relational Database Engine**:
   * Implements Physical Files (schema definitions and raw data rows) and Logical Files (filtered and indexed views).

---

## Knowledge-Graph Relationships

```text
IBM_AS400 -> inherits_from -> System_38
IBM_AS400 -> implements -> TIMI
IBM_AS400 -> implements -> Single_Level_Store
IBM_AS400 -> integrates -> DB2_for_OS400
IBM_AS400 -> provides -> Object_Based_OS_Model
TIMI -> enables -> Binary_Compatibility_Across_ISAs
TIMI -> insulates_from -> Physical_Hardware_Changes
IBM_i -> continues -> IBM_AS400
IBM_AS400 -> contrasts_with -> Unix_Process_File_Model
```

---

## Research Questions

1. How did the performance overhead of TIMI intermediate translation compare to native compilation in early 1988 hardware implementations, and at what point did CPU instruction cache scaling make TIMI compilation overhead negligible?
2. To what degree did tag-protected physical memory pointers inspire modern CPU hardware capability extensions such as ARM Morello and CHERI?
3. Could a modern operating system adopt a Single-Level Store model backed by CXL persistent memory while maintaining compatibility with POSIX file system expectations?

---

## Limitations and Uncertainties

* **Proprietary Licensed Internal Code Internals**: Exact register allocation strategies and internal optimization passes inside SLIC's microcode translator remain proprietary IBM intellectual property.
* **Early System/38 Hardware Benchmarks**: Quantitative microarchitectural benchmark datasets comparing raw System/38 hardware throughput against equivalent IBM System/370 configurations under real-world transaction loads are limited in public systems literature.

---

## Bibliography

1. Soltis, F. G. (1996). *Inside the AS/400*. Duke Press.
2. Soltis, F. G. (1981). *Design principles of the System/38*. IBM Systems Journal, 20(3), 269–286.
3. Frank, A. J., & Ricketts, I. W. (1989). *The IBM AS/400 architecture and strategy*. Computer Communications, 12(6), 346–352.
4. IBM Corporation. (1998). *AS/400 Technology Independent Machine Interface Architecture Reference*. IBM Publication GA19-5011.
5. IBM Corporation. (2000). *OS/400 Work Management Guide*. IBM Redbooks.
6. Levy, H. M. (1984). *Capability-Based Computer Systems*. Digital Press.

---

## Excavation Scorecard

| Category | Rating | Rationale |
| :--- | :--- | :--- |
| Historical Importance | ★★★★★ | Pioneered technology-independent software execution, single-level store, and integrated OS database systems at enterprise scale. |
| Technical Innovation | ★★★★★ | Elegant layered machine design decoupling application code from hardware via TIMI and tagged capability memory pointers. |
| Commercial Success | ★★★★★ | Generated hundreds of billions in enterprise revenue and served as the computing backbone for global business for over 35 years. |
| Modern Potential | ★★★★☆ | Single-Level Store and capability-based memory addressing are directly relevant to CXL persistent memory and CHERI security. |
| AI Synergy | ★★★☆☆ | DB2 record access and structured object management provide reliable transaction baselines for enterprise AI agent integration. |
| Difficulty to Recreate | ★★★★☆ | Recreating the full stack requires modeling TIMI compilation, Single-Level Store memory paging, object namespaces, and database access paths. |
