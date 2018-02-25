import pandas as pd

from .util import get_parent_leaf_headers

#TOOD: maybe turn it to class?

def write_df_to_excel(writer, df: pd.DataFrame, name, index=True, chart_each=False) -> None:
    """
    Write data, statistics, and charts of specifed DataFrame.

    writer : writer object of xlsxwriter
    df : input pd.DataFrame
    chart_each : add chart for each series (ex. usr, sys, wait)
    """
    FIXED_COL_POS = 0
    parents_leaf_dict = get_parent_leaf_headers(df)
    parents_num = max([len(parents) for parents in parents_leaf_dict.keys()])
    row_start_pos = 1
    if parents_num > 0:
        row_start_pos += parents_num
        row_start_pos += 1 # a blank row will be added at multi-index
    row_end_pos = row_start_pos + len(df)

    #TODO: adjust column width for DATA/STATS sheets.
    ## add DATA
    sheet_name_data = f'{name}_DATA'
    df.to_excel(writer, sheet_name_data,
        float_format='%.2f', index=index, freeze_panes=(row_start_pos, FIXED_COL_POS))

    ## add STAT
    df_stats = df.describe(percentiles=[.25, .50, .75, .90, .99])
    sheet_name_stats = f'{name}_STATS'
    df_stats.to_excel(writer, sheet_name_stats, float_format='%.2f', index=index)

    ## add CHART
    __add_chart_sheet(writer, parents_leaf_dict, sheet_name_data, name,
        parents_num, row_start_pos, row_end_pos, chart_each=chart_each)


def __add_chart_sheet(writer, parents_leaf_dict, sheet_name_data, name, parents_num, row_start_pos, row_end_pos, chart_each=False):
    sheet_name_chart = f'{name}_CHART'
    wb = writer.book
    ws = wb.add_worksheet(sheet_name_chart)
    chart_pos = 1
    CHART_HEIGHT = 18

    #all
    current_col_pos = 0
    for parents, leafs  in parents_leaf_dict.items():
        # sub_df = df
        # for p in parents:
        #     sub_df = df[p]
        #ALL
        start_col_pos_of_hdr = current_col_pos
        for t, subtype in [('area', 'stacked'), ('line', 'unstacked')]:
            current_col_pos = start_col_pos_of_hdr
            chart = wb.add_chart({
                'type': t, 
                'subtype': subtype
            })
            if len(parents) == 0:
                parents = (name,)
            chart.set_title({
                'name': f'{"::".join(parents)} - {subtype.capitalize()}'
            })
            __set_nice_chart(chart)
            for _ in leafs:
                current_col_pos += 1
                chart.add_series({
                    'name':       [sheet_name_data, parents_num, current_col_pos],
                    # 2-level multi index -> +2 to row position
                    # range is inclusive (need te decrement)
                    'values':     [sheet_name_data, row_start_pos, current_col_pos, row_end_pos-1, current_col_pos],
                })
            ws.insert_chart(row=chart_pos, col=1, chart=chart)
            chart_pos += CHART_HEIGHT
        #EACH
        if not chart_each:
            continue
        for col_pos, leaf in enumerate(leafs, 1):
            sub_chart = wb.add_chart({'type': 'line'})
            sub_chart.set_title({
                'name': f'{"::".join(parents)} [{leaf}]'
            })
            __set_nice_chart(sub_chart, style_id=43)  #42:dark layout
            sub_chart.add_series({
                'name':       [sheet_name_data, parents_num, col_pos],
                'values':     [sheet_name_data, row_start_pos, col_pos, row_end_pos-1, col_pos],
            })
            ws.insert_chart(row=chart_pos, col=1, chart=sub_chart)
            chart_pos += CHART_HEIGHT


def __set_nice_chart(chart, style_id=2):
    chart.set_style(style_id)  #nice ids: 10,34*,50  (2+8x)
    chart.set_size({
        'x_scale': 1.5, 
        'y_scale': 1.2
    })
    chart.set_chartarea({
        'border': {'color': 'black'}
    })
    chart.set_legend({
        'position': 'bottom'
    })


#TODO: make this usable
def plot_df(df: pd.DataFrame, name="zzz"):
    ax = df.plot(kind='area', stacked=True, alpha=0.4)
    fig = ax.get_figure()
    #NOTE: eps, pdf, pgf, png, ps, raw, rgba, svg, svgz
    fig.savefig(f'images/{name}.pdf')

