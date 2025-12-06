# Bug Localization in LeetCode-Style Algorithms Using Spectrum-Based Fault Localization (SBFL)

## Project Overview
This project uses a debugging algorithm designed to localize bugs in LeetCode style algorithm challenge Add Two Numbers.
We use Spectrum-Based Fault Localization (SBFL) with execution tracing to rank lines of code by their suspiciousness, showing us where bugs are most likely located.

## How it works
**1. Execution Tracing**

for each test case, we record:
- which lines execute in the passing runs
- which lines execute in the fialing runs

**2. Suspiciousness Scoring**

lines are ranked using SBFL's Ochiai formula:

$suspiciousness = \frac{failed_executions}{\sqrt{TotalFailed \cdot (Failed Executions + passed Executions)}}$
A score near 1.0 -> highly suspicious
A score near 0.0 -> likely not involved

**3. Bug Localization Output**

System output example:

<img width="312" height="88" alt="image" src="https://github.com/user-attachments/assets/581b9ab5-136f-417a-ba8a-f31846c12a49" />


## Bug Files Included
We created 4 bugs, each showign a realistic bug type

**Bug 1 - Incorrect Branch Logic**

 \# BUG: Only multiply val1 if > 5
 
            if val1 > 5:
                out = val1 * 2        # <-- now on a separate line
                out += val2            # <-- separate
                out += carry           # <-- separate
            else:
                out = val1 + val2 + carry


**Bug 2 - Double Carry Addition**

\# BUG: carry added twice if both nodes exist

            if l1 and l2:
                out = val1 + val2 + carry + carry  # <-- duplicated carry
            else:
                out = val1 + val2 + carry

**Bug 3 - Incorrect Digit Normalization

