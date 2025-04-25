import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score

# Directory where the files are stored
directory_path = './test_data/150K/'


# List all Excel files in the directory, excluding temporary files (those starting with ~$)
excel_files = [f for f in os.listdir(directory_path) if f.endswith('.xlsx') and not f.startswith('~$')]

# Log number of files to be processed
print(f"Found {len(excel_files)} Excel files to process.")

# Initialize an empty list to store DataFrames
all_data = []

# Loop through each file and load the data
for file in excel_files:
    file_path = os.path.join(directory_path, file)

    print(f"\nProcessing file: {file_path}")

    try:
        # Specify the engine (openpyxl is recommended for modern .xlsx files)
        df = pd.read_excel(file_path, engine='openpyxl')

        # Add a new column with the concentration information inferred from the file name
        concentration = file.split('_')[1].replace('g', '')  # Extract concentration and remove 'g', file format like "1Mohm_40g_1.xlsx"
        df['Concentration'] = concentration

        # Check first few rows to verify data
        print(f"First few rows of {file}:")
        for wavelength in df['Wavelength'].unique():
            print(f"\nWavelength: {wavelength} nm")
            print(df[df['Wavelength'] == wavelength].head(10))  # Print first 10 rows for each wavelength

        # Ensure that numeric columns are properly converted (e.g., Voltage_uV, Concentration)
        df['Voltage_uV'] = pd.to_numeric(df['Voltage_uV'], errors='coerce')  # Convert Voltage_uV to numeric
        df['Concentration'] = pd.to_numeric(df['Concentration'], errors='coerce')  # Convert Concentration to numeric

        # Log missing values count before cleaning
        missing_values = df[['Concentration', 'Wavelength', 'Voltage_uV']].isnull().sum()
        print(f"Missing values in {file}:")
        print(missing_values)

        # Check if there are missing values in the essential columns
        if df.isnull().sum().any():
            print(f"Warning: {file} contains missing values, which will be removed.")

        all_data.append(df)

    except Exception as e:
        print(f"Error reading {file}: {e}")

# Combine all the data into a single DataFrame
data = pd.concat(all_data, ignore_index=True)

# Check if data is loaded successfully
print(f"Loaded {len(data)} rows of data from all files.")

# Check missing values in the relevant columns before cleaning
missing_values = data[['Concentration', 'Wavelength', 'Voltage_uV']].isnull().sum()
print(f"Missing values before cleaning:")
print(missing_values)

# Clean the data, ensuring there are no missing values in the necessary columns
data_clean = data[['Concentration', 'Wavelength', 'Voltage_uV']].dropna()

# Log the number of clean data points
print(f"\nCleaned data contains {len(data_clean)} rows after removing missing values.")

# If no data is left after cleaning, log the issue and exit
if len(data_clean) == 0:
    print("Error: No valid data left after cleaning.")
    exit()

# Perform Regression Analysis (Linear and Polynomial):

def perform_linear_regression(x, y):
    # Reshape x to be a 2D array for sklearn
    x_reshaped = x.reshape(-1, 1)

    # Create the linear regression model
    model = LinearRegression()
    model.fit(x_reshaped, y)

    # Make predictions
    y_pred = model.predict(x_reshaped)

    # Compute R² score
    r2 = r2_score(y, y_pred)

    return model, y_pred, r2

def perform_polynomial_regression(x, y, degree=2):
    # Reshape x to be a 2D array for sklearn
    x_reshaped = x.reshape(-1, 1)

    # Create polynomial features
    poly = PolynomialFeatures(degree)
    x_poly = poly.fit_transform(x_reshaped)

    # Create the polynomial regression model
    model = LinearRegression()
    model.fit(x_poly, y)

    # Make predictions
    y_pred = model.predict(x_poly)

    # Compute R² score
    r2 = r2_score(y, y_pred)

    return model, y_pred, r2


# Function to remove the highest value and return the next N values

def get_cleaned_average_of_top_n_values(voltage_values):
    first_n=150 # 10*10*3/2

    # Sort the voltage values in descending order
    sorted_values = np.sort(voltage_values)[::-1]

    # Take only the first 150 values (if they exist)
    sorted_values = sorted_values[:first_n]

    # Calculate the IQR (Interquartile Range) to identify outliers
    Q1 = np.percentile(sorted_values, 25)  # 25th percentile (Q1)
    Q3 = np.percentile(sorted_values, 75)  # 75th percentile (Q3)
    IQR = Q3 - Q1  # Interquartile range

    # Define lower and upper bounds for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Remove outliers: values outside the IQR bounds
    cleaned_values = [v for v in sorted_values if lower_bound <= v <= upper_bound]

    # Log the outliers
    outliers = [v for v in sorted_values if v < lower_bound or v > upper_bound]
    print(f"Outliers removed: {outliers}")

    # Log the top N values
    print(f"All values after removing outliers:")
    print(cleaned_values)
    print(f"Number of values left after removing outliers: {len(cleaned_values)}")

    # Return the average of these top N values
    return np.mean(cleaned_values)


