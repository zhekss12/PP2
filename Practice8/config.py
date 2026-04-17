import os
from configparser import ConfigParser

def load_config(filename='database.ini', section='postgresql'):
    # Находим папку, в которой лежит этот скрипт
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, filename)
    
    parser = ConfigParser()
    
    # Проверяем, существует ли файл вообще
    if not os.path.exists(full_path):
        raise Exception(f"Файл не найден: {full_path}")

    # Читаем файл максимально безопасно для Windows
    # errors='ignore' просто выкинет тот самый вредный байт 0xc2
    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
        parser.read_file(f)

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(f'Секция {section} не найдена в файле {filename}')

    return config

# Этот блок ниже нужен, чтобы ты мог проверить работу конфига отдельно
if __name__ == '__main__':
    try:
        print("Проверка конфига...")
        print(load_config())
    except Exception as e:
        print(f"Ошибка при проверке: {e}")