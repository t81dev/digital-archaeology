# Seminal Books in Computing History & Architecture

This annotated bibliography lists key books that explore computer architecture, operating system design, programming languages, and historical hardware paradigms covered in the Digital Archaeology excavations.

---

### Computer Architecture & Hardware Systems

#### 1. *Computer Structures: Principles and Examples*
* **Authors**: Daniel P. Siewiorek, C. Gordon Bell, Allen Newell
* **Published**: McGraw-Hill, 1982
* **Relevance**: [Burroughs Large Systems](../excavations/burroughs-large-systems.md), [Vector Supercomputing](../excavations/vector-supercomputing.md), [Stack Machines](../excavations/stack-machines.md)
* **Description**: A monumental compendium of historic computer architectures. It provides primary hardware specifications, block diagrams, and analyses of classic machines, illustrating the rich diversity of architecture before standard ISA commoditization.

#### 2. *The Connection Machine*
* **Author**: W. Daniel Hillis
* **Published**: MIT Press, 1985
* **Relevance**: [Connection Machine](../excavations/connection-machine.md), [Cellular Automata Hardware](../excavations/cellular-automata-hardware.md)
* **Description**: Based on Hillis's groundbreaking PhD thesis, this book outlines the architecture and philosophy of the Connection Machine. It explores massively parallel, fine-grained SIMD execution and hypercube routing networks.

#### 3. *Introduction to VLSI Systems*
* **Authors**: Carver Mead, Lynn Conway
* **Published**: Addison-Wesley, 1980
* **Relevance**: [Systolic Arrays](../excavations/systolic-arrays.md), [Wafer-Scale Integration](../excavations/wafer-scale-integration.md)
* **Description**: The classic textbook that democratized custom silicon design. It contains foundational sections on systolic architectures, structured hardware design, and pipeline computation, laying the groundwork for modern specialized coprocessors.

#### 4. *High Performance Computer Architecture*
* **Author**: Harold S. Stone
* **Published**: Addison-Wesley, 1987 (Second Edition 1990)
* **Relevance**: [Vector Supercomputing](../excavations/vector-supercomputing.md), [Systolic Arrays](../excavations/systolic-arrays.md)
* **Description**: A classic hardware textbook detailing vector processors, memory interleaving, cache coherency, and interconnection network topologies. It contrasts Cray-style vector pipelines with standard SISD architectures.

#### 5. *A VLSI Architecture for Concurrent Data Structures*
* **Author**: William J. Dally
* **Published**: Kluwer Academic Publishers, 1987
* **Relevance**: [The MIT J-Machine](../excavations/j-machine.md)
* **Description**: Outlines the design of low-latency message-passing communication networks and message-driven processors for massively parallel VLSI systems. This work formed the microarchitectural basis for the MIT J-Machine.

#### 6. *Stack Computers: The New Wave*
* **Author**: Philip J. Koopman, Jr.
* **Published**: Ellis Horwood, 1989
* **Relevance**: [Stack Machines](../excavations/stack-machines.md)
* **Description**: The definitive study of stack-oriented microprocessors (such as the Novix NC4016 and Harris RTX 2000). It analyzes their hardware simplicity, rapid context switching, and close fit with the Forth programming language.

#### 7. *Embedded Computing: A VLIW Approach to Architecture, Compilers and Tools*
* **Authors**: Joseph A. Fisher, Paolo Faraboschi, Cliff Young
* **Published**: Morgan Kaufmann, 2005
* **Relevance**: [VLIW / EPIC Architectures](../excavations/vliw-epic.md)
* **Description**: The definitive reference on VLIW processor design, co-authored by the pioneer of VLIW technology. It provides deep coverage of instruction-level parallelism, trace scheduling, and compiler-controlled execution pipelines.

#### 8. *Cellular Automata Machines: A New Environment for Modeling*
* **Authors**: Tommaso Toffoli, Norman Margolus
* **Published**: MIT Press, 1987
* **Relevance**: [Cellular Automata Hardware](../excavations/cellular-automata-hardware.md), [Reversible Computing](../excavations/reversible-computing.md)
* **Description**: Outlines the architecture, physics, and programming of special-purpose cellular automata hardware (CAM-6). It demonstrates how localized grid-based updating achieves massive parallel simulation speedups.

