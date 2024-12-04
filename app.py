import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from datetime import datetime

from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# Define the directory where the Excel files will be stored
directory = "/mnt/data/excel_files"
if not os.path.exists(directory):
    os.makedirs(directory)  # Create the directory if it doesn't exist

# Define function to get the Excel file path based on the current date
def get_excel_file_path():
    today = datetime.now().strftime('%Y-%m-%d')  # Get today's date in YYYY-MM-DD format
    return os.path.join(directory, f"team_data_{today}.xlsx")

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get data from the form
        date = request.form['date']
        name = request.form['name']
        outlet = request.form['outlet']
        comments = request.form['comments']

        # Create a DataFrame for the new data
        new_data = pd.DataFrame([{
            'Date': date,
            'Name': name,
            'Outlet': outlet,
            'Comments': comments
        }])

        # Get the Excel file path for the current day
        file_path = get_excel_file_path()

        # If the file exists, read it and append the new data, otherwise create a new file
        if os.path.exists(file_path):
            df = pd.read_excel(file_path)
            df = pd.concat([df, new_data], ignore_index=True)
        else:
            df = new_data

        # Save the updated data to the Excel file
        df.to_excel(file_path, index=False)

        # Redirect to the home page after submission
        return redirect(url_for('home'))

    # Render the form if it's a GET request
    return render_template('team_form.html')

@app.route('/manager', methods=['GET'])
def manager():
    # Get the list of all files in the directory
    files = [f for f in os.listdir(directory) if f.endswith('.xlsx')]

    # Render the manager page with the list of files
    return render_template('manager_dashboard.html', files=files)

@app.route('/download/<filename>')
def download(filename):
    # Send the Excel file to the manager for download
    return send_from_directory(directory, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

