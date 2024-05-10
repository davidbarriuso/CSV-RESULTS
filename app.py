from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and file.filename.endswith('.txt'):
            df = pd.read_csv(file, sep=';', parse_dates=True)
            img = create_plot(df)
            return render_template('plot.html', plot_url=img)
    return render_template('upload.html')

def create_plot(df):
    plt.figure()
    df.plot(kind='line')
    plt.title('Visualización de Datos')
    plt.xlabel('Índice')
    plt.ylabel('Valores')
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches="tight")
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()
    return plot_url

if __name__ == '__main__':
    app.run(debug=True)
