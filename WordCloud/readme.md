# WORD CLOUD


## Preparation

Install semua requirement

```python
    pip install -r ./requirements.txt
```

File image mask diganti dengan sesuai kebutuhan `(PENTING UNTUK BACKGROUND WARNA PUTIH)`
```python
    mask = np.array(Image.open('<source images mask>'))
```

File data untuk WordCloud diganti dengan sesuai kebutuhan
```python
    data_file = pd.read_csv('<source text wordcloud>')
```
## Run

untuk menjalankan script bisa di VENV atau di global
```python
  python ./main.py
```

