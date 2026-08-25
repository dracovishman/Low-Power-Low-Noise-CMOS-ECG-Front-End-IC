# Design & Optimization of a Low-Power Low-Noise CMOS ECG Front-End IC

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Technology](https://img.shields.io/badge/CMOS-180nm-blue.svg)](docs/design_specifications.md)
[![Cadence Virtuoso](https://img.shields.io/badge/Cadence-Virtuoso%20%2F%20Spectre-green.svg)](netlists/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)](src/)

This repository contains the complete design, Cadence Spectre SPICE netlists, transistor sizing specs, architectural documentation, and Python analytical verification models for a **Low-Power, Low-Noise CMOS Analog Front-End (AFE) Integrated Circuit (IC)** tailored for Electrocardiogram (ECG) bio-signal acquisition in wearable biomedical applications.

---

## 📌 Authors & Affiliation

- **Jairus S. Solomon** ([jairus.samraj.solomon@gmail.com](mailto:jairus.samraj.solomon@gmail.com))
- **Subham P. Gupta** ([shubham01dec04@gmail.com](mailto:shubham01dec04@gmail.com))
- **Vinayak S. Salunke** ([salunkevinayak2005@gmail.com](mailto:salunkevinayak2005@gmail.com))
- **Dr. Md. Sadullah**

*School of Electronics Engineering (SENSE), Vellore Institute of Technology (VIT), Vellore, India.*

---

## 📖 Executive Summary & Novelty

Electrocardiogram (ECG) acquisition requires high-gain, low-noise amplification of weak bio-potentials (microvolt to millivolt range) under significant power-line interference (50 Hz), electrode DC offsets, motion artifacts, and flicker noise ($1/f$).

### Key Contributions:
1. **Transistor Sizing Optimization:** Sub-threshold / weak-inversion PMOS differential input pair sizing ($W/L = 36\,\mu\text{m} / 0.5\,\mu\text{m}$) maximizes $g_m / I_D$ transconductance efficiency and minimizes flicker noise without increasing current budget. Elongated channel lengths on active loads boost output resistance ($R_o$) and voltage gain.
2. **Driven Right Leg (DRL) Active Noise Cancellation:** Common-mode feedback loop senses common-mode input voltage and returns inverted feedback to body tissue, suppressing 50 Hz power-line hum and boosting CMRR to **113.54 dB**.
3. **Realistic Body Impedance Model:** Implements a two-terminal skin-dermis-tissue R-C network model to simulate physiological electrode-skin interface impedance instead of idealized voltage sources.
4. **Sub-Hertz High-Pass Filtering:** Pseudo-resistor network ($R_f \sim \text{T}\Omega$) paired with feedback capacitance ($C_f = 0.1\text{ pF}$) establishes lower cutoff frequency $f_L \approx 0.198\text{ Hz}$, eliminating baseline wander and DC offsets.

---

## 📊 Key Performance Metrics

| Metric / Parameter | Simulated Result | Requirement / Target | Unit |
| :--- | :--- | :--- | :--- |
| **Technology Node** | **180** | 180 | nm CMOS |
| **Supply Voltage ($V_{DD}$)** | **1.8** | 1.8 | V |
| **Differential Midband Gain ($A_d$)** | **79.54** | $\ge 70.0$ | dB |
| **Common-Mode Gain ($A_{cm}$)** | **-34.00** | $\le -20.0$ | dB |
| **Common-Mode Rejection Ratio (CMRR)** | **113.54** | $\ge 100.0$ | dB |
| **AC System Bandwidth (-3dB)** | **198.4 mHz to 34 kHz** | 0.5 Hz to 10 kHz | - |
| **Cardiac Signal Bandpass Range** | **0.5 to 100** | 0.5 to 100 | Hz |
| **Unity Gain Frequency ($f_u$)** | **28.557** | $\approx 30.0$ | kHz |
| **Gain-Bandwidth Product (GBW)** | **322.46** | $\ge 100$ | MHz |
| **Slew Rate (SR)** | **0.145** | $\ge 0.10$ | V/$\mu$s |

---

## 🏗️ System Architecture & Sub-Block Overview

```
                          ┌────────────────────────────────────────────────────────┐
                          │                   HUMAN BODY MODEL                     │
                          │   (Skin-Tissue Bio-Impedance Interface: Rp, Cp, Rs)    │
                          └──────────────────────────┬─────────────────────────────┘
                                                     │ Differential Bio-Signal Inputs
                                                     ▼
                          ┌────────────────────────────────────────────────────────┐
                          │               INSTRUMENTATION AMPLIFIER                │
                          │        Capacitive Feedback Gain (Av = C1 / Cf)         │
                          │       Pseudo-Resistors (Rf) for Sub-Hz Cutoff          │
                          └──────────────────────────┬─────────────────────────────┘
                                                     │
                                                     ▼
                          ┌────────────────────────────────────────────────────────┐
                          │                     FILTER STAGES                      │
                          │    High-Pass Filter (HPF) -> Baseline Wander Removal   │
                          │    50 Hz Notch Filter     -> Power-Line Hum Rejection  │
                          │    Low-Pass Filter (LPF)  -> EMG High-Freq Suppression  │
                          └──────────────────────────┬─────────────────────────────┘
                                                     │
                                                     ▼
                          ┌────────────────────────────────────────────────────────┐
                          │             TWO-STAGE OPERATIONAL AMPLIFIER            │
                          │     PMOS Sub-Threshold Differential Input (M7-M8)     │
                          │     Miller Compensation Capacitor (Cc = 2.5 pF)        │
                          └──────────────────────────┬─────────────────────────────┘
                                                     │
                                                     ▼
                                              [ AFE Output ]
                                                     │
                          ┌──────────────────────────┴─────────────────────────────┐
                          │            DRIVEN RIGHT LEG (DRL) CIRCUIT              │
                          │    Common-Mode Inversion & Feedback via Protection R    │
                          └────────────────────────────────────────────────────────┘
```

For full mathematical equations and circuit derivations, see [`docs/circuit_architecture.md`](docs/circuit_architecture.md).

---

## 📐 Transistor Sizing Summary

| Transistor | Type | Role | $W$ ($\mu\text{m}$) | $L$ ($\mu\text{m}$) | $W/L$ | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **M7, M8** | PMOS | Differential Input Pair | 36.0 | 0.50 | 72.0 | Maximize $g_m$, minimize flicker noise |
| **M0, M1** | NMOS | 1st Stage Active Load | 12.0 | 1.00 | 12.0 | Increase $r_{o1}$, output resistance |
| **M2** | NMOS | Tail Current Source | 24.0 | 1.00 | 24.0 | Stable tail bias $I_{tail}$ |
| **M3** | NMOS | 2nd Stage CS Driver | 48.0 | 0.50 | 96.0 | High output $g_{m2}$ |
| **M10, M11**| PMOS | 2nd Stage PMOS Load | 36.0 | 1.00 | 36.0 | High output resistance $r_{o2}$ |
| **M12** | PMOS | Master Bias Reference | 18.0 | 2.00 | 9.0 | Low channel length modulation ($\lambda$) |

For complete device specs and biasing parameters, see [`docs/transistor_sizing_table.md`](docs/transistor_sizing_table.md).

---

## 📂 Repository File Structure

```
.
├── README.md                           # Main repository documentation & guide
├── LICENSE                             # MIT Open Source License
├── .gitignore                          # Ignore rules for Cadence, Spectre, & Python
├── requirements.txt                    # Python visualization dependencies
├── docs/
│   ├── design_specifications.md        # Complete electrical performance specs
│   ├── circuit_architecture.md         # Equations, derivations & block topologies
│   └── transistor_sizing_table.md      # Detailed transistor W/L ratios and biasing
├── netlists/
│   ├── ota_two_stage.scs               # Two-stage OTA Spectre SPICE netlist
│   ├── instrumentation_amp.scs         # Capacitive feedback IA Spectre netlist
│   ├── drl_circuit.scs                 # Driven Right Leg feedback netlist
│   ├── filter_stages.scs               # HPF, LPF & 50Hz notch filter netlists
│   ├── body_model.scs                  # Human body bio-impedance model netlist
│   └── ecg_afe_top.scs                 # Top-level testbench & simulation deck
└── src/
    ├── simulate_afe.py                 # Python analytical simulation & verification
    └── plot_results.py                 # Script generating performance curves
```

---

## 🛠️ Verification & Simulation Instructions

### 1. Python Analytical Simulation & Visualization
Ensure Python 3.8+ is installed. Install requirements and run the simulation scripts:

```bash
# Install dependencies
pip install -r requirements.txt

# Run analytical parameter calculation
python src/simulate_afe.py

# Generate performance curves (saved to plots/)
python src/plot_results.py
```

### 2. Cadence Virtuoso & Spectre Simulation
1. Launch Cadence Virtuoso IC design environment:
   ```bash
   virtuoso &
   ```
2. Import or reference the netlist files from `netlists/` into your Virtuoso library workspace.
3. Open Analog Design Environment (ADE XL / Assembler) and load `netlists/ecg_afe_top.scs`.
4. Run Spectre simulation for **DC Operating Point**, **AC Frequency Sweep** (1 mHz to 100 MHz), and **Transient Analysis** (0 to 10s).

---

## 📜 References

1. Y. Laababid, K. E. Khadiri, and A. Tahiri, *"Design of a low-power low-noise ecg amplifier for smart wearable devices using 180nm cmos technology,"* WSEAS Transactions on Power Systems, 2022.
2. R. Kumar, *"Signal processing techniques for removing noise from ecg signals,"* Journal of Biomedical Engineering and Research, 2019.
3. J. Zhang, Z. Hong, S. Quan, and Z. Ruizhi, *"A low-noise low-power amplifier with current-reused ota for ecg recordings,"* IEEE Transactions on Biomedical Circuits and Systems, 2018.
4. M. Steyaert, W. Sansen, and C. Zhongyuan, *"A micropower low-noise monolithic instrumentation amplifier for medical purposes,"* IEEE Journal of Solid-State Circuits, 1987.
5. B. B. Winter and J. G. Webster, *"Driven right leg circuit design,"* IEEE Transactions on Biomedical Engineering, 1983.

---

## 📄 License

This repository is distributed under the terms of the [MIT License](LICENSE).
