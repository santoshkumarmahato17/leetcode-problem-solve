/**
 * Note: The returned array must be malloced, assume caller calls free().
 */
int* twoSum(int* nums, int numsSize, int target, int* returnSize) {
    for(int i=0; i<numsSize; i++){
        for(int j=i+1; j<numsSize; j++){
            //Brute force approach
    if (nums[i] + nums[j] == target){
        //Dynamic allocate memory location 
        int* result = (int*)malloc(2 * sizeof(int));
        
        //assign the position 
        result[0] = i;
        result[1] = j;
        *returnSize = 2;
        return result;
       
           
        }
       }
     }
     *returnSize =0;
     return NULL;
     

    
}
                