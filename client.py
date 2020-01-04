# install_twisted_rector must be called before importing the reactor

from kivy.support import install_twisted_reactor

install_twisted_reactor()


from twisted.internet import reactor, protocol
import datetime


class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.factory.app.on_connection(self.transport) # Called when a connection to another endpoint is made.

    def dataReceived(self, data):
        data = data.decode('utf-8').replace('\n','')
        self.factory.app.print_message(data) # Called when data is received across a transport.
        self.factory.app.save_data(data) # Write the data to a file


class EchoClientFactory(protocol.ClientFactory):
    protocol = EchoClient

    def __init__(self, app):
        self.app = app

    def startedConnecting(self, connector):
        self.app.print_message('Started to connect.')

    def clientConnectionLost(self, connector, reason):
        self.app.print_message('Lost connection.'+ reason.getErrorMessage())

    def clientConnectionFailed(self, connector, reason):
        self.app.print_message('Connection failed.'+ reason.getErrorMessage())



import kivy.app
import kivy.uix.screenmanager
import kivy.uix.button

class ClientApp(kivy.app.App):

    display_data = {}
    buttons_ids={}

    def save_data(self, data):
        date = datetime.datetime.now().strftime('%Y%m%d')
        time = datetime.datetime.now().strftime('%H:%M:%S')
        f = open('f.csv', 'a', encoding='utf-8')
        f.write(date + ',')
        f.write(time + ' ' + data)
        f.write('\n')
        f.close()

    def screen_0_on_enter(self):
        try:
            with open('host_port_date.csv', 'r', encoding='utf-8') as f:
                ls = f.readlines()
                for k,v in enumerate(ls): # 数据处理
                    v = v.strip(',\n')
                    ls[k] = v
                self.root.screens[0].ids['text_input_host'].text = ls[0]
                self.root.screens[0].ids['text_input_port'].text = ls[1]
        except:
            self.root.screens[0].ids['text_input_host'].text = ''
            self.root.screens[0].ids['text_input_port'].text = ''

    def screen_2_on_enter(self):
        try:
            with open('host_port_date.csv', 'r', encoding='utf-8') as f:
                ls = f.readlines()
                for k,v in enumerate(ls): # 数据处理
                    v = v.strip(',\n')
                    ls[k] = v
                self.root.screens[2].ids['text_input_search'].text = ls[2]
        except:
            self.root.screens[2].ids['text_input_search'].text = ''

    def screen_on_enter(self, screen_num):
        curr_screen = self.root.screens[screen_num]

        layout = curr_screen.ids['gridlayout']
        layout.bind(minimum_height=layout.setter('height'))

        # remove the widget and clear the dictionary
        for btn_key, curr_btn in ClientApp.buttons_ids.items():
            layout.remove_widget(curr_btn)

        ClientApp.display_data = {}

        fi = open('f.csv', 'r', encoding='utf-8')
        for line in fi:
            line = line.strip(',\n')
            ls = line.split(',')
            ClientApp.display_data[ls[0]] = ClientApp.display_data.get(ls[0], []) + ls[1:]
        fi.close()

        for i,text in enumerate(ClientApp.display_data[self.index]):
            btn = kivy.uix.button.Button(text=text, size=(880, 90),
                                         size_hint=(None, None),font_size='18sp')
            ClientApp.buttons_ids['btn' + str(i)] = btn # store the object for deleting them
            layout.add_widget(btn)

    def __init__(self, **kwargs):
        super(ClientApp, self).__init__(**kwargs)
        self.host = None
        self.port = None
        self.counter = 0
        self.index = ''

    def button_log_in_press(self):
        self.host = bytes(self.root.screens[0].ids['text_input_host'].text, encoding="utf8")
        self.port = int(eval(self.root.screens[0].ids['text_input_port'].text))
        self.print_message('Loaded successfully')
        self.root.current = 'connection'
        self.connect_to_server()
        with open('host_port_date.csv', 'w', encoding='utf-8') as f:
            f.write(self.root.screens[0].ids['text_input_host'].text + '\n')
            f.write(self.root.screens[0].ids['text_input_port'].text + '\n')


    def button_search_press(self):
        self.index = self.root.screens[2].ids['text_input_search'].text
        self.root.screens[3].ids['history_label'].text = self.index[:4] + '-' + self.index[4:6] + '-' + self.index[6:]

        with open('host_port_date.csv', 'r', encoding='utf-8') as fr:
            ls = fr.readlines()

        # for 3 rows in the file
        if len(ls) != 3:
            ls = ls + [self.root.screens[2].ids['text_input_search'].text]

        if len(ls) == 3:
            ls[2] = self.root.screens[2].ids['text_input_search'].text

        with open('host_port_date.csv', 'w', encoding='utf-8') as fw:
            for i in ls:
                i = i.strip(',\n')
                fw.write(i + '\n')

        self.root.screens[2].ids['text_input_search'].text = ''
        self.root.current = 'history'

    def button_send_press(self):
        self.send_message()

    def on_connection(self, connection):
        self.print_message("Connected successfully!")
        self.connection = connection

    def print_message(self, msg):
        self.counter += 1
        if self.counter == 15:
            self.root.screens[1].ids['text_label'].text = ""
            self.counter = 0
        self.root.screens[1].ids['text_label'].text += "{}\n".format(msg)

    def send_message(self, *args):
        msg = self.root.screens[1].ids['text_input'].text
        if msg and self.connection:
            self.connection.write(msg.encode('utf-8')) # self.transport.write, the self is EchoClient.
            self.root.screens[1].ids['text_input'].text = ""

    def connect_to_server(self):
        reactor.connectTCP( self.host,
                            self.port,
                            EchoClientFactory(self)) # transport a class

    def build(self):
        try:
            with open('host_port_date.csv', 'r', encoding='utf-8') as f:
                ls = f.readlines()
                for k, v in enumerate(ls):  # 数据处理
                    v = v.strip(',\n')
                    ls[k] = v
                self.root.screens[0].ids['text_input_host'].text = ls[0]
                self.root.screens[0].ids['text_input_port'].text = ls[1]
        except:
            self.root.screens[0].ids['text_input_host'].text = ''
            self.root.screens[0].ids['text_input_port'].text = ''

class MainScreen(kivy.uix.screenmanager.Screen):
    pass

class Connection(kivy.uix.screenmanager.Screen):
    pass

class Search(kivy.uix.screenmanager.Screen):
    pass

class History(kivy.uix.screenmanager.Screen):
    pass


app = ClientApp()
app.run()