# -*- coding: utf8 -*-
class PttDate(object):
  months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec' ]

  def __init__(self, year, month, day):
    super(PttDate, self).__init__()
    self.day = str(day)
    self.day = '0' + self.day if len(self.day) == 1 else self.day          
    self.month = month
    self.month = str(PttDate.months.index(self.month) + 1)
    self.month = '0' + self.month if len(self.month) == 1 else self.month  
    self.year = str(year)

  def __str__(self):
    return '-'.join( [ self.year, self.month, self.day ] )



