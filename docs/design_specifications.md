# Design Specifications & Electrical Parameters

This document details the target design specifications, simulated metrics, and operating conditions for the **Low-Power Low-Noise CMOS ECG Analog Front-End (AFE) IC**.

## 1. Operating Environment & Supply Parameters

| Parameter | Symbol | Value | Unit | Description |
| :--- | :--- | :--- | :--- | :--- |
| Technology Node | - | 180 | nm | Standard CMOS Process |
| Supply Voltage | $V_{DD}$ | 1.8 | V | Core analog supply |
| Ground | $V_{SS}$ / GND | 0.0 | V | System Reference |
| Common-Mode Input | $V_{CM,in}$ | 0.9 | V | Mid-rail bias ($V_{DD}/2$) |
| Operating Temperature | $T$ | 27 (300K) | °C | Room temperature nominal |

---

## 2. Key Performance Metrics Summary

| Specification | Parameter | Simulated Value | Target / Requirement | Unit |
| :--- | :--- | :--- | :--- | :--- |
| Differential Midband Gain | $A_d$ | **79.54** | $\ge 70.0$ | dB |
| Common-Mode Gain | $A_{cm}$ | **-34.00** | $\le -20.0$ | dB |
| Common-Mode Rejection Ratio | CMRR | **113.54** | $\ge 100.0$ | dB |
| AC System Bandwidth (-3dB) | BW | **198.4 mHz to 34 kHz** | 0.5 Hz to 10 kHz | - |
| Clinical ECG Passband | $f_{cardiac}$ | **0.5 to 100** | 0.5 to 100 | Hz |
| Unity Gain Frequency | $f_{u}$ | **28.557** | $\approx 30.0$ | kHz |
| Gain-Bandwidth Product | GBW | **323** | $\ge 100$ | MHz |
| Slew Rate | SR | **0.145** | $\ge 0.10$ | V/$\mu$s |
| Power-Line Rejection | $f_{notch}$ | **50.0** | 50.0 | Hz |
| Input-Referred Noise | $V_{n,in}$ | Low flicker noise | $\le 10$ | $\mu\text{V}_{\text{rms}}$ |

---

## 3. Sub-Block Electrical Specifications

### 3.1 Two-Stage Operational Transconductance Amplifier (OTA)
- **Input Pair:** PMOS Differential Pair ($M_7, M_8$) operated in sub-threshold / weak inversion region to maximize $g_m / I_D$ ratio and minimize flicker noise.
- **Active Load:** NMOS Load ($M_0, M_1$) with elongated channel length ($L$) to boost output resistance ($R_{o1}$).
- **Second Stage:** NMOS Common-Source ($M_3$) with PMOS active current source load ($M_{10}, M_{11}$).
- **Bias Network:** PMOS reference mirror ($M_{12}$) with extended channel length to suppress channel-length modulation ($\lambda$).
- **Frequency Compensation:** Miller Compensation Capacitor ($C_c$) providing dominant pole compensation and stable phase margin.

### 3.2 Instrumentation Amplifier (IA)
- **Gain Topology:** Capacitive feedback midband gain ($A_v = C_1 / C_f$).
- **DC Rejection:** Capacitive isolation at input ($C_1$) eliminates DC electrode offset voltage.
- **Pseudo-Resistors ($R_f$):** MOS transistors biased in cut-off state yielding Tera-ohm ($\text{T}\Omega$) equivalent resistance to establish lower cutoff frequency ($f_L = \frac{1}{2\pi R_f C_f} \approx 0.5\text{ Hz}$).

### 3.3 Driven Right Leg (DRL) Circuit
- **Function:** Active common-mode noise suppression via negative feedback back to body tissue.
- **Common-Mode Reduction:** $V_{cm,out} = \frac{V_{cm,in}}{1 + A_{DRL}}$.
- **Patient Safety:** Protection resistor ($R_{prot}$) limits maximum injection current to $I = \frac{V_{DD}}{R_{prot}} < 10\ \mu\text{A}$.
- **Loop Stability:** Integration of stabilization feedback capacitor to maintain phase margin.

### 3.4 Filter System
- **High-Pass Filter (HPF):** Cutoff $f_{c,HPF} \approx 0.5\text{ Hz}$ to eliminate baseline wander and electrode movement artifacts.
- **Low-Pass Filter (LPF):** Cutoff $f_{c,LPF} \approx 100\text{ Hz}$ to attenuate high-frequency electromyographic (EMG) muscle noise and RF interference.
- **Notch Filter:** 2nd-order active notch tuned at $f_{0} = 50\text{ Hz}$ to reject power-line hum.

### 3.5 Body Modeling Network
- **Equivalent Circuit:** 2-terminal skin-tissue bio-impedance network (epidermis R-C parallel pairs + dermis/tissue series resistance).
- **Purpose:** Realistic bio-potential source modeling during Spectre transient and AC simulations.
