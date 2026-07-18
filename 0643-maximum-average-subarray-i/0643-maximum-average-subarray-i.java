class Solution {
    public double findMaxAverage(int[] nums, int k) {
        double sum = 0;
        //taking the sum of the first k elemnts
        for ( int i=0; i<k; i++){
            sum += nums[i];
        }
        double maxSum = sum;

        //sild the window one step at a time 
        for ( int i = k; i < nums.length ; i++){
            sum = sum - nums[i-k] + nums[i];
            maxSum = Math.max(maxSum, sum);
        }

        //convert the best sum into average 
        return maxSum /k;
        
    }
}