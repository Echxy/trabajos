#include <iostream>
#include <vector>
#include <bits/stdc++.h>
using namespace std;


int filas(int n){
    vector<int> fila(n+2,0);
    vector<int> dp(n+2,0);
    for (int i = 0; i<n;i++){
        int valor;
        cin >> valor;
        fila[i] += valor;
    }
    for (int i = n-1; i>= 0; i--){
        dp[i] += max(dp[i+1],dp[i+2]+fila[i]);
    }
    int respuesta = std::max_element(dp.begin(),dp.end()) - dp.begin();
    return dp[respuesta]; 
}

void dulces(int n ,int m){
    vector<int> columnas(n+2,0);
    vector<int> dp(n+2,0);
    for(int i = 0; i<n;i++){
        columnas[i] += filas(m); // lleno las columnas 
    }
    for (int i = n-1; i>= 0; i--){
        dp[i] += max(dp[i+1],dp[i+2] + columnas[i]);
    }
    int respuesta = std::max_element(dp.begin(),dp.end()) - dp.begin();
    cout << dp[respuesta] << "\n"; 
}

int main(){
    int N, M;
    while(cin >> N >> M, N != 0){
    dulces(N,M);
    }
}