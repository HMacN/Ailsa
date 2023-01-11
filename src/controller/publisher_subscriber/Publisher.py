from controller.publisher_subscriber import ISubscriber


class Publisher:
    subscribers: ISubscriber = None

    def __init__(self):
        self.subscribers = set()

    def add_subscriber(self, new_subscriber: ISubscriber):
        self.subscribers.add(new_subscriber)

    def get_subscribers(self):
        return self.subscribers

    def remove_subscriber(self, subscriber: ISubscriber):
        if self.subscribers.__contains__(subscriber):
            self.subscribers.remove(subscriber)

    def notify_all(self):
        for s in self.subscribers:
            s.notify()

    def notify(self, subscriber: ISubscriber):
        for s in self.subscribers:
            if s == subscriber:
                s.notify()
