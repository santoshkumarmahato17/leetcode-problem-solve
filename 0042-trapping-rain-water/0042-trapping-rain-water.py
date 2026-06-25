class Solution(object):
    def trap(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        area = 0
        l = 0
        r = len(height) - 1
        tallest = 0
        while l < r:
            minim = min(height[l], height[r])
            tallest = max(tallest, minim)
            if height[l] < tallest:
                area += tallest - height[l]
            elif height[r] < tallest:
                area += tallest - height[r]
            if height[l] <= height[r]:
                l+= 1
            else:
                r -= 1

        return area
                