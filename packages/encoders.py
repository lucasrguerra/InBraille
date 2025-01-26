from packages import alphabets



def northAmerican(text):
    braille = ""
    phrases = text.split("\n")
    for phrase in phrases:
        words = phrase.replace('"', "'").split(" ")
        for word in words:
            for letter in word:
                try:
                    index_of_letter = alphabets.NorthAmerican.normal.index(letter.lower())
                    braille += alphabets.NorthAmerican.braille[index_of_letter]
                except:
                    pass
            braille += " "

        braille = braille.rstrip() + "\n"

    return braille.rstrip()



def brazilian(text):
    treated_text = ""
    phrases = text.split("\n")
    for phrase in phrases:
        for word in phrase.split(" "):
            for index, letter in enumerate(word):
                last_letter_is_alpha = False
                next_letter_is_alpha = False

                if index > 0:
                    last_letter_is_alpha = word[index - 1].isalpha()

                if index < len(word) - 1:
                    next_letter_is_alpha = word[index + 1].isalpha()

                if last_letter_is_alpha and letter == "(":
                    treated_text += " "

                treated_text += letter
                
                if next_letter_is_alpha and letter == ")":
                    treated_text += " "

            treated_text += " "

        treated_text = treated_text.rstrip() + "\n"

    braille = ""
    phrases = treated_text.split("\n")
    for phrase in phrases:
        for word in phrase.split(" "):
            try:
                is_number = word[0].isnumeric()
                if is_number:
                    braille += "⠼"

                is_upper_case = word.isupper()
                if not is_number and is_upper_case:
                    braille += "⠨⠨"

                last_letter = None
                for letter in word:
                    index_of_letter = alphabets.Brazilian.normal.index(letter.lower())

                    if not is_number and letter.isnumeric():
                        braille += "⠼"
                    
                    if letter.isupper() and not is_upper_case:
                        braille += "⠨"

                    if last_letter:
                        if last_letter.isnumeric() and letter.isalpha():
                            braille += "⠂"

                    braille += alphabets.Brazilian.braille[index_of_letter]
                    last_letter = letter
                braille += " "
            except:
                pass

        braille = braille.rstrip() + "\n"

    return braille.rstrip().replace(" ", "⠀")