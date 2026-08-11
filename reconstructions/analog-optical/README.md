# Continuous Analog & Optical Wave Accelerator Simulator

> *Continuous physical simulation modeling differential equations (using an op-amp computer) and matrix-vector multiplication (using a Mach-Zehnder Interferometer photonic tensor core).*

---

## Background

Traditional computing relies on discretizing math into binary values ($0$s and $1$s) processed sequentially in discrete clock cycles. While this guarantees high precision and deterministic repeatability, it requires massive power to overcome resistance and high-frequency clocking bottlenecks.

By contrast, **continuous computing** utilizes the natural laws of physics to process mathematical functions:
1. **Electronic [Analog Computing](../../excavations/analog-computing.md)**: Models mathematical integration and summation using continuous voltages and currents inside active operational amplifier (op-amp) feedback networks. Integration happens continuously over time through capacitor charge accumulation ($I = C \frac{dV}{dt}$).
2. **Coherent Optical (Photonic) Computing**: Performs matrix-vector multiplication at near-light-speed via constructive and destructive interference of laser beams passing through a mesh of **Mach-Zehnder Interferometers (MZIs)**.

---

## Mathematical Model

### 1. Electronic Analog Computer
We simulate an analog circuit patched to solve a second-order spring-mass-damper system:

$$\frac{d^2y}{dt^2} + 2\zeta \omega_n \frac{dy}{dt} + \omega_n^2 y = f(t)$$

* **State variables**: Displacement ($y$) and Velocity ($\frac{dy}{dt}$).
* **Hardware implementation**:
  - Integrator 1: Integrates Acceleration ($\frac{d^2y}{dt^2}$) to get Velocity.
  - Integrator 2: Integrates Velocity ($\frac{dy}{dt}$) to get Displacement.
  - Summer node: Computes the sum of damping, restoring spring forces, and external forcing function ($f(t)$).
* **Physical Constraints Modeled**:
  - **Thermal Noise**: Random voltage variations at junction points (white noise, $k_B T C$).
  - **Thermal Component Drift**: Gradual parameter drift over time as amplifiers heat up.
  - **Op-Amp Saturation**: Limits on maximum and minimum voltages (e.g., $\pm 10.0\text{ V}$).

### 2. Mach-Zehnder Interferometer Photonic Core
We simulate coherent laser light propagating through a 2x2 symmetric Mach-Zehnder Interferometer (MZI). The transfer matrix of a single MZI is:

$$U_{\text{MZI}}(\theta, \phi) = i \begin{pmatrix} e^{i\phi} \sin(\theta/2) & e^{i\phi} \cos(\theta/2) \\ \cos(\theta/2) & -\sin(\theta/2) \end{pmatrix}$$

By adjusting the micro-heater phase-shifters ($\theta, \phi$), the MZI can represent any arbitrary $2 \times 2$ unitary matrix operation.
* **Physical Constraints Modeled**:
  - **Laser RIN**: Relative Intensity Noise on the laser power.
  - **Phase Noise**: Thermal fluctuations in the MZI heaters.
  - **Photodetector Dark Current**: Signal offset/noise floor under dark conditions.
  - **Shot Noise**: Quantum fluctuations in the photodetector current.

---

## Execution Instructions

Navigate to the repository root directory and run:

```bash
# Run the Interactive Simulator
python3 reconstructions/analog-optical/analog_optical_sim.py
```

### Running Tests

This simulator includes complete unit tests verifying the mathematical equations and physical model behaviors:

```bash
# Run tests using pytest
pytest reconstructions/analog-optical/test_analog_optical_sim.py
```
