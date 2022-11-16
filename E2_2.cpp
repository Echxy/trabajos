#include <iostream>
#include <vector>
#include <bits/stdc++.h>
using namespace std;


void plebicito(int n, int u){
    vector <int> ciudades(n);
    for(int i = 0; i<n;i++){
        int ciudad;
        cin >> ciudad;
        ciudades[i] = ciudad; // meto los valores al vector
    }
// ahora deberia iniciar la busqueda binaria??
    sort(ciudades.begin(),ciudades.end());
    int l = 1; // extremo izq
    int r = (int)ciudades[n-1]; // extremo der
    //cout << "hola\n";
    while(l<r){
        //cout << "peo\n";
        int u_s = 0;
        int lr = l + (r-l)/2; // este valor va a ser mi respuesta tentativa
        //cout << lr << "lr\n";
        for(int i = 0; i<n;i++){
            int valor;
            valor = ciudades[i];
            while (valor > 0){
                valor  -= lr;
                u_s += 1;
                //cout << "pl";
            }
        }
        // aca reviso si me pase o no
        //cout  << u_s << "u_s\n";
        if(u_s <= u){
            r = lr;
        }
        else{
            l = lr+1;
        }
    }

    cout << l << "\n";

}


int main(){
    int n, u;
    while(cin >> n >> u, n != -1){
        plebicito(n,u);
    }
    return 0;
}