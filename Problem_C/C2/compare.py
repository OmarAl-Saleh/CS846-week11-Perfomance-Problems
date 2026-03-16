import subprocess
import sys
import re

def extract_time(output):
    match = re.search(r"Time:\s+([\d.]+)s", output)
    return float(match.group(1)) if match else None

print("=" * 50)
print("YOUR SOLUTION")
print("=" * 50)
r1 = subprocess.run([sys.executable, "your_solution.py"], capture_output=True, text=True)
print(r1.stdout)
if r1.stderr:
    print(r1.stderr)

print("=" * 50)
print("OPTIMAL SOLUTION")
print("=" * 50)
r2 = subprocess.run([sys.executable, "helpers/optimal_solution.pyc"], capture_output=True, text=True)
print(r2.stdout)
if r2.stderr:
    print(r2.stderr)

t1 = extract_time(r1.stdout)
t2 = extract_time(r2.stdout)

if t1 and t2 and t2 > 0:
    print("=" * 50)
    print("COMPARISON")
    print("=" * 50)
    speedup = t1 / t2
    slower_pct = ((t1 - t2) / t2) * 100
    print(f"Your solution:    {t1:.3f}s")
    print(f"Optimal solution: {t2:.3f}s")
    print(f"Optimal is {speedup:.1f}x faster ({slower_pct:.0f}% faster)")
