#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const ll neutro = 0; // en el or y el xor es 0

template <class T>
struct SegmentTree{
  int N;
  vector <T> tree;
  SegmentTree(int _N){
    N = _N;
    tree.resize(4*N);
    build(0, 0, N-1,0);
  }

  SegmentTree(vector<T> &init) {
    N = init.size();
    tree.resize(4*N);
    build(0, 0, N-1, init,0);
  }

  T mergeor(T a, T b ){
      return a | b;
    }
  T mergexor(T a , T b){
      return a ^ b;
    }
  void build(int n, int i, int j, int boo){
    if(i == j){
      tree[n] = 0;
      return;
    }
    int mid = (i+j)/2;
    if(boo == 0){
      build(2*n-1, i, mid, 1);
      build(2*n-2, mid+1, j, 1);
      tree[n] = mergeor(tree[2*n+1], tree[2*n+2]);
    if(boo == 1){
      build(2*n-1, i, mid, 0);
      build(2*n-2, mid+1, j, 0);
      tree[n] = mergexor(tree[2*n+1], tree[2*n+2]);      
  }

  void build(int n, int i, int j, vector<T> &init, int boo){
    if(i == j){
      tree[n] = init[i];
      return;
    }
    int mid = (i+j)/2;
    if( boo == 0){
      build(2*n+1, i, mid, init,1);
      build(2*n+2, mid+1, j, init,1);
      tree[n] = mergeor(tree[2*n+1], tree[2*n+2]);
    }
    if( boo == 1){
      build(2*n+1, i, mid, init,0);
      build(2*n+2, mid+1, j, init,0);
      tree[n] = mergexor(tree[2*n+1], tree[2*n+2]);
    }
  }

  T query(int l, int r){
    return query(0, 0, N-1, l, r, 0);
  }

  T query(int n, int i, int j, int l, int r, int boo){
        if ( l <= i && j <= r){ // contenido
            return tree[n];
        }
        if (r < i || j < l){ // caso fuera
            return neutro; // valor que no debe importar, pierda en toda comparacion o evaluacion
        }
        int mid = (l+r)/2; // si solo parte esta afuera y otra no divide to conquer
        if (boo == 0){
            return mergeor ( 
            query(2*n+1, i, mid , l , r, 1 ),
            query(2*n+2, mid+1, j , l ,r, 1));
        }
        if ( boo == 1){
            return mergexor ( 
            query(2*n+1, i, mid , l , r, 0),
            query(2*n+2, mid+1, j , l ,r, 0));  
  }

  void update(int t, T val){
    update(0, 0, N-1, t, val, 0);
  }
  
  void update(int n, int i, int j, int t, T val, int boo){
    if(t < i || j < t) return;
    if(i == j){
      tree[n] = val;
      return;
    }
        int mid = (i+j)/2;
        if (boo == 0){
            update(2*n+1, i , mid ,t  ,val,1);
            update(2*n+2, mid+1, j ,t ,val,1);
            tree[n] = mergeor(tree[2*n+1], tree[2*n+2]);
        }
        if (boo == 1){
            update(2*n+1, i , mid ,t  ,val,0);
            update(2*n+2, mid+1, j ,t ,val,0);
            tree[n] = mergexor(tree[2*n+1], tree[2*n+2]);
        }
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
int n,m;
cin >> n;
cin >> m; // cantidad de consultas
ll b = pow(2, n); // cantidad de valores
vector<ll> a(b);
for(int i= 0; i<b; i++){
    cin >> a[i];
}
SegmentTree<int> st(a); // creo el segment tree
for(int i =0; i<m; i++ ){
    ll c;
    ll d;
    cin >> c; // el lugar
    cin >> d; // el valor
    st.update(c,d);
    cout << st.query(0,b-1);
}

return 0;
}
