import subprocess


# # ==================================================================================================
# # media_class = 'video' or 'audio'
# def medai_names(media_class):
#     code = "ffmpeg -list_devices true -f dshow -i dummy"
#     a = subprocess.Popen(code, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8")
#     str_a = a.stdout.read()

#     split_sign = "\" (video)"
#     media_result = []
#     audio_name = "\" (audio)"
#     audio_result = []

#     while str_a.find(split_sign) != -1:
#         start_index = str_a.index("] \"")
#         end_index = str_a.index(split_sign)
#         media_result.append(str_a[start_index+3:end_index])
#         str_a = str_a[end_index+9:len(str_a)-1]
    
#     str_audio = str_a

#     while str_audio.find(audio_name) != -1:
#         start_index = str_audio.index("] \"")
#         end_index = str_audio.index(audio_name)
#         audio_result.append(str_audio[start_index+3:end_index])
#         str_audio = str_audio[end_index+9:len(str_audio)-1]

#     # print(f'{media_result = }')
#     # print(f'{audio_result = }')
    
#     if media_class == 'video':
#         return media_result
#     if media_class == 'audio':
#         return audio_result



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


a = medai_names()
print(f'{a = }')












