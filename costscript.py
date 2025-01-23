#!/usr/bin/env python3
import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

# We’ll store two HTML templates inline:
# 1) A Bootstrap-based form for Current State vs. Future State
# 2) A results page with cards showing each scenario side by side

form_html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Queueing Calculator - Compare Current & Future</title>
  <!-- Bootstrap 5 CSS (CDN) -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      margin: 20px;
    }
    .scenario-card {
      margin-bottom: 2rem;
      border: 1px solid #ddd;
      padding: 1rem;
      border-radius: 8px;
    }
    label {
      font-weight: 500;
      margin-top: 0.5rem;
    }
    .scenario-title {
      margin-bottom: 1rem;
      font-weight: 600;
      font-size: 1.25rem;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1 class="my-4">Queueing Calculator</h1>
    <p class="text-secondary">Compare <strong>Current</strong> vs. <strong>Future</strong> states with a more polished UI.</p>
    
    <form method="POST" action="/" class="row g-4">
      <!-- Current State -->
      <div class="col-12 col-lg-6 scenario-card">
        <div class="scenario-title">Current State</div>
        
        <label for="rho_you_cur">Your Utilisation (0.0 - 1.0)</label>
        <input type="number" step="0.01" id="rho_you_cur" name="rho_you_cur"
               class="form-control" placeholder="0.50" value="0.50" required>
        
        <label for="requests_cur">Requests per Week</label>
        <input type="number" step="1" id="requests_cur" name="requests_cur"
               class="form-control" placeholder="5" value="5" required>
        
        <label for="base_wait_time_cur">Base Wait Time (hrs) at Ref Util</label>
        <input type="number" step="0.01" id="base_wait_time_cur" name="base_wait_time_cur"
               class="form-control" placeholder="2.0" value="2.0" required>
        
        <label for="ref_util_cur">Ref Util (0.0 - 1.0)</label>
        <input type="number" step="0.01" id="ref_util_cur" name="ref_util_cur"
               class="form-control" placeholder="0.50" value="0.50" required>
        
        <label for="cost_of_delay_cur">Cost of Delay (£ per hour)</label>
        <input type="number" step="0.01" id="cost_of_delay_cur" name="cost_of_delay_cur"
               class="form-control" placeholder="100" value="100" required>
        
        <label for="willing_to_pay_cur">Willing to Pay (£/week)</label>
        <input type="number" step="0.01" id="willing_to_pay_cur" name="willing_to_pay_cur"
               class="form-control" placeholder="0" value="0" required>
      </div>
      
      <!-- Future State -->
      <div class="col-12 col-lg-6 scenario-card">
        <div class="scenario-title">Future State</div>
        
        <label for="rho_you_fut">Your Utilisation (0.0 - 1.0)</label>
        <input type="number" step="0.01" id="rho_you_fut" name="rho_you_fut"
               class="form-control" placeholder="0.90" value="0.90" required>
        
        <label for="requests_fut">Requests per Week</label>
        <input type="number" step="1" id="requests_fut" name="requests_fut"
               class="form-control" placeholder="5" value="5" required>
        
        <label for="base_wait_time_fut">Base Wait Time (hrs) at Ref Util</label>
        <input type="number" step="0.01" id="base_wait_time_fut" name="base_wait_time_fut"
               class="form-control" placeholder="2.0" value="2.0" required>
        
        <label for="ref_util_fut">Ref Util (0.0 - 1.0)</label>
        <input type="number" step="0.01" id="ref_util_fut" name="ref_util_fut"
               class="form-control" placeholder="0.50" value="0.50" required>
        
        <label for="cost_of_delay_fut">Cost of Delay (£ per hour)</label>
        <input type="number" step="0.01" id="cost_of_delay_fut" name="cost_of_delay_fut"
               class="form-control" placeholder="100" value="100" required>
        
        <label for="willing_to_pay_fut">Willing to Pay (£/week)</label>
        <input type="number" step="0.01" id="willing_to_pay_fut" name="willing_to_pay_fut"
               class="form-control" placeholder="500" value="500" required>
      </div>
      
      <div class="col-12 text-end">
        <button type="submit" class="btn btn-primary btn-lg">Calculate Both</button>
      </div>
    </form>
  </div>
</body>
</html>
"""

result_html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Queueing Comparison Results</title>
  <!-- Bootstrap 5 CSS (CDN) -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body { margin: 20px; }
    .scenario-card {
      border: 1px solid #ddd;
      padding: 1rem;
      border-radius: 8px;
      margin-bottom: 2rem;
    }
    .scenario-card h3 { margin-top: 0.5rem; }
    .summary-table {
      width: 100%%;
      border-collapse: collapse;
      margin-top: 1rem;
    }
    .summary-table th, .summary-table td {
      border: 1px solid #ccc;
      padding: 0.75rem;
      text-align: left;
    }
    .scenario-title {
      font-weight: 600;
      font-size: 1.25rem;
      margin-bottom: 1rem;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1 class="my-4">Comparison of Current vs. Future State</h1>
    <p class="text-secondary">A side-by-side look at queueing metrics, using a Bootstrap-based layout.</p>
    
    <div class="row">
      <div class="col-12 col-lg-6 scenario-card">
        <div class="scenario-title">Current State</div>
        <p><strong>Your Utilisation:</strong> {{ rho_you_cur }}</p>
        <p><strong>Requests/Week:</strong> {{ requests_cur }}</p>
        <p><strong>Base Wait Time:</strong> {{ base_wait_time_cur }} hrs <small>(Ref Util: {{ ref_util_cur }})</small></p>
        <p><strong>Cost of Delay:</strong> £{{ cost_of_delay_cur }}/hr</p>
        <p><strong>Willing to Pay:</strong> £{{ willing_to_pay_cur }}/week</p>
        <hr>
        <h3>Results</h3>
        <table class="summary-table">
          <tr>
            <th>Per-Request Wait Time</th>
            <td>{{ wait_cur }} hrs</td>
          </tr>
          <tr>
            <th>Total Delay</th>
            <td>{{ delay_cur }} hrs/week</td>
          </tr>
          <tr>
            <th>Total Delay Cost</th>
            <td>£{{ cost_cur }}/week</td>
          </tr>
          <tr>
            <th>Net Trade-Off</th>
            <td>£{{ net_cur }}/week</td>
          </tr>
        </table>
      </div>
      
      <div class="col-12 col-lg-6 scenario-card">
        <div class="scenario-title">Future State</div>
        <p><strong>Your Utilisation:</strong> {{ rho_you_fut }}</p>
        <p><strong>Requests/Week:</strong> {{ requests_fut }}</p>
        <p><strong>Base Wait Time:</strong> {{ base_wait_time_fut }} hrs <small>(Ref Util: {{ ref_util_fut }})</small></p>
        <p><strong>Cost of Delay:</strong> £{{ cost_of_delay_fut }}/hr</p>
        <p><strong>Willing to Pay:</strong> £{{ willing_to_pay_fut }}/week</p>
        <hr>
        <h3>Results</h3>
        <table class="summary-table">
          <tr>
            <th>Per-Request Wait Time</th>
            <td>{{ wait_fut }} hrs</td>
          </tr>
          <tr>
            <th>Total Delay</th>
            <td>{{ delay_fut }} hrs/week</td>
          </tr>
          <tr>
            <th>Total Delay Cost</th>
            <td>£{{ cost_fut }}/week</td>
          </tr>
          <tr>
            <th>Net Trade-Off</th>
            <td>£{{ net_fut }}/week</td>
          </tr>
        </table>
      </div>
    </div>
    
    <div class="text-end">
      <a href="/" class="btn btn-secondary">Back to Form</a>
    </div>
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def form():
    """Show a Bootstrap-based form for Current & Future state."""
    return render_template_string(form_html)

@app.route("/", methods=["POST"])
def calculate():
    """Calculate queueing metrics for both scenarios and display with Bootstrap styling."""
    # --- Current State ---
    rho_you_cur = float(request.form["rho_you_cur"])
    requests_cur = float(request.form["requests_cur"])
    base_wait_time_cur = float(request.form["base_wait_time_cur"])
    ref_util_cur = float(request.form["ref_util_cur"])
    cost_of_delay_cur = float(request.form["cost_of_delay_cur"])
    willing_to_pay_cur = float(request.form["willing_to_pay_cur"])
    
    # Calculate wait time for current scenario
    if (1 - rho_you_cur) == 0:
        wait_cur = 999999.9
    else:
        wait_cur = base_wait_time_cur * ((1 - ref_util_cur) / (1 - rho_you_cur))
    delay_cur = wait_cur * requests_cur
    cost_cur = delay_cur * cost_of_delay_cur
    net_cur = willing_to_pay_cur - cost_cur

    # --- Future State ---
    rho_you_fut = float(request.form["rho_you_fut"])
    requests_fut = float(request.form["requests_fut"])
    base_wait_time_fut = float(request.form["base_wait_time_fut"])
    ref_util_fut = float(request.form["ref_util_fut"])
    cost_of_delay_fut = float(request.form["cost_of_delay_fut"])
    willing_to_pay_fut = float(request.form["willing_to_pay_fut"])
    
    # Calculate wait time for future scenario
    if (1 - rho_you_fut) == 0:
        wait_fut = 999999.9
    else:
        wait_fut = base_wait_time_fut * ((1 - ref_util_fut) / (1 - rho_you_fut))
    delay_fut = wait_fut * requests_fut
    cost_fut = delay_fut * cost_of_delay_fut
    net_fut = willing_to_pay_fut - cost_fut

    # Render results
    return render_template_string(
        result_html,
        # Current scenario
        rho_you_cur=rho_you_cur,
        requests_cur=requests_cur,
        base_wait_time_cur=base_wait_time_cur,
        ref_util_cur=ref_util_cur,
        cost_of_delay_cur=cost_of_delay_cur,
        willing_to_pay_cur=willing_to_pay_cur,
        
        wait_cur=round(wait_cur, 2),
        delay_cur=round(delay_cur, 2),
        cost_cur=round(cost_cur, 2),
        net_cur=round(net_cur, 2),

        # Future scenario
        rho_you_fut=rho_you_fut,
        requests_fut=requests_fut,
        base_wait_time_fut=base_wait_time_fut,
        ref_util_fut=ref_util_fut,
        cost_of_delay_fut=cost_of_delay_fut,
        willing_to_pay_fut=willing_to_pay_fut,
        
        wait_fut=round(wait_fut, 2),
        delay_fut=round(delay_fut, 2),
        cost_fut=round(cost_fut, 2),
        net_fut=round(net_fut, 2)
    )

if __name__ == "__main__":
    # For local testing:
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
