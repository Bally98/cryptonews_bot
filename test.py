import time
import pandas as pd
from tqdm import tqdm
from datetime import datetime, timedelta, timezone
def source_text(link):
     character_1 = 'h'
     character_2 = '/'
     count_1 = 2
     count_2 = 3
     index_1 = 1
     index_2 = -1
     for j in range(count_1):
          index_1 = link.find(character_1, index_1 + 1)
     for i in range(count_2):
          index_2 = link.find(character_2, index_2 + 1)
     if index_2 != -1:
          result = link[index_1:index_2]
          return result
     else:
          return 'Error'

print(source_text('wehrwer.https://cointelegraph.com/'))


