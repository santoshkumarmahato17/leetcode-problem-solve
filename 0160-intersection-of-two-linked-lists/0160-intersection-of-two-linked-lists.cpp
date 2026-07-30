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
    ListNode *getIntersectionNode(ListNode *headA, ListNode *headB) {
        //appointing the head Pointer to the both node A & B
        ListNode* pA = headA;
        ListNode* pB = headB;
    //while loop for the compare till both node are not same
        while (pA != pB) {
            
            //pA reach the end it will jump the list B
            if (pA == nullptr)
                pA = headB;
            else
                pA = pA->next;

            //Pb reach the end it will jump the list A
            if (pB == nullptr)
                pB = headA;
            else
                pB = pB->next;
        }
       // mean pA == pB other wise return the NULL
        return pA;
    }
};