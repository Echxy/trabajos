#include <iostream>
using namespace std;

int main(){
    unsigned long long capacidad; 
    unsigned long long gain;
    cin >> capacidad;
    cin >> gain;
    unsigned long long estado = 0;
    unsigned long long dia = gain; // es inutil revisar dias donde siempre se llena
    bool check = true; // revisa que el gain sea menor que capacidad
    if(gain >= capacidad){
        dia = capacidad;
        check = false;
    }
    while(check){ // ciclo de la vida
        // es de noche
        estado += dia; // palomas atacan
        if(estado >= capacidad){ // ganaron ?
           break;
        }
        dia++; // amanece
        estado -= gain; // el malvado granero tiene refuerzos

    }
    cout << dia;
    return 0;
}