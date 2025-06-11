import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import pickle 
books=pd.read_csv("Books.csv")
rating=pd.read_csv("Ratings.csv")
user=pd.read_csv("Users.csv")
rating_with_name=rating.merge(books,on='ISBN')

num_rating_df=rating_with_name.groupby('Book-Title').count()['Book-Rating'].reset_index()
num_rating_df.rename(columns={'Book-Rating':'num_ratings'},inplace=True)
avg_rating_df=rating_with_name.groupby('Book-Title').mean()['Book-Rating'].reset_index()
avg_rating_df.rename(columns={'Book-Rating':'avg_ratings'},inplace=True)
#POPULARITY BASED RECOMMENDATION SYSTEM
popular_df=num_rating_df.merge(avg_rating_df,on='Book-Title')
popular_df=popular_df[popular_df['num_ratings']>=250].sort_values('avg_ratings',ascending=False).head(50)
popular_df=popular_df.merge(books,on='Book-Title').drop_duplicates('Book-Title')[['Book-Title','Book-Author','num_ratings','avg_ratings','Image-URL-M']]
#COLLABORATIVE FILTERING BASED RECOMMENDATION SYSTEM
r=rating_with_name.groupby('User-ID').count()['Book-Rating']>200
used_users=r[r].index
filtered=rating_with_name[rating_with_name['User-ID'].isin(used_users)]
y=filtered.groupby('Book-Title').count()['Book-Rating']>=50
famous_books=y[y].index
final_rating=filtered[filtered['Book-Title'].isin(famous_books)]
pt=final_rating.pivot_table(index='Book-Title',columns='User-ID',values='Book-Rating')
pt.fillna(0,inplace=True)
similarity=cosine_similarity(pt)
data=[]
def recommend(book_name):
    index=np.where(pt.index==book_name)[0][0]
    data=[]
    similar_items=sorted(list(enumerate(similarity[index])),key=lambda x:x[1],reverse=True)[1:6]
    for i in similar_items:
        item=[]
        temp=books[books['Book-Title']==pt.index[i[0]]]
        item.extend(list(temp.drop_duplicates("Book-Title")['Book-Title'].values))
        item.extend(list(temp.drop_duplicates("Book-Title")['Book-Author'].values))
        item.extend(list(temp.drop_duplicates("Book-Title")['Image-URL-M'].values))
        data.append(item)
    return data

pickle.dump(pt,open('pt.pkl','wb'))
pickle.dump(books,open('books.pkl','wb'))
pickle.dump(similarity,open('similarity.pkl','wb'))
top_10_images = [
    "https://www.wallpapergap.com/cdn/24/175/harry-potter-books-wallpapers-1920x1080.jpg",
    "https://www.theonering.net/torwp/wp-content/uploads/2014/07/Hobbit_3_Horizontal_Teaser.jpg",
    "https://c4.wallpaperflare.com/wallpaper/831/173/228/movies-fantasy-art-the-lord-of-the-rings-the-fellowship-of-the-ring-artwork-mountains-hd-wallpaper-preview.jpg",
    "https://www.bloomsbury.com/media/gyvd3qn0/hp1_wallpaper_desktop_768x1024-v2.jpg",
    "https://chiefessays.net/wp-content/uploads/2018/02/to-kill-a-mockingbird-book-cover.jpg",
    "https://wallpapercat.com/w/full/6/a/2/32816-1920x1080-desktop-full-hd-life-of-pi-wallpaper.jpg",
]

with open("top10_images.pkl", "wb") as images:
    pickle.dump(top_10_images, images)