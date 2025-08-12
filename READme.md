# Molecular Analyzer - Oral Availability Tool

## About
Molecular Analyzer is a graphical Python tool to visually explore and filter molecular datasets for oral drug-likeness, based on Lipinski’s Rule of Five.
It uses *tkinter* for the GUI and *seaborn/matplotlib* for dynamic plotting. 
Users can interactively filter molecules, highlight known drugs, view rule adherence statistics, and export filtered datasets.

This project was created as the **final project for a Python 101 course**.
It is under MIT license (see 'License.md').
As a beginner’s project, please be kind to its limitations and functionality. 

## Project Overview
This project is split into modular scripts and a GUI application

Script				Purpose
01_data_download.py		Download example dataset from the ChEMBL website via API
02_data_wrangling.py		Clean and prepare data for analysis
03_data_model.py		Contains the *MolecularAnalyzer* class
molecular_analyzer_app.py	Same as Script 03, but import-safe for use as module
04_run_gui.py			Runs actual GUI using the data model
chembl_data_tidy.csv		Sample data from the ChEMBL databank with Lipinski-rule columns

## 01_data_download.py
- Uses ChEMBL’s API and pandas to download molecule data.
- Data is fetched in batches to avoid memory issues and data loss.
- A timestamp is attached to the output to track download time.
- Output: A raw .csv file for further processing.

## 02_data_wrangling
- Performs light data cleaning.
- Since the download script already excludes most missing values, minimal cleaning is needed.
- Renames nested column names for clarity.
- Adds boolean Lipinski rule columns:
    Rule_mwt, Rule_alogp, Rule_hba, Rule_hbd, and is_drug
- Output saved as chembl_data_tidy.csv.

## 03_data_model.py
Defines the full 'MolecularAnalyzer' GUI class.
Features:
- Load .csv files
- Interactive scatterplot with rule filters
- Highlight actual drugs using the is_drug column
- Export filtered data
- Generate Lipinski adherence summary bar chart

## molecular_analyzer_app.py
- A renamed version of Script 03 (without leading number) to allow: 'from molecular_analyzer_app import MolecularAnalyzer'.
- This makes it importable in 04_run_gui.py.

## 04_run_gui.py
- Simple launcher to run the app.

## chembl_data_tidy.csv	
- Sample data file to use with the GUI.
Future datasets should include following columns:
'alogp, full_mwt, Rule_mwt, Rule_alogp, Rule_hba, Rule_hbd, is_drug'.
Each rule column is a boolean (True/False) indicating whether a molecule passes the respective Lipinski rule.



