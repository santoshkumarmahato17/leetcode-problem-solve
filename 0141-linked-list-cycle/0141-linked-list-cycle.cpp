/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
public:
    bool hasCycle(ListNode *head) {
        // slow is head pointer created 
        ListNode* slow = head;
        ListNode* fast = head;

        //Continue while Fast can move two steps.
        while (fast != nullptr && fast->next != nullptr) {

            slow = slow->next;

            fast = fast->next->next;

            if (slow == fast)
                return true;
        }

        return false;
    }
};