import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        self.G = nx.Graph()
        self.dict_rifugi={}

    def build_graph(self, year: int):
        """
        Costruisce il grafo (self.G) dei rifugi considerando solo le connessioni
        con campo `anno` <= year passato come argomento.
        Quindi il grafo avrà solo i nodi che appartengono almeno ad una connessione, non tutti quelli disponibili.
        :param year: anno limite fino al quale selezionare le connessioni da includere.
        """
        rifugi=DAO.readRifugi()
        for r in rifugi:
            self.dict_rifugi[r.id]=r

        archi_anno=DAO.read_connessioni_per_anno(year)

        for (u_nodo_id,v_nodo_id) in archi_anno:
            if u_nodo_id in self.dict_rifugi and v_nodo_id in self.dict_rifugi:
                u_nodo=self.dict_rifugi[u_nodo_id]
                v_nodo=self.dict_rifugi[v_nodo_id]
                self.G.add_edge(u_nodo,v_nodo)


    def get_nodes(self):
        """
        Restituisce la lista dei rifugi presenti nel grafo.
        :return: lista dei rifugi presenti nel grafo.
        """
        lista_nodi=[]
        for nodo in self.G.nodes:
            lista_nodi.append(nodo)
        return lista_nodi

    def get_num_neighbors(self, node):
        """
        Restituisce il grado (numero di vicini diretti) del nodo rifugio.
        :param node: un rifugio (cioè un nodo del grafo)
        :return: numero di vicini diretti del nodo indicato
        """
        return self.G.degree(node)

    def get_num_connected_components(self):
        """
        Restituisce il numero di componenti connesse del grafo.
        :return: numero di componenti connesse
        """
        return nx.number_connected_components(self.G)

    def get_reachable(self, start):
        """
        Deve eseguire almeno 2 delle 3 tecniche indicate nella traccia:
        * Metodi NetworkX: `dfs_tree()`, `bfs_tree()`
        * Algoritmo ricorsivo DFS
        * Algoritmo iterativo
        per ottenere l'elenco di rifugi raggiungibili da `start` e deve restituire uno degli elenchi calcolati.
        :param start: nodo di partenza, da non considerare nell'elenco da restituire.

        ESEMPIO
        a = self.get_reachable_bfs_tree(start)
        b = self.get_reachable_iterative(start)
        b = self.get_reachable_recursive(start)

        return a
        """
        albero=nx.bfs_tree(self.G, start)
        nodi=list(albero.nodes)
        nodi.remove(start)

        visitati=[]
        self.dfs(start,visitati)
        visitati.remove(start)
        return visitati


    def dfs(self,start,visitati):
        visitati.append(start)
        for vicino in self.G.neighbors(start):
            if vicino not in visitati:
                self.dfs(vicino,visitati)

