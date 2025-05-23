from mcp import MCPClient


def main(适应症=None, 副作用=None):
    client = MCPClient(
        api_key="your_api_key",
        base_url="http://localhost:8000"
    )

    while True:
        query = input("请输入查询条件（例如：抗癌药物 或 处方药）：")
        if query.lower() in ['exit', 'quit']:
            break

        try:
            response = client.execute_tool(
                tool_name="query_drug_info",
                input_data={"criteria": query}
            )
            print(f"查询结果（共{response['count']}条）：")
            for drug in response['drugs']:
                print(f"名称：{drug['name']}
                适应症：{drug['indication']}
                副作用：{drug['side_effects']}\n
                ")
        except Exception as e:
            print(f"错误：{str(e)}")


if __name__ == "__main__":
    main()