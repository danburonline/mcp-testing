import asyncio
import os
import json
import logging
from datetime import datetime
from fastmcp import Client
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Setup logging
def setup_logging():
    """Setup logging configuration for session tracking"""
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"{log_dir}/mcp_client_session_{timestamp}.log"

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler(),  # Also log to console
        ],
    )

    logger = logging.getLogger(__name__)
    logger.info("=== MCP CLIENT SESSION STARTED ===")
    logger.info(f"Log file: {log_filename}")

    return logger, log_filename


class MCPClient:
    def __init__(self, logger):
        self.client = Client("http://localhost:8080/mcp/")
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.tools = []
        self.logger = logger
        self.session_data = {
            "session_start": datetime.now().isoformat(),
            "interactions": [],
        }

    def log_interaction(self, user_input, tool_result, enhanced_response, error=None):
        """Log detailed interaction data for analysis"""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "tool_result": tool_result,
            "enhanced_response": enhanced_response,
            "error": error,
        }

        self.session_data["interactions"].append(interaction)

        # Log structured data
        self.logger.info("=" * 80)
        self.logger.info(f"USER INPUT: {user_input}")
        self.logger.info(f"TOOL RESULT: {tool_result}")
        self.logger.info(f"ENHANCED RESPONSE: {enhanced_response}")
        if error:
            self.logger.error(f"ERROR: {error}")
        self.logger.info("=" * 80)

    def save_session_data(self, log_filename):
        """Save session data as JSON for detailed analysis"""
        json_filename = log_filename.replace(".log", "_data.json")
        self.session_data["session_end"] = datetime.now().isoformat()

        try:
            with open(json_filename, "w", encoding="utf-8") as f:
                json.dump(self.session_data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Session data saved to: {json_filename}")
        except Exception as e:
            self.logger.error(f"Failed to save session data: {str(e)}")

    async def get_llm_response(self, prompt):
        """Get response from OpenAI to understand user intent"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant. The user will ask you questions and you should provide thoughtful responses. You have access to additional tools if needed.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1000,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error with OpenAI: {str(e)}"

    async def get_enhanced_response(self, original_prompt, tool_response):
        """Get enhanced response from OpenAI using the tool's response"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant. You will be given a user's original question and web search results from a search tool. Your job is to analyze the search results and provide a comprehensive, well-structured answer to the user's question. You can synthesize information from multiple sources, add context, clarify points, provide additional insights, or reorganize the information to be more helpful. Present the information in a clear, engaging way that directly addresses the user's question.",
                    },
                    {
                        "role": "user",
                        "content": f"Original question: {original_prompt}\n\nTool's response: {tool_response}\n\nPlease provide an enhanced, improved response to the original question using the tool's information as a foundation.",
                    },
                ],
                max_tokens=1500,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error with OpenAI enhancement: {str(e)}"

    async def chat(self, user_input):
        """Process user input using MCP tools first, then enhance with LLM"""
        tool_result = None
        enhanced_response = None
        error = None

        try:
            async with self.client:
                # Get available tools
                self.tools = await self.client.list_tools()
                print(f"📋 Found {len(self.tools)} available tools")
                self.logger.info(
                    f"Available tools: {[tool.name for tool in self.tools]}"
                )

                print("\n" + "─" * 60)
                print("🌐 STEP 1: Calling MCP 'search_the_web' tool...")
                print("─" * 60)
                tool_result = await self.client.call_tool(
                    "search_the_web", {"query": user_input, "max_results": 3}
                )
                print(f"🔍 SEARCH RESULTS: {tool_result}")

                print("\n" + "─" * 60)
                print("🤖 STEP 2: CLIENT LLM enhancing the search results...")
                print("─" * 60)
                enhanced_response = await self.get_enhanced_response(
                    user_input, tool_result
                )
                print(f"✨ ENHANCED RESPONSE: {enhanced_response}")

                print("\n" + "═" * 60)
                print("📋 FINAL SUMMARY")
                print("═" * 60)

                final_response = f"""
┌─ 🌐 ORIGINAL SEARCH RESULTS (search_the_web via MCP server):
│  {tool_result}
│
├─ ✨ ENHANCED CLIENT RESPONSE (Client LLM improved the search results):
│  {enhanced_response}
│
└─ 💡 WORKFLOW EXPLANATION:
   • First: MCP 'search_the_web' tool searched for relevant information
   • Then: Client LLM took those results and enhanced them
   • Result: A more comprehensive and contextualized answer
"""

                # Log the interaction
                self.log_interaction(user_input, tool_result, enhanced_response)

                return final_response

        except Exception as e:
            error = str(e)
            self.logger.error(f"Error in chat method: {error}")
            # Still log the interaction even if there was an error
            self.log_interaction(user_input, tool_result, enhanced_response, error)
            return f"❌ Error occurred: {error}"


async def main():
    # Setup logging
    logger, log_filename = setup_logging()

    mcp_client = MCPClient(logger)

    print("🚀 MCP Client with LLM is ready!")
    print(
        "💡 This client uses OpenAI to process your input and the search_the_web tool for enhanced responses"
    )
    print(f"📊 Logging to: {log_filename}")
    print("📝 Type 'quit' to exit.\n")

    logger.info("Client started and ready for interactions")

    try:
        while True:
            user_input = input("👤 Your question: ").strip()
            if user_input.lower() == "quit":
                print("👋 Goodbye!")
                logger.info("User initiated quit")
                break

            if not user_input:
                print("⚠️ Please enter a question.")
                continue

            print("\n" + "=" * 60)
            response = await mcp_client.chat(user_input)
            print(response)
            print("=" * 60 + "\n")

    except KeyboardInterrupt:
        print("\n👋 Session interrupted by user")
        logger.info("Session interrupted by KeyboardInterrupt")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        logger.error(f"Unexpected error in main: {str(e)}")
    finally:
        # Save session data before exiting
        mcp_client.save_session_data(log_filename)
        logger.info("=== MCP CLIENT SESSION ENDED ===")


if __name__ == "__main__":
    asyncio.run(main())
