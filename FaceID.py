import cv2
import os,glob
from numpy import asarray

#傳入名字，打開攝影機，訓練自己的臉部資料(200 張)，正常結束後會回傳 True，撞到名字會回傳 False
def sign_up(name:str,frame)->bool:
    if not os.path.exists("images"):
        os.makedirs("images")
    #撞到名字
    if os.path.isdir("images/"+name):
        print("此名字已存在")
        return False
    
    index=1
    total=150

    os.mkdir("images/"+name)
    face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_alt2.xml")
    while index>0:
        frame=cv2.flip(frame,1)
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=face_cascade.detectMultiScale(gray,1.1,3)
        for (x,y,w,h) in faces:
            frame=cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
            image=cv2.resize(gray[y:y+h,x:x+w],(400,400))
            __saveImg(image,index,name)
            index+=1
            if index>total:
                print("完成拍攝，關閉相機")
                index=-1
                break
        cv2.waitKey(1)

    images=[]
    labels=[]
    labelstr=[]
    count=0
    dirs=os.listdir("images")
    for d in dirs:
        if os.path.isdir("images/"+d):
            files=glob.glob("images/"+d+"/*.jpg")
            for filename in files:
                img=cv2.imread(filename,cv2.COLOR_BGR2GRAY)
                images.append(img)
                labels.append(count)
            labelstr.append(d)
            count+=1

    f=open("member.txt",'w')
    f.write(','.join(labelstr))
    f.close()

    model=cv2.face.LBPHFaceRecognizer_create()
    model.train(asarray(images),asarray(labels))
    model.save("faces_LBPH.yml")
    print("模型訓練完成")
    return True

#辨識攝影機前的人是誰，會回傳辨識出來的人名，否則回傳 False
def identify(frame)->str:
    if not os.path.exists("images"):
        os.makedirs("images")
    if not os.path.exists("faces_LBPH.yml") or not os.path.exists("member.txt"):
        return False
    model=cv2.face.LBPHFaceRecognizer_create()
    model.read("faces_LBPH.yml")
    f=open("member.txt",'r')
    names=f.readline().split(',')

    face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_alt2.xml")

    img=frame
    cv2.imwrite("images/tem.jpg",img)

    img=cv2.imread("images/tem.jpg")
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(gray,1.1,3)
    for (x,y,w,h) in faces:
        img=cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
        face_img=cv2.resize(gray[y:y+h,x:x+w],(400,400))
        try:
            val=model.predict(face_img)
            if val[1]<50:
                print("辨識結果： "+names[val[0]],val[1])
                return names[val[0]]
            else:
                print("無法辨識",val[1])
                return False
        except:
            print("ERROR!!! 錯誤！！！")
            return False
    return False

def __saveImg(image,index,name):
    filename="images/"+name+"/face{:03d}.jpg".format(index)
    cv2.imwrite(filename,image)