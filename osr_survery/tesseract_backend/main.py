import pandas as pd
from PIL import Image
import pytesseract


string = pytesseract.image_to_string(Image.open("test1.png"))
just_the_image = Image.open("test1.png")
just_the_image.show()

new_df = pd.DataFrame([0,0,0])
print(new_df)
print(string)