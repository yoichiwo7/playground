import json

from jinja2 import Environment, FileSystemLoader
import pandas as pd
import altair as alt
alt.data_transformers.enable('default', max_rows=None)

from .util import get_parent_leaf_headers, down_sample_df, get_colors


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


class HtmlChartjsWriter():
    def __init__(self, writer_config = None):
        #TODO: prepare base class for Writer classes?
        if not writer_config:
            self.__config = WriterConfig()
        else:
            self.__config = writer_config
    
    def write_df_to_html(self, df, writer, max_samples=None) -> str:
        """
        Write HTML string to writer.
        Returns HTML string.
        """
        border_colors = get_colors(1.0)
        bg_colors = get_colors(1.0)

        parents_leaf_dict = get_parent_leaf_headers(df)

        # NOTE: make generators for less memory usage. (chart and table strings might be very large)
        def make_table_generator(parent_tuple, cols, df):
            df_stats = df[parent_tuple].describe(percentiles=[.25, .50, .75, .90, .99, .999]).round(2)
            table = df_stats.to_html(col_space=10, justify="center")
            return table
        def make_chart_generator(parent_tuple, cols, df, chart_type):
            df_data = df[parent_tuple]
            if max_samples:
                df_data = down_sample_df(df_data, max_samples=max_samples)
            chart_json = self.__get_chart_json_dict(df_data, parent_tuple, cols, border_colors, bg_colors, chart_type)
            return json.dumps(chart_json)

        titles = [" : ".join(parent_tuple)
                        for parent_tuple in parents_leaf_dict.keys()]
        table_gn = (make_table_generator(parent_tuple, cols, df) 
                        for parent_tuple, cols in parents_leaf_dict.items())
        line_chart_gn = (make_chart_generator(parent_tuple, cols, df, "line") 
                        for parent_tuple, cols in parents_leaf_dict.items())
        area_chart_gn = (make_chart_generator(parent_tuple, cols, df, "area") 
                        for parent_tuple, cols in parents_leaf_dict.items())

        # Write to writer
        #TODO: specify path in better way(from module path)
        env = Environment(loader=FileSystemLoader('./plogpy/static', encoding='utf8'))
        env.globals.update(zip=zip)
        tpl = env.get_template('report.j2')
        html = tpl.render({
            "titles": titles,
            "tables": table_gn,
            "line_charts": line_chart_gn,
            "area_charts": area_chart_gn,
        })
        if writer:
            writer.write(html)
        return html
    
    def __get_chart_json_dict(self, df_data, parent_tuple, cols, border_colors, bg_colors, t):
        #TODO: Better input parameter. Fix filling bg color problem with alpha.
        #TODO: generate fills list dynamically
        if t is "line":
            chart_type = "line"
            fills = [False for _ in range(10)]
            border_width = 2
            stacked = False
        elif t is "area":
            chart_type = "line"
            fills = ['-1' for _ in range(10)]
            fills.insert(0, "origin")
            border_width = 0
            stacked = True
        else:
            raise Exception(f"Unsupported chart type: {t}")
        d = {
            "type": chart_type,
            "data": {
                "labels": df_data.index.tolist(),
                "datasets": [
                    {
                        "label": col,
                        "data": df_data[col].values.tolist(),
                        "radius": 0,
                        "fill": fill,
                        "borderWidth": 2,
                        "borderColor": fg,
                        "backgroundColor": fg
                    }
                    for col, fg, bg, fill in zip(cols, border_colors, bg_colors, fills)
                ]
            },
            "options": {
                "title": {
                    "display": True,
                    "fontSize": 20,
                    "text": " : ".join(parent_tuple) + f" <<{t} chart>>"
                },

                "chartArea": {
                    "backgroundColor": 'rgba(240, 240, 240, 1)'
                },

                "legend": {
                    "display": True,
                },
                
                # Disable animation
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
                        "stacked": stacked
                    }]
                }
            }
        }
        return d


