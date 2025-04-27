from matplotlib.ticker import FuncFormatter


def horizontal_bar_options(ax, **options):
    
    ax.invert_yaxis()
    
   
    
    ax.set_title(options.get("title", "default title"), 
                loc = "left",
                pad= options.get("title_pad", 20))

    ax.set_xlabel(options.get("xlabel", ""), loc= "left")
    ax.set_ylabel(options.get("ylabel", ""), rotation= options.get("ylabel_rotation", 0))
    ax.yaxis.set_label_coords(options.get("ylabel_x_coord", -0.07), options.get("ylabel_y_coord", 1))
    ax.legend().remove()

    return ax




def save_fig_from_ax(ax, figpath, **options):
    
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(figpath, dpi= options.get("dpi", 300))
    
    
def thousands_formatter(ax, axis= "x"):
    formatter= FuncFormatter(
        lambda val, pos: f"{int(val/1000)}k" if val else f"{val:.0f}"
    )
    if axis == "x":
        ax.xaxis.set_major_formatter(formatter)
    elif axis == "y":
        ax.xaxis.set_major_formatter(formatter)
    elif axis == "both":
        ax.xaxis.set_major_formatter(formatter)
        
    return ax 