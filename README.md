# Multi-OS Network Automation & Security Hardening
![Python](https://shields.io) ![Cisco](https://shields.io)

## 🚀 Project Overview
This repository contains a Python-based automation framework designed to standardize security configurations across a heterogeneous Cisco environment. The script manages Catalyst, Nexus, and IOS-XR platforms from a single management plane.

## 🛠 Features
- **Multi-OS Support:** Custom command mapping for IOS-XE, NX-OS, and IOS-XR.
- **Automated Hardening:** Deploys STIG-compliant banners, password encryption, and AAA settings.
- **Credential Rotation:** Securely updates administrative SSH passwords across the fleet.
- **Auto-Backup:** Generates timestamped configuration snapshots prior to any changes.
- **Legacy Support:** Programmatic workarounds for SSH-DSS key exchange on legacy hardware.

## 📈 Technical Challenges Overcome
- **Library Versioning:** Manually patched the `paramiko` transport layer to restore support for deprecated legacy encryption algorithms.
- **Adaptive Auth:** Developed retry-logic to maintain connection persistence during password rotation cycles.
- **Environment Migration:** Successfully managed project files across restricted Jump Hosts using Secure Copy (SCP).

## 📄 License
Distributed under the MIT License.
