#include<bits/stdc++.h>
#include<vector>
#include<tuple>
using namespace std;
typedef long long ll;
// debo establecer el sistema de datos como una tuple
// el primer valor debe ser la suma del los dos numeros
// el segundo valor debe ser el mayor de los 2
// tree[n] = (max(get<0>tree[2*n+1],get<0>tree[2*n+2],get<1>tree[2*n+1]+get<1>tree[2*n+1]), max(get<1>tree[2*n+1],get<1>tree[2*n+1]))
 

struct Nodo{
  ll suma;
  ll max;
};
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
    // ( max(get<0>(a),get<0>(b),get<1>(a) + get<1>(b)), max(get<1>(a), get<1>(b)) )
    Nodo p;
    ll h = max(a.suma, b.suma);
    p.suma = max( h , (a.max + b.max));
    p.max = max( a.max, b.max);
    return p;
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
  /*  if( n == 0){
        int mid = (i+j)/2;
        build(2*n+1, i, mid, init);
        build(2*n+2, mid+1, j, init);
        tree[n] = tree[2*n+1] + tree[2*n+2];
    }
    */    
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
    if(l <= i && j <= r){
      //cout << tree[n];
      return tree[n];
    } 
    int mid = (i+j)/2;
    if(mid < l || r < i)
      return query(2*n+2, mid+1, j, l, r);
    if(j < l || r < mid+1)
      return query(2*n+1, i, mid, l, r);
    return merge(
        query(2*n+1, i, mid, l, r),
        query(2*n+2, mid+1, j, l, r));
  }
 
  void update(int t, int val){
    update(0, 0, N-1, t, val);
    }
  
  void update(int n, int i, int j, int t, int val){
    if(t < i || j < t) return;
    if(i == j){
      Nodo l;
      l.suma = 0;
      l.max = val;
      //cout << to_string(n) << 'n' << to_string(tree[n].max);
      tree[n] = l;

      return;
    }
    int mid = (i+j)/2;
    update(2*n+1, i, mid, t, val);
    update(2*n+2, mid+1, j, t, val);
    tree[n] = merge(tree[2*n+1], tree[2*n+2]);
  }
};

int main(){
    int n; // cantidad de numeros
    cin >> n;
    vector<Nodo> a(n);
    for(int i = 0; i<n; i++){
        a[i].suma = 0;
        int b;
        cin >> b;
        a[i].max = b; 
    }
    // llene el vector 
    SegmentTree<Nodo> st(a);
    // creo el tree
    int c; // cant consultas
    cin >> c;
    for(int i = 0; i<c; i++){
        char k;
        int x,y;
        cin >> k >> x >> y;
        if( k == 'Q'){
            cout << (st.query(x-1,y-1)).suma << '\n';
        }
        if( k == 'U'){
            st.update(x-1,y); // esto debe ser -1
        }
    }
    return 0;
}