#include "structures.h"
#include <fstream>
#include <cctype>

int partition(Graph& a,int start,int end)
{
    Edge pivot=a[end];
    int P_index=start;
    int i;
    Edge t; 
    
    for(i=start;i<end;i++)
    {
    	if(a[i]<=pivot)
        {
            t=a[i];
            a[i]=a[P_index];
            a[P_index]=t;
            P_index++;
        }
     }
      t=a[end];
      a[end]=a[P_index];
      a[P_index]=t;
     return P_index;
}

 void Quicksort(Graph& a,int start,int end)
{
    if(start<end)
    {
         int P_index=partition(a,start,end);
             Quicksort(a,start,P_index-1);
             Quicksort(a,P_index+1,end);
    }
}

void Print(Graph ar)
{
    for (auto i=0; i<ar.size();++i)
        std::cout << ar[i].out << ' ' << ar[i].in << ' ' << ar[i].weight << '\n';
}

template<typename D>
void pre_order(t_node<D>* a, vector<std::string>& out)
{
    if(a == nullptr)
        return;
    out.push_back(a->data);
    pre_order(a->left, out);
    pre_order(a->right, out);
}

void read_file(std::string filename, Graph& out_graph, RBTree<int>& unique, int& f_)
{
    std::ifstream file(filename.c_str());
    if(!file.is_open())
    {
        std::cout << "File doesn't exist\n";
        f_++;
        return;
    }
    std::string first;
    std::string second;
    int len;   
    while(file >> first >> second >> len)
    {
        out_graph.push_back(first, second, len);
        unique.RBInsert(first, 0);
        unique.RBInsert(second, 0);
    }
    f_ = 0;
}



int main()
{
    Graph gr;
    RBTree<int> unique;
    std::string uq;
    vector<std::string> tu;
    int file_flag=0;
    std::string filename;
    do
    {
        std::cout << "Insert file's name: ";
        std::cin  >> filename;
        read_file(filename, gr, unique, file_flag);
    }
    while(file_flag);
    
    pre_order(unique.GetRoot(), tu);
    Quicksort(gr, 0, gr.size()-1);

    disjoint_set ds(tu);
    int sum=0;
    for (int i = 0; i < gr.size(); i++)
    {
         if(ds.Find(gr[i].out) != ds.Find(gr[i].in))
         {
             std::cout << gr[i].out << ' ' << gr[i].in << '\n';
             ds.Union(gr[i]);
             sum+=gr[i].weight;
         }
    }
    std::cout  << sum << '\n';
}