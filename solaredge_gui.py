#!/usr/bin/env python3
import pprint
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

from solaredge.api import SolaredgeClient
from utilities import get_env, get_logger


class SolarEdgeGUI(tk.Tk):
    """Manage and display SolarEdge monitoring data in a graphical interface.

    This class coordinates fetching data from the SolarEdge API and presenting
    it to the user through the GUI components.

    """

    def __init__(self):
        super().__init__()
        self.title("SolarEdge API Data Viewer")
        self.geometry("800x600")
        self.api_client = None
        self.create_widgets()

    def create_widgets(self):
        # API Key Entry
        tk.Label(self, text="API Key:").pack(pady=5)
        self.api_key_entry = tk.Entry(self, width=50)
        self.api_key_entry.pack(pady=5)
        env = get_env()
        if 'solaredge_apikey' in env:
            self.api_key_entry.insert(20, str(env.get('solaredge_apikey')))

        # Data Type Selection
        tk.Label(self, text="Select Data Type:").pack(pady=5)
        self.data_types = [
            "site_list", "inverter_list", "get_sites", "get_site_details", "get_data_period",
            "get_site_overview", "get_energy", "get_energy_details", "get_power", "get_power_details",
            "get_power_flow", "get_storage", "get_site_components", "get_site_inventory",
            "get_inverters", "get_env_benefits", "get_inverter_telemetry"
        ]
        self.data_type_var = tk.StringVar(value=self.data_types[0])
        self.data_type_menu = ttk.Combobox(
            self, textvariable=self.data_type_var, values=self.data_types, state="readonly")
        self.data_type_menu.pack(pady=5)

        # Site ID Entry (for methods that require it)
        tk.Label(self, text="Site ID (if required):").pack(pady=5)
        self.site_id_entry = tk.Entry(self, width=20)
        self.site_id_entry.pack(pady=5)

        # Inverter ID Entry (for methods that require it)
        tk.Label(self, text="Inverter ID (if required):").pack(pady=5)
        self.inverter_id_entry = tk.Entry(self, width=20)
        self.inverter_id_entry.pack(pady=5)

        # Fetch Button
        self.fetch_button = tk.Button(
            self, text="Fetch Data", command=self.fetch_data)
        self.fetch_button.pack(pady=10)

        # Results Display
        self.result_text = scrolledtext.ScrolledText(
            self, wrap=tk.WORD, width=100, height=25)
        self.result_text.pack(pady=10, fill=tk.BOTH, expand=True)

    def fetch_data(self):
        api_key = self.api_key_entry.get().strip()
        if not api_key:
            messagebox.showerror("Error", "API Key is required.")
            return
        if not self.api_client:
            self.api_client = SolaredgeClient(api_key)
            self.site_id_entry.insert(
                10, str(self.api_client.site_list[0]) if self.api_client.site_list else "")
            self.inverter_id_entry.insert(
                10, self.api_client.inverter_list[0] if self.api_client.inverter_list else "")
        data_type = self.data_type_var.get()
        site_id = self.site_id_entry.get().strip()
        try:
            method = self.api_client.__getattribute__(data_type)
            if isinstance(method, list):
                result = method
            else:
                if "site_id" in method.__code__.co_varnames:
                    if not site_id:
                        messagebox.showerror(
                            "Error", "Site ID is required for this data type.")
                        return
                    result = method(int(site_id))
                else:
                    result = method()
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, pprint.pformat(result, width=120))
        except Exception as e:
            messagebox.showerror("API Error", str(e))


if __name__ == "__main__":
    app = SolarEdgeGUI()
    app.mainloop()
