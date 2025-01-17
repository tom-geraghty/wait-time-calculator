Queueing Calculator README
This Python script (costscript.py) creates an Excel spreadsheet that demonstrates how increased utilisation and multiple weekly requests lead to longer wait times, higher context-switching and decision overheads, and ultimately higher costs of delay.

Contents
Requirements
Installation
Usage
Spreadsheet Columns
Examples
Troubleshooting
Requirements
Python 3.7+
The script uses the openpyxl library, which works with Python 3.7 and above.
openpyxl library
Required for writing Excel files. If you do not already have it installed, follow the instructions below.
Installation
Install Python 3

If you’re on macOS and using Homebrew, you can install Python with:
bash
Copy
brew install python
Alternatively, download and install from python.org.
Create a virtual environment (recommended)

bash
Copy
python3 -m venv venv
source venv/bin/activate
This ensures any libraries you install do not affect other Python projects.

Install openpyxl

bash
Copy
pip install openpyxl
If you prefer to install system-wide (and understand the potential implications), you can omit the virtual environment. However, using a virtual environment is the safer option.

Download or clone this repository

Place the costscript.py file in a directory of your choice.
Usage
Activate your virtual environment (if you created one):

bash
Copy
source venv/bin/activate
Run the script:

bash
Copy
python costscript.py
or make it executable and run:

bash
Copy
chmod +x costscript.py
./costscript.py
Check the generated spreadsheet
The script will create a file called queueing_calculator.xlsx in the current directory.
Open it in Excel (or another spreadsheet application) to see the results.

Spreadsheet Columns
The spreadsheet has several columns. Below is an overview:

Scenario
A label or name for each row’s scenario (e.g., “Scenario A”).

Your Utilisation (rho_you)
The fraction of your (or your team’s) time that is utilised (e.g., 0.50 for 50%).

Their Utilisation (rho_them)
The fraction of another team’s time that is utilised (e.g., 0.80 for 80%).

Requests per Week (lambda)
How many times per week you require a sign-off, decision, or information from the other team.

Base Wait Time (hrs) at Ref Util
The observed wait time per request at the reference utilisation level. For instance, if you found that at 50% utilisation, each request typically waits 2 hours, you put 2.0.

Ref Util (%) for Base Measure
The utilisation level at which the Base Wait Time was measured. For example, 0.50 if you measured it at 50% utilisation.

Context Switch Base (hrs)
The baseline overhead (in hours) for switching contexts, measured at the reference utilisation.
For instance, 0.2 hours (12 minutes).

Decision Overhead Base (hrs)
The baseline overhead (in hours) for making decisions, measured at the reference utilisation.
For instance, 0.1 hours.

Context Scaling Factor (k)
A multiplier that indicates how much more (or less) the context-switch overhead scales as utilisation increases.
If 
𝑘
=
1.0
k=1.0, doubling utilisation from the reference doubles the overhead.

Decision Scaling Factor (m)
A multiplier for how decision overhead scales with changes in utilisation.
If 
𝑚
=
1.0
m=1.0, doubling utilisation from the reference doubles the decision overhead.

Cost of Delay (£ per hour)
The cost (in pounds per hour) that represents lost opportunity, delayed revenue, or other costs associated with waiting.

Per-Request Wait Time (hrs)
Calculated from the Base Wait Time by scaling up or down according to your current utilisation versus the reference.

Per-Request Context Overhead (hrs)
How much context-switch time is incurred per request, scaled by utilisation and the Context Scaling Factor.

Per-Request Decision Overhead (hrs)
How much decision-making time is incurred per request, also scaled by utilisation.

Total Delay (hrs/week)
The combined wait time, context switching, and decision overhead multiplied by the number of weekly requests.

Total Cost (£/week)
The total delay (in hours per week) multiplied by the Cost of Delay (£ per hour), giving a weekly financial impact.

Examples
Example Scenario A
Your Utilisation: 50%
Their Utilisation: 50%
Requests per Week: 5
Base Wait Time (hrs): 2.0
Ref Util: 0.50
Context Switch Base: 0.20 hrs
Decision Overhead Base: 0.10 hrs
Context Scaling Factor (k): 1.0
Decision Scaling Factor (m): 1.0
Cost of Delay: £100/hr
Example Scenario B
Your Utilisation: 90%
Their Utilisation: 80%
Requests per Week: 10
Base Wait Time (hrs): 2.0
Ref Util: 0.50
Context Switch Base: 0.20 hrs
Decision Overhead Base: 0.10 hrs
Context Scaling Factor (k): 1.0
Decision Scaling Factor (m): 1.0
Cost of Delay: £100/hr
By comparing these scenarios in the final spreadsheet, you’ll see how the higher utilisation and number of requests in Scenario B significantly increase total delay and cost per week.


Thanks for using the Queueing Calculator!
We hope it helps illuminate how heavily-utilised teams and frequent requests can blow up wait times and costs. Feel free to modify the spreadsheet formulas to better suit your organisation’s specific context, or add additional rows/scenarios for deeper analyses.
