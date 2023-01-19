# Data normalization
Hai, semoga harimu senantiasa diberkahi.  

Jadi ini ada Google Sheets yang isinya kata-kata yang ada di dalam vocabulary hasil dari ```CountVectorizer()```.
Kata-kata di sini masih banyak yang belum bisa diproses secara langsung oleh stemmer.
Harapannya dengan normalisasi kata-kata yang ada menjadi bentuk baku kita bisa membuat data yang kita punya lebih bersih.  

Data vocabulary diambil setiap minggu di hari Jumat.
1. [Kumpulan kata per tanggal 21 Oktober 2022](https://docs.google.com/spreadsheets/d/1vPfyvw0GJJN03xn3gh-1P9RkaQTVcuEm/edit?usp=sharing&ouid=114527365404429170664&rtpof=true&sd=true), berdasarkan [dataset ini](https://github.com/YourneyID/Yourney-Incubations/blob/ml-dev/Machine%20Learning/_dataset/dataset_unique%202022-10-21a.csv).

## Notes and stuff  
### How we work with them?  
1. Buka spreadsheet yang sudah disediakan di link data vocabulary. Spreadsheet juga ada di folder Machine Learning di Drive Yourney.
2. Isi koreksi kata di kolom yang sudah disediakan pakai huruf kecil.
3. Nanti rencananya ```kata``` akan diganti dengan ```kata_koreksi```, maka:  
    1. Kata yang sudah benar ditulis ulang di ```kata_koreksi```
    2. Kata yang akan dihapus dikosongkan di ```kata_koreksi```
    3. Kata yang seharusnya jadi lebih dari satu kata ditulis pakai spasi di ```kata_koreksi``` ([Konteks ada di sini, poin ketujuh](https://github.com/YourneyID/Yourney-Incubations/new/ml-dev/Machine%20Learning/_vocab#ada-beberapa-hal-yang-perlu-diperhatikan-waktu-mengubah-kata-kata-yang-ada-menjadi-kata-baku))

### Ada beberapa hal yang perlu diperhatikan waktu mengubah kata-kata yang ada menjadi kata baku:
- Kita asumsikan ada dua bahasa dalam tweet, Bahasa Indonesia dan Bahasa inggris. Kita ubah ke dalam bentuk baku di masing-masing bahasa.
- Ada kesalahan dalam prerpocessing tweet. Niatnya menghapus RT di awal jadi kehapus semua. Untuk kata-kata yang kedengaran agak konyol mungkin karena RTnya hilang:  
    peama -> pertama  
    effo -> effort  
    apaemen -> apartemen  
    dll.  
- Ubah kata non baku:  
    afa -> apa  
    iyh -> ya  
    dll.  
- Ubah singkatan:  
    pls -> please  
    sy -> saya  
    knp -> kenapa  
    dll.  
- Singkatan umum kalau dibiarkan gapapa, diubah ke kepanjangannya juga gapapa:  
    btw -> by the way  
    jakut -> jakarta utara  
    tkp -> tempat kejadian perkara  
    dll.
- Kata dengan huruf berulang dihapus dulu huruf yang berulang sebelum diubah ke dalam bentuk baku:  
    plssss -> pls -> please  
    iyaaa -> iya -> ya  
    aamiiinnnn -> amin  
    dll.  
- Pisahkan kata yang seharusnya terpisah. Sesuaikan bentuk bakunya sesuai bahasa:  
    gakfolowporno -> tidak follow porno  
    cebongkelautaja -> cebong ke laut saja  
    aniesbaswedanforpresiden -> anies baswedan for presiden  
    dll.  
    _I swear those words are real data 💀 go check word number 124-126_
- Kata Bahasa Inggris dengan imbuhan Bahasa Indonesia (misal: bersweater) kita ambil bentuk Bahasa Inggrisnya.
- Ekspresi kita ganti dengan ```<ekspresi>``` aja kali ya?  
    **update 27/10: ada beberapa ekspresi yang bisa ditulis**  
    **update 28/10: kumpulan ekspresi bisa dilihat [di sini](https://gist.github.com/aliifnrhmn/761b5f6a288712d9af76be53f26deb36)**  
    ihhh, skksksk, beuhh -> ```<gemas>```  
    hhhhh, huhuhu -> ```<sedih>```  
    wkwkw, hahaha, sngkak -> ```<tawa>```  
    dll.  
    > tips nyari kata di dataset csv: ```(spasi)kata_yang_dicari(spasi)```  
- Kata yang bergabung dengan angka dihapus angkanya, simpan katanya:  
    3265mdpl -> mdpl  
    100m -> meter  
    24jt -> juta  
    dll.  
- _more consideration will be added soon if needed._
