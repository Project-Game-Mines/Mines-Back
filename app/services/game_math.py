from decimal import Decimal, getcontext

getcontext().prize = 28

def calculate_prize(
    bet_amount: float, 
    steps: int, 
    total_cells: int,
    total_mines: int,
    house_edge: float = 0.02
):

    if steps < 0:
        raise ValueError("steps deve ser maior ou igual a 0")
    
    safe_cells = total_cells - total_mines

    if steps > safe_cells:
        return {
            "error": "Steps maior que safe_cells",
            "safe_cells": safe_cells
        }
    
    if steps == 0:
        return {
            "prob_survive": 1.0,
            "fair_multiplier": 1.0,
            "multiplier_after_house_edge": round(1.0(1 - house_edge), 6),
            "prize": round(bet_amount * (1 - house_edge), 2)
        }
    
    prob = Decimal(1)
    for i in range(steps):
        num = Decimal(safe_cells - i)
        den = Decimal(total_cells - i)
        prob *= (num / den)

    prob_float = float(prob)

    fair_multiplier = 1 / prob_float if prob_float > 0 else float("inf")
    multiplier_after_house_edge = fair_multiplier * (1 - house_edge)

    prize = bet_amount * (1 - house_edge) / prob_float if prob_float > 0 else float("inf")

    return {
        "prob_survive": round(prob_float, 10),
        "fair_multiplier": round(fair_multiplier, 6),
        "multiplier_after_house_edge": round(multiplier_after_house_edge, 6),
        "prize": round(prize, 2)
    }
