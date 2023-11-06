from flask import Flask, jsonify, request, send_file, after_this_request
from validate_email import validate_email
import random
from playwright.async_api import async_playwright
import pandas as pd
import asyncio
# import aiohttp
import tracemalloc
import io
import os
from flask_cors import CORS
from playwright_recaptcha import recaptchav3
import time
from fake_useragent import UserAgent
from itertools import cycle
from playwright_stealth import stealth_async
from datetime import datetime
from config_db import connect_to_mongodb
app = Flask(__name__)
collection_1, collection_2,collection_3 = connect_to_mongodb()
CORS(app)
@app.route('/uploadfile', methods=['POST'])
def uploadfile():
    print('uploading file')
    uploaded_file = request.files['file']
    result_array= []
    
    if uploaded_file and allowed_file(uploaded_file.filename):
        destination = os.path.join('uploads/',uploaded_file.filename)
        uploaded_file.save(destination)
        dataset = pd.read_excel(destination)
        column_name = 'Email'
        if column_name in dataset.columns:
            emails = dataset[column_name].tolist()
            # print(column_data)
        else:
            os.remove(destination)
            return "There is no Email column in excel file and file is deleted."
        
        for email in emails:
            result = validate_email(email)
            # dataset['Validity'] = result
            result_array.append(result)
            time.sleep(4)
        #
        # dataset['Validity'] = result_array
        print(len(result_array))
        dataset['Validity'] = pd.Series(result_array)
        
        dataset.to_excel(destination, index=False)
        # column_data.to_excel(os.path.join('uploads/','emails.xlsx'), index=False)
        return "Data added"
        
    else:
        return {'error':'File upload failed, or invalid file type'}

def allowed_file(filename):
    ALLOWED_EXTS = ['xlsx']
    return '.' in filename and filename.split('.', 1)[1].lower() in ALLOWED_EXTS

# ua = UserAgent()
# ua.random
# user_agents = [ua.chrome, ua.google, ua['google chrome'], ua.firefox, ua.ff, ua.safari,  ua.edge, ua.opera ]
# user_agents_cycle = cycle(user_agents)

@app.route('/hiturls' , methods = ['POST'])
async def Scaping_Profile():
    try: 
        # type_tiny = pyshorteners.Shortener()
        tracemalloc.start()
        uploaded_file = request.files['file']
        if uploaded_file and allowed_file(uploaded_file.filename):
            destination = os.path.join('urluploads/',uploaded_file.filename)
            uploaded_file.save(destination)
            dataset = pd.read_excel(destination)
            url_column = 'url'
            rol_column = 'roles'
            if url_column in dataset.columns and rol_column in dataset.columns:
                urls = dataset[url_column].tolist()
                rols = dataset[rol_column].tolist()
                # print(urls)
                # print(rols)
                dic =[]
                for companyUrl,companyRole in zip(urls,rols):
                    Existing_record = collection_2.find_one({"url":companyUrl,"roles":companyRole})
                    if Existing_record is None:
                       dic.append({
                         'url':companyUrl,
                         'roles':companyRole,
                         'upload_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                         'file_name': uploaded_file.filename
                        })
                if dic:       
                   collection_2.insert_many(dic)
            else:
                os.remove(destination)
                return "There is no 'url' or 'roles' column in excel file and file is deleted."
            # for i in range(6):
                # Proxy = random.choice(proxy_List)
                #     print(proxy)
                # proxy={
                #     'server': 'http://'+ random_ip
                # }
            async with async_playwright() as p:
                browser_type = [p.chromium, p.firefox, p.webkit]
                browser_type_cycle = cycle(browser_type)
                counter =0
                start_index =0
                # browser = await p.chromium.launch(
                # headless = False)
                # page = await browser.new_page()
                titles = []
                links = []
                roles =[]
                url_list =[]
                for _ in range(3):
                    browser_show = next(browser_type_cycle)
                    browser = await browser_show.launch(
                    headless = False)
                    page = await browser.new_page()
                    await stealth_async(page)
                    for i in range(start_index,len(urls)):
                        url = urls[i]
                        role = rols[i]
                    # for url,role in zip(urls,rols):
                        start_index+=1
                        counter+=1
                    # for browser_type in [p.chromium, p.firefox, p.webkit]:
                    # browser_show = next(browser_type_cycle)
                    # browser = await browser_show.launch(
                    # headless = False)
                    # page = await browser.new_page()
                        user_agent = UserAgent(browsers=["chrome", "edge", "firefox", "safari","Opera","phantom","Wavebox","Rambox"]).random
                    # print(user_agent)
                    # user_agent = next(user_agents_cycle)

                        await page.set_extra_http_headers({"User-Agent": user_agent})
                        query_search =f'http://www.google.com/search?q={url} {role}'
                        await page.goto( query_search)
                    # await asyncio.sleep(random.uniform(1, 3))
                        elements = await page.query_selector_all('a')
        
                        for element in elements:
                            href ,title, role_1 = await asyncio.gather(
                            element.get_attribute('href'),
                            element.inner_text(),
                            element.inner_text()
                            )
                            if href is not None and 'linkedin.com' in href:
                                break
                      
                        title_name = title.split()[:2]
                     # print(f"title_name:::{title_name}")
                        title_name= ' '.join(title_name)
                        links.append(href)
                        titles.append(title_name)
                        url_list.append(url)
                        role_parts = role_1.lower().split()
                    # print(f'list of roles  {role_parts}')
                        filtered_role = [x for x in role_parts if any(keyword in x for keyword in ['founder', 'ceo', 'co-founder','founder/ceo'])]
                    # print(f"filter {filtered_role}")
                        if len(filtered_role) >=2:
                            roles.append(filtered_role[:2])
                        else:
                            roles.append(filtered_role[:1])
                        if counter >= 50:
                           await browser.close()
                           counter = 0
                           break
                data=[]
                for url ,title in zip(url_list,titles):
                    data.append( {
                        'url': url,
                        "name": title,
                    })
                
                collection_1.insert_many(data)
                dataset['Linked_in'] = pd.Series(links)
                dataset['name'] = pd.Series(titles)
                dataset['role']= pd.Series(roles)
                dataset.to_excel(destination, index=False)
                # await page.get_by_role('presentation').click()
                # await browser.close()
                return "Data Added",200
            # asyncio.get_event_loop().run_until_complete(main())
        else:
          return "Data not updated"
        
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "An error occurred while processing the file"}), 500

 
def allowed_file(filename):
    ALLOWED_EXTS = ['xlsx']
    return '.' in filename and filename.split('.', 1)[1].lower() in ALLOWED_EXTS

 # Define a list of user-agent strings to rotate
