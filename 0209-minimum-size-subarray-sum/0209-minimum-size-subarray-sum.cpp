class Solution {
public:
    int minSubArrayLen(int target, vector<int>& nums) {
        int i=0,j=0,sum=0,c=0,ans=INT_MAX;
        while(j<nums.size()){
            if(sum<target){
                sum+=nums[j];
                c++;
                j++;
            }
            else{
                if(ans>c)
                ans=c;
                sum-=nums[i];
                i++;
                c--;
            }
        }
        while(sum>=target){
            if(ans>c)
            ans=c;
            sum-=nums[i];
            i++;
            c--;
        }
        if(ans==INT_MAX)
        return 0;
        return ans;
    }
};