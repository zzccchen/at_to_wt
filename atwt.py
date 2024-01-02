import tkinter as tk
from periodictable import elements

# Helper function to get atomic mass
def get_atomic_mass(symbol):
    for element in elements:
        if hasattr(element, 'symbol') and element.symbol == symbol:
            return element.mass
    return None

# Atomic percent to weight percent conversion
def at_to_wt(at_percents, atomic_masses):
    total_mass = sum(at_percents[i] * atomic_masses[i] for i in range(len(at_percents)))
    return [at_percents[i] * atomic_masses[i] / total_mass * 100 for i in range(len(at_percents))]

# Weight percent to atomic percent conversion
def wt_to_at(wt_percents, atomic_masses):
    total_moles = sum(wt_percents[i] / atomic_masses[i] for i in range(len(wt_percents)))
    return [wt_percents[i] / atomic_masses[i] / total_moles * 100 for i in range(len(wt_percents))]

# Create the main window
root = tk.Tk()
root.title("Element Weight and Atomic Percent Calculator")

# Variables to store symbols and entries
element_symbols = []
entries = {}

# Function to create input fields
def create_input_fields(symbols):
    for index, symbol in enumerate(symbols):
        if symbol not in entries:
            row = tk.Frame(root)
            
            row.grid(row=periodic_table_last_row + 2 + index, column=0, sticky="ew", padx=3, pady=3)
            root.grid_rowconfigure(periodic_table_last_row + 2 + index, weight=1)

            label = tk.Label(row, text=f"{symbol} (wt.%): ")
            entry = tk.Entry(row)
            entries[symbol] = entry
            
            label.grid(row=0, column=0, sticky="w", padx=3, pady=3)
            entry.grid(row=0, column=1, sticky="ew", padx=3, pady=3)
            row.grid_columnconfigure(1, weight=1)

# Function to handle element button click
def element_button_clicked(symbol):
    if symbol not in element_symbols:
        element_symbols.append(symbol)
    create_input_fields(element_symbols)

# Function to handle conversion
def convert_button_clicked():
    wt_percents = [float(entry.get()) for entry in entries.values()]
    symbols = list(entries.keys())
    atomic_masses = [get_atomic_mass(symbol) for symbol in symbols]
    
    at_percents = wt_to_at(wt_percents, atomic_masses)
    
    for i, symbol in enumerate(symbols):
        entries[symbol].delete(0, tk.END)
        entries[symbol].insert(0, str(at_percents[i]))

# Layout periodic table by rows
periodic_table_layout = [
    # The first two periods
    ["H", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, "He"],
    ["Li", "Be", None, None, None, None, None, None, None, None, None, None, None, "B", "C", "N", "O", "F", "Ne"],
    # The second two periods
    ["Na", "Mg", None, None, None, None, None, None, None, None, None, None, None, "Al", "Si", "P", "S", "Cl", "Ar"],
    ["K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr"],
    # The third two periods
    ["Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe"],
    ["Cs", "Ba", "La", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn"],
    # The lanthanides
    ["Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu"],
    # The actinides
    ["Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr"]
]

periodic_table_last_row = len(periodic_table_layout) + 2

# Define the uniform width of the button
button_width = 3

# Create GUI layout based on periodic table layout
for period, row_elements in enumerate(periodic_table_layout, start=1):
    frame = tk.Frame(root)
    frame.grid(row=period, column=0, sticky="ew", padx=1, pady=1)
    
    # Configure frame to expand with the window
    root.grid_rowconfigure(period, weight=1)
    root.grid_columnconfigure(0, weight=1)

    for col, symbol in enumerate(row_elements, start=1):
        frame.grid_columnconfigure(col, weight=1)
        if symbol:
            btn = tk.Button(frame, text=symbol, command=lambda s=symbol: element_button_clicked(s), width=button_width)
            btn.grid(row=0, column=col, sticky="ew", padx=1, pady=1)
        else:
            # For None placeholder, create an empty label for alignment
            label = tk.Label(frame, text="  ", width=button_width)
            label.grid(row=0, column=col, sticky="ew", padx=1, pady=1)

# # Create the GUI layout based on the periodic table layout
# for period, row_elements in enumerate(periodic_table_layout, start=1):
#     frame = tk.Frame(root)
#     frame.pack(side=tk.TOP, fill=tk.X, padx=3, pady=3)
#     for i, symbol in enumerate(row_elements, start=1):
#         if symbol:
#             btn = tk.Button(frame, text=symbol, command=lambda s=symbol: element_button_clicked(s), width=3)
#             btn.pack(side=tk.LEFT, padx=1, pady=1)
#         elif symbol == None:
#             # Create an empty space for alignment
#             label = tk.Label(frame, text="   ", width=3)
#             label.pack(side=tk.LEFT, padx=1, pady=1)

# # The lanthanides and actinides are typically shown separately beneath the main table
# lanthanides_frame = tk.Frame(root)
# lanthanides_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
# for symbol in periodic_table_layout[-2]:
#     btn = tk.Button(lanthanides_frame, text=symbol, command=lambda s=symbol: element_button_clicked(s))
#     btn.pack(side=tk.LEFT, padx=2, pady=2)

# actinides_frame = tk.Frame(root)
# actinides_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
# for symbol in periodic_table_layout[-1]:
#     btn = tk.Button(actinides_frame, text=symbol, command=lambda s=symbol: element_button_clicked(s))
#     btn.pack(side=tk.LEFT, padx=2, pady=2)

# Create the Reset button and corresponding click event handler function
def reset_button_clicked():
    # Clear the recorded element symbol list
    global entries, element_symbols
    for symbol in list(entries.keys()):
        # Get the Entry control from the entries dictionary
        entry_widget = entries[symbol]
        # Delete Entry control
        entry_widget.delete(0, tk.END)
        # Get the parent Frame of the Entry control
        parent_frame = entry_widget.master
        # Destroy the entire Frame and all its child controls
        parent_frame.destroy()
        # Remove the element from the entries dictionary
        del entries[symbol]

    element_symbols.clear()

# reset_button = tk.Button(root, text="Reset", command=reset_button_clicked)
# reset_button.grid(row=periodic_table_last_row, column=1,  sticky="ew", padx=1, pady=1)

# Create a new Frame for placing buttons
button_frame = tk.Frame(root)
button_frame.grid(row=periodic_table_last_row, column=0, sticky="ew", padx=1, pady=1)

# Configure the column weight of the button Frame so that the button can equally divide the space
button_frame.grid_columnconfigure(0, weight=2)
button_frame.grid_columnconfigure(1, weight=1)

# Create a convert button and put it into the button Frame
convert_button = tk.Button(button_frame, text="Convert", command=convert_button_clicked)
convert_button.grid(row=0, column=0, sticky="ew", padx=1, pady=1)

# Create a Reset button and put it into the button Frame
reset_button = tk.Button(button_frame, text="Reset", command=reset_button_clicked)
reset_button.grid(row=0, column=1, sticky="ew", padx=1, pady=1)

root.mainloop()