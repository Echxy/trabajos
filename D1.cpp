#include <iostream>
#include <vector>
#include <bits/stdc++.h>
using namespace std;

void guardias(int n){
    vector <int> guard(n);
    vector <int> chicos(n/2);
    vector <int> grandes(n/2);
    // me ahorro tiemp
    for (int i = 0; i<n;i++){
        cin >> guard[i];
    }
    if(n % 2 == 1){
        cout << "NO"<< "\n";
        //cout << "YOO";
    } 
    else{

        sort(guard.begin(),guard.end());
        for ( int i = 0; i<(n/2); i++){
            chicos[i] = guard[i];
            grandes[i] = guard[i +((n/2))];
        }
        bool exito = true;
        for (int i = 0; i<(n/2);i++){
            if (chicos[i] >= grandes[i]){
                cout << "NO" << "\n";
                exito = false;
            }
            if ((i = (n/2)-1) && chicos[0] < grandes[i]){
                cout << "NO"<< "\n";
                exito = false;
            }
        }
        if (exito == true){
            cout << "YES"<< "\n";
            for (int i = 0; i<(n/2);i++){
                if (i != (n/2)-1){
                    cout << chicos[i] << " ";
                    cout << grandes[i] << " ";
                }
                else{
                    cout << chicos[i] << " ";
                    cout << grandes[i] << "\n";
            }  
        }
    }
}
}

// creo un set con los errores
int main(){
   int casos;
   // array  g
   cin >> casos;
   for(int i=0;i<casos;i++){
    int n;
    cin >> n;
    guardias(n);
   }
   return 0;
}

        /*for (int k = 0; k<(n/2);k++){
            cout << "ola";
            if ((chicos[k] >= grandes[k]) || (chicos[k] >= grandes[k-1])){
                cout << "NO" << "\n";
                //cout << "YOOO";
                exito = false;
            }
            else if ((k = (n/2)-1) && ((chicos[0] >= grandes[k]) || (grandes[k] <= chicos[k]))){
                //cout << chicos[0] << " " << grandes[i] << "\n";
                cout << "NO"<< "\n";
                exito = false;
            }
            }*/
