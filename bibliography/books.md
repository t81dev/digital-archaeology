# Seminal Books in Computing History & Architecture

This annotated bibliography lists key books that explore computer architecture, operating system design, programming languages, and historical hardware paradigms covered in the Digital Archaeology excavations.

---

### Computer Architecture & Hardware Systems

#### 1. *Computer Structures: Principles and Examples*
* **Authors**: Daniel P. Siewiorek, C. Gordon Bell, Allen Newell
* **Published**: McGraw-Hill, 1982
* **Relevance**: [Burroughs Large Systems](../excavations/burroughs-large-systems.md), [Vector Supercomputing](../excavations/vector-supercomputing.md), Stack Machines
* **Description**: A monumental compendium of historic computer architectures. It provides primary hardware specifications, block diagrams, and analyses of classic machines, illustrating the rich diversity of architecture before standard ISA commoditization.

#### 2. *The Connection Machine*
* **Author**: W. Daniel Hillis
* **Published**: MIT Press, 1985
* **Relevance**: [Connection Machine](../excavations/connection-machine.md), Cellular Automata Hardware
* **Description**: Based on Hillis's groundbreaking PhD thesis, this book outlines the architecture and philosophy of the Connection Machine. It explores massively parallel, fine-grained SIMD execution and hypercube routing networks.

#### 3. *Introduction to VLSI Systems*
* **Authors**: Carver Mead, Lynn Conway
* **Published**: Addison-Wesley, 1980
* **Relevance**: [Systolic Arrays](../excavations/systolic-arrays.md), Wafer-Scale Integration
* **Description**: The classic textbook that democratized custom silicon design. It contains foundational sections on systolic architectures, structured hardware design, and pipeline computation, laying the groundwork for modern specialized coprocessors.

---

### Operating Systems & Security

#### 4. *Capability-Based Computer Systems*
* **Author**: Henry M. Levy
* **Published**: Digital Press, 1984
* **Relevance**: [Capability Systems](../excavations/capability-systems.md), [Intel iAPX 432](../excavations/intel-iapx-432.md), [Multics](../excavations/multics.md)
* **Description**: The definitive survey of early hardware- and software-enforced capability systems. Levy provides structural reviews of the CAP computer, Hydra, the StarOS, and the Intel iAPX 432, detailing why fine-grained, unforgeable addressing failed to win commercially in the 1980s.

#### 5. *The Multics System: An Examination of Its Structure*
* **Author**: Elliott I. Organick
* **Published**: MIT Press, 1972
* **Relevance**: [Multics](../excavations/multics.md), Capability Systems
* **Description**: A comprehensive guide to the internal structure of Multics, focusing on its pioneering use of virtual memory, segmented addressing, and ring protection architectures.

---

### Programming Languages & Concurrency

#### 6. *Communicating Sequential Processes*
* **Author**: C.A.R. Hoare
* **Published**: Prentice Hall, 1985
* **Relevance**: [Transputers](../excavations/transputers.md), [Occam](../excavations/occam.md)
* **Description**: The mathematical and conceptual foundation for channel-based concurrency. Hoare outlines the CSP formal language, which directly inspired the INMOS Transputer, the Occam programming language, and modern concurrency models like Go channels.

#### 7. *Smalltalk-80: The Language and its Implementation*
* **Authors**: Adele Goldberg, David Robson
* **Published**: Addison-Wesley, 1983 (The "Blue Book")
* **Relevance**: [Smalltalk](../excavations/smalltalk.md), Lisp Machines
* **Description**: The authoritative description of the Smalltalk-80 virtual machine, compiler, and image-based runtime environment developed at Xerox PARC. It explains dynamic messaging, garbage collection, and object-oriented virtual hardware.

#### 8. *The Art of the Metaobject Protocol*
* **Authors**: Gregor Kiczales, Jim des Rivieres, Daniel G. Bobrow
* **Published**: MIT Press, 1991
* **Relevance**: [Lisp Machines](../excavations/lisp-machines.md), Smalltalk
* **Description**: A masterclass in language-runtime co-design. It describes the design of the Common Lisp Object System (CLOS) metaobject protocol, showing how programming languages can be made introspective, highly extensible, and adaptable.

---

### General Computing History & Case Studies

#### 9. *The Soul of a New Machine*
* **Author**: Tracy Kidder
* **Published**: Atlantic-Little, Brown, 1981
* **Relevance**: Mini-computers, VLIW/EPIC Architectures
* **Description**: A narrative non-fiction classic documenting the intense engineering effort to design Data General's Eclipse MV/8000 superminicomputer, highlighting the commercial pressure and engineering trade-offs of the era.

#### 10. *An Introduction to Ternary Computer Design*
* **Authors**: Albert S. Deng, etc.
* **Relevance**: [Balanced Ternary](../excavations/balanced-ternary.md)
* **Description**: A modern look at ternary arithmetic, ternary logic gates, and the design of non-binary computing circuits, illustrating the theoretical density advantages of base-3 arithmetic.
