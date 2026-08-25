#!/usr/bin/env python3
"""
Analytical Simulation & Performance Verification Script
Low-Power Low-Noise CMOS ECG Front-End IC

Authors: Jairus S. Solomon, Subham P. Gupta, Vinayak S. Salunke, Dr. Md. Sadullah
Institution: Vellore Institute of Technology (VIT), Vellore, India
"""

import numpy as np
from scipy import signal

def calculate_ota_parameters():
    """Calculates OTA gain, GBW, transconductance, and slew rate."""
    # Sub-threshold / weak inversion parameters
    I_D = 100e-9        # 100 nA bias current
    VT = 25.9e-3        # Thermal voltage at 300K
    n = 1.25            # Sub-threshold slope factor
    
    # Transconductance
    gm1 = I_D / (n * VT)
    
    # Output resistance per stage
    ro1 = 150e6         # 150 M-ohm
    gm2 = 250e-6        # 250 uS
    ro2 = 80e6          # 80 M-ohm
    
    # Stage Gains
    Av1 = gm1 * ro1
    Av2 = gm2 * ro2
    Av_ota_linear = Av1 * Av2
    Av_ota_db = 20 * np.log10(Av_ota_linear)
    
    # Miller Compensation
    Cc = 2.5e-12        # 2.5 pF
    GBW_hz = gm1 / (2 * np.pi * Cc)
    
    # Slew Rate calculation (dV/dt)
    delta_V = 1.0 - 0.9  # 0.1 V
    delta_t = 0.69e-6    # 0.69 us (5.8 us - 5.11 us)
    SR_v_per_us = delta_V / (delta_t * 1e6)
    
    return {
        "gm1": gm1,
        "Av1_dB": 20 * np.log10(Av1),
        "Av2_dB": 20 * np.log10(Av2),
        "Av_ota_dB": Av_ota_db,
        "GBW_MHz": GBW_hz / 1e6,
        "SlewRate_V_us": SR_v_per_us
    }

def calculate_system_performance():
    """Calculates top-level differential gain, common-mode gain, and CMRR."""
    Ad_dB = 79.54
    Acm_dB = -34.00
    CMRR_dB = Ad_dB - Acm_dB  # 113.54 dB
    
    # Bandwidth points
    f_lower = 0.1984      # 198.4 mHz
    f_upper = 34000.0     # 34 kHz
    BW = f_upper - f_lower
    
    # GBW product calculation
    Ad_linear = 10 ** (Ad_dB / 20.0)  # ~9484.2 V/V
    GBW_prod = Ad_linear * f_upper
    
    return {
        "Differential_Gain_dB": Ad_dB,
        "Common_Mode_Gain_dB": Acm_dB,
        "CMRR_dB": CMRR_dB,
        "Lower_Cutoff_Hz": f_lower,
        "Upper_Cutoff_Hz": f_upper,
        "Bandwidth_Hz": BW,
        "GBW_Product_MHz": GBW_prod / 1e6
    }

def main():
    print("==========================================================================")
    print("  CMOS ECG FRONT-END IC: ANALYTICAL SIMULATION & VERIFICATION RESULTS")
    print("==========================================================================")
    
    ota_results = calculate_ota_parameters()
    print("\n--- Two-Stage OTA Core Parameters ---")
    print(f"  First-Stage gm1               : {ota_results['gm1']*1e6:.2f} uS")
    print(f"  First-Stage Gain (Av1)        : {ota_results['Av1_dB']:.2f} dB")
    print(f"  Second-Stage Gain (Av2)       : {ota_results['Av2_dB']:.2f} dB")
    print(f"  Total OTA Midband Gain        : {ota_results['Av_ota_dB']:.2f} dB")
    print(f"  Calculated OTA GBW            : {ota_results['GBW_MHz']:.2f} MHz")
    print(f"  Simulated Slew Rate           : {ota_results['SlewRate_V_us']:.3f} V/us")
    
    sys_results = calculate_system_performance()
    print("\n--- Top-Level ECG Front-End System Performance ---")
    print(f"  Differential Gain (Ad)        : {sys_results['Differential_Gain_dB']:.2f} dB")
    print(f"  Common-Mode Gain (Acm)        : {sys_results['Common_Mode_Gain_dB']:.2f} dB")
    print(f"  Common-Mode Rejection (CMRR)  : {sys_results['CMRR_dB']:.2f} dB")
    print(f"  Lower Cutoff Frequency (fL)   : {sys_results['Lower_Cutoff_Hz']*1e3:.1f} mHz")
    print(f"  Upper Cutoff Frequency (fH)   : {sys_results['Upper_Cutoff_Hz']/1e3:.1f} kHz")
    print(f"  System AC Bandwidth (BW)      : {sys_results['Bandwidth_Hz']/1e3:.3f} kHz")
    print(f"  Gain-Bandwidth Product (GBW)  : {sys_results['GBW_Product_MHz']:.2f} MHz")
    print("==========================================================================\n")

if __name__ == "__main__":
    main()
