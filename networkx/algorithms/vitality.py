#    Copyright (C) 2012 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.
"""
Vitality measures.
"""
from .wiener import wiener_index

__author__ = "\n".join(['Aric Hagberg (hagberg@lanl.gov)',
                        'Renato Fabbri'])
__all__ = ['closeness_vitality']


def closeness_vitality(G, node=None, weight=None):
    """Returns the closeness vitality for nodes in the graph.

    The *closeness vitality* of a node, defined in Section 3.6.2 of [1],
    is the change in the sum of distances between all node pairs when
    excluding that node.

    Parameters
    ----------
    G : NetworkX graph
        A strongly-connected graph.

    weight : string
        The name of the edge attribute used as weight. This is passed
        directly to the :func:`~networkx.wiener_index` function.

    node : object
        If specified, only the closeness vitality for this node will be
        returned. Otherwise, a dictionary mappping each node to its
        closeness vitality will be returned.

    Returns
    -------
    dictionary or float
        If ``node`` is ``None``, this function returnes a dictionary
        with nodes as keys and closeness vitality as the
        value. Otherwise, it returns only the closeness vitality for the
        specified ``node``.

        The closeness vitality of a node may be negative infinity if
        removing that node would disconnect the graph.

    Examples
    --------
    >>> import networkx as nx
    >>> G = nx.cycle_graph(3)
    >>> nx.closeness_vitality(G)
    {0: 2.0, 1: 2.0, 2: 2.0}

    See Also
    --------
    closeness_centrality

    References
    ----------
    .. [1] Ulrik Brandes, Thomas Erlebach (eds.).
           *Network Analysis: Methodological Foundations*.
           Springer, 2005.
           <http://books.google.com/books?id=TTNhSm7HYrIC>

    """
    if node is not None:
        before = wiener_index(G, weight=weight)
        after = wiener_index(G.subgraph(set(G) - {node}), weight=weight)
        return before - after
    # TODO This can be trivially parallelized.
    return {v: closeness_vitality(G, node=v, weight=weight) for v in G}
