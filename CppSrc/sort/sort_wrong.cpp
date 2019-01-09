#include <iostream>
using namespace std;

int main(){
    int i,j,n;
    int temp;
    cin >> n;
    int a[n];
    for(i=0;i<n;i++){
        cin >> a[i];
    }
    for(i=0;i<n;i++){
        for(j=i+1;j<n;j++){
            if(a[i]>a[j]){
                temp=a[i];
                a[i]=a[j];
                a[j]=temp;
            }
        }
    }
    for(i=0;i<n;i++){
        cout << a[i] << " ";
    }
    cout << endl;
}

