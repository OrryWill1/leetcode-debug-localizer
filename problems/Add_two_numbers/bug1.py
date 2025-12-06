# bug1.py
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution(object):
    def addTwoNumbers(self, l1, l2):
        dummy = ListNode()
        current = dummy
        carry = 0

        while l1 or l2 or carry:
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0

            # BUG: Only multiply val1 if > 5
            if val1 > 5:
                out = val1 * 2        # <-- now on a separate line
                out += val2            # <-- separate
                out += carry           # <-- separate
            else:
                out = val1 + val2 + carry

            carry, out = divmod(out, 10)

            current.next = ListNode(out)
            current = current.next

            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None

        return dummy.next

