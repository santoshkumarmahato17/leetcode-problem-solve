int largestRectangleArea(int* heights, int heightsSize) {
    int *stack = (int*)malloc((heightsSize + 1) * sizeof(int));
    int top = -1; // Stack is empty
    int maxArea = 0;

    for(int i  = 0; i <= heightsSize; i++) {

        int currHeight = (i == heightsSize) ? 0 : heights[i];

        while(top != -1 && heights[stack[top]] > currHeight) {
            int height = heights[stack[top--]];
            int width;
            if(top == -1) {
                width = i;
            } else {
                width = i - stack[top] - 1;
            }
            int area = height * width;
            if(area > maxArea) {
                maxArea = area;
            }

        }
        stack[++top] = i;
    }
    return maxArea;
}