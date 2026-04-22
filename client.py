# fastmcp_client.py
import asyncio
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters

async def main():
    # 创建服务器参数
    server_params = StdioServerParameters(
        command="python",
        args=["test.py"]
    )
    
    print("正在连接FastMCP服务器...")
    
    # 使用stdio_client连接
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化会话（这是关键步骤）
            await session.initialize()
            print("✅ 已连接到服务器\n")
            
            # 列出所有工具
            tools = await session.list_tools()
            print("📦 可用工具:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            
            # 调用get_desktop_files
            print("\n📁 获取桌面文件列表...")
            result = await session.call_tool("get_desktop_files", {})
            if result.content:
                print(f"桌面文件: {result.content[0].text}")
            
            # 测试计算器
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