#### 9. *Wafer Scale Integration*
* **Author**: Earl E. Swartzlander Jr. (Editor)
* **Published**: Kluwer Academic Publishers, 1989
* **Relevance**: [Wafer-Scale Integration](../excavations/wafer-scale-integration.md)
* **Description**: A compilation of early wafer-scale integration research, focusing on defect tolerance, monolithic routing interconnects, and redundant block architectures to build systems spanning entire silicon wafers.

---

### Operating Systems & Security

#### 10. *Capability-Based Computer Systems*
* **Author**: Henry M. Levy
* **Published**: Digital Press, 1984
* **Relevance**: [Capability Systems](../excavations/capability-systems.md), [Intel iAPX 432](../excavations/intel-iapx-432.md), [Multics](../excavations/multics.md)
* **Description**: The definitive survey of early hardware- and software-enforced capability systems. Levy provides structural reviews of the CAP computer, Hydra, StarOS, and the Intel iAPX 432, detailing why fine-grained, unforgeable addressing failed to win commercially in the 1980s.

#### 11. *The Multics System: An Examination of Its Structure*
* **Author**: Elliott I. Organick
* **Published**: MIT Press, 1972
* **Relevance**: [Multics](../excavations/multics.md), [Capability Systems](../excavations/capability-systems.md)
* **Description**: A comprehensive guide to the internal structure of Multics, focusing on its pioneering use of virtual memory, segmented addressing, and ring protection architectures.

#### 12. *The Cambridge CAP Computer and its Operating System*
* **Authors**: Maurice V. Wilkes, Roger M. Needham
* **Published**: Elsevier North-Holland, 1979
* **Relevance**: [Capability Systems](../excavations/capability-systems.md)
* **Description**: Analyzes the hardware and software architecture of the CAP Computer, the first operational system to implement hardware capability-based memory protection with unforgeable capability registers.

#### 13. *The Design of the UNIX Operating System*
* **Author**: Maurice J. Bach
* **Published**: Prentice Hall, 1986
* **Relevance**: [Plan 9](../excavations/plan-9.md), [Multics](../excavations/multics.md)
* **Description**: Explains the internal mechanisms of classic UNIX file systems, process control, and character/block I/O, illustrating the architectural lineage that led to Plan 9's namespace and file-centric distributed system.

---

### Programming Languages & Concurrency

#### 14. *Communicating Sequential Processes*
* **Author**: C.A.R. Hoare
* **Published**: Prentice Hall, 1985
* **Relevance**: [Transputers](../excavations/transputers.md), [Occam](../excavations/occam.md)
* **Description**: The mathematical and conceptual foundation for channel-based concurrency. Hoare outlines the CSP formal language, which directly inspired the INMOS Transputer, the Occam programming language, and modern concurrency models like Go channels.

#### 15. *Smalltalk-80: The Language and its Implementation*
* **Authors**: Adele Goldberg, David Robson
* **Published**: Addison-Wesley, 1983 (The "Blue Book")
* **Relevance**: [Smalltalk](../excavations/smalltalk.md), [Lisp Machines](../excavations/lisp-machines.md)
* **Description**: The authoritative description of the Smalltalk-80 virtual machine, compiler, and image-based runtime environment developed at Xerox PARC. It explains dynamic messaging, garbage collection, and object-oriented virtual hardware.

#### 16. *The Art of the Metaobject Protocol*
* **Authors**: Gregor Kiczales, Jim des Rivieres, Daniel G. Bobrow
* **Published**: MIT Press, 1991
* **Relevance**: [Lisp Machines](../excavations/lisp-machines.md), [Smalltalk](../excavations/smalltalk.md)
* **Description**: A masterclass in language-runtime co-design. It describes the design of the Common Lisp Object System (CLOS) metaobject protocol, showing how programming languages can be made introspective, highly extensible, and adaptable.

