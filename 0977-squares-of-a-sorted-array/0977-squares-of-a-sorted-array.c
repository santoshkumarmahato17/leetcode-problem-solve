/**
 * Note: The returned array must be malloced, assume caller calls free().
 */
int* sortedSquares(int* nums, int numsSize, int* returnSize) {
    
    *returnSize = numsSize; 

    
    // Fix 1: Allocate memory for the result array
    int* result = (int*)malloc(numsSize * sizeof(int));
    
    int left = 0;
    int right = numsSize - 1;
    int index = numsSize - 1; // Tracks where to insert in the result array

    while (left <= right) {
        // Fix 2: Correctly square the elements
        int leftsquares = nums[left] * nums[left];
        int rightsquares = nums[right] * nums[right];
        
        if (leftsquares > rightsquares) {
            // Fix 3: Use the correct variable 'index'
            result[index] = leftsquares;
            left++;
        } else {
            result[index] = rightsquares;
            // Fix 4: Decrement 'right' to move inward
            right--;
        }
        // Move the index pointer backward for the next largest number
        index--;
    }
    
    return result;
}