void moveZeroes(int* nums, int numsSize) {
    //Declaration LastNonZeros
    int LastNonZeros = 0;
    //loop for the pointer movie 
    for(int i=0; i<numsSize; i++){
        //condition to check nonzero
        if(nums[i] != 0){
            
            //swap method 
            int temp = nums[LastNonZeros];
            nums[LastNonZeros] = nums[i];
            nums[i] = temp;
            //increment 
           LastNonZeros++;
        }
     } 
     
}