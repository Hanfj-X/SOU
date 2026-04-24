# Updating (老铁，别急，正在抓紧更新)
--

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
