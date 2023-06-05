import pyinstaller_versionfile

name = 'HL7 CS'
ver = '1.0.1.9'
encoding = 'UTF-8'

history = '''
    History changed:
        1.0.1:
            1.0.1.9: New: Ввод строки для IP клиентов заменен на выпадающий список, чтобы добавить в список новый хост, нужно нажать Enter
            1.0.1.8: New: Добавлена возможность генерации текущего времени для HL7 сообщений.
            1.0.1.7: New: Реализован запуск программы из командной строки с параметрами (Список параметров: HL7.exe -h(--help))
            1.0.1.6: New: Изменен минимальный размер окна приложения. История сообщений автоматически скроется, если будет недостаточно места для её отображения.
            1.0.1.5: New: Добавлена возможность копировать информацию об отправке сообщения и выбранный сегмент HL7 в буфер.
            1.0.1.4: New: Добавлена возможность изменять сегмент Acknowledgment Code (MSA_1) в ответе от сервера.
                     New: Добавлена кнопка 'Clear' для очистки текстовых редакторов на вкладке 'SERVER'.
            1.0.1.3: New: Добавлена возможность изменять размер текстовых редакторов.
                     Fix: Вылет программы при получении сервером сообщения в кодировке отличной от UTF-8.
            1.0.1.2: Fix: Вылет программы при получении сервером сообщения не HL7 формата.
'''

pyinstaller_versionfile.create_versionfile(
    output_file="version.txt",
    version=ver,
    company_name="GNU General Public License",
    file_description=name,
    internal_name=name,
    legal_copyright="© GNU General Public License. All rights reserved.",
    original_filename="HL7.exe",
    product_name=name)

with open('README.md', mode='w', encoding=encoding) as readme:
    readme.write(f'# {name} {ver} \n')
    readme.write(history)
    # with open('history.txt', mode='r', encoding=encoding) as history:
    #     readme.write(history.read())
