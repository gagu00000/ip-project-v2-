# 🛒 UAE Promo Pulse Simulator + Data Rescue Dashboard

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> A comprehensive data quality toolkit and promotional simulation dashboard for UAE retail operations.

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Quick Start](#quick-start)
3. [Project Structure](#project-structure)
4. [Data Model](#data-model)
5. [Data Cleaning Rules & Justifications](#data-cleaning-rules--justifications)
6. [KPI Definitions](#kpi-definitions)
7. [Demand Uplift Logic](#demand-uplift-logic)
8. [Simulation Constraints](#simulation-constraints)
9. [Assumptions Documentation](#assumptions-documentation)
10. [Critical Thinking Answers](#critical-thinking-answers)
11. [Scope Control Notes](#scope-control-notes)
12. [Faculty Testing Guide](#faculty-testing-guide)

---

## 🎯 Project Overview

### Business Context

This project simulates a real-world scenario for a **UAE omnichannel retailer** operating across:
- **Cities**: Dubai, Abu Dhabi, Sharjah
- **Channels**: App, Web, Marketplace
- **Fulfillment**: Own warehouse, 3PL (Third-Party Logistics)

### Problem Statement

Build an end-to-end Python solution that:

1. **Phase 1 (Data Rescue Toolkit)**: Cleans messy/dirty data exports
2. **Phase 2 (Promo Pulse Simulator)**: Runs what-if discount simulations
3. **Final Output**: Interactive dashboard with Executive/Manager views

### Key Features

| Feature | Description |
|---------|-------------|
| 🧹 Data Cleaning | Automated validation, cleaning, and issue logging |
| 📊 KPI Engine | 12+ business metrics computed in real-time |
| 🎮 What-If Simulation | Rule-based demand uplift with constraints |
| 👔 Executive View | Financial KPIs, revenue trends, recommendations |
| 🔧 Manager View | Operational metrics, stockout risks, data quality |
| 📁 Column Mapping | Dynamic schema mapping for custom datasets |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

```bash
# Clone or download the project
cd uae-promo-pulse-simulator

# Install dependencies
pip install -r requirements.txt