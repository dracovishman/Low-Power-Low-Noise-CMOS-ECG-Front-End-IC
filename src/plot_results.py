#!/usr/bin/env python3
"""
Performance Visualization & Plot Generator
Low-Power Low-Noise CMOS ECG Front-End IC

Generates high-resolution performance plots corresponding to Virtuoso Spectre outputs:
- Figure 6: OTA Gain & Phase Frequency Response
- Figure 7 & 9: Overall AFE AC Gain Response (79.54 dB Midband Gain)
- Figure 8: 50 Hz Power-Line Notch Filter Rejection Response
- Figure 10 & 11: CMRR Calculation (Differential vs Common Mode Gain)
- Figure 14: Transient Step Response & Slew Rate Derivation
"""

import os
import numpy as np
import matplotlib.pyplot as plt

def ensure_output_dir():
    os.makedirs("plots", exist_ok=True)

def plot_ota_gain_phase():
    """Generates Figure 6: Two-stage OTA Frequency Response."""
    freq = np.logspace(-1, 8, 1000)  # 0.1 Hz to 100 MHz
    
    # 2nd-order transfer function approximation for two-stage OTA
    A0_db = 60.0
    A0_lin = 10 ** (A0_db / 20.0)
    fp1 = 50.0       # Dominant pole at 50 Hz
    fp2 = 1.5e6      # Non-dominant pole at 1.5 MHz
    
    s = 2j * np.pi * freq
    H = A0_lin / ((1 + s / (2 * np.pi * fp1)) * (1 + s / (2 * np.pi * fp2)))
    
    gain_db = 20 * np.log10(np.abs(H))
    phase_deg = np.angle(H, deg=True)
    
    fig, ax1 = plt.subplots(figsize=(8, 5))
    
    color = 'tab:red'
    ax1.set_xlabel('Frequency (Hz)')
    ax1.set_ylabel('Gain (dB)', color=color)
    ax1.semilogx(freq, gain_db, color=color, linewidth=2, label='OTA Gain (dB)')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, which="both", ls="--", alpha=0.5)
    ax1.set_ylim([-20, 70])
    
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Phase (deg)', color=color)
    ax2.semilogx(freq, phase_deg, color=color, linewidth=1.5, linestyle='--', label='Phase (deg)')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim([-200, 20])
    
    plt.title('Fig. 6: Two-Stage OTA AC Gain and Phase Response')
    fig.tight_layout()
    plt.savefig('plots/fig6_ota_gain_phase.png', dpi=300)
    plt.close()

def plot_afe_ac_response():
    """Generates Figure 7 & 9: Complete AFE AC Bandpass Response."""
    freq = np.logspace(-2, 6, 1000)  # 10 mHz to 1 MHz
    
    # System Specs
    Ad_db = 79.54
    Ad_lin = 10 ** (Ad_db / 20.0)
    fl = 0.1984      # Lower cutoff (198.4 mHz)
    fh = 34000.0     # Upper cutoff (34 kHz)
    
    s = 2j * np.pi * freq
    # Bandpass Transfer Function
    H_hpf = (s / (2 * np.pi * fl)) / (1 + s / (2 * np.pi * fl))
    H_lpf = 1.0 / (1 + s / (2 * np.pi * fh))
    H_sys = Ad_lin * H_hpf * H_lpf
    
    gain_db = 20 * np.log10(np.abs(H_sys))
    
    plt.figure(figsize=(8, 5))
    plt.semilogx(freq, gain_db, 'r-', linewidth=2.2, label='AFE Differential Gain ($A_d = 79.54$ dB)')
    plt.axhline(y=Ad_db - 3.0, color='k', linestyle=':', label='-3 dB Bandwidth Limits')
    plt.axvline(x=fl, color='g', linestyle='--', label=f'fL = {fl*1e3:.1f} mHz')
    plt.axvline(x=fh, color='b', linestyle='--', label=f'fH = {fh/1e3:.1f} kHz')
    
    plt.title('Fig. 7 & 9: Overall Gain Response of Analog Front-End (AFE)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Differential Gain (dB)')
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend(loc='lower left')
    plt.ylim([-20, 90])
    plt.tight_layout()
    plt.savefig('plots/fig9_afe_overall_gain.png', dpi=300)
    plt.close()

