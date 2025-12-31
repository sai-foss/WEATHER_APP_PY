import base64
from io import BytesIO

import matplotlib

matplotlib.use("Agg")  # server-side
import matplotlib.pyplot as plt
import networkx as nx


def ab_graph_png_data_url(weight: float = 500) -> str:
    G = nx.DiGraph()
    G.add_edge("A", "B")

    pos = {"A": (0, 0), "B": (1, 0)}  # fixed positions

    fig, ax = plt.subplots(figsize=(5, 2.2), dpi=160)
    fig.patch.set_facecolor("#18191b")
    ax.set_facecolor("black")
    ax.axis("off")
    ax.set_title(
        "Total Scheduled flights",
        color="white",
        fontsize=18,
        pad=10,
    )

    # Nodes (labels inside nodes)
    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=2200,
        node_color="#9ec5ff",
        ax=ax,
    )
    nx.draw_networkx_labels(
        G,
        pos,
        labels={"A": "ONT", "B": "DFW"},
        font_size=16,
        font_weight="bold",
        font_color="black",
        ax=ax,
    )

    # Directed edge
    nx.draw_networkx_edges(
        G,
        pos,
        ax=ax,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=25,
        width=3.5,
        edge_color="#9ec5ff",
        min_source_margin=27,  # adhoc
        min_target_margin=23,  # also adhoc
        connectionstyle="arc3,rad=0.0",
    )

    # Weight label on edge
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels={("A", "B"): str(weight)},
        font_color="white",
        font_size=20,
        bbox=dict(boxstyle="round,pad=0.2", fc="#18191b", ec="none"),
        ax=ax,
    )

    buf = BytesIO()
    plt.tight_layout(pad=0)
    fig.savefig(
        buf,
        format="png",
        bbox_inches="tight",
        pad_inches=0.05,
        facecolor=fig.get_facecolor(),
    )
    plt.close(fig)

    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64}"
