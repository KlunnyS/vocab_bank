from flask import Flask, render_template, redirect, url_for, flash, request
from werkzeug.utils import secure_filename
from uuid import uuid4
import os

from forms import KanjiForm, VocabForm, KanjiSearch
from models import db, Kanji, Vocab

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sigma67'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kanji.db'
app.config['SQLALCHEMY_BINDS'] = { 'vocab':'sqlite:///vocab.db' }
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/img/upload'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/' ,methods=['GET', 'POST'])
def home_page():
    form = KanjiSearch()
    
    if form.validate_on_submit():
        print("????",form.kanji.data)
        N5 = Kanji.query.filter_by(level="N5",kanji=form.kanji.data).all()
        N4 = Kanji.query.filter_by(level="N4",kanji=form.kanji.data).all()
        N3 = Kanji.query.filter_by(level="N3",kanji=form.kanji.data).all()
        N2 = Kanji.query.filter_by(level="N2",kanji=form.kanji.data).all()
        N1 = Kanji.query.filter_by(level="N1",kanji=form.kanji.data).all()
    else:
        N5 = Kanji.query.filter_by(level="N5").all()
        N4 = Kanji.query.filter_by(level="N4").all()
        N3 = Kanji.query.filter_by(level="N3").all()
        N2 = Kanji.query.filter_by(level="N2").all()
        N1 = Kanji.query.filter_by(level="N1").all()
        
    N5_count = len(N5)
    N4_count = len(N4)
    N3_count = len(N3)
    N2_count = len(N2)
    N1_count = len(N1)
    return render_template('index.html',N5=N5,N5_count=N5_count,N4=N4,N4_count=N4_count,N3=N3,N3_count=N3_count,N2=N2,N2_count=N2_count,N1=N1,N1_count=N1_count,form=form)

@app.route('/vocab/<kanji>')
def vocab(kanji):
    vocab = Vocab.query.all() 
    desired = []
    for word in vocab:
        if kanji in word.kanji_list:
            desired.append(word)
    return render_template('vocab.html',vocab=desired,kanji=kanji)


@app.route('/add-kanji',methods=['GET', 'POST'] )
def add_kanji():
    form = KanjiForm()
    if form.validate_on_submit():
        print(form.stroke_order,type(form.stroke_order))
        
        if form.stroke_order.data:#works yay
            file = form.stroke_order.data

            old = os.path.splitext(file.filename)[1].lower()

            filename = f"{uuid4().hex}{old}"

            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            file.save(path)

            # filename = None
        else:
            filename = None   

        new_kanji = Kanji(
            kanji = form.kanji.data,
            stroke_order = filename,
            level = form.level.data,
            meanings = form.meanings.data,
            kun = form.kun.data,
            on= form.on.data,
            radical = form.radical.data
        )
    
        db.session.add(new_kanji)
        db.session.commit()
        return redirect(url_for('home_page'))
    
    return render_template('add-kanji.html',form=form)

@app.route('/add-vocab',methods=['GET', 'POST'] )
def add_vocab():
    form = VocabForm()
    if form.validate_on_submit():

        new_Vocab = Vocab(
            kanji_list = form.kanji_list.data,
            vocab = form.vocab.data,
            translation = form.translation.data
        )
    
        db.session.add(new_Vocab)
        db.session.commit()
        return redirect(url_for('home_page'))
    
    return render_template('add-vocab.html',form=form)


@app.route("/edit-kanji/<int:kanji_id>",methods=['GET', 'POST'])
def edit_kanji(kanji_id):
    form = KanjiForm()
    kanji = Kanji.query.get_or_404(kanji_id)
    if form.validate_on_submit():
        print(form.stroke_order.data)
        if form.stroke_order.data:
            file = form.stroke_order.data

            old = os.path.splitext(file.filename)[1].lower()

            filename = f"{uuid4().hex}{old}"

            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            file.save(path)

        else:
            filename = "default.png"

        kanji.kanji = form.kanji.data
        if form.change_stroke_order.data:
            kanji.stroke_order = filename
        if form.change_level.data:
            kanji.level = form.level.data
        kanji.meanings = form.meanings.data
        kanji.kun = form.kun.data
        kanji.on = form.on.data
        kanji.radical = form.radical.data
        
        db.session.commit()
        return redirect(url_for('home_page'))
        
    return render_template('edit-kanji.html',form=form,kanji=kanji)

@app.route("/edit-vocab/<int:vocab_id>",methods=['GET', 'POST'])
def edit_vocab(vocab_id):
    form = VocabForm()
    vocab = Vocab.query.get_or_404(vocab_id)
    
    if form.validate_on_submit():

        vocab.vocab = form.vocab.data
        vocab.kanji_list = form.kanji_list.data
        vocab.translation = form.translation.data
        
        db.session.commit()
        return redirect(url_for('home_page'))
        
    return render_template('edit-vocab.html',form=form,vocab=vocab)

@app.route("/odstran/<int:kanji_id>")
def del_kanji(kanji_id):
    kanji = Kanji.query.get_or_404(kanji_id)
    db.session.delete(kanji)
    db.session.commit()
    return redirect(url_for("home_page"))