int removeDuplicates(int* nums, int numsSize) {
    //empty  array
    if(numsSize==0){
        return 0;
    }
    int k = 0;
    //loop for array start
    for(int i = 0; i < numsSize; i++){
        //find new unique element 
        if(nums[i] != nums[k]){
            k++; //move the point pointer
            //copy the unique element to its new position 
            nums[k]=nums[i];  
        }
        
    }
    return k+1;// total unique indix k+1

}