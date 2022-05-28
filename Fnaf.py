import pyautogui
import cv2
import tkinter as tk


answer = 'n'#input("Test mode? Y or N? ")
test = False
if str.lower(answer) == 'y':
    test = True

Sizes = [0.5,1,0.5,1]
#Sizes.append(float(input("Door 1 X: "))); Sizes.append(float(input("Door 1 Y: ")))
#Sizes.append(float(input("Door 2 X: "))); Sizes.append(float(input("Door 2 Y: ")))
#Sizes.append(float(input("Light 1 X: "))); Sizes.append(float(input("Light 1 Y: ")))
#Sizes.append(float(input("Light 2 X: "))); Sizes.append(float(input("Light 2 Y: ")))
#Sizes.append(float(input("Tablet X: "))); Sizes.append(float(input("Tablet Y: ")))

num = 0
for i in Sizes:
    if (1 - Sizes[num]) < 0.5 and Sizes[num] != 1:
        Sizes[num] = 1 - Sizes[num]
    Pieces = int(1/Sizes[num])

    if Pieces > 1:
        for j in range(1, Pieces + 1):
            print("Section {0} ".format(j), end='')
            if j == Pieces - 1: print("or ", end='')
        Sizes[num] = [int(input(" ")),Pieces]
    elif Pieces < 1:
        intp = int(input("Section 1 or 2? "))
        if intp == 1:
            Sizes[num] = [i, 1]
        elif intp == 2:
            Sizes[num] = [1 - i, 1]
    else:
        Sizes[num] = [1, 1]
    num += 1
if test: print(Sizes)

def CheckLight():
    variables = []
    pyautogui.screenshot('screen.png')
    greyimage = cv2.imread('screen.png',0)
    size = greyimage.shape

    for i in range(0, len(Sizes), 2):
        #Sizes = Which Piece, # of Pieces
        X_Piece = Sizes[i][0]
        Y_Piece = Sizes[i + 1][0]
        X_NumPiece = Sizes[i][1]  
        Y_NumPiece = Sizes[i+1][1]
        
        res_X = int(1/X_NumPiece * size[1])
        res_Y = int(1/Y_NumPiece * size[0])
        res = res_X * res_Y

        X = int(size[1] * ((X_Piece-1)/X_NumPiece))
        Y = int(size[0] * ((Y_Piece-1)/Y_NumPiece))
        img = greyimage[Y:(res_Y + Y), X:(res_X + X)]
        (thresh, blackAndWhiteImage) = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        #cv2.imshow("cropped", blackAndWhiteImage); cv2.waitKey(0)

        white = cv2.countNonZero(blackAndWhiteImage)
        black = res - white
        if test: print("White:{0}. Black:{1}.".format(white,black), end=' ')
        if white > black:
            if test: print("White," + str(white), end=' ')
            variables.append(True)
        else:
            if test: print("Black," + str(black), end=' ')
            variables.append(False)
        if test: print("On{0}={1}".format(i//2, variables[i]), flush=True)
    return variables

def FurtherTime(sec, Power, Drain):
    new_sec = sec + (2**Drain)
    new_Power = Power
    Power_Change = False
    if new_sec == 96:
        new_Power -= 1
        new_sec = 0
        Power_Change = True
    return (new_sec, new_Power, Power_Change)

window = tk.Tk()
window.overrideredirect(True)
window.attributes('-topmost', 1)


Power = 100
m_second = 0
if test: print("Power Left:100%")
powerOutput = tk.Label(window, text="Power Left: {0}%".format(Power), fg="white", bg="black", font=("System", 26))
powerOutput.pack()
screen_height = window.winfo_screenheight()
screen_width = window.winfo_screenwidth()
window.update_idletasks()
window.update()
posX = int(screen_width - window.winfo_width())
posY = 0
window.geometry(f'+{posX}+{posY}')
window.update_idletasks()
window.update()
pastWidth = window.winfo_width()

while (1):
    switches = CheckLight()
    Drain_Speed = 0
    for i in range(len(switches)):
        Drain_Speed += int(switches[i])
    (m_second, Power, PowerChange) = FurtherTime(m_second, Power, Drain_Speed)
    if PowerChange: 
        if test: print("Power Left: {0}%".format(Power))
        PowerChange = False
        powerOutput.destroy()
        powerOutput = tk.Label(window, text="Power Left: {0}%".format(Power), fg="white", bg="black", font=("System", 26))
        powerOutput.pack()
        window.update_idletasks()
        window.update()
        if(window.winfo_width() != pastWidth): 
            posX = int(screen_width - window.winfo_width())
            window.geometry(f'+{posX}+0')
            window.update_idletasks()
            window.update()
            pastWidth = window.winfo_width()