#TODO: use this or not?
class HtmlEchartsWriter():
    def __init__(self, writer_config = None):
        #TODO: prepare base class for Writer classes?
        if not writer_config:
            self.__config = WriterConfig()
        else:
            self.__config = writer_config
    
    def write_df_to_html(self, df, writer, max_samples=None) -> str:
        """
        Write HTML string to writer.
        Returns HTML string.
        """
        parents_leaf_dict = get_parent_leaf_headers(df)

        # NOTE: make generators for less memory usage. (chart and table strings might be very large)
        def make_table_generator(parent_tuple, cols, df):
            df_stats = df[parent_tuple].describe(percentiles=[.25, .50, .75, .90, .99, .999]).round(2)
            table = df_stats.to_html(col_space=10, justify="center")
            return table
        def make_chart_generator(parent_tuple, cols, df):
            df_data = df[parent_tuple]
            if max_samples:
                df_data = down_sample_df(df_data, max_samples=max_samples)
            chart_json = self.__get_chart_json_dict(df_data, parent_tuple, cols)
            return json.dumps(chart_json)

        titles = [" : ".join(parent_tuple)
                        for parent_tuple in parents_leaf_dict.keys()]
        table_gn = (make_table_generator(parent_tuple, cols, df) 
                        for parent_tuple, cols in parents_leaf_dict.items())
        chart_gn = (make_chart_generator(parent_tuple, cols, df) 
                        for parent_tuple, cols in parents_leaf_dict.items())

        # Write to writer
        #TODO: specify path in better way(from module path)
        env = Environment(loader=FileSystemLoader('./plogpy/static', encoding='utf8'))
        env.globals.update(zip=zip)
        tpl = env.get_template('echarts.j2')
        html = tpl.render({
            "titles": titles,
            "tables": table_gn,
            "charts": chart_gn,
        })
        if writer:
            writer.write(html)
        return html
    
    def __get_chart_json_dict(self, df_data, parent_tuple, cols):
        d = {
            "title": {
                "text": ' '.join(parent_tuple)
            },
            "tooltip": {},
            "legend": {
                "data": cols
            },
            "xAxis": {
                "data": df_data.index.tolist()
            },
            "yAxis": {},
            "series": [
                {
                    "name": col,
                    "type": 'line',
                    "stack": 'stacked',
                    "areaStyle": {"normal": {}},
                    "data": df_data[col].values.tolist()
                }
                for col in cols
            ]
        }
        return d


class XlsxWriter():
    def __init__(self, writer_config = None):
        if not writer_config:
            self.__config = WriterConfig()
        else:
            self.__config = writer_config

    def write_df_to_excel(self, writer, df: pd.DataFrame, name, index=True,
            max_samples=None,
            enable_data_sheet=True,
            enable_stats_sheet=True,
            enable_chart_sheet=True,
            chart_each=False) -> None:
        """
        Write data, statistics, and charts of specifed DataFrame.

        writer : writer object of xlsxwriter
        df : input pd.DataFrame
        chart_each : add chart for each series (ex. usr, sys, wait)
        """

        df_stats = df.describe(percentiles=[.25, .50, .75, .90, .99])
        df_data = df

        print(max_samples)
        if max_samples:
            df_data = down_sample_df(df_data, max_samples=max_samples)

        FIXED_COL_POS = 0
        parents_leaf_dict = get_parent_leaf_headers(df_data)
        parents_num = max([len(parents) for parents in parents_leaf_dict.keys()])
        row_start_pos = 1
        if parents_num > 0:
            row_start_pos += parents_num
            row_start_pos += 1 # a blank row will be added at multi-index
        row_end_pos = row_start_pos + len(df_data)

        #TODO: adjust column width for DATA/STATS sheets.
        ## add DATA
        if enable_data_sheet:
            sheet_name_data = f'{name}_DATA'
            df_data.to_excel(writer, sheet_name_data,
                float_format='%.2f', index=index, freeze_panes=(row_start_pos, FIXED_COL_POS))

        ## add STAT
        if enable_stats_sheet:
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
