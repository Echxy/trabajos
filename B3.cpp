#include <iostream>
#include <vector>
#include <bits/stdc++.h>
using namespace std;


int Mona(int n){
    vector<int> lista(n);
    vector<int> puntajes(n,0);
    for (int i = 0; i<n;i++){
        cin >> lista[i];
    }

// ahora que llené la lista de numeros voy a ver el caso base
// el caso base debe ser el último elemento de la lista    
    puntajes[n-1] = lista[n-1];
    for (int i = n-2; i>=0;i--){ // de fin a principio
        int k;
        puntajes[i] += lista[i]; // avanzo
        k = puntajes[i] + i;
        if( k<=(n-1)){ // si no me pasé
            puntajes[i] += puntajes[k];
        }
        // el else es no hacer nada;
    }
    // llené puntajes
    int respuesta = std::max_element(puntajes.begin(),puntajes.end()) - puntajes.begin();
    cout << puntajes[respuesta] << "\n";
}





int main(){
   int casos;
   // array  g
   cin >> casos;
   for(int i=0;i<casos;i++){
    int n;
    cin >> n;
    Mona(n);
   }
   return 0;
}
