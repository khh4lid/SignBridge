<div align="center">

# 🤟 SignBridge

### Real-Time Arabic Sign Language to Speech Translation

[![Demo](https://img.shields.io/badge/🌐_Live_Demo-HuggingFace-brightgreen?style=for-the-badge)](https://huggingface.co/spaces/Khaled0wleed/SignBridge)
[![GitHub](https://img.shields.io/badge/GitHub-SignBridge-purple?style=for-the-badge&logo=github)](https://github.com/khh4lid/SignBridge)
[![Hackathon](https://img.shields.io/badge/🏆_Hackathon-Darb_2025-orange?style=for-the-badge)](https://github.com/khh4lid/SignBridge)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

*Giving Voice to the Silent — إعطاء صوت للصامتين*

</div>

---

## 📋 Table of Contents

- **[👥 Team Members](#-team-members)**
- **[🎯 General](#-general)**
  - [Description](#description)
  - [Problem Statement](#problem-statement)
  - [Our Solution](#our-solution)
  - [Visual Demo](#visual-demo)
  - [Features](#features)
  - [System Architecture](#system-architecture)
- **[🛠️ Hardware Setup](#️-hardware-setup)**
  - [Required Components](#required-components)
  - [Camera Configuration](#camera-configuration)
  - [Bluetooth Speaker Setup](#bluetooth-speaker-setup)
- **[🧠 AI Model](#-ai-model)**
  - [Dataset](#dataset)
  - [Feature Extraction](#feature-extraction)
  - [Training](#training)
  - [Evaluation Results](#evaluation-results)
- **[⚙️ Software Pipeline](#️-software-pipeline)**
  - [Camera Module](#camera-module)
  - [Hand Detection](#hand-detection)
  - [Predictor](#predictor)
  - [Word Builder](#word-builder)
  - [Text to Speech](#text-to-speech)
- **[🌐 Web Demo](#-web-demo)**
  - [FastAPI Backend](#fastapi-backend)
  - [Frontend Interface](#frontend-interface)
  - [How to Use](#how-to-use)
- **[🚀 Installation & Running](#-installation--running)**
  - [Quick Start](#quick-start)
  - [Run on Raspberry Pi](#run-on-raspberry-pi)
  - [Run Web Demo Locally](#run-web-demo-locally)
- **[📁 Project Structure](#-project-structure)**
- **[📊 Results](#-results)**
- **[📈 Impact](#-impact)**

---

## 👥 Team Members

| Name | Role | Responsibility |
|---|---|---|
| **Khaled Waleed** | Hardware & Integration Lead | Raspberry Pi 5 setup, camera integration, system pipeline, project management |
| **Abdullah Waleed** | AI & Data Engineer | Dataset preparation, model training, MediaPipe landmark extraction, 78-feature algorithm |
| **Abdullah Nashwan** | Audio Engineer | Arabic TTS integration, Bluetooth speaker, speech quality optimization |
| **Abdulqader Al-Saqqaf** | Design & Business | Product design, UX, business plan, market research |
| **Ashraf Al-Junaidi** | Marketing & Strategy | Brand identity, digital marketing, target market, hackathon presentation |

---

## 🎯 General

### Description

SignBridge is a **portable, low-cost, real-time device** that translates Arabic Sign Language hand gestures into spoken Arabic audio. It runs entirely on a Raspberry Pi 5 with no cloud dependency.

### Problem Statement

Over **430 million people** worldwide live with hearing or speech disabilities. In daily interactions — hospitals, schools, pharmacies — deaf and mute individuals face a significant communication barrier with people who do not understand sign language.
