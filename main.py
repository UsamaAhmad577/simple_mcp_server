import os
import time
import logging
from mcp.server.fastmcp import FastMCP, Context

# 1. Configure logging FIRST before instantiating FastMCP
script_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(script_dir, "mcp_server.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=log_file_path,
    filemode='a'
)

logger = logging.getLogger(__name__)

# 2. Instantiate FastMCP after logging configuration
mcp = FastMCP("add_integers")


class MCPError(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")


@mcp.tool()
def add(a: int, b: int) -> int:
    """
    add two integers and return the sum
    """
    logger.info(f"adding {a} and {b}")
    result = a + b
    logger.info(f"Result is {result}")
    return result


@mcp.tool()
def divide(a: int, b: int) -> float:
    """
    divide two integers
    a: numerator 
    b: denominator
    return : result of division
    """
    if b == 0:
        raise MCPError(code=400, message="division by zero not allowed")
    return a / b


@mcp.tool()
def long_process(steps: int) -> str:
    """
    simulate a long running process
    """
    for i in range(steps):
        logger.info(f"processing step {i+1} of {steps}")
        time.sleep(0.1)
    return "process complete"


if __name__ == "__main__":
    logger.info("Starting MCP server...")
    mcp.run(transport='stdio')