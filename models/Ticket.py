from datetime import datetime

class Ticket():
    """Class for Game post
    attributes:
        Games: [Dict List]
        total_odds: int
        date: Date
        starts: DateTime
        ticket_index: ticket number in ticket lists
        status
        games_no
    """

    def __init__(self, *args, **kwargs):
        if kwargs:
            for k, v in kwargs.items():
                if k != '__class__':
                    setattr(self, k, v)
        self.created_at = datetime.now()

    def to_dict(self) -> dict:
        """Returns a dictionary of class instance"""
        temp = self.__dict__.copy()
        temp['created_at'] = datetime.isoformat(temp['created_at'])
        temp['__class__'] = self.__class__.__name__
        if '_sa_instance_state' in temp:
            del temp['_sa_instance_state']
        return temp