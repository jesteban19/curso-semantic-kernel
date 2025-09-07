import asyncio

from semantic_kernel import Kernel
from semantic_kernel.agents import AgentGroupChat, ChatCompletionAgent
from semantic_kernel.agents.strategies import TerminationStrategy
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion


def _create_kernel_with_chat_completion(service_id: str) -> Kernel:
    kernel = Kernel()
    kernel.add_service(OpenAIChatCompletion(service_id=service_id, ai_model_id="gpt-5-nano"))
    return kernel


class ApprovalTerminationStrategy(TerminationStrategy):
    """A strategy for determining when an agent should terminate."""

    async def should_agent_terminate(self, agent, history):
        """Check if the agent should terminate."""
        return "approved" in history[-1].content.lower()


REVIEWER_NAME = "ArtDirector"
REVIEWER_INSTRUCTIONS = """
Eres un director de arte con opiniones sobre copywriting, fruto de tu pasión por David Ogilvy.
El objetivo es determinar si el texto presentado tiene 100 letras o menos  es apto para imprimir.
De ser así, indica que está "Approved".
De no ser así, solo ofrece consejos sobre cómo perfeccionar el texto sugerido sin ejemplos.
"""

COPYWRITER_NAME = "CopyWriter"
COPYWRITER_INSTRUCTIONS = """
Eres redactor con diez años de experiencia y eres conocido por tu brevedad y tu humor irónico.
El objetivo es refinar y elegir el mejor texto como experto en la materia.
Solo proporciona una propuesta por respuesta.
Estás totalmente concentrado en el objetivo.
No pierdas el tiempo con charlas superficiales.
Considera las sugerencias al refinar una idea.
"""


#TASK = "un ejercicio corto de programación."
TASK = "un eslogan para una tienda de ropa para adolescentes con estilo urbano"

async def main():
    # 1. Create the reviewer agent based on the chat completion service
    agent_reviewer = ChatCompletionAgent(
        kernel=_create_kernel_with_chat_completion("artdirector"),
        name=REVIEWER_NAME,
        instructions=REVIEWER_INSTRUCTIONS,
    )

    # 2. Create the copywriter agent based on the chat completion service
    agent_writer = ChatCompletionAgent(
        kernel=_create_kernel_with_chat_completion("copywriter"),
        name=COPYWRITER_NAME,
        instructions=COPYWRITER_INSTRUCTIONS,
    )

    # 3. Place the agents in a group chat with a custom termination strategy
    group_chat = AgentGroupChat(
        agents=[
            agent_writer,
            agent_reviewer,
        ],
        termination_strategy=ApprovalTerminationStrategy(
            agents=[agent_reviewer],
            maximum_iterations=10,
        ),
    )

    # 4. Add the task as a message to the group chat
    await group_chat.add_chat_message(message=TASK)
    print(f"# User: {TASK}")

    # 5. Invoke the chat
    async for content in group_chat.invoke():
        print(f"# {content.name}: {content.content}")

if __name__ == "__main__":
    asyncio.run(main())