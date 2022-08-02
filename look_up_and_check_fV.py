import urllib.request
import urllib.parse
import os
import download_and_save_pdf as PDF_s

pdf_path_1 = "https://www.fakturowo.pl/pobierz?api_id=<ID>&api_numer={}"
pdf_path = "https://www.fakturowo.pl/api?api_id=<ID>&api_zadanie=3&p={}"
dir_path = '/samba/main/<DIR>'
print(dir_path)
fV_id = []
id_api = []

def parse_date_from_id(f):
    f_t = f.split('/')
    l = len(f_t)
    return str(f_t[l-2]) + "_" + str(f_t[l-1])

def check_dir(f):
    dir = os.listdir(dir_path)
    dirName = dir_path + "/" + str(f)
    if f.replace("/", "_") not in dir:
        try:
            # Create target Directory
            os.mkdir(dirName)
            print("Directory ", dirName, " Created ")
        except FileExistsError:
            print("Directory ", dirName, " already exists")
    return dirName

def do_exist_fV_on_path(f, dir):
    f_t = f.replace("/", "_")
    dir_t = os.listdir(dir)
    if str(f_t + ".pdf") not in dir_t:
        #print("file not exists " + f_t)
        return 0
    else:
        #print("file exists " + f_t)
        return 1

def list_id_f(fV_id):
    i = 0
    for fv in fV_id:
        #print(parse_date_from_id(fv))
        dir_dest = check_dir(parse_date_from_id(fv))
        if not (do_exist_fV_on_path(fv, dir_dest)):
            fv_t = fv.replace("/", "_")
            if PDF_s.download_file(pdf_path_1.format(id_api[i]), (dir_dest + "/" + fv_t)):
                print("File ", fv_t, " has been copied ")
        i = i + 1

def remove_tags(line):
    return line.decode("utf-8")


def how_many_pages():
    with urllib.request.urlopen(pdf_path.format(1)) as response:
        html = response.read()
    html = html.split(b'\n')
    return int(remove_tags(html[1]))


def put_Fv_to_var(id):
    fV_id.append(id)

def put_api_to_var(api):
    id_api.append(api)

def parse_api_response():

    pages = how_many_pages()
    for page in range(pages):
        with urllib.request.urlopen(pdf_path.format(str(page+1))) as response:
            html = response.read().split(b'\n')
            n_line = 1
            for line in html:
                if n_line < 3:
                    n_line = n_line + 1
                    continue
                else:
                    #print(urllib.parse.unquote(line.decode("utf-8", errors='ignore')))
                    id_fV = (line.decode("utf-8", errors='ignore')).split(';')
                    put_Fv_to_var(id_fV[2])
                    put_api_to_var(id_fV[0])

parse_api_response()
list_id_f(fV_id)

#for fv in fV_id:
#    print(fv)
#i=1
#for line in html:
#
#    print(str(i) + "  " + str(line))
#    i = i+1






