# 功能要求
- 输入：用户用自然语言表述的一个任务
- 输出：该自然语言输入中的地理位置信息

## 举例
- 输入：查询新华路行人违章
- 输出：新华路

# 实现方式

python函数：
```python
def language_to_location(language):
    """从自然语言中提取地理位置信息
    input:
        language: str. 一段文本
    output:
        location: str. 表示地点的文本
    """
```

# 实现原理

通过langchain调用大模型实现。