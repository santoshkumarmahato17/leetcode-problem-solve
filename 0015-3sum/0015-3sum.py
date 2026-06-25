class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
      
        # 1. Initialize data structures to count occurrences of each number
        negative = defaultdict(int)
        positive = defaultdict(int)
        zeros = 0
        
        for num in nums:
            if num < 0:
                negative[num] += 1
            elif num > 0:
                positive[num] += 1
            else:
                zeros += 1
        
        result = []
        
        # 2. Handle cases involving Zero(s)
        if zeros:
            # Check for triplets like (0, -x, x)
            for n in negative:
                if -n in positive:
                    result.append([0, n, -n]) # Use list [] instead of tuple ()
            # If there are 3+ zeros, we can make a triplet (0, 0, 0)
            if zeros > 2:
                result.append([0, 0, 0])

        # 3. Handle non-zero triplets (negative + negative + positive OR positive + positive + negative)
        for set1, set2 in ((negative, positive), (positive, negative)):
            set1Items = list(set1.items())
            for i, (j, k) in enumerate(set1Items):
                # Try every pair (j, j2) in the first set
                for j2, k2 in set1Items[i:]:
                    # Check if the third number (-j - j2) exists in the second set
                    # Logic: j + j2 + target = 0 => target = -(j + j2)
                    target = -j - j2
                    if target in set2:
                        # Ensure we don't pick the same number twice unless it appears multiple times
                        if j != j2 or (j == j2 and k > 1):
                            result.append([j, j2, target])
                            
        return result