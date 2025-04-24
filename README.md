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

This study examined the voltage response of a photodiode to glucose concentrations at various wavelengths. The results showed different sensitivities across the tested wavelengths, which are critical for optimizing the system's ability to detect glucose effectively.

- 940 nm: This wavelength exhibits minimal absorption by glucose, resulting in very small voltage fluctuations, typically maintaining a steady output around 5 uV with less than 0.01 uV of change. Due to these negligible voltage changes, 940 nm is best used as a reference channel rather than for detecting glucose levels.

- 1550 nm and 1610 nm: These wavelengths demonstrated the most pronounced response to glucose concentration changes, making them the most effective for glucose detection. The voltage response was significantly influenced by glucose concentration, and both linear and polynomial regression models showed a good fit to the data, particularly for higher glucose concentrations.

- 1410 nm: While 1410 nm exhibits high absorption from water, it can still serve as a reference wavelength. The high water absorption at this wavelength affects glucose detection, but it can be useful for compensating for variations in water content in biological samples. Using 1410 nm as a reference allows the system to correct for water interference, improving the accuracy of glucose measurements at other wavelengths.

## Improvements for Future Work

1. Enhancing the Use of 1410 nm as a Reference:

- Although 1410 nm is not ideal for glucose detection due to high water absorption, its ability to capture water content changes makes it a valuable reference wavelength. By using 1410 nm alongside other glucose-sensitive wavelengths like 1550 nm and 1610 nm, the system can account for water variation and improve the overall glucose detection accuracy.

2. Utilizing a Multi-Wavelength Approach:

- To improve the robustness and precision of the system, a multi-wavelength sensing system should be implemented. Using 940 nm as a stable reference wavelength, 1410 nm for water content correction, and 1550 nm or 1610 nm for glucose-specific measurements could help isolate glucose signals from water interference and other confounding factors, enhancing the overall accuracy.

3. Exploring Additional Glucose-Sensitive Wavelengths:

- Future work should explore other wavelengths that offer a higher glucose absorption rate while minimizing the influence of water. Identifying optimal wavelengths for glucose-specific detection will refine the system and improve its performance.

4. Refining Calibration Techniques:

- Advanced calibration methods that utilize 1410 nm to compensate for water content variations will improve the system's ability to accurately measure glucose levels. Implementing a better calibration approach will help in correcting for the interference from water absorption, making the system more reliable across a range of glucose concentrations.

In conclusion, by combining 1410 nm for water content correction with glucose-sensitive wavelengths like 1550 nm and 1610 nm, and using 940 nm as a reference, a more accurate and reliable multi-wavelength glucose detection system can be developed. Future improvements focusing on refining calibration and selecting the optimal wavelengths will significantly enhance the performance of the system.

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
