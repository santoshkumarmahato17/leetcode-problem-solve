class Solution:
    def climbStairs(self, n: int) -> int:


        if n == 1 or n == 2:
            return n
        first: int = 1
        second: int = 2
        third: int = None
        
        for i in range(3, n+1):
            third = first + second
            first = second
            second = third

        return third