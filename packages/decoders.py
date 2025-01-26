from packages import alphabets



def northAmerican(braille):
    text = ""
    phrases = braille.split("\n")
    for phrase in phrases:
        words = phrase.replace('"', "'").split(" ")
        for word in words:
            for letter in word:
                try:
                    index_of_letter = alphabets.NorthAmerican.braille.index(letter)
                    text += alphabets.NorthAmerican.normal[index_of_letter]
                except:
                    pass
            text += " "

        text = text.rstrip() + "\n"

    return text.rstrip()



def brazilian(braille):
    text = ""
    phrases = braille.split("\n")
    for phrase in phrases:
        for word in phrase.split("⠀"):
            try:
                treated_word = word

                is_number = word[0] == "⠼"
                if is_number:
                    treated_word = treated_word[1:]

                if word.startswith("⠣⠄"):
                    text += "("
                    treated_word = treated_word[2:]

                if word.startswith("⠷⠄"):
                    text += "["
                    treated_word = treated_word[2:]

                if word.endswith("⠄⠜"):
                    treated_word = treated_word[:-2]

                if word.endswith("⠄⠾"):
                    treated_word = treated_word[:-2]

                is_upper_case = False
                if not is_number and word.startswith("⠨⠨"):
                    is_upper_case = True
                    treated_word = treated_word[2:]

                last_letter = None
                for letter in treated_word:
                    if letter == "⠠" or letter == "⠨":
                        continue

                    if letter == "⠂" and last_letter == "⠠":
                        text += "/"
                        continue

                    if letter == "⠴" and last_letter == "⠸":
                        text += "%"
                        continue

                    if is_number and letter == "⠂":
                        is_number = False
                        continue
                    
                    index_of_letter = -1
                    try:
                        index_of_letter = alphabets.Brazilian.braille.index(letter)
                    except:
                        last_letter = letter
                        continue

                    if is_number:
                        index_of_letter = (alphabets.Brazilian.braille[38:]).index(letter) + 38
                    
                    if is_upper_case or last_letter == "⠨":
                        text += alphabets.Brazilian.normal[index_of_letter].upper()
                    else:
                        text += alphabets.Brazilian.normal[index_of_letter]

                    last_letter = letter

                if word.endswith("⠄⠜"):
                    text += ")"

                if word.endswith("⠄⠾"):
                    text += "]"

            except:
                pass
            
            text += " "

        text = text.rstrip() + "\n"

    return text.rstrip()