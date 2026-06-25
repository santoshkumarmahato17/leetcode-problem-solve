/**
 * Note: The returned array must be malloced, assume caller calls free().
 */
int* sortArrayByParity(int* nums, int numsSize, int* returnSize) {
    
    int left = 0;
    int right = numsSize - 1;
    
    while(left < right){
        //check even number
        if(nums[left] % 2 == 0){
            left++;
        }
        //check odd number
        else if(nums[right] % 2 != 0){
            right--;
        }
        //swap even > odd
        else{
        int temp = nums[left];
        nums[left] = nums[right];
        nums[right] = temp;
        left++;
        right--;
        }
    }
    *returnSize = numsSize;
     return nums;

    
}