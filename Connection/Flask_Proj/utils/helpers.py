import random
import string
import datetime

def generate_random_string(length):
    """生成指定长度的随机字符串"""
    if not isinstance(length, int) or length < 0:
        raise ValueError("Length must be a non-negative integer.")
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def parse_combined_datetime_str(dt_str):
    """
    安全地将 'YYYY-MM-DDTHH:mm:ss' 格式的字符串转换为 datetime 对象。
    如果字符串为 None 或解析失败，则返回 None。
    """
    if dt_str:
        try:
            return datetime.datetime.fromisoformat(dt_str)
        except ValueError as e:
            print(f"日期时间解析错误: {dt_str} - {e}")
            return None
    return None