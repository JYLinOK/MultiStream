from platform import release
import cv2
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import tkinter.ttk
import tkinter.messagebox
import subprocess
import time
import json 

# __________________________________________________________________________________________________
# Global Variables
listbox_media_select = 0
listbox_camera_select = 0
media_cameras_dict = {}
json_path = './media/media.json'
stream_config = {}
stream_config_path = './config/plugflow.json'
cameras_able = []
previous_cameras_able = []
release_cap = []
# __________________________________________________________________________________________________
# Functions
# __________________________________________________________________________________________________
def get_the_cameras_num():
    global cameras_able

    i = 0
    cameras_able = []
    still_has_camera = True

    while(still_has_camera):
        cap_i = cv2.VideoCapture(i)
        ref, frame = cap_i.read()
        if ref:
            cameras_able.append(i)
        else:
            still_has_camera = False
            
        i += 1
    return cameras_able



# __________________________________________________________________________________________________
def get_camera_image(cap, image_width, image_height):
    ref, frame = cap.read()
    frame = cv2.flip(frame, 1) 
    cvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    pilImage = Image.fromarray(cvimage)
    pilImage = pilImage.resize((image_width, image_height),Image.ANTIALIAS)
    tkImage =  ImageTk.PhotoImage(image=pilImage)
    return tkImage



# __________________________________________________________________________________________________
def testBtn():
    print('testBtn')



# __________________________________________________________________________________________________
def get_index(i, len_cams):
    index_str = ''
    if len_cams > 1:
        if i == 0:
            index_str = ''
        else:
            index_str = str(i+1)
    else:
        if i == 0:
            index_str = ''
    return index_str



