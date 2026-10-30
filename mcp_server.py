# -*- coding: utf-8 -*-
"""
GenPark Student Space MCP Server
FastMCP standard interface for SuperMemo SM-2 calculations, retention forecasting, and Rasch IRT calibration.
"""

import json
from typing import Dict, Any
from client import GenParkStudentSpace

try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("genpark-student-space")
except ImportError:
    class MockFastMCP:
        def __init__(self, name):
            self.name = name
        def tool(self):
            def decorator(f):
                return f
            return decorator
    mcp = MockFastMCP("genpark-student-space")

student = GenParkStudentSpace()

@mcp.tool()
def calculate_sm2_interval_and_ease(
    repetition_count: int,
    previous_interval_days: int,
    previous_ease_factor: float = 2.5,
    response_quality: int = 4
) -> str:
    """
    Calculates next review interval and new ease factor using SuperMemo SM-2 algorithm.
    """
    res = student.calculate_sm2_interval_and_ease(repetition_count, previous_interval_days, previous_ease_factor, response_quality)
    return json.dumps(res, indent=2)

@mcp.tool()
def forecast_ebbinghaus_retention(
    memory_stability_days: float = 14.0,
    elapsed_days: float = 5.0
) -> str:
    """
    Forecasts probability of recall using exponential Ebbinghaus forgetting curve.
    """
    res = student.forecast_ebbinghaus_retention(memory_stability_days, elapsed_days)
    return json.dumps(res, indent=2)

@mcp.tool()
def calibrate_rasch_item_difficulty(
    student_ability_theta: float = 1.2,
    item_difficulty_beta: float = 0.8
) -> str:
    """
    Computes probability of correct answer using Rasch 1-parameter Item Response Theory.
    """
    res = student.calibrate_rasch_item_difficulty(student_ability_theta, item_difficulty_beta)
    return json.dumps(res, indent=2)

def main():
    print("Testing Student Space:")
    print(calculate_sm2_interval_and_ease(2, 6, 2.5, 5))

if __name__ == "__main__":
    main()
