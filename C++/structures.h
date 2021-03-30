
#include <iostream>
#include <stdexcept>
#include <initializer_list>
#include <string>


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
template<typename T> class allocator {
public:
    T* allocate(int n) { return (T*) malloc(n * sizeof(T)); }
    void deallocate(T* p) { free(p); }

    void construct(T* p, const T& v) { new(p) T{v}; }
    void destroy(T* p) { p->~T(); }
};

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
template<typename T, typename A = allocator<T>>
class vector {
protected:
    int sz;
    T* elem;
    int space;
    A alloc;
public:
    vector() : sz{0}, elem{nullptr}, space{0}
    {}

    explicit vector(int n, T null_elem=0) : sz{n}, elem{nullptr}, space{n}
    {
        elem = alloc.allocate(n);
        for (T* p = elem; p != elem + n; ++p) alloc.construct(p, null_elem);
    }
    vector(std::initializer_list<T>);

    vector(const vector&);                      
    vector& operator=(const vector&);           

    vector(vector&&);                           
    vector& operator=(vector&&);                

    ~vector()                                   
    {
        for (T* p = elem; p != elem + sz; ++p) alloc.destroy(p);
        alloc.deallocate(elem);
    } 

    T& operator[](int n) { return elem[n]; }    
    const T& operator[](int n) const { return elem[n]; }

    int size() const { return sz; }
    int capacity() const { return space; }

    void reserve(int);                          
    void push_back(const T&);
};

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

template<typename T, typename A> vector<T,A>::vector(std::initializer_list<T> lst)
:sz (lst.size()),
elem {new T[sz]}, space (lst.size())
{
	std::copy(lst.begin(), lst.end(), elem);
}


template<typename T, typename A> vector<T,A>::vector(const vector<T,A>& v)
    : sz{v.sz}, elem{nullptr}, space{v.sz}
{
    elem = alloc.allocate(v.sz);
    std::copy(v.elem, v.elem + v.sz, elem);
}

template<typename T, typename A>
vector<T,A>& vector<T,A>::operator=(const vector<T,A>& v)
{
    if (this == &v) return *this;       

    if (v.sz <= space) {                
        for (int i = 0; i < v.sz; ++i) elem[i] = v.elem[i];
        for (int i = v.sz; i < sz; ++i) alloc.destroy(&elem[i]);
        sz = v.sz;
        return *this;
    }

    T* p = alloc.allocate(v.sz);        
    std::copy(v.elem, v.elem + v.sz, p);
    for (T* q = elem; q != elem + sz; ++q) alloc.destroy(q);
    alloc.deallocate(elem);
    space = sz = v.sz;
    elem = p;
    return *this;
}

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

template<typename T, typename A> vector<T,A>::vector(vector<T,A>&& v)
    : sz{v.sz}, elem{v.elem}, space{v.space}
{
    v.sz = 0;
    v.elem = nullptr;
}

template<typename T, typename A>
vector<T,A>& vector<T,A>::operator=(vector<T,A>&& v)
{
    for (T* p = elem; p != elem + sz; ++p) alloc.destroy(p);
    alloc.deallocate(elem);
    elem = v.elem;
    sz = v.sz;
    space = v.space;
    v.sz = 0;
    v.elem = nullptr;
    return *this;
}

template<typename T, typename A>
void vector<T,A>::reserve(int newalloc)
{
    if (newalloc <= space) return;      
    T* p = alloc.allocate(newalloc);    
    for (int i = 0; i < sz; ++i) alloc.construct(&p[i], elem[i]);   
    for (int i = 0; i < sz; ++i) alloc.destroy(&elem[i]);           
    alloc.deallocate(elem);             
    elem = p;
    space = newalloc;
}

template<typename T, typename A>
void vector<T,A>::push_back(const T& val)
{
    if (space == 0) reserve(8);         
    else if (sz == space) reserve(2 * space);   
    alloc.construct(&elem[sz], val);            
    ++sz;                                      
}


