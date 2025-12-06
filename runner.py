import json
import  coverage # Keeping this here just in case!
from problems.Add_two_numbers.add_two_numbers_correct import Solution as RefSolution
from problems.Add_two_numbers.bug1 import Solution as BugSolution

# Helper to convert array to ListNode
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def array_to_list(arr):
    dummy = ListNode()
    current = dummy
    for val in arr:
        current.next = ListNode(val)
        current = current.next
    return dummy.next

# Helper to convert ListNode to array
def list_to_array(node):
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result

def run_solution(SolutionClass, tests, file_path):
    results = []

    for test in tests:
        # cov = coverage.Coverage(include=[file_path])  # only track this file
        cov = coverage.Coverage(include=[file_path], branch=True)
        cov.start()

        l1 = array_to_list(test["l1"])
        l2 = array_to_list(test["l2"])
        expected = test["expected"]

        solution = SolutionClass()
        output = solution.addTwoNumbers(l1, l2)

        cov.stop()
        cov.save()

        output_array = list_to_array(output)
        passed = output_array == expected

        _, _, executed_lines, _ = cov.analysis(file_path)

        results.append({
            "id": test["id"],
            "passed": passed,
            "executed_lines": executed_lines
        })

    return results




# def compute_suspiciousness(results, total_passed, total_failed):
def compute_suspiciousness(results, total_failed):
    suspiciousness = {}

    # all lines executed at least once
    all_lines = set(line for r in results for line in r['executed_lines'])

    for line in all_lines:
        ef = sum(1 for r in results if not r['passed'] and line in r['executed_lines'])
        ep = sum(1 for r in results if r['passed'] and line in r['executed_lines'])

        # Ochiai denominator
        denom = ((ef + ep) * total_failed) ** 0.5

        if denom == 0:
            score = 0.0
        else:
            score = ef / denom

        suspiciousness[line] = score

    return suspiciousness


# Load test cases
with open("problems/Add_two_numbers/tests.json") as f:
    tests = json.load(f)

# Run tests
print("Running ref.py (correct solution)...")
ref_results = run_solution(RefSolution, tests, 'problems/Add_two_numbers/add_two_numbers_correct.py')
print(ref_results)

print("\nRunning bug1.py (buggy solution)...")
bug_results = run_solution(BugSolution, tests, 'problems/Add_two_numbers/bug1.py')
print(bug_results)



# Calculate total passed/failed for buggy solution
total_passed = sum(r['passed'] for r in bug_results)
total_failed = len(bug_results) - total_passed

# Compute suspiciousness
susp_scores = compute_suspiciousness(bug_results, total_failed)

# Rank lines by suspiciousness
sorted_lines = sorted(susp_scores.items(), key=lambda x: x[1], reverse=True)

print("\nMost suspicious lines:")
for line, score in sorted_lines:
    print(f"Line {line}: {score:.2f}")
