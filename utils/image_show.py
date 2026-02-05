
import os


def show_image(agent):
    png_bytes = agent.get_graph(xray=True).draw_mermaid_png()
    with open("agent_graph.png", "wb") as f:
        f.write(png_bytes)
    os.system("open agent_graph.png")