# Fit Models for Each Concentration and Wavelength:

# Unique concentrations in the dataset
concentrations = data_clean['Concentration'].unique()

# Log the unique concentrations
print(f"Unique concentrations found: {concentrations}")

# Unique wavelengths in the dataset
wavelengths = data_clean['Wavelength'].unique()

# Log the unique wavelengths
print(f"Unique wavelengths found: {wavelengths}")



# Function to perform regression and plot the results for each wavelength and concentration
def process_wavelength_and_regression(wavelength_data, concentrations, wavelength):
    try:
        # Prepare lists for regression (x = concentration, y = average voltage)
        x = []
        y = []

        for concentration in concentrations:
            concentration_data = wavelength_data[wavelength_data['Concentration'] == concentration]

            # Log the length of the voltage data for the current concentration and wavelength
            voltage_length = len(concentration_data['Voltage_uV'].values)
            print(f"\nLength of voltage data for Concentration: {concentration}mg/mL, Wavelength: {wavelength} nm: {voltage_length}")


            average_voltage = get_cleaned_average_of_top_n_values(concentration_data['Voltage_uV'].values)
            print(f"Average Voltage (after removing outliers): {average_voltage:.2f} uV")

            # Add concentration and the average voltage for this concentration
            x.append(concentration)
            y.append(average_voltage)

            print(f"Top N average voltage for Concentration: {concentration}mg/mL, Wavelength: {wavelength} nm: {average_voltage:.2f} uV")

        # Now perform regression with the concentration as the feature (x) and the averaged voltage as the target (y)
        x = np.array(x)  # Concentrations (independent variable)
        y = np.array(y)  # Average Voltage (dependent variable)

        # Log the regression data
        print(f"\nRegression data for Wavelength: {wavelength} nm")
        print(f"x (Concentration): {x}")
        print(f"y (Average Voltage): {y}")

        # Perform Linear Regression
        linear_model, linear_predictions, r2_linear = perform_linear_regression(x, y)

        # Perform Polynomial Regression (degree 2 as an example)
        poly = PolynomialFeatures(degree=2)
        x_poly = poly.fit_transform(x.reshape(-1, 1))  # Apply the polynomial transformation
        poly_model = LinearRegression()
        poly_model.fit(x_poly, y)

        # Generate smooth line for the polynomial fit by using np.linspace to generate continuous x values
        x_smooth = np.linspace(x.min(), x.max(), 500)
        x_smooth_poly = poly.transform(x_smooth.reshape(-1, 1))  # Apply the polynomial transformation to smooth x values
        poly_smooth = poly_model.predict(x_smooth_poly)

        # Calculate R² for polynomial fit
        r2_poly = r2_score(y, poly_model.predict(x_poly))

        # Plotting the results
        plt.figure(figsize=(10, 6))
        plt.scatter(x, y, color='black', label='Data')
        plt.plot(x, linear_predictions, label=f'Linear Fit (R² = {r2_linear:.2f})', color='blue')
        plt.plot(x_smooth, poly_smooth, label=f'Polynomial Fit (R² = {r2_poly:.2f})', color='red')
        plt.xlabel('Concentration (mg/dL)')
        plt.ylabel('Average Voltage (uV)')
        plt.title(f'Voltage vs Concentration for Wavelength: {wavelength} nm')
        plt.legend()
        # Save the plot with a filename based on the wavelength
        filename = f"150K_{wavelength}nm.png"
        plt.savefig(filename)
        plt.close()  # Close the plot to avoid hanging on large datasets

        print(f'Linear R²: {r2_linear:.3f}')
        print(f'Polynomial R²: {r2_poly:.3f}')
    except Exception as e:
        print(f"Error processing Wavelength {wavelength} nm: {e}")
        # Move to next wavelength if an error occurs

# Loop through each wavelength (940 nm, 1410 nm, 1550 nm, 1610 nm) and concentration
for wavelength in data_clean['Wavelength'].unique():
    print(f"\nProcessing for Wavelength: {wavelength} nm")

    # Filter the data for the current wavelength
    wavelength_data = data_clean[data_clean['Wavelength'] == wavelength]

    # Process regression and plotting for this wavelength
    process_wavelength_and_regression(wavelength_data, concentrations, wavelength)

