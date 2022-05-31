import aqgFunction


# Main Function
def main():
    # Create AQG object
    inputTextPath = "D://PHD Projects/Khushabu Khandait/Test6/Automatic-Question-Generator-master/AutomaticQuestionGenerator/data.txt"
    readFile = open(inputTextPath, 'r+', encoding="utf8")
    inputText = readFile.read()
    text =inputText
    aqg = aqgFunction.AutomaticQuestionGenerator()
    
    inputTextPath = "D://PHD Projects/Khushabu Khandait/Test6/Automatic-Question-Generator-master/AutomaticQuestionGenerator/data.txt"
    readFile = open(inputTextPath, 'r+', encoding="utf8")
    #readFile = open(inputTextPath, 'r+', encoding="utf8", errors = 'ignore')

    inputText = readFile.read()
    #inputText = '''I am Dipta. I love codding. I build my carrier with this.'''

    questionList = aqg.aqgParse(inputText)
    aqg.display(questionList)

    #aqg.DisNormal(questionList)

    return 0


# Call Main Function
if __name__ == "__main__":
    main()

