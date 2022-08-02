import json
import urllib.request
import urllib.parse
import json
import requests
import xml.etree.ElementTree as ET
from redminelib import Redmine

redmine = Redmine('http://<REDMINE IP>/redmine', username='<bot user>', password='<password>')
project = redmine.project.get('montaze-2')
issue = redmine.issue

pdf_path = "https://www.fakturowo.pl/api?api_id=<ID>&api_zadanie=3&p={}"
api_request = "http://<REDMINE IP>/redmine/issues.xml?&project_id=11&status_id=25&key=<REDMINE KEY>"
api_request_2 = "http://<REDMINE IP>/redmine/issues/{}.json?&key=<REDMINE KEY>"
header_api = {"Content-Type": "application/json", "X-Redmine-API-Key": "<REDMINE KEY>"}
params_d = {'header': header_api}
json_req = {
    "issue": {
        "subject": "Example"
    }
}

fv_paid = []

def  update_redmine_issue(id_issue):
    i = issue.update(id_issue, status_id=24)
    print(i)


def read_issues(api_request):
    response = requests.get(api_request)
    return response.text

data = read_issues(api_request)

root = ET.fromstring(data)
def parse_FV_from_field(filed):
    f_out = []
    f_t = filed.split(';')
    for i in f_t:
        if not i.strip() in ["None", ""]:
            f_out.append(i.strip())
    return f_out

def remove_tags(line):
    return line.decode("utf-8")

def how_many_pages():
    with urllib.request.urlopen(pdf_path.format(1)) as response:
        html = response.read()
    html = html.split(b'\n')
    return int(remove_tags(html[1]))

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
                    #print(id_fV)
                    if id_fV[16] == "1":
                        fv_paid.append(id_fV[2])
                    #put_Fv_to_var(id_fV[2])
                    #put_api_to_var(id_fV[0])

def compare_fv_in_FV_api(fv_array, id_issue):
    f_pay = 0
    f_len = len(fv_array)
    if f_len == 0:
        return 0

    #print(id_issue)
    #print(fv_array)


    for f in fv_array:
        if f in fv_paid:
            f_pay = f_pay + 1

    if f_pay < f_len:
        print(id_issue + " not paid")

    else:
        print(id_issue + " paid")
        update_redmine_issue(id_issue)

parse_api_response()

for table in root.iter('issue'):
    id_issue = 0
    for child in table:
        if child.tag == "id":
            id_issue = child.text
            #print(id_issue)
        #print(child.tag)
        if child.tag == "custom_fields":
            for cf in child.iter('custom_field'):
                if cf.attrib['id'] == "27":
                    for fv in cf:
                        compare_fv_in_FV_api(parse_FV_from_field(str(fv.text)), id_issue)



        #print(child.tag, child.attrib)
        #print(child.text)


#print(tree)