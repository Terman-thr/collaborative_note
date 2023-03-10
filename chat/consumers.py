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
            # print("article:", article)
            # print("highlightCnt:", highlightCnt)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'article_text',
                    'article': article,
                    'highlightCnt': highlightCnt
                }
            )
        
        elif type == 'note':
            comment = text_data_json['comment']
            id = text_data_json['id']
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'comment_text',
                    'comment': comment,
                    'id': id
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
        
        elif type == 'clearNote':
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'clear_note'
                }
            )

    def clear_note(self, event):
        self.send(text_data=json.dumps({
            'type': 'clear_note'
        }))


    def article_text(self, event):
        article = event['article']
        highlightCnt = event['highlightCnt']
        self.send(text_data=json.dumps({
            'type': 'article',
            'article': article,
            'highlightCnt': highlightCnt
        }))


    def comment_text(self, event):
        comment = event['comment']
        id = event['id']
        self.send(text_data=json.dumps({
            'type': 'note',
            'comment': comment,
            'id': id
        }))



    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))

