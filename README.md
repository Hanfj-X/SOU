# Updating (别急，正在抓紧更新)
--


<div align="center">

# [Can Multimodal Large Language Models Truly Understand Small Objects?]

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![arXiv](https://img.shields.io/badge/arXiv-2401.xxxxx-b31b1b.svg)](https://arxiv.org/)
[![HuggingFace](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Models-ffcc00)](https://huggingface.co/)

[**[🏠 Homepage]**](你的链接) | [**[📖 Paper]**](你的链接) | [**[📊 Dataset]**](你的链接) | [**[📦 Code]**](你的链接)

</div>

---

## 0. Introduction

Vision-language models (VLMs) have shown significant potential in interpreting medical imagery. However, existing benchmarks often fail to assess whether these models truly understand clinical logic. 

To bridge this gap, we introduce **[项目缩写, 如 SOU-Bench]**, a comprehensive benchmark designed for clinical visual reasoning.

# SOU
# Annotations_Driving

Generate driving scene VQA datasets from COCO annotations.

**Files**:
- `json_manager.py`: JSON data management
- `CreateJson_Driving.py`: Dataset generator (6 task types)
- `val.json`: Example COCO annotations

**Prerequisites**:
1. Place your image dataset in the folder specified in `CreateJson_Driving.py` (e.g., `Images_Driving`)
2. Install dependencies: `pip install pycocotools opencv-python`

**Usage**:
1. Update image path in `CreateJson_Driving.py` to match your dataset folder
2. Run: `python CreateJson_Driving.py`
