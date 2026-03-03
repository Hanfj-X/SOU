import json
import os
from typing import List, Dict, Any, Optional


class JsonManager:
    """
    A class for managing JSON data storage and retrieval.
    It provides methods for loading, saving, and manipulating JSON data in a file.
    The data structure is a list of dictionaries, where each dictionary represents a conversation.
    Each conversation contains "messages" (a list of message dictionaries) and "images" (a list of image paths).
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data: List[Dict] = []
        self._load_data()

    def _load_data(self):
        """从JSON文件加载数据"""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    self.data = json.load(file)
            else:
                self.data = []
                self._save_data()  # 创建新文件
        except (json.JSONDecodeError, FileNotFoundError):
            # 如果文件损坏或不存在，初始化空数据
            self.data = []
            self._save_data()

    def _save_data(self):
        """保存数据到JSON文件"""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"文件保存错误: {e}")

    def clear_all_data(self):
        """清除所有数据"""
        self.data = []
        self._save_data()
        print("所有数据已清除")

    def add_conversation(self, messages: List[Dict], images: List[str]):
        """添加一个新的对话"""
        new_conversation = {
            "messages": messages,
            "images": images
        }
        self.data.append(new_conversation)
        self._save_data()
        # print(f"对话已添加，当前共有 {len(self.data)} 个对话")

    def delete_conversation_by_image(self, image_path: str) -> bool:
        """根据images索引删除对话"""
        initial_length = len(self.data)
        self.data = [conv for conv in self.data if image_path not in conv.get("images", [])]

        if len(self.data) < initial_length:
            self._save_data()
            print(f"已删除包含图像 '{image_path}' 的对话")
            return True
        else:
            print(f"未找到包含图像 '{image_path}' 的对话")
            return False

    def get_all_conversations(self) -> List[Dict]:
        """获取所有对话"""
        return self.data

    def get_conversation_by_image(self, image_path: str) -> Optional[Dict]:
        """根据images索引查找对话"""
        for conversation in self.data:
            if image_path in conversation.get("images", []):
                return conversation
        return None

    def update_conversation(self, image_path: str, new_messages: List[Dict] = None, new_images: List[str] = None):
        """更新指定对话的内容"""
        for conversation in self.data:
            if image_path in conversation.get("images", []):
                if new_messages is not None:
                    conversation["messages"] = new_messages
                if new_images is not None:
                    conversation["images"] = new_images
                self._save_data()
                print(f"已更新包含图像 '{image_path}' 的对话")
                return True
        print(f"未找到包含图像 '{image_path}' 的对话")
        return False

    def get_conversation_count(self) -> int:
        """获取对话数量"""
        return len(self.data)

    def get_all_images(self) -> List[str]:
        """获取所有唯一的图像路径"""
        all_images = []
        for conversation in self.data:
            all_images.extend(conversation.get("images", []))
        return list(set(all_images))  # 去重

    def backup_data(self, backup_path: str):
        """备份数据到指定文件"""
        try:
            with open(backup_path, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=2)
            print(f"数据已备份到: {backup_path}")
        except IOError as e:
            print(f"备份失败: {e}")

    def restore_from_backup(self, backup_path: str):
        """从备份文件恢复数据"""
        try:
            with open(backup_path, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
            self._save_data()
            print(f"已从备份文件恢复数据")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"恢复失败: {e}")