template<typename D>
struct t_node
    {
    std::string data; //ключ
    D value;
    t_node<D>* parent;
    t_node<D>* left;
    t_node<D>* right;
    char color;
    };

template<typename D>
class RBTree{
    
    
    public:
    //инициализация
    RBTree(): root{nullptr} {}
    void RBInsert(std::string, D);
    //Возвращает корень дерева
    t_node<D>* GetRoot() {return root;}
    t_node<D>* SearchInexact(std::string);
    //дестуктор
    ~RBTree() { DeleteTree(root);}
    D& operator[](std::string n) { return SearchInexact(n)->value; }

    private:
    void DeleteTree(t_node<D>*);  
    t_node<D>* DeleteBST(t_node<D>*, std::string);
    void SetColor(t_node<D>*, char);
    t_node<D>* Minimum(t_node<D>*);
    char GetColor(t_node<D>*);
    void LeftRotate(t_node<D>*);
    void RightRotate(t_node<D>*);
    void Insert(t_node<D>*, t_node<D>*);
    t_node<D>* root;
    

    
};

//Полное удаление дерева
template<typename D>
void RBTree<D>::DeleteTree(t_node<D>* node)  
{  
    if (node == NULL) 
        return;  

    DeleteTree(node->left);  
    DeleteTree(node->right);  
      
    delete node; 
}  

//Установка цвета узла
template<typename D>
void RBTree<D>::SetColor(t_node<D> *node, char color) {
    if (node == nullptr)
        return;

    node->color = color;
}

//Рекурсивный поиск узла с заданным значением
template<typename D>
t_node<D>* RBTree<D>::DeleteBST(t_node<D>*root, std::string data) {
    if (root == nullptr)
        return root;

    if (data < root->data)
        return DeleteBST(root->left, data);

    if (data > root->data)
        return DeleteBST(root->right, data);

    if (root->left == nullptr || root->right == nullptr)
        return root;

    t_node<D>*temp = Minimum(root->right);
    root->data = temp->data;
    return DeleteBST(root->right, temp->data);
}



//Возвращаяет цвет узла
//Null = черный
template<typename D>
char RBTree<D>::GetColor(t_node<D>* Node)
{
    if(Node != nullptr)
        return Node->color;
    return 'b';
}

//Левый поворот поддерева
template<typename D>
void RBTree<D>::LeftRotate(t_node<D> *x)
{
    t_node<D>*y = x->right;
    x->right = y->left;
    if(y->left != nullptr) {y->left->parent = x;}
    y->parent = x->parent;
    if(x->parent == nullptr) {root = y;}
    else if(x == x->parent->left) {x->parent->left = y;}
    else {x->parent->right = y;}
    y->left = x;
    x->parent = y;
}

//Правый поворот поддерева
template<typename D>
void RBTree<D>::RightRotate(t_node<D>* x)
{
    t_node<D>* y = x->left;
    x->left = y->right;
    if(y->right != nullptr) {y->right->parent = x;}
    y->parent = x->parent;
    if(x->parent == nullptr) {root = y;}
    else if(x == x->parent->left) {x->parent->left = y;}
    else {x->parent->right = y;}
    y->right = x;
    x->parent = y;
}

