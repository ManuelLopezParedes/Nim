import tkinter as tk
from tkinter import messagebox
from ia import JugadorIA
from logica import Logica

class Interfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Nim")
        self.root.geometry("600x500")
        
        # Variables del juego
        self.palitos = 0
        self.palitos_max = 0
        self.modo = 1  # 1: JvsJ, 2: JvsCPU
        self.dificultad = "facil"
        self.turno_j1 = True
        self.ia = None
        
        self.crear_menu_inicial()
    
    def crear_menu_inicial(self):
        """Crea la interfaz del menú inicial"""
        self.limpiar_ventana()
        
        # Título
        titulo = tk.Label(self.root, text="JUEGO DE NIM", font=("Arial", 20, "bold"))
        titulo.pack(pady=20)
        
        # Frame para configuración
        frame_config = tk.Frame(self.root)
        frame_config.pack(pady=20)
        
        # Configuración de los controles
        self.crear_controles_configuracion(frame_config)
        
        # Botón para iniciar juego
        btn_iniciar = tk.Button(self.root, text="Iniciar Juego", font=("Arial", 14, "bold"), 
                               bg="green", fg="white", command=self.iniciar_juego)
        btn_iniciar.pack(pady=20)
    
    def crear_controles_configuracion(self, parent):
        """Crea los controles de configuración del juego"""
        # Número de palitos
        tk.Label(parent, text="Número de palitos:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        self.entry_palitos = tk.Entry(parent, font=("Arial", 12), width=10)
        self.entry_palitos.grid(row=0, column=1, pady=5, padx=10)
        self.entry_palitos.insert(0, "15")
        
        # Máximo de palitos por turno
        tk.Label(parent, text="Máximo a retirar por turno:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        self.entry_max = tk.Entry(parent, font=("Arial", 12), width=10)
        self.entry_max.grid(row=1, column=1, pady=5, padx=10)
        self.entry_max.insert(0, "3")
        
        # Modo de juego
        tk.Label(parent, text="Modo de juego:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
        self.modo_var = tk.IntVar(value=1)
        tk.Radiobutton(parent, text="Jugador vs Jugador", variable=self.modo_var, value=1, 
                      font=("Arial", 10)).grid(row=2, column=1, sticky="w", pady=2)
        tk.Radiobutton(parent, text="Jugador vs CPU", variable=self.modo_var, value=2, 
                      font=("Arial", 10)).grid(row=3, column=1, sticky="w", pady=2)
        
        # Dificultad
        self.crear_controles_dificultad(parent)
    
    def crear_controles_dificultad(self, parent):
        """Crea los controles de dificultad"""
        tk.Label(parent, text="Dificultad de la IA:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", pady=5)
        self.dificultad_var = tk.StringVar(value="facil")
        dificultad_frame = tk.Frame(parent)
        dificultad_frame.grid(row=4, column=1, sticky="w", pady=5)
        tk.Radiobutton(dificultad_frame, text="Fácil", variable=self.dificultad_var, value="facil", 
                      font=("Arial", 10)).pack(side=tk.LEFT)
        tk.Radiobutton(dificultad_frame, text="Difícil", variable=self.dificultad_var, value="dificil", 
                      font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
    
    def iniciar_juego(self):
        """Inicia el juego con la configuración seleccionada"""
        try:
            self.palitos = int(self.entry_palitos.get())
            self.palitos_max = int(self.entry_max.get())
            self.modo = self.modo_var.get()
            self.dificultad = self.dificultad_var.get()
            
            if self.palitos <= 0 or self.palitos_max <= 0:
                messagebox.showerror("Error", "Los valores deben ser mayores a 0")
                return
            
            if self.modo == 2:
                self.ia = JugadorIA(estrategia=self.dificultad)
            
            self.turno_j1 = True
            self.crear_interfaz_juego()
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa números válidos")
    
    def crear_interfaz_juego(self):
        """Crea la interfaz principal del juego"""
        self.limpiar_ventana()
        
        # Frame superior con información
        self.crear_frame_informacion()
        
        # Visualización de palitos
        self.crear_visualizacion_palitos()
        
        # Controles de juego
        self.crear_controles_juego()
        
        # Botón para reiniciar
        self.crear_boton_reiniciar()
        
        self.dibujar_palitos()
    
    def crear_frame_informacion(self):
        """Crea el frame con información del juego"""
        frame_info = tk.Frame(self.root, bg="lightgray", height=80)
        frame_info.pack(fill=tk.X, pady=5)
        frame_info.pack_propagate(False)
        
        self.label_info = tk.Label(frame_info, text=f"Palitos restantes: {self.palitos}", 
                                  font=("Arial", 14, "bold"), bg="lightgray")
        self.label_info.pack(pady=10)
        
        self.label_turno = tk.Label(frame_info, 
                                  text=f"Turno: {Logica.get_current_player(self.turno_j1, self.modo)}", 
                                  font=("Arial", 12), bg="lightgray")
        self.label_turno.pack()
    
    def crear_visualizacion_palitos(self):
        """Crea el canvas para visualizar los palitos"""
        frame_palitos = tk.Frame(self.root)
        frame_palitos.pack(pady=20)
        self.canvas_palitos = tk.Canvas(frame_palitos, width=400, height=100, bg="white")
        self.canvas_palitos.pack()
    
    def crear_controles_juego(self):
        """Crea los controles para realizar jugadas"""
        frame_controles = tk.Frame(self.root)
        frame_controles.pack(pady=20)
        
        if self.es_turno_jugador():
            self.crear_botones_jugada(frame_controles)
        else:
            self.crear_mensaje_turno_ia(frame_controles)
    
    def crear_botones_jugada(self, parent):
        """Crea los botones para las jugadas posibles"""
        tk.Label(parent, text="Selecciona cuántos palitos quitar:", 
                font=("Arial", 12)).pack()
        
        frame_botones = tk.Frame(parent)
        frame_botones.pack(pady=10)
        
        max_jugada = min(self.palitos, self.palitos_max)
        for i in range(1, max_jugada + 1):
            btn = tk.Button(frame_botones, text=str(i), font=("Arial", 12), width=4,
                           command=lambda x=i: self.realizar_jugada(x))
            btn.pack(side=tk.LEFT, padx=5)
    
    def crear_mensaje_turno_ia(self, parent):
        """Crea el mensaje para el turno de la IA"""
        tk.Label(parent, text="Es el turno de la IA...", 
                font=("Arial", 12)).pack()
        self.root.after(1000, self.turno_ia)
    
    def crear_boton_reiniciar(self):
        """Crea el botón para reiniciar el juego"""
        btn_reiniciar = tk.Button(self.root, text="Reiniciar Juego", font=("Arial", 12),
                                 command=self.crear_menu_inicial)
        btn_reiniciar.pack(pady=10)
    
    def es_turno_jugador(self):
        """Determina si es el turno de un jugador humano"""
        if self.modo == 1:  # JvsJ - ambos son humanos
            return True
        else:  # JvsCPU - solo J1 es humano
            return self.turno_j1
    
    def dibujar_palitos(self):
        """Dibuja los palitos en el canvas"""
        self.canvas_palitos.delete("all")
        
        if self.palitos == 0:
            self.canvas_palitos.create_text(200, 50, text="¡JUEGO TERMINADO!", 
                                          font=("Arial", 16, "bold"), fill="red")
            return
        
        # Dibujar palitos como líneas verticales
        palitos_por_fila = 10
        espacio = 30
        
        for i in range(self.palitos):
            fila = i // palitos_por_fila
            columna = i % palitos_por_fila
            x = 50 + columna * espacio
            y = 20 + fila * 40
            
            self.canvas_palitos.create_line(x, y, x, y + 30, width=3, fill="brown")
            self.canvas_palitos.create_oval(x-2, y+28, x+2, y+32, fill="green")
    
    def realizar_jugada(self, cantidad):
        """Realiza una jugada y actualiza el juego"""
        if not Logica.es_jugada_valida(cantidad, self.palitos, self.palitos_max):
            messagebox.showerror("Error", "Jugada inválida")
            return
        
        self.palitos -= cantidad
        
        # Actualizar interfaz
        self.label_info.config(text=f"Palitos restantes: {self.palitos}")
        self.dibujar_palitos()
        
        # Verificar si el juego terminó
        if Logica.es_juego_terminado(self.palitos):
            self.mostrar_ganador()
            return
        
        # Cambiar turno y continuar
        self.turno_j1 = not self.turno_j1
        self.label_turno.config(text=f"Turno: {Logica.get_current_player(self.turno_j1, self.modo)}")
        self.crear_interfaz_juego()
    
    def turno_ia(self):
        """Maneja el turno de la IA"""
        if not self.ia or self.turno_j1:
            return
        
        cantidad = self.ia.decidir_jugada(self.palitos, self.palitos_max)
        
        messagebox.showinfo("Jugada de la IA", f"La IA quitó {cantidad} palito(s)")
        self.realizar_jugada(cantidad)
    
    def mostrar_ganador(self):
        """Muestra el mensaje del ganador"""
        ganador = Logica.obtener_ganador(self.turno_j1, self.modo)
        
        mensaje = f"¡{ganador} es el ganador!\n\nEl jugador que tomó el último palito pierde."
        messagebox.showinfo("¡Juego Terminado!", mensaje)
        
        if messagebox.askyesno("Juego Terminado", "¿Quieres jugar otra vez?"):
            self.crear_menu_inicial()
    
    def limpiar_ventana(self):
        """Limpia todos los widgets de la ventana"""
        for widget in self.root.winfo_children():
            widget.destroy()