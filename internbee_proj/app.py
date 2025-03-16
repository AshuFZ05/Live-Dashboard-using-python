from flask import Flask, render_template, request
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def process_csv(file_path):
    df = pd.read_csv(file_path)
    return df

def generate_plots(df):
    plot_paths = []
    numeric_columns = df.select_dtypes(include=['number']).columns
    if len(numeric_columns) >= 2:
        plt.figure(figsize=(6, 4))
        sns.histplot(df[numeric_columns[1]], kde=True, bins=20, color='#007bff')
        plt.xlabel("Values", fontsize=12, color='#333')
        plt.ylabel("Frequency", fontsize=12, color='#333')
        plt.title("Histogram of {}".format(numeric_columns[1]), fontsize=14, color='#007bff')
        plt.grid(True, linestyle='--', alpha=0.6)
        plot_path = os.path.join("static", "histogram.png")
        plt.savefig(plot_path, bbox_inches='tight', dpi=100)
        plt.close()
        plot_paths.append("histogram.png")
        
        plt.figure(figsize=(6, 4))
        sns.barplot(x=df[numeric_columns[0]], y=df[numeric_columns[1]], palette="viridis")
        plt.xlabel(numeric_columns[0], fontsize=12)
        plt.ylabel(numeric_columns[1], fontsize=12)
        plt.title("Bar Plot of {} vs {}".format(numeric_columns[0], numeric_columns[1]), fontsize=14)
        plot_path = os.path.join("static", "barplot.png")
        plt.savefig(plot_path, bbox_inches='tight', dpi=100)
        plt.close()
        plot_paths.append("barplot.png")
        
        plt.figure(figsize=(6, 4))
        sns.boxplot(y=df[numeric_columns[1]], color='skyblue')
        plt.title("Box Plot of {}".format(numeric_columns[1]), fontsize=14)
        plot_path = os.path.join("static", "boxplot.png")
        plt.savefig(plot_path, bbox_inches='tight', dpi=100)
        plt.close()
        plot_paths.append("boxplot.png")
    
    return plot_paths

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        df = process_csv(file_path)
        plot_filenames = generate_plots(df)
        return render_template('dashboard.html', tables=[df.to_html(classes='table table-hover table-bordered text-center')], plot_filenames=plot_filenames)
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)