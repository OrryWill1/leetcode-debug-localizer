# bug_branch.py
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def addTwoNumbers(self, l1, l2):
        dummy = ListNode()
        current = dummy
        carry = 0

        while l1 or l2 or carry:
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0

            # BUG: only multiply val1 if it's > 5 (incorrect logic)
            if val1 > 5:
                out = val1 * 2 + val2 + carry  # buggy branch
            else:
                out = val1 + val2 + carry

            carry, out = divmod(out, 10)

            current.next = ListNode(out)
            current = current.next

            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None

        return dummy.next
