#menggunkan library wordcloud
from wordcloud import WordCloud, STOPWORDS , ImageColorGenerator
import pandas as pd
import matplotlib.pylab as plt
from PIL import Image
import numpy as np

#masking untuk wordcloud berbentuk logo twitter
mask = np.array(Image.open('H:\BANGKIT\CAPSTONE\WordCloud\logo.png'))

#stopword dari wordcloud dengan bahasa indo
stop = open('stopwords_id.txt', 'r').read()

#membaca data dari file csv (cleaned_kuliner dapat diganti dengan file csv lainnya)
data_file = pd.read_csv('H:\BANGKIT\CAPSTONE\WordCloud\Cleaned_Kuliner.csv')

#wordcloud
wordcloud = WordCloud(stopwords = stop, 
                      width=1600, 
                      height=1600,
                      mask=mask,
                      background_color="White",
                      collocations=False,
                      colormap="Set2").generate(''.join(data_file['cleaned_tweet']))

#enhance dari wordcloud
plt.figure(figsize=(20,20),
           facecolor='k',
           edgecolor='k')
plt.imshow(wordcloud,interpolation='bilinear')
plt.axis('off')
plt.tight_layout (pad=0)

#simpan hasil ke folder output
wordcloud.to_file ('H:\BANGKIT\CAPSTONE\WordCloud\output\Kuliner.png')
plt.show()