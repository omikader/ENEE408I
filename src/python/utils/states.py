from enum import Enum

class States(Enum):
	STOP = 0
	FL = 1  # fast left
	FF = 2  # fast forward
	FR = 3  # fast right
	FB = 4  # fast backwards
	SL = 5  # slow left
	SF = 6  # slow forward
	SR = 7  # slow right
	SB = 8  # slow backwards
	NA = 9 
