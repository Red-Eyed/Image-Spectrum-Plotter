#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil

import numpy as np
import cv2 as cv
from plotly.offline import plot
import plotly.graph_objs as go
import pandas as pd


print("Script started!")

image_path = os.path.abspath("images")
plots_path = os.path.abspath("plots")
excel_path = os.path.abspath("excels")

shutil.rmtree(plots_path, ignore_errors=True)
os.mkdir(plots_path)

shutil.rmtree(excel_path, ignore_errors=True)
os.mkdir(excel_path)

excel_filename = os.path.join(excel_path, "all_excel.xlsx")
excel_writer = pd.ExcelWriter(excel_filename, engine='xlsxwriter')

for image_name in os.listdir(image_path):

    image = cv.imread(os.path.join(image_path, image_name), cv.IMREAD_GRAYSCALE).astype(np.float32)
    size = (500, 500)
    image = cv.resize(image, size)
    image = cv.normalize(image, image, 0, 1, cv.NORM_MINMAX)

    data = [go.Surface(z=image)]

    layout = go.Layout(
        title=image_name,
        autosize=False,
        width=1000,
        height=500,
        margin=dict(
            l=65,
            r=50,
            b=65,
            t=90
        )
    )
    fig = go.Figure(data=data, layout=layout)

    plot_filename = os.path.join(plots_path, "plot_" + image_name.rstrip(".")) + ".html"
    plot(fig, filename=plot_filename, auto_open=False)

    pd.DataFrame(image).to_excel(excel_writer=excel_writer, sheet_name=image_name)

excel_writer.save()

print("Script finished!")
