class Solution {
public:
    int longestMountain(vector<int>& arr) {
      int n=arr.size();
      int l=1;
      int c=1;
      int p=arr[0];
      bool t=1;
      for(int i=1;i<n;i++)
      {
          p=arr[i-1];
          if(arr[i]>p)
          {
              if(t==0)
              {c=1;t=1;}
              c++;
          }
          else if(arr[i]<p)
          {
           if(c==1)
           continue;
           c++;
           t=0;
           l=max(l,c);
          }
          else
          c=1;
      }
      if(l==1)
      return 0;
      else return l;  
    }
};