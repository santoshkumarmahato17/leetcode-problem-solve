/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    ListNode* removeNthFromEnd(ListNode* head, int n) {
         ListNode* temp = head;
        int length = 0;
//Find the total length of the linked list
        while (temp != nullptr) {
            length++;
            temp = temp->next;
        }
//Check if the first node needs to be removed
        if (n == length) {
            ListNode* newHead = head->next;
            delete head;
            return newHead;
        }
//Find the node just before the node to delete
        int steps = length - n;
        temp = head;

        for (int i = 1; i < steps; i++) {
            temp = temp->next;
        }

        ListNode* nodeToDelete = temp->next;
        temp->next = temp->next->next;
        delete nodeToDelete;

        return head;
    }
};