# user_agents = [
#                 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.1234.0 Safari/537.36",
#                 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/99.0.0.0 Safari/537.36",
                # Add more user agents here
            # ]  
# proxy_List=[
#      {'server':'http://185.140.53.137:80'},
#      {'server':'http://186.121.235.66:8080'},
#      {'server':'http://47.88.62.42:80'},
#      {'server':'http://177.105.93.15:8080'},
#      {'server':'http://20.206.106.192:80'},
#      {'server':'http://20.111.54.16:80'},
#      {'server':'http://20.210.113.32:80'},
#      {'server':'http://220.73.173.111:3001'},
#      {'server':'http://51.75.206.209:80'},
#      {'server':'http://43.157.67.116:8888'},
#      {'server':'http://4.175.121.88:80'},
#      {'server':'http://12.186.205.121:80'}
# ]
            
                



@app.route('/dnldurlfile', methods = ['GET'])
def dnldurlfile():
    try:
        args = request.args
        file_name = args.get('name')
        file_path = os.path.join('urluploads/', file_name)
        
        return_data = io.BytesIO()
        with open(file_path, 'rb') as fo:
            return_data.write(fo.read())
    # (after writing, cursor will be at last byte, so move it to start)
        return_data.seek(0)

        # os.remove(file_path)
        
        return send_file(return_data, as_attachment=True, mimetype='application/vnd.ms-excel', download_name='Ids.xlsx')
#  os.remove(file_path)
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred while downloading the file"}), 500
    
@app.route('/dnldemailfile', methods = ['GET'])
def dnldemailfile():
    try:
        args = request.args
        file_name = args.get('name')
        file_path = os.path.join('uploads/', file_name)

        with open(file_path, 'rb') as fo:
            return_data = io.BytesIO(fo.read())

        # You should not remove the file here; it's done after sending it

        # Send the file as a response
        return send_file(
            return_data,
            as_attachment=True,
            mimetype='application/vnd.ms-excel',
            download_name='updated.xlsx'
        )
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred while downloading the file"}), 500

# Run the flask App
if __name__ == '__main__':
 app.run(debug=False, host='0.0.0.0')    
