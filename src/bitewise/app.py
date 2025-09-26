# Minimal stub so the CLI can launch without Gemini or full notebook code.

def run() -> int:
    """
    Launch a tiny placeholder UI if running inside Jupyter,
    otherwise print clear instructions.
    """
    try:
        import ipywidgets as widgets
        from IPython.display import display
    except Exception:
        print(
            "BiteWise demo requires Jupyter + ipywidgets.\n"
            "Install and run:\n"
            "  pip install jupyterlab ipywidgets\n"
            "  jupyter lab  # then open notebooks/bitewise_demo.ipynb"
        )
        return 1

    header = widgets.HTML(
        "<h2>BiteWise demo (stub)</h2>"
        "<p>This is a placeholder. Real UI coming next step.</p>"
    )
    btn = widgets.Button(description="Say hi")
    out = widgets.Output()

    def _click(_):
        with out:
            out.clear_output()
            print("BiteWise is alive. ✅")

    btn.on_click(_click)
    display(widgets.VBox([header, btn, out]))
    return 0