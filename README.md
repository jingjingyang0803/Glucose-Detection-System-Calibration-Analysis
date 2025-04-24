# Glucose Detection System Calibration Analysis

## Overview

This repository contains code for analyzing the calibration data of a non-invasive glucose detection system. The system uses a photodiode and infrared (IR) LEDs across different wavelengths to measure glucose concentrations. The analysis focuses on modeling the relationship between photodiode voltage output and glucose concentration, performing regression analysis (both linear and polynomial), and evaluating the performance of the system across various wavelengths.

### Project Objectives:

- **Voltage Response Analysis**: Analyzing the photodiode voltage output in response to different glucose concentrations.
- **Calibration Curve Fitting**: Performing linear and polynomial regression to model the voltage-concentration relationship.
- **Wavelength Sensitivity Evaluation**: Assessing the sensitivity of different wavelengths (940 nm, 1450 nm, 1590 nm, 1600 nm) to glucose absorption.
- **System Calibration**: Part of the broader calibration of the glucose detection system to ensure accurate glucose measurements.

---

## Dataset Description

The dataset consists of voltage measurements from a photodiode exposed to varying concentrations of glucose. The concentrations range from **40g to 250g**, and the data was collected in three separate trials for each concentration level.

### File Naming Format:

The Excel files are named using the following format: `R_Xg_Y.xlsx`, where:

- `R` refers to the resistance used in the experiment.
- `Xg` indicates the glucose concentration in grams (e.g., `40g`, `55g`, `70g`, etc.).
- `Y` refers to the trial number (1, 2, or 3).

### Data Columns:

1. **Timestamp**: The time when the measurement was taken.
2. **Elapsed_Time_s**: The elapsed time in seconds during the measurement.
3. **Wavelength**: The wavelength of light used during the measurement (e.g., 940 nm, 1450 nm, 1590 nm, 1600 nm).
4. **Voltage_uV**: The voltage output of the photodiode in microvolts, which corresponds to the glucose concentration.
5. **Concentration (g)**: The glucose concentration in grams, which is the target variable for the analysis.

### File Structure:

- **Excel Files**: Each file contains data for a specific glucose concentration and wavelength. The files are organized by glucose concentration and trial number.
- **PNG Files**: Graphical outputs of the measurement sets corresponding to each Excel file.

---

## Python Methods

This analysis was performed using Python, utilizing several libraries for data manipulation, regression analysis, and visualization.

### Key Libraries:

- **pandas**: For data loading and manipulation.
- **numpy**: For numerical operations and calculations.
- **matplotlib**: For plotting graphs and visualizing data.
- **scikit-learn**: For performing linear and polynomial regression models.

### Analysis Workflow:

1. **Data Loading**:
   The Excel files corresponding to different glucose concentrations were loaded into a pandas DataFrame using `pandas.read_excel()`. Each file was processed individually and combined into a single DataFrame for further analysis.

2. **Regression Analysis**:
   Linear and polynomial regression models were applied to the data to fit the voltage-concentration relationship. Both models were evaluated for each wavelength to compare their performance in predicting glucose concentrations based on the voltage readings.

3. **Performance Evaluation**:
   The **R² score** was used to evaluate the goodness-of-fit for each regression model. A higher R² value indicates a better fit between the model and the data.

4. **Visualization**:
   The results of the regression models were visualized using **matplotlib** to display:
   - The raw data points for each concentration.
   - The linear regression line.
   - The polynomial regression curve.

## Results and Conclusions

### Voltage Response Trends:

The voltage output from the photodiode decreased as glucose concentration increased, which is consistent with the **Beer-Lambert Law**, where higher glucose concentrations reduce light transmittance. This behavior was observed across all wavelengths tested.

### Calibration Models:

Both **linear** and **polynomial regression** models were applied to the data. The polynomial model offered a slightly better fit at higher concentrations, demonstrating a more accurate representation of the data. However, the linear model performed sufficiently well for concentrations within the physiological range (70-180 mg/dL), making it a practical choice for implementation in the system.

### Wavelength Sensitivity:

- **1550 nm** and **1610 nm** wavelengths showed the most pronounced sensitivity to glucose concentration changes, making them ideal candidates for glucose detection.
- **940 nm** exhibited minimal voltage change, indicating its suitability as a reference channel that experiences low glucose interaction.

## Recommendations:

- **Use 1550 nm and 1610 nm wavelengths** for more accurate glucose measurements due to their high sensitivity to glucose absorption.
- **Linear models** are suitable for glucose concentrations within the physiological range (70–180 mg/dL). However, **polynomial models** should be considered for higher concentrations to achieve better accuracy.
- A **multi-wavelength approach**, combining reference and glucose-sensitive channels, should be used to improve the robustness of the system and reduce errors caused by external variables.

## How to Run the Analysis

### Install Dependencies:

To install the required libraries, use the following command:

```bash
pip install pandas numpy matplotlib scikit-learn openpyxl
```

### Run the Analysis:

- Clone or download the repository.

- Place the Excel files in the specified directory.

- Run the analysis script (analysis.py) or use Jupyter Notebook for an interactive experience.

### Adjust File Paths:

Ensure that the file paths are correctly set in the script to point to where your Excel files are stored.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
