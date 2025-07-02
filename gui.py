import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import seaborn as sns
from logic import (
    initialize_system, recommend_crops, crop_details, estimate_resources,
    get_yield_stats, plot_yield_by_crop, plot_yield_by_region, plot_crop_region_matrix,
    analyze_market, plot_market_prices, get_soil_fertility, plot_soil_fertility_distribution,
    get_weather, plot_weather_trends, get_irrigation_method, get_storage_advice, save_user_data
)
class AgriSmartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AgriSmart: Smart Farming Assistant")
        self.root.geometry("1000x700")

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TNotebook', tabposition='n')
        self.style.configure('TNotebook.Tab', padding=[20, 10], font=('Arial', 11, 'bold'))
        self.style.configure("TFrame", background="#f0f7f4")

        initialize_system()
        self.create_tabs()

    def create_tabs(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True)

        self.recommend_tab = ttk.Frame(notebook)
        self.graphs_tab = ttk.Frame(notebook)
        self.market_tab = ttk.Frame(notebook)
        self.soil_tab = ttk.Frame(notebook)
        self.fertilizer_tab = ttk.Frame(notebook)

        notebook.add(self.recommend_tab, text='Crop Recommendation')
        notebook.add(self.graphs_tab, text='Yield & Weather Graphs')
        notebook.add(self.market_tab, text='Market Analysis')
        notebook.add(self.soil_tab, text='Soil Info')
        notebook.add(self.fertilizer_tab, text='Fertilizer & Irrigation')

        self.setup_recommend_tab()
        self.setup_graph_tab()
        self.setup_market_tab()
        self.setup_soil_tab()
        self.setup_fertilizer_tab()

    def setup_recommend_tab(self):
        frame = ttk.LabelFrame(self.recommend_tab, text="Input Parameters")
        frame.pack(pady=20, padx=20, fill="x")

        labels = ["Soil", "temp", "Season", "Duration", "Water Requirement"]
        self.inputs = {}

        for i, lbl in enumerate(labels):
            ttk.Label(frame, text=lbl+":").grid(row=i, column=0, sticky='e')
            entry = ttk.Entry(frame)
            entry.grid(row=i, column=1)
            self.inputs[lbl] = entry

        ttk.Button(frame, text="Recommend Crops", command=self.get_recommendations).grid(row=5, column=0, columnspan=2, pady=10)

        self.recommend_output = tk.Listbox(self.recommend_tab, height=10)
        self.recommend_output.pack(pady=10, padx=20, fill="both")
        self.recommend_output.bind("<<ListboxSelect>>", self.show_crop_info)

    def get_recommendations(self):
        params = {k.lower().replace(" ", "_"): v.get() or None for k, v in self.inputs.items()}
        if params['temp']: params['temp'] = float(params['temp'])
        crops = recommend_crops(**params)

        self.recommend_output.delete(0, tk.END)
        if crops:
            for crop in crops:
                self.recommend_output.insert(tk.END, crop)
        else:
            messagebox.showinfo("No Matches", "No crops matched your criteria.")

    def show_crop_info(self, event):
        sel = event.widget.curselection()
        if sel:
            crop = event.widget.get(sel[0])
            info = crop_details(crop)
            fert = estimate_resources(crop, 1)
            text = f"Crop: {crop}\nSoil: {info[2]}\nTemp: {info[3]}-{info[4]}°C\nWater: {info[5]}\nSeason: {info[6]}\nDuration: {info[7]} days\n\nFertilizer: {fert['fertilizer']} ({fert['total_fertilizer']}kg/ha)\nIrrigation: {fert['irrigation_method']}"
            messagebox.showinfo("Crop Details", text)

    def setup_graph_tab(self):
        graph_frame = ttk.Frame(self.graphs_tab)
        graph_frame.pack(pady=20)

        ttk.Button(graph_frame, text="Yield by Crop", command=self.display_yield_by_crop).pack(side="left", padx=5)
        ttk.Button(graph_frame, text="Yield by Region", command=self.display_yield_by_region).pack(side="left", padx=5)
        ttk.Button(graph_frame, text="Weather Trend", command=self.display_weather).pack(side="left", padx=5)

        self.canvas_frame = ttk.Frame(self.graphs_tab)
        self.canvas_frame.pack(fill="both", expand=True)

    def clear_canvas(self):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

    def embed_plot(self, fig):
        self.clear_canvas()
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def display_yield_by_crop(self):
        df = get_yield_stats()
        if df.empty: return
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=df, x="year", y="yield_per_hectare", hue="crop_name", ax=ax)
        ax.set_title("Yield by Crop")
        self.embed_plot(fig)

    def display_yield_by_region(self):
        df = get_yield_stats()
        if df.empty: return
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=df, x="year", y="yield_per_hectare", hue="region", ax=ax)
        ax.set_title("Yield by Region")
        self.embed_plot(fig)

    def display_weather(self):
        region = tk.simpledialog.askstring("Region Input", "Enter region:")
        if not region: return
        df = get_weather(region=region)
        if df.empty: return
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.lineplot(data=df, x="month", y="avg_temp", label="Temp", ax=ax)
        sns.lineplot(data=df, x="month", y="rainfall_mm", label="Rainfall", ax=ax)
        ax.set_title(f"Weather Trend in {region}")
        ax.legend()
        self.embed_plot(fig)

    def setup_market_tab(self):
        ttk.Button(self.market_tab, text="Show Market Prices", command=self.show_prices).pack(pady=10)
        self.market_output = tk.Text(self.market_tab, height=20)
        self.market_output.pack(fill="both", expand=True)

    def show_prices(self):
        df = analyze_market()
        self.market_output.delete("1.0", tk.END)
        self.market_output.insert(tk.END, df.to_string(index=False))

    def setup_soil_tab(self):
        ttk.Button(self.soil_tab, text="Show Soil Fertility", command=self.show_soil).pack(pady=10)
        self.soil_output = tk.Text(self.soil_tab, height=20)
        self.soil_output.pack(fill="both", expand=True)

    def show_soil(self):
        df = get_soil_fertility()
        self.soil_output.delete("1.0", tk.END)
        self.soil_output.insert(tk.END, df.to_string(index=False))

    def setup_fertilizer_tab(self):
        frame = ttk.LabelFrame(self.fertilizer_tab, text="Get Fertilizer & Irrigation Info")
        frame.pack(padx=20, pady=20)

        ttk.Label(frame, text="Crop Name:").grid(row=0, column=0)
        self.fert_crop_entry = ttk.Entry(frame)
        self.fert_crop_entry.grid(row=0, column=1)

        ttk.Label(frame, text="Land Area (ha):").grid(row=1, column=0)
        self.area_entry = ttk.Entry(frame)
        self.area_entry.grid(row=1, column=1)

        ttk.Button(frame, text="Get Info", command=self.get_fertilizer_irrigation).grid(row=2, column=0, columnspan=2, pady=10)

    def get_fertilizer_irrigation(self):
        crop = self.fert_crop_entry.get()
        try:
            area = float(self.area_entry.get())
        except ValueError:
            messagebox.showerror("Invalid", "Please enter valid land area")
            return
        info = estimate_resources(crop, area)
        text = f"Fertilizer: {info['fertilizer']} ({info['total_fertilizer']}kg)\nIrrigation: {info['irrigation_method']}"
        messagebox.showinfo("Fertilizer & Irrigation Info", text)


if __name__ == "__main__":
    root = tk.Tk()
    app = AgriSmartApp(root)
    root.mainloop()
