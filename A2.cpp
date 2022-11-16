#include <iostream>
#include <vector>
#include <bits/stdc++.h>
using namespace std;

int main(){
    int n;
    int q;
    cin >> n;
    cin >> q;
    vector <int> a(n);
    for(int i= 0;i<n;i++){
        cin >> a[i];
    }

    for(int i=0;i<q;i++){
        int c; // consulta
        int l = 0; // extremo izq
        int r = n-1; // extremo der
        cin >> c;
        while(l<r){
            int lr = l + (r-l)/2;
            //cout << a[lr] << "este es la prueba \n";
            if(a[lr] >= c){
              //  cout << "ta grande \n";
                r = lr;
            }
            else{
            //    cout << "ta chico \n";
                l = lr+1;
            }
        }
        //cout << l << "este es L \n";
        if(a[l] == c){
            cout << l << "\n";
        }
        else {
            cout << -1 << "\n";
        }
    }
    return 0;
}