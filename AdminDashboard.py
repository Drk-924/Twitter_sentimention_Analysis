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


def logout(request):
    return render(request,"page1.html")
    
def dummy(request):
    sql="select * from statements order by sid desc";
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
    return render(request,"index.html", {'list': {'items':payload}})
def UserFeedback(request):
    questions = request.POST.getlist('c1')
    totalque=request.POST.get('totalque')
    intcount=0
    for x in questions:
        intcount=intcount+1
    payload1 = []
    content1={}
    content1={'tque':str(totalque),'tp':str(intcount) }
    payload1.append(content1)
    return render(request,"UserFeedback.html",{'list': {'items':payload1}})

def tweetsbymeth2(request):
    
    #-------------------apply statement tokenisation--------------------------------
    #inputText = '''I am Dipta. I love codding. I build my carrier with this.'''
    inputTextPath = "C:/Users/Parimal/Desktop/Twitter project/Code Work/data.txt"
    readFile = open(inputTextPath, 'r+', encoding="utf8")
    inputText = readFile.read()
    text =inputText
    print("------------Statement Tokenisation --------")
    x=sent_tokenize(text)
    para=""
    stm=""
    payload1 = []
    content1={}
    payload2 = []
    
    payload = []
    content={}
    key = "inputs"
    qgen=0
    val=request.session['val']
    global API_URL
    #API_URL = "https://api-inference.huggingface.co/models/iarfmoose/t5-base-question-generator"
    print("value",val)
    API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-xlm-roberta-base-sentiment"
    headers = {"Authorization": "Bearer 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"}
    response = requests.post(API_URL, headers=headers, json=text)
    json_str  = response.json()
    y = json_str[0]
    print(y)
    a1=y[0]
    print(a1['score'])
    content = {'statement': str(a1['score']*100) }
    payload.append(content)
    content = {}
    y1 = json_str[0]
    a2=y1[1]
    content={'tque':str(a2['score']*100)}
    payload1.append(content)

    content2 = {}
    y2 = json_str[0]
    a3=y2[2]
    content2={'tque1':str(a3['score']*100)}
    payload2.append(content2)
    
    return render(request,"GeneratedResultScoreMeth2.html",{'list': {'items':payload},'list2':{'items2':payload1},'list3':{'items3':payload2}})






def t5question_gen(request):
    
    #-------------------apply statement tokenisation--------------------------------
    #inputText = '''I am Dipta. I love codding. I build my carrier with this.'''
    inputTextPath = "C:/Users/Parimal/Desktop/Twitter project/Code Work/data.txt"
    readFile = open(inputTextPath, 'r+', encoding="utf8")
    inputText = readFile.read()
    text =inputText
    print("------------Statement Tokenisation --------")
    x=sent_tokenize(text)
    para=""
    stm=""
    payload1 = []
    content1={}
    
    payload = []
    content={}
    key = "inputs"
    qgen=0
    val=request.session['val']
    global API_URL
    #API_URL = "https://api-inference.huggingface.co/models/iarfmoose/t5-base-question-generator"
    print("value",val)
    if(val=="t5generator"):
        API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment"
        print("value",val)
    if(val=="t5generatorsmall"):
        API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-xlm-roberta-base-sentiment"
        print("value",val)
    if(val=="bart"):
        API_URL = "https://api-inference.huggingface.co/models/voidful/bart-eqg-question-generator"
        print("value",val)
    if(val=="gp2"):
        API_URL = "https://api-inference.huggingface.co/models/danyaljj/gpt2_question_generation_given_paragraph"
        print("value",val)
    headers = {"Authorization": "Bearer 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"}
    response = requests.post(API_URL, headers=headers, json=text)
    json_str  = response.json()
    y = json_str[0]
    a1=y[0]
    print(a1['score'])
    content = {'statement': str(a1['score']*100) }
    payload.append(content)
    content = {}
    y1 = json_str[0]
    a2=y1[1]
    content={'tque':str(a2['score']*100)}
    payload1.append(content)
    
    return render(request,"GeneratedResultScore.html",{'list': {'items':payload},'list2':{'items2':payload1}})

def exquestiongen(request):
     # Create AQG object
    aqg = aqgFunction.AutomaticQuestionGenerator()
    inputTextPath = "C:/Users/Parimal/Desktop/Twitter project/Code Work/data.txt"
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
    inputTextPath = "C:/Users/Parimal/Desktop/Twitter project/Code Work/data.txt"
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
        
        f = open("C:/Users/Parimal/Desktop/Twitter project/Code Work/lama.txt", "w")
        f.write(para)
        f.close()

        print("-------Proposed----------------")
        inputTextPath1 = "C:/Users/Parimal/Desktop/Twitter project/Code Work/lama.txt"
        readFile1 = open(inputTextPath1, 'r+', encoding="utf8")
        inputText1 = readFile1.read()
        questionList1 = aqg.aqgParse(inputText1)
        payload = []
        content={}
        payload2 = []
        content2={}
        content2 = {'data': inputText }
        payload2.append(content2)
        qgen=0
        for x in questionList1:
            if(x==None):
                print("null")
            else:
                content = {'statement': x }
                payload.append(content)
                qgen=qgen+1
                content = {}
        print("QGen",qgen)
        content={'tque':str(qgen)}
        payload1.append(content)
        print(payload1)
        return render(request,"ProposedQuestionGen.html",{'list': {'items':payload},'list2':{'items2':payload1}})

