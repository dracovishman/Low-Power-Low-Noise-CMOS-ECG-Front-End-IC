# Transistor Sizing & Biasing Specifications

This document outlines the geometric sizing ($W/L$ ratios), multiplier factors, and operational roles for all MOS transistors in the two-stage OTA, Instrumentation Amplifier, Driven Right Leg (DRL) circuit, and filter stages.

---

## 1. Two-Stage OTA Transistor Sizing Table

All devices are designed for a 180nm ($L_{min} = 0.18\ \mu\text{m}$) CMOS technology node with $V_{DD} = 1.8\text{ V}$.

| Transistor | Type | Function / Role | Width ($W$) ($\mu\text{m}$) | Length ($L$) ($\mu\text{m}$) | $W/L$ Ratio | Optimization Objective |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **M7** | PMOS | Differential Input Pair (Positive) | 36.0 | 0.50 | 72.0 | High $g_m$, Low Flicker Noise ($1/f$) |
| **M8** | PMOS | Differential Input Pair (Negative) | 36.0 | 0.50 | 72.0 | High $g_m$, Low Flicker Noise ($1/f$) |
| **M0** | NMOS | First Stage Active Load (Left) | 12.0 | 1.00 | 12.0 | High output resistance $r_{o1}$, Matched |
| **M1** | NMOS | First Stage Active Load (Right) | 12.0 | 1.00 | 12.0 | High output resistance $r_{o1}$, Matched |
| **M2** | NMOS | Tail Current Source | 24.0 | 1.00 | 24.0 | Constant tail current bias ($I_{tail}$) |
| **M3** | NMOS | Second Stage Common-Source Driver | 48.0 | 0.50 | 96.0 | High output transconductance $g_{m2}$ |
| **M10** | PMOS | Second Stage Active Load Driver | 36.0 | 1.00 | 36.0 | High output resistance $r_{o2}$ |
| **M11** | PMOS | Second Stage Current Source | 36.0 | 1.00 | 36.0 | High output resistance $r_{o2}$ |
| **M12** | PMOS | Master Bias Reference Transistor | 18.0 | 2.00 | 9.0 | Low channel length modulation ($\lambda$) |

---

## 2. Passive Components & Compensation Parameters

| Component | Description | Parameter Value | Unit | Function |
| :--- | :--- | :--- | :--- | :--- |
| **$C_c$** | Miller Compensation Capacitor | 2.50 | pF | Dominant pole positioning, Phase margin stability |
| **$C_1$** | IA Input Coupling Capacitor | 10.0 | pF | Sets midband gain ($A_v = C_1/C_f$), DC blocking |
| **$C_f$** | IA Feedback Capacitor | 0.10 | pF | Controls feedback factor & midband gain |
| **$R_f$** | Pseudo-Resistor (MOS off-state) | $\sim 3.18 \times 10^{12}$ | $\Omega$ ($\text{T}\Omega$) | Establishes lower cutoff frequency $f_L \approx 0.5\text{ Hz}$ |
| **$R_{prot}$**| DRL Protection Resistor | 100 | k$\Omega$ | Patient safety protection (limits fault current) |
| **$C_{drl}$** | DRL Loop Stabilization Cap | 10.0 | pF | Prevents high-frequency oscillation in DRL loop |

---

## 3. Sub-Threshold Biasing Design Strategy

1. **Input Stage ($M_7, M_8$):** Large channel width ($W = 36\ \mu\text{m}$) and moderate length ($L = 0.5\ \mu\text{m}$) yield a high gate area ($W \times L = 18\ \mu\text{m}^2$), suppressing flicker noise. Biasing in sub-threshold maximizes transconductance efficiency:
   $$\frac{g_m}{I_D} = \frac{1}{n V_T} \approx 25\text{ to }30\ \text{V}^{-1}$$

2. **Active Loads ($M_0, M_1, M_{10}, M_{11}$):** Channel lengths are deliberately increased ($L = 1.0\ \mu\text{m} > L_{min}$) to minimize channel-length modulation parameter $\lambda$, maximizing transistor drain resistance $r_o = \frac{1}{\lambda I_D}$.

3. **Current Mirror ($M_{12}$):** Channel length is set to $L = 2.0\ \mu\text{m}$ to ensure precise current mirroring and immunity to supply variation.
