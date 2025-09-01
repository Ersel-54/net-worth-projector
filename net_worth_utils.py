import pandas as pd
from datetime import datetime


def project_net_worth(
    start_net_worth: float,
    annual_interest_rate: float,
    income_streams: list,
    monthly_expenses: float,
    years: int,
):
    """Project net worth over time with multiple income streams.

    Args:
        start_net_worth (float): Initial net worth at day 0.
        annual_interest_rate (float): Annual interest rate as a decimal
            (e.g., 0.05 for 5%).
        income_streams (list[dict]): A list of dictionaries, each
            containing:
            - 'monthly_income' (float): Monthly income amount.
            - 'annual_growth_rate' (float): Annual growth rate as a
              decimal.
            - 'terminal_value' (float): Maximum value the income stream
              can reach.
        monthly_expenses (float): Monthly expenses to deduct.
        years (int): Number of years to project.

    Returns:
        pd.DataFrame: A DataFrame with monthly net worth.
    """
    assert years >= 0
    assert monthly_expenses >= 0

    months = years * 12
    monthly_interest_rate = (1 + annual_interest_rate) ** (1 / 12) - 1

    net_worth = start_net_worth
    net_worth_over_time = []
    dates = [datetime.today() + pd.DateOffset(months=i) for i in range(months)]

    for month in range(months):
        # Compound net worth monthly.
        net_worth *= 1 + monthly_interest_rate

        # Deduct monthly expenses.
        net_worth -= monthly_expenses

        # Add income streams.
        for income_stream in income_streams:
            monthly_income = income_stream["monthly_income"]
            monthly_growth_rate = (
                1 + income_stream.get("annual_growth_rate", 0)
            ) ** (1 / 12) - 1

            # Contribution for this month.
            contribution = monthly_income * (
                (1 + monthly_growth_rate) ** month
            )

            # Enforce the terminal value.
            terminal_value = income_stream.get("terminal_value")
            if terminal_value is not None:
                contribution = min(contribution, terminal_value)

            # Add the contribution to net worth.
            net_worth += contribution

        net_worth_over_time.append(net_worth)

    df = pd.DataFrame({"Date": dates, "Net Worth": net_worth_over_time})

    return df


def find_net_worth_milestone(
    df: pd.DataFrame, target: float
) -> datetime | None:
    """Find the first date when the net worth reaches or exceeds a target.

    Args:
        df (pd.DataFrame): DataFrame with columns 'Date' and 'Net Worth'.
        target (float): The net worth milestone to find.

    Returns:
        datetime | None: The first date the milestone is reached, or
            None if not reached.
    """
    target_rows = df[df["Net Worth"] >= target]
    if target_rows.empty:
        return None

    milestone_idx = target_rows.index[0]
    return df.loc[milestone_idx, "Date"]
