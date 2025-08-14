from pydantic import BaseModel
from typing import Dict, List

class BudgetInput(BaseModel):
    monthly_income: float
    rent: float
    utilities: float
    insurance: float
    food: float
    transportation: float
    entertainment: float
    other: float

class BudgetAnalysis(BaseModel):
    total_expenses: float
    remaining: float
    breakdown: Dict[str, float]
    rule_50_30_20: Dict[str, Dict[str, float]]  # {Needs/Wants/Savings: {target, actual}}

class SavingsInput(BaseModel):
    target_amount: float
    current_amount: float
    monthly_contribution: float

class SavingsProjection(BaseModel):
    progress_pct: float
    remaining: float
    months_to_goal: float
    projection_12mo: List[float]

class InvestInput(BaseModel):
    initial_investment: float
    monthly_investment: float
    annual_return_pct: float
    years: int

class InvestOutput(BaseModel):
    total_future_value: float
    total_invested: float
    total_gains: float


def analyze_budget(data: BudgetInput) -> BudgetAnalysis:
    total_expenses = data.rent + data.utilities + data.insurance + data.food + data.transportation + data.entertainment + data.other
    remaining = data.monthly_income - total_expenses
    breakdown = {
        "Rent/Mortgage": data.rent,
        "Utilities": data.utilities,
        "Insurance": data.insurance,
        "Food": data.food,
        "Transportation": data.transportation,
        "Entertainment": data.entertainment,
        "Other": data.other,
    }
    needs_target = data.monthly_income * 0.5
    wants_target = data.monthly_income * 0.3
    savings_target = data.monthly_income * 0.2
    needs_actual = data.rent + data.utilities + data.insurance + data.food
    wants_actual = data.transportation + data.entertainment + data.other
    savings_actual = max(remaining, 0)
    return BudgetAnalysis(
        total_expenses=total_expenses,
        remaining=remaining,
        breakdown=breakdown,
        rule_50_30_20={
            "Needs": {"target": needs_target, "actual": needs_actual},
            "Wants": {"target": wants_target, "actual": wants_actual},
            "Savings": {"target": savings_target, "actual": savings_actual},
        },
    )


def project_savings(data: SavingsInput) -> SavingsProjection:
    progress_pct = (data.current_amount / data.target_amount * 100) if data.target_amount > 0 else 0.0
    remaining = data.target_amount - data.current_amount
    months_to_goal = (remaining / data.monthly_contribution) if data.monthly_contribution > 0 else float("inf")
    # 12 month simple projection capped by target
    projection = []
    current = data.current_amount
    for i in range(12):
        current = min(current + data.monthly_contribution, data.target_amount)
        projection.append(current)
    return SavingsProjection(
        progress_pct=progress_pct,
        remaining=remaining,
        months_to_goal=months_to_goal,
        projection_12mo=projection,
    )


def invest_calculate(data: InvestInput) -> InvestOutput:
    monthly_rate = (data.annual_return_pct / 100.0) / 12.0
    months = data.years * 12
    fv_initial = data.initial_investment * ((1 + data.annual_return_pct/100.0) ** data.years)
    fv_monthly = data.monthly_investment * (((1 + monthly_rate) ** months - 1) / monthly_rate) if monthly_rate > 0 else data.monthly_investment * months
    total_future_value = fv_initial + fv_monthly
    total_invested = data.initial_investment + (data.monthly_investment * months)
    total_gains = total_future_value - total_invested
    return InvestOutput(
        total_future_value=total_future_value,
        total_invested=total_invested,
        total_gains=total_gains,
    )

