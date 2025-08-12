"""A Class in object orientated programming adhering to analyze molecular propperties"""

"""Importing modules needed for functions"""
import tkinter as tk # Need to build GUI
from tkinter import filedialog, ttk # filedialog needed to read in .csv, tkk enables creating a notebook/tab window
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk # FigureCanvasTkAgg supplies backend, NavigationToolbar2Tk Inserts toolbar
from matplotlib.figure import Figure # Generate Figure Object for tkinter window
import pandas as pd # General df handling
import seaborn as sns # Use to plot figures, DA/ML friendly

"""Defining MolecularAnalyzer Class with Attributes and Methods"""
class MolecularAnalyzer:
    """Class to analyze molecular properties, filter for adherence to defined rules (Lipinski and potentially others), and dynamically plotting"""
    def __init__(self, root):
        """Initialises the App, generating variables needed in the GUI/plot rendering process, starting 'build_gui()' function"""
        self.root = root    #starts tkinter window
        self.root.title("Oral availability filter")

        # Empty variables for plotting in GUI
        self.data = None
        self.empty_data = pd.DataFrame({'alogp': [],
                                        'full_mwt': []})
        self.empty_data2 = pd.DataFrame({'Rule': [],
                                         'Count': [],
                                         'Rule of Adherence': []})

        # List to append filtered scatter object after filtering for rendering the scatterplot
        self.scatter_objects = []

        # Rule columns for filtering in barchart
        self.rule_columns = ['Rule_mwt',
                             'Rule_alogp',
                             'Rule_hba',
                             'Rule_hbd']

        # Control variables (linked to checkboxes in GUI), for dynamic filtering
        self.var_mwt = tk.BooleanVar()
        self.var_clogP = tk.BooleanVar()
        self.var_hba = tk.BooleanVar()
        self.var_hbd = tk.BooleanVar()
        self.var_drug = tk.BooleanVar()

        # Build GUI
        self.build_gui()

    def build_gui(self):
        """Initialises the GUI containing a Notebook with multiple tabs, each tab is build modular afterwards"""
        # GUI layout: notebook with two tabs for now
        self.notebook = ttk.Notebook(self.root) # Initialise Notebook widget with multiple tabs
        self.notebook.grid(row=0, column=0, sticky='nswe')

        self.tab1 = tk.Frame(self.notebook) # Initialise Tab frame
        self.tab2 = tk.Frame(self.notebook)
        self.notebook.add(self.tab1, text='Scatter Plot')   # Append tabs to notebook and name them
        self.notebook.add(self.tab2, text='Bar Chart')

        self.root.rowconfigure(0, weight=1) # Make window expandable
        self.root.columnconfigure(0, weight=1)

        self.build_tab1() # Build tab modular
        self.build_tab2()

    def build_tab1(self):
        """Modul for tab1, builds the whole tab with widgets and wired functions"""
        # Filter controls frame
        f1 = tk.Frame(self.tab1)    # Initialise a frame to adhere buttons (and the plot?) to
        f1.grid(row=0, column=0, sticky='nswe')

        # Buttons and checkboxes
        b1 = tk.Button(f1, text='Choose file', command=self.askfile) # Load data
        b1.grid(row=0, sticky='we')

        b2 = tk.Checkbutton(f1, text='Rule "Molecular Weight"', variable=self.var_mwt, anchor='w', command=self.update_plot) # Toggle filter
        b2.grid(row=1, sticky='we')

        b3 = tk.Checkbutton(f1, text='Rule "clogP"', variable=self.var_clogP, anchor='w', command=self.update_plot)
        b3.grid(row=2, sticky='we')

        b4 = tk.Checkbutton(f1, text='Rule "Hydrogen Bond Acceptors"', variable=self.var_hba, anchor='w', command=self.update_plot)
        b4.grid(row=3, sticky='we')

        b5 = tk.Checkbutton(f1, text='Rule "Hydrogen Bond Donors"', variable=self.var_hbd, anchor='w', command=self.update_plot)
        b5.grid(row=4, sticky='we')

        b6 = tk.Checkbutton(f1, text='Show drugs', variable=self.var_drug, anchor='w', command=self.update_plot)  # checkbutton
        b6.grid(row=5, sticky="we")

        b7 = tk.Button(f1, text='Save selection', command=self.savefile) # Saves data
        b7.grid(row=7, sticky='we')

        # Placeholder figure
        self.fig1 = Figure(figsize=(10, 6)) # Initialise figure
        self.ax1 = self.fig1.add_subplot(111) # Common practice adds a single subplot in the figure, could add more later

        sns.set_theme(style="white") # Set theme
        sns.scatterplot(data=self.empty_data, # Set plot, data and which values are used on the axes
                        x='alogp',
                        y='full_mwt',
                        ax=self.ax1)

        self.ax1.set(xlabel='Predicted logP (AlogP)', # Name plot elements
                     ylabel='Molecular Weight (MW) in Da',
                     title='Estimating Drug-Likeness Based on Oral Availability\nAccording to the "Lipinski Rules of Five"')

        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.tab1) # Embedding Canvas with tinker
        self.canvas1.draw()
        self.canvas1.get_tk_widget().grid(row=0, column=1, sticky="nswe") # add canvas to the layout

        self.toolbar_frame1 = tk.Frame(self.tab1) # Adds toolbar , linking it to canvas, placing it into toolbar frame
        self.toolbar_frame1.grid(row=1, column=1, sticky='we')
        self.toolbar1 = NavigationToolbar2Tk(self.canvas1, self.toolbar_frame1)
        self.toolbar1.update()

    def build_tab2(self):
        """Modul for tab2, builds the whole tab with widgets and wired functions"""
        # Placeholder bar chart in tab 2
        self.fig2 = Figure(figsize=(12, 6))
        self.ax2 = self.fig2.add_subplot(111)

        #Plot
        sns.set_theme(style="white")
        sns.barplot(data=self.empty_data2,
                    x='Rule',
                    y='Count',
                    hue='Rule of Adherence',
                    ax=self.ax2)

        #Labels and title
        self.ax2.set(xlabel='Lipinski Rule',
                     ylabel='Number of Molecules',
                     title='Adherence to Lipinski Rules')

        #layout adjustments
        self.fig2.tight_layout() # Spans the whole window

        #Embedding canvas in tkinter
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.tab2)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().grid(row=0, column=1, sticky="nswe")

        # Adding toolbar
        self.toolbar_frame2 = tk.Frame(self.tab2)
        self.toolbar_frame2.grid(row=1, column=1, sticky='we')
        self.toolbar2 = NavigationToolbar2Tk(self.canvas2, self.toolbar_frame2)
        self.toolbar2.update()

    def askfile(self):
        """Enables User to choose a CSV for analysis, updates variable 'data', runs functions 'update_plot' and 'lipinskibarchart to display read in data, generates 'summary_df' need for plot in tab2"""
        # Open a file dialog to select a CSV file
        selected_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")]) # Prompts User to select file

        if selected_file:
            try:
                self.data = pd.read_csv(selected_file) # Reads in data
                print("Data loaded successfully!")
                self.update_plot()  #Updates scatterplot to display current data
                summary_df = self.summarize_rule_overlap() # Generates a df need for barchart in tab2
                self.lipinskibarchart(summary_df) # Displays barchart in tab2

            except Exception as e:
                print(f"Error loading file: {e}") # Error if data is faulty

    def get_active_filters(self):
        """Enables dynamic filtering of data, 'selection' need for plotting selected data points"""
        selection = pd.Series([True] * len(self.data)) # All data is True for the length of the whole df

        if self.var_mwt.get(): # Toggled boolean returns False if filter applied in the plot
            selection &= self.data['Rule_mwt'] # &= "And" operator on the selection series and rule column, keeps rows that are True
        if self.var_clogP.get():
            selection &= self.data['Rule_alogp']
        if self.var_hba.get():
            selection &= self.data['Rule_hba']
        if self.var_hbd.get():
            selection &= self.data['Rule_hbd']

        return selection # Returns data for other functions to use

    def savefile(self):
        """Save filtered selection of data as CSV"""
        # Get active selection using active filter
        selection = self.get_active_filters()

        # Get the filtered data based on the active filters
        filtered_data = self.data[selection]

        # Open Save File Dialog to choose saving spot
        filename = filedialog.asksaveasfilename(initialdir='/',
                                                title='Save as: ',
                                                defaultextension=".csv",  # neat addition I found
                                                filetypes=(('CSV files', '*.csv'), ('All files', "*.*")))
        # Save file
        filtered_data.to_csv(filename, index=False)

    def plot_bright_drug_split(self, df):
        """Splits data selection into 'is drug'/'no drug' to highlight actual drug if selected, plots both selection ontop of each other"""
        drug = df[df['is_drug']] # df['is_drug'] gives booleans df[df['is_drug']] returns just True statements
        no_drug = df[~df['is_drug']] # ~ inverst boolean -> is False

        # Rendering scatter plots for 'is drug'/'no drug' on top of each other / same axis
        self.scatter_objects.append(sns.scatterplot(
            x=drug['alogp'],
            y=drug['full_mwt'],
            color='red',
            edgecolor='w',
            linewidth=0.5,
            s=40,
            ax=self.ax1,
            label='Is drug'
        ))

        self.scatter_objects.append(sns.scatterplot(
            x=no_drug['alogp'],
            y=no_drug['full_mwt'],
            color='#1f77b4',
            edgecolor='w',
            linewidth=0.5,
            s=40,
            ax=self.ax1,
            label='Selected'
        ))

    def plot_bright_all(self, df):
        """Plots selected data in a scatterplot with bright coloring"""
        self.scatter_objects.append(sns.scatterplot(
            x=df['alogp'],
            y=df['full_mwt'],
            color='#1f77b4',
            edgecolor='w',
            linewidth=0.5,
            s=40,
            ax=self.ax1,
            label='Selected'
        ))

    def plot_faded(self, df):
        """Plots data that is not selected by user in a scatter plot wit muted color"""
        self.scatter_objects.append(sns.scatterplot(
            x=df['alogp'],
            y=df['full_mwt'],
            color='gray',
            edgecolor='w',
            linewidth=0.5,
            s=40,
            alpha=0.2,
            ax=self.ax1,
            label='Filtered out'
        ))

    def format_plot(self):
        """Formats the scatter plot again, if update_plot() is called it wipes previous settings"""
        self.ax1.set_xlabel('Predicted logP (AlogP)')
        self.ax1.set_ylabel('Molecular Weight (MW) in Da')
        self.ax1.set_title('Estimating Drug-Likeness Based on Oral Availability\nAccording to the "Lipinski Rules of Five"')
        self.ax1.legend() # Updated legend depending on filter status

    def update_plot(self):
        """Updates scatter plot with User input (loading new data or toggling check buttons)"""
        if self.data is None:
            print("No data loaded.")
            return

        # Cleanup of previous plot
        self.ax1.cla()  # Clear previous plot
        self.scatter_objects = [] # resets variable to clean up

        selection = self.get_active_filters() # gets current filters

        # Slices data into selections
        bright_points = self.data[selection]
        faded_points = self.data[~selection]

        if self.var_drug.get():
            self.plot_bright_drug_split(bright_points) # Check if 'is drug' filter was used
        else:
            self.plot_bright_all(bright_points)

        self.plot_faded(faded_points)
        self.format_plot()

        self.canvas1.draw() # Updating GUI

    def summarize_rule_overlap(self):
        """Calculates the cumulative adherence of a given molecule to the set of rules per rule"""
        summary = []

        # For each rule: "If a molecule passes this rule, how many other rules does it also pass?"
        for rule in self.rule_columns: # Defined a class variable
            other_rules = [r for r in self.rule_columns if r != rule] #for rule that are not this rule

            # Only consider molecules that pass the current rule
            subset = self.data[self.data[rule]].copy()  # Selects molecules that adhere to the current rule
                                                        # .copy() is like [:], prevents editing original df

            # Count how many other rules each of these molecules pass
            subset['num_other_passed'] = subset[other_rules].sum(axis=1) # gives a df without current rule
                                                                        # axis = 1 counts how many are True

            # Count how many pass at least  1, 2, 3 other rules
            counts = {
                'Rule': rule.replace('Rule_', '').upper(), # removes 'Rule'
                '>=1_other': (subset['num_other_passed'] >= 1).astype(int).sum(),
                '>=2_other': (subset['num_other_passed'] >= 2).astype(int).sum(),
                '>=3_other': (subset['num_other_passed'] >= 3).astype(int).sum(),
            }

            summary.append(counts)

        return pd.DataFrame(summary) # Converts data into df for outside access

    def lipinskibarchart(self, summary_df):
        # Clear previous plot
        self.ax2.cla()

        # Reshape the summary DataFrame due to nesting into long format
        rule_summary_melted = summary_df.melt(
            id_vars="Rule",
            value_vars=['>=1_other', '>=2_other', '>=3_other'],
            var_name="Rule Adherence",
            value_name="Count"
        )

        # Rebuild the bar chart
        sns.barplot(
            x='Rule',
            y='Count',
            hue='Rule Adherence',
            data=rule_summary_melted,
            ax=self.ax2
        )

        # Set the axes
        self.ax2.set_xlabel('Lipinski Rule')
        self.ax2.set_ylabel('Number of Molecules')
        self.ax2.set_title('Adherence to Lipinski Rules')

        # Extend plot in window
        self.fig2.tight_layout()

        # Redraw GUI
        self.canvas2.draw()

if __name__ == "__main__": # Do this if function(Class is imported into other scripts
    root = tk.Tk()  # Initialise the main tk window
    app = MolecularAnalyzer(root) # Creates an instance of the Class
    root.mainloop() # starts event loop - keeps GUI running until its closed