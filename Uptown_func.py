#Date and Time
from datetime import date, datetime
today = date.today()
now = datetime.now()
the_date = today.strftime('%m.%d.%Y')
the_time = now.strftime('%H.%M')


#File Conversions
import pandas as pd
def csv_2_excel(csv_path, save_path):
    if not save_path.endswith('.xlsx'):
        save_path = save_path + '.xlsx'
    (pd.read_csv(csv_path)).to_excel(save_path, index = None, header = True)


#CSV Functions
import os, csv 
def read_csv(read_file):
    output = []
    with open(read_file, 'r') as listfile:
        rows = csv.reader(listfile)
        for row in rows: 
            output.append(row)
    return output

def newcsv(output_name, titlerow, list_of_lists, excel = False):
    with open(output_name, 'w', newline="") as output:
        write = csv.writer(output)
        write.writerow(titlerow)
        write.writerows(list_of_lists)
    filepath = str(os.getcwd()) + "\\" + output_name
    if excel:
        csv_2_excel(filepath, filepath.replace('.csv', '.xlsx'))
        filepath = filepath.replace('.csv', '.xlsx')
    return filepath


#QRCode Functions
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image
def make_QR(data, save, path = '', logo = False):
    if not save.endswith('.jpg'):
        save = save+'.jpg'
    if path != '':
        if path[-1] != '/':
            path = path+'/'
    if not logo:
        img = qrcode.make(data)
    else:
        logo = Image.open(logo)
        basewidth = 100
        wpercent = (basewidth/float(logo.size[0]))
        hsize = int((float(logo.size[1])*float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
        QRcode = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H
        )
        QRcode.add_data(data)
        QRcode.make()
        img = QRcode.make_image(
            fill_color='Black', back_color="white").convert('RGB')
        # set size of QR code
        pos = ((img.size[0] - logo.size[0]) // 2,
            (img.size[1] - logo.size[1]) // 2)
        img.paste(logo, pos)

    img.save(path+save)

def read_QR_frm_file(QRfile):
    img = Image.open(QRfile)
    result = decode(img)
    results = []
    for QR in result:
        info = QR.data.decode('utf-8')
        print(info)
        results.append(info)
    return results

def contact_QR_data(full_name, company, title, email, mobile_phone, work_phone):
    name_data = full_name.split()
    first, last = name_data[0], name_data[-1]
    contact = 'BEGIN:VCARD\nVERSION:3.0\nN:' + last + ';' + first + '\nFN:' + full_name + '\nORG:' + company + ', LLC\nTITLE:' + title + '\nTEL;WORK;VOICE:' + work_phone + '\nTEL;CELL:' + mobile_phone + '\nTEL;FAX:\nEMAIL;WORK;INTERNET:' + email + '\nEND:VCARD'
    print(f'Making QR for {full_name} from {company}')
    print('')
    return contact

def directory_contact_QR(CSV_Source, save_folder = ''):
    contacts = read_csv(CSV_Source)

    for contact in contacts:
        photo, full_name, company, title, email, mobile_phone, work_phone = contact
        if company != 'Holder Construction Group, LLC':
            if mobile_phone != '' and work_phone != '':    
                data = contact_QR_data(full_name, company, title, email, mobile_phone, work_phone)
                savename = full_name + '_' + company
                make_QR(data, savename, path = save_folder)

def wifi_QR_data(network, password):
    wifi = 'WIFI:T:WPA;S:'+network+';P:'+password+';H:;'
    return wifi


#OS Parsing Functions
import os
def list_files(directory): #Prints Indented File Structure for Given Directory
    for root, dirs, files in os.walk(directory):
        level = root.replace(directory, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

def file_index(directories, savename, title = ['Host Folder', 'Filename', 'Filetype', 'LNK']): #logs all files in a [directory] in a CSV with hyperlinks

    filepaths, filenames, folders = [], [], []
    for Folder in directories:
        print('Searching... ', end = '')
        for root, dirs, files in os.walk(Folder):
            for file in files:
                filepaths.append(os.path.join(root,file))
                filenames.append(file)
                folders.append(root)


        LOLs = []
        for x in range(len(filepaths)):
            path, name = folders[x], filenames[x]
            type = (name.split('.'))[-1]
            lnk = f'=HYPERLINK(\"{path}\",\"{name}\")'
            lst = [path, name, type, lnk]
            exc = ['dat', 'rvt', 'rws', 'slog', 'indd']
            if type not in exc:
                LOLs.append(lst)
    
    if savename.endswith('.csv'):
        savename = savename.replace(+ '_' + the_date + '.csv')
    else:
        savename = savename + '_' + the_date + '.csv'

    newcsv(savename, title, LOLs, excel = True)
    
#File Conversions
import pandas as pd
def csv_2_excel(csv_path, save_path):
    if not save_path.endswith('.xlsx'):
        save_path = save_path + '.xlsx'
    (pd.read_csv(csv_path)).to_excel(save_path, index = None, header = True)

