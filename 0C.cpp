#include <iostream>
using namespace std;
// quieres encontrar el 1, anotar sus coodenadas y luegos hacer un abs() en cada una con un -2 cara encontrar la dist
int main() {
   int mat[5][5];
   int a,b;
   for (int n=0; n<5; n++){
        for (int m = 0; m<5; m++){
            cin >> mat[n][m];
            if (mat[n][m] == 1) {
                a = n;
                b = m;
            }
        }
    }

    int sol = abs(a-2) + abs(b-2);
    cout << sol << "\n";
    return 0;
}