#!/usr/bin/env python3

import sys
print(sys.executable)


import openpyxl
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

def create_queueing_spreadsheet(filename="queueing_calculator.xlsx"):
    """
    Creates an Excel spreadsheet modeling queueing delay, context overhead,
    decision overhead, etc., factoring in requests per week.
    """
    # Create a new workbook and select the active worksheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Queueing Calculator"

    # ------------ HEADER ROW ------------
    headers = [
        "Scenario",
        "Your Utilization (rho_you)",
        "Their Utilization (rho_them)",
        "Requests per Week (lambda)",
        "Base Wait Time (hrs) at Ref Util",
        "Ref Util (%) for base measure",
        "Context Switch Base (hrs)",
        "Decision Overhead Base (hrs)",
        "Context Scaling Factor (k)",
        "Decision Scaling Factor (m)",
        "Cost of Delay (£ per hour)",

        # Calculated columns
        "Per-Request Wait Time (hrs)",      # col 12
        "Per-Request Context Overhead (hrs)", # col 13
        "Per-Request Decision Overhead (hrs)", # col 14
        "Total Delay (hrs/week)",          # col 15
        "Total Cost (£/week)"              # col 16
    ]

    for col_idx, header in enumerate(headers, start=1):
        ws.cell(row=1, column=col_idx, value=header)
        ws.column_dimensions[get_column_letter(col_idx)].width = 28  # widen columns a bit

    # ------------ EXAMPLE SCENARIO ROWS ------------
    # We’ll provide two example scenarios. You can add more rows if you like.

    data_scenario1 = [
        "Scenario A",  # A label
        0.50,          # rho_you
        0.50,          # rho_them
        5,             # Requests/week
        2.0,           # Base Wait Time (hrs)
        0.50,          # Ref Util
        0.20,          # Context Switch Base (hrs)
        0.10,          # Decision Overhead Base (hrs)
        1.0,           # k (context scaling)
        1.0,           # m (decision scaling)
        100.0          # Cost of Delay £/hr
    ]

    data_scenario2 = [
        "Scenario B",
        0.90,  # rho_you
        0.80,  # rho_them
        10,    # Requests/week
        2.0,   # Base Wait Time (hrs)
        0.50,  # Ref Util
        0.20,  # Context Switch Base (hrs)
        0.10,  # Decision Overhead Base (hrs)
        1.0,   # k
        1.0,   # m
        100.0  # Cost of Delay £/hr
    ]

    # Place the example data in rows 2 and 3
    for row_idx, scenario_data in enumerate([data_scenario1, data_scenario2], start=2):
        for col_idx, val in enumerate(scenario_data, start=1):
            ws.cell(row=row_idx, column=col_idx, value=val)

    # ------------ FORMULAS ------------
    # Assign column indices for readability (1-based ind