def prstatementtoken(request):
    aqg = aqgFunction.AutomaticQuestionGenerator()
    #-----------------------get Stop Words------------------
    en_stops = set(stopwords.words('english'))
    val=request.GET.get('value')
    request.session['val']=val

    #-------------------apply statement tokenisation--------------------------------
    #inputText = '''I am Dipta. I love codding. I build my carrier with this.'''
    inputTextPath = "C:/Users/Parimal/Desktop/Twitter project/Code Work/data.txt"
    readFile = open(inputTextPath, 'r+', encoding="utf8")
    inputText = readFile.read()
    text =inputText
    print("------------Statement Tokenisation --------")
    x=sent_tokenize(text)
    para=""
    stm=""
    payload = []
    content={}
    payload2 = []
    content2={}
    content2 = {'data': inputText }
    payload2.append(content2)
    for k in x:
        content = {'statement': k }
        payload.append(content)
        content = {}
    return render(request,"PRStatementTokenisation.html",{'list': {'items':payload}})

def statementtoken(request):
    aqg = aqgFunction.AutomaticQuestionGenerator()
    #-----------------------get Stop Words------------------
    en_stops = set(stopwords.words('english'))
    val=request.GET.get('value')
    request.session['val']=val

    #-------------------apply statement tokenisation--------------------------------
    #inputText = '''I am Dipta. I love codding. I build my carrier with this.'''
    inputTextPath = "C:/Users/Parimal/Desktop/Twitter project/Code Work/data.txt"
    readFile = open(inputTextPath, 'r+', encoding="utf8")
    inputText = readFile.read()
    text =inputText
    print("------------Statement Tokenisation --------")
    x=sent_tokenize(text)
    para=""
    stm=""
    payload = []
    content={}
    payload2 = []
    content2={}
    content2 = {'data': inputText }
    payload2.append(content2)
    for k in x:
        content = {'statement': k }
        payload.append(content)
        content = {}
    return render(request,"StatementTokenisation.html",{'list': {'items':payload}})
def wordtoken(request):
    aqg = aqgFunction.AutomaticQuestionGenerator()
    #-----------------------get Stop Words------------------
    en_stops = set(stopwords.words('english'))

    #-------------------apply statement tokenisation--------------------------------
    #inputText = '''I am Dipta. I love codding. I build my carrier with this.'''
    inputTextPath = "C:/Users/Parimal/Desktop/Twitter project/Code Work/data.txt"
    readFile = open(inputTextPath, 'r+', encoding="utf8")
    inputText = readFile.read()
    text =inputText
    print("------------Statement Tokenisation --------")
    x=sent_tokenize(text)
    para=""
    stm=""
    payload = []
    content={}
    payload2 = []
    content2={}
    content2 = {'data': inputText }
    payload2.append(content2)
    for k in x:
        nltk_tokens = nltk.word_tokenize(k)
        for j in nltk_tokens:
            content = {'statement': j }
            payload.append(content)
            content = {}
    return render(request,"WordTokenisation.html",{'list': {'items':payload}})

