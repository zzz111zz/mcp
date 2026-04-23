# FastMCP 服务端与客户端项目搭建完整步骤
## 一、环境准备
1. **创建项目文件夹**
新建空文件夹（如`mcp_demo`），存放服务端与客户端代码。
2. **安装依赖**
打开终端，进入项目目录，执行安装命令：
```bash
pip install mcp
```
3. **确认Python环境**
确保已安装Python 3.8及以上版本。

---

## 二、编写服务端代码（test.py）
1. 在项目目录下新建`test.py`文件。
2. 写入以下服务端代码：
```python
import os
from mcp.server.fastmcp import FastMCP

# 初始化FastMCP服务
mcp = FastMCP("FileSystem")

@mcp.tool()
def get_desktop_files() -> list:
    '''获取当前用户的桌面文件列表'''
    return os.listdir(os.path.expanduser("~/Desktop"))

@mcp.tool()
def calculator(a: float, b: float, operator: str) -> float:
    """执行基础数学运算（支持+-*/）
    Args:
        operator: 运算符，必须是'+', '-', '*', '/'之一
    """
    if operator == '+':
        return a + b
    elif operator == '-':
        return a - b
    elif operator == '*':
        return a * b
    elif operator == '/':
        return a / b
    else:
        raise ValueError("无效运算符")

if __name__ == "__main__":
    # 启动服务，使用stdio传输
    mcp.run(transport='stdio')
```

---

## 三、编写客户端代码（fastmcp_client.py）
1. 在项目目录下新建`fastmcp_client.py`文件。
2. 写入以下客户端代码：
```python
# fastmcp_client.py
import asyncio
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters

async def main():
    # 配置服务端启动参数
    server_params = StdioServerParameters(
        command="python",
        args=["test.py"]
    )
    
    print("正在连接FastMCP服务器...")
    
    # 建立stdio连接
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化会话
            await session.initialize()
            print("✅ 已连接到服务器\n")
            
            # 列出所有可用工具
            tools = await session.list_tools()
            print("📦 可用工具:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            
            # 调用获取桌面文件工具
            print("\n📁 获取桌面文件列表...")
            result = await session.call_tool("get_desktop_files", {})
            if result.content:
                print(f"桌面文件: {result.content[0].text}")
            
            # 调用计算器工具
            print("\n🧮 测试计算器:")
            
            # 加法
            result = await session.call_tool("calculator", {
                "a": 10,
                "b": 5,
                "operator": "+"
            })
            print(f"10 + 5 = {result.content[0].text}")
            
            # 乘法
            result = await session.call_tool("calculator", {
                "a": 7,
                "b": 8,
                "operator": "*"
            })
            print(f"7 * 8 = {result.content[0].text}")
            
            # 除法
            result = await session.call_tool("calculator", {
                "a": 100,
                "b": 4,
                "operator": "/"
            })
            print(f"100 / 4 = {result.content[0].text}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 四、运行项目
1. **直接运行客户端**
客户端会自动启动服务端并建立连接，终端执行：
```bash
python fastmcp_client.py
```
2. **运行成功输出**
- 显示连接成功提示
- 列出`get_desktop_files`、`calculator`两个工具
- 打印桌面文件列表
- 输出计算器运算结果

---

## 五、项目结构
最终项目目录结构：
```
mcp_demo/
├── test.py          # FastMCP服务端
└── fastmcp_client.py  # MCP客户端
```

---

## 六、核心说明
1. **通信方式**：基于`stdio`（标准输入输出）实现服务端与客户端通信。
2. **工具注册**：服务端用`@mcp.tool()`装饰器定义可调用工具。
3. **调用流程**：客户端连接→初始化会话→列出工具→调用工具。

