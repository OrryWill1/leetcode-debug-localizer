import sys
import json
import os
import multiprocessing
import traceback

import problems.Add_two_numbers.add_two_numbers_correct as correct_module
import problems.Add_two_numbers.bug1 as buggy_module  # Change this to bugX to test the other bug, with X being the number

RefSolution = correct_module.Solution
BugSolution = buggy_module.Solution

# Helper Stuff
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

# Tracing stuff
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

# Worker function for multiprocessing
def run_test_worker(SolutionClass, ListNodeClass, test, file_path, result_queue):
    try:
        branch_executions.clear()
        sys.settrace(trace_branches)

        l1 = array_to_list(test["l1"], ListNodeClass)
        l2 = array_to_list(test["l2"], ListNodeClass)
        expected = test["expected"]

        solution = SolutionClass()
        output = solution.addTwoNumbers(l1, l2)

        sys.settrace(None)
        executed_lines = branch_executions.get(os.path.abspath(file_path), set())
        output_array = list_to_array(output)
        passed = output_array == expected

        result_queue.put({
            "id": test["id"],
            "passed": passed,
            "executed_lines": executed_lines
        })
    except Exception:
        sys.settrace(None)
        result_queue.put({
            "id": test["id"],
            "passed": False,
            "executed_lines": set(),
            "error": traceback.format_exc()
        })

# Test Runner with timeout
def run_solution(SolutionClass, ListNodeClass, tests, file_path, timeout=5):
    results = []
    abs_path = os.path.abspath(file_path)
    print(f"\n[DEBUG] Using absolute path for tracing:\n  {abs_path}\n")

    for test in tests:
        result_queue = multiprocessing.Queue()
        p = multiprocessing.Process(target=run_test_worker, args=(SolutionClass, ListNodeClass, test, file_path, result_queue))
        p.start()
        p.join(timeout)

        if p.is_alive():
            p.terminate()
            p.join()
            print(f"Test {test['id']} terminated due to timeout (possible infinite loop)")
            results.append({
                "id": test["id"],
                "passed": False,
                "executed_lines": set(),
                "timeout": True
            })
        else:
            result = result_queue.get()
            if "error" in result:
                print(f"Test {test['id']} raised an exception:\n{result['error']}")
            results.append(result)

        branch_executions.clear()

    return results

# Compute Ochiai
def compute_suspiciousness_ochiai(results):
    total_failed = sum(1 for r in results if not r.get("passed", False))
    all_lines = set(line for r in results for line in r.get("executed_lines", set()))
    suspiciousness = {}

    for line in sorted(all_lines):
        EF = sum(1 for r in results if not r.get("passed", False) and line in r.get("executed_lines", set()))
        EP = sum(1 for r in results if r.get("passed", False) and line in r.get("executed_lines", set()))
        denom = (total_failed * (EF + EP)) ** 0.5
        score = 0.0 if denom == 0 else EF / denom
        suspiciousness[line] = score

    return suspiciousness, all_lines, total_failed

# Main
if __name__ == "__main__":
    with open("problems/Add_two_numbers/tests.json") as f:
        tests = json.load(f)

<<<<<<< HEAD
correct_file = os.path.abspath("problems/Add_two_numbers/add_two_numbers_correct.py")
buggy_file   = os.path.abspath("problems/Add_two_numbers/bug1.py")
buggy_filetwo = os.path.abspath("problems/Add_two_numbers/bug2.py")
buggy_filethree = os.path.abspath("problems/Add_two_numbers/bug3.py")
buggy_filefour = os.path.abspath("problems/Add_two_numbers/bug4.py")

=======
    correct_file = os.path.abspath("problems/Add_two_numbers/add_two_numbers_correct.py")
    buggy_file = os.path.abspath("problems/Add_two_numbers/bug1.py") # Change this to bugX to test the other bug, with X being the number
>>>>>>> 7dc0a29483ab010e0951c4dd9d0e6c59e99927de

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

    susp_scores, all_lines, total_failed = compute_suspiciousness_ochiai(bug_results)

    print(f"\nFAILED TESTS: {total_failed}/{len(bug_results)}")
    print("\n=== Suspiciousness (Ochiai) ===")
    for line in sorted(all_lines):
        print(f"Line {line:3d}: {susp_scores.get(line, 0):.2f}")

    print("\n=== Ranked (Most Suspicious First) ===")
    ranked = sorted(susp_scores.items(), key=lambda x: x[1], reverse=True)
    for line, score in ranked:
        print(f"Line {line:3d}: {score:.2f}")
