import pandas as pd
from PIL import Image
import pytesseract


"""
string = pytesseract.image_to_string(Image.open("test1.png"))
just_the_image = Image.open("test1.png")
just_the_image.show()

new_df = pd.DataFrame([0,0,0])
print(new_df)
print(string)
"""

def only_alpha_num(list_of_strings):
    new_list = []
    for string in list_of_strings:
        for character in string:
            if character.isalnum():
                new_list.append(string)
                break
    return(new_list)




def scan_to_string(image_object):
    bw_image = image_object.convert("L")
    string = pytesseract.image_to_string(bw_image)
    print("We were able to find: " + string)
    # get rid of all the extra line breaks that tesseract thinks it sees
    string_list = string.split("\n")
    # delete all the items without alphanumerics to get 
    string_list = only_alpha_num(string_list)
    # delete all the un-needed punctuation
    # bring it all back together into a string with line breaks
    found_text = "\n".join(string_list)
    if found_text == "":
        found_text = "No text succesfully extracted"
    return found_text