import networkx as nx


def print_ascii_tree(adj, root, node_str=str, sort_children=False, max_depth=None):
    """
    Affiche un arbre en ASCII en compactant les chaînes de nœuds à enfant unique
    (ex: A ─ B ─ C). Les branches des enfants du dernier nœud de la chaîne
    sont alignées sous ce dernier.
    - adj: dict {noeud: [enfants]}
    - root: racine
    - node_str: fonction d'affichage d'un noeud -> str
    - sort_children: trie les enfants pour un rendu stable
    - max_depth: profondeur max à afficher (None = illimité)
    """
    seen = set()

    def children_of(n):
        ch = list(adj.get(n, []))
        if sort_children:
            ch.sort(key=node_str)
        return ch

    def collapse_chain(start):
        """Retourne (head_text, last_text, last_node, added_depth)
        head_text: texte avant le dernier (ex: 'A ─ B ─ ')
        last_text: texte du dernier noeud de la chaîne
        """
        chain = [start]
        cur = start
        added = 0
        while True:
            ch = children_of(cur)
            if len(ch) == 1 and ch[0] not in seen:
                cur = ch[0]
                chain.append(cur)
                seen.add(cur)
                added += 1
            else:
                break
        parts = [node_str(x) for x in chain]
        if len(parts) == 1:
            head_text, last_text = "", parts[0]
        else:
            head_text = " ─ ".join(parts[:-1]) + " ─ "
            last_text = parts[-1]
        return head_text, last_text, chain[-1], added

    def recurse(node, prefix, is_last, is_root=False, depth=0):
        if max_depth is not None and depth > max_depth:
            return
        head_text, last_text, last_node, added = collapse_chain(node)

        # Ligne courante
        marker = "" if is_root else ("└─ " if is_last else "├─ ")
        print(prefix + marker + head_text + last_text)

        # Préfixe pour les enfants: prolonger la colonne verticale si nécessaire
        child_prefix = prefix
        if not is_root:
            child_prefix += "  " if is_last else "│ "
        # Décalage supplémentaire pour aligner sous le dernier noeud de la chaîne
        child_prefix += " " * len(head_text)

        # Enfants du dernier noeud de la chaîne
        ch = children_of(last_node)
        for i, c in enumerate(ch):
            if c in seen:
                print(
                    child_prefix
                    + ("└─ " if i == len(ch) - 1 else "├─ ")
                    + node_str(c)
                    + " ↺"
                )
                continue
            seen.add(c)
            recurse(
                c,
                child_prefix,
                i == len(ch) - 1,
                is_root=False,
                depth=depth + 1 + added,
            )

    seen.add(root)
    recurse(root, prefix="", is_last=True, is_root=True, depth=0)


def print_nx_tree(G, root, **kwargs):
    """
    Construit un arbre BFS depuis 'root' puis l'affiche avec print_ascii_tree.
    **kwargs sont passés à print_ascii_tree (node_str, sort_children, max_depth).
    """
    bfs_tree = nx.bfs_tree(G, root)  # garantit un arbre (pas de cycles)
    adj = {u: list(bfs_tree.successors(u)) for u in bfs_tree.nodes()}
    print_ascii_tree(adj, root, **kwargs)
