class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:

        nums.sort()
        n = len(nums)
        res = []
        for i in range(n-3):
            for j in range(i+1, n-2):
                temp = [nums[i], nums[j]]
                c = target - nums[i] - nums[j]
                seen = Counter()
                for k in range(j+1, n):
                    x = nums[k]
                    if seen[c-x] == 0:
                        seen[x] = 1
                    else: 
                        seen[x] = 1
                        cur = temp + [c-x, x]
                        if cur not in res:
                            res.append(cur)
                        
        
        return res   