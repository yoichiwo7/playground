import json

import pandas as pd

from .util import get_parent_leaf_headers


#TODO: rafactor class/namespace organization.

class WriterConfig():
    def __init__(self,
        chart_width_ratio = 1.0,
        chart_height_ratio = 1.0,
        #TODO: make types more generic.
        chart_types = [("line", "unstacked"), ("area", "stacked")],
        chart_type_foreach = ("scatter", "")
    ):
        self.chart_width_ratio = chart_width_ratio
        self.chart_height_ratio = chart_height_ratio
        self.chart_types = chart_types
        self.chart_type_foreach = chart_type_foreach


class HtmlWriter():
    def __init__(self, writer_config = None):
        #TODO: prepare base class for Writer classes?
        if not writer_config:
            self.__config = WriterConfig()
        else:
            self.__config = writer_config
    
    def write_df_to_html(self, df, writer):
        #TODO: Use HTML template. Read data from df.
        parents_leaf_dict = get_parent_leaf_headers(df)
        l = [100, 10, 50, 2, 20, 30, 45]

        html = """
<html>

<head>
    <meta charset="utf-8">
    <title>Report</title>
</head>
 <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/1.11.8/semantic.min.css"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/1.11.8/semantic.min.js"></script>

<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.4.0/Chart.min.js"></script>
"""
        myid = 100
        for parent_tuple, cols in parents_leaf_dict.items():
            myid += 1
            # table
            html += '<body>'
            html += f'<h2>Statistics: {" : ".join(parent_tuple)}</h2>'
            html += df[parent_tuple].describe().to_html()

            # chart
            sub_df = df[parent_tuple]
            #TODO: Use application/json script tag for data separation?
            html += '<canvas id="canvas%d"></canvas> </body>' % (myid)
            #html += '<script type="application/json" id="json%d">' % (myid)
            #html += '</script>'
            html += "<script> var ctx = document.getElementById('canvas%d').getContext('2d'); " % (myid)
            #html += "var elem = document.getElementById('json%d');" % (myid)
            #html += "var data = JSON.parse(elem.textContent);"
            chart_json = {
                "type": "line",
                "data": {
                    "labels": sub_df.index.tolist(),
                    "datasets": [
                        {
                            "label": col,
                            "data": sub_df[col].values.tolist(),
                            "radius": 0
                        }
                        for col in cols
                    ]
                },
                "options": {
                    "title": {
                        "display": True,
                        "fontSize": 20,
                        "text": " : ".join(parent_tuple)
                    },
                    "legend": {
                        "display": True,
                    },
                    "animation": {
                        "duration": 0
                    },
                    "responsiveAnimationDuration": 0,
                    "elements": {
                        "line": {
                            "tension": 0, # disables bezier curves
                        }
                    },
                    "scales": {
                        "yAxes": [{
                            "stacked": True
                        }]
                    }
                }
            }
            html += f"var chart = new Chart(ctx, {json.dumps(chart_json)});"
            html += '</script>'
            html += '</html>'
        # Write to writer
        writer.write(html)


class XlsxWriter():
    def __init__(self, writer_config = None):
        if not writer_config:
            self.__config = WriterConfig()
        else:
            self.__config = writer_config

    def write_df_to_excel(self, writer, df: pd.DataFrame, name, index=True,
            enable_data_sheet=True,
            enable_stats_sheet=True,
            enable_chart_sheet=True,
            chart_each=False,
            use_png=False) -> None:
        """
        Write data, statistics, and charts of specifed DataFrame.

        writer : writer object of xlsxwriter
        df : input pd.DataFrame
        chart_each : add chart for each series (ex. usr, sys, wait)
        """

        #TODO: add use_png support

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
        if enable_data_sheet:
            sheet_name_data = f'{name}_DATA'
            df.to_excel(writer, sheet_name_data,
                float_format='%.2f', index=index, freeze_panes=(row_start_pos, FIXED_COL_POS))

        ## add STAT
        if enable_stats_sheet:
            df_stats = df.describe(percentiles=[.25, .50, .75, .90, .99])
            sheet_name_stats = f'{name}_STATS'
            df_stats.to_excel(writer, sheet_name_stats, float_format='%.2f', index=index)

        ## add CHART
        if enable_chart_sheet:
            self.__add_chart_sheet(writer, parents_leaf_dict, sheet_name_data, name,
                parents_num, row_start_pos, row_end_pos, chart_each=chart_each)


    def __add_chart_sheet(self, writer, parents_leaf_dict, sheet_name_data, name, parents_num, row_start_pos, row_end_pos, chart_each=False):
        sheet_name_chart = f'{name}_CHART'
        wb = writer.book
        ws = wb.add_worksheet(sheet_name_chart)
        chart_pos = 1
        chart_height = int(18 * self.__config.chart_height_ratio)

        #all
        current_col_pos = 0
        for parents, leafs  in parents_leaf_dict.items():
            # sub_df = df
            # for p in parents:
            #     sub_df = df[p]
            #ALL
            start_col_pos_of_hdr = current_col_pos
            for t, subtype in self.__config.chart_types:
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
                self.__set_nice_chart(chart)
                for _ in leafs:
                    current_col_pos += 1
                    chart.add_series({
                        'name':       [sheet_name_data, parents_num, current_col_pos],
                        # 2-level multi index -> +2 to row position
                        # range is inclusive (need te decrement)
                        'values':     [sheet_name_data, row_start_pos, current_col_pos, row_end_pos-1, current_col_pos],
                    })
                ws.insert_chart(row=chart_pos, col=1, chart=chart)
                chart_pos += chart_height
            #EACH
            if not chart_each:
                continue
            for col_pos, leaf in enumerate(leafs, 1):
                sub_chart = wb.add_chart({
                    'type': self.__config.chart_type_foreach[0],
                    'subtype': self.__config.chart_type_foreach[1]
                })
                sub_chart.set_title({
                    'name': f'{"::".join(parents)} [{leaf}]'
                })
                self.__set_nice_chart(sub_chart, style_id=43)  #42:dark layout
                categories = None
                if self.__config.chart_type_foreach[0] == "scatter":
                    categories = [sheet_name_data, row_start_pos, 0, row_end_pos-1, 0]
                sub_chart.add_series({
                    'name':       [sheet_name_data, parents_num, col_pos],
                    'categories': categories,
                    'values':     [sheet_name_data, row_start_pos, col_pos, row_end_pos-1, col_pos],
                })
                ws.insert_chart(row=chart_pos, col=1, chart=sub_chart)
                chart_pos += chart_height



    def __set_nice_chart(self, chart, style_id=2):
        chart.set_style(style_id)  #nice ids: 10,34*,50  (2+8x)
        chart.set_size({
            'x_scale': 1.5 * self.__config.chart_width_ratio,
            'y_scale': 1.2 * self.__config.chart_height_ratio
        })
        chart.set_chartarea({
            'border': {'color': 'black'}
        })
        chart.set_legend({
            'position': 'bottom'
        })


    #TODO: make this usable
    def plot_df(self, df: pd.DataFrame, name="zzz"):
        ax = df.plot(kind='area', stacked=True, alpha=0.4)
        fig = ax.get_figure()
        #NOTE: eps, pdf, pgf, png, ps, raw, rgba, svg, svgz
        fig.savefig(f'images/{name}.pdf')

