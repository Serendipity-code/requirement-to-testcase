"""
文件操作工具
提供文件读写功能
"""
import os
from typing import Dict, Any


class FileOperations:
    """文件操作工具类"""
    
    @staticmethod
    def read_file(path: str) -> str:
        """
        读取文件内容
        
        Args:
            path: 文件路径
            
        Returns:
            文件内容字符串
            
        Raises:
            FileNotFoundError: 文件不存在
            Exception: 其他读取错误
        """
        try:
            if not os.path.exists(path):
                raise FileNotFoundError(f"文件不存在: {path}")
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return content
        except Exception as e:
            raise Exception(f"读取文件失败: {str(e)}")
    
    @staticmethod
    def write_file(path: str, content: str) -> bool:
        """
        写入文件内容
        
        Args:
            path: 文件路径
            content: 要写入的内容
            
        Returns:
            bool: 写入是否成功
            
        Raises:
            Exception: 写入错误
        """
        try:
            # 确保目录存在
            directory = os.path.dirname(path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
        except Exception as e:
            raise Exception(f"写入文件失败: {str(e)}")