# ==================================================================================================
# media_class = 'video' or 'audio'
def medai_names():
    code = "ffmpeg -list_devices true -f dshow -i dummy"
    a = subprocess.Popen(code, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8")
    str_a = a.stdout.read()

    split_sign = "\""
    media_result = []

    sum = 0
    while (str_a.find(split_sign) != -1) and sum < 100:
        sum += 1
        start_index = str_a.find(split_sign)
        end_index = str_a[start_index+1:].find(split_sign)
        end_index = start_index+end_index
        item_str = str_a[start_index+1:end_index+1]
        if item_str[0:1] != '\n' and item_str[0:1] != '@' and item_str != '':
            media_result.append(item_str)
        str_a = str_a[end_index+2:len(str_a)-1]
    return media_result
    

# ==================================================================================================
# ==================================================================================================
def plugFlow(i, len_cams):
    global json_path
    global media_cameras_dict
    global stream_config
    global stream_config_path
    global cameras_able

    with open(json_path, 'r', encoding='utf-8') as f:
        f_dict = json.load(f)
        if f_dict != {}: media_cameras_dict = f_dict
    
    with open(stream_config_path, 'r', encoding='utf-8') as f:
        f_dict = json.load(f)
        if f_dict != {}: stream_config = f_dict

    # print('plugFlow ', i)
    entry_str = frame2.children['!entry'+get_index(i, len_cams)].get()
    entry_str = entry_str.strip()
    # print(f'{type(i) = }')
    # print(f'{entry_str = }')
    # print(f'{media_cameras_dict = }')
    print(f'\n{media_cameras_dict[str(i)] = }')
    print(f'{stream_config = }')

    code = ''
    a = ''
    if 'udp' in entry_str:
        stream_url = entry_str
        stream_config = stream_config['udp']
        code = a + "ffmpeg -rtbufsize " + stream_config['rtbufsize'] + " -re -f dshow -i video=\"" + \
                media_cameras_dict[str(i)] + "\"" + " -framerate " + stream_config['framerate'] +  \
                " -bufsize " + stream_config['bufsize'] + " -vcodec " + stream_config['vcodec'] + \
                    " -preset:" + stream_config['preset'] + " -tune:" + stream_config['tune'] + \
                        " -f " + stream_config['f'] + " -max_delay " + stream_config['max_delay'] + \
                            " -g " + stream_config['g'] + " -b:" + stream_config['b'] + " " + stream_url
        
    elif 'rtp' in entry_str:
        stream_url = entry_str
        stream_config = stream_config['rtp']
        code = a + "ffmpeg -rtbufsize " + stream_config['rtbufsize'] + " -re -f dshow -i video=\"" + \
                media_cameras_dict[str(i)] + "\"" + " -framerate " + stream_config['framerate'] +  \
                " -bufsize " + stream_config['bufsize'] + " -vcodec " + stream_config['vcodec'] + \
                    " -preset:" + stream_config['preset'] + " -tune:" + stream_config['tune'] + \
                        " -f " + stream_config['f'] + " -max_delay " + stream_config['max_delay'] + \
                            " -g " + stream_config['g'] + " -b:" + stream_config['b'] + " " + stream_url
    
    elif 'tcp' in entry_str:
        stream_url = entry_str
        stream_config = stream_config['tcp']
        code = a + "ffmpeg -rtbufsize " + stream_config['rtbufsize'] + " -re -f dshow -i video=\"" + \
                media_cameras_dict[str(i)] + "\"" + " -framerate " + stream_config['framerate'] +  \
                " -bufsize " + stream_config['bufsize'] + " -vcodec " + stream_config['vcodec'] + \
                    " -preset:" + stream_config['preset'] + " -tune:" + stream_config['tune'] + \
                        " -f " + stream_config['f'] + " -max_delay " + stream_config['max_delay'] + \
                            " -g " + stream_config['g'] + " -b:" + stream_config['b'] + " " + stream_url

    

    print(f'\n{code = }')
    print(f'\n{cameras_able = }')

    if i in cameras_able:
        global release_cap
        if i not in release_cap:
            del cameras_able[cameras_able.index(i)]
            print(f'\ndelete {cameras_able = }')
            time.sleep(1)

        release_cap.append(i)
    else:
        print('Camera not found.')

    subprocess.Popen(code)
    


# ==================================================================================================
# __________________________________________________________________________________________________
def scroll_bar(value):
    print(f'{value = }')
    print(f'{type(value) = }')
    # d = frame2.place_info()
    # print(f'{d = }')
    # print(f'{type(d) = }')
    frame2.place(x=20, y=-int(value))



# __________________________________________________________________________________________________
def showCamWins(option):
    global cameras_able
    global previous_cameras_able

    if len(cameras_able) > 0:
        show_cameras = []
        if option == 'all':
            show_cameras = previous_cameras_able
        elif option == 'now':
            show_cameras = cameras_able

        progressLoading.pack()
        progressLoading['value'] = 10
        frame1.update()

        canvas_dict = {}
        len_show_cameras = len(show_cameras)

        if len_show_cameras == 1:
            image_width_local = int(screenwidth*0.8)
            image_height_local = int(screenheight*0.7)

        else:
            image_width_local = image_width
            image_height_local = image_height

        for i in show_cameras:
            canvas = Canvas(frame2, bg = 'white', width=image_width_local, height=image_height_local) 
            label = Label(frame2, text = 'video '+str(i), bg='white', font=("consle", 16), width=int(image_width/20), height=1)
            entry = Entry(frame2, width=int(image_width/10))
            button = Button(frame2, text = 'plug flow '+str(i)+'->', command=lambda index=i, len_cams=len_show_cameras:plugFlow(index, len_cams))

            # _______________________________________________________________________________
            canvas_dict['canvas'+str(i)] = canvas

            row_i = int(i / column)
            column_i = i % column

            unit = 4
            initial = 1
            label.grid(row=row_i*unit+initial, column=column_i, padx=padx_box, pady=pady_box) 
            canvas.grid(row=row_i*unit+initial+1, column=column_i , padx=padx_box, pady=pady_box) 
            button.grid(row=row_i*unit+initial+2, column=column_i , padx=padx_box, pady=pady_box) 
            entry.grid(row=row_i*unit+initial+3, column=column_i , padx=padx_box, pady=pady_box) 
                # _______________________________________________________________________________

                # progressLoading['value'] = int((i/len(show_cameras))/2)

        for i in range(10):
            time.sleep(0.05)
            progressLoading['value'] = 10*i
            frame1.update()


        cap_dict = {}
        for i in show_cameras:
            # progressLoading['value'] += int(30/len_cam)
            # frame1.update()
            cap_dict['cap'+str(i)] = cv2.VideoCapture(i)
        # print('cap_dict = ', cap_dict)
        # print('code = \n', cade_c)

        progressLoading['value'] = 90
        frame1.update()
        time.sleep(0.2)

        # print("progressLoading['value'] = ", progressLoading['value'])
        # ___________________________________
        # ___________________________________
        progressLoading['value'] = 100
        frame1.update()

        progressLoading.pack_forget()
        # entry_inividual.pack_forget()
        # button_flow.pack_forget()
        frame3.pack_forget()
        # ___________________________________
        # ___________________________________

        while True:
            global release_cap
            if len(release_cap) > 0:
                for item in cap_dict:
                    item_i = int(item[item.index('p')+1:])
                    if item_i in release_cap:
                        cap = cap_dict['cap'+str(item_i)]
                        if cap.isOpened():
                            cap.release()

            if len(cap_dict) > 0:
                cade_c = cameras_code(cameras_able)
                exec(str(cade_c))
                root_window.update()
                root_window.after(1)
    else:
        cv2.destroyAllWindows()


# __________________________________________________________________________________________________
def showChirldren():
    print('root_window.children = ', root_window.children)
    # root_window.children['!label']['text'] = "Text updated"


# __________________________________________________________________________________________________
def cameras_code(code_cameras):
    code = ''
    canvas_i_name = '!canvas'
    root_box = 'frame2'

    # print('code_cameras = ', code_cameras)

    if len(code_cameras) > 1:
        for i in code_cameras:
            if i == 0:
                canvas_i_name = '!canvas'
            else:
                canvas_i_name = '!canvas' + str(i+1)

            str_i = "img" + str(i) + " = get_camera_image(cap_dict['cap'+str(" + str(i) + ")], image_width_local, image_height_local)" + \
            "\n" + root_box + ".children['" + canvas_i_name + "'].create_image(0, 0, anchor='nw', image=" + "img" + str(i) +")"
            code += str_i + '\n'

    else:
        i = code_cameras[0]
        canvas_i_name = '!canvas'
        str_i = "img" + str(i) + " = get_camera_image(cap_dict['cap'+str(" + str(i) + ")], image_width_local, image_height_local)" + \
        "\n" + root_box + ".children['" + canvas_i_name + "'].create_image(0, 0, anchor='nw', image=" + "img" + str(i) +")"
        code = str_i

    return code


# __________________________________________________________________________________________________
def list_media():
    print('list_media')
    global json_path
    global media_cameras_dict

    frameMadia.place(x=screenwidth*0.1, y=50, width=screenwidth*0.8, height=screenheight*0.8)
    video_set = medai_names()

    show_str = ''
    for item in video_set:
        show_str += item + '\n'
    text_cameras.delete(0.0, tkinter.END)
    text_cameras.insert(INSERT, show_str)
    text_cameras.place(x=screenwidth*0.1, y=20, height=screenheight*0.3, width=screenwidth*0.6)
    
    listbox_media.place(x=screenwidth*0.1, y=screenheight*0.38, width=screenwidth*0.2)
    select_media_btn.place(x=screenwidth*0.19, y=screenheight*0.34)
    
    listbox_cameras.place(x=screenwidth*0.31, y=screenheight*0.38, width=screenwidth*0.1)
    select_camera_btn.place(x=screenwidth*0.35, y=screenheight*0.34)

    # button_media.place(x=screenwidth*0.415, y=screenheight*0.46)
    btn_clear_media.place(x=screenwidth*0.415, y=screenheight*0.46)
    listbox_config.place(x=screenwidth*0.47, y=screenheight*0.38, width=screenwidth*0.23)

    media_list = medai_names()
    listbox_media.delete(0, tkinter.END)
    listbox_cameras.delete(0, tkinter.END)
    listbox_config.delete(0, tkinter.END)

    for i, item in enumerate(media_list):
        listbox_media.insert(i, item)
        listbox_cameras.insert(i, i)
    
    with open(json_path, 'r', encoding='utf-8') as f:
        f_dict = json.load(f)
        if f_dict != {}: media_cameras_dict = f_dict
        
    for i in media_cameras_dict:
        listbox_config.insert(i, 'camera ' + str(i) + ':  ' + media_cameras_dict[i])

    

# __________________________________________________________________________________________________
def select_media():
    print('select_media')
    global listbox_media_select
    a = listbox_media.curselection()
    # listbox_media.activate(a[0])
    if len(a) > 0:
        listbox_media_select = listbox_media.get(a[0])


# __________________________________________________________________________________________________
def select_camera():
    print('select_camera')
    global listbox_camera_select
    global listbox_media_select
    global media_cameras_dict
    a = listbox_cameras.curselection()

    # print(f'{type(listbox_camera_select) = }')
    # listbox_cameras.activate(a[0])
    if len(a) > 0:
        listbox_camera_select = listbox_cameras.get(a[0])
        media_cameras_dict[str(listbox_camera_select)] = listbox_media_select
        bind_media()


# __________________________________________________________________________________________________
def bind_media():
    print('bind_media')
    global listbox_media_select
    global listbox_camera_select
    global media_cameras_dict
    global json_path

    listbox_config.delete(0, tkinter.END)

    for i in media_cameras_dict:
        listbox_config.insert(i, 'camera ' + str(i) + ':  ' + media_cameras_dict[i])

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(media_cameras_dict, f, indent=2, ensure_ascii=False)



# __________________________________________________________________________________________________
def clear_media():
    print('clear_media')
    global media_cameras_dict
    global listbox_config
    global json_path

    media_cameras_dict.clear()
    listbox_config.delete(0, tkinter.END)

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({}, f)



# __________________________________________________________________________________________________
def close_media():
    print('close_media')
    text_cameras.place_forget()
    frameMadia.place_forget()


# __________________________________________________________________________________________________
def show_all():
    print('show_all')
    text_cameras.place_forget()
    frameMadia.place_forget()
    showCamWins('all')


# __________________________________________________________________________________________________
def show_one():
    print('show_one')
    text_cameras.place_forget()
    frameMadia.place_forget()
    frame3.pack(fill=X)



# __________________________________________________________________________________________________
def plug_one():
    global cameras_able
    print('plug_one')
    cameras = []
    if entry_inividual.get() != '':
        cameras.append(int(entry_inividual.get()))
    else:
        cameras = [0]
    print('cameras = ', cameras)
    cameras_able = cameras
    showCamWins('now')




# __________________________________________________________________________________________________
def close_all():
    global cameras_able
    print('close_all')
    cameras_able.clear()
    root_window.destroy()

    code = "python main.py"
    subprocess.Popen(code)



# __________________________________________________________________________________________________
def about():
    note = 'MultiSteam is a simple and fast multiple camera monitoring and streaming toolkit that supports the streaming of UDP, TCP and RTP for multiple cameras at the same time.'
    result = tk.messagebox.showinfo('About', note)



def t():
    pass



# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# Main Function
if __name__ == '__main__':
    # =========================================================================
    # =========================================================================
    # set the root window and name it
    root_window = tk.Tk()
    root_window.iconbitmap('./ydook.ico') 
    root_window.title('MultiStream')
    column = 3

    # get the size of the current screen:
    screenwidth = root_window.winfo_screenwidth()
    screenheight = root_window.winfo_screenheight()

    # Maxsize the window with the size of the screen
    root_window.geometry("%dx%d" %(screenwidth, screenheight))
    root_window.attributes("-topmost",True)
    

    # main menu
    mainmenu = Menu(root_window)
    # cameramenu menu
    cameramenu = Menu(mainmenu, tearoff=False)
    mainmenu.add_cascade(label="Camera", menu=cameramenu)
    cameramenu.add_command(label="Show All", command=show_all, accelerator="Ctrl+A")
    cameramenu.add_command(label="Show One", command=show_one, accelerator="Ctrl+O")
    cameramenu.add_command(label="Close All", command=close_all, accelerator="Ctrl+C")
    
    # media menu
    videomenu = Menu(mainmenu, tearoff=False)
    mainmenu.add_cascade(label="Meida", menu=videomenu)
    videomenu.add_command(label="List Media", command=list_media, accelerator="Ctrl+M")
    videomenu.add_command(label="Close Media", command=close_media, accelerator="Shift+M")
    
    # about menu
    aboutmenu = Menu(mainmenu, tearoff=False)
    mainmenu.add_cascade(label="About", menu=aboutmenu)
    aboutmenu.add_command(label="About MultiStream", command=about, accelerator="Ctrl+H")
    
    # load the main menu
    root_window.config(menu=mainmenu)


    # =========================================================================
    # New frame
    # frame1 = tk.Frame(root_window, bg='white', width=10, height=10)
    frame1 = tk.Frame(root_window, bg='white')
    frame1.place(x=0, y=0, relwidth=1)

    frame2 = tk.Frame(root_window, bg='azure')
    frame2.place(x=10, y=30, width=screenwidth-50)

    scale = Scale(root_window, from_=0, to=2*screenwidth-10, command=scroll_bar, resolution=5, length =200, sliderlength=20)
    scale.place(x=0, y=0, height=screenheight-100)


    progressLoading = tkinter.ttk.Progressbar(frame1, length=screenwidth/2)
    progressLoading.pack(side=TOP, fill=X, padx='100px')
    # maximum value
    progressLoading['maximum'] = 100
    # initial value
    progressLoading['value'] = 0
    progressLoading.pack_forget()

    # __________________________________________
    frame3 = tk.Frame(frame1, bg='ivory')
    frame3.pack(fill=X)

    entry_inividual = tk.Entry(frame3)
    entry_inividual.pack(padx=20, pady=6)
    button_flow = tk.Button(frame3, text="plug flow", command=plug_one)
    button_flow.pack(padx=20, pady=6)

    frame3.pack_forget()
    # __________________________________________


    # _________________________________________________________________________________________________
    # Media Configuration
    frameMadia = tk.Frame(root_window, bg='lightblue')

    text_cameras = Text(frameMadia, width=50, height=20, undo=True, autoseparators=False)
    listbox_media = Listbox(frameMadia, width=50, height=20, bg='lavender')
    select_media_btn = tk.Button(frameMadia, text="Select", command=select_media)

    listbox_cameras = Listbox(frameMadia, width=50, height=20, bg='linen')
    select_camera_btn = tk.Button(frameMadia, text="Select", command=select_camera)

    listbox_config = Listbox(frameMadia, width=50, height=20, bg='plum')
    # button_media = tk.Button(frameMadia, text="Bind >>", command=bind_media)
    btn_clear_media = tk.Button(frameMadia, text="<< Clear", command=clear_media)
    # _________________________________________________________________________________________________


    # =========================================================================
    # =========================================================================
    # Manually set the cameras_able
    # cameras_able = [0, 1]

    # Automaticly set the cameras_able
    previous_cameras_able = get_the_cameras_num()
    cameras_able = previous_cameras_able
    print('cameras_able = ', cameras_able)
    print('previous_cameras_able = ', previous_cameras_able)
    cameras_num = len(cameras_able)

    adjust = 0.7
    adjust_w_h = 0.6
    image_width = 0
    image_height = 0

    if cameras_num <= column:
        image_width = int((screenwidth * adjust) / cameras_num)
        image_height = int(image_width * adjust_w_h)
    else:
        image_width = int((screenwidth * adjust) / column)
        image_height = int(image_width * adjust_w_h)


    padx_box = (screenwidth * (1-adjust)) / (cameras_num * 2.5)
    # pady_box = (screenheight * (1-adjust)) / (cameras_num * 2)
    pady_box = 8




    # =========================================================================>>
    # =========================================================================>>
    # ___________________
    # ___________________
    # cap.release()
    root_window.mainloop()  
















