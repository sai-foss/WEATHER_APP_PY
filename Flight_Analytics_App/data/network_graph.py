import plotly.graph_objects as go


def two_node_directed(weight: float = 500) -> go.Figure:
    # Positions
    x0, y0 = 0, 0
    x1, y1 = 10, 0

    fig = go.Figure()

    # Edge (for hover)
    fig.add_trace(
        go.Scatter(
            x=[x0, x1],
            y=[y0, y1],
            mode="lines",
            hoverinfo="text",
            text=[f"weight: {weight}"],
            line=dict(width=6),
        )
    )

    # Nodes
    fig.add_trace(
        go.Scatter(
            x=[x0, x1],
            y=[y0, y1],
            mode="markers+text",
            text=["A", "B"],
            textposition="bottom center",
            marker=dict(size=60),
            hoverinfo="skip",
        )
    )

    # Direction arrow A -> B
    fig.add_annotation(
        x=x1,
        y=y1,
        ax=x0,
        ay=y0,
        xref="x",
        yref="y",
        axref="x",
        ayref="y",
        showarrow=True,
        arrowhead=3,
        arrowsize=1.2,
        arrowwidth=4,
        text="",
    )

    # Weight label near midpoint
    fig.add_annotation(x=(x0 + x1) / 2, y=y0 + 0.6, text=str(weight), showarrow=False)

    fig.update_layout(
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(visible=False, range=[-2, 12]),
        yaxis=dict(visible=False, range=[-3, 3], scaleanchor="x", scaleratio=1),
    )
    return fig
