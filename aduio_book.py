import PyPDF2
import pyttsx3


pdfReader = PyPDF2.PdfReader(open('osama.pdf.pdf', 'rb'))

speaker = pyttsx3.init("PDF")

for page_num in range(pdfReader.numPages):
    text = pdfReader.getPage(page_num).extract_text()
    speaker.say(text)
    speaker.runAndWait()

speaker.stop()
speaker.save_to_file(text, 'audio.mp3')
speaker.runAndWait()
