# Circuit Architecture & Theoretical Derivations

This document presents the complete architectural breakdown, sub-block schematics, governing equations, and design methodology for the CMOS ECG Analog Front-End (AFE) IC.

---

## 1. System Block Diagram

The complete AFE integrated circuit processes bio-potential signals captured from electrodes placed on the human body. The signal flow is structured as follows:

```
[ Human Body Model ] ──► [ Instrumentation Amplifier ] ──► [ HPF / LPF / Notch Filters ] ──► [ Two-Stage OTA ] ──► Output
         ▲                                                                                              │
         └───────────────────────── [ DRL Circuit ] ◄───────────────────────────────────────────────────┘
```

---

## 2. Two-Stage Operational Transconductance Amplifier (OTA)

### 2.1 Topology & Sizing Rationale
The core amplification stage is a two-stage CMOS Operational Transconductance Amplifier.
- **First Stage:** PMOS differential pair ($M_7, M_8$) with NMOS active current mirror load ($M_0, M_1$).
- **Second Stage:** NMOS common-source amplifier ($M_3$) with PMOS active current-source load ($M_{10}, M_{11}$).
- **Frequency Compensation:** Miller capacitor ($C_c$) connected across the second stage.

### 2.2 Voltage Gain Derivation
The total low-frequency voltage gain $A_v$ is given by the product of the first-stage gain ($A_{v1}$) and second-stage gain ($A_{v2}$):

$$A_{v1} = g_{m1} \cdot r_{o1}$$
$$A_{v2} = g_{m2} \cdot r_{o2}$$
$$A_v = A_{v1} \cdot A_{v2} = (g_{m1} \cdot r_{o1})(g_{m2} \cdot r_{o2})$$

where:
- $g_{m1} = g_{m7,8}$ is the transconductance of the PMOS input differential pair.
- $r_{o1} = r_{o8} \parallel r_{o1}$ is the output resistance of the first stage.
- $g_{m2} = g_{m3}$ is the transconductance of the second-stage NMOS driver.
- $r_{o2} = r_{o3} \parallel r_{o11}$ is the output resistance of the second stage.

### 2.3 Sub-Threshold Biasing
To minimize power consumption for wearable devices, transistors are biased in the sub-threshold (weak inversion) region:

$$g_m = \frac{I_D}{n V_T}$$

where $V_T = \frac{k T}{q} \approx 25.9\text{ mV}$ at 300K, and $n$ is the sub-threshold slope factor ($1 < n < 1.5$). In saturation (strong inversion):

$$g_m = \sqrt{2 \mu C_{ox} \frac{W}{L} I_D}$$

Increasing the $\frac{W}{L}$ ratio of the input pair increases $g_m$ and voltage gain without increasing drain current $I_D$.

### 2.4 Noise Performance
Flicker noise ($1/f$ noise) dominates at low ECG frequencies (0.5 Hz to 100 Hz). The flicker noise voltage power spectral density is expressed as:

$$V_n^2 = \frac{K}{C_{ox} W L f}$$

To suppress flicker noise:
1. PMOS devices ($M_7, M_8$) are chosen for the differential input pair due to their lower hole-trap density ($K_{PMOS} < K_{NMOS}$).
2. Input transistor area ($W \times L$) is maximized.

### 2.5 Unity Gain Bandwidth (GBW)
With Miller compensation capacitor $C_c$, the dominant pole is positioned at the first stage output, yielding:

$$\text{GBW} = \frac{g_{m1}}{2\pi C_c}$$

---

## 3. Instrumentation Amplifier (IA) Stage

### 3.1 Capacitive Feedback Architecture
The IA provides high input impedance and precise closed-loop gain control using capacitive feedback:

$$A_v = \frac{C_1}{C_f}$$

where $C_1$ is the input coupling capacitor and $C_f$ is the feedback capacitor. Input capacitors $C_1$ block DC electrode offset voltages.

### 3.2 Pseudo-Resistor Implementation
Pseudo-resistors ($R_f$) implemented via MOS transistors in off-state provide sub-hertz lower cutoff frequency $f_L$:

$$f_L = \frac{1}{2\pi R_f C_f}$$

With $R_f \sim \text{T}\Omega$ and $C_f \sim \text{pF}$, $f_L < 0.5\text{ Hz}$ is achieved.

### 3.3 Input-Referred Noise
The input-referred noise power of the instrumentation amplifier is given by:

$$V_{n,in}^2 = \left( \frac{C_1 + C_f + C_{par}}{C_1} \right)^2 V_{n,ota}^2$$

where $C_{par}$ represents parasitic capacitance at the OTA input terminals.

---

## 4. Driven Right Leg (DRL) Circuit

### 4.1 Common-Mode Rejection Enhancement
The DRL circuit detects common-mode noise ($V_{cm,in}$) present at the differential inputs, amplifies and inverts it with gain $-A_{DRL}$, and injects it back to the human body via a third electrode:

$$V_{cm,out} = \frac{V_{cm,in}}{1 + A_{DRL}}$$

This active feedback suppresses 50 Hz power-line hum and increases total CMRR:

$$\text{CMRR} = 20 \log_{10} \left( \frac{A_d}{A_{cm}} \right)$$

Simulated values achieve $A_d = 79.54\text{ dB}$, $A_{cm} = -34.00\text{ dB}$, yielding $\text{CMRR} = 113.54\text{ dB}$.

### 4.2 Patient Safety
A current-limiting protection resistor $R_{prot}$ is placed in series with the DRL electrode output:

$$I_{body} = \frac{V_{DD}}{R_{prot}} \le 10\ \mu\text{A}$$

---

## 5. Filtering Stages

### 5.1 Bandpass Response
- **High-Pass Filter (HPF):** First-order RC network, $f_c = \frac{1}{2\pi R_{HPF} C_{HPF}} \approx 0.5\text{ Hz}$. Removes baseline drift.
- **Low-Pass Filter (LPF):** First-order active RC network, $f_c = \frac{1}{2\pi R_{LPF} C_{LPF}} \approx 100\text{ Hz}$. Attenuates high-frequency noise.

### 5.2 50 Hz Notch Filter
A 2nd-order active notch filter rejects power-line interference. Transfer function $H(s)$:

$$H(s) = \frac{s^2 + \omega_0^2}{s^2 + \frac{\omega_0}{Q} s + \omega_0^2}$$

where $\omega_0 = 2\pi \times 50\text{ rad/s}$ and $Q$ is the quality factor controlling notch selectivity.

---

## 6. Body Impedance Model

Instead of an ideal AC voltage source, an equivalent electrical model of human skin and tissue impedance is placed at the input:

- $R_s$: Tissue resistance ($\approx 500\ \Omega$)
- $R_{p1}, C_{p1}, R_{p2}, C_{p2}$: Skin-electrode interface parallel impedance ($R_p \approx 50\text{ k}\Omega$, $C_p \approx 10\text{ nF}$)

This provides realistic input loading during simulations.
