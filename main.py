from Tkinter import *
import os
import datetime
import qrtools #https://github.com/primetang/qrtools GNU GPL v3.0
#coding:utf8

cwd = os.getcwd()

names = {}
date = datetime.datetime.now().strftime("%B %d, %Y")

class QR_Attendance(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        self.initUI()

    def initUI(self):
        self.pack()
        Label(self, text='QR Attendance', font='Helvetica 20', height=2, background='green').grid(columnspan=5,stick = W+E+N+S)
        self.names_list = Listbox(self, width=60, height=12)
        self.names_list.grid(pady=5, padx = 5, stick=W, rowspan=2)
        Button(self, text = "START SCAN", font='bold', command=self.scanner).grid(row=1, column=1, padx=10)
        Button(self, text = 'Save', font='bold', command=self.save_to_file).grid(row=2, column=1)

    def scanner(self):
        import cv2
        cv2.namedWindow("webcam")
        vc = cv2.VideoCapture(0)

        if vc.isOpened():
            rval,frame = vc.read()
        else:
            rval=False
        display_text='N/A'
        while rval:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.putText(gray, display_text, (15, 460), cv2.FONT_HERSHEY_PLAIN, 2, 255, 2)
            cv2.imshow("webcam", gray)
            cv2.imwrite('test.png', gray)
            qr = qrtools.QR()
            qr.decode('test.png')
            the_text = qr.data.strip().encode('utf-8')
            if the_text != 'NULL':
                display_text = the_text
                names[the_text] = 'Signed in'
            rval, frame = vc.read()
            key = cv2.waitKey(20)
            if key == 27:
                break
        vc.release()
        cv2.destroyWindow("webcam")
        for name in names:
            self.names_list.insert(END, name)

    def save_to_file(self):
        txtfile = open('names.txt', 'w')
        txtfile.write(date + '\n')
        for name in names:
            txtfile.write(name+'\n')

def main():
    root = Tk()
    root.title("QR Attendance")
    QR_Attendance(root)
    root.mainloop()
main()
