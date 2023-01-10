from controller import ISubscriber


class Publisher:
    subscriber: ISubscriber = None

    def set_subscriber(self, new_subscriber: ISubscriber):
        self.subscriber = new_subscriber

    def get_subscribers(self):
        return self.subscriber
