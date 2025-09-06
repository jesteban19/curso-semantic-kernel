
import asyncio
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

async def main():

    agent = ChatCompletionAgent(
        service=OpenAIChatCompletion(ai_model_id="gpt-5-nano"),
        name="SK-Assistant",
        instructions="""Eres un asistente útil de documentación en python, 
        en un parrafo muy breve explicaras el termino que el usuario te proporcione.""",
    )


    response = await agent.get_response(messages="Necesito saber que es un decorador en python")
    print(response.content)

asyncio.run(main()) 