class Solution {
public:
    ListNode* removeElements(ListNode* head, int val) {
        // Create a dummy node on the stack to handle head deletion safely
        ListNode dummy(-1);
        dummy.next = head;
        
        ListNode* curr = &dummy;
        
        // Single-pass traversal loop
        while (curr->next != nullptr) {
            if (curr->next->val == val) {
                // Target found: capture node pointer to free memory
                ListNode* nodeToDelete = curr->next;
                
                // Rewire the pointer to bypass the target node
                curr->next = curr->next->next;
                
                // Delete the node from memory
                delete nodeToDelete;
            } else {
                // Move forward only if no node was deleted
                curr = curr->next;
            }
        }
        
        // Return the true head (dummy.next automatically updates)
        return dummy.next;
    }
};
