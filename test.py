# import googletrans
# from googletrans import Translator

# # print(googletrans.LANGUAGES)

# text1 = "Hello welcome to my website!"


# translator = Translator()

# # print(translator.detect(text1))

# trans1 = translator.translate(text1, src='en', dest='ko')
# trans2 = translator.translate(text1, src='en', dest ='ja')

# print("English to Japanese: ", trans1.text)
# print("일본어로 번역:",trans2.text)

# # print(googletrans.LANGCODES)

from gtts import gTTS
tts = gTTS('hello')
tts.save('hello.mp3')