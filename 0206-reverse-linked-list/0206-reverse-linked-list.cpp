#include <iostream>
using namespace std;
class Solution{
    public:
    ListNode* reverseList(ListNode* head){

    //assign the first node as null
    //using the ListNode* for return the address of the first node 
    ListNode* prev = nullptr;

    // create the another pointer named is "current"
    ListNode* current = head;

// Continue until every node has been processed.
    while ( current != nullptr){
        ListNode* next = current->next;
        current->next = prev;
        prev = current;
        current = next;
    }
    return prev;
}
};