import sys
import json
import os

import problems.Add_two_numbers.add_two_numbers_correct as correct_module
import problems.Add_two_numbers.bug1 as buggy_module #Change this to bug2 to test the other bug

RefSolution = correct_module.Solution
BugSolution = buggy_module.Solution

# Helper Stuff!
def array_to_list(arr, ListNodeClass):
    dummy = ListNodeClass()
    current = dummy
    for val in arr:
        current.next = ListNodeClass(val)
        current = current.next
    return dummy.next

def list_to_array(node):
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result

# Tracing stuff, because Python is evil
branch_executions = {}

def trace_branches(frame, event, arg):
    if event != "line":
        return trace_branches
    co = frame.f_code
    filename = os.path.abspath(co.co_filename)
    lineno = frame.f_lineno
    if filename not in branch_executions:
        branch_executions[filename] = set()
    branch_executions[filename].add(lineno)
    return trace_branches

# Test Runner
def run_solution(SolutionClass, ListNodeClass, tests, file_path):
    results = []
    abs_path = os.path.abspath(file_path)
    print(f"\n[DEBUG] Using absolute path for tracing:\n  {abs_path}\n")

    for test in tests:
        branch_executions.clear()
        sys.settrace(trace_branches)

        l1 = array_to_list(test["l1"], ListNodeClass)
        l2 = array_to_list(test["l2"], ListNodeClass)
        expected = test["expected"]

        solution = SolutionClass()
        output = solution.addTwoNumbers(l1, l2)

        sys.settrace(None)  # stop tracing
        executed_lines = branch_executions.get(abs_path, set())

        output_array = list_to_array(output)
        passed = output_array == expected

        print(f"Test {test['id']} executed lines: {sorted(executed_lines)}")

        results.append({
            "id": test["id"],
            "passed": passed,
            "executed_lines": executed_lines
        })

    return results

# This right here computes ochiai suspiciousness scores.
def compute_suspiciousness_ochiai(results):
    total_failed = sum(1 for r in results if not r["passed"])
    all_lines = set(line for r in results for line in r["executed_lines"])
    suspiciousness = {}

    for line in sorted(all_lines):
        EF = sum(1 for r in results if not r["passed"] and line in r["executed_lines"])
        EP = sum(1 for r in results if r["passed"] and line in r["executed_lines"])
        denom = (total_failed * (EF + EP)) ** 0.5
        score = 0.0 if denom == 0 else EF / denom
        suspiciousness[line] = score

    return suspiciousness, all_lines, total_failed

# Main (this stuff gets exec'd!)
with open("problems/Add_two_numbers/tests.json") as f:
    tests = json.load(f)

correct_file = os.path.abspath("problems/Add_two_numbers/add_two_numbers_correct.py")
buggy_file   = os.path.abspath("problems/Add_two_numbers/bug1.py")
buggy_filetwo = os.path.abspath("problems/Add_two_numbers/bug2.py")
buggy_filethree = os.path.abspath("problems/Add_two_numbers/bug3.py")
buggy_filefour = os.path.abspath("problems/Add_two_numbers/bug4.py")


print("Running CORRECT solution...")
ref_results = run_solution(
    RefSolution,
    correct_module.ListNode,
    tests,
    correct_file
)

print("\nRunning BUGGY solution...")
bug_results = run_solution(
    BugSolution,
    buggy_module.ListNode,
    tests,
    buggy_file
)
"""
# I can't figure out how to get this to work with two buggy files at once...
print("\nRunning SECOND BUGGY solution...")
bug_results_two = run_solution(
    BugSolution,
    buggy_module.ListNode,
    tests,
    buggy_filetwo
)
"""
susp_scores, all_lines, total_failed = compute_suspiciousness_ochiai(bug_results)

print(f"\nFAILED TESTS: {total_failed}/{len(bug_results)}")

print("\n=== Suspiciousness (Ochiai) ===")
for line in sorted(all_lines):
    print(f"Line {line:3d}: {susp_scores.get(line, 0):.2f}")

print("\n=== Ranked (Most Suspicious First) ===")
ranked = sorted(susp_scores.items(), key=lambda x: x[1], reverse=True)
for line, score in ranked:
    print(f"Line {line:3d}: {score:.2f}")