#### 17. *LISP Machine Manual*
* **Authors**: Daniel Weinreb, David Moon
* **Published**: MIT Artificial Intelligence Laboratory, 1979
* **Relevance**: [Lisp Machines](../excavations/lisp-machines.md)
* **Description**: The foundational technical specification for the MIT CADR Lisp Machine, explaining hardware-supported tagging, dynamic memory representation, and stack frame organization tailored for dynamic symbolic execution.

#### 18. *Computer Organization and Programming: With an Emphasis on the Burroughs B5000/B6000 Series*
* **Author**: Elliott I. Organick
* **Published**: Academic Press, 1973
* **Relevance**: [Burroughs Large Systems](../excavations/burroughs-large-systems.md), [Stack Machines](../excavations/stack-machines.md)
* **Description**: The definitive textbook analyzing the stack-oriented, descriptor-based hardware architecture of the Burroughs B5000 and B6000 series, showing how hardware and high-level language compilers can be co-designed.

#### 19. *The Implementation of Functional Programming Languages*
* **Author**: Simon L. Peyton Jones
* **Published**: Prentice Hall, 1987
* **Relevance**: [Graph Reduction Machines](../excavations/graph-reduction-machines.md)
* **Description**: A comprehensive handbook outlining how to compile functional languages to graph reduction architectures. It covers combinator graph reduction, G-machines, and custom functional hardware pipelines.

#### 20. *How to Write Parallel Programs: A First Course*
* **Authors**: Nicholas Carriero, David Gelernter
* **Published**: MIT Press, 1990
* **Relevance**: [Linda Tuple Spaces](../excavations/linda-tuple-spaces.md)
* **Description**: The definitive textbook introducing Linda's generative communication model and coordinate-free tuple space operations, explaining how the tuple space paradigm enables decoupled parallel coordination.

---

### Physical, Mathematical & History Foundations

#### 21. *Feynman Lectures on Computation*
* **Author**: Richard P. Feynman (edited by Tony Hey and Robin W. Allen)
* **Published**: Addison-Wesley, 1996
* **Relevance**: [Reversible Computing](../excavations/reversible-computing.md)
* **Description**: Contains seminal lectures on reversible computing, conservative logic, and the physical limits of computation. Feynman analyzes how Fredkin gates and quantum-mechanical systems can compute without dissipating thermodynamic heat.

#### 22. *Computer Science and Multiple-Valued Logic: Theory and Applications*
* **Author**: David C. Rine (Editor)
* **Published**: North-Holland, 1977 (Revised Edition 1984)
* **Relevance**: [Balanced Ternary](../excavations/balanced-ternary.md)
* **Description**: The classic comprehensive reference on non-binary algebraic logic, circuit implementations, and multi-valued hardware design, providing a rigorous mathematical foundation for ternary computer engineering.

#### 23. *Principles of Superconductive Devices and Circuits*
* **Authors**: Theodore Van Duzer, Charles W. Turner
* **Published**: Prentice Hall, 1981 (Second Edition 1999)
* **Relevance**: [Superconducting & Cryogenic Microarchitectures](../excavations/superconducting-cryogenic.md)
* **Description**: The definitive textbook on Josephson junctions, superconducting transmission lines, and the electromagnetic physics that underpin single flux quantum (SFQ) logic.

#### 24. *Introduction to Fourier Optics*
* **Author**: Joseph W. Goodman
* **Published**: McGraw-Hill, 1968 (Second Edition 1996)
* **Relevance**: [Optical Computing](../excavations/optical-computing.md), [Analog Computing](../excavations/analog-computing.md)
* **Description**: The seminal textbook explaining the mathematical principles of wave optics and spatial filtering, which form the bedrock of continuous optical computing and holographic matrix processing.

#### 25. *The Soul of a New Machine*
* **Author**: Tracy Kidder
* **Published**: Atlantic-Little, Brown, 1981
* **Relevance**: [VLIW / EPIC Architectures](../excavations/vliw-epic.md)
* **Description**: A narrative non-fiction classic documenting the intense engineering effort to design Data General's Eclipse MV/8000 superminicomputer, highlighting the commercial pressure and engineering trade-offs of the era.
