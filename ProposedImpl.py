from django.http import HttpResponse
from django.shortcuts import render
import pymysql
from datetime import date
import json
import requests
import pandas as pd
import urllib.request
from datetime import datetime
from urllib.request import Request, urlopen
from nltk.tokenize import sent_tokenize
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet   #Import wordnet from the NLTK
from nltk.corpus import stopwords
import nltk
from django.core.files.storage import FileSystemStorage
import requests
from . import aqgFunction
mydb=pymysql.connect(host="localhost",user="root",password="root",database="questiongenerator")
def exquestiongen(request):
     # Create AQG object
     
    aqg = aqgFunction.AutomaticQuestionGenerator()
    inputTextPath = "D://PHD Projects/Khushabu Khandait/Test6/Automatic-Question-Generator-master/AutomaticQuestionGenerator/data.txt"
    readFile = open(inputTextPath, 'r+', encoding="utf8")
    inputText = readFile.read()
    questionList = aqg.aqgParse(inputText)
    payload = []
    content={}
    payload2 = []
    content2={}
    content2 = {'data': inputText }
    payload2.append(content2)
    for x in questionList:
        content = {'statement': x }
        payload.append(content)
        ontent = {}
        print(x)
    #aqg.display(questionList)
    return render(request,"ExistingQuestiionGen.html",{'list': {'items':payload},'list2':{'items':payload2}})

def proposedque(request):

    aqg = aqgFunction.AutomaticQuestionGenerator()
    #-----------------------get Stop Words------------------
    en_stops = set(stopwords.words('english'))

    #-------------------apply statement tokenisation--------------------------------
    #inputText = '''I am Dipta. I love codding. I build my carrier with this.'''
    inputTextPath = "D://PHD Projects/Khushabu Khandait/Test6/Automatic-Question-Generator-master/AutomaticQuestionGenerator/data.txt"
    readFile = open(inputTextPath, 'r+', encoding="utf8")
    inputText = readFile.read()
    text =inputText
    print("------------Statement Tokenisation --------")
    x=sent_tokenize(text)
    para=""
    stm=""
    for k in x:
        final_para=""
        stm=""
        nltk_tokens = nltk.word_tokenize(k)
        print (nltk_tokens)
        for j in nltk_tokens:
            vect=""
            if j not in en_stops:
                try:
                    synset = wordnet.synsets(j)
                    wordnet.synsets(j)
                    vect=synset[0].lemmas()[0].name()
                    print('Synonym of'+ j+' is: '+ synset[0].lemmas()[0].name())
                    
                except:
                    vect=j
                    print("exp")
            else:
                vect=j
                print("Stop word "+j)
            stm=stm+" "+vect
        
        para=para+""+stm
            
        print("Final Statement ----"+stm)
        print("===============Final Paragraph================")
        print("Final  ----"+para)
        
        f = open("D://PHD Projects/Khushabu Khandait/Test6/Automatic-Question-Generator-master/AutomaticQuestionGenerator/lama.txt", "w")
        f.write(para)
        f.close()

        print("-------Proposed----------------")
        inputTextPath1 = "D://PHD Projects/Khushabu Khandait/Test6/Automatic-Question-Generator-master/AutomaticQuestionGenerator/lama.txt"
        readFile1 = open(inputTextPath1, 'r+', encoding="utf8")
        inputText1 = readFile1.read()
        questionList1 = aqg.aqgParse(inputText1)
        payload = []
        content={}
        payload2 = []
        content2={}
        content2 = {'data': inputText }
        payload2.append(content2)
        for x in questionList1:
            content = {'statement': x }
            payload.append(content)
            content = {}
        return render(request,"ProposedQuestionGen.html",{'list': {'items':payload},'list2':{'items':payload2}})
def addtotext(request):
    statement=request.POST.get('statement')
    f = open("D://PHD Projects/Khushabu Khandait/Test6/Automatic-Question-Generator-master/AutomaticQuestionGenerator/data.txt", 'w')
    cur=mydb.cursor()
    sql="insert into statements(statement)values(%s)"
    values=(statement.strip())
    cur.execute(sql,values)
    mydb.commit()
    f.write(statement)
    return render(request,"AdminDashboard.html")
    
def adminhome(request):
    return render(request,"AdminDashboard.html")

def uploadedstatements(request):
    sql="select * from statements";
    cur1=mydb.cursor()
    cur1.execute(sql)
    result=cur1.fetchall()
    payload = []
    content={}
    #json=jsonify(result)
    for row in result:
        content = {'statement': row[1]}
        payload.append(content)
        content = {}
    print(f"json: {json.dumps(payload)}")
    return render(request,"UploadedStatement.html", {'list': {'items':payload}})
