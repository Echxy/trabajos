#include <iostream>
#include <vector>
#include <bits/stdc++.h>
using namespace std;


void hace_set(int n){
    set<tuple<int,int,int>> trios;
    for (int i = 1; i<=n; i++){
        int valor;
        cin >> valor;
        tuple<int,int,int> rango;
        if (valor == 0){
            rango = make_tuple(i+1,n,i);
            trios.insert(rango);
        }
        else {
            rango = make_tuple(((i/(valor+1))+1),i/valor,i);
            trios.insert(rango);
        }
    }
    vector <int> a(n);
    set<tuple<int,int>> duos;
    int valor = get<0>(*trios.begin()); // el primero del rango
    a[get<2>(*trios.begin())-1] = valor; // al indice
    trios.erase(trios.begin()); // lo borro
    while(trios.empty() == false){
        while(get<0>(*trios.begin()) == valor || get<0>(*trios.begin()) == valor+1 ){ // reviso los siguientes?
            duos.insert(make_tuple(get<1>(*trios.begin()),get<2>(*trios.begin()))); // los inserto en el duos
            trios.erase(trios.begin()); // lo borro
        }
        valor += 1; // esto me ayuda para el siguiente loop
        // una vez que acaba el loop
        // tomo el primero del duo
        a[get<1>(*duos.begin())-1] = valor; // meto el segundo valor
        duos.erase(duos.begin()); // lo borro
        // ahora deberia loopear? 
    }
    while(duos.empty() == false){
        valor +=1;
        a[get<1>(*duos.begin())-1] = valor; // meto el segundo valor
         duos.erase(duos.begin()); // lo borro
    }
    for(int i = 0;i<n;i++){
        cout << a[i] << " ";
    }
    
}
// DEBO CAMBIAR LOS ERASE???
// lo LOGREEEEEEEEEE
// lets GOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
// optimizao la formula de rangos
// 2am posting 
// gg izi facilito como desactivo los bots



int main(){
    int casos;
    cin >> casos;
    for (int i = 0; i < casos; i++){
        int n;
        cin >> n;
        hace_set(n);
        cout << "\n";
    }
    return 0;
}
