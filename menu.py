import tkinter as tk
import tkinter.colorchooser as cc


def run_simulation(final_color, N, K):
    print(f"{final_color}, {N}, {K}")


class Menu:
    final_color = None
    color_button = None

    def get_color(self):
        self.final_color = cc.askcolor()[1]

    def select_colors(self):
        self.color_button.config(state=tk.NORMAL)

    def stop_simulation(self):
        pass

    def run(self):
        root = tk.Tk()
        root.title("Genetic Color Match")
        root.geometry("500x500")

        # Create a frame for the input boxes
        input_frame = tk.Frame(root, padx=10, pady=10)
        input_frame.pack()

        self.color_button = tk.Button(input_frame, text="Choose Target Color", command=self.get_color,
                                      state=tk.DISABLED)
        self.color_button.pack(pady=20)
        self.color_button.config(state=tk.NORMAL)

        # Create the input labels and entry boxes
        label1 = tk.Label(input_frame, text="N")
        label1.pack(side="left")

        N = tk.Entry(input_frame, width=10)
        N.pack(side="left", padx=5)
        N.insert(12, "12")

        label2 = tk.Label(input_frame, text="K")
        label2.pack(side="left")

        K = tk.Entry(input_frame, width=10)
        K.pack(side="left", padx=5)

        # Create the button to run the function
        button = tk.Button(root, text="Run Function",
                           command=lambda: run_simulation(self.final_color, int(N.get()), int(K.get())))
        button.pack(pady=10)

        stop_button = tk.Button(root, text="Stop Simulation", command=lambda: self.stop_simulation())
        stop_button.pack(pady=10)

        stop_button = tk.Button(root, text="Stop Program", command=root.destroy)
        stop_button.pack(pady=10)

        root.mainloop()
