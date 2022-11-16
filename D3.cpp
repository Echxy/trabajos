// PARA EL SAPO Y SEPO LO QUE PODRIAS HACER ES:
// SUPER TEORICOOOOO
// DEBO PENSAR CUAL ES EL CASO BASE
// ESTE PODRIA SER LO PEOR DONDE SACO TODAS DE A UNA
// PENSAR SI JUEGA UN ROL LOS BORDES O EL CENTRO
// TAMBIEN PENSAR COMO ES LA RECURSION 
#include <vector>
#include <algorithm>
#include <bits/stdc++.h>
using namespace std;
vector<int> piedra;
vector<vector<int>> dp;

int solve(int i, int j){
    if(i>j){
        return 0;
    }
    if (dp[i][j] != -1){
        return dp[i][j];
    }
    int chico =  (1 + solve(i+1,j));
    if(piedra[i] == piedra[j]){
        chico = min(chico, solve(i+1,j-1));
    }
    for(int k= i+1; k<j; k++){
        if(piedra[i] == piedra[k]){
        chico = min(solve(i,k) + solve(k+1 , j),chico);
        }
    }
    dp[i][j] = chico;
    // cout << chico << "i,j " << i << ", "<< j << "\n";
    return dp[i][j];

}
void sapo(){
    int n;
    cin >> n;
    piedra.resize(n);
    dp.resize(n , vector<int>(n,-1));
    for(int i = 0; i<n; i++){
        int p = 0;
        cin >> p;
        piedra[i] = p;
    }
    for(int i = 0; i<n; i++){
        dp[i][i] = 1;
        if((i+1<n) && (piedra[i] == piedra[i+1])){
            dp[i][i+1] = 1;
        }
        else if (i+1<n){
            dp[i][i+1] = 2;
        }
    }
    cout << solve(0,n-1);
            
}


int main(){
    sapo();
   return 0;
}