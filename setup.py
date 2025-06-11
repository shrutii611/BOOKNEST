from flask import Flask,render_template,request
import pickle
import numpy as np
popular_df=pickle.load(open('popular.pkl','rb'))
pt=pickle.load(open('pt.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))
images=pickle.load(open('top10_images.pkl','rb'))
app=Flask(__name__)

@app.route("/", methods=['GET','POST'])
def hello_world():
   if request.method=='GET':
        return render_template('home.html',
                               images=images,
                               book_name=list(popular_df['Book-Title'].values),
                               author=list(popular_df['Book-Author'].values),
                               image=list(popular_df['Image-URL-M'].values),
                               votes=list(popular_df['num_ratings'].values),
                               rating=list(popular_df['avg_ratings'].values))
   
@app.route("/recommend",methods=['GET'])
def recommend():
   if request.method=='GET':
       return render_template('recommend.html')
   
@app.route("/recommend_books",methods=['POST'])
def recommend_books():
    user_input=request.form.get('user_input')
    index=np.where(pt.index==user_input)[0][0]
    data=[]
    similar_items=sorted(list(enumerate(similarity[index])),key=lambda x:x[1],reverse=True)[1:6]
    for i in similar_items:
        item=[]
        temp=books[books['Book-Title']==pt.index[i[0]]]
        item.extend(list(temp.drop_duplicates("Book-Title")['Book-Title'].values))
        item.extend(list(temp.drop_duplicates("Book-Title")['Book-Author'].values))
        item.extend(list(temp.drop_duplicates("Book-Title")['Image-URL-M'].values))
        data.append(item)
    print(data)
    return render_template('recommend.html',data=data)



@app.route('/bot')
def bot():
    if request.method=='GET':
        return render_template('bot.html')
    
@app.route('/todo')
def todo():
    if request.method=='GET':
        return render_template('todo.html')
if __name__=='__main__':
    app.run(debug=True)
