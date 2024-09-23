import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from config import ConfigManager
from converter import Converter

class MP3ToMP4App:
    def __init__(self, root):
        self.root = root
        self.root.title("Convertidor MP3 a MP4")
        self.config_manager = ConfigManager()
        self.converter = Converter(self.config_manager)
        self.config = self.config_manager.get_config()

        self.setup_gui()

    def setup_gui(self):
        self.root.configure(bg='#2e2e2e')  # Fondo oscuro
        self.root.geometry("800x600")  # Tamaño por defecto más grande

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background='#2e2e2e', foreground='white')
        style.configure("TFrame", background='#2e2e2e')
        style.configure("TLabel", background='#2e2e2e', foreground='white')
        style.configure("TButton", background='#2e2e2e', foreground='white')
        style.configure("TEntry", fieldbackground='#3e3e3e', foreground='white')

        notebook = ttk.Notebook(self.root)
        notebook.pack(pady=10, expand=True)

        # Pestaña Conversión
        frame_conversion = ttk.Frame(notebook)
        notebook.add(frame_conversion, text="Conversión")

        label = ttk.Label(frame_conversion, text="Selecciona tus archivos MP3")
        label.pack(pady=10)

        button_seleccionar_archivos = ttk.Button(frame_conversion, text="Seleccionar archivos MP3", command=self.seleccionar_archivos)
        button_seleccionar_archivos.pack(pady=20)

        button_abrir_ruta = ttk.Button(frame_conversion, text="Abrir ruta de salida", command=self.abrir_ruta_salida)
        button_abrir_ruta.pack(pady=20)

        # Pestaña Configuración
        frame_configuracion = ttk.Frame(notebook)
        notebook.add(frame_configuracion, text="Configuración")

        label_width = ttk.Label(frame_configuracion, text="Ancho del video por defecto:")
        label_width.pack(pady=5)
        self.entry_width = ttk.Entry(frame_configuracion)
        self.entry_width.pack(pady=5)
        self.entry_width.insert(0, self.config.get("width", 1920))

        label_height = ttk.Label(frame_configuracion, text="Alto del video por defecto:")
        label_height.pack(pady=5)
        self.entry_height = ttk.Entry(frame_configuracion)
        self.entry_height.pack(pady=5)
        self.entry_height.insert(0, self.config.get("height", 1080))

        label_default_image = ttk.Label(frame_configuracion, text="Imagen predeterminada:")
        label_default_image.pack(pady=5)
        self.entry_default_image = ttk.Entry(frame_configuracion)
        self.entry_default_image.pack(pady=5)
        self.entry_default_image.insert(0, self.config.get("default_image", ""))

        label_output_path = ttk.Label(frame_configuracion, text="Ruta de salida fija:")
        label_output_path.pack(pady=5)
        self.entry_output_path = ttk.Entry(frame_configuracion)
        self.entry_output_path.pack(pady=5)
        self.entry_output_path.insert(0, self.config.get("output_path", ""))

        button_seleccionar_imagen = ttk.Button(frame_configuracion, text="Seleccionar imagen predeterminada", command=self.seleccionar_imagen_predeterminada)
        button_seleccionar_imagen.pack(pady=5)

        button_seleccionar_ruta = ttk.Button(frame_configuracion, text="Seleccionar ruta de salida fija", command=self.seleccionar_ruta_salida)
        button_seleccionar_ruta.pack(pady=5)

        button_guardar_config = ttk.Button(frame_configuracion, text="Guardar configuración", command=self.guardar_configuracion_general)
        button_guardar_config.pack(pady=20)

    def seleccionar_archivos(self):
        mp3_paths = filedialog.askopenfilenames(filetypes=[("MP3 files", "*.mp3")])
        if mp3_paths:
            output_path = self.config["output_path"]
            if output_path:
                self.mostrar_progreso(mp3_paths, output_path)
            else:
                messagebox.showerror("Error", "La ruta de salida no está establecida. Por favor, configúrela en la pestaña de Configuración.")

    def mostrar_progreso(self, mp3_paths, output_path):
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Progreso de Conversión")
        progress_window.geometry("400x100")
        progress_window.configure(bg='#2e2e2e')

        progress_label = ttk.Label(progress_window, text="Convirtiendo archivos...", background='#2e2e2e', foreground='white')
        progress_label.pack(pady=10)

        progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=300, mode="determinate")
        progress_bar.pack(pady=20)

        def actualizar_progreso():
            for i, mp3_path in enumerate(mp3_paths):
                try:
                    self.converter.convertir_mp3_a_mp4([mp3_path], output_path)
                    progress_bar['value'] = (i + 1) / len(mp3_paths) * 100
                    progress_window.update_idletasks()
                except Exception as e:
                    messagebox.showerror("Error", f"Error al convertir el archivo {mp3_path}: {e}")
            progress_window.destroy()
            messagebox.showinfo("Conversión completa", "Todos los archivos se han convertido exitosamente.")

        self.root.after(100, actualizar_progreso)

    def seleccionar_ruta_salida(self):
        output_path = filedialog.askdirectory()
        if output_path:
            self.entry_output_path.delete(0, tk.END)
            self.entry_output_path.insert(0, output_path)
            self.config["output_path"] = output_path
            self.config_manager.guardar_configuracion()
            messagebox.showinfo("Ruta de salida", f"Ruta de salida fija establecida: {output_path}")

    def abrir_ruta_salida(self):
        output_path = self.config["output_path"]
        if output_path and os.path.exists(output_path):
            os.startfile(output_path)  # Para Windows
        else:
            messagebox.showerror("Error", "La ruta de salida no está establecida o no existe.")

    def guardar_configuracion_general(self):
        try:
            self.config["width"] = int(self.entry_width.get())
            self.config["height"] = int(self.entry_height.get())
            self.config["default_image"] = self.entry_default_image.get()
            self.config["output_path"] = self.entry_output_path.get()
            self.config_manager.guardar_configuracion()
            messagebox.showinfo("Configuración", "Configuración guardada con éxito.")
        except ValueError:
            messagebox.showerror("Error", "El ancho y alto deben ser valores numéricos.")

    def seleccionar_imagen_predeterminada(self):
        image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if image_path:
            self.entry_default_image.delete(0, tk.END)
            self.entry_default_image.insert(0, image_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = MP3ToMP4App(root)
    root.mainloop()
