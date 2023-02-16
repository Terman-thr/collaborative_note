import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add) (
            self.room_group_name,
            self.channel_name
        )
        self.accept()

        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are now connected!'
        }))


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        if type == 'highlight':
            article = text_data_json['article']
            highlightCnt = text_data_json['highlightCnt']
            print("article:", article)
            print("highlightCnt:", highlightCnt)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'article_text',
                    'article': article,
                    'highlightCnt': highlightCnt
                }
            )
            
        elif type == 'chat':
            message = text_data_json['message']
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )


    def article_text(self, event):
        article = event['article']
        highlightCnt = event['highlightCnt']
        self.send(text_data=json.dumps({
            'type': 'article',
            'article': article,
            'highlightCnt': highlightCnt
        }))



    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))

