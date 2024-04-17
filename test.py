from googletrans import Translator

# Khởi tạo một đối tượng Translator
translator = Translator()

# Dịch một đoạn văn bản từ tiếng Anh sang tiếng Tây Ban Nha
text = "Spy Kids"
translated_text = translator.translate(text, src='en', dest='vi')

# In kết quả dịch
print(translated_text.text)