//Вставка элемента в дерево
//Выполняется проверка нарушений свойств
//Выполняется балансировка
template<typename D>
void RBTree<D>::RBInsert(std::string key, D value)
{
    t_node<D>* y = SearchInexact(key);
    if(y!=nullptr && key == y->data)
    {
        y->value = value;
        return;
    }
    t_node<D>* new_node = new t_node<D>;
    new_node->left = nullptr;
    new_node->right = nullptr;
    new_node->parent = nullptr;
    new_node->data = key;
    new_node->value = value;
    Insert(new_node, y);
    new_node->color = 'r';
    while(new_node != root && GetColor(new_node->parent) == 'r')
    {
        if(new_node->parent == new_node->parent->parent->left)
        {
            t_node<D>* y = new_node->parent->parent->right;
            if(GetColor(y) == 'r')
            {
                new_node->parent->color = 'b';
                y->color = 'b';
                new_node->parent->parent->color = 'r';
                new_node = new_node->parent->parent;
            }
            else
            {
                if(new_node == new_node->parent->right)
                {
                    new_node = new_node->parent;
                    LeftRotate(new_node);
                }
                new_node->parent->color = 'b';
                new_node->parent->parent->color = 'r';
                RightRotate(new_node->parent->parent);
            }
        }
        else
        {
            t_node<D>* y = new_node->parent->parent->left;
            if(GetColor(y) == 'r')
            {
                new_node->parent->color = 'b';
                y->color = 'b';
                new_node->parent->parent->color = 'r';
                new_node = new_node->parent->parent;
            }
            else
            {
                if(new_node == new_node->parent->left)
                {
                    new_node = new_node->parent;
                    RightRotate(new_node);
                }
                new_node->parent->color = 'b';
                new_node->parent->parent->color = 'r';
                LeftRotate(new_node->parent->parent);
            }
        }
    }
    root->color = 'b';
}

//Вставка узла в бинарное дерево
//Обычная вставка - не выполняется проверок на сбалансированность
//Не балансирует дерево
template<typename D>
void RBTree<D>::Insert(t_node<D>* z, t_node<D>* y)
{
    z->parent = y;
    if(y == nullptr)
        root = z;
    else if(z->data < y->data)
        y->left = z;
    else
        y->right = z;    
}
//Ищет и возврашает позицию, на которую нужно вставить элемент
//с заданным ключом
template<typename D>
t_node<D>* RBTree<D>::SearchInexact(std::string key)
{
    t_node<D>* y = nullptr;
    t_node<D>* x = root;

    while(x != nullptr && key != x->data)
    {
        y = x;
        if(key < x->data)
            x = x->left;
        else
            x = x->right;
    }
    if(x != nullptr)
        y = x;
    return y;
}




struct Edge
{
    std::string out;
    std::string in;
    int weight;

    bool operator<(const Edge& i)
    {
        return weight < i.weight;
    }
    bool operator>(const Edge& i)
    {
        return weight > i.weight;
    }
    bool operator!=(const Edge& i)
    {
        if((out == i.out) && (in == i.in) && (weight == i.weight))
            return false;
        else
        return true;
    }
    bool operator<=(const Edge& i)
    {
        return weight <= i.weight;
    }
    bool operator>=(const Edge& i)
    {
        return weight >= i.weight;
    }
};


//************************************************************************************
class Graph : public vector<Edge>
{
    public:
    void push_back(std::string, std::string, int);
    bool operator==(const Graph& tmp)
    {
        if(sz!=tmp.size())
            return false;
        for(auto i=0; i<sz; ++i)
        {
            if(this->elem[i] != tmp[i])
                return false;
        }
        return true;
    }
};

void Graph::push_back(std::string out, std::string in, int weight)
{
    Edge tmp;
    tmp.out = out;
    tmp.in = in;
    tmp.weight = weight;
    vector<Edge>::push_back(tmp);
}


class disjoint_set
{
    private:
    RBTree<std::string> set;
    RBTree<int> rank;

    public:

    disjoint_set(vector<std::string>& vertex)
    {
        for(int i=0; i<vertex.size(); i++)
        {
            set.RBInsert(vertex[i], vertex[i]);
            rank.RBInsert(vertex[i], 0);
        }
    }

    std::string Find(std::string x)
    {
        while(x != set[x])
        {
            x = set[x];
        }
        return x;
    }

    void Union(Edge x)
    {
        std::string rx=Find(x.out);
        std::string ry=Find(x.in);

        if(rx==ry)
        {
            return;
        }
        if(rank[rx]>rank[ry])
        {
            set[ry] = rx;
        }
        else
        {
            set[rx] = ry;
            if(rank[rx] == rank[ry])
            {
                rank[ry] = rank[rx]+1;
            }
        }

    }
};