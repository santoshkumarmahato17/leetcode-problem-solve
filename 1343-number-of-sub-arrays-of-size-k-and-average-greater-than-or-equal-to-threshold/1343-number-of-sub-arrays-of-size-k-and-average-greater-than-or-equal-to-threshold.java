class Solution {
    public int numOfSubarrays(int[] arr, int k, int threshold) {
        int n = arr.length;
        int sum = 0;
        int count = 0;

        // Calculate the sum of the first window
        for (int i = 0; i < k; i++) {
            sum += arr[i];
        }

        if (sum >= threshold * k) {
            count++;
        }

        // Slide the window
        for (int i = k; i < n; i++) {
            sum = sum - arr[i - k] + arr[i];

            if (sum >= threshold * k) {
                count++;
            }
        }

        return count;
    }
}