

class Solution {
    public int lengthOfLongestSubstring(String s) {
        Set<Character> window = new HashSet<>();
        int left = 0,maxLen = 0; 

        for (int right = 0; right < s.length(); right++)  // Right pointer expands the window
        {
            while (window.contains(s.charAt(right))) {
                window.remove(s.charAt(left));
                left++;
            }

            //Add the current character to the window
            window.add(s.charAt(right));

            //Update maximum length of the valid winndow
            maxLen = Math.max(maxLen, right - left + 1);
        }

        return maxLen;
    }
}