#include <iostream>
#include <vector>
using namespace std;

int main() {
// supongamos que entran la primera
int n,h;
cin >> n >> h;
int agachados = 0;
vector <int> a(n);
for(int i = 0; i < n; i++){
    cin >> a[i];
    if (a[i] > h){
        // le sumo 1 a agachados
        agachados++;
    }
}
cout << agachados + n << "\n";
return 0;
}