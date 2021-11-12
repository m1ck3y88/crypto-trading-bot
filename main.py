import tkinter as tk
import logging

from coinbasepro_products import get_products


logger = logging.getLogger()

logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler('info.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


if __name__ == '__main__':

    coinbase_products = get_products()

    root = tk.Tk()
    root.configure(bg='gray12')

    i = 0
    j = 0

    calibri_font = ("Calibri", 11, "normal")

    for product in coinbase_products:
        label_widget = tk.Label(root, text=product, bg='gray12', fg='SteelBlue1', width=13)
        label_widget.grid(row=i, column=j, sticky='ew')

        if i == 4:
            j += 1
            i = 0
        else:
            i += 1

    root.mainloop()
