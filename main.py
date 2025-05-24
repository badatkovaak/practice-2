from copy import deepcopy
from typing import Callable
from flet.matplotlib_chart import MatplotlibChart
import flet as ft
import matplotlib.pyplot as plt
import numerical_solver as ns
import re


def main(page: ft.Page):
    def create_figure_from_params(info: ns.MilneMethodInfo):
        fig = plt.figure()
        ax = fig.add_subplot()

        if len(info.ys) > 1:
            for _ in range(len(info.ys) - 1):
                info.ys.pop()

            info.n = 1

        try:
            ns.numerically_solve(info)
        except ZeroDivisionError:
            print("ZeroDivisionError has occurred, input correct data")
            return fig

        xs = [info.x_start + i * info.h for i in range(info.n)]
        ax.plot(xs, info.ys, "r")

        return fig

    def create_function(input: str) -> Callable[[float, float], float] | None:
        input1 = deepcopy(input)
        input1 = re.sub(r"math\.[a-zA-Z]{2,}", "", input1)

        if re.match(r".*[a-zA-Z]{2,}.*", input1):
            print("passed invalid function")
            return None

        function_template = (
            f"import math\n\ndef f(x,y):\n  res = {input}\n  return res\n"
        )

        try:
            code = compile(function_template, "<string>", "exec")
        except Exception:
            print("an error occurred while compiling")
            return None

        namespace = {}

        try:
            exec(code, namespace)
        except Exception:
            print("an error occurred while in exec")
            return None

        return namespace["f"]

    def update_figure(info: ns.MilneMethodInfo, chart: MatplotlibChart):
        chart.figure = create_figure_from_params(info)
        chart.update()

    def upadate_table(info: ns.MilneMethodInfo, value_table: ft.DataTable):
        if value_table.rows is None:
            return

        if value_table.rows.__len__() > 0:
            for _ in range(value_table.rows.__len__()):
                value_table.rows.pop()

        data_table_len = min(10, info.ys.__len__())
        for i in range(data_table_len):
            value_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(info.x_start + i * info.h))),
                        ft.DataCell(ft.Text(str(info.ys[i]))),
                    ],
                )
            )

        page.update()

    def h_on_submit(
        info: ns.MilneMethodInfo, chart: MatplotlibChart, value_table: ft.DataTable, e
    ):
        print(e)
        info.h = float(e.data)
        update_figure(info, chart)
        upadate_table(info, value_table)

    def x_start_on_submit(
        info: ns.MilneMethodInfo, chart: MatplotlibChart, value_table: ft.DataTable, e
    ):
        print(e)
        info.x_start = float(e.data)
        update_figure(info, chart)
        upadate_table(info, value_table)

    def x_end_on_submit(
        info: ns.MilneMethodInfo, chart: MatplotlibChart, value_table: ft.DataTable, e
    ):
        print(e)
        info.x_end = float(e.data)
        update_figure(info, chart)
        upadate_table(info, value_table)

    def y_start_on_submit(
        info: ns.MilneMethodInfo, chart: MatplotlibChart, value_table: ft.DataTable, e
    ):
        print(e)
        info.ys[0] = float(e.data)
        update_figure(info, chart)
        upadate_table(info, value_table)

    def function_on_submit(
        info: ns.MilneMethodInfo, chart: MatplotlibChart, value_table: ft.DataTable, e
    ):
        print("function - ", e)
        f = create_function(e.data)

        if f is None:
            return

        info.f = f

        update_figure(info, chart)
        upadate_table(info, value_table)

    page.title = "Practice App"
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    info = ns.MilneMethodInfo(
        f=lambda x, y: x + y * x,
        y_start=2,
        x_start=2,
        x_end=3,
        h=0.01,
    )

    chart = None
    value_table = None
    func = lambda f: lambda x: f(info, chart, value_table, x)

    page.add(
        ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(
                            "derivative of y (use y and x as variables, python math module is available):"
                        ),
                        ft.TextField(
                            value="x + y/x",
                            on_submit=func(function_on_submit),
                        ),
                        ft.Text("h:"),
                        ft.TextField(
                            value="0.01",
                            on_submit=func(h_on_submit),
                        ),
                        ft.Text("start value of x:"),
                        ft.TextField(
                            value="2",
                            on_submit=func(x_start_on_submit),
                        ),
                        ft.Text("end value of x:"),
                        ft.TextField(
                            value="3",
                            on_submit=func(x_end_on_submit),
                        ),
                        ft.Text("start value of y:"),
                        ft.TextField(
                            value="1",
                            on_submit=func(y_start_on_submit),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                value_table := ft.DataTable(
                    columns=[ft.DataColumn(ft.Text("x")), ft.DataColumn(ft.Text("y"))],
                    vertical_lines=ft.BorderSide(1, ft.Colors.GREY_800),
                ),
                chart := MatplotlibChart(
                    create_figure_from_params(info), isolated=True, original_size=True
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        )
    )

    upadate_table(info, value_table)
    page.update()


if __name__ == "__main__":
    ft.app(main)
