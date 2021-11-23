class Rotor:
    wirings = [["EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"],    # I + notch
               ["AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"],    # II
               ["BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"],    # III
               ["ESOVPZJAYQUIRHXLNFTGKDCMWB", "J"],    # IV
               ["VZBRGITYUPSDNHLXAWMJQOFECK", "Z"]]    # V

    def __init__(self, number, start_letter):
        self.rotations = ord(start_letter) - 65
        self.number = number    # rotor I, II, etc.
        self.wiring = Rotor.wirings[self.number-1][0]
        self.notch = Rotor.wirings[self.number-1][1]

    def rotate(self):
        self.rotations = (self.rotations + 1) % 26

    def get_letter(self, letter):
        letter_num = ord(letter) - 65   # A=0, B=1 ...
        return self.wiring[(letter_num + self.rotations) % 26]

    def get_letter_reversed(self, letter):
        # get the position of given letter in this rotor's wiring
        for index, char in enumerate(self.wiring):
            if char == letter.upper():
                letter_index = (index - self.rotations) % 26    # take into account the rotation of rotor
                return chr(letter_index + 65)   # return character of the position of the given letter in the wiring


def reflector_get_letter(letter):
    wiring = "YRUHQSLDPXNGOKMIEBFZCWVJAT"   # German Army & Air force UKW-B (reflector-B) wiring
    letter_num = ord(letter) - 65  # A=0, B=1 ...
    return wiring[letter_num]


rotors = [Rotor(3, "A"), Rotor(2, "A"), Rotor(1, "A")]  # displayed backwards ie. I II III
total_rotations = 0
double_step = False
show_details = False


def rotate_rotors():
    global total_rotations, double_step
    rotors[0].rotate()  # rotate 1st rotor
    if chr(rotors[0].rotations+65) == chr(ord(rotors[0].notch)+1):
        rotors[1].rotate()  # rotate 2nd rotor

        if chr(rotors[1].rotations+65) == chr(ord(rotors[1].notch)+1):
            rotors[2].rotate()  # rotate 3rd rotor

    if chr(rotors[1].rotations+65) == rotors[1].notch and not double_step:
        double_step = True

    elif double_step:
        rotors[1].rotate()
        rotors[2].rotate()
        double_step = False

    total_rotations += 1


def check_plugs(letter, plugs):
    for plug in plugs:
        if letter in plug:
            if letter == plug[0]:
                letter = plug[1]
            else:
                letter = plug[0]
    return letter


def keep_alpha(ascii_code):
    if ascii_code>90:
        return chr((ascii_code - 65) % 26 + 65)
    else:
        return chr(ascii_code)


def generate_letter(letter):
    rotate_rotors()
    l1 = rotors[0].get_letter(letter)
    l2 = rotors[1].get_letter(chr(ord(l1) - rotors[0].rotations))
    l3 = rotors[2].get_letter(chr(ord(l2) - rotors[1].rotations))
    l4 = reflector_get_letter(chr(ord(l3) - rotors[2].rotations))
    l5 = rotors[2].get_letter_reversed(keep_alpha(ord(l4) + rotors[2].rotations))
    l6 = rotors[1].get_letter_reversed(keep_alpha(ord(l5) + rotors[1].rotations))
    l7 = rotors[0].get_letter_reversed(keep_alpha(ord(l6) + rotors[0].rotations))

    if show_details:
        print("Rotor positions:", chr(rotors[2].rotations+65), chr(rotors[1].rotations+65), chr(rotors[0].rotations+65))
        print("1st encoding: ", l1)
        print("2nd encoding: ", l2)
        print("3rd encoding: ", l3)
        print("reflector encoding: ", l4)
        print("4th encoding: ", l5)
        print("5th encoding: ", l6)
        print("6th encoding: ", l7, "\n")
    return check_plugs(l7, plugs)


def set_rotor(i):
    r1 = input(f"Enter number of rotor (1-5) in slot {i+1}: ")
    p1 = input(f"Enter position of rotor in slot {i+1} (A-Z): ")

    if not r1.isnumeric() or int(r1) < 1 or int(r1) > 5 or not p1.isalpha() or len(p1) != 1:
        print("Invalid input. Repeating...\n")
        set_rotor(i)
    elif (i != 0 and rotors[i-1].number == int(r1)) or (i != 0 and rotors[i-2].number == int(r1)):
        print("That rotor has already been used. Repeating...\n")
        set_rotor(i)
    else:
        print("Using rotor with wirings:", rotors[i].wiring)
        rotors[i] = Rotor(int(r1), p1.upper())


plugs = []

print("The Enigma I simulator. Enter \\I for instructions.")

while True:
    entered_string = input().upper()

    if entered_string == "\\I":
        print("="*3, "Instructions", "="*3,
              "\nThe Enigma machine uses rotors and plugs to encipher plaintext to ciphertext."
              "\nYou can decode messages by making sure your machine uses the same settings as the one that created the"
              " ciphertext."
              "\nYou can enter multiple letters in one line or enter letters on individual lines. It doesn't matter."
              "\nEverything is case-insensitive."
              "\nTo select rotors and their positions, enter \\R"
              "\nTo select the placement of plugs, enter \\P. Only 10 plugs are available."
              "\nTo reset plugs, enter \\RP"
              "\nTo show details of each encoding, enter \\SD"
              "\nTo quit, enter \\Q")

    elif entered_string == "\\R":
        print("Slots go from right to left (slot 1 is right-most rotor)")
        for i in range(len(rotors)):
            set_rotor(i)

    elif entered_string == "\\P":
        if plugs:  # show all plugs
            print("Current plugs:")
            for plug in plugs:
                print(f"{plug[0]}-{plug[1]}")

        connections = input("Enter letters to connect (in form A-B,C-D,E-F...). 10 plugs max: ").upper().replace(" ", "").split(",")
        connections = [c.split("-") for c in connections]
        invalid = False
        for c in connections:
            if len(c) == 2 and "".join(c).isalpha():
                c.sort()  # arrange letters in each plug alphabetically
            else:
                invalid = True
                print("Invalid input. Enter connection in form 'A-B,C-D,E-F...' next time")
                break

            # check for repeated letters
            for letter in c:
                for plug in plugs:
                    if letter in plug:
                        invalid = True
                        print(f"Invalid: Letter '{letter}' is already in use.")
                        break

        if not invalid:
            if len(plugs) + len(connections) <= 10:
                plugs += connections
            else:
                print("Invalid: That is too many plugs. You can reset plugs with \\PR")

    elif entered_string == "\\PR":
        print("Removing all plugs...")
        plugs.clear()

    elif entered_string == "\\SD":
        print("Show details mode toggled.")
        show_details = not show_details

    elif entered_string == "\\Q":
        break

    else:
        output = []
        show_warning = False
        for char in entered_string:
            if char.isalpha():
                swapped_char = check_plugs(char, plugs)
                output.append(generate_letter(swapped_char))
            else:
                show_warning = True
        if show_warning:
            print("Ignoring non-alphabetical characters:")
        string_out = "".join(output)
        print(" ".join(string_out[i:i+5] for i in range(0, len(string_out), 5)))  # print output as string