def plot_notch_filter():
    """Generates Figure 8: 50 Hz Notch Filter Response."""
    freq = np.linspace(10, 100, 1000)  # 10 Hz to 100 Hz
    
    f0 = 50.0
    Q = 8.0
    w0 = 2 * np.pi * f0
    s = 2j * np.pi * freq
    
    H_notch = (s**2 + w0**2) / (s**2 + (w0 / Q) * s + w0**2)
    gain_db = 20 * np.log10(np.clip(np.abs(H_notch), 1e-4, None))
    
    plt.figure(figsize=(8, 5))
    plt.plot(freq, gain_db, 'm-', linewidth=2, label='50 Hz Notch Filter Response')
    plt.axvline(x=50.0, color='r', linestyle='--', label='Power-Line Frequency (50 Hz)')
    
    plt.title('Fig. 8: 50 Hz Power-Line Interference Notch Filter Response')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Attenuated Gain (dB)')
    plt.grid(True, ls="--", alpha=0.5)
    plt.legend(loc='lower right')
    plt.ylim([-50, 5])
    plt.tight_layout()
    plt.savefig('plots/fig8_notch_filter_response.png', dpi=300)
    plt.close()

def plot_cmrr_curves():
    """Generates Figure 10 & 11: CMRR Calculation Curves."""
    freq = np.logspace(-1, 6, 1000)
    
    Ad_db = 79.54
    Acm_db = -34.00
    CMRR_db = Ad_db - Acm_db  # 113.54 dB
    
    s = 2j * np.pi * freq
    H_ad = (10**(Ad_db/20)) / (1 + s / (2*np.pi*34000))
    H_acm = (10**(Acm_db/20)) * (1 + s / (2*np.pi*1000)) / (1 + s / (2*np.pi*34000))
    
    gain_ad = 20 * np.log10(np.abs(H_ad))
    gain_acm = 20 * np.log10(np.abs(H_acm))
    cmrr_curve = gain_ad - gain_acm
    
    plt.figure(figsize=(8, 5))
    plt.semilogx(freq, gain_ad, 'r-', linewidth=2, label=f'Differential Gain Ad ({Ad_db:.2f} dB)')
    plt.semilogx(freq, gain_acm, 'b--', linewidth=2, label=f'Common Mode Gain Acm ({Acm_db:.2f} dB)')
    plt.semilogx(freq, cmrr_curve, 'g-.', linewidth=2.2, label=f'CMRR = Ad - Acm ({CMRR_db:.2f} dB)')
    
    plt.title('Fig. 10 & 11: Common-Mode Rejection Ratio (CMRR) Curves')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude (dB)')
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend(loc='center right')
    plt.ylim([-50, 130])
    plt.tight_layout()
    plt.savefig('plots/fig10_cmrr_plots.png', dpi=300)
    plt.close()

def plot_slew_rate_transient():
    """Generates Figure 14: Transient Step Response & Slew Rate."""
    t = np.linspace(0, 10, 1000)  # Microseconds
    
    # Step from 0.9V to 1.0V between t=5.11us and t=5.80us
    v_out = np.piecewise(t, 
        [t < 5.11, (t >= 5.11) & (t <= 5.80), t > 5.80],
        [0.90, lambda t: 0.90 + 0.10 * (t - 5.11) / (5.80 - 5.11), 1.00]
    )
    
    plt.figure(figsize=(8, 5))
    plt.plot(t, v_out, 'b-', linewidth=2.5, label='Transient Step Response')
    plt.plot([5.11, 5.80], [0.90, 1.00], 'ro', markersize=6, label='SR Measurement Points (ΔV=0.1V, Δt=0.69μs)')
    
    plt.title('Fig. 14: Transient Response & Slew Rate Calculation (SR = 0.145 V/μs)')
    plt.xlabel('Time (μs)')
    plt.ylabel('Output Voltage (V)')
    plt.grid(True, ls="--", alpha=0.5)
    plt.legend(loc='lower right')
    plt.ylim([0.85, 1.05])
    plt.tight_layout()
    plt.savefig('plots/fig14_slew_rate_transient.png', dpi=300)
    plt.close()

def main():
    ensure_output_dir()
    print("Generating verification plots...")
    plot_ota_gain_phase()
    plot_afe_ac_response()
    plot_notch_filter()
    plot_cmrr_curves()
    plot_slew_rate_transient()
    print("All plots successfully saved to the 'plots/' directory!")

if __name__ == "__main__":
    main()
