class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        vector<int> ans;
        deque<int> qu; // Stores indices of elements
        int n = nums.size();

        // Edge case safety check
        if (n == 0 || k == 0) return ans;

        for (int i = 0; i < n; i++) {
            // 1. Remove indices that have slid out of the current window
            if (!qu.empty() && qu.front() == i - k) {
                qu.pop_front();
            }

            // 2. Maintain monotonic decreasing order:
            // Remove elements from the back that are smaller than the current element
            while (!qu.empty() && nums[qu.back()] < nums[i]) {
                qu.pop_back();
            }

            // 3. Add the current element's index to the back of the queue
            qu.push_back(i);

            // 4. The front of the queue is always the maximum element for the current window.
            // Start adding to answers once we've reached at least the first window size 'k'
            if (i >= k - 1) {
                ans.push_back(nums[qu.front()]);
            }
        }

        return ans;
    }
};