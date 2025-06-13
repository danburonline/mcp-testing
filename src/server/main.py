from fastmcp.server import FastMCP
import json
import random
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

mcp: FastMCP = FastMCP("Custom STDIO MCP Server")

# Mock search data for different types of queries
MOCK_SEARCH_RESULTS = {
    "weather": [
        "Today's weather forecast shows sunny skies with temperatures reaching 75°F (24°C) with light winds from the southwest.",
        "Current weather conditions: Clear skies, 72°F (22°C), humidity at 45%, wind speeds of 8 mph.",
        "Weather alert: Partly cloudy conditions expected later today with possible light showers in the evening.",
    ],
    "news": [
        "Breaking: Tech industry sees major breakthrough in renewable energy storage solutions.",
        "Market update: Global stocks show mixed performance amid economic uncertainty.",
        "Sports news: Local team advances to championship finals after impressive victory.",
    ],
    "technology": [
        "Latest AI developments show promising advances in natural language processing capabilities.",
        "New smartphone technology features improved battery life and enhanced camera systems.",
        "Cloud computing trends indicate increased adoption of edge computing solutions.",
    ],
    "health": [
        "Medical research reveals new insights into preventive healthcare practices.",
        "Nutrition study highlights benefits of Mediterranean diet for heart health.",
        "Exercise guidelines updated to include more flexibility and strength training recommendations.",
    ],
    "finance": [
        "Stock market analysis shows tech sector outperforming traditional industries.",
        "Cryptocurrency trends indicate increased institutional adoption and regulatory clarity.",
        "Economic indicators suggest steady growth with moderate inflation expectations.",
    ],
    "general": [
        "Recent studies indicate growing interest in sustainable living practices.",
        "Educational institutions are adapting to new digital learning methodologies.",
        "Travel industry shows signs of recovery with increased domestic tourism.",
    ],
}


def get_search_category(query: str) -> str:
    """Determine the category of search based on query keywords"""
    query_lower = query.lower()

    if any(
        word in query_lower
        for word in ["weather", "temperature", "rain", "sunny", "cloudy", "forecast"]
    ):
        return "weather"
    elif any(
        word in query_lower
        for word in ["news", "breaking", "latest", "current events", "politics"]
    ):
        return "news"
    elif any(
        word in query_lower
        for word in ["technology", "tech", "ai", "computer", "software", "internet"]
    ):
        return "technology"
    elif any(
        word in query_lower
        for word in ["health", "medical", "doctor", "medicine", "fitness", "nutrition"]
    ):
        return "health"
    elif any(
        word in query_lower
        for word in ["finance", "money", "stock", "investment", "crypto", "economy"]
    ):
        return "finance"
    else:
        return "general"


@mcp.tool("search_the_web")
def search_the_web(query: str, max_results: int = 3) -> str:
    """Search the web for real-time information (mocked results for demonstration)"""
    try:
        # Get the appropriate category for the search
        category = get_search_category(query)

        # Get random results from the category
        available_results = MOCK_SEARCH_RESULTS[category]
        num_results = min(max_results, len(available_results))
        selected_results = random.sample(available_results, num_results)

        # Format the response
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        search_results = []

        for i, result in enumerate(selected_results, 1):
            search_results.append(
                {
                    "rank": i,
                    "title": f"Search Result {i}",
                    "snippet": result,
                    "url": f"https://example-source-{i}.com/article-{random.randint(1000, 9999)}",
                    "last_updated": timestamp,
                }
            )

        response = {
            "query": query,
            "search_timestamp": timestamp,
            "results_found": num_results,
            "search_results": search_results,
        }

        # Return formatted JSON string
        return json.dumps(response, indent=2)

    except Exception as e:
        return json.dumps(
            {
                "error": f"Search failed: {str(e)}",
                "query": query,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            },
            indent=2,
        )


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="localhost", port=8080)
