import asyncio
from llm_handler import get_gpt3_response

async def test():
    gpt_resp = await get_gpt3_response("Recommend a movie like Seven.")
    print("GPT3:", gpt_resp)

if __name__ == "__main__":
    asyncio.run(test())
