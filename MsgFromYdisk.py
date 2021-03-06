import yadisk
import pickle

class ApiMsg:

    def __init__(self, token, user_name, remote_dir):
        self.y = yadisk.YaDisk(token=token)
        self.loc_user = user_name
        self.remote_dir = remote_dir
        self._init()

    def _init(self):
        ls = ['init']
        if not self.y.is_file(f"{self.remote_dir}/{self.loc_user}.msg"):
            print('Иницилизация.')
            with open('temp.msg', 'wb') as f:
                pickle.dump(ls, f)
                # Загружает "temp.msg" в "/destination.txt"
            self.y.upload("temp.msg", f"{self.remote_dir}/{self.loc_user}.msg")

    def _send_msg(self, ms):
        """
        Send message to Ydisk
        :param ms: message
        :return:
        """
        self.y.download(f"{self.remote_dir}/{self.loc_user}.msg", "temp.msg")
        with open('temp.msg', 'rb') as f:
            data = pickle.load(f)
        data.append(ms)
        # Безвозвратно удаляет файл
        self.y.remove(f"{self.remote_dir}/{self.loc_user}.msg", permanently=True)
        with open('temp.msg', 'wb') as f:
            pickle.dump(data, f)
        # Загружает "output.txt" в "/destination.txt"
        self.y.upload("temp.msg", f"{self.remote_dir}/{self.loc_user}.msg")
        print(f'Сообщние отправлено пользоватедем {self.loc_user}.')

    def _get_msg(self, rem_user):
        """
        Get message from remote user
        :param rem_user: Name remote user
        :return:
        """
        if self.y.is_file(f"{self.remote_dir}/{rem_user}.msg"):
            self.y.download(f"{self.remote_dir}/{rem_user}.msg", "temp.msg")
            with open('temp.msg', 'rb') as f:
                data = pickle.load(f)[-1]
            print(data)
        else:
            print('fСообщений от пользователя {rem_user} нет.')

    def _get_msg_all(self, rem_user):
        """
        Get list message from remote user
        :param rem_user:
        :return:
        """
        if self.y.is_file(f"{self.remote_dir}/{rem_user}.msg"):
            self.y.download(f"{self.remote_dir}/{rem_user}.msg", "temp.msg")
            with open('temp.msg', 'rb') as f:
                data = pickle.load(f)
            print(f'Список сообщений пользователя {rem_user}:')
            print('-----------------')
            [print(cn, ms) for cn, ms in enumerate(data)]
        else:
            #return 'fСообщений от пользователя {rem_user} нет.'
            print('fСообщений от пользователя {rem_user} нет.')

    def _admin(self, command):
        if command == 'lm':
            ret = self.y.listdir(self.remote_dir)
            print('Список диалогов пользователей:')
            [print(obj['name']) for obj in list(ret) if obj['name'].endswith('msg')]
        elif command == 'ls':
            ret = self.y.listdir(self.remote_dir)
            print('Список файлов на сервере:')
            [print(obj['name']) for obj in list(ret)]
        elif command == 'rm':
            ret = self.y.listdir(self.remote_dir)
            [self.y.remove(f"{self.remote_dir}/{obj['name']}") for obj in list(ret)]
            print('На сервере все файлы удалены !')

    def __call__(self, **kwargs):
        self._main(**kwargs)

    def _main(self, cm='-h', prm=None):
        if cm == '-h':
            print('Справка')
            print('-----------------------')
            print(f'Прочитать последнее сообщение: main(cm = "-r", prm= <имя_пользователя>)')
            print(f'Прочитать все сообщения: main(cm = "-ra", prm = <имя_пользователя>)')
            print(f'Отправка сообщения: main(cm = "-w", prm = <Текст (в кавычках)>)')
            print(f'Список диалогов: main(cm = "-adm", prm = "lm")')
            print(f'Список файлов на сервере: main(cm = "-adm", prm = "ls")')
            print(f'Удалить все файлы с сервера: main(cm = "-adm", prm = "rm")')
            print(f'Скачать файл с сервера: main(cm = "-get", prm = <имя_файла>)')
            print(f'Отправить файл на сервер: main(cm = "-set", prm = <имя_файла>)')
        else:
            self._init()
        if cm == '-r':
            self._get_msg(prm)
        elif cm == '-ra':
            self._get_msg_all(prm)
        elif cm == '-w':
            self._send_msg(prm)
        elif cm == '-adm':
            self._admin(prm)
        elif cm == '-get':
            self._get_file(prm)
        elif cm == '-set':
            self._set_file(prm)

    def _get_file(self, file_name):
        self.y.download(f"{self.remote_dir}/{file_name}", file_name)
        print(f'Файл {file_name} скачан.')

    def _set_file(self, file_name):
        if self.y.is_file(f"{self.remote_dir}/{file_name}"):
            self.y.remove(f"{self.remote_dir}/{file_name}")
        self.y.upload(file_name, f"{self.remote_dir}/{file_name}")
        print(f'Файл {file_name} загружен на сервер.')


if __name__ == '__main__':
    import MyToken
    msg = ApiMsg(token=MyToken.token,  user_name='your_name', remote_dir = '/olimp')
                           
    #msg(cm = "-h") # Справка
    #msg(cm = "-adm", prm = "rm") # Удалить все файлы на сервере
    #msg(cm="-get", prm='dm.msg') # Скачать файл с сервера
    #msg(cm="-set", prm="MsgFromYdisk.py") # Отправить файл на сервер
    #msg(cm = "-adm", prm = "ls") # Список файлов на сервере

    msg(cm = "-adm", prm = "lm") # Список сообщений
    #msg(cm = "-ra", prm = "Bill_Gates") # Прочитать все сообщения пользователя "Bill_Gates"
    #msg(cm = "-r", prm = "Bill_Gates") # Прочитать последнее сообщение пользователя "Bill_Gates"
    #msg(cm = "-w", prm = "Привет") # Отправить сообщение                       
