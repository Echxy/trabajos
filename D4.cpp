#include<bits/stdc++.h>
using namespace std;

template <class T>
struct SegmentTree{
  int N;
  vector <T> tree;
  SegmentTree(int _N){
    N = _N;
    tree.resize(4*N);
    build(0, 0, N-1);
  }

  SegmentTree(vector<T> &init) {
    N = init.size();
    tree.resize(4*N);
    build(0, 0, N-1, init);
  }

  T merge(T a, T b){ // Reemplazar esta funcion para determinar como juntar dos nodos para obtener el valor de su padre, en este caso es suma
    return a + b;
  }
  
  void build(int n, int i, int j){
    if(i == j){
      tree[n] = 0;
      return;
    }
    int mid = (i+j)/2;
    build(2*n+1, i, mid);
    build(2*n+2, mid+1, j);
    tree[n] = merge(tree[2*n+1], tree[2*n+2]);
  }

  void build(int n, int i, int j, vector<T> &init){
    if(i == j){
      tree[n] = init[i];
      return;
    }
    int mid = (i+j)/2;
    build(2*n+1, i, mid, init);
    build(2*n+2, mid+1, j, init);
    tree[n] = merge(tree[2*n+1], tree[2*n+2]);
  }

  T query(int l, int r){
    return query(0, 0, N-1, l, r);
  }

  T query(int n, int i, int j, int l, int r){
    if(l <= i && j <= r) return tree[n];
    int mid = (i+j)/2;
    if(mid < l || r < i)
      return query(2*n+2, mid+1, j, l, r);
    if(j < l || r < mid+1)
      return query(2*n+1, i, mid, l, r);
    return merge(
        query(2*n+1, i, mid, l, r),
        query(2*n+2, mid+1, j, l, r));
  }

  void update(int t, T val){
    update(0, 0, N-1, t, val);
  }
  
  void update(int n, int i, int j, int t, T val){
    if(t < i || j < t) return;
    if(i == j){
      tree[n] = val;
      return;
    }
    int mid = (i+j)/2;
    update(2*n+1, i, mid, t, val);
    update(2*n+2, mid+1, j, t, val);
    tree[n] = merge(tree[2*n+1], tree[2*n+2]);
  }

  int search(int from, T val){
    if(!from) return search(0, 0, N-1, val);
    return search(0, 0, N-1, val+query(0, from-1));
  }

  int search(int n, int i, int j, T val){
    if(tree[n] < val) return -1;
    if(i==j && tree[n] >= val) return i;
    int mid = (i+j)/2;
    if(tree[2*n+1] >= val) return search(2*n+1, i, mid, val);
    else return search(2*n+2, mid+1, j, val-tree[2*n+1]);
  }
};




int main(){
    int n;
    cin >> n;
    unsigned int k;
    cin >> k;
    vector<int> a(n);
    for (int i=0;i<n;i++) a[i] = 1; // lleno
    SegmentTree<int> st(a); // crear segment tree con el vector a
    int pos = 0;
    int step = k+1;
    int q = 0;
    for(int i = n; i>=1; i--){
      //cout << i << " ";
      k = step;
      k %= i;
      if(k == 0) k = i;
       // arreglar la cantidad de saltos
      //cout << k << " ";
      int l; // donde esta la posicion
      if ( st.query(pos,n-1) < k){ 
          q = st.query(pos,n-1);
          //cout << q << " ";
          pos = 0;
          l = st.search(pos,k-q);
      }
      else{
          l = st.search(pos,k); // indice donde esta mi respuesta
      } 
      pos = l;
      l += 1; // el valor 
      cout << l << '\n';
      st.update(l-1,0);
    }
    return 0;
}














/*
int main(){
    int n;
    int k;
    cin >> n; // cantidad de elementos 
    cin >> k; // de a cuantos es el corte
    vector<int> a(n);
    for(int i = 0; i<n; i++){
        a[i] = 1;
    }    
    /*for(int i = 0; i<n; i++){
      cout << a[i];
    }
    SegmentTree<int> st(a);
    int pos = 0; // en donde partimos
    for (int i = n; i >= 1; i--) { // viendo los restantes
        int step = k+1;
        step = step % i;
        cout << step << ;
        int r = st.query(pos , n);
        cout << r << " " ;
        if (step > r)
        {
            pos = 0; /// Set it back to first pos
            step -= r; /// Number of step traveled
        }
        pos = st.search(pos, step);
        cout << pos+1 << " ";
        st.update(pos+1, 0);
        pos += step%n;
        
        // no tengo idea que hacer
        // seguramente tiene que ver con
        // query imprimir, y update a wea inutil
        // teoria si es algo con % k+1      
    }
    return 0;
}
*/