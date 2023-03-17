#include <iostream>
using namespace std;
int main() 
{
string str;
cin>>str;
int count = 0;
for(int i = 0;str[i];i++)
    count++;
cout<<count;
}