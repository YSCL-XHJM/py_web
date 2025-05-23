from mcp import FastMCP, mcpapp
import sqlite3
from fastapi import HTTPException

# 初始化MCP服务
app = FastMCP("DrugQueryService")

# 数据库连接
conn = sqlite3.connect('database/drug_data.db')
conn.row_factory = sqlite3.Row


# 定义查询工具
@app.tool(description="根据条件查询药物信息")
async def query_drug_info(criteria: str) -> dict:
    try:
        cursor = conn.cursor()
        query = f"SELECT * FROM drugs WHERE name LIKE '%{criteria}%' OR indication LIKE '%{criteria}%'"
        cursor.execute(query)
        results = cursor.fetchall()

        return {
            "drugs": [dict(row) for row in results],
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 启动服务
if __name__ == "__main__":
    app.run(port=8000)