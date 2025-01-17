Inputs (Columns 1–11)
Scenario
A label or name for this row’s scenario (e.g., “Scenario A”, “Scenario B”).
- Use this to distinguish between different utilisation assumptions or different teams.

Your Utilisation (rho_you)
The fraction (0 to 1) of your (or your team’s) total capacity that is already occupied.
- Example: 0.5 = 50% utilised, 0.9 = 90% utilised.

Their Utilisation (rho_them)
The fraction (0 to 1) of another team’s/person’s capacity that is in use.
- Example: If you rely on someone else who is 80% busy, you’d put 0.8.

Requests per Week (lambda)
How many times per week you need something—information, sign-off, access, or decisions—from another person/team.
- This figure directly multiplies your per-request overhead and wait time to produce a total weekly delay.

Base Wait Time (hrs) at Ref Util
The observed or estimated wait time per request at some known “Reference Utilisation.”
- For instance, if at 50% utilisation you typically wait 2 hours for a response, then 2.0 goes here.

Ref Util (%) for Base Measure
The utilisation level at which you originally measured the Base Wait Time.
- If you measured it at 50% utilisation, you’d put 0.50.

Context Switch Base (hrs)
The baseline overhead (in hours) for context switching per request, measured at the reference utilisation.
- For example, 0.2 hours (12 minutes) is how much time you spend “switching tasks” when utilisation is at the reference level.

Decision Overhead Base (hrs)
The baseline overhead (in hours) for decision-making per request, at the reference utilisation.
- For example, 0.1 hours might be the time for a quick approval at the reference level.

Context Scaling Factor (k)
A multiplier indicating how context-switching overhead increases (or decreases) as utilisation changes away from the reference.
- If 
𝑘
=
1.0
k=1.0, doubling utilisation relative to the reference doubles the context-switching overhead.

Decision Scaling Factor (m)
A multiplier indicating how decision-making overhead scales with utilisation changes.
- If 
𝑚
=
1.0
m=1.0, doubling utilisation relative to the reference doubles the decision overhead.

Cost of Delay (£ per hour)
How much each hour of delay costs in monetary terms.
- This can represent lost revenue, opportunity cost, or fully-loaded labour cost.

Calculated Outputs (Columns 12–16)
Per-Request Wait Time (hrs)

A formula that scales your Base Wait Time to the current utilisation level.
Typically, a ratio-based approach is used (such as:
Per-Request Wait Time
=
Base Wait Time
×
1
−
Ref Util
 
1
−
𝜌
you
 
Per-Request Wait Time=Base Wait Time× 
1−ρ 
you
​
 
1−Ref Util
​
 
) to illustrate how wait time becomes disproportionately longer as 
𝜌
you
ρ 
you
​
  approaches 1.
Per-Request Context Overhead (hrs)

The context-switch cost per request, scaled by your current utilisation:
=
Context Switch Base
×
(
𝜌
you
Ref Util
)
×
𝑘
=Context Switch Base×( 
Ref Util
ρ 
you
​
 
​
 )×k
Per-Request Decision Overhead (hrs)

The decision-making overhead per request, similarly scaled:
=
Decision Overhead Base
×
(
𝜌
you
Ref Util
)
×
𝑚
=Decision Overhead Base×( 
Ref Util
ρ 
you
​
 
​
 )×m
Total Delay (hrs/week)

The total hours of delay per week, factoring in how many requests arrive:
=
(
Per-Request Wait
+
Context Overhead
+
Decision Overhead
)
×
Requests per Week
=(Per-Request Wait+Context Overhead+Decision Overhead)×Requests per Week
Total Cost (£/week)

Converts the total weekly delay into a monetary figure:
=
Total Delay (hrs/week)
×
Cost of Delay (£ per hour)
=Total Delay (hrs/week)×Cost of Delay (£ per hour)
This helps quantify, in pounds, the financial impact of having a high volume of requests and high utilisation.


Putting It All Together
Columns 1–11: Input parameters for each scenario—who is busy, how many requests there are, what the baseline overheads are, and how costs scale.
Columns 12–16: Formula-driven outputs showing the per-request delays (wait, context, decision) multiplied by Requests per Week to produce a weekly time cost, and then converted into a Total Cost in pounds per week.
By comparing rows (multiple scenarios), you can demonstrate how different utilisation levels or numbers of requests drastically affect total delays and costs.
