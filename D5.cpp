#include<bits/stdc++.h>
using namespace std;
 
// Función para implementar el algoritmo KMP
void KMP(int text_length, string text, string pattern)
{
    int m = text.length();
    int n = text_length;
 
    if (n == 0)
    {
        return;
    }
    if (m < n)
    {
        return;
    }
 
    // next[i] almacena el índice de la siguiente mejor coincidencia parcial
    int next[n + 1];
 
    for (int i = 0; i < n + 1; i++) {
        next[i] = 0;
    }
 
    for (int i = 1; i < n; i++)
    {
        int j = next[i + 1];
 
        while (j > 0 && pattern[j] != pattern[i]) {
            j = next[j];
        }
 
        if (j > 0 || pattern[j] == pattern[i]) {
            next[i + 1] = j + 1;
        }
    }
 
    for (int i = 0, j = 0; i < m; i++)
    {
        if (text[i] == pattern[j])
        {
            if (++j == n) {
                cout << i - j + 1 << endl;
            }
        }
        else if (j > 0)
        {
            j = next[j];
            i--;    // ya que `i` se incrementará en la siguiente iteración
        }
    }
}
 
// Programa para implementar el algoritmo KMP en C++
int main()
{
    std::ios::sync_with_stdio(0); std::cin.tie(0);
    int pat_len;
    string text;
    string pattern;
    cin >> pat_len;
    cin >> pattern;
    cin >> text;
    KMP(pat_len, text, pattern);
    cout << '\n';
    
    return 0;
}