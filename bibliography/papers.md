# Landmark Research Papers

This annotated bibliography contains foundational research papers, technical reports, and academic publications that introduced or analyzed key technologies documented in our excavations.

---

### Non-Von Neumann & Parallel Architectures

#### 1. *Communicating Sequential Processes*
* **Author**: C. A. R. Hoare
* **Journal**: *Communications of the ACM (CACM)*, Volume 21, Issue 8, August 1978
* **Relevance**: [Transputers](../excavations/transputers.md), [Occam](../excavations/occam.md)
* **Description**: The classic paper that introduced Communicating Sequential Processes (CSP). It proposed that concurrency and input/output channels should be treated as fundamental programming language primitives, directly inspiring the OCCAM language and INMOS hardware.

#### 2. *The Manchester Prototype Dataflow Computer*
* **Authors**: J. R. Gurd, C. C. Kirkham, I. Watson
* **Journal**: *Communications of the ACM (CACM)*, Volume 28, Issue 1, January 1985
* **Relevance**: [Dataflow Computing](../excavations/dataflow-computing.md)
* **Description**: A comprehensive technical overview of the Manchester Dataflow Machine, detailing its tagged-token execution model, hardware layout, and performance on streaming data.

#### 3. *Systolic Architectures for VLSI*
* **Authors**: H. T. Kung, Charles E. Leiserson
* **In**: *Introduction to VLSI Systems* (Mead & Conway), 1980
* **Relevance**: [Systolic Arrays](../excavations/systolic-arrays.md)
* **Description**: The landmark publication that introduced the concept of systolic arrays. It describes how data can be "pumped" rhythmically through a regular network of simple processing elements to achieve highly efficient matrix computations.

#### 4. *The Connection Machine (Computer Architecture)*
* **Author**: W. Daniel Hillis
* **Journal**: *IEEE Transactions on Computers*, Volume C-34, 1985
* **Relevance**: [Connection Machine](../excavations/connection-machine.md)
* **Description**: Hillis's seminal paper outlining the engineering challenges and communication routing mechanisms of a 65,536-node SIMD supercomputer.

---

### Systems, Memory Models & Security

#### 5. *The Protection of Information in Computer Systems*
* **Authors**: Jerome H. Saltzer, Michael D. Schroeder
* **Journal**: *Proceedings of the IEEE*, Volume 63, Issue 9, September 1975
* **Relevance**: [Multics](../excavations/multics.md), [Capability Systems](../excavations/capability-systems.md)
* **Description**: A classic system security paper outlining design principles for secure operating systems, drawing heavily on lessons from Multics and early descriptor-based memory protection.

#### 6. *Capability-Based Computer Systems*
* **Author**: Henry M. Levy
* **Published**: ACM Digital Library, 1984
* **Relevance**: [Capability Systems](../excavations/capability-systems.md), [Intel iAPX 432](../excavations/intel-iapx-432.md)
* **Description**: Explains the theory of capabilities as unforgeable hardware-enforced addressing structures, contrasting object-capabilities with standard ACL security models.

#### 7. *Plan 9 from Bell Labs*
* **Authors**: Rob Pike, Dave Presotto, Ken Thompson, Howard Trickey
* **Journal**: *Computing Systems*, Volume 8, Issue 3, Summer 1995
* **Relevance**: [Plan 9](../excavations/plan-9.md), [Inferno](../excavations/inferno.md)
* **Description**: The primary paper introducing Plan 9, describing its unified distributed resource model where files, devices, and connections are represented uniformly in a single name space via the 9P (Styx) protocol.

---

### Hardware, Physics & Mathematics

#### 8. *Irreversibility and Heat Generation in the Computing Process*
* **Author**: Rolf Landauer
* **Journal**: *IBM Journal of Research and Development*, Volume 5, Issue 3, 1961
* **Relevance**: [Reversible Computing](../excavations/reversible-computing.md)
* **Description**: Introduces "Landauer's Principle", proving that any logically irreversible operation (such as erasing a bit) must dissipate a minimum amount of thermodynamic energy ($k T \ln 2$), establishing the physical foundation for reversible and adiabatic computing.

#### 9. *A Ternary Computer: Setun*
* **Authors**: N. P. Brousentsov, S. P. Maslov, V. P. Rozin, A. M. Tishulina
* **Published**: Moscow State University Bulletin, 1960 (Translated to English)
* **Relevance**: [Balanced Ternary](../excavations/balanced-ternary.md)
* **Description**: Technical overview of the Setun computer, the only known commercially manufactured balanced ternary computer, describing its use of dual-state magnetic cores to represent base-3 digits.

#### 10. *Silicon Brains: Neuromorphic Microchips*
* **Author**: Carver Mead
* **Journal**: *Proceedings of the IEEE*, Volume 78, Issue 10, October 1990
* **Relevance**: [Neuromorphic Hardware](../excavations/neuromorphic-hardware.md)
* **Description**: A foundational paper for neuromorphic engineering. Mead describes how analog subthreshold CMOS circuits can naturally model the biophysics of biological neurons and synapses, bypassing standard digital von Neumann limits.
