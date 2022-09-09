import pandas as pd
import requests
from bs4 import BeautifulSoup


URL = "https://www.sas.com/en_us/partners/find-a-partner.html#a-z"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
partners = soup.find_all("li", class_="listItem")
# print(len(partners))
# for partner in partners[118:]:
url_list = []
for partner in partners[118:-16]:
    url_list_dict = {}
    # print(partner, end="\n"*2)
    company_name = partner.find("span", class_="title")
    link_element = partner.find("a")
    url = link_element["href"]

    url_list_dict["Company Name"] = company_name.text.strip()
    url_list_dict["URL"] = url

    url_list.append(url_list_dict)

df = pd.DataFrame(url_list)



fields = []
# n_test = length
# print(length)
length = 50
start_ind = 1350
while start_ind < 1800:
    output = []
    print("start ind : ",start_ind)
    i = start_ind
    for dict_company in url_list[start_ind:start_ind+length]:
        output_dict = {}
        page = requests.get(dict_company["URL"])
        soup = BeautifulSoup(page.content, "html.parser")
        field_elements = soup.find_all("div", class_="text parbase section")
        # print(field_elements[30])
        i+=1
        try:
            output_dict["Name"] = field_elements[30].find("h3").text
            output_dict["Description"] = field_elements[30].find("p").text
            output_dict["Type"] = field_elements[32].find("p").text
            output_dict["Business Topic"]= field_elements[33].find("p").text
            output_dict["Geography"] = field_elements[34].find("p").text
            output_dict["Certifications"] = field_elements[35].find("p").text
            output_dict["Additional Experience"] = field_elements[36].find("p").text
            output_dict["Diversity"] = field_elements[37].find("p").text
            output_dict["Engagement Model"] = field_elements[38].find("p").text
            output_dict["Industries"] = field_elements[39].find("p").text
            output_dict["Languages"] = field_elements[40].find("p").text
            output_dict["URL"] = dict_company["URL"]
        except (AttributeError, IndexError) as e:
            output_dict["Name"] = dict_company["Company Name"]
            output_dict["Description"] = ""
            output_dict["Type"] = ""
            output_dict["Business Topic"]= ""
            output_dict["Geography"] = ""
            output_dict["Certifications"] = ""
            output_dict["Additional Experience"] = ""
            output_dict["Diversity"] = ""
            output_dict["Engagement Model"] = ""
            output_dict["Industries"] = ""
            output_dict["Languages"] = ""
            output_dict["URL"] = dict_company["URL"]
            print(f"{i}/{1800} ----- {dict_company['Company Name'], dict_company['URL']} FAILED======================")
            output.append(output_dict)
            continue
        output.append(output_dict)
        print(f"{i}/{1800} ----- {dict_company['Company Name']} SUCCESS")
    pd.DataFrame(output).to_csv(f"Output_{start_ind}-{start_ind+length}.csv",index=False)
    start_ind += length