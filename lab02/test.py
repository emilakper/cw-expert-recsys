import asyncio
from llm_handler import get_qwen_response

async def test():
    gpt_resp = await get_qwen_response("Recommend a movie like Seven.")
    print("ans:", gpt_resp)

if __name__ == "__main__":
    asyncio.run(test())
