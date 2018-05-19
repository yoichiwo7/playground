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
        header = """
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
        footer = """
</html>
        """
        html = header
        first_level_cols = set([tup[0] for tup in df.columns.tolist()])
        l = [100, 10, 50, 2, 20, 30, 45]
        for col in first_level_cols:
            # table
            html += '<body>'
            html += f'<h2>Statistics: {col}</h2>'
            html += df[col].describe().to_html()

            # chart
            #TODO: 
            html += '<canvas id="%s"></canvas> </body>' % (col)
            html += '<script type="application/json" id="json%s">' % (col)
            l = [e*2 for e in l]
            html += str(l)
            html += '</script>'
            html += "<script> var ctx = document.getElementById('%s').getContext('2d'); " % (col)
            html += "var elem = document.getElementById('json%s');" % (col)
            html += """
console.log(elem);
var data = JSON.parse(elem.textContent);
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: ["January", "February", "March", "April", "May", "June", "July"],
        datasets: [{
            label: "My First dataset",
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: data,
        }]
    },

    // Configuration options go here
    options: {}
});
            </script>
            """

        html += footer
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

