#!/usr/bin/env python3
"""Call the Solaredge API and print the results."""

import pprint
import tkinter
from tkinter import ttk

from solaredge.api import SolaredgeClient
from utilities import get_env, get_logger



def main() -> None:
    
    logger = get_logger(destination="stdout") # noqa
    env = get_env()

    with SolaredgeClient(apikey=env.get('solaredge_apikey')) as client:
        for site in client.get_sites():
            
            root = tkinter.Tk(className="SolarEdge")
            
            frm = ttk.Frame(root, padding=10)
            frm.master.title("Solaredge Title")
            frm.grid()
            ttk.Label(frm, text=pprint.pformat(site)).grid(column=0, row=0)
            ttk.Button(frm, text="Update", command=root.destroy).grid(column=1, row=0)            
            ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=1)
            root.mainloop()


if __name__ == "__main__":
    main()