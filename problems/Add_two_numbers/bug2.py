# bug2.py
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

            # BUG: carry added twice if both nodes exist
            if l1 and l2:
                out = val1 + val2 + carry + carry  # <-- duplicated carry
            else:
                out = val1 + val2 + carry

            carry, out = divmod(out, 10)

            current.next = ListNode(out)
            current = current.next

            if l1:
                l1 = l1.next
            if l2:
                l2 = l2.next

        return dummy.next