def stopwordremoval(request):
    aqg = aqgFunction.AutomaticQuestionGenerator()
    #-----------------------get Stop Words------------------
    en_stops = set(stopwords.words('english'))

    #-------------------apply statement tokenisation--------------------------------
    #inputText = '''I am Dipta. I love codding. I build my carrier with this.'''
    inputTextPath = "C:/Users/Parimal/Desktop/Twitter project/Code Work/data.txt"
    readFile = open(inputTextPath, 'r+', encoding="utf8")
    inputText = readFile.read()
    text =inputText
    print("------------Statement Tokenisation --------")
    x=sent_tokenize(text)
    para=""
    stm=""
    payload = []
    content={}
    payload2 = []
    content2={}
    content2 = {'data': inputText }
    payload2.append(content2)
    for k in x:
        nltk_tokens = nltk.word_tokenize(k)
        for j in nltk_tokens:
            if j not in en_stops:
                content = {'statement': j }
                payload.append(content)
                content = {}
    return render(request,"StopwordRemoval.html",{'list': {'items':payload}})
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()
def wordvectorisation(request):

    #print (json_str[1])
    aqg = aqgFunction.AutomaticQuestionGenerator()
    #-----------------------get Stop Words------------------
    en_stops = set(stopwords.words('english'))

    #-------------------apply statement tokenisation--------------------------------
    #inputText = '''I am Dipta. I love codding. I build my carrier with this.'''
    inputTextPath = "C:/Users/Parimal/Desktop/Twitter project/Code Work/data.txt"
    readFile = open(inputTextPath, 'r+', encoding="utf8")
    inputText = readFile.read()
    text =inputText
    print("------------Statement Tokenisation --------")
    x=sent_tokenize(text)
    para=""
    stm=""
    payload = []
    content={}
    payload2 = []
    content2={}
    content2 = {'data': inputText }
    payload2.append(content2)
    for k in x:
        nltk_tokens = nltk.word_tokenize(k)
        for j in nltk_tokens:
            if j not in en_stops:
                try:
                    
                    synset = wordnet.synsets(j)
                    wordnet.synsets(j)
                    vect=synset[0].lemmas()[0].name()
                    content = {'statement': 'Word Vector of '+ j+' is: '+ synset[0].lemmas()[0].name() }
                    payload.append(content)
                    content = {}
                except:
                    print("exp")
    return render(request,"WordVectorisation.html",{'list': {'items':payload}})
def paraformation(request):
    aqg = aqgFunction.AutomaticQuestionGenerator()
    #-----------------------get Stop Words------------------
    en_stops = set(stopwords.words('english'))

    #-------------------apply statement tokenisation--------------------------------
    #inputText = '''I am Dipta. I love codding. I build my carrier with this.'''
    inputTextPath = "C:/Users/Parimal/Desktop/Twitter project/Code Work/data.txt"
    readFile = open(inputTextPath, 'r+', encoding="utf8")
    inputText = readFile.read()
    text =inputText
    print("------------Statement Tokenisation --------")
    x=sent_tokenize(text)
    para=""
    stm=""
    vect=""
    payload = []
    content={}
    payload2 = []
    content2={}
    content2 = {'data': inputText }
    payload2.append(content2)
    for k in x:
        nltk_tokens = nltk.word_tokenize(k)
        for j in nltk_tokens:
            if j not in en_stops:
                try:
                    synset = wordnet.synsets(j)
                    wordnet.synsets(j)
                    vect=synset[0].lemmas()[0].name()
                    
                except:
                    print("exp")
            else:
                vect=j
            stm=stm+" "+vect
        para=para+""+stm
        


    API_URL = "https://api-inference.huggingface.co/models/distilgpt2"
    headers = {"Authorization": "Bearer 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"}
    
    payload1={}
    key = "inputs"
    value = text
    #payload1 = {
               # "inputs": text,
                #}
    payload1[key]=value
    response = requests.post(API_URL, headers=headers, json=payload1)
    json_str  = response.json()
    y = json_str[0]
    content = {'statement': str(y["generated_text"]) }
    payload.append(content)
    content = {}
    print(y["generated_text"])
    return render(request,"ParaFormation.html",{'list': {'items':payload}})

def proposedqagen(request):
    
    inputTextPath = "C:/Users/Parimal/Desktop/Twitter project/Code Work/data.txt"
    readFile = open(inputTextPath, 'r+', encoding="utf8")
    inputText = readFile.read()
    text =inputText
    
    API_URL = "https://api-inference.huggingface.co/models/distilgpt2"
    headers = {"Authorization": "Bearer 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"}
    
    payload1={}
    key = "inputs"
    value = text
    #payload1 = {
               # "inputs": text,
                #}
    payload1[key]=value
    response = requests.post(API_URL, headers=headers, json=payload1)
    json_str  = response.json()
    y = json_str[0]
    data=str(y["generated_text"])
    #---------------Generating Question---------------------------
    aqg = aqgFunction.AutomaticQuestionGenerator()
    questionList1 = aqg.aqgParse(data)
    payload = []
    content={}
    payload2 = []
    content2={}
    payload1 = []
    content1={}
    content2 = {'data': data }
    payload2.append(content2)
    qgen=0
    for x in questionList1:
        content = {'statement': x }
        payload.append(content)
        content = {}
        qgen=qgen+1
    content={'tque':str(qgen)}
    payload1.append(content)
    return render(request,"ProposedQuestionGen.html",{'list': {'items':payload},'list2':{'items2':payload1}})
    
    

def addtotext(request):
    statement=request.POST.get('statement')
    f = open("C:/Users/Parimal/Desktop/Twitter project/Code Work/data.txt", 'w')
    cur=mydb.cursor()
    sql="insert into statements(statement)values(%s)"
    values=(statement.strip())
    cur.execute(sql,values)
    mydb.commit()
    f.write(statement)
    return render(request,"index.html")
    
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
