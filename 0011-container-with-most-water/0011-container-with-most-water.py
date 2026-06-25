class Solution:
    def maxArea(self, height: List[int]) -> int:
        a=0
        m = max(height)
        s = 0
        l = len(height)-1
        h = 0
        while True:
            if h > m or s==l:
                break
            if height[s] >= h and height[l] >= h:
                c = h * (l-s)
                a = max(c, a)
                h += 1
            elif height[s] < h:
                s += 1
            elif height[l] < h:
                l -= 1
        return a
	