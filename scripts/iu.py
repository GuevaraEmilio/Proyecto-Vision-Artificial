import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import subprocess
import sys
import os

class ClasificadorBiomas:
    def __init__(self, root):
        self.root = root
        self.root.title("Clasificador de Biomas")
        
        # Configurar pantalla completa
        self.root.attributes('-fullscreen', True)
        self.root.bind('<Escape>', lambda e: self.root.attributes('-fullscreen', False))
        self.root.bind('<F11>', lambda e: self.root.attributes('-fullscreen', True))
        
        # Color de fondo moderno (gris muy claro)
        self.root.configure(bg='#f5f5f5')
        
        # Título con diseño minimalista
        titulo = tk.Label(
            root, 
            text="Clasificador de Biomas",
            font=('Helvetica', 28, 'bold'),
            bg='#f5f5f5',
            fg='#2c3e50',
            pady=30
        )
        titulo.pack()
        
        # Frame principal con más espacio
        main_frame = tk.Frame(root, bg='#f5f5f5')
        main_frame.pack(expand=True, fill='both', padx=80, pady=30)
        
        # Frame superior (botón circular + imagen)
        top_frame = tk.Frame(main_frame, bg='#f5f5f5')
        top_frame.pack(expand=True, fill='both')
        
        # Frame izquierdo para el botón circular
        left_frame = tk.Frame(top_frame, bg='#f5f5f5')
        left_frame.pack(side='left', padx=40, expand=False)
        
        # Canvas para botón circular con sombra
        canvas_size = 100
        self.canvas_btn = tk.Canvas(
            left_frame,
            width=canvas_size + 10,
            height=canvas_size + 10,
            bg='#f5f5f5',
            highlightthickness=0
        )
        self.canvas_btn.pack(pady=80)
        
        # Sombra del círculo (efecto de profundidad)
        self.canvas_btn.create_oval(
            7, 7, 
            canvas_size + 3, canvas_size + 3,
            fill='#d0d0d0',
            outline=''
        )
        
        # Círculo principal con gradiente simulado
        self.circulo = self.canvas_btn.create_oval(
            5, 5, 
            canvas_size, canvas_size,
            fill='#3498db',
            outline='#2980b9',
            width=2
        )
        
        # Texto del botón
        self.canvas_btn.create_text(
            canvas_size // 2 + 2, canvas_size // 2 + 2,
            text="📁",
            font=('Arial', 32),
            fill='white'
        )
        
        # Texto debajo del botón
        tk.Label(
            left_frame,
            text="Cargar\nImagen",
            font=('Helvetica', 11),
            bg='#f5f5f5',
            fg='#7f8c8d'
        ).pack()
        
        # Hacer el canvas clickeable
        self.canvas_btn.bind('<Button-1>', lambda e: self.cargar_imagen())
        self.canvas_btn.bind('<Enter>', self.on_enter_circular)
        self.canvas_btn.bind('<Leave>', self.on_leave_circular)
        self.canvas_btn.configure(cursor='hand2')
        
        # Frame para la imagen central con bordes redondeados simulados
        image_container = tk.Frame(top_frame, bg='#f5f5f5')
        image_container.pack(side='left', expand=True, fill='both', padx=30)
        
        # Borde con sombra
        shadow_frame = tk.Frame(
            image_container,
            bg='#e0e0e0',
            relief='flat'
        )
        shadow_frame.pack(expand=True, fill='both', padx=3, pady=3)
        
        self.imagen_frame = tk.Frame(
            shadow_frame,
            bg='white',
            relief='flat',
            bd=0
        )
        self.imagen_frame.pack(expand=True, fill='both', padx=2, pady=2)
        
        # Label para mostrar la imagen
        self.imagen_label = tk.Label(
            self.imagen_frame,
            text="Selecciona una imagen\npara clasificar el bioma",
            font=('Helvetica', 14),
            bg='white',
            fg='#95a5a6'
        )
        self.imagen_label.pack(expand=True)
        
        # Frame inferior para botones rectangulares
        bottom_frame = tk.Frame(main_frame, bg='#f5f5f5')
        bottom_frame.pack(pady=40)
        
        # Botones rectangulares con diseño moderno
        btn_frame = tk.Frame(bottom_frame, bg='#f5f5f5')
        btn_frame.pack()
        
        # Botón Clasificar con diseño plano
        self.btn_clasificar = tk.Button(
            btn_frame,
            text="CLASIFICAR",
            font=('Helvetica', 12, 'bold'),
            width=18,
            height=2,
            bg='#27ae60',
            fg='white',
            relief='flat',
            bd=0,
            cursor='hand2',
            activebackground='#229954',
            activeforeground='white',
            command=self.clasificar
        )
        self.btn_clasificar.pack(side='left', padx=15)
        self.btn_clasificar.bind('<Enter>', lambda e: self.btn_clasificar.config(bg='#229954'))
        self.btn_clasificar.bind('<Leave>', lambda e: self.btn_clasificar.config(bg='#27ae60'))
        
        self.btn_limpiar = tk.Button(
            btn_frame,
            text="LIMPIAR",
            font=('Helvetica', 12, 'bold'),
            width=18,
            height=2,
            bg='#e74c3c',
            fg='white',
            relief='flat',
            bd=0,
            cursor='hand2',
            activebackground='#c0392b',
            activeforeground='white',
            command=self.limpiar
        )
        self.btn_limpiar.pack(side='left', padx=15)
        self.btn_limpiar.bind('<Enter>', lambda e: self.btn_limpiar.config(bg='#c0392b'))
        self.btn_limpiar.bind('<Leave>', lambda e: self.btn_limpiar.config(bg='#e74c3c'))
        
        # Variables para almacenar la imagen y ruta
        self.imagen_actual = None
        self.ruta_imagen = None
        
        # Ruta al script de predicción (ajustar si está en otra carpeta)
        self.script_prediccion = 'predict_biomas2.py'
    
    def on_enter_circular(self, event):
        """Efecto hover - entrar"""
        self.canvas_btn.itemconfig(self.circulo, fill='#5dade2')
    
    def on_leave_circular(self, event):
        """Efecto hover - salir"""
        self.canvas_btn.itemconfig(self.circulo, fill='#3498db')
        
    def cargar_imagen(self):
        """Cargar una imagen desde el sistema de archivos"""
        archivo = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[
                ("Archivos de imagen", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if archivo:
            try:
                # Guardar la ruta del archivo
                self.ruta_imagen = archivo
                
                # Cargar y redimensionar la imagen para visualización
                img = Image.open(archivo)
                
                # Obtener dimensiones del frame
                frame_width = self.imagen_frame.winfo_width()
                frame_height = self.imagen_frame.winfo_height()
                
                # Si el frame aún no tiene dimensiones, usar valores por defecto
                if frame_width <= 1:
                    frame_width = 900
                if frame_height <= 1:
                    frame_height = 550
                
                # Redimensionar manteniendo aspecto
                img.thumbnail((frame_width - 40, frame_height - 40), Image.Resampling.LANCZOS)
                
                # Convertir para tkinter
                self.imagen_actual = ImageTk.PhotoImage(img)
                
                # Mostrar imagen
                self.imagen_label.configure(image=self.imagen_actual, text="")
                self.imagen_label.image = self.imagen_actual
                
                print(f"Imagen cargada: {archivo}")
                
            except Exception as e:
                self.imagen_label.configure(
                    text=f"Error al cargar imagen:\n{str(e)}",
                    image=""
                )
                self.ruta_imagen = None
    
    def clasificar(self):
        """Clasificar la imagen cargada usando predict_biomas.py"""
        if not self.imagen_actual or not self.ruta_imagen:
            # Mensaje si no hay imagen cargada
            mensaje = tk.Toplevel(self.root)
            mensaje.title("Aviso")
            mensaje.geometry("350x150")
            mensaje.configure(bg='white')
            mensaje.resizable(False, False)
            
            # Centrar ventana
            mensaje.transient(self.root)
            mensaje.grab_set()
            
            tk.Label(
                mensaje,
                text="⚠",
                font=('Arial', 32),
                bg='white',
                fg='#f39c12'
            ).pack(pady=15)
            
            tk.Label(
                mensaje,
                text="Por favor, carga una imagen primero",
                font=('Helvetica', 12),
                bg='white',
                fg='#2c3e50'
            ).pack(pady=10)
            
            tk.Button(
                mensaje,
                text="ENTENDIDO",
                command=mensaje.destroy,
                bg='#3498db',
                fg='white',
                font=('Helvetica', 10, 'bold'),
                relief='flat',
                bd=0,
                cursor='hand2',
                width=15
            ).pack(pady=15)
            return
        
        # Verificar que existe el script de predicción
        if not os.path.exists(self.script_prediccion):
            messagebox.showerror(
                "Error",
                f"No se encontró el archivo '{self.script_prediccion}'.\n"
                f"Asegúrate de que esté en la misma carpeta o especifica la ruta correcta."
            )
            return
        
        try:
            # Llamar al script de predicción como proceso separado
            print(f"Ejecutando: python {self.script_prediccion} {self.ruta_imagen}")
            
            resultado = subprocess.run(
                [sys.executable, self.script_prediccion, self.ruta_imagen],
                capture_output=True,
                text=True,
                timeout=30  # timeout de 30 segundos
            )
            
            # Verificar si hubo error
            if resultado.returncode != 0:
                error_msg = resultado.stderr if resultado.stderr else "Error desconocido"
                messagebox.showerror(
                    "Error en clasificación",
                    f"El script de predicción falló:\n{error_msg}"
                )
                print(f"STDERR: {resultado.stderr}")
                return
            
            # Obtener el bioma predicho (viene en stdout)
            bioma_predicho = resultado.stdout.strip()
            
            # Mostrar información de debug
            print(f"STDOUT: {resultado.stdout}")
            print(f"STDERR: {resultado.stderr}")
            print(f"Bioma predicho: {bioma_predicho}")
            
            # Ventana de resultado con diseño moderno
            resultado_ventana = tk.Toplevel(self.root)
            resultado_ventana.title("Resultado de Clasificación")
            resultado_ventana.geometry("400x200")
            resultado_ventana.configure(bg='white')
            resultado_ventana.resizable(False, False)
            
            # Centrar ventana
            resultado_ventana.transient(self.root)
            resultado_ventana.grab_set()
            
            tk.Label(
                resultado_ventana,
                text="✓ Clasificación completada",
                font=('Helvetica', 16, 'bold'),
                bg='white',
                fg='#27ae60'
            ).pack(pady=25)
            
            tk.Label(
                resultado_ventana,
                text="Bioma detectado:",
                font=('Helvetica', 11),
                bg='white',
                fg='#7f8c8d'
            ).pack()
            
            tk.Label(
                resultado_ventana,
                text=bioma_predicho,
                font=('Helvetica', 18, 'bold'),
                bg='white',
                fg='#2c3e50'
            ).pack(pady=10)
            
            tk.Button(
                resultado_ventana,
                text="CERRAR",
                command=resultado_ventana.destroy,
                bg='#3498db',
                fg='white',
                font=('Helvetica', 11, 'bold'),
                relief='flat',
                bd=0,
                cursor='hand2',
                width=15,
                height=2
            ).pack(pady=20)
            
        except subprocess.TimeoutExpired:
            messagebox.showerror(
                "Error",
                "La clasificación tardó demasiado tiempo y se canceló."
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al ejecutar la clasificación:\n{str(e)}"
            )
            print(f"Error detallado: {e}")
    
    def limpiar(self):
        """Limpiar la imagen actual"""
        self.imagen_actual = None
        self.ruta_imagen = None
        self.imagen_label.configure(
            image="",
            text="Selecciona una imagen\npara clasificar el bioma"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = ClasificadorBiomas(root)
    root.mainloop()