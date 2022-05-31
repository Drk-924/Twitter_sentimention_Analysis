import aqgFunction
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import wordnet as wn
# Main Function
def main():
    # Create AQG object
    aqg = aqgFunction.AutomaticQuestionGenerator()

    inputTextPath = "D://PHD Projects/Khushabu Khandait/Test6/Automatic-Question-Generator-master/AutomaticQuestionGenerator/data.txt"

    readFile = open(inputTextPath, 'r+', encoding="utf8")
    
    #readFile = open(inputTextPath, 'r+', encoding="utf8", errors = 'ignore')

    #-------------------apply statement tokenisation--------------------------------
    

    inputText = readFile.read()
    #inputText = '''I am Dipta. I love codding. I build my carrier with this.'''

    text =inputText
    print("------------Statement Tokenisation --------")
    x=sent_tokenize(text)
    
    for k in x:
        nltk_tokens = nltk.word_tokenize(k)
        
        print (nltk_tokens)
        print(k)




    questionList = aqg.aqgParse(inputText)
    #print(questionList)
    out=aqg.display(questionList)
    
    #aqg.DisNormal(questionList)

    return 0


# Call Main Function
if __name__ == "__main__":
    main()

