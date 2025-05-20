#!/usr/bin/env python3
"""Simple tool to analyze financial statements.

This script reads a JSON file containing an income statement and balance
sheet and prints a few common financial ratios.
"""

import json
import sys
from dataclasses import dataclass


@dataclass
class IncomeStatement:
    revenue: float
    cost_of_goods_sold: float
    operating_expenses: float
    interest_expense: float
    taxes: float


@dataclass
class BalanceSheet:
    current_assets: float
    current_liabilities: float
    total_assets: float
    total_liabilities: float
    shareholder_equity: float


def compute_ratios(income: IncomeStatement, balance: BalanceSheet) -> dict:
    """Return a dictionary of financial ratios."""
    gross_profit = income.revenue - income.cost_of_goods_sold
    net_income = (
        income.revenue
        - income.cost_of_goods_sold
        - income.operating_expenses
        - income.interest_expense
        - income.taxes
    )

    gross_margin = gross_profit / income.revenue if income.revenue else 0
    operating_margin = (
        (income.revenue - income.cost_of_goods_sold - income.operating_expenses)
        / income.revenue
        if income.revenue
        else 0
    )
    return_on_assets = net_income / balance.total_assets if balance.total_assets else 0
    return_on_equity = (
        net_income / balance.shareholder_equity if balance.shareholder_equity else 0
    )
    current_ratio = (
        balance.current_assets / balance.current_liabilities
        if balance.current_liabilities
        else 0
    )
    debt_to_equity = (
        balance.total_liabilities / balance.shareholder_equity
        if balance.shareholder_equity
        else 0
    )

    return {
        "gross_margin": gross_margin,
        "operating_margin": operating_margin,
        "net_income": net_income,
        "return_on_assets": return_on_assets,
        "return_on_equity": return_on_equity,
        "current_ratio": current_ratio,
        "debt_to_equity": debt_to_equity,
    }


def load_financials(path: str) -> tuple:
    """Load financial statements from a JSON file."""
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    income = IncomeStatement(**data["income_statement"])
    balance = BalanceSheet(**data["balance_sheet"])
    return income, balance


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python financial_analyzer.py <financials.json>")
        return 1
    income, balance = load_financials(argv[1])
    ratios = compute_ratios(income, balance)
    for key, value in ratios.items():
        print(f"{key}: {value:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
