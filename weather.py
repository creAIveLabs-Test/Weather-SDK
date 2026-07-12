from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("weather")  # server name clients will see

HEADERS = {"User-Agent": "weather-mcp/0.1 (learning project)"}  # NWS API requires this


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """US weather forecast for a lat/lon. Use for any weather question."""
    async with httpx.AsyncClient(headers=HEADERS, timeout=15) as c:
        pt = await c.get(f"https://api.weather.gov/points/{latitude},{longitude}")
        pt.raise_for_status()
        fc = await c.get(pt.json()["properties"]["forecast"])
        fc.raise_for_status()
        p = fc.json()["properties"]["periods"][0]
        return p["name"] + ": " + p["detailedForecast"]


if __name__ == "__main__":
    mcp.run(transport="stdio")  # local transport for Claude Desktop / Claude Code
