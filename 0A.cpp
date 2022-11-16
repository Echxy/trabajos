
#include <iostream>
using namespace std;

int main() {
    int sandia;
    cin >> sandia;
    int resto = sandia/2;
    if ( ((resto*2) == sandia) && (sandia != 2) ) {
    cout << "YES";} 
    else  cout << "NO";
    
    return 0;
}