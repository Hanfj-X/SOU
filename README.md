# Updating (别急，正在抓紧更新)
--


<div align="center">

# MLLM-ISU
### The First-Ever Comprehensive Benchmark for Multimodal Large Language Models based Intrusion Scene Understanding

[**[📖 Paper]**](链接) | [**[📊 Dataset (Hugging Face)]**](你的HF链接) | [**[🤖 ModelScope List]**](可选：模型列表链接)

</div>

## 🌟 Highlights
* **First-Ever Benchmark**: Specifically designed for **Intrusion Scene Understanding (ISU)** in complex environments.
* **Comprehensive Evaluation**: Benchmarking 10+ state-of-the-art MLLMs (e.g., Qwen2.5-VL, InternVL2) using their official implementations.
* **Real-world Scenarios**: Covering diverse intrusion cases with high-quality multimodal data.
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
