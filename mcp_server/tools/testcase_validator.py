"""
测试用例验证工具
验证测试用例的格式和完整性
"""
import json
from typing import Dict, Any, List


class TestCaseValidator:
    """测试用例验证工具类"""
    
    # 必填字段
    REQUIRED_FIELDS = ['title', 'steps', 'expected_result']
    
    # 可选字段
    OPTIONAL_FIELDS = ['description', 'precondition', 'actual_result', 'pass_fail']
    
    # 所有有效字段
    VALID_FIELDS = REQUIRED_FIELDS + OPTIONAL_FIELDS
    
    @staticmethod
    def validate_test_case(test_case_json: str) -> Dict[str, Any]:
        """
        验证测试用例格式
        
        Args:
            test_case_json: JSON 格式的测试用例字符串（单个或数组）
            
        Returns:
            dict: 验证结果，包含 valid, errors, warnings
            
        Example:
            {
                "valid": True,
                "errors": [],
                "warnings": [],
                "test_cases_count": 5,
                "message": "验证通过"
            }
        """
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "test_cases_count": 0,
            "message": ""
        }
        
        try:
            # 解析 JSON
            if isinstance(test_case_json, str):
                data = json.loads(test_case_json)
            else:
                data = test_case_json
            
            # 确保是列表
            if isinstance(data, dict):
                test_cases = [data]
            elif isinstance(data, list):
                test_cases = data
            else:
                result["valid"] = False
                result["errors"].append("测试用例数据必须是对象或数组")
                return result
            
            result["test_cases_count"] = len(test_cases)
            
            # 验证每个测试用例
            for idx, test_case in enumerate(test_cases, 1):
                case_errors = TestCaseValidator._validate_single_case(test_case, idx)
                if case_errors:
                    result["errors"].extend(case_errors)
                    result["valid"] = False
            
            # 设置消息
            if result["valid"]:
                result["message"] = f"验证通过，共 {result['test_cases_count']} 条测试用例"
            else:
                result["message"] = f"验证失败，发现 {len(result['errors'])} 个错误"
            
            return result
            
        except json.JSONDecodeError as e:
            result["valid"] = False
            result["errors"].append(f"JSON 解析失败: {str(e)}")
            result["message"] = "JSON 格式错误"
            return result
        except Exception as e:
            result["valid"] = False
            result["errors"].append(f"验证过程出错: {str(e)}")
            result["message"] = "验证失败"
            return result
    
    @staticmethod
    def _validate_single_case(test_case: Dict[str, Any], index: int) -> List[str]:
        """
        验证单个测试用例
        
        Args:
            test_case: 测试用例字典
            index: 测试用例索引（用于错误提示）
            
        Returns:
            list: 错误列表
        """
        errors = []
        
        # 检查是否为字典
        if not isinstance(test_case, dict):
            errors.append(f"测试用例 #{index}: 必须是对象类型")
            return errors
        
        # 检查必填字段
        for field in TestCaseValidator.REQUIRED_FIELDS:
            if field not in test_case:
                errors.append(f"测试用例 #{index}: 缺少必填字段 '{field}'")
            elif not test_case[field]:
                errors.append(f"测试用例 #{index}: 字段 '{field}' 不能为空")
        
        # 验证字段类型
        if 'title' in test_case and not isinstance(test_case['title'], str):
            errors.append(f"测试用例 #{index}: 'title' 必须是字符串")
        
        if 'description' in test_case and test_case['description'] and not isinstance(test_case['description'], str):
            errors.append(f"测试用例 #{index}: 'description' 必须是字符串")
        
        if 'precondition' in test_case and test_case['precondition'] and not isinstance(test_case['precondition'], str):
            errors.append(f"测试用例 #{index}: 'precondition' 必须是字符串")
        
        if 'steps' in test_case:
            if not isinstance(test_case['steps'], (list, str)):
                errors.append(f"测试用例 #{index}: 'steps' 必须是字符串或数组")
            elif isinstance(test_case['steps'], list):
                if not test_case['steps']:
                    errors.append(f"测试用例 #{index}: 'steps' 数组不能为空")
                for step_idx, step in enumerate(test_case['steps'], 1):
                    if not isinstance(step, str):
                        errors.append(f"测试用例 #{index}: 'steps[{step_idx}]' 必须是字符串")
        
        if 'expected_result' in test_case and not isinstance(test_case['expected_result'], str):
            errors.append(f"测试用例 #{index}: 'expected_result' 必须是字符串")
        
        # 检查无效字段
        for field in test_case.keys():
            if field not in TestCaseValidator.VALID_FIELDS:
                errors.append(f"测试用例 #{index}: 包含无效字段 '{field}'")
        
        return errors
