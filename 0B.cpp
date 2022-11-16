#include <iostream>
using namespace std;

void palabra(){
    string entrada;
    cin >> entrada;
    if (entrada.size() > 10) {
        cout << entrada.front() << entrada.size()-2 << entrada.back() << "\n";
    }
    else { 
        cout << entrada << "\n";
    }
}

int main() {
        int test;
        cin >> test;
        for (int i = 0; i<test;i++){
            palabra();
        }
        return 0;
        }













 