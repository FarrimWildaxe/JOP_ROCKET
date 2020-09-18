from capstone import *
import re
import pefile
import sys
import binascii
import copy
import os
from collections import OrderedDict
from lists import *
#from jmps.loadlibrary import *
from ui import *
import win32api
import win32con
from ctypes import windll
from ctypes import wintypes
import sys
import win32file
from collections import OrderedDict
import hashlib
from stackpivot import *
from checkIt import *
# from printing import *
NewCounter = 0

numArgs = len(sys.argv)
peName = ''#'filezilla.exe'  # hardcoded for testing, made irrelevant if supplied with 
modName = peName
PEsList = []
PE_path =""
PEsList_Index = 0
skipZero = False
numPE = 1
skipPath = False
FoundApisAddress = []
FoundApisName = []
saveAPI=0x00
VP = 0
VA=""
MA=""
GPA=""
MemCpyAddress=""
VPl = []
VAl=[]
GPAl=[]
MAl=[]
badChars = ["zz"]
fname=""


numVPAA = 5
if numArgs > 1:			# to get full functionality, need to put file location for binary that is installed (may need to find some DLLs in that directory)
	peName= sys.argv[1] 
	matchObj = re.match( r'^[a-z]+:[\\|/]+', peName, re.M|re.I)
	if matchObj:
		head, tail = os.path.split(peName)
		peName = tail
		PE_path = head
		skipPath = True
	if not matchObj:
		skipPath = False
	matchObj = re.match( r'^[a-z0-9]+.txt', peName, re.M|re.I)
	if matchObj:
		head, tail = os.path.split(peName)
		with open(tail, "r") as ins:
			for line in ins:
				line2 = line.rstrip('\n')
				PEsList.append(line2)
		peName = PEsList[0]
		head, tail = os.path.split(peName)
		peName = tail
		PE_path = head
		numPE = len(PEsList)
		skipPath = True
		print PEsList
	try:
		if sys.argv[2] =="-all":
			DoEverything = True
	except:
		pass
PEtemp = PE_path + "/"+ peName

if skipPath == True:
	pe = pefile.PE(PEtemp)
if skipPath == False:
	pe = pefile.PE(peName)

directory =""
newpath =""
index = 0
PE_DLL = []
PE_DLLS = []
PE_DLLS2 = []
Remove = []
DLL_str ="Module"
DLL_Protect = []
PE_Protect =""
o = 0
#objs[o].data2 = objs[o].pe.sections[0].get_data()[0:4]
cs = Cs(CS_ARCH_X86, CS_MODE_32)
CheckallModules = False
getJMP = True
getCALL = False
getDG = False
printAllJMP = False
printja = False
printjb = False
printjc = False
printjd = False
printjdi = False
printjsi = False
printjbp = False
printjsp = False
printAllCall = False
printca = False
printcb = False
printcc = False
printcd = False
printdi = False
printsi = False
printcbp = False
printcsp = False

printptrja = False
printptrjb = False
printptrjc = False
printptrjd = False
printptrjdi = False
printptrjsi = False
printptrjbp = False
printptrjsp = False
printptrca = False
printptrcb = False
printptrcc = False
printptrcd = False
printptrdi = False
printptrsi = False
printptrcbp = False
printptrcsp = False

printDeref = False
printAllMath = False
printStack = False
printAdd = False
printSub = False
printMul = False
printDiv = False
printMovement = False
printMov = False
printMovV = False
printMovS = False
printLea = False
printXchg = False
printAllStack = False
printPop = False
printPush = False
printDec = False
printInc = False
printBitwise = False
printShiftLeft = False
printShiftRight = False
printRotateRight = False
printRotateLeft = False
printEverything = False
printRecommended = True
peNameSkip = True
Depth = 5
printDispatcherEAX = False
printDispatcherEBX = False
printDispatcherECX = False
printDispatcherEDX = False
printDispatcherEDI = False
printDispatcherESI = False
printDispatcherEBP = False
printDispatcherEAXBest = False
printDispatcherEBXBest = False
printDispatcherECXBest = False
printDispatcherEDXBest = False
printDispatcherEDIBest = False
printDispatcherESIBest = False
printDispatcherEBPBest = False
printDispatcherEAXOther = False
printDispatcherEBXOther = False
printDispatcherECXOther = False
printDispatcherEDXOther = False
printDispatcherEDIOther = False
printDispatcherESIOther = False
printDispatcherEBPOther = False
DoEverything = False
#VirtualAdd = objs[o].VirtualAdd
#ImageBase = pe.OPTIONAL_HEADER.ImageBase
#vSize = objs[o].pe.sections[0].Misc_VirtualSize
#objs[o].startLoc = VirtualAdd + ImageBase

#entryPoint = pe.OPTIONAL_HEADER.addressOfEntryPoint
#data = pe.get_memory_mapped_image()[entryPoint:entryPoint+vSize]
#objs[o].data2 = objs[o].pe.sections[0].get_data()[VirtualAdd:VirtualAdd+vSize]
entryPoint = 0 
VirtualAdd= 0 
ImageBase= 0 
vSize= 0 
startAddress= 0 
endAddy= 0 
entryPoint= 0 
#data2 	= 0 
total = 0
w=0
path1 = ""
ans = ""
total2 = 0 
levelTwo = False
bit32 = True
hashCheckVal = 4

if skipPath == False:
	PEtemp = peName
if skipPath == True:
	PEtemp = PE_path + "/"+ peName
#https://stackoverflow.com/questions/1345632/determine-if-an-executable-or-library-is-32-or-64-bits-on-windows
if win32file.GetBinaryType(PEtemp) == 6:
	bit32 = False
else:
	bit32 = True


#start class
class MyBytes:

	def _init_(self): #, name):
		"""Initializes the data."""
		global pe
		self.peName = 'filezilla.exe'
		self.modName2 ='modName2'
		self.pe = pe #pefile.PE(self.peName)
		self.data2 = 0
		self.VirtualAdd = 0
		self.ImageBase = 0
		self.vSize = 0
		self.startLoc = 0
		self.endAddy = 0
		self.entryPoint = 0
		self.listOP_JMP_EAX2 = []
		self.listOP_JMP_EBX = []
		self.listOP_JMP_ECX = []
		self.listOP_JMP_EDX = []
		self.listOP_JMP_ESI = []
		self.listOP_JMP_EDI = []
		self.listOP_JMP_ESP = []  
		self.listOP_JMP_EBP = []
		self.listOP_JMP_EAX_CNT = []
		self.listOP_JMP_EBX_CNT = []
		self.listOP_JMP_ECX_CNT = []
		self.listOP_JMP_EDX_CNT = []
		self.listOP_JMP_ESI_CNT = []
		self.listOP_JMP_EDI_CNT = []
		self.listOP_JMP_ESP_CNT = []  
		self.listOP_JMP_EBP_CNT = []
		self.listOP_JMP_EAX_NumOps = []
		self.listOP_JMP_EBX_NumOps = []
		self.listOP_JMP_ECX_NumOps = []
		self.listOP_JMP_EDX_NumOps = []
		self.listOP_JMP_ESI_NumOps = []
		self.listOP_JMP_EDI_NumOps = []
		self.listOP_JMP_ESP_NumOps = []  
		self.listOP_JMP_EBP_NumOps = []
		self.listOP_CALL_EAX = []
		self.listOP_CALL_EBX = []
		self.listOP_CALL_ECX = []
		self.listOP_CALL_EDX = []
		self.listOP_CALL_EDI = []
		self.listOP_CALL_ESI = []
		self.listOP_CALL_EBP = []
		self.listOP_CALL_EAX_CNT = []
		self.listOP_CALL_EBX_CNT = []
		self.listOP_CALL_ECX_CNT = []
		self.listOP_CALL_EDX_CNT = []
		self.listOP_CALL_ESI_CNT = []
		self.listOP_CALL_EDI_CNT = []
		self.listOP_CALL_EBP_CNT = []
		self.listOP_CALL_EAX_Module = []
		self.listOP_CALL_EBX_Module = []
		self.listOP_CALL_ECX_Module = []
		self.listOP_CALL_EDX_Module = []
		self.listOP_CALL_ESI_Module = []
		self.listOP_CALL_EDI_Module = []
		self.listOP_CALL_ESP_Module = []
		self.listOP_CALL_EBP_Module = []
		self.listOP_CALL_EAX_NumOps = []
		self.listOP_CALL_EBX_NumOps = []
		self.listOP_CALL_ECX_NumOps = []
		self.listOP_CALL_EDX_NumOps = []
		self.listOP_CALL_ESI_NumOps = []
		self.listOP_CALL_EDI_NumOps = []
		self.listOP_CALL_ESP_NumOps = []
		self.listOP_CALL_EBP_NumOps = []
		self.listOP_JMP_EAX_Module = []
		self.listOP_JMP_EBX_Module = []
		self.listOP_JMP_ECX_Module = []
		self.listOP_JMP_EDX_Module = []
		self.listOP_JMP_ESI_Module = []
		self.listOP_JMP_EDI_Module = []
		self.listOP_JMP_ESP_Module = []
		self.listOP_JMP_EBP_Module = []
		self.listOP_JMP_PTR_EAX = []
		self.listOP_JMP_PTR_EAX_CNT = []
		self.listOP_JMP_PTR_EAX_NumOps = []
		self.listOP_JMP_PTR_EAX_Module = []
		self.listOP_JMP_PTR_EBX = []
		self.listOP_JMP_PTR_EBX_CNT = []
		self.listOP_JMP_PTR_EBX_NumOps = []
		self.listOP_JMP_PTR_EBX_Module = []
		self.listOP_JMP_PTR_ECX = []
		self.listOP_JMP_PTR_ECX_CNT = []
		self.listOP_JMP_PTR_ECX_NumOps = []
		self.listOP_JMP_PTR_ECX_Module = []
		self.listOP_JMP_PTR_EDX = []
		self.listOP_JMP_PTR_EDX_CNT = []
		self.listOP_JMP_PTR_EDX_NumOps = []
		self.listOP_JMP_PTR_EDX_Module = []
		self.listOP_JMP_PTR_EDI = []
		self.listOP_JMP_PTR_EDI_CNT = []
		self.listOP_JMP_PTR_EDI_NumOps = []
		self.listOP_JMP_PTR_EDI_Module = []
		self.listOP_JMP_PTR_ESI = []
		self.listOP_JMP_PTR_ESI_CNT = []
		self.listOP_JMP_PTR_ESI_NumOps = []
		self.listOP_JMP_PTR_ESI_Module = []
		self.listOP_JMP_PTR_ESP = []
		self.listOP_JMP_PTR_ESP_CNT = []
		self.listOP_JMP_PTR_ESP_NumOps = []
		self.listOP_JMP_PTR_ESP_Module = []
		self.listOP_JMP_PTR_EBP = []
		self.listOP_JMP_PTR_EBP_CNT = []
		self.listOP_JMP_PTR_EBP_NumOps = []
		self.listOP_JMP_PTR_EBP_Module = []
		self.listOP_CALL_PTR_EAX = []
		self.listOP_CALL_PTR_EAX_CNT = []
		self.listOP_CALL_PTR_EAX_NumOps = []
		self.listOP_CALL_PTR_EAX_Module = []
		self.listOP_CALL_PTR_EBX = []
		self.listOP_CALL_PTR_EBX_CNT = []
		self.listOP_CALL_PTR_EBX_NumOps = []
		self.listOP_CALL_PTR_EBX_Module = []
		self.listOP_CALL_PTR_ECX = []
		self.listOP_CALL_PTR_ECX_CNT = []
		self.listOP_CALL_PTR_ECX_NumOps = []
		self.listOP_CALL_PTR_ECX_Module = []
		self.listOP_CALL_PTR_EDX = []
		self.listOP_CALL_PTR_EDX_CNT = []
		self.listOP_CALL_PTR_EDX_NumOps = []
		self.listOP_CALL_PTR_EDX_Module = []
		self.listOP_CALL_PTR_EDI = []
		self.listOP_CALL_PTR_EDI_CNT = []
		self.listOP_CALL_PTR_EDI_NumOps = []
		self.listOP_CALL_PTR_EDI_Module = []
		self.listOP_CALL_PTR_ESI = []
		self.listOP_CALL_PTR_ESI_CNT = []
		self.listOP_CALL_PTR_ESI_NumOps = []
		self.listOP_CALL_PTR_ESI_Module = []
		self.listOP_CALL_PTR_ESP = []
		self.listOP_CALL_PTR_ESP_CNT = []
		self.listOP_CALL_PTR_ESP_NumOps = []
		self.listOP_CALL_PTR_ESP_Module = []
		self.listOP_CALL_PTR_EBP = []
		self.listOP_CALL_PTR_EBP_CNT = []
		self.listOP_CALL_PTR_EBP_NumOps = []
		self.listOP_CALL_PTR_EBP_Module = []
		self.protect =""
		self.depStatus=""
		self.aslrStatus=""
		self.sehSTATUS=""
		self.CFGstatus=""
		self.listOP_Base = []
		self.listOP_Base_CNT = []
		self.listOP_Base_NumOps = []
		self.listOP_Base_Module = []
		self.listOP_BaseDG = []
		self.listOP_BaseDG_CNT = []
		self.listOP_BaseDG_NumOps = []
		self.listOP_BaseDG_Module = []
		self.listOP_BaseDG_EAX = []
		self.listOP_BaseDG_CNT_EAX = []
		self.listOP_BaseDG_NumOps_EAX = []
		self.listOP_BaseDG_Module_EAX = []
		self.listOP_BaseDG_EBX = []
		self.listOP_BaseDG_CNT_EBX = []
		self.listOP_BaseDG_NumOps_EBX = []
		self.listOP_BaseDG_Module_EBX = []
		self.listOP_BaseDG_ECX = []
		self.listOP_BaseDG_CNT_ECX = []
		self.listOP_BaseDG_NumOps_ECX = []
		self.listOP_BaseDG_Module_ECX = []
		self.listOP_BaseDG_EDX = []
		self.listOP_BaseDG_CNT_EDX = []
		self.listOP_BaseDG_NumOps_EDX = []
		self.listOP_BaseDG_Module_EDX = []
		self.listOP_BaseDG_EDI = []
		self.listOP_BaseDG_CNT_EDI = []
		self.listOP_BaseDG_NumOps_EDI = []
		self.listOP_BaseDG_Module_EDI = []
		self.listOP_BaseDG_ESI = []
		self.listOP_BaseDG_CNT_ESI = []
		self.listOP_BaseDG_NumOps_ESI = []
		self.listOP_BaseDG_Module_ESI = []
		self.listOP_BaseDG_EBP = []
		self.listOP_BaseDG_CNT_EBP = []
		self.listOP_BaseDG_NumOps_EBP = []
		self.listOP_BaseDG_Module_EBP = []
		self.listOP_BaseDG_ESP = []
		self.listOP_BaseDG_CNT_ESP = []
		self.listOP_BaseDG_NumOps_ESP = []
		self.listOP_BaseDG_Module_ESP = []
		self.listOP_BaseDG_EAX_Best = []
		self.listOP_BaseDG_CNT_EAX_Best = []
		self.listOP_BaseDG_NumOps_EAX_Best = []
		self.listOP_BaseDG_Module_EAX_Best = []
		self.listOP_BaseDG_ESP_Best = []
		self.listOP_BaseDG_CNT_ESP_Best = []
		self.listOP_BaseDG_NumOps_ESP_Best = []
		self.listOP_BaseDG_Module_ESP_Best = []
		self.listOP_BaseDG_EBX_Best = []
		self.listOP_BaseDG_CNT_EBX_Best = []
		self.listOP_BaseDG_NumOps_EBX_Best = []
		self.listOP_BaseDG_Module_EBX_Best = []
		self.listOP_BaseDG_ECX_Best = []
		self.listOP_BaseDG_CNT_ECX_Best = []
		self.listOP_BaseDG_NumOps_ECX_Best = []
		self.listOP_BaseDG_Module_ECX_Best = []
		self.listOP_BaseDG_EDX_Best = []
		self.listOP_BaseDG_CNT_EDX_Best = []
		self.listOP_BaseDG_NumOps_EDX_Best = []
		self.listOP_BaseDG_Module_EDX_Best = []
		self.listOP_BaseDG_EDI_Best = []
		self.listOP_BaseDG_CNT_EDI_Best = []
		self.listOP_BaseDG_NumOps_EDI_Best = []
		self.listOP_BaseDG_Module_EDI_Best = []
		self.listOP_BaseDG_ESI_Best = []
		self.listOP_BaseDG_CNT_ESI_Best = []
		self.listOP_BaseDG_NumOps_ESI_Best = []
		self.listOP_BaseDG_Module_ESI_Best = []
		self.listOP_BaseDG_EBP_Best = []
		self.listOP_BaseDG_CNT_EBP_Best = []
		self.listOP_BaseDG_NumOps_EBP_Best = []
		self.listOP_BaseDG_Module_EBP_Best = []
		self.listOP_BaseDG_EAX_Other = []
		self.listOP_BaseDG_CNT_EAX_Other = []
		self.listOP_BaseDG_NumOps_EAX_Other = []
		self.listOP_BaseDG_Module_EAX_Other = []
		self.listOP_BaseDG_EBX_Other = []
		self.listOP_BaseDG_CNT_EBX_Other = []
		self.listOP_BaseDG_NumOps_EBX_Other = []
		self.listOP_BaseDG_Module_EBX_Other = []
		self.listOP_BaseDG_ECX_Other = []
		self.listOP_BaseDG_CNT_ECX_Other = []
		self.listOP_BaseDG_NumOps_ECX_Other = []
		self.listOP_BaseDG_Module_ECX_Other = []
		self.listOP_BaseDG_EDX_Other = []
		self.listOP_BaseDG_CNT_EDX_Other = []
		self.listOP_BaseDG_NumOps_EDX_Other = []
		self.listOP_BaseDG_Module_EDX_Other = []
		self.listOP_BaseDG_EDI_Other = []
		self.listOP_BaseDG_CNT_EDI_Other = []
		self.listOP_BaseDG_NumOps_EDI_Other = []
		self.listOP_BaseDG_Module_EDI_Other = []
		self.listOP_BaseDG_ESI_Other = []
		self.listOP_BaseDG_CNT_ESI_Other = []
		self.listOP_BaseDG_NumOps_ESI_Other = []
		self.listOP_BaseDG_Module_ESI_Other = []
		self.listOP_BaseDG_EBP_Other = []
		self.listOP_BaseDG_CNT_EBP_Other = []
		self.listOP_BaseDG_NumOps_EBP_Other = []
		self.listOP_BaseDG_Module_EBP_Other = []
		self.listOP_BaseDG_ESP_Other = []
		self.listOP_BaseDG_CNT_ESP_Other = []
		self.listOP_BaseDG_NumOps_ESP_Other = []
		self.listOP_BaseDG_Module_ESP_Other = []
		self.listOP_BaseAdd = []
		self.listOP_BaseAdd_CNT = []
		self.listOP_BaseAdd_NumOps  = []
		self.listOP_BaseAdd_Module  = []
		self.listOP_BaseAddEAX = []
		self.listOP_BaseAddEAX_CNT = []
		self.listOP_BaseAddEAX_NumOps  = []
		self.listOP_BaseAddEAX_Module  = []
		self.listOP_BaseAddEBX = []
		self.listOP_BaseAddEBX_CNT = []
		self.listOP_BaseAddEBX_NumOps  = []
		self.listOP_BaseAddECX = []
		self.listOP_BaseAddECX_CNT = []
		self.listOP_BaseAddECX_NumOps  = []
		self.listOP_BaseAddEDX = []
		self.listOP_BaseAddEDX_CNT = []
		self.listOP_BaseAddEDX_NumOps  = []
		self.listOP_BaseAddEDI = []
		self.listOP_BaseAddEDI_CNT = []
		self.listOP_BaseAddEDI_NumOps  = []
		self.listOP_BaseAddESI = []
		self.listOP_BaseAddESI_CNT = []
		self.listOP_BaseAddESI_NumOps  = []
		self.listOP_BaseAddESP = []
		self.listOP_BaseAddESP_CNT = []
		self.listOP_BaseAddESP_NumOps  = []
		self.listOP_BaseAddEBP = []
		self.listOP_BaseAddEBP_CNT = []
		self.listOP_BaseAddEBP_NumOps  = []
		self.listOP_BaseAddEBX_Module  = []
		self.listOP_BaseAddECX_Module  = []
		self.listOP_BaseAddEDX_Module  = []
		self.listOP_BaseAddEDI_Module  = []
		self.listOP_BaseAddESI_Module  = []
		self.listOP_BaseAddEBP_Module  = []
		self.listOP_BaseAddESP_Module  = []
		self.listOP_BaseSub = []
		self.listOP_BaseSub_CNT = []
		self.listOP_BaseSub_NumOps  = []
		self.listOP_BaseSub_Module  = []
		self.listOP_BaseSubEAX = []
		self.listOP_BaseSubEAX_CNT = []
		self.listOP_BaseSubEAX_NumOps  = []
		self.listOP_BaseSubEBX = []
		self.listOP_BaseSubEBX_CNT = []
		self.listOP_BaseSubEBX_NumOps  = []
		self.listOP_BaseSubECX = []
		self.listOP_BaseSubECX_CNT = []
		self.listOP_BaseSubECX_NumOps  = []
		self.listOP_BaseSubEDX = []
		self.listOP_BaseSubEDX_CNT = []
		self.listOP_BaseSubEDX_NumOps  = []
		self.listOP_BaseSubEDI = []
		self.listOP_BaseSubEDI_CNT = []
		self.listOP_BaseSubEDI_NumOps  = []
		self.listOP_BaseSubESI = []
		self.listOP_BaseSubESI_CNT = []
		self.listOP_BaseSubESI_NumOps  = []
		self.listOP_BaseSubESP = []
		self.listOP_BaseSubESP_CNT = []
		self.listOP_BaseSubESP_NumOps  = []
		self.listOP_BaseSubEBP = []
		self.listOP_BaseSubEBP_CNT = []
		self.listOP_BaseSubEBP_NumOps  = []
		self.listOP_BaseSubEAX_Module  = []
		self.listOP_BaseSubEBX_Module  = []
		self.listOP_BaseSubECX_Module  = []
		self.listOP_BaseSubEDX_Module  = []
		self.listOP_BaseSubESI_Module  = []
		self.listOP_BaseSubEDI_Module  = []
		self.listOP_BaseSubEBP_Module  = []
		self.listOP_BaseSubESP_Module  = []
		self.listOP_BaseMul = []
		self.listOP_BaseMul_CNT = []
		self.listOP_BaseMul_NumOps  = []
		self.listOP_BaseMulEAX = []
		self.listOP_BaseMulEAX_CNT = []
		self.listOP_BaseMulEAX_NumOps  = []
		self.listOP_BaseMulEBX = []
		self.listOP_BaseMulEBX_CNT = []
		self.listOP_BaseMulEBX_NumOps  = []
		self.listOP_BaseMulECX = []
		self.listOP_BaseMulECX_CNT = []
		self.listOP_BaseMulECX_NumOps  = []
		self.listOP_BaseMulEDX = []
		self.listOP_BaseMulEDX_CNT = []
		self.listOP_BaseMulEDX_NumOps  = []
		self.listOP_BaseMulEDI = []
		self.listOP_BaseMulEDI_CNT = []
		self.listOP_BaseMulEDI_NumOps  = []
		self.listOP_BaseMulESI = []
		self.listOP_BaseMulESI_CNT = []
		self.listOP_BaseMulESI_NumOps  = []
		self.listOP_BaseMulESP = []
		self.listOP_BaseMulESP_CNT = []
		self.listOP_BaseMulESP_NumOps  = []
		self.listOP_BaseMulEBP = []
		self.listOP_BaseMulEBP_CNT = []
		self.listOP_BaseMulEBP_NumOps  = []
		self.listOP_BaseMul_Module  = []
		self.listOP_BaseMulEAX_Module  = []
		self.listOP_BaseMulEBX_Module  = []
		self.listOP_BaseMulECX_Module  = []
		self.listOP_BaseMulEDX_Module  = []
		self.listOP_BaseMulEDI_Module  = []
		self.listOP_BaseMulESI_Module  = []
		self.listOP_BaseMulEBP_Module  = []
		self.listOP_BaseMulESP_Module  = []
		self.listOP_BaseDiv_Module  = []
		self.listOP_BaseDiv = []
		self.listOP_BaseDiv_CNT = []
		self.listOP_BaseDiv_NumOps  = []
		self.listOP_BaseDivEAX = []
		self.listOP_BaseDivEAX_CNT = []
		self.listOP_BaseDivEAX_NumOps  = []
		self.listOP_BaseDivEDX = []
		self.listOP_BaseDivEDX_CNT = []
		self.listOP_BaseDivEDX_NumOps  = []
		self.listOP_BaseDiv_Module  = []
		self.listOP_BaseDivEAX_Module  = []
		self.listOP_BaseDivEDX_Module  = []
		self.listOP_BaseMov = []
		self.listOP_BaseMov_CNT = []
		self.listOP_BaseMov_NumOps  = []
		self.listOP_BaseMovEAX = []
		self.listOP_BaseMovEAX_CNT = []
		self.listOP_BaseMovEAX_NumOps  = []
		self.listOP_BaseMovEBX = []
		self.listOP_BaseMovEBX_CNT = []
		self.listOP_BaseMovEBX_NumOps  = []
		self.listOP_BaseMovECX = []
		self.listOP_BaseMovECX_CNT = []
		self.listOP_BaseMovECX_NumOps  = []
		self.listOP_BaseMovEDX = []
		self.listOP_BaseMovEDX_CNT = []
		self.listOP_BaseMovEDX_NumOps  = []
		self.listOP_BaseMovEDI = []
		self.listOP_BaseMovEDI_CNT = []
		self.listOP_BaseMovEDI_NumOps  = []
		self.listOP_BaseMovESI = []
		self.listOP_BaseMovESI_CNT = []
		self.listOP_BaseMovESI_NumOps  = []
		self.listOP_BaseMovESP = []
		self.listOP_BaseMovESP_CNT = []
		self.listOP_BaseMovESP_NumOps  = []
		self.listOP_BaseMovEBP = []
		self.listOP_BaseMovEBP_CNT = []
		self.listOP_BaseMovEBP_NumOps  = []
		self.listOP_BaseMov_Module = []
		self.listOP_BaseMovEAX_Module = []
		self.listOP_BaseMovEBX_Module = []
		self.listOP_BaseMovECX_Module = []
		self.listOP_BaseMovEDX_Module = []
		self.listOP_BaseMovESI_Module = []
		self.listOP_BaseMovEDI_Module = []
		self.listOP_BaseMovEBP_Module = []
		self.listOP_BaseMovESP_Module = []
		self.listOP_BaseMovShuf = []
		self.listOP_BaseMovShuf_CNT = []
		self.listOP_BaseMovShuf_NumOps  = []
		self.listOP_BaseMovShufEAX = []
		self.listOP_BaseMovShufEAX_CNT = []
		self.listOP_BaseMovShufEAX_NumOps  = []
		self.listOP_BaseMovShufEBX = []
		self.listOP_BaseMovShufEBX_CNT = []
		self.listOP_BaseMovShufEBX_NumOps  = []
		self.listOP_BaseMovShufECX = []
		self.listOP_BaseMovShufECX_CNT = []
		self.listOP_BaseMovShufECX_NumOps  = []
		self.listOP_BaseMovShufEDX = []
		self.listOP_BaseMovShufEDX_CNT = []
		self.listOP_BaseMovShufEDX_NumOps  = []
		self.listOP_BaseMovShufEDI = []
		self.listOP_BaseMovShufEDI_CNT = []
		self.listOP_BaseMovShufEDI_NumOps  = []
		self.listOP_BaseMovShufESI = []
		self.listOP_BaseMovShufESI_CNT = []
		self.listOP_BaseMovShufESI_NumOps  = []
		self.listOP_BaseMovShufESP = []
		self.listOP_BaseMovShufESP_CNT = []
		self.listOP_BaseMovShufESP_NumOps  = []
		self.listOP_BaseMovShufEBP = []
		self.listOP_BaseMovShufEBP_CNT = []
		self.listOP_BaseMovShufEBP_NumOps  = []
		self.listOP_BaseMovShuf_Module = []
		self.listOP_BaseMovShufEAX_Module = []
		self.listOP_BaseMovShufEBX_Module = []
		self.listOP_BaseMovShufECX_Module = []
		self.listOP_BaseMovShufEDX_Module = []
		self.listOP_BaseMovShufESI_Module = []
		self.listOP_BaseMovShufEDI_Module = []
		self.listOP_BaseMovShufEBP_Module = []
		self.listOP_BaseMovShufESP_Module = []
		self.listOP_BaseMovDeref = []
		self.listOP_BaseMovDeref_CNT = []
		self.listOP_BaseMovDeref_NumOps = []
		self.listOP_BaseMovDeref_Module = []
		self.listOP_BaseMovDerefEAX= []
		self.listOP_BaseMovDerefEAX_CNT = []
		self.listOP_BaseMovDerefEAX_NumOps = []
		self.listOP_BaseMovDerefEAX_Module = []
		self.listOP_BaseMovDerefEBX = []
		self.listOP_BaseMovDerefEBX_CNT = []
		self.listOP_BaseMovDerefEBX_NumOps = []
		self.listOP_BaseMovDerefEBX_Module = []
		self.listOP_BaseMovDerefECX = []
		self.listOP_BaseMovDerefECX_CNT = []
		self.listOP_BaseMovDerefECX_NumOps = []
		self.listOP_BaseMovDerefECX_Module = []
		self.listOP_BaseMovDerefEDX = []
		self.listOP_BaseMovDerefEDX_CNT = []
		self.listOP_BaseMovDerefEDX_NumOps = []
		self.listOP_BaseMovDerefEDX_Module = []
		self.listOP_BaseMovDerefESI = []
		self.listOP_BaseMovDerefESI_CNT = []
		self.listOP_BaseMovDerefESI_NumOps = []
		self.listOP_BaseMovDerefESI_Module = []
		self.listOP_BaseMovDerefEDI = []
		self.listOP_BaseMovDerefEDI_CNT = []
		self.listOP_BaseMovDerefEDI_NumOps = []
		self.listOP_BaseMovDerefEDI_Module = []
		self.listOP_BaseMovDerefESP = []
		self.listOP_BaseMovDerefESP_CNT = []
		self.listOP_BaseMovDerefESP_NumOps = []
		self.listOP_BaseMovDerefESP_Module = []
		self.listOP_BaseMovDerefEBP = []
		self.listOP_BaseMovDerefEBP_CNT = []
		self.listOP_BaseMovDerefEBP_NumOps = []
		self.listOP_BaseMovDerefEBP_Module = []
		self.listOP_BaseMovVal = []
		self.listOP_BaseMovVal_CNT = []
		self.listOP_BaseMovVal_NumOps  = []
		self.listOP_BaseMovValEAX = []
		self.listOP_BaseMovValEAX_CNT = []
		self.listOP_BaseMovValEAX_NumOps  = []
		self.listOP_BaseMovValEBX = []
		self.listOP_BaseMovValEBX_CNT = []
		self.listOP_BaseMovValEBX_NumOps  = []
		self.listOP_BaseMovValECX = []
		self.listOP_BaseMovValECX_CNT = []
		self.listOP_BaseMovValECX_NumOps  = []
		self.listOP_BaseMovValEDX = []
		self.listOP_BaseMovValEDX_CNT = []
		self.listOP_BaseMovValEDX_NumOps  = []
		self.listOP_BaseMovValEDI = []
		self.listOP_BaseMovValEDI_CNT = []
		self.listOP_BaseMovValEDI_NumOps  = []
		self.listOP_BaseMovValESI = []
		self.listOP_BaseMovValESI_CNT = []
		self.listOP_BaseMovValESI_NumOps  = []
		self.listOP_BaseMovValESP = []
		self.listOP_BaseMovValESP_CNT = []
		self.listOP_BaseMovValESP_NumOps  = []
		self.listOP_BaseMovValEBP = []
		self.listOP_BaseMovValEBP_CNT = []
		self.listOP_BaseMovValEBP_NumOps  = []
		self.listOP_BaseMovVal_Module = []
		self.listOP_BaseMovValEAX_Module = []
		self.listOP_BaseMovValEBX_Module = []
		self.listOP_BaseMovValECX_Module = []
		self.listOP_BaseMovValEDX_Module = []
		self.listOP_BaseMovValESI_Module = []
		self.listOP_BaseMovValEDI_Module = []
		self.listOP_BaseMovValEBP_Module = []
		self.listOP_BaseMovValESP_Module = []
		self.listOP_BaseLea = []
		self.listOP_BaseLea_CNT = []
		self.listOP_BaseLea_NumOps  = []
		self.listOP_BaseLeaEAX = []
		self.listOP_BaseLeaEAX_CNT = []
		self.listOP_BaseLeaEAX_NumOps  = []
		self.listOP_BaseLeaEBX = []
		self.listOP_BaseLeaEBX_CNT = []
		self.listOP_BaseLeaEBX_NumOps  = []
		self.listOP_BaseLeaECX = []
		self.listOP_BaseLeaECX_CNT = []
		self.listOP_BaseLeaECX_NumOps  = []
		self.listOP_BaseLeaEDX = []
		self.listOP_BaseLeaEDX_CNT = []
		self.listOP_BaseLeaEDX_NumOps  = []
		self.listOP_BaseLeaEDI = []
		self.listOP_BaseLeaEDI_CNT = []
		self.listOP_BaseLeaEDI_NumOps  = []
		self.listOP_BaseLeaESI = []
		self.listOP_BaseLeaESI_CNT = []
		self.listOP_BaseLeaESI_NumOps  = []
		self.listOP_BaseLeaESP = []
		self.listOP_BaseLeaESP_CNT = []
		self.listOP_BaseLeaESP_NumOps  = []
		self.listOP_BaseLeaEBP = []
		self.listOP_BaseLeaEBP_CNT = []
		self.listOP_BaseLeaEBP_NumOps  = []
		self.listOP_BaseLea_Module = []
		self.listOP_BaseLeaEAX_Module = []
		self.listOP_BaseLeaEBX_Module = []
		self.listOP_BaseLeaECX_Module = []
		self.listOP_BaseLeaEDX_Module = []
		self.listOP_BaseLeaESI_Module = []
		self.listOP_BaseLeaEDI_Module = []
		self.listOP_BaseLeaEBP_Module = []
		self.listOP_BaseLeaESP_Module = []
		self.listOP_BasePush = []
		self.listOP_BasePush_CNT = []
		self.listOP_BasePush_NumOps  = []
		self.listOP_BasePushEAX = []
		self.listOP_BasePushEAX_CNT = []
		self.listOP_BasePushEAX_NumOps  = []
		self.listOP_BasePushEBX = []
		self.listOP_BasePushEBX_CNT = []
		self.listOP_BasePushEBX_NumOps  = []
		self.listOP_BasePushECX = []
		self.listOP_BasePushECX_CNT = []
		self.listOP_BasePushECX_NumOps  = []
		self.listOP_BasePushEDX = []
		self.listOP_BasePushEDX_CNT = []
		self.listOP_BasePushEDX_NumOps  = []
		self.listOP_BasePushEDI = []
		self.listOP_BasePushEDI_CNT = []
		self.listOP_BasePushEDI_NumOps  = []
		self.listOP_BasePushESI = []
		self.listOP_BasePushESI_CNT = []
		self.listOP_BasePushESI_NumOps  = []
		self.listOP_BasePushESP = []
		self.listOP_BasePushESP_CNT = []
		self.listOP_BasePushESP_NumOps  = []
		self.listOP_BasePushEBP = []
		self.listOP_BasePushEBP_CNT = []
		self.listOP_BasePushEBP_NumOps  = []
		self.listOP_BasePush_Module = []
		self.listOP_BasePushEAX_Module = []
		self.listOP_BasePushEBX_Module = []
		self.listOP_BasePushECX_Module = []
		self.listOP_BasePushEDX_Module = []
		self.listOP_BasePushESI_Module = []
		self.listOP_BasePushEDI_Module = []
		self.listOP_BasePushEBP_Module = []
		self.listOP_BasePushESP_Module = []
		self.listOP_RET_Pop =[]
		self.listOP_RET_Pop_CNT =[]
		self.listOP_RET_Pop_NumOps =[]
		self.listOP_RET_Pop_Module =[]
		self.listOP_RET_Pop_NumOps =[]
		self.listOP_RET_Pop_EAX_NumOps =[]
		self.listOP_RET_Pop_EBX_NumOps =[]
		self.listOP_RET_Pop_ECX_NumOps =[]
		self.listOP_RET_Pop_EDX_NumOps =[]
		self.listOP_RET_Pop_EDI_NumOps =[]
		self.listOP_RET_Pop_ESI_NumOps =[]
		self.listOP_RET_Pop_ESP_NumOps =[]
		self.listOP_RET_Pop_EBP_NumOps =[]
		self.listOP_RET_Pop_EAX =[]
		self.listOP_RET_Pop_EAX_CNT =[]
		self.listOP_RET_Pop_EAX_ =[]
		self.listOP_RET_Pop_EAX_Module =[]
		self.listOP_RET_Pop_EBX =[]
		self.listOP_RET_Pop_EBX_CNT =[]
		self.listOP_RET_Pop_EBX_ =[]
		self.listOP_RET_Pop_EBX_Module =[]
		self.listOP_RET_Pop_ECX =[]
		self.listOP_RET_Pop_ECX_CNT =[]
		self.listOP_RET_Pop_ECX_ =[]
		self.listOP_RET_Pop_ECX_Module =[]
		self.listOP_RET_Pop_EDX =[]
		self.listOP_RET_Pop_EDX_CNT =[]
		self.listOP_RET_Pop_EDX_ =[]
		self.listOP_RET_Pop_EDX_Module =[]
		self.listOP_RET_Pop_EDI =[]
		self.listOP_RET_Pop_EDI_CNT =[]
		self.listOP_RET_Pop_EDI_ =[]
		self.listOP_RET_Pop_EDI_Module =[]
		self.listOP_RET_Pop_ESI =[]
		self.listOP_RET_Pop_ESI_CNT =[]
		self.listOP_RET_Pop_ESI_ =[]
		self.listOP_RET_Pop_ESI_Module =[]
		self.listOP_RET_Pop_ESP =[]
		self.listOP_RET_Pop_ESP_CNT =[]
		self.listOP_RET_Pop_ESP_ =[]
		self.listOP_RET_Pop_ESP_Module =[]
		self.listOP_RET_Pop_EBP =[]
		self.listOP_RET_Pop_EBP_CNT =[]
		self.listOP_RET_Pop_EBP_ =[]
		self.listOP_RET_Pop_EBP_Module =[]
		self.listOP_BasePop = []
		self.listOP_BasePop_CNT = []
		self.listOP_BasePop_NumOps  = []
		self.listOP_BasePopEAX = []
		self.listOP_BasePopEAX_CNT = []
		self.listOP_BasePopEAX_NumOps  = []
		self.listOP_BasePopEBX = []
		self.listOP_BasePopEBX_CNT = []
		self.listOP_BasePopEBX_NumOps  = []
		self.listOP_BasePopECX = []
		self.listOP_BasePopECX_CNT = []
		self.listOP_BasePopECX_NumOps  = []
		self.listOP_BasePopEDX = []
		self.listOP_BasePopEDX_CNT = []
		self.listOP_BasePopEDX_NumOps  = []
		self.listOP_BasePopEDI = []
		self.listOP_BasePopEDI_CNT = []
		self.listOP_BasePopEDI_NumOps  = []
		self.listOP_BasePopESI = []
		self.listOP_BasePopESI_CNT = []
		self.listOP_BasePopESI_NumOps  = []
		self.listOP_BasePopESP = []
		self.listOP_BasePopESP_CNT = []
		self.listOP_BasePopESP_NumOps  = []
		self.listOP_BasePopEBP = []
		self.listOP_BasePopEBP_CNT = []
		self.listOP_BasePopEBP_NumOps  = []
		self.listOP_BasePop_Module = []
		self.listOP_BaseStackPivot = []
		self.listOP_BaseStackPivot_CNT = []
		self.listOP_BaseStackPivot_NumOps = []
		self.listOP_BaseStackPivot_Module = []
		self.listOP_BaseStackPivot_Special = []
		self.listOP_BaseStackPivotEAX = []
		self.listOP_BaseStackPivotEAX_CNT = []
		self.listOP_BaseStackPivotEAX_NumOps = []
		self.listOP_BaseStackPivotEAX_Module = []
		self.listOP_BaseStackPivotEAX_Special = []
		self.listOP_BaseStackPivotEBX = []
		self.listOP_BaseStackPivotEBX_CNT = []
		self.listOP_BaseStackPivotEBX_NumOps = []
		self.listOP_BaseStackPivotEBX_Module = []
		self.listOP_BaseStackPivotEBX_Special = []
		self.listOP_BaseStackPivotECX = []
		self.listOP_BaseStackPivotECX_CNT = []
		self.listOP_BaseStackPivotECX_NumOps = []
		self.listOP_BaseStackPivotECX_Module = []
		self.listOP_BaseStackPivotECX_Special = []
		self.listOP_BaseStackPivotEDX = []
		self.listOP_BaseStackPivotEDX_CNT = []
		self.listOP_BaseStackPivotEDX_NumOps = []
		self.listOP_BaseStackPivotEDX_Module = []
		self.listOP_BaseStackPivotEDX_Special = []
		self.listOP_BaseStackPivotEDI = []
		self.listOP_BaseStackPivotEDI_CNT = []
		self.listOP_BaseStackPivotEDI_NumOps = []
		self.listOP_BaseStackPivotEDI_Module = []
		self.listOP_BaseStackPivotEDI_Special = []
		self.listOP_BaseStackPivotESI = []
		self.listOP_BaseStackPivotESI_CNT = []
		self.listOP_BaseStackPivotESI_NumOps = []
		self.listOP_BaseStackPivotESI_Module = []
		self.listOP_BaseStackPivotESI_Special = []
		self.listOP_BaseStackPivotEBP = []
		self.listOP_BaseStackPivotEBP_CNT = []
		self.listOP_BaseStackPivotEBP_NumOps = []
		self.listOP_BaseStackPivotEBP_Module = []
		self.listOP_BaseStackPivotEBP_Special = []
		self.listOP_BaseStackPivotESP = []
		self.listOP_BaseStackPivotESP_CNT = []
		self.listOP_BaseStackPivotESP_NumOps = []
		self.listOP_BaseStackPivotESP_Module = []
		self.listOP_BaseStackPivotESP_Special = []
		self.listOP_BasePopEAX_Module = []
		self.listOP_BasePopEBX_Module = []
		self.listOP_BasePopECX_Module = []
		self.listOP_BasePopEDX_Module = []
		self.listOP_BasePopEDI_Module = []
		self.listOP_BasePopESI_Module = []
		self.listOP_BasePopEBP_Module = []
		self.listOP_BasePopESP_Module = []
		self.listOP_BaseInc = []
		self.listOP_BaseInc_CNT = []
		self.listOP_BaseInc_NumOps  = []
		self.listOP_BaseIncEAX = []
		self.listOP_BaseIncEAX_CNT = []
		self.listOP_BaseIncEAX_NumOps  = []
		self.listOP_BaseIncEBX = []
		self.listOP_BaseIncEBX_CNT = []
		self.listOP_BaseIncEBX_NumOps  = []
		self.listOP_BaseIncECX = []
		self.listOP_BaseIncECX_CNT = []
		self.listOP_BaseIncECX_NumOps  = []
		self.listOP_BaseIncEDX = []
		self.listOP_BaseIncEDX_CNT = []
		self.listOP_BaseIncEDX_NumOps  = []
		self.listOP_BaseIncEDI = []
		self.listOP_BaseIncEDI_CNT = []
		self.listOP_BaseIncEDI_NumOps  = []
		self.listOP_BaseIncESI = []
		self.listOP_BaseIncESI_CNT = []
		self.listOP_BaseIncESI_NumOps  = []
		self.listOP_BaseIncESP = []
		self.listOP_BaseIncESP_CNT = []
		self.listOP_BaseIncESP_NumOps  = []
		self.listOP_BaseIncEBP = []
		self.listOP_BaseIncEBP_CNT = []
		self.listOP_BaseIncEBP_NumOps  = []
		self.listOP_BaseInc_Module = []
		self.listOP_BaseIncEAX_Module = []
		self.listOP_BaseIncEBX_Module = []
		self.listOP_BaseIncECX_Module = []
		self.listOP_BaseIncEDX_Module = []
		self.listOP_BaseIncEDI_Module = []
		self.listOP_BaseIncESI_Module = []
		self.listOP_BaseIncEBP_Module = []
		self.listOP_BaseIncESP_Module = []
		self.listOP_BaseDec = []
		self.listOP_BaseDec_CNT = []
		self.listOP_BaseDec_NumOps  = []
		self.listOP_BaseDecEAX = []
		self.listOP_BaseDecEAX_CNT = []
		self.listOP_BaseDecEAX_NumOps  = []
		self.listOP_BaseDecEBX = []
		self.listOP_BaseDecEBX_CNT = []
		self.listOP_BaseDecEBX_NumOps  = []
		self.listOP_BaseDecECX = []
		self.listOP_BaseDecECX_CNT = []
		self.listOP_BaseDecECX_NumOps  = []
		self.listOP_BaseDecEDX = []
		self.listOP_BaseDecEDX_CNT = []
		self.listOP_BaseDecEDX_NumOps  = []
		self.listOP_BaseDecEDI = []
		self.listOP_BaseDecEDI_CNT = []
		self.listOP_BaseDecEDI_NumOps  = []
		self.listOP_BaseDecESI = []
		self.listOP_BaseDecESI_CNT = []
		self.listOP_BaseDecESI_NumOps  = []
		self.listOP_BaseDecESP = []
		self.listOP_BaseDecESP_CNT = []
		self.listOP_BaseDecESP_NumOps  = []
		self.listOP_BaseDecEBP = []
		self.listOP_BaseDecEBP_CNT = []
		self.listOP_BaseDecEBP_NumOps  = []
		self.listOP_BaseDec_Module = []
		self.listOP_BaseDecEAX_Module = []
		self.listOP_BaseDecEBX_Module = []
		self.listOP_BaseDecECX_Module = []
		self.listOP_BaseDecEDX_Module = []
		self.listOP_BaseDecESI_Module = []
		self.listOP_BaseDecEDI_Module = []
		self.listOP_BaseDecEBP_Module = []
		self.listOP_BaseDecESP_Module = []
		self.listOP_BaseXchg = []
		self.listOP_BaseXchg_CNT = []
		self.listOP_BaseXchg_NumOps  = []
		self.listOP_BaseXchgEAX = []
		self.listOP_BaseXchgEAX_CNT = []
		self.listOP_BaseXchgEAX_NumOps  = []
		self.listOP_BaseXchgEBX = []
		self.listOP_BaseXchgEBX_CNT = []
		self.listOP_BaseXchgEBX_NumOps  = []
		self.listOP_BaseXchgECX = []
		self.listOP_BaseXchgECX_CNT = []
		self.listOP_BaseXchgECX_NumOps  = []
		self.listOP_BaseXchgEDX = []
		self.listOP_BaseXchgEDX_CNT = []
		self.listOP_BaseXchgEDX_NumOps  = []
		self.listOP_BaseXchgEDI = []
		self.listOP_BaseXchgEDI_CNT = []
		self.listOP_BaseXchgEDI_NumOps  = []
		self.listOP_BaseXchgESI = []
		self.listOP_BaseXchgESI_CNT = []
		self.listOP_BaseXchgESI_NumOps  = []
		self.listOP_BaseXchgESP = []
		self.listOP_BaseXchgESP_CNT = []
		self.listOP_BaseXchgESP_NumOps  = []
		self.listOP_BaseXchgEBP = []
		self.listOP_BaseXchgEBP_CNT = []
		self.listOP_BaseXchgEBP_NumOps  = []
		self.listOP_BaseXchg_Module = []
		self.listOP_BaseXchgEAX_Module = []
		self.listOP_BaseXchgEBX_Module = []
		self.listOP_BaseXchgECX_Module = []
		self.listOP_BaseXchgEDX_Module = []
		self.listOP_BaseXchgEDI_Module = []
		self.listOP_BaseXchgESI_Module = []
		self.listOP_BaseXchgEBP_Module = []
		self.listOP_BaseXchgESP_Module = []
		self.listOP_BaseShiftLeft = []
		self.listOP_BaseShiftLeft_CNT = []
		self.listOP_BaseShiftLeft_NumOps  = []
		self.listOP_BaseShiftLeft_Module = []
		self.listOP_BaseShiftRight = []
		self.listOP_BaseShiftRight_CNT = []
		self.listOP_BaseShiftRight_NumOps  = []
		self.listOP_BaseShiftRight_Module = []
		self.listOP_BaseRotLeft = []
		self.listOP_BaseRotLeft_CNT = []
		self.listOP_BaseRotLeft_NumOps  = []
		self.listOP_BaseRotLeft_Module = []
		self.listOP_BaseRotRight = []
		self.listOP_BaseRotRight_CNT = []
		self.listOP_BaseRotRight_NumOps  = []
		self.listOP_BaseRotRight_Module = []
		self.SpOutGadgetAll = []
		self.SpOutNumBytesAll = []
		self.SpOutGadgetEAX = []
		self.SpOutNumBytesEAX = []
		self.SpOutGadgetEBX = []
		self.SpOutNumBytesEBX = []
		self.SpOutGadgetECX = []
		self.SpOutNumBytesECX = []
		self.SpOutGadgetEDX = []
		self.SpOutNumBytesEDX = []
		self.SpOutGadgetEDI = []
		self.SpOutNumBytesEDI = []
		self.SpOutGadgetESI = []
		self.SpOutNumBytesESI = []
		self.SpOutGadgetEBP = []
		self.SpOutNumBytesEBP = []
		self.SpOutGadgetESP = []
		self.SpOutNumBytesESP = []
		self.specialPOPGadget = []
		self.specialPOPBytes = []
		self.specialPOPGadgetBest = []
		self.specialPOPBytesBest = []
		self.specialPOPGadgetRet  =[]
		self.specialPOPBytesRet   =[]

		self.specialPOPGadgetRetEAX  =[]
		self.specialPOPBytesRetEAX   =[]
		self.specialPOPGadgetRetBestEAX  = []
		self.specialPOPBytesRetBestEAX =[]
		self.specialPOPGadgetRet  =[]
		self.specialPOPBytesRet   =[]
		self.specialPOPBytesRetTup =[]
		self.specialPOPGadgetRetEBX =[]
		self.specialPOPBytesRetEBX =[]
		self.specialPOPGadgetRetBestEBX =[]
		self.specialPOPBytesRetBestEBX =[]
		self.specialPOPGadgetRetECX =[]
		self.specialPOPBytesRetECX =[]
		self.specialPOPGadgetRetBestECX =[]
		self.specialPOPBytesRetBestECX =[]
		self.specialPOPGadgetRetEDX =[]
		self.specialPOPBytesRetEDX =[]
		self.specialPOPGadgetRetBestEDX =[]
		self.specialPOPBytesRetBestEDX =[]
		self.specialPOPGadgetRetEDI =[]
		self.specialPOPBytesRetEDI =[]
		self.specialPOPGadgetRetBestEDI =[]
		self.specialPOPBytesRetBestEDI =[]
		self.specialPOPGadgetRetESI =[]
		self.specialPOPBytesRetESI =[]
		self.specialPOPGadgetRetBestESI =[]
		self.specialPOPBytesRetBestESI =[]
		self.specialPOPGadgetRetESP =[]
		self.specialPOPBytesRetESP =[]
		self.specialPOPGadgetRetBestESP =[]
		self.specialPOPBytesRetBestESP =[]
		self.specialPOPGadgetRetEBP =[]
		self.specialPOPBytesRetEBP =[]
		self.specialPOPGadgetRetBestEBP =[]
		self.specialPOPBytesRetBestEBP =[]
		self.specialPOPGadgetBestEAX = []
		self.specialPOPBytesBestEAX = []
		self.specialPOPGadgetBestEBX = []
		self.specialPOPBytesBestEBX = []
		self.specialPOPGadgetBestECX = []
		self.specialPOPBytesBestECX = []
		self.specialPOPGadgetBestEDX = []
		self.specialPOPBytesBestEDX = []
		self.specialPOPGadgetBestEDI = []
		self.specialPOPBytesBestEDI = []
		self.specialPOPGadgetBestESI = []
		self.specialPOPBytesBestESI = []
		self.specialPOPGadgetBestEBP = []
		self.specialPOPBytesBestEBP = []
		self.specialPOPGadgetBestESP = []
		self.specialPOPBytesBestESP = []
		self.specialPOPGadgetEAX = []
		self.specialPOPBytesEAX = []
		self.specialPOPGadgetEBX = []
		self.specialPOPBytesEBX = []
		self.specialPOPGadgetECX = []
		self.specialPOPBytesECX = []
		self.specialPOPGadgetEDX = []
		self.specialPOPBytesEDX = []
		self.specialPOPGadgetEDI = []
		self.specialPOPBytesEDI = []
		self.specialPOPGadgetESI = []
		self.specialPOPBytesESI = []
		self.specialPOPGadgetEBP = []
		self.specialPOPBytesEBP = []
		self.specialPOPGadgetESP = []
		self.specialPOPBytesESP = []
		self.listOP_RET = []
		self.listOP_RET_CNT = []
		self.listOP_RET_NumOps = []
		self.listOP_RET_Module = []
	

# end classs
objs = []
obj = MyBytes()
obj._init_()
objs.append(obj)

def noApi_MS(DLLs):
	global Remove
	for dll in DLLs:
		matchObj = re.match( r'\bapi-ms\b', dll, re.M|re.I) # This is in system32 or wow64 /downlevel - not typically loaded at start. This is found by recursively searching imports and more likely than not will not be loaded right away. Thus, it is excluded.
		if matchObj:
			Remove.append(dll)
		matchObj = re.match( r'\bpython\b', dll, re.M|re.I)  # Typically this is an error from not finding the correct  file location
		if matchObj:
			Remove.append(dll)
def listReducer(dlls):	
	fun2=  list(OrderedDict.fromkeys(dlls))
	return fun2
def getDLLs():
	global PE_DLLS
	name = ""
	try:
		for entry in pe.DIRECTORY_ENTRY_IMPORT:
			print entry.dll
			name = entry.dll
			if entry.dll == "WSOCK32.dll":
				name = "ws2_32.dll"
			PE_DLLS.append(name)
	except:
		pass
def getDLLs2(dll):
	global PE_DLLS
	name = ""
	for entry in pe.DIRECTORY_ENTRY_IMPORT:
		print entry.dll
		name = entry.dll
		if entry.dll == "WSOCK32.dll":
			name = "ws2_32.dll"
		PE_DLLS.append(name)
def extractDLLNew(dllName):
	global o
	global index
	global  newpath
	global ans
	global PE_Protect
	global PE_path
		# A very small portin of this loadlibrary comes from: https://www.programcreek.com/python/example/53932/ctypes.wintypes.HANDLE
		# All of the elaborate loading through alternate means is entirely original
	#index = 0
	print dllName
#remove if could not be found
	try:
		dllHandle = win32api.LoadLibraryEx(dllName, 0, win32con.LOAD_LIBRARY_AS_DATAFILE)
		windll.kernel32.GetModuleHandleW.restype = wintypes.HMODULE
		windll.kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
		windll.kernel32.GetModuleFileNameW.restype = wintypes.DWORD
		windll.kernel32.GetModuleFileNameW.argtypes = [wintypes.HANDLE, wintypes.LPWSTR, wintypes.DWORD]
		h_module_base = windll.kernel32.GetModuleHandleW(dllName)
		module_path = wintypes.create_unicode_buffer(255)
		windll.kernel32.GetModuleFileNameW(h_module_base, module_path, 255)
		pe = pefile.PE(module_path.value)
		win32api.FreeLibrary(dllHandle)

		if h_module_base is None:
			directory = r'C:\Program Files\testing'  
			directory = PE_path
			newpath = os.path.abspath(os.path.join(directory, dllName))
			if os.path.exists(newpath):
				module_path.value = newpath
				ans = newpath
			else:
				if bit32:
					directory = r'C:\Windows\SysWOW64'
					newpath = os.path.abspath(os.path.join(directory, dllName))
					if os.path.exists(newpath):
						module_path.value = newpath
						ans = newpath
					else:
						print "\t\tNote: " + dllName + " will be excluded. Please scan this manually if needed."
						Remove.append(dllName)
				if not bit32:
					directory = r'C:\Windows\System32'
					newpath = os.path.abspath(os.path.join(directory, dllName))
					if os.path.exists(newpath):
						module_path.value = newpath
						ans = newpath
					else:
						print "\t\tNote: " + dllName + " will be excluded. Please scan this manually if needed."
						Remove.append(dllName)
		head, tail = os.path.split(module_path.value)
		if tail != dllName:
			print "\tNote: " + str(tail) + " is being searched instead of " + dllName + "."
			PE_DLLS[index] = tail
			Remove.append(dllName)
		ans = module_path.value

		objs[o].protect = str(dllName) + "\t"
		objs[o].depStatus = "\tDEP: " + str(dep())
		objs[o].aslrStatus = "\tASLR: " + str(aslr())
		objs[o].sehSTATUS = "\tSAFESEH: " + str(seh())
		objs[o].CFGstatus = "\tCFG: " + str(CFG())
		objs[o].protect = objs[o].protect + objs[o].depStatus + objs[o].aslrStatus + objs[o].sehSTATUS + objs[o].CFGstatus
		DLL_Protect.append(objs[o].protect)
		PE_Protect = PE_Protect + str(objs[o].protect)
		print objs[o].protect

		index += 1
	except:
		directory = r'C:\Program Files\testing'  #hardcoded testing, made irrelevant by next line
		directory = PE_path
		newpath = os.path.abspath(os.path.join(directory, dllName))
		if os.path.exists(newpath):
			ans = os.path.abspath(os.path.join(directory, dllName))
		else:
			if bit32:
				directory = r'C:\Windows\SysWOW64'
				newpath = os.path.abspath(os.path.join(directory, dllName))
				if os.path.exists(newpath):
					ans = os.path.abspath(os.path.join(directory, dllName))
				else:
					print "\t\tNote: " + dllName + " will be excluded. Please scan this manually if needed."
					Remove.append(dllName)
			if not bit32:
				directory = r'C:\Windows\System32'
				newpath = os.path.abspath(os.path.join(directory, dllName))
				if os.path.exists(newpath):
					ans = os.path.abspath(os.path.join(directory, dllName))
				else:
					print "\t\tNote: " + dllName + " will be excluded. Please scan this manually if needed."
					Remove.append(dllName)

		objs[o].protect = str(dllName) + "\t"
		objs[o].depStatus = "\tDEP: " + str(dep())
		objs[o].aslrStatus = "\tASLR: " + str(aslr())
		objs[o].sehSTATUS = "\tSAFESEH: " + str(seh())
		objs[o].CFGstatus = "\tCFG: " + str(CFG())
		objs[o].protect = objs[o].protect + objs[o].depStatus + objs[o].aslrStatus + objs[o].sehSTATUS + objs[o].CFGstatus
		DLL_Protect.append(objs[o].protect)

		PE_Protect = PE_Protect + str(objs[o].protect)
		print objs[o].protect

		index += 1
		pass
	print  "\t* " + str(ans)
	return ans

def digDeeper(PE_DLL):
	global PE_DLLS2
	print ""#"in dig deeper"
	print PE_DLL
	sp()
 	for dll in PE_DLL:
 		newpath = ""
 		print newpath
 		sp()
 		newpath = extractDLLNew(dll)
 		print newpath
 		sp()
 		pe = pefile.PE(newpath)
		name = ""
		try:
			for entry in pe.DIRECTORY_ENTRY_IMPORT:
				name = entry.dll
				if entry.dll == "WSOCK32.dll":
					name = "ws2_32.dll"
				PE_DLLS2.append(name)
		except:
			pass
def moreDLLs(): 
	global PE_DLLS
	global PE_DLLS2
	global index
	if levelTwo:
		index=0
		print "before start of dig deeper"
		print PE_DLLS
		sp()
		digDeeper(PE_DLLS)
		i=0
		PE_DLLS2 = listReducer(PE_DLLS2)
		for dll in PE_DLLS2:
			test = extractDLL(PE_DLLS2[i])
			i +=1
		PE_DLLS2 = listReducer(PE_DLLS2)
		PE_DLLS.extend(PE_DLLS2)
		PE_DLLS = listReducer(PE_DLLS)
def clearHashChecker():
	hashchecker[:]=[]
	hashcheckerPre[:]=[]
def clearAllObject(): #4
	global o
	print "clearing primary objects..."
	sp()
	o = 0
	for f in objs:
		objs[o].listOP_JMP_EAX2[:] = []
		objs[o].listOP_JMP_EBX[:] = []
		objs[o].listOP_JMP_ECX[:] = []
		objs[o].listOP_JMP_EDX[:] = []
		objs[o].listOP_JMP_ESI[:] = []
		objs[o].listOP_JMP_EDI[:] = []
		objs[o].listOP_JMP_ESP[:] = []  
		objs[o].listOP_JMP_EBP[:] = []
		objs[o].listOP_JMP_EAX_CNT[:] = []
		objs[o].listOP_JMP_EBX_CNT[:] = []
		objs[o].listOP_JMP_ECX_CNT[:] = []
		objs[o].listOP_JMP_EDX_CNT[:] = []
		objs[o].listOP_JMP_ESI_CNT[:] = []
		objs[o].listOP_JMP_EDI_CNT[:] = []
		objs[o].listOP_JMP_ESP_CNT[:] = []  
		objs[o].listOP_JMP_EBP_CNT[:] = []

		objs[o].listOP_JMP_EAX_NumOps[:] = []
		objs[o].listOP_JMP_EBX_NumOps[:] = []
		objs[o].listOP_JMP_ECX_NumOps[:] = []
		objs[o].listOP_JMP_EDX_NumOps[:] = []
		objs[o].listOP_JMP_ESI_NumOps[:] = []
		objs[o].listOP_JMP_EDI_NumOps[:] = []
		objs[o].listOP_JMP_ESP_NumOps[:] = []  
		objs[o].listOP_JMP_EBP_NumOps[:] = []

		objs[o].listOP_RET [:] = []
		objs[o].listOP_RET_CNT [:] = []
		objs[o].listOP_RET_NumOps [:] = []
		objs[o].listOP_RET_Module [:] = []
		objs[o].listOP_CALL_EAX[:] = []
		objs[o].listOP_CALL_EBX[:] = []
		objs[o].listOP_CALL_ECX[:] = []
		objs[o].listOP_CALL_EDX[:] = []
		objs[o].listOP_CALL_EDI[:] = []
		objs[o].listOP_CALL_ESI[:] = []
		objs[o].listOP_CALL_EBP[:] = []
		objs[o].listOP_CALL_EAX_CNT[:] = []
		objs[o].listOP_CALL_EBX_CNT[:] = []
		objs[o].listOP_CALL_ECX_CNT[:] = []
		objs[o].listOP_CALL_EDX_CNT[:] = []
		objs[o].listOP_CALL_ESI_CNT[:] = []
		objs[o].listOP_CALL_EDI_CNT[:] = []
		objs[o].listOP_CALL_EBP_CNT[:] = []
		objs[o].listOP_CALL_EAX_Module[:] = []
		objs[o].listOP_CALL_EBX_Module[:] = []
		objs[o].listOP_CALL_ECX_Module[:] = []
		objs[o].listOP_CALL_EDX_Module[:] = []
		objs[o].listOP_CALL_ESI_Module[:] = []
		objs[o].listOP_CALL_EDI_Module[:] = []
		objs[o].listOP_CALL_ESP_Module[:] = []
		objs[o].listOP_CALL_EBP_Module[:] = []
		objs[o].listOP_CALL_EAX_NumOps[:] = []
		objs[o].listOP_CALL_EBX_NumOps[:] = []
		objs[o].listOP_CALL_ECX_NumOps[:] = []
		objs[o].listOP_CALL_EDX_NumOps[:] = []
		objs[o].listOP_CALL_ESI_NumOps[:] = []
		objs[o].listOP_CALL_EDI_NumOps[:] = []
		objs[o].listOP_CALL_ESP_NumOps[:] = []
		objs[o].listOP_CALL_EBP_NumOps[:] = []
		objs[o].listOP_JMP_EAX_Module[:] = []
		objs[o].listOP_JMP_EBX_Module[:] = []
		objs[o].listOP_JMP_ECX_Module[:] = []
		objs[o].listOP_JMP_EDX_Module[:] = []
		objs[o].listOP_JMP_ESI_Module[:] = []
		objs[o].listOP_JMP_EDI_Module[:] = []
		objs[o].listOP_JMP_ESP_Module[:] = []
		objs[o].listOP_JMP_EBP_Module[:] = []
		o = o +1
	o=0
	print "Clearing complete."
	sp()


def addListBase(address, valCount, NumOpsDis, modName):
#	print "addlistbase"
	listOP_Base.append(address)
	listOP_Base_CNT.append(valCount)
	listOP_Base_NumOps.append(NumOpsDis)
	listOP_Base_Module.append(modName)	

def addListBaseDG(address, valCount, numOps, modName):
	objs[o].listOP_BaseDG.append(address)
	objs[o].listOP_BaseDG_CNT.append(valCount)
	objs[o].listOP_BaseDG_NumOps.append(numOps)
	objs[o].listOP_BaseDG_Module.append(modName)

def addListBaseDG_EAX(address, valCount, numOps, modName):
	objs[o].listOP_BaseDG_EAX.append(address)
	objs[o].listOP_BaseDG_CNT_EAX.append(valCount)
	objs[o].listOP_BaseDG_NumOps_EAX.append(numOps)
	objs[o].listOP_BaseDG_Module_EAX.append(modName)
def addListBaseDG_EBX(address, valCount, numOps, modName):
	objs[o].listOP_BaseDG_EBX.append(address)
	objs[o].listOP_BaseDG_CNT_EBX.append(valCount)
	objs[o].listOP_BaseDG_NumOps_EBX.append(numOps)
	objs[o].listOP_BaseDG_Module_EBX.append(modName)
def addListBaseDG_ECX(address, valCount, numOps, modName):
	objs[o].listOP_BaseDG_ECX.append(address)
	objs[o].listOP_BaseDG_CNT_ECX.append(valCount)
	objs[o].listOP_BaseDG_NumOps_ECX.append(numOps)
	objs[o].listOP_BaseDG_Module_ECX.append(modName)
def addListBaseDG_EDX(address, valCount, numOps, modName):
	objs[o].listOP_BaseDG_EDX.append(address)
	objs[o].listOP_BaseDG_CNT_EDX.append(valCount)
	objs[o].listOP_BaseDG_NumOps_EDX.append(numOps)
	objs[o].listOP_BaseDG_Module_EDX.append(modName)
def addListBaseDG_EDI(address, valCount, numOps, modName):
	objs[o].listOP_BaseDG_EDI.append(address)
	objs[o].listOP_BaseDG_CNT_EDI.append(valCount)
	objs[o].listOP_BaseDG_NumOps_EDI.append(numOps)
	objs[o].listOP_BaseDG_Module_EDI.append(modName)
def addListBaseDG_ESI(address, valCount, numOps, modName):
	objs[o].listOP_BaseDG_ESI.append(address)
	objs[o].listOP_BaseDG_CNT_ESI.append(valCount)
	objs[o].listOP_BaseDG_NumOps_ESI.append(numOps)
	objs[o].listOP_BaseDG_Module_ESI.append(modName)
def addListBaseDG_EBP(address, valCount, numOps, modName):
	objs[o].listOP_BaseDG_EBP.append(address)
	objs[o].listOP_BaseDG_CNT_EBP.append(valCount)
	objs[o].listOP_BaseDG_NumOps_EBP.append(numOps)
	objs[o].listOP_BaseDG_Module_EBP.append(modName)
def addListBaseDG_ESP(address, valCount, numOps, modName):
	objs[o].listOP_BaseDG_ESP.append(address)
	objs[o].listOP_BaseDG_CNT_ESP.append(valCount)
	objs[o].listOP_BaseDG_NumOps_ESP.append(numOps)
	objs[o].listOP_BaseDG_Module_ESP.append(modName)
def addListBaseDG_EAX_Best(address, valCount, numOps, modName):
	objs[o].listOP_BaseDG_EAX_Best.append(address)
	objs[o].listOP_BaseDG_CNT_EAX_Best.append(valCount)
	objs[o].listOP_BaseDG_NumOps_EAX_Best.append(numOps)
	objs[o].listOP_BaseDG_Module_EAX_Best.append(modName)
def addListBaseDG_EBX_Best(address, valCount, numOps, modName):
	objs[o].listOP_BaseDG_EBX_Best.append(address)
	objs[o].listOP_BaseDG_CNT_EBX_Best.append(valCount)
	objs[o].listOP_BaseDG_NumOps_EBX_Best.append(numOps)
	objs[o].listOP_BaseDG_Module_EBX_Best.append(modName)
def addListBaseDG_ECX_Best(address, valCount, numOps, modName):
	objs[o].listOP_BaseDG_ECX_Best.append(address)
	objs[o].listOP_BaseDG_CNT_ECX_Best.append(valCount)
	objs[o].listOP_BaseDG_NumOps_ECX_Best.append(numOps)
	objs[o].listOP_BaseDG_Module_ECX_Best.append(modName)
def addListBaseDG_EDX_Best(address, valCount, numOps, modName):
	objs[o].listOP_BaseDG_EDX_Best.append(address)
	objs[o].listOP_BaseDG_CNT_EDX_Best.append(valCount)
	objs[o].listOP_BaseDG_NumOps_EDX_Best.append(numOps)
	objs[o].listOP_BaseDG_Module_EDX_Best.append(modName)
def addListBaseDG_EDI_Best(address, valCount, numOps, modName):
	objs[o].listOP_BaseDG_EDI_Best.append(address)
	objs[o].listOP_BaseDG_CNT_EDI_Best.append(valCount)
	objs[o].listOP_BaseDG_NumOps_EDI_Best.append(numOps)
	objs[o].listOP_BaseDG_Module_EDI_Best.append(modName)
def addListBaseDG_ESI_Best(address, valCount, numOps, modName):
	objs[o].listOP_BaseDG_ESI_Best.append(address)
	objs[o].listOP_BaseDG_CNT_ESI_Best.append(valCount)
	objs[o].listOP_BaseDG_NumOps_ESI_Best.append(numOps)
	objs[o].listOP_BaseDG_Module_ESI_Best.append(modName)
def addListBaseDG_EBP_Best(address, valCount, numOps, modName):
	objs[o].listOP_BaseDG_EBP_Best.append(address)
	objs[o].listOP_BaseDG_CNT_EBP_Best.append(valCount)
	objs[o].listOP_BaseDG_NumOps_EBP_Best.append(numOps)
	objs[o].listOP_BaseDG_Module_EBP_Best.append(modName)	
def addListBaseDG_ESP_Best(address, valCount, numOps, modName):
	objs[o].listOP_BaseDG_ESP_Best.append(address)
	objs[o].listOP_BaseDG_CNT_ESP_Best.append(valCount)
	objs[o].listOP_BaseDG_NumOps_ESP_Best.append(numOps)
	objs[o].listOP_BaseDG_Module_ESP_Best.append(modName)	

def addListBaseDG_EAX_Other(address, valCount, numOps, modName):
	objs[o].listOP_BaseDG_EAX_Other.append(address)
	objs[o].listOP_BaseDG_CNT_EAX_Other.append(valCount)
	objs[o].listOP_BaseDG_NumOps_EAX_Other.append(numOps)
	objs[o].listOP_BaseDG_Module_EAX_Other.append(modName)
def addListBaseDG_EBX_Other(address, valCount, numOps, modName):
	objs[o].listOP_BaseDG_EBX_Other.append(address)
	objs[o].listOP_BaseDG_CNT_EBX_Other.append(valCount)
	objs[o].listOP_BaseDG_NumOps_EBX_Other.append(numOps)
	objs[o].listOP_BaseDG_Module_EBX_Other.append(modName)
def addListBaseDG_ECX_Other(address, valCount, numOps, modName):
	objs[o].listOP_BaseDG_ECX_Other.append(address)
	objs[o].listOP_BaseDG_CNT_ECX_Other.append(valCount)
	objs[o].listOP_BaseDG_NumOps_ECX_Other.append(numOps)
	objs[o].listOP_BaseDG_Module_ECX_Other.append(modName)
def addListBaseDG_EDX_Other(address, valCount, numOps, modName):
	objs[o].listOP_BaseDG_EDX_Other.append(address)
	objs[o].listOP_BaseDG_CNT_EDX_Other.append(valCount)
	objs[o].listOP_BaseDG_NumOps_EDX_Other.append(numOps)
	objs[o].listOP_BaseDG_Module_EDX_Other.append(modName)
def addListBaseDG_EDI_Other(address, valCount, numOps, modName):
	objs[o].listOP_BaseDG_EDI_Other.append(address)
	objs[o].listOP_BaseDG_CNT_EDI_Other.append(valCount)
	objs[o].listOP_BaseDG_NumOps_EDI_Other.append(numOps)
	objs[o].listOP_BaseDG_Module_EDI_Other.append(modName)
def addListBaseDG_ESI_Other(address, valCount, numOps, modName):
	objs[o].listOP_BaseDG_ESI_Other.append(address)
	objs[o].listOP_BaseDG_CNT_ESI_Other.append(valCount)
	objs[o].listOP_BaseDG_NumOps_ESI_Other.append(numOps)
	objs[o].listOP_BaseDG_Module_ESI_Other.append(modName)
def addListBaseDG_EBP_Other(address, valCount, numOps, modName):
	objs[o].listOP_BaseDG_EBP_Other.append(address)
	objs[o].listOP_BaseDG_CNT_EBP_Other.append(valCount)
	objs[o].listOP_BaseDG_NumOps_EBP_Other.append(numOps)
	objs[o].listOP_BaseDG_Module_EBP_Other.append(modName)
def addListSPAll(x,y):
	objs[o].SpOutGadgetAll.append(x)
	objs[o].SpOutNumBytesAll.append(y)
def addListSPEAX(x,y):
	objs[o].SpOutGadgetEAX.append(x)
	objs[o].SpOutNumBytesEAX.append(y)
def addListSPEBX(x,y):
	objs[o].SpOutGadgetEBX.append(x)
	objs[o].SpOutNumBytesEBX.append(y)
def addListSPECX(x,y):
	objs[o].SpOutGadgetECX.append(x)
	objs[o].SpOutNumBytesECX.append(y)
def addListSPEDX(x,y):
	objs[o].SpOutGadgetEDX.append(x)
	objs[o].SpOutNumBytesEDX.append(y)
def addListSPEDI(x,y):
	objs[o].SpOutGadgetEDI.append(x)
	objs[o].SpOutNumBytesEDI.append(y)
def addListSPESI(x,y):
	objs[o].SpOutGadgetESI.append(x)
	objs[o].SpOutNumBytesESI.append(y)
def addListSPEBP(x,y):
	objs[o].SpOutGadgetEBP.append(x)
	objs[o].SpOutNumBytesEBP.append(y)
def addSpecialPOP(x,y):
	objs[o].specialPOPGadget.append(x)
	objs[o].specialPOPBytes.append(y)
def addSpecialPOPBest(x,y):
	objs[o].specialPOPGadgetBest.append(x)
	objs[o].specialPOPBytesBest.append(y)

def addSpecialPOP_RET(x,y):
	objs[o].specialPOPGadgetRet.append(x)
	objs[o].specialPOPBytesRet.append(y)
	# objs[o].specialPOPBytesRetTup.append(tuple)

def addSpecialPOP_RETEAX(x,y):
	objs[o].specialPOPGadgetRetEAX.append(x)
	objs[o].specialPOPBytesRetEAX.append(y)
def addSpecialPOPRetBestEAX(x,y):
	objs[o].specialPOPGadgetRetBestEAX.append(x)
	objs[o].specialPOPBytesRetBestEAX.append(y)
	# objs[o].specialPOPBytesRetTup.append(tu	
def addSpecialPOP_RETEBX(x,y):
	objs[o].specialPOPGadgetRetEBX.append(x)
	objs[o].specialPOPBytesRetEBX.append(y)
def addSpecialPOPRetBestEBX(x,y):
	objs[o].specialPOPGadgetRetBestEBX.append(x)
	objs[o].specialPOPBytesRetBestEBX.append(y)
def addSpecialPOP_RETECX(x,y):
	objs[o].specialPOPGadgetRetECX.append(x)
	objs[o].specialPOPBytesRetECX.append(y)
def addSpecialPOPRetBestECX(x,y):
	objs[o].specialPOPGadgetRetBestECX.append(x)
	objs[o].specialPOPBytesRetBestECX.append(y)
def addSpecialPOP_RETEDX(x,y):
	objs[o].specialPOPGadgetRetEDX.append(x)
	objs[o].specialPOPBytesRetEDX.append(y)
def addSpecialPOPRetBestEDX(x,y):
	# print "savingbestPopedx"
	objs[o].specialPOPGadgetRetBestEDX.append(x)
	objs[o].specialPOPBytesRetBestEDX.append(y)
	# print "done"
def addSpecialPOP_RETEDI(x,y):
	objs[o].specialPOPGadgetRetEDI.append(x)
	objs[o].specialPOPBytesRetEDI.append(y)
def addSpecialPOPRetBestEDI(x,y):
	objs[o].specialPOPGadgetRetBestEDI.append(x)
	objs[o].specialPOPBytesRetBestEDI.append(y)
def addSpecialPOP_RETESI(x,y):
	objs[o].specialPOPGadgetRetESI.append(x)
	objs[o].specialPOPBytesRetESI.append(y)
def addSpecialPOPRetBestESI(x,y):
	objs[o].specialPOPGadgetRetBestESI.append(x)
	objs[o].specialPOPBytesRetBestESI.append(y)
def addSpecialPOP_RETESP(x,y):
	objs[o].specialPOPGadgetRetESP.append(x)
	objs[o].specialPOPBytesRetESP.append(y)
def addSpecialPOPRetBestESP(x,y):
	objs[o].specialPOPGadgetRetBestESP.append(x)
	objs[o].specialPOPBytesRetBestESP.append(y)
def addSpecialPOP_RETEBP(x,y):
	objs[o].specialPOPGadgetRetEBP.append(x)
	objs[o].specialPOPBytesRetEBP.append(y)
def addSpecialPOPRetBestEBP(x,y):
	objs[o].specialPOPGadgetRetBestEBP.append(x)
	objs[o].specialPOPBytesRetBestEBP.append(y)

def addSpecialPOPBestEAX(x,y):
	# print "addspecialpopbesteax"
	objs[o].specialPOPGadgetBestEAX.append(x)
	objs[o].specialPOPBytesBestEAX.append(y)
	# print "eax-f"
	# for e in objs[o].specialPOPGadgetBestEAX:
	# 	print e
	# print "eax-f2"

	# for e in objs[o].specialPOPGadgetEAX:
	# 	print e
def addSpecialPOPBestEBX(x,y):
	objs[o].specialPOPGadgetBestEBX.append(x)
	objs[o].specialPOPBytesBestEBX.append(y)
def addSpecialPOPBestECX(x,y):
	objs[o].specialPOPGadgetBestECX.append(x)
	objs[o].specialPOPBytesBestECX.append(y)
def addSpecialPOPBestEDX(x,y):
	objs[o].specialPOPGadgetBestEDX.append(x)
	objs[o].specialPOPBytesBestEDX.append(y)
def addSpecialPOPBestEDI(x,y):
	objs[o].specialPOPGadgetBestEDI.append(x)
	objs[o].specialPOPBytesBestEDI.append(y)
def addSpecialPOPBestESI(x,y):
	objs[o].specialPOPGadgetBestESI.append(x)
	objs[o].specialPOPBytesBestESI.append(y)
def addSpecialPOPBestEBP(x,y):
	objs[o].specialPOPGadgetBestEBP.append(x)
	objs[o].specialPOPBytesBestEBP.append(y)
def addSpecialPOPBestESP(x,y):
	objs[o].specialPOPGadgetBestESP.append(x)
	objs[o].specialPOPBytesBestESP.append(y)
def addSpecialPOP_EAX(x,y):
	objs[o].specialPOPGadgetEAX.append(x)
	objs[o].specialPOPBytesEAX.append(y)
def addSpecialPOP_EBX(x,y):
	objs[o].specialPOPGadgetEBX.append(x)
	objs[o].specialPOPBytesEBX.append(y)
def addSpecialPOP_ECX(x,y):
	objs[o].specialPOPGadgetECX.append(x)
	objs[o].specialPOPBytesECX.append(y)
def addSpecialPOP_EDX(x,y):
	objs[o].specialPOPGadgetEDX.append(x)
	objs[o].specialPOPBytesEDX.append(y)
def addSpecialPOP_EDI(x,y):
	objs[o].specialPOPGadgetEDI.append(x)
	objs[o].specialPOPBytesEDI.append(y)
def addSpecialPOP_ESI(x,y):
	objs[o].specialPOPGadgetESI.append(x)
	objs[o].specialPOPBytesESI.append(y)
def addSpecialPOP_EBP(x,y):
	objs[o].specialPOPGadgetEBP.append(x)
	objs[o].specialPOPBytesEBP.append(y)
def addSpecialPOP_ESP(x,y):
	objs[o].specialPOPGadgetESP.append(x)
	objs[o].specialPOPBytesESP.append(y)
def addListSPESP(x,y):
	objs[o].SpOutGadgetESP.append(x)
	objs[o].SpOutNumBytesESP.append(y)
def addListBaseAdd(address, valCount, numOps, modName):
	objs[o].listOP_BaseAdd.append(address)
	objs[o].listOP_BaseAdd_CNT.append(valCount)
	objs[o].listOP_BaseAdd_NumOps.append(numOps)
	objs[o].listOP_BaseAdd_Module.append(modName)
def addListBaseAddEAX(address, valCount, numOps, modName):
	objs[o].listOP_BaseAddEAX.append(address)
	objs[o].listOP_BaseAddEAX_CNT.append(valCount)
	objs[o].listOP_BaseAddEAX_NumOps.append(numOps)
	objs[o].listOP_BaseAddEAX_Module.append(modName)
	# print "finished save"
def addListBaseAddEBX(address, valCount, numOps, modName):
	objs[o].listOP_BaseAddEBX.append(address)
	objs[o].listOP_BaseAddEBX_CNT.append(valCount)
	objs[o].listOP_BaseAddEBX_NumOps.append(numOps)
	objs[o].listOP_BaseAddEBX_Module.append(modName)
def addListBaseAddECX(address, valCount, numOps, modName):
	objs[o].listOP_BaseAddECX.append(address)
	objs[o].listOP_BaseAddECX_CNT.append(valCount)
	objs[o].listOP_BaseAddECX_NumOps.append(numOps)
	objs[o].listOP_BaseAddECX_Module.append(modName)
def addListBaseAddEDX(address, valCount, numOps, modName):
	objs[o].listOP_BaseAddEDX.append(address)
	objs[o].listOP_BaseAddEDX_CNT.append(valCount)
	objs[o].listOP_BaseAddEDX_NumOps.append(numOps)
	objs[o].listOP_BaseAddEDX_Module.append(modName)
def addListBaseAddESI(address, valCount, numOps, modName):
	objs[o].listOP_BaseAddESI.append(address)
	objs[o].listOP_BaseAddESI_CNT.append(valCount)
	objs[o].listOP_BaseAddESI_NumOps.append(numOps)
	objs[o].listOP_BaseAddESI_Module.append(modName)
def addListBaseAddEDI(address, valCount, numOps, modName):
	objs[o].listOP_BaseAddEDI.append(address)
	objs[o].listOP_BaseAddEDI_CNT.append(valCount)
	objs[o].listOP_BaseAddEDI_NumOps.append(numOps)
	objs[o].listOP_BaseAddEDI_Module.append(modName)
def addListBaseAddESP(address, valCount, numOps, modName):
	objs[o].listOP_BaseAddESP.append(address)
	objs[o].listOP_BaseAddESP_CNT.append(valCount)
	objs[o].listOP_BaseAddESP_NumOps.append(numOps)
	objs[o].listOP_BaseAddESP_Module.append(modName)
def addListBaseAddEBP(address, valCount, numOps, modName):
	objs[o].listOP_BaseAddEBP.append(address)
	objs[o].listOP_BaseAddEBP_CNT.append(valCount)
	objs[o].listOP_BaseAddEBP_NumOps.append(numOps)
	objs[o].listOP_BaseAddEBP_Module.append(modName)



#add list Sub 
def addListBaseSub(address, valCount, numOps, modName):
	objs[o].listOP_BaseSub.append(address)
	objs[o].listOP_BaseSub_CNT.append(valCount)
	objs[o].listOP_BaseSub_NumOps.append(numOps)
	objs[o].listOP_BaseSub_Module.append(modName)

def addListBaseSubEAX(address, valCount, numOps, modName):
	objs[o].listOP_BaseSubEAX.append(address)
	objs[o].listOP_BaseSubEAX_CNT.append(valCount)
	objs[o].listOP_BaseSubEAX_NumOps.append(numOps)
	objs[o].listOP_BaseSubEAX_Module.append(modName)
def addListBaseSubEBX(address, valCount, numOps, modName):
	objs[o].listOP_BaseSubEBX.append(address)
	objs[o].listOP_BaseSubEBX_CNT.append(valCount)
	objs[o].listOP_BaseSubEBX_NumOps.append(numOps)
	objs[o].listOP_BaseSubEBX_Module.append(modName)
def addListBaseSubECX(address, valCount, numOps, modName):
	objs[o].listOP_BaseSubECX.append(address)
	objs[o].listOP_BaseSubECX_CNT.append(valCount)
	objs[o].listOP_BaseSubECX_NumOps.append(numOps)
	objs[o].listOP_BaseSubECX_Module.append(modName)
def addListBaseSubEDX(address, valCount, numOps, modName):
	objs[o].listOP_BaseSubEDX.append(address)
	objs[o].listOP_BaseSubEDX_CNT.append(valCount)
	objs[o].listOP_BaseSubEDX_NumOps.append(numOps)
	objs[o].listOP_BaseSubEDX_Module.append(modName)
def addListBaseSubESI(address, valCount, numOps, modName):
	objs[o].listOP_BaseSubESI.append(address)
	objs[o].listOP_BaseSubESI_CNT.append(valCount)
	objs[o].listOP_BaseSubESI_NumOps.append(numOps)
	objs[o].listOP_BaseSubESI_Module.append(modName)
def addListBaseSubEDI(address, valCount, numOps, modName):
	objs[o].listOP_BaseSubEDI.append(address)
	objs[o].listOP_BaseSubEDI_CNT.append(valCount)
	objs[o].listOP_BaseSubEDI_NumOps.append(numOps)
	objs[o].listOP_BaseSubEDI_Module.append(modName)
def addListBaseSubESP(address, valCount, numOps, modName):
	objs[o].listOP_BaseSubESP.append(address)
	objs[o].listOP_BaseSubESP_CNT.append(valCount)
	objs[o].listOP_BaseSubESP_NumOps.append(numOps)
	objs[o].listOP_BaseSubESP_Module.append(modName)
def addListBaseSubEBP(address, valCount, numOps, modName):
	objs[o].listOP_BaseSubEBP.append(address)
	objs[o].listOP_BaseSubEBP_CNT.append(valCount)
	objs[o].listOP_BaseSubEBP_NumOps.append(numOps)
	objs[o].listOP_BaseSubEBP_Module.append(modName)

#add list Mul 
def addListBaseMul(address, valCount, numOps, modName):
	objs[o].listOP_BaseMul.append(address)
	objs[o].listOP_BaseMul_CNT.append(valCount)
	objs[o].listOP_BaseMul_NumOps.append(numOps)
	objs[o].listOP_BaseMul_Module.append(modName)
def addListBaseMulEAX(address, valCount, numOps, modName):
	objs[o].listOP_BaseMulEAX.append(address)
	objs[o].listOP_BaseMulEAX_CNT.append(valCount)
	objs[o].listOP_BaseMulEAX_NumOps.append(numOps)
	objs[o].listOP_BaseMulEAX_Module.append(modName)
def addListBaseMulEBX(address, valCount, numOps, modName):
	objs[o].listOP_BaseMulEBX.append(address)
	objs[o].listOP_BaseMulEBX_CNT.append(valCount)
	objs[o].listOP_BaseMulEBX_NumOps.append(numOps)
	objs[o].listOP_BaseMulEBX_Module.append(modName)
def addListBaseMulECX(address, valCount, numOps, modName):
	objs[o].listOP_BaseMulECX.append(address)
	objs[o].listOP_BaseMulECX_CNT.append(valCount)
	objs[o].listOP_BaseMulECX_NumOps.append(numOps)
	objs[o].listOP_BaseMulECX_Module.append(modName)
def addListBaseMulEDX(address, valCount, numOps, modName):
	objs[o].listOP_BaseMulEDX.append(address)
	objs[o].listOP_BaseMulEDX_CNT.append(valCount)
	objs[o].listOP_BaseMulEDX_NumOps.append(numOps)
	objs[o].listOP_BaseMulEDX_Module.append(modName)
def addListBaseMulESI(address, valCount, numOps, modName):
	objs[o].listOP_BaseMulESI.append(address)
	objs[o].listOP_BaseMulESI_CNT.append(valCount)
	objs[o].listOP_BaseMulESI_NumOps.append(numOps)
	objs[o].listOP_BaseMulESI_Module.append(modName)
def addListBaseMulEDI(address, valCount, numOps, modName):
	objs[o].listOP_BaseMulEDI.append(address)
	objs[o].listOP_BaseMulEDI_CNT.append(valCount)
	objs[o].listOP_BaseMulEDI_NumOps.append(numOps)
	objs[o].listOP_BaseMulEDI_Module.append(modName)
def addListBaseMulEBP(address, valCount, numOps, modName):
	objs[o].listOP_BaseMulEBP.append(address)
	objs[o].listOP_BaseMulEBP_CNT.append(valCount)
	objs[o].listOP_BaseMulEBP_NumOps.append(numOps)
	objs[o].listOP_BaseMulEBP_Module.append(modName)


#DIV
def addListBaseDiv(address, valCount, numOps, modName):
	objs[o].listOP_BaseDiv.append(address)
	objs[o].listOP_BaseDiv_CNT.append(valCount)
	objs[o].listOP_BaseDiv_NumOps.append(numOps)
	objs[o].listOP_BaseDiv_Module.append(modName)
def addListBaseDivEAX(address, valCount, numOps, modName):
	objs[o].listOP_BaseDivEAX.append(address)
	objs[o].listOP_BaseDivEAX_CNT.append(valCount)
	objs[o].listOP_BaseDivEAX_NumOps.append(numOps)
	objs[o].listOP_BaseDivEAX_Module.append(modName)
def addListBaseDivEDX(address, valCount, numOps, modName):
	objs[o].listOP_BaseDivEDX.append(address)
	objs[o].listOP_BaseDivEDX_CNT.append(valCount)
	objs[o].listOP_BaseDivEDX_NumOps.append(numOps)
	objs[o].listOP_BaseDivEDX_Module.append(modName)
def addListBaseMovEAX(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovEAX.append(address)
	objs[o].listOP_BaseMovEAX_CNT.append(valCount)
	objs[o].listOP_BaseMovEAX_NumOps.append(numOps)
	objs[o].listOP_BaseMovEAX_Module.append(modName)
def addListBaseMov(address, valCount, numOps, modName):
	objs[o].listOP_BaseMov.append(address)
	objs[o].listOP_BaseMov_CNT.append(valCount)
	objs[o].listOP_BaseMov_NumOps.append(numOps)
	objs[o].listOP_BaseMov_Module.append(modName)
def addListBaseMovEBX(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovEBX.append(address)
	objs[o].listOP_BaseMovEBX_CNT.append(valCount)
	objs[o].listOP_BaseMovEBX_NumOps.append(numOps)
	objs[o].listOP_BaseMovEBX_Module.append(modName)
def addListBaseMovECX(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovECX.append(address)
	objs[o].listOP_BaseMovECX_CNT.append(valCount)
	objs[o].listOP_BaseMovECX_NumOps.append(numOps)
	objs[o].listOP_BaseMovECX_Module.append(modName)
	
def addListBaseMovEDX(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovEDX.append(address)
	objs[o].listOP_BaseMovEDX_CNT.append(valCount)
	objs[o].listOP_BaseMovEDX_NumOps.append(numOps)
	objs[o].listOP_BaseMovEDX_Module.append(modName)
def addListBaseMovESI(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovESI.append(address)
	objs[o].listOP_BaseMovESI_CNT.append(valCount)
	objs[o].listOP_BaseMovESI_NumOps.append(numOps)
	objs[o].listOP_BaseMovESI_Module.append(modName)
def addListBaseMovEDI(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovEDI.append(address)
	objs[o].listOP_BaseMovEDI_CNT.append(valCount)
	objs[o].listOP_BaseMovEDI_NumOps.append(numOps)
	objs[o].listOP_BaseMovEDI_Module.append(modName)
def addListBaseMovESP(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovESP.append(address)
	objs[o].listOP_BaseMovESP_CNT.append(valCount)
	objs[o].listOP_BaseMovESP_NumOps.append(numOps)
	objs[o].listOP_BaseMovESP_Module.append(modName)
def addListBaseMovEBP(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovEBP.append(address)
	objs[o].listOP_BaseMovEBP_CNT.append(valCount)
	objs[o].listOP_BaseMovEBP_NumOps.append(numOps)
	objs[o].listOP_BaseMovEBP_Module.append(modName)
def addListBaseMovShuf(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovShuf.append(address)
	objs[o].listOP_BaseMovShuf_CNT.append(valCount)
	objs[o].listOP_BaseMovShuf_NumOps.append(numOps)
	objs[o].listOP_BaseMovShuf_Module.append(modName)
def addListBaseMovShufEAX(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovShufEAX.append(address)
	objs[o].listOP_BaseMovShufEAX_CNT.append(valCount)
	objs[o].listOP_BaseMovShufEAX_NumOps.append(numOps)
	objs[o].listOP_BaseMovShufEAX_Module.append(modName)
def addListBaseMovShufEBX(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovShufEBX.append(address)
	objs[o].listOP_BaseMovShufEBX_CNT.append(valCount)
	objs[o].listOP_BaseMovShufEBX_NumOps.append(numOps)
	objs[o].listOP_BaseMovShufEBX_Module.append(modName)
def addListBaseMovShufECX(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovShufECX.append(address)
	objs[o].listOP_BaseMovShufECX_CNT.append(valCount)
	objs[o].listOP_BaseMovShufECX_NumOps.append(numOps)
	objs[o].listOP_BaseMovShufECX_Module.append(modName)
def addListBaseMovShufEDX(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovShufEDX.append(address)
	objs[o].listOP_BaseMovShufEDX_CNT.append(valCount)
	objs[o].listOP_BaseMovShufEDX_NumOps.append(numOps)
	objs[o].listOP_BaseMovShufEDX_Module.append(modName)
def addListBaseMovShufESI(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovShufESI.append(address)
	objs[o].listOP_BaseMovShufESI_CNT.append(valCount)
	objs[o].listOP_BaseMovShufESI_NumOps.append(numOps)
	objs[o].listOP_BaseMovShufESI_Module.append(modName)
def addListBaseMovShufEDI(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovShufEDI.append(address)
	objs[o].listOP_BaseMovShufEDI_CNT.append(valCount)
	objs[o].listOP_BaseMovShufEDI_NumOps.append(numOps)
	objs[o].listOP_BaseMovShufEDI_Module.append(modName)
def addListBaseMovShufESP(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovShufESP.append(address)
	objs[o].listOP_BaseMovShufESP_CNT.append(valCount)
	objs[o].listOP_BaseMovShufESP_NumOps.append(numOps)
	objs[o].listOP_BaseMovShufESP_Module.append(modName)
def addListBaseMovShufEBP(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovShufEBP.append(address)
	objs[o].listOP_BaseMovShufEBP_CNT.append(valCount)
	objs[o].listOP_BaseMovShufEBP_NumOps.append(numOps)
	objs[o].listOP_BaseMovShufEBP_Module.append(modName)
def addListMovDeref(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovDeref.append(address)
	objs[o].listOP_BaseMovDeref_CNT.append(valCount)
	objs[o].listOP_BaseMovDeref_NumOps.append(numOps)
	objs[o].listOP_BaseMovDeref_Module.append(modName)
def addListMovDerefEAX(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovDerefEAX.append(address)
	objs[o].listOP_BaseMovDerefEAX_CNT.append(valCount)
	objs[o].listOP_BaseMovDerefEAX_NumOps.append(numOps)
	objs[o].listOP_BaseMovDerefEAX_Module.append(modName)
def addListMovDerefEBX(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovDerefEBX.append(address)
	objs[o].listOP_BaseMovDerefEBX_CNT.append(valCount)
	objs[o].listOP_BaseMovDerefEBX_NumOps.append(numOps)
	objs[o].listOP_BaseMovDerefEBX_Module.append(modName)
def addListMovDerefECX(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovDerefECX.append(address)
	objs[o].listOP_BaseMovDerefECX_CNT.append(valCount)
	objs[o].listOP_BaseMovDerefECX_NumOps.append(numOps)
	objs[o].listOP_BaseMovDerefECX_Module.append(modName)
def addListMovDerefEDX(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovDerefEDX.append(address)
	objs[o].listOP_BaseMovDerefEDX_CNT.append(valCount)
	objs[o].listOP_BaseMovDerefEDX_NumOps.append(numOps)
	objs[o].listOP_BaseMovDerefEDX_Module.append(modName)
def addListMovDerefESI(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovDerefESI.append(address)
	objs[o].listOP_BaseMovDerefESI_CNT.append(valCount)
	objs[o].listOP_BaseMovDerefESI_NumOps.append(numOps)
	objs[o].listOP_BaseMovDerefESI_Module.append(modName)
def addListMovDerefEDI(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovDerefEDI.append(address)
	objs[o].listOP_BaseMovDerefEDI_CNT.append(valCount)
	objs[o].listOP_BaseMovDerefEDI_NumOps.append(numOps)
	objs[o].listOP_BaseMovDerefEDI_Module.append(modName)
def addListMovDerefESP(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovDerefESP.append(address)
	objs[o].listOP_BaseMovDerefESP_CNT.append(valCount)
	objs[o].listOP_BaseMovDerefESP_NumOps.append(numOps)
	objs[o].listOP_BaseMovDerefESP_Module.append(modName)
def addListMovDerefEBP(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovDerefEBP.append(address)
	objs[o].listOP_BaseMovDerefEBP_CNT.append(valCount)
	objs[o].listOP_BaseMovDerefEBP_NumOps.append(numOps)
	objs[o].listOP_BaseMovDerefEBP_Module.append(modName)	
#mov value into reg
def addListBaseMovVal(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovVal.append(address)
	objs[o].listOP_BaseMovVal_CNT.append(valCount)
	objs[o].listOP_BaseMovVal_NumOps.append(numOps)
	objs[o].listOP_BaseMovVal_Module.append(modName)
def addListBaseMovValEAX(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovValEAX.append(address)
	objs[o].listOP_BaseMovValEAX_CNT.append(valCount)
	objs[o].listOP_BaseMovValEAX_NumOps.append(numOps)
	objs[o].listOP_BaseMovValEAX_Module.append(modName)
def addListBaseMovValEBX(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovValEBX.append(address)
	objs[o].listOP_BaseMovValEBX_CNT.append(valCount)
	objs[o].listOP_BaseMovValEBX_NumOps.append(numOps)
	objs[o].listOP_BaseMovValEBX_Module.append(modName)
def addListBaseMovValECX(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovValECX.append(address)
	objs[o].listOP_BaseMovValECX_CNT.append(valCount)
	objs[o].listOP_BaseMovValECX_NumOps.append(numOps)
	objs[o].listOP_BaseMovValECX_Module.append(modName)
def addListBaseMovValEDX(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovValEDX.append(address)
	objs[o].listOP_BaseMovValEDX_CNT.append(valCount)
	objs[o].listOP_BaseMovValEDX_NumOps.append(numOps)
	objs[o].listOP_BaseMovValEDX_Module.append(modName)
def addListBaseMovValESI(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovValESI.append(address)
	objs[o].listOP_BaseMovValESI_CNT.append(valCount)
	objs[o].listOP_BaseMovValESI_NumOps.append(numOps)
	objs[o].listOP_BaseMovValESI_Module.append(modName)
def addListBaseMovValEDI(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovValEDI.append(address)
	objs[o].listOP_BaseMovValEDI_CNT.append(valCount)
	objs[o].listOP_BaseMovValEDI_NumOps.append(numOps)
	objs[o].listOP_BaseMovValEDI_Module.append(modName)
def addListBaseMovValESP(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovValESP.append(address)
	objs[o].listOP_BaseMovValESP_CNT.append(valCount)
	objs[o].listOP_BaseMovValESP_NumOps.append(numOps)
	objs[o].listOP_BaseMovValESP_Module.append(modName)
def addListBaseMovValEBP(address, valCount, numOps, modName):
	objs[o].listOP_BaseMovValEBP.append(address)
	objs[o].listOP_BaseMovValEBP_CNT.append(valCount)
	objs[o].listOP_BaseMovValEBP_NumOps.append(numOps)
	objs[o].listOP_BaseMovValEBP_Module.append(modName)
#LEA
def addListBaseLea(address, valCount, numOps, modName):
	objs[o].listOP_BaseLea.append(address)
	objs[o].listOP_BaseLea_CNT.append(valCount)
	objs[o].listOP_BaseLea_NumOps.append(numOps)
	objs[o].listOP_BaseLea_Module.append(modName)
def addListBaseLeaEAX(address, valCount, numOps, modName):
	objs[o].listOP_BaseLeaEAX.append(address)
	objs[o].listOP_BaseLeaEAX_CNT.append(valCount)
	objs[o].listOP_BaseLeaEAX_NumOps.append(numOps)
	objs[o].listOP_BaseLeaEAX_Module.append(modName)
def addListBaseLeaEBX(address, valCount, numOps, modName):
	objs[o].listOP_BaseLeaEBX.append(address)
	objs[o].listOP_BaseLeaEBX_CNT.append(valCount)
	objs[o].listOP_BaseLeaEBX_NumOps.append(numOps)
	objs[o].listOP_BaseLeaEBX_Module.append(modName)
def addListBaseLeaECX(address, valCount, numOps, modName):
	objs[o].listOP_BaseLeaECX.append(address)
	objs[o].listOP_BaseLeaECX_CNT.append(valCount)
	objs[o].listOP_BaseLeaECX_NumOps.append(numOps)
	objs[o].listOP_BaseLeaECX_Module.append(modName)
def addListBaseLeaEDX(address, valCount, numOps, modName):
	objs[o].listOP_BaseLeaEDX.append(address)
	objs[o].listOP_BaseLeaEDX_CNT.append(valCount)
	objs[o].listOP_BaseLeaEDX_NumOps.append(numOps)
	objs[o].listOP_BaseLeaEDX_Module.append(modName)
def addListBaseLeaESI(address, valCount, numOps, modName):
	objs[o].listOP_BaseLeaESI.append(address)
	objs[o].listOP_BaseLeaESI_CNT.append(valCount)
	objs[o].listOP_BaseLeaESI_NumOps.append(numOps)
	objs[o].listOP_BaseLeaESI_Module.append(modName)
def addListBaseLeaEDI(address, valCount, numOps, modName):
	objs[o].listOP_BaseLeaEDI.append(address)
	objs[o].listOP_BaseLeaEDI_CNT.append(valCount)
	objs[o].listOP_BaseLeaEDI_NumOps.append(numOps)
	objs[o].listOP_BaseLeaEDI_Module.append(modName)
def addListBaseLeaESP(address, valCount, numOps, modName):
	objs[o].listOP_BaseLeaESP.append(address)
	objs[o].listOP_BaseLeaESP_CNT.append(valCount)
	objs[o].listOP_BaseLeaESP_NumOps.append(numOps)
	objs[o].listOP_BaseLeaESP_Module.append(modName)
def addListBaseLeaEBP(address, valCount, numOps, modName):
	objs[o].listOP_BaseLeaEBP.append(address)
	objs[o].listOP_BaseLeaEBP_CNT.append(valCount)
	objs[o].listOP_BaseLeaEBP_NumOps.append(numOps)
	objs[o].listOP_BaseLeaEBP_Module.append(modName)
#Push reg
def addListBasePush(address, valCount, numOps, modName):
	objs[o].listOP_BasePush.append(address)
	objs[o].listOP_BasePush_CNT.append(valCount)
	objs[o].listOP_BasePush_NumOps.append(numOps)
	objs[o].listOP_BasePush_Module.append(modName)
def addListBasePushEAX(address, valCount, numOps, modName):
	objs[o].listOP_BasePushEAX.append(address)
	objs[o].listOP_BasePushEAX_CNT.append(valCount)
	objs[o].listOP_BasePushEAX_NumOps.append(numOps)
	objs[o].listOP_BasePushEAX_Module.append(modName)
def addListBasePushEBX(address, valCount, numOps, modName):
	objs[o].listOP_BasePushEBX.append(address)
	objs[o].listOP_BasePushEBX_CNT.append(valCount)
	objs[o].listOP_BasePushEBX_NumOps.append(numOps)
	objs[o].listOP_BasePushEBX_Module.append(modName)
def addListBasePushECX(address, valCount, numOps, modName):
	objs[o].listOP_BasePushECX.append(address)
	objs[o].listOP_BasePushECX_CNT.append(valCount)
	objs[o].listOP_BasePushECX_NumOps.append(numOps)
	objs[o].listOP_BasePushECX_Module.append(modName)
def addListBasePushEDX(address, valCount, numOps, modName):
	objs[o].listOP_BasePushEDX.append(address)
	objs[o].listOP_BasePushEDX_CNT.append(valCount)
	objs[o].listOP_BasePushEDX_NumOps.append(numOps)
	objs[o].listOP_BasePushEDX_Module.append(modName)
def addListBasePushESI(address, valCount, numOps, modName):
	objs[o].listOP_BasePushESI.append(address)
	objs[o].listOP_BasePushESI_CNT.append(valCount)
	objs[o].listOP_BasePushESI_NumOps.append(numOps)
	objs[o].listOP_BasePushESI_Module.append(modName)
def addListBasePushEDI(address, valCount, numOps, modName):
	objs[o].listOP_BasePushEDI.append(address)
	objs[o].listOP_BasePushEDI_CNT.append(valCount)
	objs[o].listOP_BasePushEDI_NumOps.append(numOps)
	objs[o].listOP_BasePushEDI_Module.append(modName)
def addListBasePushESP(address, valCount, numOps, modName):
	objs[o].listOP_BasePushESP.append(address)
	objs[o].listOP_BasePushESP_CNT.append(valCount)
	objs[o].listOP_BasePushESP_NumOps.append(numOps)
	objs[o].listOP_BasePushESP_Module.append(modName)
def addListBasePushEBP(address, valCount, numOps, modName):
	objs[o].listOP_BasePushEBP.append(address)
	objs[o].listOP_BasePushEBP_CNT.append(valCount)
	objs[o].listOP_BasePushEBP_NumOps.append(numOps)
	objs[o].listOP_BasePushEBP_Module.append(modName)
#POP
def addListRETPop(address, valCount, numOps, modName):
	objs[o].listOP_RET_Pop.append(address)
	objs[o].listOP_RET_Pop_CNT.append(valCount)
	objs[o].listOP_RET_Pop_NumOps.append(numOps)
	objs[o].listOP_RET_Pop_Module.append(modName)
def addListRETPopEAX(address, valCount, numOps, modName):
	objs[o].listOP_RET_Pop_EAX.append(address)
	objs[o].listOP_RET_Pop_EAX_CNT.append(valCount)
	objs[o].listOP_RET_Pop_EAX_NumOps.append(numOps)
	objs[o].listOP_RET_Pop_EAX_Module.append(modName)
def addListRETPopEBX(address, valCount, numOps, modName):
	objs[o].listOP_RET_Pop_EBX.append(address)
	objs[o].listOP_RET_Pop_EBX_CNT.append(valCount)
	objs[o].listOP_RET_Pop_EBX_NumOps.append(numOps)
	objs[o].listOP_RET_Pop_EBX_Module.append(modName)
def addListRETPopECX(address, valCount, numOps, modName):
	objs[o].listOP_RET_Pop_ECX.append(address)
	objs[o].listOP_RET_Pop_ECX_CNT.append(valCount)
	objs[o].listOP_RET_Pop_ECX_NumOps.append(numOps)
	objs[o].listOP_RET_Pop_ECX_Module.append(modName)
def addListRETPopEDX(address, valCount, numOps, modName):
	objs[o].listOP_RET_Pop_EDX.append(address)
	objs[o].listOP_RET_Pop_EDX_CNT.append(valCount)
	objs[o].listOP_RET_Pop_EDX_NumOps.append(numOps)
	objs[o].listOP_RET_Pop_EDX_Module.append(modName)
def addListRETPopEDI(address, valCount, numOps, modName):
	objs[o].listOP_RET_Pop_EDI.append(address)
	objs[o].listOP_RET_Pop_EDI_CNT.append(valCount)
	objs[o].listOP_RET_Pop_EDI_NumOps.append(numOps)
	objs[o].listOP_RET_Pop_EDI_Module.append(modName)
def addListRETPopESI(address, valCount, numOps, modName):
	objs[o].listOP_RET_Pop_ESI.append(address)
	objs[o].listOP_RET_Pop_ESI_CNT.append(valCount)
	objs[o].listOP_RET_Pop_ESI_NumOps.append(numOps)
	objs[o].listOP_RET_Pop_ESI_Module.append(modName)
def addListRETPopESP(address, valCount, numOps, modName):
	objs[o].listOP_RET_Pop_ESP.append(address)
	objs[o].listOP_RET_Pop_ESP_CNT.append(valCount)
	objs[o].listOP_RET_Pop_ESP_NumOps.append(numOps)
	objs[o].listOP_RET_Pop_ESP_Module.append(modName)
def addListRETPopEBP(address, valCount, numOps, modName):
	objs[o].listOP_RET_Pop_EBP.append(address)
	objs[o].listOP_RET_Pop_EBP_CNT.append(valCount)
	objs[o].listOP_RET_Pop_EBP_NumOps.append(numOps)
	objs[o].listOP_RET_Pop_EBP_Module.append(modName)
def addListBasePop(address, valCount, numOps, modName):
	objs[o].listOP_BasePop.append(address)
	objs[o].listOP_BasePop_CNT.append(valCount)
	objs[o].listOP_BasePop_NumOps.append(numOps)
	objs[o].listOP_BasePop_Module.append(modName)
def addListBasePopEAX(address, valCount, numOps, modName):
	objs[o].listOP_BasePopEAX.append(address)
	objs[o].listOP_BasePopEAX_CNT.append(valCount)
	objs[o].listOP_BasePopEAX_NumOps.append(numOps)
	objs[o].listOP_BasePopEAX_Module.append(modName)
def addListBasePopEBX(address, valCount, numOps, modName):
	objs[o].listOP_BasePopEBX.append(address)
	objs[o].listOP_BasePopEBX_CNT.append(valCount)
	objs[o].listOP_BasePopEBX_NumOps.append(numOps)
	objs[o].listOP_BasePopEBX_Module.append(modName)
def addListBasePopECX(address, valCount, numOps, modName):
	objs[o].listOP_BasePopECX.append(address)
	objs[o].listOP_BasePopECX_CNT.append(valCount)
	objs[o].listOP_BasePopECX_NumOps.append(numOps)
	objs[o].listOP_BasePopECX_Module.append(modName)
def addListBasePopEDX(address, valCount, numOps, modName):
	objs[o].listOP_BasePopEDX.append(address)
	objs[o].listOP_BasePopEDX_CNT.append(valCount)
	objs[o].listOP_BasePopEDX_NumOps.append(numOps)
	objs[o].listOP_BasePopEDX_Module.append(modName)
def addListBasePopESI(address, valCount, numOps, modName):
	objs[o].listOP_BasePopESI.append(address)
	objs[o].listOP_BasePopESI_CNT.append(valCount)
	objs[o].listOP_BasePopESI_NumOps.append(numOps)
	objs[o].listOP_BasePopESI_Module.append(modName)
def addListBasePopEDI(address, valCount, numOps, modName):
	objs[o].listOP_BasePopEDI.append(address)
	objs[o].listOP_BasePopEDI_CNT.append(valCount)
	objs[o].listOP_BasePopEDI_NumOps.append(numOps)
	objs[o].listOP_BasePopEDI_Module.append(modName)
def addListBasePopESP(address, valCount, numOps, modName):
	objs[o].listOP_BasePopESP.append(address)
	objs[o].listOP_BasePopESP_CNT.append(valCount)
	objs[o].listOP_BasePopESP_NumOps.append(numOps)
	objs[o].listOP_BasePopESP_Module.append(modName)
def addListBasePopEBP(address, valCount, numOps, modName):
	objs[o].listOP_BasePopEBP.append(address)
	objs[o].listOP_BasePopEBP_CNT.append(valCount)
	objs[o].listOP_BasePopEBP_NumOps.append(numOps)
	objs[o].listOP_BasePopEBP_Module.append(modName)
def addListStackPivot(address, valCount, numOps, modName, special):
	objs[o].listOP_BaseStackPivot.append(address)
	objs[o].listOP_BaseStackPivot_CNT.append(valCount)
	objs[o].listOP_BaseStackPivot_NumOps.append(numOps)
	objs[o].listOP_BaseStackPivot_Module.append(modName)
	objs[o].listOP_BaseStackPivot_Special.append(special)
def addListStackPivotEAX(address, valCount, numOps, modName, special):
	objs[o].listOP_BaseStackPivotEAX.append(address)
	objs[o].listOP_BaseStackPivotEAX_CNT.append(valCount)
	objs[o].listOP_BaseStackPivotEAX_NumOps.append(numOps)
	objs[o].listOP_BaseStackPivotEAX_Module.append(modName)
	objs[o].listOP_BaseStackPivotEAX_Special.append(special)
def addListStackPivotEBX(address, valCount, numOps, modName, special):
	objs[o].listOP_BaseStackPivotEBX.append(address)
	objs[o].listOP_BaseStackPivotEBX_CNT.append(valCount)
	objs[o].listOP_BaseStackPivotEBX_NumOps.append(numOps)
	objs[o].listOP_BaseStackPivotEBX_Module.append(modName)
	objs[o].listOP_BaseStackPivotEBX_Special.append(special)
def addListStackPivotECX(address, valCount, numOps, modName, special):
	objs[o].listOP_BaseStackPivotECX.append(address)
	objs[o].listOP_BaseStackPivotECX_CNT.append(valCount)
	objs[o].listOP_BaseStackPivotECX_NumOps.append(numOps)
	objs[o].listOP_BaseStackPivotECX_Module.append(modName)
	objs[o].listOP_BaseStackPivotECX_Special.append(special)
def addListStackPivotEDX(address, valCount, numOps, modName, special):
	objs[o].listOP_BaseStackPivotEDX.append(address)
	objs[o].listOP_BaseStackPivotEDX_CNT.append(valCount)
	objs[o].listOP_BaseStackPivotEDX_NumOps.append(numOps)
	objs[o].listOP_BaseStackPivotEDX_Module.append(modName)
	objs[o].listOP_BaseStackPivotEDX_Special.append(special)
def addListStackPivotEDI(address, valCount, numOps, modName, special):
	objs[o].listOP_BaseStackPivotEDI.append(address)
	objs[o].listOP_BaseStackPivotEDI_CNT.append(valCount)
	objs[o].listOP_BaseStackPivotEDI_NumOps.append(numOps)
	objs[o].listOP_BaseStackPivotEDI_Module.append(modName)
	objs[o].listOP_BaseStackPivotEDI_Special.append(special)
def addListStackPivotESI(address, valCount, numOps, modName, special):
	objs[o].listOP_BaseStackPivotESI.append(address)
	objs[o].listOP_BaseStackPivotESI_CNT.append(valCount)
	objs[o].listOP_BaseStackPivotESI_NumOps.append(numOps)
	objs[o].listOP_BaseStackPivotESI_Module.append(modName)
	objs[o].listOP_BaseStackPivotESI_Special.append(special)
def addListStackPivotEBP(address, valCount, numOps, modName, special):
	objs[o].listOP_BaseStackPivotEBP.append(address)
	objs[o].listOP_BaseStackPivotEBP_CNT.append(valCount)
	objs[o].listOP_BaseStackPivotEBP_NumOps.append(numOps)
	objs[o].listOP_BaseStackPivotEBP_Module.append(modName)
	objs[o].listOP_BaseStackPivotEBP_Special.append(special)
def addListStackPivotESP(address, valCount, numOps, modName, special):
	objs[o].listOP_BaseStackPivotESP.append(address)
	objs[o].listOP_BaseStackPivotESP_CNT.append(valCount)
	objs[o].listOP_BaseStackPivotESP_NumOps.append(numOps)
	objs[o].listOP_BaseStackPivotESP_Module.append(modName)
	objs[o].listOP_BaseStackPivotESP_Special.append(special)
#Inc
def addListBaseInc(address, valCount, numOps, modName):
	objs[o].listOP_BaseInc.append(address)
	objs[o].listOP_BaseInc_CNT.append(valCount)
	objs[o].listOP_BaseInc_NumOps.append(numOps)
	objs[o].listOP_BaseInc_Module.append(modName)
def addListBaseIncEAX(address, valCount, numOps, modName):
	objs[o].listOP_BaseIncEAX.append(address)
	objs[o].listOP_BaseIncEAX_CNT.append(valCount)
	objs[o].listOP_BaseIncEAX_NumOps.append(numOps)
	objs[o].listOP_BaseIncEAX_Module.append(modName)
def addListBaseIncEBX(address, valCount, numOps, modName):
	objs[o].listOP_BaseIncEBX.append(address)
	objs[o].listOP_BaseIncEBX_CNT.append(valCount)
	objs[o].listOP_BaseIncEBX_NumOps.append(numOps)
	objs[o].listOP_BaseIncEBX_Module.append(modName)
def addListBaseIncECX(address, valCount, numOps, modName):
	objs[o].listOP_BaseIncECX.append(address)
	objs[o].listOP_BaseIncECX_CNT.append(valCount)
	objs[o].listOP_BaseIncECX_NumOps.append(numOps)
	objs[o].listOP_BaseIncECX_Module.append(modName)
def addListBaseIncEDX(address, valCount, numOps, modName):
	objs[o].listOP_BaseIncEDX.append(address)
	objs[o].listOP_BaseIncEDX_CNT.append(valCount)
	objs[o].listOP_BaseIncEDX_NumOps.append(numOps)
	objs[o].listOP_BaseIncEDX_Module.append(modName)
def addListBaseIncESI(address, valCount, numOps, modName):
	objs[o].listOP_BaseIncESI.append(address)
	objs[o].listOP_BaseIncESI_CNT.append(valCount)
	objs[o].listOP_BaseIncESI_NumOps.append(numOps)
	objs[o].listOP_BaseIncESI_Module.append(modName)
def addListBaseIncEDI(address, valCount, numOps, modName):
	objs[o].listOP_BaseIncEDI.append(address)
	objs[o].listOP_BaseIncEDI_CNT.append(valCount)
	objs[o].listOP_BaseIncEDI_NumOps.append(numOps)
	objs[o].listOP_BaseIncEDI_Module.append(modName)
def addListBaseIncESP(address, valCount, numOps, modName):
	objs[o].listOP_BaseIncESP.append(address)
	objs[o].listOP_BaseIncESP_CNT.append(valCount)
	objs[o].listOP_BaseIncESP_NumOps.append(numOps)
	objs[o].listOP_BaseIncESP_Module.append(modName)
def addListBaseIncEBP(address, valCount, numOps, modName):
	objs[o].listOP_BaseIncEBP.append(address)
	objs[o].listOP_BaseIncEBP_CNT.append(valCount)
	objs[o].listOP_BaseIncEBP_NumOps.append(numOps)
	objs[o].listOP_BaseIncEBP_Module.append(modName)
#Dec
def addListBaseDec(address, valCount, numOps, modName):
	objs[o].listOP_BaseDec.append(address)
	objs[o].listOP_BaseDec_CNT.append(valCount)
	objs[o].listOP_BaseDec_NumOps.append(numOps)
	objs[o].listOP_BaseDec_Module.append(modName)
def addListBaseDecEAX(address, valCount, numOps, modName):
	objs[o].listOP_BaseDecEAX.append(address)
	objs[o].listOP_BaseDecEAX_CNT.append(valCount)
	objs[o].listOP_BaseDecEAX_NumOps.append(numOps)
	objs[o].listOP_BaseDecEAX_Module.append(modName)
def addListBaseDecEBX(address, valCount, numOps, modName):
	objs[o].listOP_BaseDecEBX.append(address)
	objs[o].listOP_BaseDecEBX_CNT.append(valCount)
	objs[o].listOP_BaseDecEBX_NumOps.append(numOps)
	objs[o].listOP_BaseDecEBX_Module.append(modName)
def addListBaseDecECX(address, valCount, numOps, modName):
	objs[o].listOP_BaseDecECX.append(address)
	objs[o].listOP_BaseDecECX_CNT.append(valCount)
	objs[o].listOP_BaseDecECX_NumOps.append(numOps)
	objs[o].listOP_BaseDecECX_Module.append(modName)
def addListBaseDecEDX(address, valCount, numOps, modName):
	objs[o].listOP_BaseDecEDX.append(address)
	objs[o].listOP_BaseDecEDX_CNT.append(valCount)
	objs[o].listOP_BaseDecEDX_NumOps.append(numOps)
	objs[o].listOP_BaseDecEDX_Module.append(modName)
def addListBaseDecESI(address, valCount, numOps, modName):
	objs[o].listOP_BaseDecESI.append(address)
	objs[o].listOP_BaseDecESI_CNT.append(valCount)
	objs[o].listOP_BaseDecESI_NumOps.append(numOps)
	objs[o].listOP_BaseDecESI_Module.append(modName)
def addListBaseDecEDI(address, valCount, numOps, modName):
	objs[o].listOP_BaseDecEDI.append(address)
	objs[o].listOP_BaseDecEDI_CNT.append(valCount)
	objs[o].listOP_BaseDecEDI_NumOps.append(numOps)
	objs[o].listOP_BaseDecEDI_Module.append(modName)
def addListBaseDecESP(address, valCount, numOps, modName):
	objs[o].listOP_BaseDecESP.append(address)
	objs[o].listOP_BaseDecESP_CNT.append(valCount)
	objs[o].listOP_BaseDecESP_NumOps.append(numOps)
	objs[o].listOP_BaseDecESP_Module.append(modName)
def addListBaseDecEBP(address, valCount, numOps, modName):
	objs[o].listOP_BaseDecEBP.append(address)
	objs[o].listOP_BaseDecEBP_CNT.append(valCount)
	objs[o].listOP_BaseDecEBP_NumOps.append(numOps)
	objs[o].listOP_BaseDecEBP_Module.append(modName)

#Xchg
def addListBaseXchg(address, valCount, numOps, modName):
	objs[o].listOP_BaseXchg.append(address)
	objs[o].listOP_BaseXchg_CNT.append(valCount)
	objs[o].listOP_BaseXchg_NumOps.append(numOps)
	objs[o].listOP_BaseXchg_Module.append(modName)
def addListBaseXchgEAX(address, valCount, numOps, modName):
	objs[o].listOP_BaseXchgEAX.append(address)
	objs[o].listOP_BaseXchgEAX_CNT.append(valCount)
	objs[o].listOP_BaseXchgEAX_NumOps.append(numOps)
	objs[o].listOP_BaseXchgEAX_Module.append(modName)
def addListBaseXchgEBX(address, valCount, numOps, modName):
	objs[o].listOP_BaseXchgEBX.append(address)
	objs[o].listOP_BaseXchgEBX_CNT.append(valCount)
	objs[o].listOP_BaseXchgEBX_NumOps.append(numOps)
	objs[o].listOP_BaseXchgEBX_Module.append(modName)
def addListBaseXchgECX(address, valCount, numOps, modName):
	objs[o].listOP_BaseXchgECX.append(address)
	objs[o].listOP_BaseXchgECX_CNT.append(valCount)
	objs[o].listOP_BaseXchgECX_NumOps.append(numOps)
	objs[o].listOP_BaseXchgECX_Module.append(modName)
def addListBaseXchgEDX(address, valCount, numOps, modName):
	objs[o].listOP_BaseXchgEDX.append(address)
	objs[o].listOP_BaseXchgEDX_CNT.append(valCount)
	objs[o].listOP_BaseXchgEDX_NumOps.append(numOps)
	objs[o].listOP_BaseXchgEDX_Module.append(modName)
def addListBaseXchgESI(address, valCount, numOps, modName):
	objs[o].listOP_BaseXchgESI.append(address)
	objs[o].listOP_BaseXchgESI_CNT.append(valCount)
	objs[o].listOP_BaseXchgESI_NumOps.append(numOps)
	objs[o].listOP_BaseXchgESI_Module.append(modName)
def addListBaseXchgEDI(address, valCount, numOps, modName):
	objs[o].listOP_BaseXchgEDI.append(address)
	objs[o].listOP_BaseXchgEDI_CNT.append(valCount)
	objs[o].listOP_BaseXchgEDI_NumOps.append(numOps)
	objs[o].listOP_BaseXchgEDI_Module.append(modName)
def addListBaseXchgESP(address, valCount, numOps, modName):
	objs[o].listOP_BaseXchgESP.append(address)
	objs[o].listOP_BaseXchgESP_CNT.append(valCount)
	objs[o].listOP_BaseXchgESP_NumOps.append(numOps)
	objs[o].listOP_BaseXchgESP_Module.append(modName)
def addListBaseXchgEBP(address, valCount, numOps, modName):
	objs[o].listOP_BaseXchgEBP.append(address)
	objs[o].listOP_BaseXchgEBP_CNT.append(valCount)
	objs[o].listOP_BaseXchgEBP_NumOps.append(numOps)
	objs[o].listOP_BaseXchgEBX_Module.append(modName)
#LEFT SHIFT
def addListBaseShiftLeft(address, valCount, numOps, modName):
	objs[o].listOP_BaseShiftLeft.append(address)
	objs[o].listOP_BaseShiftLeft_CNT.append(valCount)
	objs[o].listOP_BaseShiftLeft_NumOps.append(numOps)
	objs[o].listOP_BaseShiftLeft_Module.append(modName)
#RIGHT SHIFT
def addListBaseShiftRight(address, valCount, numOps, modName):
	objs[o].listOP_BaseShiftRight.append(address)
	objs[o].listOP_BaseShiftRight_CNT.append(valCount)
	objs[o].listOP_BaseShiftRight_NumOps.append(numOps)
	objs[o].listOP_BaseShiftRight_Module.append(modName)
#ROTATE RIGHT
def addListBaseRotRight(address, valCount, numOps, modName):
	objs[o].listOP_BaseRotRight.append(address)
	objs[o].listOP_BaseRotRight_CNT.append(valCount)
	objs[o].listOP_BaseRotRight_NumOps.append(numOps)
	objs[o].listOP_BaseRotRight_Module.append(modName)
#ROTATE LEFT
def addListBaseRotLeft(address, valCount, numOps, modName):
	objs[o].listOP_BaseRotLeft.append(address)
	objs[o].listOP_BaseRotLeft_CNT.append(valCount)
	objs[o].listOP_BaseRotLeft_NumOps.append(numOps)
	objs[o].listOP_BaseRotLeft_Module.append(modName)

def clearListAddAll():
	objs[o].listOP_BaseAdd[:] = []
	objs[o].listOP_BaseAdd_CNT[:] = []
	objs[o].listOP_BaseAdd_NumOps[:] = []
	objs[o].listOP_BaseAddEAX[:] = []
	objs[o].listOP_BaseAddEAX_CNT[:] = []
	objs[o].listOP_BaseAddEAX_NumOps[:] = []
	objs[o].listOP_BaseAddEBX[:] = []
	objs[o].listOP_BaseAddEBX_CNT[:] = []
	objs[o].listOP_BaseAddEBX_NumOps[:] = []
	objs[o].listOP_BaseAddECX[:] = []
	objs[o].listOP_BaseAddECX_CNT[:] = []
	objs[o].listOP_BaseAddECX_NumOps[:] = []
	objs[o].listOP_BaseAddEDX[:] = []
	objs[o].listOP_BaseAddEDX_CNT[:] = []
	objs[o].listOP_BaseAddEDX_NumOps[:] = []
	objs[o].listOP_BaseAddESI[:] = []
	objs[o].listOP_BaseAddESI_CNT[:] = []
	objs[o].listOP_BaseAddESI_NumOps[:] = []
	objs[o].listOP_BaseAddEDI[:] = []
	objs[o].listOP_BaseAddEDI_CNT[:] = []
	objs[o].listOP_BaseAddEDI_NumOps[:] = []
	objs[o].listOP_BaseAddESP[:] = []
	objs[o].listOP_BaseAddESP_CNT[:] = []
	objs[o].listOP_BaseAddESP_NumOps[:] = []
	objs[o].listOP_BaseAddEBP[:] = []
	objs[o].listOP_BaseAddEBP_CNT[:] = []
	objs[o].listOP_BaseAddEBP_NumOps[:] = []
	objs[o].listOP_BaseAdd_Module[:] = []
	objs[o].listOP_BaseAddEBX_Module[:] = []
	objs[o].listOP_BaseAddEAX_Module[:] = []

	objs[o].listOP_BaseAddECX_Module[:] = []
	objs[o].listOP_BaseAddEDX_Module[:] = []
	objs[o].listOP_BaseAddEDI_Module[:] = []
	objs[o].listOP_BaseAddESI_Module[:] = []
	objs[o].listOP_BaseAddEBP_Module[:] = []
def clearListBaseAdd():
	objs[o].listOP_BaseAdd[:] = []
	objs[o].listOP_BaseAdd_CNT[:] = []
	objs[o].listOP_BaseAdd_NumOps[:] = []
	objs[o].listOP_BaseAdd_Module[:] = []
def clearListBaseAddEAX():
	objs[o].listOP_BaseAddEAX[:] = []
	objs[o].listOP_BaseAddEAX_CNT[:] = []
	objs[o].listOP_BaseAddEAX_NumOps[:] = []
	objs[o].listOP_BaseAddEAX_Module[:] = []
def clearListBaseAddEBX():
	objs[o].listOP_BaseAddEBX[:] = []
	objs[o].listOP_BaseAddEBX_CNT[:] = []
	objs[o].listOP_BaseAddEBX_NumOps[:] = []
	objs[o].listOP_BaseAddEBX_Module[:] = []
def clearListBaseAddECX():
	objs[o].listOP_BaseAddECX[:] = []
	objs[o].listOP_BaseAddECX_CNT[:] = []
	objs[o].listOP_BaseAddECX_NumOps[:] = []
	objs[o].listOP_BaseAddECX_Module[:] = []
def clearListBaseAddEDX():
	objs[o].listOP_BaseAddEDX[:] = []
	objs[o].listOP_BaseAddEDX_CNT[:] = []
	objs[o].listOP_BaseAddEDX_NumOps[:] = []
	objs[o].listOP_BaseAddEDX_Module[:] = []
def clearListBaseAddESI():
	objs[o].listOP_BaseAddESI[:] = []
	objs[o].listOP_BaseAddESI_CNT[:] = []
	objs[o].listOP_BaseAddESI_NumOps[:] = []
	objs[o].listOP_BaseAddESI_Module[:] = []
def clearListBaseAddEDI():
	objs[o].listOP_BaseAddEDI[:] = []
	objs[o].listOP_BaseAddEDI_CNT[:] = []
	objs[o].listOP_BaseAddEDI_NumOps[:] = []
	objs[o].listOP_BaseAddEDI_Module[:] = []
def clearListBaseAddESP():
	objs[o].listOP_BaseAddESP[:] = []
	objs[o].listOP_BaseAddESP_CNT[:] = []
	objs[o].listOP_BaseAddESP_NumOps[:] = []
	objs[o].listOP_BaseAddESP_Module[:] = []
def clearListBaseAddEBP():
	objs[o].listOP_BaseAddEBP[:] = []
	objs[o].listOP_BaseAddEBP_CNT[:] = []
	objs[o].listOP_BaseAddEBP_NumOps[:] = []
	objs[o].listOP_BaseAddEBP_Module[:] = []
def clearListSubAll():
	objs[o].listOP_BaseSub[:] = []
	objs[o].listOP_BaseSub_CNT[:] = []
	objs[o].listOP_BaseSub_NumOps[:] = []
	objs[o].listOP_BaseSubEAX[:] = []
	objs[o].listOP_BaseSubEAX_CNT[:] = []
	objs[o].listOP_BaseSubEAX_NumOps[:] = []
	objs[o].listOP_BaseSubEBX[:] = []
	objs[o].listOP_BaseSubEBX_CNT[:] = []
	objs[o].listOP_BaseSubEBX_NumOps[:] = []
	objs[o].listOP_BaseSubECX[:] = []
	objs[o].listOP_BaseSubECX_CNT[:] = []
	objs[o].listOP_BaseSubECX_NumOps[:] = []
	objs[o].listOP_BaseSubEDX[:] = []
	objs[o].listOP_BaseSubEDX_CNT[:] = []
	objs[o].listOP_BaseSubEDX_NumOps[:] = []
	objs[o].listOP_BaseSubESI[:] = []
	objs[o].listOP_BaseSubESI_CNT[:] = []
	objs[o].listOP_BaseSubESI_NumOps[:] = []
	objs[o].listOP_BaseSubEDI[:] = []
	objs[o].listOP_BaseSubEDI_CNT[:] = []
	objs[o].listOP_BaseSubEDI_NumOps[:] = []
	objs[o].listOP_BaseSubESP[:] = []
	objs[o].listOP_BaseSubESP_CNT[:] = []
	objs[o].listOP_BaseSubESP_NumOps[:] = []
	objs[o].listOP_BaseSubEBP[:] = []
	objs[o].listOP_BaseSubEBP_CNT[:] = []
	objs[o].listOP_BaseSubEBP_NumOps[:] = []
	objs[o].listOP_BaseSubEAX_Module[:] = []
	objs[o].listOP_BaseSubEBX_Module[:] = []
	objs[o].listOP_BaseSubECX_Module[:] = []
	objs[o].listOP_BaseSubEDX_Module[:] = []
	objs[o].listOP_BaseSubESI_Module[:] = []
	objs[o].listOP_BaseSubEDI_Module[:] = []
	objs[o].listOP_BaseSubEBP_Module[:] = []
	objs[o].listOP_BaseSub_Module[:] = []

def clearListBaseSub():
	objs[o].listOP_BaseSub[:] = []
	objs[o].listOP_BaseSub_CNT[:] = []
	objs[o].listOP_BaseSub_NumOps[:] = []
	objs[o].listOP_BaseSub_Module[:] = []
def clearListBaseSubEAX():
	objs[o].listOP_BaseSubEAX[:] = []
	objs[o].listOP_BaseSubEAX_CNT[:] = []
	objs[o].listOP_BaseSubEAX_NumOps[:] = []
	objs[o].listOP_BaseSubEAX_Module[:] = []
def clearListBaseSubEBX():
	objs[o].listOP_BaseSubEBX[:] = []
	objs[o].listOP_BaseSubEBX_CNT[:] = []
	objs[o].listOP_BaseSubEBX_NumOps[:] = []
	objs[o].listOP_BaseSubEBX_Module[:] = []
def clearListBaseSubECX():
	objs[o].listOP_BaseSubECX[:] = []
	objs[o].listOP_BaseSubECX_CNT[:] = []
	objs[o].listOP_BaseSubECX_NumOps[:] = []
	objs[o].listOP_BaseSubECX_Module[:] = []
def clearListBaseSubEDX():
	objs[o].listOP_BaseSubEDX[:] = []
	objs[o].listOP_BaseSubEDX_CNT[:] = []
	objs[o].listOP_BaseSubEDX_NumOps[:] = []
	objs[o].listOP_BaseSubEDX_Module[:] = []
def clearListBaseSubESI():
	objs[o].listOP_BaseSubESI[:] = []
	objs[o].listOP_BaseSubESI_CNT[:] = []
	objs[o].listOP_BaseSubESI_NumOps[:] = []
	objs[o].listOP_BaseSubESI_Module[:] = []
def clearListBaseSubEDI():
	objs[o].listOP_BaseSubEDI[:] = []
	objs[o].listOP_BaseSubEDI_CNT[:] = []
	objs[o].listOP_BaseSubEDI_NumOps[:] = []
	objs[o].listOP_BaseSubEDI_Module[:] = []
def clearListBaseSubESP():
	objs[o].listOP_BaseSubESP[:] = []
	objs[o].listOP_BaseSubESP_CNT[:] = []
	objs[o].listOP_BaseSubESP_NumOps[:] = []
	objs[o].listOP_BaseSubESP_Module[:] = []
def clearListBaseSubEBP():
	objs[o].listOP_BaseSubEBP[:] = []
	objs[o].listOP_BaseSubEBP_CNT[:] = []
	objs[o].listOP_BaseSubEBP_NumOps[:] = []
	objs[o].listOP_BaseSubEBP_Module[:] = []

def clearListBaseMulECX():
	objs[o].listOP_BaseMulECX[:] = []
	objs[o].listOP_BaseMulECX_CNT[:] = []
	objs[o].listOP_BaseMulECX_NumOps[:] = []
	objs[o].listOP_BaseMulECX_Module[:] = []
#add list Sub 
def clearListMulAll():
	objs[o].listOP_BaseMul[:] = []
	objs[o].listOP_BaseMul_CNT[:] = []
	objs[o].listOP_BaseMul_NumOps[:] = []
	objs[o].listOP_BaseMulEAX[:] = []
	objs[o].listOP_BaseMulEAX_CNT[:] = []
	objs[o].listOP_BaseMulEAX_NumOps[:] = []
	objs[o].listOP_BaseMulEBX[:] = []
	objs[o].listOP_BaseMulEBX_CNT[:] = []
	objs[o].listOP_BaseMulEBX_NumOps[:] = []
	objs[o].listOP_BaseMulECX[:] = []
	objs[o].listOP_BaseMulECX_CNT[:] = []
	objs[o].listOP_BaseMulECX_NumOps[:] = []
	objs[o].listOP_BaseMulEDX[:] = []
	objs[o].listOP_BaseMulEDX_CNT[:] = []
	objs[o].listOP_BaseMulEDX_NumOps[:] = []
	objs[o].listOP_BaseMulESI[:] = []
	objs[o].listOP_BaseMulESI_CNT[:] = []
	objs[o].listOP_BaseMulESI_NumOps[:] = []
	objs[o].listOP_BaseMulEDI[:] = []
	objs[o].listOP_BaseMulEDI_CNT[:] = []
	objs[o].listOP_BaseMulEDI_NumOps[:] = []
	objs[o].listOP_BaseMulESP[:] = []
	objs[o].listOP_BaseMulESP_CNT[:] = []
	objs[o].listOP_BaseMulESP_NumOps[:] = []
	objs[o].listOP_BaseMulEBP[:] = []
	objs[o].listOP_BaseMulEBP_CNT[:] = []
	objs[o].listOP_BaseMulEBP_NumOps[:] = []
	objs[o].listOP_BaseMul_Module[:] = []
	objs[o].listOP_BaseMulEAX_Module[:] = []
	objs[o].listOP_BaseMulEBX_Module[:] = []
	objs[o].listOP_BaseMulECX_Module[:] = []
	objs[o].listOP_BaseMulEDX_Module[:] = []
	objs[o].listOP_BaseMulEDI_Module[:] = []
	objs[o].listOP_BaseMulESI_Module[:] = []
	objs[o].listOP_BaseMulEBP_Module[:] = []
#add list Mul 
def clearListBaseMul():
	objs[o].listOP_BaseMul[:] = []
	objs[o].listOP_BaseMul_CNT[:] = []
	objs[o].listOP_BaseMul_NumOps[:] = []
	objs[o].listOP_BaseMul_Module[:] = []
def clearListBaseMulEAX():
	objs[o].listOP_BaseMulEAX[:] = []
	objs[o].listOP_BaseMulEAX_CNT[:] = []
	objs[o].listOP_BaseMulEAX_NumOps[:] = []
	objs[o].listOP_BaseMulEAX_Module[:] = []
def clearListBaseMulEBX():
	objs[o].listOP_BaseMulEBX[:] = []
	objs[o].listOP_BaseMulEBX_CNT[:] = []
	objs[o].listOP_BaseMulEBX_NumOps[:] = []
	objs[o].listOP_BaseMulEBX_Module[:] = []
def clearListBaseMulECX():
	objs[o].listOP_BaseMulECX[:] = []
	objs[o].listOP_BaseMulECX_CNT[:] = []
	objs[o].listOP_BaseMulECX_NumOps[:] = []
	objs[o].listOP_BaseMulECX_Module[:] = []
def clearListBaseMulEDX():
	objs[o].listOP_BaseMulEDX[:] = []
	objs[o].listOP_BaseMulEDX_CNT[:] = []
	objs[o].listOP_BaseMulEDX_NumOps[:] = []
	objs[o].listOP_BaseMulEDX_Module[:] = []
def clearListBaseMulESI():
	objs[o].listOP_BaseMulESI[:] = []
	objs[o].listOP_BaseMulESI_CNT[:] = []
	objs[o].listOP_BaseMulESI_NumOps[:] = []
	objs[o].listOP_BaseMulESI_Module[:] = []
def clearListBaseMulEDI():
	objs[o].listOP_BaseMulEDI[:] = []
	objs[o].listOP_BaseMulEDI_CNT[:] = []
	objs[o].listOP_BaseMulEDI_NumOps[:] = []
	objs[o].listOP_BaseMulEDI_Module[:] = []
def clearListBaseMulESP():
	objs[o].listOP_BaseMulESP[:] = []
	objs[o].listOP_BaseMulESP_CNT[:] = []
	objs[o].listOP_BaseMulESP_NumOps[:] = []
	objs[o].listOP_BaseMulESP_Module[:] = []
def clearListBaseMulEBP():
	objs[o].listOP_BaseMulEBP[:] = []
	objs[o].listOP_BaseMulEBP_CNT[:] = []
	objs[o].listOP_BaseMulEBP_NumOps[:] = []
	objs[o].listOP_BaseMulEBP_Module[:] = []
def clearListBaseMul():
	objs[o].listOP_BaseMul[:] = []
	objs[o].listOP_BaseMul_CNT[:] = []
	objs[o].listOP_BaseMul_NumOps[:] = []
	objs[o].listOP_BaseMul_Module[:] = []

#DIV

def clearListDiv():
	objs[o].listOP_BaseDiv[:] = []
	objs[o].listOP_BaseDiv_CNT[:] = []
	objs[o].listOP_BaseDiv_NumOps[:] = []
	objs[o].listOP_BaseDivEAX[:] = []
	objs[o].listOP_BaseDivEAX_CNT[:] = []
	objs[o].listOP_BaseDivEAX_NumOps[:] = []
	objs[o].listOP_BaseDivEDX[:] = []
	objs[o].listOP_BaseDivEDX_CNT[:] = []
	objs[o].listOP_BaseDivEDX_NumOps[:] = []
	objs[o].listOP_BaseDiv_Module[:] = []
	objs[o].listOP_BaseDivEAX_Module[:] = []
	objs[o].listOP_BaseDivEDX_Module[:] = []
def clearListBaseDiv():
	objs[o].listOP_BaseDiv[:] = []
	objs[o].listOP_BaseDiv_CNT[:] = []
	objs[o].listOP_BaseDiv_NumOps[:] = []
	objs[o].listOP_BaseDiv_Module[:] = []
def clearListBaseDivEAX():
	objs[o].listOP_BaseDivEAX[:] = []
	objs[o].listOP_BaseDivEAX_CNT[:] = []
	objs[o].listOP_BaseDivEAX_NumOps[:] = []
	objs[o].listOP_BaseDivEAX_Module[:] = []
def clearListBaseDivEDX():
	objs[o].listOP_BaseDivEDX[:] = []
	objs[o].listOP_BaseDivEDX_CNT[:] = []
	objs[o].listOP_BaseDivEDX_NumOps[:] = []
	objs[o].listOP_BaseDivEDX_Module[:] = []

def clearListBaseMulECX():
	objs[o].listOP_BaseMulECX[:] = []
	objs[o].listOP_BaseMulECX_CNT[:] = []
	objs[o].listOP_BaseMulECX_NumOps[:] = []
	objs[o].listOP_BaseMulECX_Module[:] = []
#MOV
def clearListMovAll():
	objs[o].listOP_BaseMov[:] = []
	objs[o].listOP_BaseMov_CNT[:] = []
	objs[o].listOP_BaseMov_NumOps[:] = []
	objs[o].listOP_BaseMovEAX[:] = []
	objs[o].listOP_BaseMovEAX_CNT[:] = []
	objs[o].listOP_BaseMovEAX_NumOps[:] = []
	objs[o].listOP_BaseMovEBX[:] = []
	objs[o].listOP_BaseMovEBX_CNT[:] = []
	objs[o].listOP_BaseMovEBX_NumOps[:] = []
	objs[o].listOP_BaseMovECX[:] = []
	objs[o].listOP_BaseMovECX_CNT[:] = []
	objs[o].listOP_BaseMovECX_NumOps[:] = []
	objs[o].listOP_BaseMovEDX[:] = []
	objs[o].listOP_BaseMovEDX_CNT[:] = []
	objs[o].listOP_BaseMovEDX_NumOps[:] = []
	objs[o].listOP_BaseMovESI[:] = []
	objs[o].listOP_BaseMovESI_CNT[:] = []
	objs[o].listOP_BaseMovESI_NumOps[:] = []
	objs[o].listOP_BaseMovEDI[:] = []
	objs[o].listOP_BaseMovEDI_CNT[:] = []
	objs[o].listOP_BaseMovEDI_NumOps[:] = []
	objs[o].listOP_BaseMovESP[:] = []
	objs[o].listOP_BaseMovESP_CNT[:] = []
	objs[o].listOP_BaseMovESP_NumOps[:] = []
	objs[o].listOP_BaseMovEBP[:] = []
	objs[o].listOP_BaseMovEBP_CNT[:] = []
	objs[o].listOP_BaseMovEBP_NumOps[:] = []
	objs[o].listOP_BaseMov_Module = []
	objs[o].listOP_BaseMovEAX_Module = []
	objs[o].listOP_BaseMovEBX_Module = []
	objs[o].listOP_BaseMovECX_Module = []
	objs[o].listOP_BaseMovEDX_Module = []
	objs[o].listOP_BaseMovESI_Module = []
	objs[o].listOP_BaseMovEDI_Module = []
	objs[o].listOP_BaseMovEBP_Module = []

def clearListBaseMov():
	objs[o].listOP_BaseMov[:] = []
	objs[o].listOP_BaseMov_CNT[:] = []
	objs[o].listOP_BaseMov_NumOps[:] = []
	objs[o].listOP_BaseMov_Module = []
def clearListBaseMovEAX():
	objs[o].listOP_BaseMovEAX[:] = []
	objs[o].listOP_BaseMovEAX_CNT[:] = []
	objs[o].listOP_BaseMovEAX_NumOps[:] = []
	objs[o].listOP_BaseMovEAX_Module = []
def clearListBaseMovEBX():
	objs[o].listOP_BaseMovEBX[:] = []
	objs[o].listOP_BaseMovEBX_CNT[:] = []
	objs[o].listOP_BaseMovEBX_NumOps[:] = []
	objs[o].listOP_BaseMovEBX_Module = []
def clearListBaseMovECX():
	objs[o].listOP_BaseMovECX[:] = []
	objs[o].listOP_BaseMovECX_CNT[:] = []
	objs[o].listOP_BaseMovECX_NumOps[:] = []
	objs[o].listOP_BaseMovECX_Module = []
def clearListBaseMovEDX():
	objs[o].listOP_BaseMovEDX[:] = []
	objs[o].listOP_BaseMovEDX_CNT[:] = []
	objs[o].listOP_BaseMovEDX_NumOps[:] = []
	objs[o].listOP_BaseMovEDX_Module = []
def clearListBaseMovESI():
	objs[o].listOP_BaseMovESI[:] = []
	objs[o].listOP_BaseMovESI_CNT[:] = []
	objs[o].listOP_BaseMovESI_NumOps[:] = []
	objs[o].listOP_BaseMovESI_Module = []
def clearListBaseMovEDI():
	objs[o].listOP_BaseMovEDI[:] = []
	objs[o].listOP_BaseMovEDI_CNT[:] = []
	objs[o].listOP_BaseMovEDI_NumOps[:] = []
	objs[o].listOP_BaseMovEDI_Module = []
def clearListBaseMovESP():
	objs[o].listOP_BaseMovESP[:] = []
	objs[o].listOP_BaseMovESP_CNT[:] = []
	objs[o].listOP_BaseMovESP_NumOps[:] = []
	objs[o].listOP_BaseMovESP_Module = []
def clearListBaseMovEBP():
	objs[o].listOP_BaseMovEBP[:] = []
	objs[o].listOP_BaseMovEBP_CNT[:] = []
	objs[o].listOP_BaseMovEBP_NumOps[:] = []
	objs[o].listOP_BaseMovEBP_Module = []
#mov shuffle
def clearListMovShufAll():
	objs[o].listOP_BaseMovShuf[:] = []
	objs[o].listOP_BaseMovShuf_CNT[:] = []
	objs[o].listOP_BaseMovShuf_NumOps[:] = []
	objs[o].listOP_BaseMovShufEAX[:] = []
	objs[o].listOP_BaseMovShufEAX_CNT[:] = []
	objs[o].listOP_BaseMovShufEAX_NumOps[:] = []
	objs[o].listOP_BaseMovShufEBX[:] = []
	objs[o].listOP_BaseMovShufEBX_CNT[:] = []
	objs[o].listOP_BaseMovShufEBX_NumOps[:] = []
	objs[o].listOP_BaseMovShufECX[:] = []
	objs[o].listOP_BaseMovShufECX_CNT[:] = []
	objs[o].listOP_BaseMovShufECX_NumOps[:] = []
	objs[o].listOP_BaseMovShufEDX[:] = []
	objs[o].listOP_BaseMovShufEDX_CNT[:] = []
	objs[o].listOP_BaseMovShufEDX_NumOps[:] = []
	objs[o].listOP_BaseMovShufESI[:] = []
	objs[o].listOP_BaseMovShufESI_CNT[:] = []
	objs[o].listOP_BaseMovShufESI_NumOps[:] = []
	objs[o].listOP_BaseMovShufEDI[:] = []
	objs[o].listOP_BaseMovShufEDI_CNT[:] = []
	objs[o].listOP_BaseMovShufEDI_NumOps[:] = []
	objs[o].listOP_BaseMovShufESP[:] = []
	objs[o].listOP_BaseMovShufESP_CNT[:] = []
	objs[o].listOP_BaseMovShufESP_NumOps[:] = []
	objs[o].listOP_BaseMovShufEBP[:] = []
	objs[o].listOP_BaseMovShufEBP_CNT[:] = []
	objs[o].listOP_BaseMovShufEBP_NumOps[:] = []
	objs[o].listOP_BaseMovShuf_Module [:] = []
	objs[o].listOP_BaseMovShufEAX_Module [:] = []
	objs[o].listOP_BaseMovShufEBX_Module [:] = []
	objs[o].listOP_BaseMovShufECX_Module [:] = []
	objs[o].listOP_BaseMovShufEDX_Module [:] = []
	objs[o].listOP_BaseMovShufESI_Module [:] = []
	objs[o].listOP_BaseMovShufEDI_Module [:] = []
	objs[o].listOP_BaseMovShufEBP_Module [:] = []
	objs[o].listOP_BaseMovDeref[:] = []
	objs[o].listOP_BaseMovDeref_CNT[:] = []
	objs[o].listOP_BaseMovDeref_NumOps[:] = []
	objs[o].listOP_BaseMovDeref_Module[:] = []
	objs[o].listOP_BaseMovDerefEAX
	objs[o].listOP_BaseMovDerefEAX_CNT[:] = []
	objs[o].listOP_BaseMovDerefEAX_NumOps[:] = []
	objs[o].listOP_BaseMovDerefEAX_Module[:] = []
	objs[o].listOP_BaseMovDerefEBX[:] = []
	objs[o].listOP_BaseMovDerefEBX_CNT[:] = []
	objs[o].listOP_BaseMovDerefEBX_NumOps[:] = []
	objs[o].listOP_BaseMovDerefEBX_Module[:] = []
	objs[o].listOP_BaseMovDerefECX[:] = []
	objs[o].listOP_BaseMovDerefECX_CNT[:] = []
	objs[o].listOP_BaseMovDerefECX_NumOps[:] = []
	objs[o].listOP_BaseMovDerefECX_Module[:] = []
	objs[o].listOP_BaseMovDerefEDX[:] = []
	objs[o].listOP_BaseMovDerefEDX_CNT[:] = []
	objs[o].listOP_BaseMovDerefEDX_NumOps[:] = []
	objs[o].listOP_BaseMovDerefEDX_Module[:] = []
	objs[o].listOP_BaseMovDerefESI[:] = []
	objs[o].listOP_BaseMovDerefESI_CNT[:] = []
	objs[o].listOP_BaseMovDerefESI_NumOps[:] = []
	objs[o].listOP_BaseMovDerefESI_Module[:] = []
	objs[o].listOP_BaseMovDerefEDI[:] = []
	objs[o].listOP_BaseMovDerefEDI_CNT[:] = []
	objs[o].listOP_BaseMovDerefEDI_NumOps[:] = []
	objs[o].listOP_BaseMovDerefEDI_Module[:] = []
	objs[o].listOP_BaseMovDerefESP[:] = []
	objs[o].listOP_BaseMovDerefESP_CNT[:] = []
	objs[o].listOP_BaseMovDerefESP_NumOps[:] = []
	objs[o].listOP_BaseMovDerefESP_Module[:] = []
	objs[o].listOP_BaseMovDerefEBP[:] = []
	objs[o].listOP_BaseMovDerefEBP_CNT[:] = []
	objs[o].listOP_BaseMovDerefEBP_NumOps[:] = []
	objs[o].listOP_BaseMovDerefEBP_Module[:] = []
def clearListBaseMovShuf():
	objs[o].listOP_BaseMovShuf[:] = []
	objs[o].listOP_BaseMovShuf_CNT[:] = []
	objs[o].listOP_BaseMovShuf_NumOps[:] = []
	objs[o].listOP_BaseMovShuf_Module = []
def clearListBaseMovShufEAX():
	objs[o].listOP_BaseMovShufEAX[:] = []
	objs[o].listOP_BaseMovShufEAX_CNT[:] = []
	objs[o].listOP_BaseMovShufEAX_NumOps[:] = []
	objs[o].listOP_BaseMovShufEAX_Module = []
def clearListBaseMovShufEBX():
	objs[o].listOP_BaseMovShufEBX[:] = []
	objs[o].listOP_BaseMovShufEBX_CNT[:] = []
	objs[o].listOP_BaseMovShufEBX_NumOps[:] = []
	objs[o].listOP_BaseMovShufEBX_Module = []
def clearListBaseMovShufECX():
	objs[o].listOP_BaseMovShufECX[:] = []
	objs[o].listOP_BaseMovShufECX_CNT[:] = []
	objs[o].listOP_BaseMovShufECX_NumOps[:] = []
	objs[o].listOP_BaseMovShufECX_Module = []
def clearListBaseMovShufEDX():
	objs[o].listOP_BaseMovShufEDX[:] = []
	objs[o].listOP_BaseMovShufEDX_CNT[:] = []
	objs[o].listOP_BaseMovShufEDX_NumOps[:] = []
	objs[o].listOP_BaseMovShufEDX_Module = []
def clearListBaseMovShufESI():
	objs[o].listOP_BaseMovShufESI[:] = []
	objs[o].listOP_BaseMovShufESI_CNT[:] = []
	objs[o].listOP_BaseMovShufESI_NumOps[:] = []
	objs[o].listOP_BaseMovShufESI_Module = []
def clearListBaseMovShufEDI():
	objs[o].listOP_BaseMovShufEDI[:] = []
	objs[o].listOP_BaseMovShufEDI_CNT[:] = []
	objs[o].listOP_BaseMovShufEDI_NumOps[:] = []
	objs[o].listOP_BaseMovShufEDI_Module = []
def clearListBaseMovShufESP():
	objs[o].listOP_BaseMovShufESP[:] = []
	objs[o].listOP_BaseMovShufESP_CNT[:] = []
	objs[o].listOP_BaseMovShufESP_NumOps[:] = []
	objs[o].listOP_BaseMovShufESP_Module = []
def clearListBaseMovShufEBP():
	objs[o].listOP_BaseMovShufEBP[:] = []
	objs[o].listOP_BaseMovShufEBP_CNT[:] = []
	objs[o].listOP_BaseMovShufEBP_NumOps[:] = []
	objs[o].listOP_BaseMovShufEBP_Module = []
#mov value into reg
def clearListMovValAll():
	objs[o].listOP_BaseMovVal[:] = []
	objs[o].listOP_BaseMovVal_CNT[:] = []
	objs[o].listOP_BaseMovVal_NumOps[:] = []
	objs[o].listOP_BaseMovValEAX[:] = []
	objs[o].listOP_BaseMovValEAX_CNT[:] = []
	objs[o].listOP_BaseMovValEAX_NumOps[:] = []
	objs[o].listOP_BaseMovValEBX[:] = []
	objs[o].listOP_BaseMovValEBX_CNT[:] = []
	objs[o].listOP_BaseMovValEBX_NumOps[:] = []
	objs[o].listOP_BaseMovValECX[:] = []
	objs[o].listOP_BaseMovValECX_CNT[:] = []
	objs[o].listOP_BaseMovValECX_NumOps[:] = []
	objs[o].listOP_BaseMovValEDX[:] = []
	objs[o].listOP_BaseMovValEDX_CNT[:] = []
	objs[o].listOP_BaseMovValEDX_NumOps[:] = []
	objs[o].listOP_BaseMovValESI[:] = []
	objs[o].listOP_BaseMovValESI_CNT[:] = []
	objs[o].listOP_BaseMovValESI_NumOps[:] = []
	objs[o].listOP_BaseMovValEDI[:] = []
	objs[o].listOP_BaseMovValEDI_CNT[:] = []
	objs[o].listOP_BaseMovValEDI_NumOps[:] = []
	objs[o].listOP_BaseMovValESP[:] = []
	objs[o].listOP_BaseMovValESP_CNT[:] = []
	objs[o].listOP_BaseMovValESP_NumOps[:] = []
	objs[o].listOP_BaseMovValEBP[:] = []
	objs[o].listOP_BaseMovValEBP_CNT[:] = []
	objs[o].listOP_BaseMovValEBP_NumOps[:] = []
	objs[o].listOP_BaseMovVal_Module = []
	objs[o].listOP_BaseMovValEAX_Module = []
	objs[o].listOP_BaseMovValEBX_Module = []
	objs[o].listOP_BaseMovValECX_Module = []
	objs[o].listOP_BaseMovValEDX_Module = []
	objs[o].listOP_BaseMovValESI_Module = []
	objs[o].listOP_BaseMovValEDI_Module = []
	objs[o].listOP_BaseMovValEBP_Module = []
def clearListBaseMovVal():
	objs[o].listOP_BaseMovVal[:] = []
	objs[o].listOP_BaseMovVal_CNT[:] = []
	objs[o].listOP_BaseMovVal_NumOps[:] = []
	objs[o].listOP_BaseMovVal_Module = []
def clearListBaseMovValEAX():
	objs[o].listOP_BaseMovValEAX[:] = []
	objs[o].listOP_BaseMovValEAX_CNT[:] = []
	objs[o].listOP_BaseMovValEAX_NumOps[:] = []
	objs[o].listOP_BaseMovValEAX_Module = []
def clearListBaseMovValEBX():
	objs[o].listOP_BaseMovValEBX[:] = []
	objs[o].listOP_BaseMovValEBX_CNT[:] = []
	objs[o].listOP_BaseMovValEBX_NumOps[:] = []
	objs[o].listOP_BaseMovValEBX_Module = []
def clearListBaseMovValECX():
	objs[o].listOP_BaseMovValECX[:] = []
	objs[o].listOP_BaseMovValECX_CNT[:] = []
	objs[o].listOP_BaseMovValECX_NumOps[:] = []
	objs[o].listOP_BaseMovValECX_Module = []
def clearListBaseMovValEDX():
	objs[o].listOP_BaseMovValEDX[:] = []
	objs[o].listOP_BaseMovValEDX_CNT[:] = []
	objs[o].listOP_BaseMovValEDX_NumOps[:] = []
	objs[o].listOP_BaseMovValEDX_Module = []
def clearListBaseMovValESI():
	objs[o].listOP_BaseMovValESI[:] = []
	objs[o].listOP_BaseMovValESI_CNT[:] = []
	objs[o].listOP_BaseMovValESI_NumOps[:] = []
	objs[o].listOP_BaseMovValESI_Module = []
def clearListBaseMovValEDI():
	objs[o].listOP_BaseMovValEDI[:] = []
	objs[o].listOP_BaseMovValEDI_CNT[:] = []
	objs[o].listOP_BaseMovValEDI_NumOps[:] = []
	objs[o].listOP_BaseMovValEDI_Module = []
def clearListBaseMovValESP():
	objs[o].listOP_BaseMovValESP[:] = []
	objs[o].listOP_BaseMovValESP_CNT[:] = []
	objs[o].listOP_BaseMovValESP_NumOps[:] = []
	objs[o].listOP_BaseMovValESP_Module = []
def clearListBaseMovValEBP():
	objs[o].listOP_BaseMovValEBP[:] = []
	objs[o].listOP_BaseMovValEBP_CNT[:] = []
	objs[o].listOP_BaseMovShufEBP_NumOps[:] = []
	objs[o].listOP_BaseMovValEBP_Module = []
#LEA
def clearListLeaAll():
	objs[o].listOP_BaseLea[:] = []
	objs[o].listOP_BaseLea_CNT[:] = []
	objs[o].listOP_BaseLea_NumOps[:] = []
	objs[o].listOP_BaseLeaEAX[:] = []
	objs[o].listOP_BaseLeaEAX_CNT[:] = []
	objs[o].listOP_BaseLeaEAX_NumOps[:] = []
	objs[o].listOP_BaseLeaEBX[:] = []
	objs[o].listOP_BaseLeaEBX_CNT[:] = []
	objs[o].listOP_BaseLeaEBX_NumOps[:] = []
	objs[o].listOP_BaseLeaECX[:] = []
	objs[o].listOP_BaseLeaECX_CNT[:] = []
	objs[o].listOP_BaseLeaECX_NumOps[:] = []
	objs[o].listOP_BaseLeaEDX[:] = []
	objs[o].listOP_BaseLeaEDX_CNT[:] = []
	objs[o].listOP_BaseLeaEDX_NumOps[:] = []
	objs[o].listOP_BaseLeaESI[:] = []
	objs[o].listOP_BaseLeaESI_CNT[:] = []
	objs[o].listOP_BaseLeaESI_NumOps[:] = []
	objs[o].listOP_BaseLeaEDI[:] = []
	objs[o].listOP_BaseLeaEDI_CNT[:] = []
	objs[o].listOP_BaseLeaEDI_NumOps[:] = []
	objs[o].listOP_BaseLeaESP[:] = []
	objs[o].listOP_BaseLeaESP_CNT[:] = []
	objs[o].listOP_BaseLeaESP_NumOps[:] = []
	objs[o].listOP_BaseLeaEBP[:] = []
	objs[o].listOP_BaseLeaEBP_CNT[:] = []
	objs[o].listOP_BaseLeaEBP_NumOps[:] = []
	objs[o].listOP_BaseLea_Module = []
	objs[o].listOP_BaseLeaEAX_Module = []
	objs[o].listOP_BaseLeaEBX_Module = []
	objs[o].listOP_BaseLeaECX_Module = []
	objs[o].listOP_BaseLeaEDX_Module = []
	objs[o].listOP_BaseLeaESI_Module = []
	objs[o].listOP_BaseLeaEDI_Module = []
	objs[o].listOP_BaseLeaEBP_Module = []
def clearListBaseLea():
	objs[o].listOP_BaseLea[:] = []
	objs[o].listOP_BaseLea_CNT[:] = []
	objs[o].listOP_BaseLea_NumOps[:] = []
	objs[o].listOP_BaseLea_Module = []
def clearListBaseLeaEAX():
	objs[o].listOP_BaseLeaEAX[:] = []
	objs[o].listOP_BaseLeaEAX_CNT[:] = []
	objs[o].listOP_BaseLeaEAX_NumOps[:] = []
	objs[o].listOP_BaseLeaEAX_Module = []
def clearListBaseLeaEBX():
	objs[o].listOP_BaseLeaEBX[:] = []
	objs[o].listOP_BaseLeaEBX_CNT[:] = []
	objs[o].listOP_BaseLeaEBX_NumOps[:] = []
	objs[o].listOP_BaseLeaEBX_Module = []
def clearListBaseLeaECX():
	objs[o].listOP_BaseLeaECX[:] = []
	objs[o].listOP_BaseLeaECX_CNT[:] = []
	objs[o].listOP_BaseLeaECX_NumOps[:] = []
	objs[o].listOP_BaseLeaECX_Module = []
def clearListBaseLeaEDX():
	objs[o].listOP_BaseLeaEDX[:] = []
	objs[o].listOP_BaseLeaEDX_CNT[:] = []
	objs[o].listOP_BaseLeaEDX_NumOps[:] = []
	objs[o].listOP_BaseLeaEDX_Module = []
def clearListBaseLeaESI():
	objs[o].listOP_BaseLeaESI[:] = []
	objs[o].listOP_BaseLeaESI_CNT[:] = []
	objs[o].listOP_BaseLeaESI_NumOps[:] = []
	objs[o].listOP_BaseLeaESI_Module = []
def clearListBaseLeaEDI():
	objs[o].listOP_BaseLeaEDI[:] = []
	objs[o].listOP_BaseLeaEDI_CNT[:] = []
	objs[o].listOP_BaseLeaEDI_NumOps[:] = []
	objs[o].listOP_BaseLeaEDI_Module = []
def clearListBaseLeaESP():
	objs[o].listOP_BaseLeaESP[:] = []
	objs[o].listOP_BaseLeaESP_CNT[:] = []
	objs[o].listOP_BaseLeaESP_NumOps[:] = []
	objs[o].listOP_BaseLeaESP_Module = []
def clearListBaseLeaEBP():
	objs[o].listOP_BaseLeaEBP[:] = []
	objs[o].listOP_BaseLeaEBP_CNT[:] = []
	objs[o].listOP_BaseLeaEBP_NumOps[:] = []
	objs[o].listOP_BaseLeaEBP_Module = []

#Push reg
def clearListPushAll():
	objs[o].listOP_BasePush[:] = []
	objs[o].listOP_BasePush_CNT[:] = []
	objs[o].listOP_BasePush_NumOps[:] = []
	objs[o].listOP_BasePushEAX[:] = []
	objs[o].listOP_BasePushEAX_CNT[:] = []
	objs[o].listOP_BasePushEAX_NumOps[:] = []
	objs[o].listOP_BasePushEBX[:] = []
	objs[o].listOP_BasePushEBX_CNT[:] = []
	objs[o].listOP_BasePushEBX_NumOps[:] = []
	objs[o].listOP_BasePushECX[:] = []
	objs[o].listOP_BasePushECX_CNT[:] = []
	objs[o].listOP_BasePushECX_NumOps[:] = []
	objs[o].listOP_BasePushEDX[:] = []
	objs[o].listOP_BasePushEDX_CNT[:] = []
	objs[o].listOP_BasePushEDX_NumOps[:] = []
	objs[o].listOP_BasePushESI[:] = []
	objs[o].listOP_BasePushESI_CNT[:] = []
	objs[o].listOP_BasePushESI_NumOps[:] = []
	objs[o].listOP_BasePushEDI[:] = []
	objs[o].listOP_BasePushEDI_CNT[:] = []
	objs[o].listOP_BasePushEDI_NumOps[:] = []
	objs[o].listOP_BasePushESP[:] = []
	objs[o].listOP_BasePushESP_CNT[:] = []
	objs[o].listOP_BasePushESP_NumOps[:] = []
	objs[o].listOP_BasePushEBP[:] = []
	objs[o].listOP_BasePushEBP_CNT[:] = []
	objs[o].listOP_BasePushEBP_NumOps[:] = []
	objs[o].listOP_BasePush_Module = []
	objs[o].listOP_BasePushEAX_Module = []
	objs[o].listOP_BasePushEBX_Module = []
	objs[o].listOP_BasePushECX_Module = []
	objs[o].listOP_BasePushEDX_Module = []
	objs[o].listOP_BasePushESI_Module = []
	objs[o].listOP_BasePushEDI_Module = []
	objs[o].listOP_BasePushEBP_Module = []

def clearListBasePush():
	objs[o].listOP_BasePush[:] = []
	objs[o].listOP_BasePush_CNT[:] = []
	objs[o].listOP_BasePush_NumOps[:] = []
	objs[o].listOP_BasePush_Module = []
def clearListBasePushEAX():
	objs[o].listOP_BasePushEAX[:] = []
	objs[o].listOP_BasePushEAX_CNT[:] = []
	objs[o].listOP_BasePushEAX_NumOps[:] = []
	objs[o].listOP_BasePushEAX_Module = []
def clearListBasePushEBX():
	objs[o].listOP_BasePushEBX[:] = []
	objs[o].listOP_BasePushEBX_CNT[:] = []
	objs[o].listOP_BasePushEBX_NumOps[:] = []
	objs[o].listOP_BasePushEBX_Module = []
def clearListBasePushECX():
	objs[o].listOP_BasePushECX[:] = []
	objs[o].listOP_BasePushECX_CNT[:] = []
	objs[o].listOP_BasePushECX_NumOps[:] = []
	objs[o].listOP_BasePushECX_Module = []
def clearListBasePushEDX():
	objs[o].listOP_BasePushEDX[:] = []
	objs[o].listOP_BasePushEDX_CNT[:] = []
	objs[o].listOP_BasePushEDX_NumOps[:] = []
	objs[o].listOP_BasePushEDX_Module = []
def clearListBasePushESI():
	objs[o].listOP_BasePushESI[:] = []
	objs[o].listOP_BasePushESI_CNT[:] = []
	objs[o].listOP_BasePushESI_NumOps[:] = []
	objs[o].listOP_BasePushESI_Module = []
def clearListBasePushEDI():
	objs[o].listOP_BasePushEDI[:] = []
	objs[o].listOP_BasePushEDI_CNT[:] = []
	objs[o].listOP_BasePushEDI_NumOps[:] = []
	objs[o].listOP_BasePushEDI_Module = []
def clearListBasePushESP():
	objs[o].listOP_BasePushESP[:] = []
	objs[o].listOP_BasePushESP_CNT[:] = []
	objs[o].listOP_BasePushESP_NumOps[:] = []
	objs[o].listOP_BasePushESP_Module = []
def clearListBasePushEBP():
	objs[o].listOP_BasePushEBP[:] = []
	objs[o].listOP_BasePushEBP_CNT[:] = []
	objs[o].listOP_BasePushEBP_NumOps[:] = []
	objs[o].listOP_BasePushEBP_Module = []
#POP
def clearListPopAll():
	objs[o].listOP_BasePop[:] = []
	objs[o].listOP_BasePop_CNT[:] = []
	objs[o].listOP_BasePop_NumOps[:] = []
	objs[o].listOP_BasePopEAX[:] = []
	objs[o].listOP_BasePopEAX_CNT[:] = []
	objs[o].listOP_BasePopEAX_NumOps[:] = []
	objs[o].listOP_BasePopEBX[:] = []
	objs[o].listOP_BasePopEBX_CNT[:] = []
	objs[o].listOP_BasePopEBX_NumOps[:] = []
	objs[o].listOP_BasePopECX[:] = []
	objs[o].listOP_BasePopECX_CNT[:] = []
	objs[o].listOP_BasePopECX_NumOps[:] = []
	objs[o].listOP_BasePopEDX[:] = []
	objs[o].listOP_BasePopEDX_CNT[:] = []
	objs[o].listOP_BasePopEDX_NumOps[:] = []
	objs[o].listOP_BasePopESI[:] = []
	objs[o].listOP_BasePopESI_CNT[:] = []
	objs[o].listOP_BasePopESI_NumOps[:] = []
	objs[o].listOP_BasePopEDI[:] = []
	objs[o].listOP_BasePopEDI_CNT[:] = []
	objs[o].listOP_BasePopEDI_NumOps[:] = []
	objs[o].listOP_BasePopESP[:] = []
	objs[o].listOP_BasePopESP_CNT[:] = []
	objs[o].listOP_BasePopESP_NumOps[:] = []
	objs[o].listOP_BasePopEBP[:] = []
	objs[o].listOP_BasePopEBP_CNT[:] = []
	objs[o].listOP_BasePopEBP_NumOps[:] = []
	objs[o].listOP_BasePop_Module [:] = []
	objs[o].listOP_BasePopEAX_Module [:] = []
	objs[o].listOP_BasePopEBX_Module [:] = []
	objs[o].listOP_BasePopECX_Module [:] = []
	objs[o].listOP_BasePopEDX_Module [:] = []
	objs[o].listOP_BasePopEDI_Module [:] = []
	objs[o].listOP_BasePopESI_Module [:] = []
	objs[o].listOP_BasePopEBP_Module [:] = []
	objs[o].listOP_RET_Pop [:] =[]
	objs[o].listOP_RET_Pop_CNT [:]=[]
	objs[o].listOP_RET_Pop_NumOps [:]=[]
	objs[o].listOP_RET_Pop_Module [:]=[]
	objs[o].listOP_RET_Pop_EAX [:] = []
	objs[o].listOP_RET_Pop_EAX_CNT [:] = []
	objs[o].listOP_RET_Pop_EAX_ [:] = []
	objs[o].listOP_RET_Pop_EAX_Module [:] = []
	objs[o].listOP_RET_Pop_EBX [:] = []
	objs[o].listOP_RET_Pop_EBX_CNT [:] = []
	objs[o].listOP_RET_Pop_EBX_ [:] = []
	objs[o].listOP_RET_Pop_EBX_Module [:] = []
	objs[o].listOP_RET_Pop_ECX [:] = []
	objs[o].listOP_RET_Pop_ECX_CNT [:] = []
	objs[o].listOP_RET_Pop_ECX_ [:] = []
	objs[o].listOP_RET_Pop_ECX_Module [:] = []
	objs[o].listOP_RET_Pop_EDX [:] = []
	objs[o].listOP_RET_Pop_EDX_CNT [:] = []
	objs[o].listOP_RET_Pop_EDX_ [:] = []
	objs[o].listOP_RET_Pop_EDX_Module [:] = []
	objs[o].listOP_RET_Pop_EDI [:] = []
	objs[o].listOP_RET_Pop_EDI_CNT [:] = []
	objs[o].listOP_RET_Pop_EDI_ [:] = []
	objs[o].listOP_RET_Pop_EDI_Module [:] = []
	objs[o].listOP_RET_Pop_ESI [:] = []
	objs[o].listOP_RET_Pop_ESI_CNT [:] = []
	objs[o].listOP_RET_Pop_ESI_ [:] = []
	objs[o].listOP_RET_Pop_ESI_Module [:] = []
	objs[o].listOP_RET_Pop_ESP [:] = []
	objs[o].listOP_RET_Pop_ESP_CNT [:] = []
	objs[o].listOP_RET_Pop_ESP_ [:] = []
	objs[o].listOP_RET_Pop_ESP_Module [:] = []
	objs[o].listOP_RET_Pop_EBP [:] = []
	objs[o].listOP_RET_Pop_EBP_CNT [:] = []
	objs[o].listOP_RET_Pop_EBP_ [:] = []
	objs[o].listOP_RET_Pop_EBP_Module [:] = []

def clearListStackPivot():
	objs[o].listOP_BaseStackPivot = []
	objs[o].listOP_BaseStackPivot_CNT = []
	objs[o].listOP_BaseStackPivot_NumOps = []
	objs[o].listOP_BaseStackPivot_Module = []
	objs[o].listOP_BaseStackPivot_Special = []
	objs[o].listOP_BaseStackPivotEAX = []
	objs[o].listOP_BaseStackPivotEAX_CNT = []
	objs[o].listOP_BaseStackPivotEAX_NumOps = []
	objs[o].listOP_BaseStackPivotEAX_Module = []
	objs[o].listOP_BaseStackPivotEAX_Special = []
	objs[o].listOP_BaseStackPivotEBX = []
	objs[o].listOP_BaseStackPivotEBX_CNT = []
	objs[o].listOP_BaseStackPivotEBX_NumOps = []
	objs[o].listOP_BaseStackPivotEBX_Module = []
	objs[o].listOP_BaseStackPivotEBX_Special = []
	objs[o].listOP_BaseStackPivotECX = []
	objs[o].listOP_BaseStackPivotECX_CNT = []
	objs[o].listOP_BaseStackPivotECX_NumOps = []
	objs[o].listOP_BaseStackPivotECX_Module = []
	objs[o].listOP_BaseStackPivotECX_Special = []
	objs[o].listOP_BaseStackPivotEDX = []
	objs[o].listOP_BaseStackPivotEDX_CNT = []
	objs[o].listOP_BaseStackPivotEDX_NumOps = []
	objs[o].listOP_BaseStackPivotEDX_Module = []
	objs[o].listOP_BaseStackPivotEDX_Special = []
	objs[o].listOP_BaseStackPivotEDI = []
	objs[o].listOP_BaseStackPivotEDI_CNT = []
	objs[o].listOP_BaseStackPivotEDI_NumOps = []
	objs[o].listOP_BaseStackPivotEDI_Module = []
	objs[o].listOP_BaseStackPivotEDI_Special = []
	objs[o].listOP_BaseStackPivotESI = []
	objs[o].listOP_BaseStackPivotESI_CNT = []
	objs[o].listOP_BaseStackPivotESI_NumOps = []
	objs[o].listOP_BaseStackPivotESI_Module = []
	objs[o].listOP_BaseStackPivotESI_Special = []
	objs[o].listOP_BaseStackPivotEBP = []
	objs[o].listOP_BaseStackPivotEBP_CNT = []
	objs[o].listOP_BaseStackPivotEBP_NumOps = []
	objs[o].listOP_BaseStackPivotEBP_Module = []
	objs[o].listOP_BaseStackPivotEBP_Special = []
	objs[o].listOP_BaseStackPivotESP = []
	objs[o].listOP_BaseStackPivotESP_CNT = []
	objs[o].listOP_BaseStackPivotESP_NumOps = []
	objs[o].listOP_BaseStackPivotESP_Module = []
	objs[o].listOP_BaseStackPivotESP_Special = []
def clearListStackPivotEAX(address, valCount, numOps, modName, special):
	objs[o].listOP_BaseStackPivotEAX = []
	objs[o].listOP_BaseStackPivotEAX_CNT = []
	objs[o].listOP_BaseStackPivotEAX_NumOps = []
	objs[o].listOP_BaseStackPivotEAX_Module = []
	objs[o].listOP_BaseStackPivotEAX_Special = []
def clearListStackPivotEBX(address, valCount, numOps, modName, special):
	objs[o].listOP_BaseStackPivotEBX = []
	objs[o].listOP_BaseStackPivotEBX_CNT = []
	objs[o].listOP_BaseStackPivotEBX_NumOps = []
	objs[o].listOP_BaseStackPivotEBX_Module = []
	objs[o].listOP_BaseStackPivotEBX_Special = []
def clearListStackPivotECX(address, valCount, numOps, modName, special):
	objs[o].listOP_BaseStackPivotECX = []
	objs[o].listOP_BaseStackPivotECX_CNT = []
	objs[o].listOP_BaseStackPivotECX_NumOps = []
	objs[o].listOP_BaseStackPivotECX_Module = []
	objs[o].listOP_BaseStackPivotECX_Special = []
def clearListStackPivotEDX(address, valCount, numOps, modName, special):
	objs[o].listOP_BaseStackPivotEDX = []
	objs[o].listOP_BaseStackPivotEDX_CNT = []
	objs[o].listOP_BaseStackPivotEDX_NumOps = []
	objs[o].listOP_BaseStackPivotEDX_Module = []
	objs[o].listOP_BaseStackPivotEDX_Special = []
def clearListStackPivotEDI(address, valCount, numOps, modName, special):
	objs[o].listOP_BaseStackPivotEDI = []
	objs[o].listOP_BaseStackPivotEDI_CNT = []
	objs[o].listOP_BaseStackPivotEDI_NumOps = []
	objs[o].listOP_BaseStackPivotEDI_Module = []
	objs[o].listOP_BaseStackPivotEDI_Special = []
def clearListStackPivotESI(address, valCount, numOps, modName, special):
	objs[o].listOP_BaseStackPivotESI = []
	objs[o].listOP_BaseStackPivotESI_CNT = []
	objs[o].listOP_BaseStackPivotESI_NumOps = []
	objs[o].listOP_BaseStackPivotESI_Module = []
	objs[o].listOP_BaseStackPivotESI_Special = []
def clearListStackPivotEBP(address, valCount, numOps, modName, special):
	objs[o].listOP_BaseStackPivotEBP = []
	objs[o].listOP_BaseStackPivotEBP_CNT = []
	objs[o].listOP_BaseStackPivotEBP_NumOps = []
	objs[o].listOP_BaseStackPivotEBP_Module = []
	objs[o].listOP_BaseStackPivotEBP_Special = []
def clearListStackPivotESP(address, valCount, numOps, modName, special):
	objs[o].listOP_BaseStackPivotESP = []
	objs[o].listOP_BaseStackPivotESP_CNT = []
	objs[o].listOP_BaseStackPivotESP_NumOps = []
	objs[o].listOP_BaseStackPivotESP_Module = []
	objs[o].listOP_BaseStackPivotESP_Special = []
def clearListBasePop():
	objs[o].listOP_BasePop[:] = []
	objs[o].listOP_BasePop_CNT[:] = []
	objs[o].listOP_BasePop_NumOps[:] = []
	objs[o].listOP_BasePop_Module = []
def clearListRETPop():
	objs[o].listOP_RET_Pop [:] = []
	objs[o].listOP_RET_Pop_CNT [:] = []
	objs[o].listOP_RET_Pop_NumOps [:] = []
	objs[o].listOP_RET_Pop_Module [:] = []
def clearListBasePopEAX():
	objs[o].listOP_BasePopEAX[:] = []
	objs[o].listOP_BasePopEAX_CNT[:] = []
	objs[o].listOP_BasePopEAX_NumOps[:] = []
	objs[o].listOP_BasePopEAX_Module = []
def clearListBasePopEBX():
	objs[o].listOP_BasePopEBX[:] = []
	objs[o].listOP_BasePopEBX_CNT[:] = []
	objs[o].listOP_BasePopEBX_NumOps[:] = []
	objs[o].listOP_BasePopEBX_Module = []
def clearListBasePopECX():
	objs[o].listOP_BasePopECX[:] = []
	objs[o].listOP_BasePopECX_CNT[:] = []
	objs[o].listOP_BasePopECX_NumOps[:] = []
	objs[o].listOP_BasePopECX_Module = []
def clearListBasePopEDX():
	objs[o].listOP_BasePopEDX[:] = []
	objs[o].listOP_BasePopEDX_CNT[:] = []
	objs[o].listOP_BasePopEDX_NumOps[:] = []
	objs[o].listOP_BasePopEDX_Module = []
def clearListBasePopESI():
	objs[o].listOP_BasePopESI[:] = []
	objs[o].listOP_BasePopESI_CNT[:] = []
	objs[o].listOP_BasePopESI_NumOps[:] = []
	objs[o].listOP_BasePopESI_Module = []
def clearListBasePopEDI():
	objs[o].listOP_BasePopEDI[:] = []
	objs[o].listOP_BasePopEDI_CNT[:] = []
	objs[o].listOP_BasePopEDI_NumOps[:] = []
	objs[o].listOP_BasePopEDI_Module = []
def clearListBasePopESP():
	objs[o].listOP_BasePopESP[:] = []
	objs[o].listOP_BasePopESP_CNT[:] = []
	objs[o].listOP_BasePopESP_NumOps[:] = []
	objs[o].listOP_BasePopESP_Module = []
def clearListBasePopEBP():
	objs[o].listOP_BasePopEBP[:] = []
	objs[o].listOP_BasePopEBP_CNT[:] = []
	objs[o].listOP_BasePopEBP_NumOps[:] = []
	objs[o].listOP_BasePopEBP_Module = []
#Inc
def clearListIncAll():
	objs[o].listOP_BaseInc[:] = []
	objs[o].listOP_BaseInc_CNT[:] = []
	objs[o].listOP_BaseInc_NumOps[:] = []
	objs[o].listOP_BaseIncEAX[:] = []
	objs[o].listOP_BaseIncEAX_CNT[:] = []
	objs[o].listOP_BaseIncEAX_NumOps[:] = []
	objs[o].listOP_BaseIncEBX[:] = []
	objs[o].listOP_BaseIncEBX_CNT[:] = []
	objs[o].listOP_BaseIncEBX_NumOps[:] = []
	objs[o].listOP_BaseIncECX[:] = []
	objs[o].listOP_BaseIncECX_CNT[:] = []
	objs[o].listOP_BaseIncECX_NumOps[:] = []
	objs[o].listOP_BaseIncEDX[:] = []
	objs[o].listOP_BaseIncEDX_CNT[:] = []
	objs[o].listOP_BaseIncEDX_NumOps[:] = []
	objs[o].listOP_BaseIncESI[:] = []
	objs[o].listOP_BaseIncESI_CNT[:] = []
	objs[o].listOP_BaseIncESI_NumOps[:] = []
	objs[o].listOP_BaseIncEDI[:] = []
	objs[o].listOP_BaseIncEDI_CNT[:] = []
	objs[o].listOP_BaseIncEDI_NumOps[:] = []
	objs[o].listOP_BaseIncESP[:] = []
	objs[o].listOP_BaseIncESP_CNT[:] = []
	objs[o].listOP_BaseIncESP_NumOps[:] = []
	objs[o].listOP_BaseIncEBP[:] = []
	objs[o].listOP_BaseIncEBP_CNT[:] = []
	objs[o].listOP_BaseIncEBP_NumOps[:] = []	
	objs[o].listOP_BaseInc_Module = []
	objs[o].listOP_BaseIncEAX_Module = []
	objs[o].listOP_BaseIncEBX_Module = []
	objs[o].listOP_BaseIncECX_Module = []
	objs[o].listOP_BaseIncEDX_Module = []
	objs[o].listOP_BaseIncEDI_Module = []
	objs[o].listOP_BaseIncESI_Module = []
	objs[o].listOP_BaseIncEBP_Module = []

def clearListBaseInc():
	objs[o].listOP_BaseInc[:] = []
	objs[o].listOP_BaseInc_CNT[:] = []
	objs[o].listOP_BaseInc_NumOps[:] = []
	objs[o].listOP_BaseInc_Module = []
def clearListBaseIncEAX():
	objs[o].listOP_BaseIncEAX[:] = []
	objs[o].listOP_BaseIncEAX_CNT[:] = []
	objs[o].listOP_BaseIncEAX_NumOps[:] = []
	objs[o].listOP_BaseIncEAX_Module = []
def clearListBaseIncEBX():
	objs[o].listOP_BaseIncEBX[:] = []
	objs[o].listOP_BaseIncEBX_CNT[:] = []
	objs[o].listOP_BaseIncEBX_NumOps[:] = []
	objs[o].listOP_BaseIncEBX_Module = []
def clearListBaseIncECX():
	objs[o].listOP_BaseIncECX[:] = []
	objs[o].listOP_BaseIncECX_CNT[:] = []
	objs[o].listOP_BaseIncECX_NumOps[:] = []
	objs[o].listOP_BaseIncECX_Module = []
def clearListBaseIncEDX():
	objs[o].listOP_BaseIncEDX[:] = []
	objs[o].listOP_BaseIncEDX_CNT[:] = []
	objs[o].listOP_BaseIncEDX_NumOps[:] = []
	objs[o].listOP_BaseIncEDX_Module = []
def clearListBaseIncESI():
	objs[o].listOP_BaseIncESI[:] = []
	objs[o].listOP_BaseIncESI_CNT[:] = []
	objs[o].listOP_BaseIncESI_NumOps[:] = []
	objs[o].listOP_BaseIncESI_Module = []
def clearListBaseIncEDI():
	objs[o].listOP_BaseIncEDI[:] = []
	objs[o].listOP_BaseIncEDI_CNT[:] = []
	objs[o].listOP_BaseIncEDI_NumOps[:] = []
	objs[o].listOP_BaseIncEDI_Module = []
def clearListBaseIncESP():
	objs[o].listOP_BaseIncESP[:] = []
	objs[o].listOP_BaseIncESP_CNT[:] = []
	objs[o].listOP_BaseIncESP_NumOps[:] = []
	objs[o].listOP_BaseIncESP_Module = []
def clearListBaseIncEBP():
	objs[o].listOP_BaseIncEBP[:] = []
	objs[o].listOP_BaseIncEBP_CNT[:] = []
	objs[o].listOP_BaseIncEBP_NumOps[:] = []
	objs[o].listOP_BaseIncEBP_Module = []
#Dec
def clearListDecAll():
	objs[o].listOP_BaseDec[:] = []
	objs[o].listOP_BaseDec_CNT[:] = []
	objs[o].listOP_BaseDec_NumOps[:] = []
	objs[o].listOP_BaseDecEAX[:] = []
	objs[o].listOP_BaseDecEAX_CNT[:] = []
	objs[o].listOP_BaseDecEAX_NumOps[:] = []
	objs[o].listOP_BaseDecEBX[:] = []
	objs[o].listOP_BaseDecEBX_CNT[:] = []
	objs[o].listOP_BaseDecEBX_NumOps[:] = []
	objs[o].listOP_BaseDecECX[:] = []
	objs[o].listOP_BaseDecECX_CNT[:] = []
	objs[o].listOP_BaseDecECX_NumOps[:] = []
	objs[o].listOP_BaseDecEDX[:] = []
	objs[o].listOP_BaseDecEDX_CNT[:] = []
	objs[o].listOP_BaseDecEDX_NumOps[:] = []
	objs[o].listOP_BaseDecESI[:] = []
	objs[o].listOP_BaseDecESI_CNT[:] = []
	objs[o].listOP_BaseDecESI_NumOps[:] = []
	objs[o].listOP_BaseDecEDI[:] = []
	objs[o].listOP_BaseDecEDI_CNT[:] = []
	objs[o].listOP_BaseDecEDI_NumOps[:] = []
	objs[o].listOP_BaseDecESP[:] = []
	objs[o].listOP_BaseDecESP_CNT[:] = []
	objs[o].listOP_BaseDecESP_NumOps[:] = []
	objs[o].listOP_BaseDecEBP[:] = []
	objs[o].listOP_BaseDecEBP_CNT[:] = []
	objs[o].listOP_BaseDecEBP_NumOps[:] = []
	objs[o].listOP_BaseDec_Module = []
	objs[o].listOP_BaseDecEAX_Module = []
	objs[o].listOP_BaseDecEBX_Module = []
	objs[o].listOP_BaseDecECX_Module = []
	objs[o].listOP_BaseDecEDX_Module = []
	objs[o].listOP_BaseDecESI_Module = []
	objs[o].listOP_BaseDecEDI_Module = []
	objs[o].listOP_BaseDecEBP_Module = []
def clearListBaseDec():
	objs[o].listOP_BaseDec[:] = []
	objs[o].listOP_BaseDec_CNT[:] = []
	objs[o].listOP_BaseDec_NumOps[:] = []
	objs[o].listOP_BaseDec_Module = []
def clearListBaseDecEAX():
	objs[o].listOP_BaseDecEAX[:] = []
	objs[o].listOP_BaseDecEAX_CNT[:] = []
	objs[o].listOP_BaseDecEAX_NumOps[:] = []
	objs[o].listOP_BaseDecEAX_Module = []
def clearListBaseDecEBX():
	objs[o].listOP_BaseDecEBX[:] = []
	objs[o].listOP_BaseDecEBX_CNT[:] = []
	objs[o].listOP_BaseDecEBX_NumOps[:] = []
	objs[o].listOP_BaseDecEBX_Module = []
def clearListBaseDecECX():
	objs[o].listOP_BaseDecECX[:] = []
	objs[o].listOP_BaseDecECX_CNT[:] = []
	objs[o].listOP_BaseDecECX_NumOps[:] = []
	objs[o].listOP_BaseDecECX_Module = []
def clearListBaseDecEDX():
	objs[o].listOP_BaseDecEDX[:] = []
	objs[o].listOP_BaseDecEDX_CNT[:] = []
	objs[o].listOP_BaseDecEDX_NumOps[:] = []
	objs[o].listOP_BaseDecEDX_Module = []
def clearListBaseDecESI():
	objs[o].listOP_BaseDecESI[:] = []
	objs[o].listOP_BaseDecESI_CNT[:] = []
	objs[o].listOP_BaseDecESI_NumOps[:] = []
	objs[o].listOP_BaseDecESI_Module = []
def clearListBaseDecEDI():
	objs[o].listOP_BaseDecEDI[:] = []
	objs[o].listOP_BaseDecEDI_CNT[:] = []
	objs[o].listOP_BaseDecEDI_NumOps[:] = []
	objs[o].listOP_BaseDecEDI_Module = []
def clearListBaseDecESP():
	objs[o].listOP_BaseDecESP[:] = []
	objs[o].listOP_BaseDecESP_CNT[:] = []
	objs[o].listOP_BaseDecESP_NumOps[:] = []
	objs[o].listOP_BaseDecESP_Module = []
def clearListBaseDecEBP():
	objs[o].listOP_BaseDecEBP[:] = []
	objs[o].listOP_BaseDecEBP_CNT[:] = []
	objs[o].listOP_BaseDecEBP_NumOps[:] = []
	objs[o].listOP_BaseDecEBP_Module = []
#Xchg
def clearListXchgAll():
	objs[o].listOP_BaseXchg[:] = []
	objs[o].listOP_BaseXchg_CNT[:] = []
	objs[o].listOP_BaseXchg_NumOps[:] = []
	objs[o].listOP_BaseXchgEAX[:] = []
	objs[o].listOP_BaseXchgEAX_CNT[:] = []
	objs[o].listOP_BaseXchgEAX_NumOps[:] = []
	objs[o].listOP_BaseXchgEBX[:] = []
	objs[o].listOP_BaseXchgEBX_CNT[:] = []
	objs[o].listOP_BaseXchgEBX_NumOps[:] = []
	objs[o].listOP_BaseXchgECX[:] = []
	objs[o].listOP_BaseXchgECX_CNT[:] = []
	objs[o].listOP_BaseXchgECX_NumOps[:] = []
	objs[o].listOP_BaseXchgEDX[:] = []
	objs[o].listOP_BaseXchgEDX_CNT[:] = []
	objs[o].listOP_BaseXchgEDX_NumOps[:] = []
	objs[o].listOP_BaseXchgESI[:] = []
	objs[o].listOP_BaseXchgESI_CNT[:] = []
	objs[o].listOP_BaseXchgESI_NumOps[:] = []
	objs[o].listOP_BaseXchgEDI[:] = []
	objs[o].listOP_BaseXchgEDI_CNT[:] = []
	objs[o].listOP_BaseXchgEDI_NumOps[:] = []
	objs[o].listOP_BaseXchgESP[:] = []
	objs[o].listOP_BaseXchgESP_CNT[:] = []
	objs[o].listOP_BaseXchgESP_NumOps[:] = []
	objs[o].listOP_BaseXchgEBP[:] = []
	objs[o].listOP_BaseXchgEBP_CNT[:] = []
	objs[o].listOP_BaseXchgEBP_NumOps[:] = []
	objs[o].listOP_BaseXchg_Module = []
	objs[o].listOP_BaseXchgEAX_Module = []
	objs[o].listOP_BaseXchgEBX_Module = []
	objs[o].listOP_BaseXchgECX_Module = []
	objs[o].listOP_BaseXchgEDX_Module = []
	objs[o].listOP_BaseXchgEDI_Module = []
	objs[o].listOP_BaseXchgESI_Module = []
	objs[o].listOP_BaseXchgEBP_Module = []
def clearListBaseXchg():
	objs[o].listOP_BaseXchg[:] = []
	objs[o].listOP_BaseXchg_CNT[:] = []
	objs[o].listOP_BaseXchg_NumOps[:] = []
	objs[o].listOP_BaseXchg_Module = []
def clearListBaseXchgEAX():
	objs[o].listOP_BaseXchgEAX[:] = []
	objs[o].listOP_BaseXchgEAX_CNT[:] = []
	objs[o].listOP_BaseXchgEAX_NumOps[:] = []
	objs[o].listOP_BaseXchgEAX_Module = []
def clearListBaseXchgEBX():
	objs[o].listOP_BaseXchgEBX[:] = []
	objs[o].listOP_BaseXchgEBX_CNT[:] = []
	objs[o].listOP_BaseXchgEBX_NumOps[:] = []
	objs[o].listOP_BaseXchgEBX_Module = []
def clearListBaseXchgECX():
	objs[o].listOP_BaseXchgECX[:] = []
	objs[o].listOP_BaseXchgECX_CNT[:] = []
	objs[o].listOP_BaseXchgECX_NumOps[:] = []
	objs[o].listOP_BaseXchgECX_Module = []
def clearListBaseXchgEDX():
	objs[o].listOP_BaseXchgEDX[:] = []
	objs[o].listOP_BaseXchgEDX_CNT[:] = []
	objs[o].listOP_BaseXchgEDX_NumOps[:] = []
	objs[o].listOP_BaseXchgEDX_Module = []
def clearListBaseXchgESI():
	objs[o].listOP_BaseXchgESI[:] = []
	objs[o].listOP_BaseXchgESI_CNT[:] = []
	objs[o].listOP_BaseXchgESI_NumOps[:] = []
	objs[o].listOP_BaseXchgESI_Module = []
def clearListBaseXchgEDI():
	objs[o].listOP_BaseXchgEDI[:] = []
	objs[o].listOP_BaseXchgEDI_CNT[:] = []
	objs[o].listOP_BaseXchgEDI_NumOps[:] = []
	objs[o].listOP_BaseXchgEDI_Module = []
def clearListBaseXchgESP():
	objs[o].listOP_BaseXchgESP[:] = []
	objs[o].listOP_BaseXchgESP_CNT[:] = []
	objs[o].listOP_BaseXchgESP_NumOps[:] = []
	objs[o].listOP_BaseXchgESP_Module = []
def clearListBaseXchgEBP():
	objs[o].listOP_BaseXchgEBP[:] = []
	objs[o].listOP_BaseXchgEBP_CNT[:] = []
	objs[o].listOP_BaseXchgEBP_NumOps[:] = []
	objs[o].listOP_BaseXchgEBP_Module = []
#LEFT SHIFT
def clearListShiftLeft():
	objs[o].listOP_BaseShiftLeft[:] = []
	objs[o].listOP_BaseShiftLeft_CNT[:] = []
	objs[o].listOP_BaseShiftLeft_NumOps[:] = []
	objs[o].listOP_BaseShiftLeft_Module[:] = []
#RIGHT SHIFT
def clearListShiftRight():
	objs[o].listOP_BaseShiftRight[:] = []
	objs[o].listOP_BaseShiftRight_CNT[:] = []
	objs[o].listOP_BaseShiftRight_NumOps[:] = []
	objs[o].listOP_BaseShiftRight_Module[:] = []
#ROTATE RIGHT
def clearListRotRight():
	objs[o].listOP_BaseRotRight[:] = []
	objs[o].listOP_BaseRotRight_CNT[:] = []
	objs[o].listOP_BaseRotRight_NumOps[:] = []
	objs[o].listOP_BaseRotRight_Module[:] = []
#ROTATE LEFT
def clearListRotLeft():
	objs[o].listOP_BaseRotLeft[:] = []
	objs[o].listOP_BaseRotLeft_CNT[:] = []
	objs[o].listOP_BaseRotLeft_NumOps[:] = []
	objs[o].listOP_BaseRotLeft_Module[:] = []
def clearListSpAll():
	objs[o].SpOutGadgetAll [:] = []
	objs[o].SpOutNumBytesAll [:] = []
	objs[o].SpOutGadgetEAX [:] = []
	objs[o].SpOutNumBytesEAX [:] = []
	objs[o].SpOutGadgetEBX [:] = []
	objs[o].SpOutNumBytesEBX [:] = []
	objs[o].SpOutGadgetECX [:] = []
	objs[o].SpOutNumBytesECX [:] = []
	objs[o].SpOutGadgetEDX [:] = []
	objs[o].SpOutNumBytesEDX [:] = []
	objs[o].SpOutGadgetEDI [:] = []
	objs[o].SpOutNumBytesEDI [:] = []
	objs[o].SpOutGadgetESI [:] = []
	objs[o].SpOutNumBytesESI [:] = []
	objs[o].SpOutGadgetEBP [:] = []
	objs[o].SpOutNumBytesEBP [:] = []
	objs[o].SpOutGadgetESP [:] = []
	objs[o].SpOutNumBytesESP [:] = []
def clearListSpecialPOP():
	objs[o].specialPOPGadget [:] = []
	objs[o].specialPOPBytes [:] = []
	objs[o].specialPOPGadgetBest [:] = []
	objs[o].specialPOPBytesBest [:] = []
	objs[o].specialPOPGadgetBestEAX [:] = []
	objs[o].specialPOPBytesBestEAX [:] = []
	objs[o].specialPOPGadgetBestEBX [:] = []
	objs[o].specialPOPBytesBestEBX [:] = []
	objs[o].specialPOPGadgetBestECX [:] = []
	objs[o].specialPOPBytesBestECX [:] = []
	objs[o].specialPOPGadgetBestEDX [:] = []
	objs[o].specialPOPBytesBestEDX [:] = []
	objs[o].specialPOPGadgetBestEDI [:] = []
	objs[o].specialPOPBytesBestEDI [:] = []
	objs[o].specialPOPGadgetBestESI [:] = []
	objs[o].specialPOPBytesBestESI [:] = []
	objs[o].specialPOPGadgetBestEBP [:] = []
	objs[o].specialPOPBytesBestEBP [:] = []
	objs[o].specialPOPGadgetBestESP [:] = []
	objs[o].specialPOPBytesBestESP [:] = []
	objs[o].specialPOPGadgetEAX [:] = []
	objs[o].specialPOPBytesEAX [:] = []
	objs[o].specialPOPGadgetEBX [:] = []
	objs[o].specialPOPBytesEBX [:] = []
	objs[o].specialPOPGadgetECX [:] = []
	objs[o].specialPOPBytesECX [:] = []
	objs[o].specialPOPGadgetEDX [:] = []
	objs[o].specialPOPBytesEDX [:] = []
	objs[o].specialPOPGadgetEDI [:] = []
	objs[o].specialPOPBytesEDI [:] = []
	objs[o].specialPOPGadgetESI [:] = []
	objs[o].specialPOPBytesESI [:] = []
	objs[o].specialPOPGadgetEBP [:] = []
	objs[o].specialPOPBytesEBP [:] = []
	objs[o].specialPOPGadgetESP [:] = []
	objs[o].specialPOPBytesESP [:] = []

def clearListPopRet():
	objs[o].specialPOPGadgetRetEBX [:] =[]
	objs[o].specialPOPBytesRetEBX [:] =[]
	objs[o].specialPOPGadgetRetBestEBX [:] =[]
	objs[o].specialPOPBytesRetBestEBX [:] =[]
	objs[o].specialPOPGadgetRetECX [:] =[]
	objs[o].specialPOPBytesRetECX [:] =[]
	objs[o].specialPOPGadgetRetBestECX [:] =[]
	objs[o].specialPOPBytesRetBestECX [:] =[]
	objs[o].specialPOPGadgetRetEDX [:] =[]
	objs[o].specialPOPBytesRetEDX [:] =[]
	objs[o].specialPOPGadgetRetBestEDX [:] =[]
	objs[o].specialPOPBytesRetBestEDX [:] =[]
	objs[o].specialPOPGadgetRetEDI [:] =[]
	objs[o].specialPOPBytesRetEDI [:] =[]
	objs[o].specialPOPGadgetRetBestEDI [:] =[]
	objs[o].specialPOPBytesRetBestEDI [:] =[]
	objs[o].specialPOPGadgetRetESI [:] =[]
	objs[o].specialPOPBytesRetESI [:] =[]
	objs[o].specialPOPGadgetRetBestESI [:] =[]
	objs[o].specialPOPBytesRetBestESI [:] =[]
	objs[o].specialPOPGadgetRetESP [:] =[]
	objs[o].specialPOPBytesRetESP [:] =[]
	objs[o].specialPOPGadgetRetBestESP [:] =[]
	objs[o].specialPOPBytesRetBestESP [:] =[]
	objs[o].specialPOPGadgetRetEBP [:] =[]
	objs[o].specialPOPBytesRetEBP [:] =[]
	objs[o].specialPOPGadgetRetBestEBP [:] =[]
	objs[o].specialPOPBytesRetBestEBP [:] =[]
	objs[o].specialPOPGadgetRetEAX [:] =[]
	objs[o].specialPOPBytesRetEAX   [:] =[]
	objs[o].specialPOPGadgetRetBestEAX [:] = []
	objs[o].specialPOPBytesRetBestEAX [:]=[]

	objs[o].specialPOPGadgetRet [:] =[]
	objs[o].specialPOPBytesRet   [:] =[]
	objs[o].specialPOPBytesRetTup [:] =[]
	
def clearListBaseDG_EAX():
	objs[o].listOP_BaseDG_EAX[:] = []
	objs[o].listOP_BaseDG_CNT_EAX[:] = []
	objs[o].listOP_BaseDG_NumOps_EAX[:] = []
	objs[o].listOP_BaseDG_Module_EAX[:] = []
def clearListBaseDG_EBX():
	objs[o].listOP_BaseDG_EBX[:] = []
	objs[o].listOP_BaseDG_CNT_EBX[:] = []
	objs[o].listOP_BaseDG_NumOps_EBX[:] = []
	objs[o].listOP_BaseDG_Module_EBX[:] = []

def clearListBaseDG_ECX():
	objs[o].listOP_BaseDG_ECX[:] = []
	objs[o].listOP_BaseDG_CNT_ECX[:] = []
	objs[o].listOP_BaseDG_NumOps_ECX[:] = []
	objs[o].listOP_BaseDG_Module_ECX[:] = []
def clearListBaseDG_EDX():
	objs[o].listOP_BaseDG_EDX[:] = []
	objs[o].listOP_BaseDG_CNT_EDX[:] = []
	objs[o].listOP_BaseDG_NumOps_EDX[:] = []
	objs[o].listOP_BaseDG_Module_EDX[:] = []
def clearListBaseDG_EDI():
	objs[o].listOP_BaseDG_EDI[:] = []
	objs[o].listOP_BaseDG_CNT_EDI[:] = []
	objs[o].listOP_BaseDG_NumOps_EDI[:] = []
	objs[o].listOP_BaseDG_Module_EDI[:] = []
def clearListBaseDG_ESI():
	objs[o].listOP_BaseDG_ESI[:] = []
	objs[o].listOP_BaseDG_CNT_ESI[:] = []
	objs[o].listOP_BaseDG_NumOps_ESI[:] = []
	objs[o].listOP_BaseDG_Module_ESI[:] = []
def clearListBaseDG_EBP():
	objs[o].listOP_BaseDG_EBP[:] = []
	objs[o].listOP_BaseDG_CNT_EBP[:] = []
	objs[o].listOP_BaseDG_NumOps_EBP[:] = []
	objs[o].listOP_BaseDG_Module_EBP[:] = []
	
def clearListBaseDG_EAX():
	objs[o].listOP_BaseDG_EAX[:] = []
	objs[o].listOP_BaseDG_CNT_EAX[:] = []
	objs[o].listOP_BaseDG_NumOps_EAX[:] = []
	objs[o].listOP_BaseDG_Module_EAX[:] = []
def clearListBaseDG_EBX():
	objs[o].listOP_BaseDG_EBX[:] = []
	objs[o].listOP_BaseDG_CNT_EBX[:] = []
	objs[o].listOP_BaseDG_NumOps_EBX[:] = []
	objs[o].listOP_BaseDG_Module_EBX[:] = []

def clearListBaseDG_ECX():
	objs[o].listOP_BaseDG_ECX[:] = []
	objs[o].listOP_BaseDG_CNT_ECX[:] = []
	objs[o].listOP_BaseDG_NumOps_ECX[:] = []
	objs[o].listOP_BaseDG_Module_ECX[:] = []
def clearListBaseDG_EDX():
	objs[o].listOP_BaseDG_EDX[:] = []
	objs[o].listOP_BaseDG_CNT_EDX[:] = []
	objs[o].listOP_BaseDG_NumOps_EDX[:] = []
	objs[o].listOP_BaseDG_Module_EDX[:] = []
def clearListBaseDG_EDI():
	objs[o].listOP_BaseDG_EDI[:] = []
	objs[o].listOP_BaseDG_CNT_EDI[:] = []
	objs[o].listOP_BaseDG_NumOps_EDI[:] = []
	objs[o].listOP_BaseDG_Module_EDI[:] = []
def clearListBaseDG_ESI():
	objs[o].listOP_BaseDG_ESI[:] = []
	objs[o].listOP_BaseDG_CNT_ESI[:] = []
	objs[o].listOP_BaseDG_NumOps_ESI[:] = []
	objs[o].listOP_BaseDG_Module_ESI[:] = []
def clearListBaseDG_EBP():
	objs[o].listOP_BaseDG_EBP[:] = []
	objs[o].listOP_BaseDG_CNT_EBP[:] = []
	objs[o].listOP_BaseDG_NumOps_EBP[:] = []
	objs[o].listOP_BaseDG_Module_EBP[:] = []
def clearListBaseDG_EAX_Best():
	objs[o].listOP_BaseDG_EAX_Best[:] = []
	objs[o].listOP_BaseDG_CNT_EAX_Best[:] = []
	objs[o].listOP_BaseDG_NumOps_EAX_Best[:] = []
	objs[o].listOP_BaseDG_Module_EAX_Best[:] = []
def clearListBaseDG_EBX_Best():
	objs[o].listOP_BaseDG_EBX_Best[:] = []
	objs[o].listOP_BaseDG_CNT_EBX_Best[:] = []
	objs[o].listOP_BaseDG_NumOps_EBX_Best[:] = []
	objs[o].listOP_BaseDG_Module_EBX_Best[:] = []

def clearListBaseDG_ECX_Best():
	objs[o].listOP_BaseDG_ECX_Best[:] = []
	objs[o].listOP_BaseDG_CNT_ECX_Best[:] = []
	objs[o].listOP_BaseDG_NumOps_ECX_Best[:] = []
	objs[o].listOP_BaseDG_Module_ECX_Best[:] = []
def clearListBaseDG_EDX_Best():
	objs[o].listOP_BaseDG_EDX_Best[:] = []
	objs[o].listOP_BaseDG_CNT_EDX_Best[:] = []
	objs[o].listOP_BaseDG_NumOps_EDX_Best[:] = []
	objs[o].listOP_BaseDG_Module_EDX_Best[:] = []
def clearListBaseDG_EDI_Best():
	objs[o].listOP_BaseDG_EDI_Best[:] = []
	objs[o].listOP_BaseDG_CNT_EDI_Best[:] = []
	objs[o].listOP_BaseDG_NumOps_EDI_Best[:] = []
	objs[o].listOP_BaseDG_Module_EDI_Best[:] = []
def clearListBaseDG_ESI_Best():
	objs[o].listOP_BaseDG_ESI_Best[:] = []
	objs[o].listOP_BaseDG_CNT_ESI_Best[:] = []
	objs[o].listOP_BaseDG_NumOps_ESI_Best[:] = []
	objs[o].listOP_BaseDG_Module_ESI_Best[:] = []
def clearListBaseDG_EBP_Best():
	objs[o].listOP_BaseDG_EBP_Best[:] = []
	objs[o].listOP_BaseDG_CNT_EBP_Best[:] = []
	objs[o].listOP_BaseDG_NumOps_EBP_Best[:] = []
	objs[o].listOP_BaseDG_Module_EBP_Best[:] = []
def clearListBaseDG_EAX_Other():
	objs[o].listOP_BaseDG_EAX_Other[:] = []
	objs[o].listOP_BaseDG_CNT_EAX_Other[:] = []
	objs[o].listOP_BaseDG_NumOps_EAX_Other[:] = []
	objs[o].listOP_BaseDG_Module_EAX_Other[:] = []
def clearListBaseDG_EBX_Other():
	objs[o].listOP_BaseDG_EBX_Other[:] = []
	objs[o].listOP_BaseDG_CNT_EBX_Other[:] = []
	objs[o].listOP_BaseDG_NumOps_EBX_Other[:] = []
	objs[o].listOP_BaseDG_Module_EBX_Other[:] = []
def clearListBaseDG_ECX_Other():
	objs[o].listOP_BaseDG_ECX_Other[:] = []
	objs[o].listOP_BaseDG_CNT_ECX_Other[:] = []
	objs[o].listOP_BaseDG_NumOps_ECX_Other[:] = []
	objs[o].listOP_BaseDG_Module_ECX_Other[:] = []
def clearListBaseDG_EDX_Other():
	objs[o].listOP_BaseDG_EDX_Other[:] = []
	objs[o].listOP_BaseDG_CNT_EDX_Other[:] = []
	objs[o].listOP_BaseDG_NumOps_EDX_Other[:] = []
	objs[o].listOP_BaseDG_Module_EDX_Other[:] = []
def clearListBaseDG_EDI_Other():
	objs[o].listOP_BaseDG_EDI_Other[:] = []
	objs[o].listOP_BaseDG_CNT_EDI_Other[:] = []
	objs[o].listOP_BaseDG_NumOps_EDI_Other[:] = []
	objs[o].listOP_BaseDG_Module_EDI_Other[:] = []
def clearListBaseDG_ESI_Other():
	objs[o].listOP_BaseDG_ESI_Other[:] = []
	objs[o].listOP_BaseDG_CNT_ESI_Other[:] = []
	objs[o].listOP_BaseDG_NumOps_ESI_Other[:] = []
	objs[o].listOP_BaseDG_Module_ESI_Other[:] = []
def clearListBaseDG_EBP_Other():
	objs[o].listOP_BaseDG_EBP_Other[:] = []
	objs[o].listOP_BaseDG_CNT_EBP_Other[:] = []
	objs[o].listOP_BaseDG_NumOps_EBP_Other[:] = []
	objs[o].listOP_BaseDG_Module_EBP_Other[:] = []
def clearListDG_All():
	objs[o].listOP_BaseDG_EAX[:] = []
	objs[o].listOP_BaseDG_CNT_EAX[:] = []
	objs[o].listOP_BaseDG_NumOps_EAX[:] = []
	objs[o].listOP_BaseDG_Module_EAX[:] = []
	objs[o].listOP_BaseDG_EBX[:] = []
	objs[o].listOP_BaseDG_CNT_EBX[:] = []
	objs[o].listOP_BaseDG_NumOps_EBX[:] = []
	objs[o].listOP_BaseDG_Module_EBX[:] = []
	objs[o].listOP_BaseDG_ECX[:] = []
	objs[o].listOP_BaseDG_CNT_ECX[:] = []
	objs[o].listOP_BaseDG_NumOps_ECX[:] = []
	objs[o].listOP_BaseDG_Module_ECX[:] = []
	objs[o].listOP_BaseDG_EDX[:] = []
	objs[o].listOP_BaseDG_CNT_EDX[:] = []
	objs[o].listOP_BaseDG_NumOps_EDX[:] = []
	objs[o].listOP_BaseDG_Module_EDX[:] = []
	objs[o].listOP_BaseDG_EDI[:] = []
	objs[o].listOP_BaseDG_CNT_EDI[:] = []
	objs[o].listOP_BaseDG_NumOps_EDI[:] = []
	objs[o].listOP_BaseDG_Module_EDI[:] = []
	objs[o].listOP_BaseDG_ESI[:] = []
	objs[o].listOP_BaseDG_CNT_ESI[:] = []
	objs[o].listOP_BaseDG_NumOps_ESI[:] = []
	objs[o].listOP_BaseDG_Module_ESI[:] = []
	objs[o].listOP_BaseDG_EBP[:] = []
	objs[o].listOP_BaseDG_CNT_EBP[:] = []
	objs[o].listOP_BaseDG_NumOps_EBP[:] = []
	objs[o].listOP_BaseDG_Module_EBP[:] = []
	objs[o].listOP_BaseDG_EAX[:] = []
	objs[o].listOP_BaseDG_CNT_EAX[:] = []
	objs[o].listOP_BaseDG_NumOps_EAX[:] = []
	objs[o].listOP_BaseDG_Module_EAX[:] = []
	objs[o].listOP_BaseDG_EBX[:] = []
	objs[o].listOP_BaseDG_CNT_EBX[:] = []
	objs[o].listOP_BaseDG_NumOps_EBX[:] = []
	objs[o].listOP_BaseDG_Module_EBX[:] = []
	objs[o].listOP_BaseDG_ECX[:] = []
	objs[o].listOP_BaseDG_CNT_ECX[:] = []
	objs[o].listOP_BaseDG_NumOps_ECX[:] = []
	objs[o].listOP_BaseDG_Module_ECX[:] = []
	objs[o].listOP_BaseDG_EDX[:] = []
	objs[o].listOP_BaseDG_CNT_EDX[:] = []
	objs[o].listOP_BaseDG_NumOps_EDX[:] = []
	objs[o].listOP_BaseDG_Module_EDX[:] = []
	objs[o].listOP_BaseDG_EDI[:] = []
	objs[o].listOP_BaseDG_CNT_EDI[:] = []
	objs[o].listOP_BaseDG_NumOps_EDI[:] = []
	objs[o].listOP_BaseDG_Module_EDI[:] = []
	objs[o].listOP_BaseDG_ESI[:] = []
	objs[o].listOP_BaseDG_CNT_ESI[:] = []
	objs[o].listOP_BaseDG_NumOps_ESI[:] = []
	objs[o].listOP_BaseDG_Module_ESI[:] = []
	objs[o].listOP_BaseDG_EBP[:] = []
	objs[o].listOP_BaseDG_CNT_EBP[:] = []
	objs[o].listOP_BaseDG_NumOps_EBP[:] = []
	objs[o].listOP_BaseDG_Module_EBP[:] = []
	objs[o].listOP_BaseDG_EAX_Best[:] = []
	objs[o].listOP_BaseDG_CNT_EAX_Best[:] = []
	objs[o].listOP_BaseDG_NumOps_EAX_Best[:] = []
	objs[o].listOP_BaseDG_Module_EAX_Best[:] = []
	objs[o].listOP_BaseDG_EBX_Best[:] = []
	objs[o].listOP_BaseDG_CNT_EBX_Best[:] = []
	objs[o].listOP_BaseDG_NumOps_EBX_Best[:] = []
	objs[o].listOP_BaseDG_Module_EBX_Best[:] = []
	objs[o].listOP_BaseDG_ECX_Best[:] = []
	objs[o].listOP_BaseDG_CNT_ECX_Best[:] = []
	objs[o].listOP_BaseDG_NumOps_ECX_Best[:] = []
	objs[o].listOP_BaseDG_Module_ECX_Best[:] = []
	objs[o].listOP_BaseDG_EDX_Best[:] = []
	objs[o].listOP_BaseDG_CNT_EDX_Best[:] = []
	objs[o].listOP_BaseDG_NumOps_EDX_Best[:] = []
	objs[o].listOP_BaseDG_Module_EDX_Best[:] = []
	objs[o].listOP_BaseDG_EDI_Best[:] = []
	objs[o].listOP_BaseDG_CNT_EDI_Best[:] = []
	objs[o].listOP_BaseDG_NumOps_EDI_Best[:] = []
	objs[o].listOP_BaseDG_Module_EDI_Best[:] = []
	objs[o].listOP_BaseDG_ESI_Best[:] = []
	objs[o].listOP_BaseDG_CNT_ESI_Best[:] = []
	objs[o].listOP_BaseDG_NumOps_ESI_Best[:] = []
	objs[o].listOP_BaseDG_Module_ESI_Best[:] = []
	objs[o].listOP_BaseDG_EBP_Best[:] = []
	objs[o].listOP_BaseDG_CNT_EBP_Best[:] = []
	objs[o].listOP_BaseDG_NumOps_EBP_Best[:] = []
	objs[o].listOP_BaseDG_Module_EBP_Best[:] = []
	objs[o].listOP_BaseDG_EAX_Other[:] = []
	objs[o].listOP_BaseDG_CNT_EAX_Other[:] = []
	objs[o].listOP_BaseDG_NumOps_EAX_Other[:] = []
	objs[o].listOP_BaseDG_Module_EAX_Other[:] = []
	objs[o].listOP_BaseDG_EBX_Other[:] = []
	objs[o].listOP_BaseDG_CNT_EBX_Other[:] = []
	objs[o].listOP_BaseDG_NumOps_EBX_Other[:] = []
	objs[o].listOP_BaseDG_Module_EBX_Other[:] = []
	objs[o].listOP_BaseDG_ECX_Other[:] = []
	objs[o].listOP_BaseDG_CNT_ECX_Other[:] = []
	objs[o].listOP_BaseDG_NumOps_ECX_Other[:] = []
	objs[o].listOP_BaseDG_Module_ECX_Other[:] = []
	objs[o].listOP_BaseDG_EDX_Other[:] = []
	objs[o].listOP_BaseDG_CNT_EDX_Other[:] = []
	objs[o].listOP_BaseDG_NumOps_EDX_Other[:] = []
	objs[o].listOP_BaseDG_Module_EDX_Other[:] = []
	objs[o].listOP_BaseDG_EDI_Other[:] = []
	objs[o].listOP_BaseDG_CNT_EDI_Other[:] = []
	objs[o].listOP_BaseDG_NumOps_EDI_Other[:] = []
	objs[o].listOP_BaseDG_Module_EDI_Other[:] = []
	objs[o].listOP_BaseDG_ESI_Other[:] = []
	objs[o].listOP_BaseDG_CNT_ESI_Other[:] = []
	objs[o].listOP_BaseDG_NumOps_ESI_Other[:] = []
	objs[o].listOP_BaseDG_Module_ESI_Other[:] = []
	objs[o].listOP_BaseDG_EBP_Other[:] = []
	objs[o].listOP_BaseDG_CNT_EBP_Other[:] = []
	objs[o].listOP_BaseDG_NumOps_EBP_Other[:] = []
	objs[o].listOP_BaseDG_Module_EBP_Other[:] = []

def clearPopRets():
	global o
	objs[o].listOP_RET_Pop [:]=[]
	objs[o].listOP_RET_Pop_CNT [:]=[]
	objs[o].listOP_RET_Pop_NumOps [:]=[]
	objs[o].listOP_RET_Pop_Module [:]=[]
	objs[o].listOP_RET_Pop_EAX [:]=[]
	objs[o].listOP_RET_Pop_EAX_CNT [:]=[]
	objs[o].listOP_RET_Pop_EAX_NumOps [:]=[]
	objs[o].listOP_RET_Pop_EAX_Module [:]=[]
	objs[o].listOP_RET_Pop_EBX [:]=[]
	objs[o].listOP_RET_Pop_EBX_CNT [:]=[]
	objs[o].listOP_RET_Pop_EBX_NumOps [:]=[]
	objs[o].listOP_RET_Pop_EBX_Module [:]=[]
	objs[o].listOP_RET_Pop_ECX [:]=[]
	objs[o].listOP_RET_Pop_ECX_CNT [:]=[]
	objs[o].listOP_RET_Pop_ECX_NumOps [:]=[]
	objs[o].listOP_RET_Pop_ECX_Module [:]=[]
	objs[o].listOP_RET_Pop_EDX [:]=[]
	objs[o].listOP_RET_Pop_EDX_CNT [:]=[]
	objs[o].listOP_RET_Pop_EDX_NumOps [:]=[]
	objs[o].listOP_RET_Pop_EDX_Module [:]=[]
	objs[o].listOP_RET_Pop_EDI [:]=[]
	objs[o].listOP_RET_Pop_EDI_CNT [:]=[]
	objs[o].listOP_RET_Pop_EDI_NumOps [:]=[]
	objs[o].listOP_RET_Pop_EDI_Module [:]=[]
	objs[o].listOP_RET_Pop_ESI [:]=[]
	objs[o].listOP_RET_Pop_ESI_CNT [:]=[]
	objs[o].listOP_RET_Pop_ESI_NumOps [:]=[]
	objs[o].listOP_RET_Pop_ESI_Module [:]=[]
	objs[o].listOP_RET_Pop_ESP [:]=[]
	objs[o].listOP_RET_Pop_ESP_CNT [:]=[]
	objs[o].listOP_RET_Pop_ESP_NumOps [:]=[]
	objs[o].listOP_RET_Pop_ESP_Module [:]=[]
	objs[o].listOP_RET_Pop_EBP [:]=[]
	objs[o].listOP_RET_Pop_EBP_CNT [:]=[]
	objs[o].listOP_RET_Pop_EBP_NumOps [:]=[]
	objs[o].listOP_RET_Pop_EBP_Module [:]=[]
def clearAllSpecial():
	PE_DLL[:]  = []
	PE_DLLS[:] = []
	PE_DLLS2[:]  = []
	Remove[:]  = []
	DLL_Protect[:]  = []

def clearAll(): #4c
	global o
	global w
	o = 0
	print "Clearing auxillary objects..."
	sp()
	clearAllSpecial()
	for obj in objs:
		clearListPopRet()
		clearListAddAll()
		clearListSubAll()
		clearListMulAll()
		clearListDiv()
		clearListMovAll()
		clearListMovValAll()
		clearListMovShufAll()
		clearListLeaAll()
		clearListPushAll()
		clearListPopAll()
		clearListXchgAll()
		clearListIncAll()
		clearListDecAll()
		clearListShiftLeft()
		clearListShiftRight()
		clearListRotRight()
		clearListRotLeft()
		clearListDG_All()
		clearListStackPivot()
		clearListSpAll()
		clearListSpecialPOP()
		clearPopRets()
		o = o + 1
	o = 0
	print "clearing all complete."
	sp()


def dep():	
   return bool(pe.OPTIONAL_HEADER.DllCharacteristics & 0x0100)
def aslr():
   return bool(pe.OPTIONAL_HEADER.DllCharacteristics & 0x0040)
def seh():
   return bool(pe.OPTIONAL_HEADER.DllCharacteristics & 0x0400)
def CFG():
   return bool(pe.OPTIONAL_HEADER.DllCharacteristics & 0x4000)

def Extraction():
	global entryPoint
	global VirtualAdd
	global ImageBase
	global vSize
	global startAddress
	global endAddy
	global entryPoint
	global data2 
	global PE_Protect
	global o
	global modName
	global peName

#	obj = MyBytes()
#	obj._init_()
#	objs.append(obj)
	modName = peName
	try:
		head, tail = os.path.split(peName)
		modName = tail
	except:
		pass
	PEtemp = PE_path + "/"+ peName
	if skipPath == False:
		pe = pefile.PE(peName)
	if skipPath == True:
		pe = pefile.PE(PEtemp)
	
	#data = pe.get_memory_mapped_image()[entryPoint:entryPoint+vSize]
	#objs[o].data2 = pe.sections[0].get_data()[VirtualAdd:VirtualAdd+vSize]
	#initMods(modName)
	o = 0

	objs[o].entryPoint = pe.OPTIONAL_HEADER.AddressOfEntryPoint
	objs[o].VirtualAdd = pe.sections[0].VirtualAddress
	print pe.sections[0].VirtualAddress
	objs[o].ImageBase = pe.OPTIONAL_HEADER.ImageBase
	objs[o].vSize = pe.sections[0].Misc_VirtualSize
	objs[o].startLoc = objs[o].VirtualAdd + objs[o].ImageBase
	objs[o].endAddy = objs[o].startLoc + objs[o].vSize
	objs[o].endAddy2 = objs[o].startLoc + objs[o].vSize
	tem =0
	#objs[o].data2  = pe.sections[0].get_data()[objs[o].VirtualAdd:objs[o].VirtualAdd+objs[o].vSize]   OLD 722
	objs[o].data2  = pe.sections[0].get_data()[0:]
	global DLL_Protect

	objs[o].protect = str(peName) + "\t"
	objs[o].depStatus = "\tDEP: " + str(dep())
	objs[o].aslrStatus = "\tASLR: " + str(aslr())
	objs[o].sehSTATUS = "\tSAFESEH: " + str(seh())
	objs[o].CFGstatus = "\tCFG: " + str(CFG())
	objs[o].protect = objs[o].protect + objs[o].depStatus + objs[o].aslrStatus + objs[o].sehSTATUS + objs[o].CFGstatus
	DLL_Protect.append(objs[o].protect)
	print objs[o].protect

def Extractionold():

	global PE_Protect
	PEtemp = PE_path + "/"+ peName
	objs[o].pe = pefile.PE(PEtemp)
	pe = pefile.PE(PEtemp)
	#data = pe.get_memory_mapped_image()[entryPoint:entryPoint+vSize]
	#objs[o].data2 = objs[o].pe.sections[0].get_data()[VirtualAdd:VirtualAdd+vSize]
	entryPoint = pe.OPTIONAL_HEADER.addressOfEntryPoint
	objs[o].entryPoint = pe.OPTIONAL_HEADER.addressOfEntryPoint
	objs[o].VirtualAdd = pe.sections[0].Virtualaddress
	objs[o].ImageBase = pe.OPTIONAL_HEADER.ImageBase
	objs[o].vSize = pe.sections[0].Misc_VirtualSize
	objs[o].startLoc = VirtualAdd + ImageBase
	objs[o].endAddy = objs[o].startLoc + objs[o].vSize

	objs[o].entryPoint = pe.OPTIONAL_HEADER.addressOfEntryPoint
	
	#data = pe.get_memory_mapped_image()[entryPoint:entryPoint+vSize]
	objs[o].data2 = objs[o].pe.sections[0].get_data()[VirtualAdd:VirtualAdd+vSize]

	global DLL_Protect

	objs[o].protect = str(peName) + "\t"
	objs[o].depStatus = "\tDEP: " + str(dep())
	objs[o].aslrStatus = "\tASLR: " + str(aslr())
	objs[o].sehSTATUS = "\tSAFESEH: " + str(seh())
	objs[o].CFGstatus = "\tCFG: " + str(CFG())
	objs[o].protect = objs[o].protect + objs[o].depStatus + objs[o].aslrStatus + objs[o].sehSTATUS + objs[o].CFGstatus
	DLL_Protect.append(protect)
	print protect
def extractDLL(dll):
	"print extractdll"
	sp()
	dllName = dll
		# Part of this loadlibrary comes from: https://www.programcreek.com/python/example/53932/ctypes.wintypes.HANDLE
	print dllName
	sp()
	try:
		dllHandle = win32api.LoadLibraryEx(dllName, 0, win32con.LOAD_LIBRARY_AS_DATAFILE)
		windll.kernel32.GetModuleHandleW.restype = wintypes.HMODULE
		windll.kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
		windll.kernel32.GetModuleFileNameW.restype = wintypes.DWORD
		windll.kernel32.GetModuleFileNameW.argtypes = [wintypes.HANDLE, wintypes.LPWSTR, wintypes.DWORD]
		h_module_base = windll.kernel32.GetModuleHandleW(dllName)
		module_path = wintypes.create_unicode_buffer(255)
		windll.kernel32.GetModuleFileNameW(h_module_base, module_path, 255)
		objs[o].e = pefile.PE(module_path.value)
		win32api.FreeLibrary(dllHandle)
		
		objs[o].protect = str(dllName) + "\t"
		objs[o].depStatus = "\tDEP: " + str(dep())
		objs[o].aslrStatus = "\tASLR: " + str(aslr())
		objs[o].sehSTATUS = "\tSAFESEH: " + str(seh())
		objs[o].CFGstatus = "\tCFG: " + str(CFG())
		objs[o].protect = objs[o].protect + objs[o].depStatus + objs[o].aslrStatus + objs[o].sehSTATUS + objs[o].CFGstatus
		DLL_Protect.append(objs[o].protect)
		protect = objs[o].protect
		print module_path.value
		print protect
	except:
		print dllName + " could not be located. Please search for this manually if needed."
		sp()
		pass
def getProtectStatus(dll):
	global o
	print "extractdll"
	sp()
	dllName = dll
		# Part of this loadlibrary comes from: https://www.programcreek.com/python/example/53932/ctypes.wintypes.HANDLE
	print dllName
	sp()
	try:
		objs[o].protect = str(dllName) + "\t"
		objs[o].depStatus = "\tDEP: " + str(dep())
		objs[o].aslrStatus = "\tASLR: " + str(aslr())
		objs[o].sehSTATUS = "\tSAFESEH: " + str(seh())
		objs[o].CFGstatus = "\tCFG: " + str(CFG())
		#objs[o].protect = objs[o].protect + objs[o].depStatus + objs[o].aslrStatus + objs[o].sehSTATUS + objs[o].CFGstatus
		#DLL_Protect.append(objs[o].protect)
		#protect = objs[o].protect
		#print module_path.value
		#print protect
	except:
		print "Protect status: " + dllName + " could not be be registered and is skipped."
		sp()
		pass

def extractDLL_Min(dll):
	print "extracting enter"
	sp()
	global pe
	global modName
	global o
	#print "o val" + str(o)
	dllName = dll
	modName = dll
#	#print "\n\n-name"
	print dllName
	sp()
	obj = MyBytes()
	obj._init_()
	objs.append(obj)
	#o = o + 1

	print "o = " + str(o)
	sp()
	
		# Part of this loadlibrary comes from: https://www.programcreek.com/python/example/53932/ctypes.wintypes.HANDLE
	dllHandle = win32api.LoadLibraryEx(dllName, 0, win32con.LOAD_LIBRARY_AS_DATAFILE)
	windll.kernel32.GetModuleHandleW.restype = wintypes.HMODULE
	windll.kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
	windll.kernel32.GetModuleFileNameW.restype = wintypes.DWORD
	windll.kernel32.GetModuleFileNameW.argtypes = [wintypes.HANDLE, wintypes.LPWSTR, wintypes.DWORD]
	h_module_base = windll.kernel32.GetModuleHandleW(dllName)
	module_path = wintypes.create_unicode_buffer(255)
	windll.kernel32.GetModuleFileNameW(h_module_base, module_path, 255)
	pe = pefile.PE(module_path.value)
	win32api.FreeLibrary(dllHandle)
 
	global PE_Protect
	print module_path.value
	print "  "
	print dllName
	#print ""#"in extractdllMin"
	#print "o " + str(o)
	sp()
	#data = pe.get_memory_mapped_image()[entryPoint:entryPoint+vSize]
	#objs[o].data2 = objs[o].pe.sections[0].get_data()[VirtualAdd:VirtualAdd+vSize]
	objs[o].entryPoint = pe.OPTIONAL_HEADER.AddressOfEntryPoint
	print "\tEntryPoint\t" + str(hex(objs[o].entryPoint))
	objs[o].VirtualAdd = pe.sections[0].VirtualAddress
	#print "Virtual Address\t" + str(hex(objs[o].VirtualAdd))
	objs[o].ImageBase = pe.OPTIONAL_HEADER.ImageBase
	print "\tImagebase\t\t" + str(hex(objs[o].ImageBase ))
	objs[o].vSize = pe.sections[0].Misc_VirtualSize
	print "\tVirtual Size\t\t" + str(hex(objs[o].vSize))
	objs[o].startLoc = objs[o].VirtualAdd + objs[o].ImageBase
	objs[o].endAddy = objs[o].startLoc + objs[o].vSize
 
	#data = pe.get_memory_mapped_image()[entryPoint:entryPoint+vSize]
	objs[o].data2  = pe.sections[0].get_data()[objs[o].VirtualAdd:objs[o].VirtualAdd+objs[o].vSize]

	print "Done extracting"
	sp()
def extractDLL_MinNew(dll):
	print "NEW: extracting enter"
	sp()
	global pe
	global modName
	global o
	global index
	#print "o val" + str(o)
	dllName = dll
	modName = dll
#	#print "\n\n-name"
	print dllName
	sp()
	obj = MyBytes()
	obj._init_()
	objs.append(obj)
	#o = o + 1
	print "o = " + str(o)
	sp()
	#initMods(dll)
	newpath = extractDLLNew(dll)
	print newpath
	sp()
 	pe = pefile.PE(newpath)
	global PE_Protect
	objs[o].entryPoint = pe.OPTIONAL_HEADER.AddressOfEntryPoint
	print "\tEntryPoint:\t" + str(hex(objs[o].entryPoint))
	objs[o].VirtualAdd = pe.sections[0].VirtualAddress
	#print "objs[o].VirtualAdd:\t" + str(hex(objs[o].VirtualAdd))
	objs[o].ImageBase = pe.OPTIONAL_HEADER.ImageBase
	print "\tImagebase:\t\t" + str(hex(objs[o].ImageBase ))
	objs[o].vSize = pe.sections[0].Misc_VirtualSize
	print "\tVirtual size:\t\t" + str(hex(objs[o].vSize))
	objs[o].startLoc = objs[o].VirtualAdd + objs[o].ImageBase
	#print "objs[o].startLoc:\t" + str(hex(objs[o].startLoc))
	objs[o].endAddy = objs[o].startLoc + objs[o].vSize
	#print "objs[o].endAddy:\t\t" + str(hex(objs[o].endAddy))
 
	#data = pe.get_memory_mapped_image()[entryPoint:entryPoint+vSize]
	objs[o].data2  = pe.sections[0].get_data()[objs[o].VirtualAdd:objs[o].VirtualAdd+objs[o].vSize]

	print "extracting end"
	sp()
def show1(int):
		show = "{0:02x}".format(int) #
		return show

def showProtectStatus():
	print "Mitigations for " + str(peName) + "\n"
	
	for i in  DLL_Protect:
		print i

	
	
def setHowDeep():
	global Depth
	print "what should be the depth for dispatcher gadgets?\n"
	sp()
	vt = raw_input()
	Depth = vt
	print "Current depth value is now at " + str(Depth) + ".\n"
	sp()

def setHashCheck():
	global hashCheckVal
	print "what should be the hash check value?\n"
	sp()
	vt = raw_input()
	hashCheckVal = vt
	print "Current depth value is now at " + str(hashCheckVal) + ".\n"
	sp()


def setImageBase():
	global ImageBase
	global o
	print "What should the new image base be?\n"
	sp()
	vt = raw_input()
	objs[0].ImageBase = vt
	print "Current image base value is now at " + str(objs[0].ImageBase) + ".\n"
	sp()	
def disHereJmp(address, NumOpsDis, Reg):
	global o
	w=0
	## Capstone does not seem to allow me to start disassemblying at a given point, so I copy out a chunk to  disassemble. I append a 0x00 because it does not always disassemble correctly (or at all) if just two bytes. I cause it not to be displayed through other means. It simply take the starting address of the jmp [reg], disassembles backwards, and copies it to a variable that I examine more closely.
	lGoBack = linesGoBackFindOP

	CODED2 = b""

	x = NumOpsDis
	for i in range (x, 0, -1):
		CODED2 += objs[o].data2[address-i]
	CODED2 += objs[o].data2[address]
	CODED2 += objs[o].data2[address+1]
	CODED2 += b"\x00"

	# I create the individual lines of code that will appear>
	val =""
	val2 = []
	val3 = []
	address2 = address + objs[o].startLoc + 1000
	val5 =[]
	


	for i in cs.disasm(CODED2, address-x):
		add = hex(int(i.address))
		addb = hex(int(i.address +  objs[o].VirtualAdd))
		add2 = str(add)
		add3 = hex (int(i.address + objs[o].startLoc	))
		add4 = str(add3)
		val =  i.mnemonic + " " + i.op_str + "\t\t\t\t"  + add4 + " (offset " + addb + ")\n"
		val2.append(val)
		val3.append(add2)
		val5.append(val)
		#print val

# My method is to to detect if there is a ret, jmp or call in the gadget. If I find it, I cut out the offending lines and any leading up to it, leaving only safe gadgets that terminate in a jmp or call. The solution is a reversed for loop with enum and checking to see if jmp or call appears before the end of the gadget. If I do, I excise that line and all above it.  when I intially locate a desired sequence, e.g. jmp eax, I then capture the lines immediately before it. This is a way to ensure  that instructions petaining to control flow are not in the gadget.

	tz = val2.__len__()
	tk=0
	save=0x00
	# I need to iterate through this in reverse, starting with the jmp [reg].  I contains index number and e is to enumerate, i.e. show what the value is. In this case, it is iterating through an array of  strings containing the disasembly. The goal is ultimately to cut this down by removing other control flow instructions. The end result will be I will know the address of the jmp [reg] and how many lines  to go back without encountering a control flow instruction.
	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__() 
		if tk < 1:
			save = val3[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1

		# Use regular expressions to find lines that have control flow and other undesired instructions, so they and preceding lines can be excised. 
		# matchObj2 = re.compile( r"\bjo\b|\bjno\b|\bjsn\b|\bjs\b|\bje\b|\bjz\b|\bjne\b|\bjnz\b|\bjb\b|\bjnae\b|\bjc\b|\bjnb\bjae\b|\bjnc\b|\bjbe\bjna\b|\bja\b|\bjnben\b|\bjl\b|\bjnge\b|\bjge\bjnl\b|\bjle\b|\bjng\bjg\b|\bjnle\b|\bjp\b|\bjpe\b|\bjnp\b|\bjpo\bjczz\b|\bjecxz\b|\bcall\b|\bint\b|\bdb\b", re.M|re.I)
		# if re.findall(matchObj2, e):   #if "ret"  in e:
		# 	if i != 1:
		# 		if i > val2.__len__():
		# 			break  # Gracefully break on unusual cases
		# 		else:
		# 			try: 
		# 				del val2[i]
		# 				del val3[i]
		# 			except IndexError:
		# 				pass
		# 		i = i-1
		# 		while i <= (val2.__len__()):
		# 			if i <0:
		# 				break
		# 			else:
		# 				del val2[i]	
		# 				del val3[i]
		# 				i=i-1
		# 				if i == (val2.__len__()-1):
		# 					break
	tz = val2.__len__()
	tk=0
	save=0
	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = val3[i]   # This allows me to save the initial  address of the target jmp [reg] address.
			saveq = int(save, 16)
		tk += 1
# Here I search for excise ret's from JOP gadget. I had tried to incorporate this functionality into the
# above, but I would run into test cases that would cause errors. This seemed the best solution, even if
# inelegant.
		# matchObj2 = re.compile( r"\bret\b", re.M|re.I)
		# if re.findall(matchObj2, e):   #if "ret"  in e:
		# 	if i != 0:
		# 		if i > val2.__len__():
		# 			break  # Gracefully break on unusual cases
		# 		else:
		# 			try: 
		# 				del val2[i]
		# 				del val3[i]
		# 			except IndexError:
		# 				pass
		# 		i = i-1
		# 		while i <= (val2.__len__()):
		# 			if i <0:
		# 				break
		# 			else:
		# 				del val2[i]	
		# 				del val3[i]
		# 				i=i-1
		# 				if i == (val2.__len__()-1):
		# 					break

	matchObj = re.match( r'jmp [e]+', val, re.M|re.I)
	if matchObj:
		if save != 0:
			if val2.__len__() > 1:
				if val2.__len__() == 2:
					matchObj = re.match( r'\bnop\b|\bleave\b|\bcall\b|\bret\b|\bjmp\b|\bljmp\b|\bretf\b|\bhlt\b', val2[i-2], re.M|re.I)
					if matchObj:
						counter()
					else:
						save = int(save, 16)
						addListBase(save, val2.__len__(), NumOpsDis, modName) # fist parameter: address of target jmp [reg]; second parameter: number of lines to go back. third parameter: number of ops to go back.
	
				else:
					matchObj = re.match( r'\bnop\b|\bleave\b|\bcall\b|\bret\b|\bjmp\b|\bljmp\b|\bjo\b|\bjno\b|\bjsn\b|\bjs\b|\bje\b|\bjz\b|\bjne\b|\bjnz\b|\bjb\b|\bjnae\b|\bjc\b|\bjnb\bjae\b|\bjnc\b|\bjbe\bjna\b|\bja\b|\bjnben\b|\bjl\b|\bjnge\b|\bjge\bjnl\b|\bjle\b|\bjng\bjg\b|\bjnle\b|\bjp\b|\bjpe\b|\bjnp\b|\bjpo\bjczz\b|\bjecxz\b|\bcall\b|\bint\b|\bdb\b|\bretf\b|\bhltf\b|\bret\b', val2[i-2], re.M|re.I)
					if not matchObj:
						save = int(save, 16)
						addListBase(save, val2.__len__(), NumOpsDis, modName) # fist parameter: address of target jmp [reg]; second parameter: number of lines to go back. third parameter: number of ops to go back.
						while lGoBack > 1:
							try:
								matchObj = re.match( r'\badd\b|\badc\b', val2[i-lGoBack], re.M|re.I)
								if matchObj: 
									matchObj = re.match( r'^[add|adc]+ [byte|dword]+ ptr+ \[e[abcds]+[px]+ [+|-]+ 0x|^add [byte|dword]+ ptr+ \[e[abcds][px] \+ 0x|^add e[abcds][px], [dword|byte]+ ptr \[e[abcds][xp] \+ 0x|^add [byte|dword]+ ptr \[eax\], [al|eax]|^add [byte|dword]+ ptr \[ebx\], [bl|bx]|^add [byte|dword]+ ptr \[ecx\], [cl|ecx]|^add [byte|dword]+ ptr \[edx\], [dl|edx]|^[add|adc]+ eax, [dword|byte]+ ptr \[[e|a]+[a|l]+|^[add|adc]+ ebx, [dword|byte]+ ptr \[[e|b]+[b|l]+|^[add|adc]+ ecx, [dword|byte]+ ptr \[[e|c]+[c|l]+|^[add|adc]+ edx, [dword|byte]+ ptr \[[e|d]+[d|l]+|^[add|adc]+ edi, [dword|byte]+ ptr \[[e|d]+[d|i]+|^[add|adc]+ esi, [dword|byte]+ ptr \[[e|s]+[s|i]+|^[add|adc]+ ebp, [dword|byte]+ ptr \[[e|b]+[b|p]+|^[add|adc]+ esp, [dword|byte]+ ptr \[[e|s]+[s|p]+|^[add|adc]+ a[l|h]+, a[l|h]+|^[add|adc]+ b[l|h]+, b[l|h]+|^[add|adc]+ c[l|h]+, c[l|h]+|^[add|adc]+ d[l|h]+, d[l|h]+|^[add|adc]+ di, di|^[add|adc]+ si, si|^[add|adc]+ sp, sp|^[add|adc]+ bp, bp', val2[i-lGoBack], re.M|re.I)   
									# I am using regular expressions to eliminate what would be garbage gadgets, of which there would be countless, off the wall, unintended instructions that would do nothing of any practical value.
									if not matchObj:
										y = val2[i-lGoBack]
										if (y == val2[i-lGoBack]):
											numLines= giveLineNum(val5,y)
											y =stupidPre(val5, numLines)
											if y == True:
												addListBaseAdd(saveq, numLines, NumOpsDis, modName)

										#print "ADDDING************************************\n\n"
										#eax - saving add to specific registers -- far more useful.
										matchObj1 = re.match( r'^[add|adc]+ [dword|byte]* [ptr]* [\[]*[e]*a[x|l|h]+|[add|adc]+ [e]*a[x|l|h]+ ', val2[i-lGoBack], re.M|re.I)
										if matchObj1:
											# print "***************"
											# print "b: " + val2[i-lGoBack]
											y = val2[i-lGoBack]
											# print "y:" + y
											# addListRETPopEDI(saveq, giveLineNum(val5,y), NumOpsDis, modName)
											# print "popedi:"
											# print "all:"
											# print binaryToStr(CODED2)
											# print "i: " + str(i) + " lGoBack: " + str(lGoBack) +  " i-lGoBack: " + str(i-lGoBack)	
											# print "answer: " + str(giveLineNum(val5,val2[i-lGoBack]))
										
											# for x in val2:
											# 	print x
											# print "i-lGoBack: " + str(i-lGoBack)
											# print "a: " + val2[i-lGoBack]
											# if (y != val2[i-lGoBack]):
											# 	print "weird: " + y
											# 	print "  was: " +  val2[i-lGoBack]
											if (y == val2[i-lGoBack]):
											# 	print "REAL"
												# modName2 = Ct()


												numLines= giveLineNum(val5,y)
												y =stupidPreJ(val5, numLines)
												if y == True:
													# print "enter true"
													addListBaseAddEAX(saveq, numLines, NumOpsDis, modName)
													# print Ct()
													counter()

											# print val3[i-lGoBack]
											
											# print "lgoback: (below)"
											# print val2[lGoBack]
											# print val3[lGoBack]
											# print "answer: " + str(giveLineNum(val2))

											# numLines= giveLineNum(val5,val2[i-lGoBack])
											# z =stupidPreJ(val5, numLines)
											# if z == True:
											# 	addListBaseAddEAX(saveq, numLines, NumOpsDis, modName)
											# addListBaseAddEAX(save, lGoBack, NumOpsDis, modName)
										#	print "ADDDING************************************\n\n"
										
										#ebx
										matchObj1 = re.match( r'^[add|adc]+ [dword|byte]* [ptr]* [\[]*[e]*b[x|l|h]+|[add|adc]+ [e]*b[x|l|h]+', val2[i-lGoBack], re.M|re.I)

										
										if matchObj1:
											# print "***********************************************"
											# print "1ebx"
											# print "b: " + val2[i-lGoBack]
											y = val2[i-lGoBack]
											# print "y:" + y
											# # addListRETPopEDI(saveq, giveLineNum(val5,y), NumOpsDis, modName)
											# print "saveebx:"
											# print "all:"
											# print binaryToStr(CODED2)
											# print "i: " + str(i) + " lGoBack: " + str(lGoBack) +  " i-lGoBack: " + str(i-lGoBack)	
											# # print "answer: " + str(giveLineNum(val5,val2[i-lGoBack]))
										
											# for x in val2:
											# 	print x
											# print "i-lGoBack: " + str(i-lGoBack)
											# print "a: " + val2[i-lGoBack]
											# if (y != val2[i-lGoBack]):
											# 	print "weird: " + y
											# 	print "  was: " +  val2[i-lGoBack]
											if (y == val2[i-lGoBack]):
											# # 	print "REAL"
											# 	modName2 = Ct()

												
												# modName2= Ct()
												numLines= giveLineNum(val5,y)
												y =stupidPreJ(val5, numLines)
												if y == True:
													# print "savingebx"
													addListBaseAddEBX(saveq, numLines, NumOpsDis, modName)
													# print Ct()
													# counter()
											# print "***********************************************"


											# numLines= giveLineNum(val5,val2[i-lGoBack])
											# z =stupidPre(val5, numLines)
											# if z == True:
											# 	print "saveebx"
											# 	addListBaseAddEBX(saveq, numLines, NumOpsDis, modName)

											# addListBaseAddEBX(save, lGoBack, NumOpsDis, modName)
										#ecx
										matchObj = re.match( r'^[add|adc]+ [dword|byte]* [ptr]* [\[]*[e]*c[x|l|h]+|[add|adc]+ [e]*c[x|l|h]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												# print "saveecx"
												addListBaseAddECX(saveq, numLines, NumOpsDis, modName)

											# addListBaseAddECX(save, lGoBack, NumOpsDis, modName)
										#eDx
										matchObj = re.match( r'^[add|adc]+ [dword|byte]* [ptr]* [\[]*[e]*d[x|l|h]+|[add|adc]+ [e]*d[x|l|h]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												# print "saveedx"
												addListBaseAddEDX(saveq, numLines, NumOpsDis, modName)

											# addListBaseAddEDX(save, lGoBack, NumOpsDis, modName)
										#ESI 
										matchObj = re.match( r'^[add|adc]+ [dword|byte]* [ptr]* [\[]*[e]*si|[add|adc]+ [e]*si', val2[i-lGoBack], re.M|re.I)
										if matchObj:

											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												# print "saveesi"
												addListBaseAddESI(saveq, numLines, NumOpsDis, modName)
											# addListBaseAddESI(save, lGoBack, NumOpsDis, modName)
										#EDI 
										matchObj = re.match( r'^[add|adc]+ [dword|byte]* [ptr]* [\[]*[e]*di|[add|adc]+ [e]*di', val2[i-lGoBack], re.M|re.I)
										if matchObj:

											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												# print "saveedi"
												addListBaseAddEDI(saveq, numLines, NumOpsDis, modName)
											# addListBaseAddEDI(save, lGoBack, NumOpsDis, modName)
										#esp
										matchObj = re.match( r'^[add|adc]+ [dword|byte]* [ptr]* [\[]*[e]*sp|[add|adc]+ [e]*sp', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												# print "saveesp"
												addListBaseAddESP(saveq, numLines, NumOpsDis, modName)

											# addListBaseAddESP(save, lGoBack, NumOpsDis, modName)
										#EBP
										matchObj = re.match( r'^[add|adc]+ [dword|byte]* [ptr]* [\[]*[e]*bp|[add|adc]+ [e]*bp', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												# print "saveebp"
												addListBaseAddEBP(saveq, numLines, NumOpsDis, modName)

											# addListBaseAddEBP(save, lGoBack, NumOpsDis, modName)
							except IndexError:
								pass

							#Searching for Sub operations
							try:
								matchObj = re.match( r'\bsub\b|\bsbb\b', val2[i-lGoBack], re.M|re.I)
								if matchObj: 
									#print "**sub**"
									#print val2[i-lGoBack]
									matchObj = re.match( r'^[sub|sbb]+ [byte|dword]+ ptr+ \[e[abcds]+[px]+ [+|-]+ 0x|^[sub|sbb]+ [byte|dword]+ ptr+ \[e[abcds][px] \+ 0x|^[sub|sbb]+ e[abcds][px], [dword|byte]+ ptr \[e[abcds][xp] \+ 0x|^[sub|sbb]+ [byte|dword]+ ptr \[eax\], [al|eax]+|^[sub|sbb]+ [byte|dword]+ ptr \[ebx\], [bl|bx]+|^[sub|sbb]+ [byte|dword]+ ptr \[ecx\], [cl|ecx]+|^[sub|sbb]+ [byte|dword]+ ptr \[edx\], [dl|edx]+|^[sub|sbb]+ eax, [dword|byte]+ ptr \[[e|a]+[a|l]+|^[sub|sbb]+ ebx, [dword|byte]+ ptr \[[e|b]+[b|l]+|^[sub|sbb]+ ecx, [dword|byte]+ ptr \[[e|c]+[c|l]+|^[sub|sbb]+ edx, [dword|byte]+ ptr \[[e|d]+[d|l]+|^[sub|sbb]+ edi, [dword|byte]+ ptr \[[e|d]+[d|i]+|^[sub|sbb]+ esi, [dword|byte]+ ptr \[[e|s]+[s|i]+|^[sub|sbb]+ ebp, [dword|byte]+ ptr \[[e|b]+[b|p]+|^[sub|sbb]+ esp, [dword|byte]+ ptr \[[e|s]+[s|p]+|^[sub|sbb]+ a[l|h]+, a[l|h]+|^[sub|sbb]+ b[l|h]+, b[l|h]+|^[sub|sbb]+ c[l|h]+, c[l|h]+|^[sub|sbb]+ d[l|h]+, d[l|h]+|^[sub|sbb]+ di, di|^[sub|sbb]+ si, si|^[sub|sbb]+ sp, sp|^[sub|sbb]+ bp, bp', val2[i-lGoBack], re.M|re.I)  
									if not matchObj:
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListBaseSub(saveq, numLines, NumOpsDis, modName)
										# addListBaseSub(save, lGoBack, NumOpsDis, modName) 
										#eax - saving add to specific registers -- far more useful.
										matchObj = re.match( r'^[sub|sbb]+ [dword|byte]* [ptr]* [\[]*[e]*a[x|l|h]*|[sub|sbb]+ [e]*a[x|l|h]', val2[i-lGoBack], re.M|re.I)
										if matchObj:										
											numLines= giveLineNum(val5,val2[i-lGoBack])				
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseSubEAX(saveq, numLines, NumOpsDis, modName)
											# addListBaseSubEAX(save, lGoBack, NumOpsDis, modName)
										
										#ebx
										matchObj = re.match( r'^[sub|sbb]+ [dword|byte]* [ptr]* [\[]*[e]*b[x|l|h]*|[sub|sbb]+ [e]*b[x|l|h]*', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseSubEBX(saveq, numLines, NumOpsDis, modName)
											# addListBaseSubEBX(save, lGoBack, NumOpsDis, modName)
										#ecx
										matchObj = re.match( r'^[sub|sbb]+ [dword|byte]* [ptr]* [\[]*[e]*c[x|l|h]*|[sub|sbb]+ [e]*c[x|l|h]*', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseSubECX(saveq, numLines, NumOpsDis, modName)
											# addListBaseSubECX(save, lGoBack, NumOpsDis, modName)
										#eDx
										matchObj = re.match( r'^[sub|sbb]+ [dword|byte]* [ptr]* [\[]*[e]*d[x|l|h]*|[sub|sbb]+ [e]*d[x|l|h]*', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseSubEDX(saveq, numLines, NumOpsDis, modName)
											# addListBaseSubEDX(save, lGoBack, NumOpsDis, modName)
										#ESI 
										matchObj = re.match( r'^[sub|sbb]+ [dword|byte]* [ptr]* [\[]*[e]*si|[sub|sbb]+ [e]*si', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseSubESI(saveq, numLines, NumOpsDis, modName)
											# addListBaseSubESI(save, lGoBack, NumOpsDis, modName)
										#EDI 
										matchObj = re.match( r'^[sub|sbb]+ [dword|byte]* [ptr]* [\[]*[e]*di|[sub|sbb]+ [e]*di', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseSubEDI(saveq, numLines, NumOpsDis, modName)
											# addListBaseSubEDI(save, lGoBack, NumOpsDis, modName)
										#esp
										matchObj = re.match( r'^[sub|sbb]+ [dword|byte]* [ptr]* [\[]*[e]*sp|[sub|sbb]+ [e]*sp', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseSubESP(saveq, numLines, NumOpsDis, modName)
											# addListBaseSubESP(save, lGoBack, NumOpsDis, modName)
										#EBP
										matchObj = re.match( r'^[sub|sbb]+ [dword|byte]* [ptr]* [\[]*[e]*bp|[sub|sbb]+ [e]*bp', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseSubEBP(saveq, numLines, NumOpsDis, modName)											
											# addListBaseSubEBP(save, lGoBack, NumOpsDis, modName)
							except IndexError:
								pass
							#Searching for Mul operations
							#Some of the imul instructions I do not think would be very typical for a normal program, but feasible as uninteded instructions.
							try: 
								matchObj = re.match( r'\bmul\b|\bmulb\b|\bmulw\b|\bmull\b|\bmulwl\b|\bmulbwl\b|\bimul\b|\bimulb\b|\bimulw\b|\bimull\b|\bimulwl\b|\bimulbwl\b', val2[i-lGoBack], re.M|re.I)
							
								if matchObj: 
									matchObj = re.match( r'^[mul|imul]+ [e]*ax, [e]*ax|^[mul|imul]+ [e]*bx, [e]*bx|^[mul|imul]+ [e]*cx, [e]*cx|^[mul|imul]+ [e]*dx, [e]*dx|^[mul|imul]+ [e]*di, [e]*di|^[mul|imul]+ [e]*si, [e]*si|^[mul|imul]+ [e]*bp, [e]*bp|^[mul|imul]+ [e]*sp, [e]*sp', val2[i-lGoBack], re.M|re.I)
									if not matchObj:

										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListBaseMul(saveq, numLines, NumOpsDis, modName)


										#eax - saving add to specific registers -- far more useful.
										matchObj = re.match( r'^mul', val2[i-lGoBack], re.M|re.I)  # mul will save in edx : eax or dx: ax by default, so any would work
										if matchObj:
											matchObj = re.match( r'^imul', val2[i-lGoBack], re.M|re.I)
											if not matchObj:

												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "savem"
													addListBaseMulEAX(saveq, numLines, NumOpsDis, modName)
													addListBaseMulEDX(saveq, numLines, NumOpsDis, modName)
												# addListBaseMulEAX(save, lGoBack, NumOpsDis, modName)
												# addListBaseMulEDX(save, lGoBack, NumOpsDis, modName)
										
										matchObj = re.match( r'^imul[b|w|l]* [e]*[abcdsp]+[xbpi]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											matchObj = re.match( r'^imul[b|w|l]* [e]*[abcdsp]+[xbpi]+,', val2[i-lGoBack], re.M|re.I)
											if not matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "savem"
													addListBaseMulEAX(saveq, numLines, NumOpsDis, modName)
													addListBaseMulEDX(saveq, numLines, NumOpsDis, modName)


												# addListBaseMulEAX(save, lGoBack, NumOpsDis, modName)
												# addListBaseMulEDX(save, lGoBack, NumOpsDis, modName)

										matchObj = re.match( r'^imul[b|w|l]* [e]*ax, [e]*[abcdsp]+[xbpi]+, |^imul[b|w|l]* [e]*ax, [dword|byte]+ ptr \[[e]*[abcdsp]+[xbpi]+\], ', val2[i-lGoBack], re.M|re.I)
										if matchObj:

											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												# print "savem"
												addListBaseMulEAX(saveq, numLines, NumOpsDis, modName)
											# addListBaseMulEAX(save, lGoBack, NumOpsDis, modName)

											#two operand form
										matchObj = re.match( r'^imul[b|w|l]* [e]*ax, [e]*[abcdsp]+[xbpi]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											matchObj = re.match( r'^imul[b|w|l]* [e]*ax, [e]*[abcdsp]+[xbpi]+,', val2[i-lGoBack], re.M|re.I)
											if not matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "savem"
													addListBaseMulEAX(saveq, numLines, NumOpsDis, modName)
												# addListBaseMulEAX(save, lGoBack, NumOpsDis, modName)

										#ebx
										matchObj = re.match( r'^imul[b|w|l]* [e]*bx, [e]*[abcdsp]+[xbpi]+, |^imul[b|w|l]* [e]*bx, [dword|byte]+ ptr \[[e]*[abcdsp]+[xbpi]+\], ', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												# print "savem"
												addListBaseMulEBX(saveq, numLines, NumOpsDis, modName)
											# addListBaseMulEBX(save, lGoBack, NumOpsDis, modName)

										#two operand form
										matchObj = re.match( r'^imul[b|w|l]* [e]*bx, [e]*[abcdsp]+[xbpi]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											matchObj = re.match( r'^imul[b|w|l]* [e]*bx, [e]*[abcdsp]+[xbpi]+,', val2[i-lGoBack], re.M|re.I)
											if not matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "savem"
													addListBaseMulEBX(saveq, numLines, NumOpsDis, modName)
												# addListBaseMulEBX(save, lGoBack, NumOpsDis, modName)
										#ecx
										matchObj = re.match( r'^imul[b|w|l]* [e]*cx, [e]*[abcdsp]+[xbpi]+, |^imul[b|w|l]* [e]*cx, [dword|byte]+ ptr \[[e]*[abcdsp]+[xbpi]+\], ', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												# print "savem"
												addListBaseMulECX(saveq, numLines, NumOpsDis, modName)
											# addListBaseMulECX(save, lGoBack, NumOpsDis, modName)

										#two operand form
										matchObj = re.match( r'^imul[b|w|l]* [e]*cx, [e]*[abcdsp]+[xbpi]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											matchObj = re.match( r'^imul[b|w|l]* [e]*cx, [e]*[abcdsp]+[xbpi]+,', val2[i-lGoBack], re.M|re.I)
											if not matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "savem"
													addListBaseMulECX(saveq, numLines, NumOpsDis, modName)
												# addListBaseMulECX(save, lGoBack, NumOpsDis, modName)
										#eDx
										matchObj = re.match( r'^imul[b|w|l]* [e]*dx, [e]*[abcdsp]+[xbpi]+, |^imul[b|w|l]* [e]*dx, [dword|byte]+ ptr \[[e]*[abcdsp]+[xbpi]+\], ', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												# print "savem"
												addListBaseMulEDX(saveq, numLines, NumOpsDis, modName)

											# addListBaseMulEDX(save, lGoBack, NumOpsDis, modName)

										#two operand form
										matchObj = re.match( r'^imul[b|w|l]* [e]*dx, [e]*[abcdsp]+[xbpi]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											matchObj = re.match( r'^imul[b|w|l]* [e]*dx, [e]*[abcdsp]+[xbpi]+,', val2[i-lGoBack], re.M|re.I)
											if not matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "savem"
													addListBaseMulEDX(saveq, numLines, NumOpsDis, modName)
													# addListBaseMulEDX(save, lGoBack, NumOpsDis, modName)

										#ESI 
										matchObj = re.match( r'^imul[b|w|l]* [e]*si, [e]*[abcdsp]+[xbpi]+, |^imul[b|w|l]* [e]*si, [dword|byte]+ ptr \[[e]*[abcdsp]+[xbpi]+\], ', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												# print "savem"
												addListBaseMulESI(saveq, numLines, NumOpsDis, modName)
											# addListBaseMulESI(save, lGoBack, NumOpsDis, modName)

										#two operand form
										matchObj = re.match( r'^imul[b|w|l]* [e]*si, [e]*[abcdsp]+[xbpi]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											matchObj = re.match( r'^imul[b|w|l]* [e]*si, [e]*[abcdsp]+[xbpi]+,', val2[i-lGoBack], re.M|re.I)
											if not matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "savem"
													addListBaseMulESI(saveq, numLines, NumOpsDis, modName)
													# addListBaseMulESI(save, lGoBack, NumOpsDis, modName)

										#EDI 
										matchObj = re.match( r'^imul[b|w|l]* [e]*di, [e]*[abcdsp]+[xbpi]+, |^imul[b|w|l]* [e]*di, [dword|byte]+ ptr \[[e]*[abcdsp]+[xbpi]+\], ', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												# print "savem"
												addListBaseMulEDI(saveq, numLines, NumOpsDis, modName)
											# addListBaseMulEDI(save, lGoBack, NumOpsDis, modName)

										#two operand form
										matchObj = re.match( r'^imul[b|w|l]* [e]*di, [e]*[abcdsp]+[xbpi]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											matchObj = re.match( r'^imul[b|w|l]* [e]*di, [e]*[abcdsp]+[xbpi]+,', val2[i-lGoBack], re.M|re.I)
											if not matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "savem"
													addListBaseMulEDI(saveq, numLines, NumOpsDis, modName)
													# addListBaseMulEDI(save, lGoBack, NumOpsDis, modName)
										
										#esp
										matchObj = re.match( r'^imul[b|w|l]* [e]*sp, [e]*[abcdsp]+[xbpi]+, |^imul[b|w|l]* [e]*sp, [dword|byte]+ ptr \[[e]*[abcdsp]+[xbpi]+\], ', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											#addListBaseMulESP(save, lGoBack, NumOpsDis, modName)
											pass

										#two operand form
										matchObj = re.match( r'^imul[b|w|l]* [e]*sp, [e]*[abcdsp]+[xbpi]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											matchObj = re.match( r'^imul[b|w|l]* [e]*sp, [e]*[abcdsp]+[xbpi]+,', val2[i-lGoBack], re.M|re.I)
											if not matchObj:
												#addListBaseMulESP(save, lGoBack, NumOpsDis, modName)
												pass
										#EBP
										matchObj = re.match( r'^imul[b|w|l]* [e]*bp, [e]*[abcdsp]+[xbpi]+, |^imul[b|w|l]* [e]*bp, [dword|byte]+ ptr \[[e]*[abcdsp]+[xbpi]+\], ', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												# print "savem"
												addListBaseMulEBP(saveq, numLines, NumOpsDis, modName)
											# addListBaseMulEBP(save, lGoBack, NumOpsDis, modName)

										#two operand form
										matchObj = re.match( r'^imul[b|w|l]* [e]*bp, [e]*[abcdsp]+[xbpi]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											matchObj = re.match( r'^imul[b|w|l]* [e]*bp, [e]*[abcdsp]+[xbpi]+,', val2[i-lGoBack], re.M|re.I)
											if not matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "savem"
													addListBaseMulEBP(saveq, numLines, NumOpsDis, modName)
												# addListBaseMulEBP(save, lGoBack, NumOpsDis, modName)
							except IndexError:
								pass

							#####DIV/IDIV


							try: 
								matchObj = re.match( r'\bdiv\b|\bdivb\b|\bdivw\b|\bdivl\b|\bdivwl|\bdivbwl\b|\bidiv\b|\bidivb\b|\bidivw\b|\bidivl\b|\bidivwl|\bidivbwl\b', val2[i-lGoBack], re.M|re.I)
							
								if matchObj: 
									numLines= giveLineNum(val5,val2[i-lGoBack])
									z =stupidPreJ(val5, numLines)
									if z == True:
										# print "saveDiv"
										addListBaseDiv(saveq, numLines, NumOpsDis, modName)
										addListBaseDivEAX(saveq, numLines, NumOpsDis, modName)
										addListBaseDivEDX(saveq, numLines, NumOpsDis, modName)
									# addListBaseDiv(save, lGoBack, NumOpsDis, modName)
									# addListBaseDivEAX(save, lGoBack, NumOpsDis, modName)
									# addListBaseDivEDX(save, lGoBack, NumOpsDis, modName)
							except IndexError:
								pass

							#searching for mov
							try: 
								matchObj = re.match( r'\bmov\b', val2[i-lGoBack], re.M|re.I)
							
								if matchObj: 
									matchObj = re.match( r'^mov [e]*a[x|l|h]+, [dword|byte]+ [ptr]* \[[e]*a[x|l|h]|^mov [e]*b[x|l|h]+, [dword|byte]+ [ptr]* \[[e]*b[x|l|h]*|^mov [e]*c[x|l|h]+, [dword|byte]+ [ptr]* \[[e]*c[x|l|h]*|^mov [e]*d[x|l|h]+, [dword|byte]+ [ptr]* \[[e]*d[x|l|h]*|^mov [e]*di, [dword|byte]+ [ptr]* \[[e]*di|^mov [e]*si, [dword|byte]+ [ptr]* \[[e]*si|^mov [e]*sp, [dword|byte]+ [ptr]* \[[e]*sp|^mov [e]*bp, [dword|byte]+ [ptr]* \[[e]*bp|mov [e]*a[x|l|h]+, [e]*a[x|l|h]+|mov [e]*b[x|l|h]+, [e]*b[x|l|h]+|mov [e]*c[x|l|h]+, [e]*c[x|l|h]+|mov [e]*d[x|l|h]+, [e]*d[x|l|h]+|mov [e]*di, [e]*di|mov [e]*si, [e]*si|mov [e]*bp, [e]*bp+|mov [e]*sp, [e]*sp|^mov [e]*a[x|l|h]+, [dword|byte]+ [ptr]* \[[e]*a[x|l|h] [+|-]+|^mov [dword|byte]+ ptr \[[e]*[abcdspb]+[x|l|h|i|p]+ [+|-]+ |^mov [e]*[abcdspb]+[x|l|h|i|p]+, [dword|byte]+ ptr \[0x|^mov [e]*a[x|l|h]+, [dword|byte]+ [ptr]* \[[e]*a[x|l|h]+ [+|-]+|^mov [e]*[abcdspb]+[x|l|h|i|p]+, es|^mov [e]*[abcdsb]+[x|l|h|p|i]+, [dword|byte]+ [ptr]* \[[e]*[abcdsb]+[x|l|h|p|i]+ [-|+]+ 0x[0-9]*', val2[i-lGoBack], re.M|re.I)
									if not matchObj:
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											# print "savem"
											addListBaseMov(saveq, numLines, NumOpsDis, modName)
										# addListBaseMov(save, lGoBack, NumOpsDis, modName) 
										#eax - saving add to specific registers -- far more useful.
																				
										matchObj = re.match( r'^mov [e]*a[x|l|h]+|^mov [dword|byte]+ ptr \[[e]*a[x|l|h]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												# print "savem"
												addListBaseMovEAX(saveq, numLines, NumOpsDis, modName)
											# addListBaseMovEAX(save, lGoBack, NumOpsDis, modName)
										#ebx
										matchObj = re.match( r'^mov [e]*b[x|l|h]+|^mov [dword|byte]+ ptr \[[e]*b[x|l|h]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												# print "savem"
												addListBaseMovEBX(saveq, numLines, NumOpsDis, modName)
											# addListBaseMovEBX(save, lGoBack, NumOpsDis, modName)
										#ecx
										matchObj = re.match( r'^mov [e]*c[x|l|h]+|^mov [dword|byte]+ ptr \[[e]*c[x|l|h]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												# print "savem"
												addListBaseMovECX(saveq, numLines, NumOpsDis, modName)
											# addListBaseMovECX(save, lGoBack, NumOpsDis, modName)
											
										#eDx
										matchObj = re.match( r'^mov [e]*d[x|l|h]+|^mov [dword|byte]+ ptr \[[e]*d[x|l|h]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												# print "savem"
												addListBaseMovEDX(saveq, numLines, NumOpsDis, modName)
											# addListBaseMovEDX(save, lGoBack, NumOpsDis, modName)

										#ESI 
										matchObj = re.match( r'^mov [e]*si|^mov [dword|byte]+ ptr \[[e]*si', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												# print "savem"
												addListBaseMovESI(saveq, numLines, NumOpsDis, modName)
											# addListBaseMovESI(save, lGoBack, NumOpsDis, modName)
										#EDI 
										matchObj = re.match( r'^mov [e]*di|^mov [dword|byte]+ ptr \[[e]*di', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												# print "savem"
												addListBaseMovEDI(saveq, numLines, NumOpsDis, modName)
											# addListBaseMovEDI(save, lGoBack, NumOpsDis, modName)
										#esp
										matchObj = re.match( r'^mov [e]*sp|^mov [dword|byte]+ ptr \[[e]*sp', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												# print "savem"
												addListBaseMovESP(saveq, numLines, NumOpsDis, modName)
											# addListBaseMovESP(save, lGoBack, NumOpsDis, modName)
										#EBP
										matchObj = re.match( r'^mov [e]*bp|^mov [dword|byte]+ ptr \[[e]*bp', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												# print "savem"
												addListBaseMovEBP(saveq, numLines, NumOpsDis, modName)
											# addListBaseMovEBP(save, lGoBack, NumOpsDis, modName)
							except IndexError:
								pass

							#searching for lea
							try: 
								matchObj = re.match( r'\blea\b', val2[i-lGoBack], re.M|re.I)
							
								if matchObj: 
									matchObj = re.match( r'^lea [e]*a[x|l|h]+, [dword|byte]+ [ptr]* \[[e]*a[x|l|h]*|^lea [e]*b[x|l|h]+, [dword|byte]+ [ptr]* \[[e]*b[x|l|h]*|^lea [e]*c[x|l|h]+, [dword|byte]+ [ptr]* \[[e]*c[x|l|h]*|^lea [e]*d[x|l|h]+, [dword|byte]+ [ptr]* \[[e]*d[x|l|h]*|^lea [e]*di, [dword|byte]+ [ptr]* \[[e]*di|^lea [e]*si, [dword|byte]+ [ptr]* \[[e]*si|^lea [e]*sp, [dword|byte]+ [ptr]* \[[e]*sp|^lea [e]*bp, [dword|byte]+ [ptr]* \[[e]*bp|lea [e]*a[x|l|h]+, [e]*a[x|l|h]+|lea [e]*b[x|l|h]+, [e]*b[x|l|h]+|lea [e]*c[x|l|h]+, [e]*c[x|l|h]+|lea [e]*d[x|l|h]+, [e]*d[x|l|h]+|lea [e]*di, [e]*di|lea [e]*si, [e]*si|lea [e]*bp, [e]*bp+|lea [e]*sp, [e]*sp|^lea [e]*a[x|l|h]+, [dword|byte]+ [ptr]* \[[e]*a[x|l|h] [+|-]+|^lea [dword|byte]+ ptr \[[e]*[abcdspb]+[x|l|h|i|p]+ [+|-]+ |^lea [e]*[abcdspb]+[x|l|h|i|p]+, [dword|byte]+ ptr \[0x|^lea [e]*a[x|l|h]+, [dword|byte]+ [ptr]* \[[e]*a[x|l|h]+ [+|-]+|^lea [e]*[abcdspb]+[x|l|h|i|p]+, es|^lea [e]*[abcdspb]+[x|l|h|i|p]+, [dword|byte]+ [ptr]* \[[e]*[abcdspb]+[x|l|h|i|p]+ [+|-]+ [e]*[abcdspb]+[x|l|h|i|p]+\*', val2[i-lGoBack], re.M|re.I)
									if not matchObj:
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListBaseLea(saveq, numLines, NumOpsDis, modName)
										# addListBaseLea(save, lGoBack, NumOpsDis, modName) 
										#eax - saving add to specific registers -- far more useful.
										
										
										matchObj = re.match( r'^lea [e]*a[x|l|h]+|^lea [dword|byte]+ ptr \[[e]*a[x|l|h]', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseLeaEAX(saveq, numLines, NumOpsDis, modName)
											# addListBaseLeaEAX(save, lGoBack, NumOpsDis, modName)
										#ebx
										matchObj = re.match( r'^lea [e]*b[x|l|h]+|^lea [dword|byte]+ ptr \[[e]*b[x|l|h]', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseLeaEBX(saveq, numLines, NumOpsDis, modName)
											# addListBaseLeaEBX(save, lGoBack, NumOpsDis, modName)
										#ecx
										matchObj = re.match( r'^lea [e]*c[x|l|h]+|^lea [dword|byte]+ ptr \[[e]*c[x|l|h]', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseLeaECX(saveq, numLines, NumOpsDis, modName)
											# addListBaseLeaECX(save, lGoBack, NumOpsDis, modName)
										#eDx
										matchObj = re.match( r'^lea [e]*d[x|l|h]+|^lea [dword|byte]+ ptr \[[e]*d[x|l|h]', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseLeaEDX(saveq, numLines, NumOpsDis, modName)
											# addListBaseLeaEDX(save, lGoBack, NumOpsDis, modName)

										#ESI 
										matchObj = re.match( r'^lea [e]*si|^lea [dword|byte]+ ptr \[[e]*si', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseLeaESI(saveq, numLines, NumOpsDis, modName)
											# addListBaseLeaESI(save, lGoBack, NumOpsDis, modName)
										#EDI 
										matchObj = re.match( r'^lea [e]*di|^lea [dword|byte]+ ptr \[[e]*di', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											# print "leaedi enter"
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												# print "leaedi true"
												addListBaseLeaEDI(saveq, numLines, NumOpsDis, modName)
											# addListBaseLeaEDI(save, lGoBack, NumOpsDis, modName)
										#esp
										matchObj = re.match( r'^lea [e]*sp|^lea [dword|byte]+ ptr \[[e]*sp', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseLeaESP(saveq, numLines, NumOpsDis, modName)
											# addListBaseLeaESP(save, lGoBack, NumOpsDis, modName)
										#EBP
										matchObj = re.match( r'^lea [e]*bp|^lea [dword|byte]+ ptr \[[e]*bp', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseLeaEBP(saveq, numLines, NumOpsDis, modName)
											# addListBaseLeaEBP(save, lGoBack, NumOpsDis, modName)
							except IndexError:
								pass
							#

							#mov shuffle
							try: 
								matchObj = re.match( r'\bmov\b', val2[i-lGoBack], re.M|re.I)
							
								if matchObj: 
									matchObj = re.match( r'^mov [e]*a[x|l]+, [dword|byte]+ [ptr]* \[[e]*a[x|l|h]*|^mov [e]*b[x|l]+, [dword|byte]+ [ptr]* \[[e]*b[x|l|h]*|^mov [e]*c[x|l]+, [dword|byte]+ [ptr]* \[[e]*c[x|l|h]*|^mov [e]*d[x|l|h]+, [dword|byte]+ [ptr]* \[[e]*d[x|l|h]*|^mov [e]*di, [dword|byte]+ [ptr]* \[[e]*di|^mov [e]*si, [dword|byte]+ [ptr]* \[[e]*si|^mov [e]*sp, [dword|byte]+ [ptr]* \[[e]*sp|^mov [e]*bp, [dword|byte]+ [ptr]* \[[e]*bp|mov [e]*a[x|l]+, [e]*a[x|l|h]+|mov [e]*b[x|l]+, [e]*b[x|l|h]+|mov [e]*c[x|l|h]+, [e]*c[x|l|h]+|mov [e]*d[x|l]+, [e]*d[x|l|h]+|mov [e]*di, [e]*di|mov [e]*si, [e]*si|mov [e]*bp, [e]*bp+|mov [e]*sp, [e]*sp|^mov [e]*a[x|l]+, [dword|byte]+ [ptr]* \[[e]*a[x|l|h] [+|-]+|^mov [dword|byte]+ ptr \[[e]*[abcdspb]+[x|l|h|i|p]+ [+|-]+ |^mov [e]*[abcdspb]+[x|l|i|p]+, [dword|byte]+ ptr \[0x|^mov [e]*a[x|l]+, [dword|byte]+ [ptr]* \[[e]*a[x|l|h]+ [+|-]+|^mov [e]*[abcdspb]+[x|l|i|p]+, es', val2[i-lGoBack], re.M|re.I)
									if not matchObj:
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListBaseMovShuf(saveq, numLines, NumOpsDis, modName)
											# addListBaseMovShuf(save, lGoBack, NumOpsDis, modName) 

										#eax - saving add to specific registers -- far more useful.
																				
										matchObj = re.match( r'^mov [e]*a[x|l]+, [e]*[abcdspb]+[x|l|h|i|p]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseMovShufEAX(saveq, numLines, NumOpsDis, modName)
											# addListBaseMovShufEAX(save, lGoBack, NumOpsDis, modName)
										#ebx
										matchObj = re.match( r'^mov [e]*b[x|l]+, [e]*[abcdspb]+[x|l|h|i|p]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseMovShufEBX(saveq, numLines, NumOpsDis, modName)
											# addListBaseMovShufEBX(save, lGoBack, NumOpsDis, modName)
										#ecx
										matchObj = re.match( r'^mov [e]*c[x|l]+, [e]*[abcdspb]+[x|l|h|i|p]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseMovShufECX(saveq, numLines, NumOpsDis, modName)
											# addListBaseMovShufECX(save, lGoBack, NumOpsDis, modName)
										#eDx
										matchObj = re.match( r'^mov [e]*d[x|l]+, [e]*[abcdspb]+[x|l|h|i|p]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseMovShufEDX(saveq, numLines, NumOpsDis, modName)
											# addListBaseMovShufEDX(save, lGoBack, NumOpsDis, modName)

										#ESI 
										matchObj = re.match( r'^mov [e]*si, [e]*[abcdspb]+[x|l|h|i|p]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseMovShufESI(saveq, numLines, NumOpsDis, modName)
											# addListBaseMovShufESI(save, lGoBack, NumOpsDis, modName)
										#EDI 
										matchObj = re.match( r'^mov [e]*di, [e]*[abcdspb]+[x|l|h|i|p]+', val2[i-lGoBack], re.M|re.I)
										
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseMovShufEDI(saveq, numLines, NumOpsDis, modName)
											# addListBaseMovShufEDI(save, lGoBack, NumOpsDis, modName)
										#esp
										matchObj = re.match( r'^mov [e]*sp, [e]*[abcdspb]+[x|l|h|i|p]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:									
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseMovShufESP(saveq, numLines, NumOpsDis, modName)
											# addListBaseMovShufESP(save, lGoBack, NumOpsDis, modName)
										#EBP
										matchObj = re.match( r'^mov [e]*bp, [e]*[abcdspb]+[x|l|h|i|p]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseMovShufEBP(saveq, numLines, NumOpsDis, modName)
											# addListBaseMovShufEBP(save, lGoBack, NumOpsDis, modName)
							except IndexError:
								pass

							#mov value into registers
							try: 
								matchObj = re.match( r'\bmov\b', val2[i-lGoBack], re.M|re.I)
							
								if matchObj: 
									matchObj = re.match( r'^mov [e]*a[x|l]+, [dword|byte]+ [ptr]* \[[e]*a[x|l|h]*|^mov [e]*b[x|l]+, [dword|byte]+ [ptr]* \[[e]*b[x|l|h]*|^mov [e]*c[x|l]+, [dword|byte]+ [ptr]* \[[e]*c[x|l|h]*|^mov [e]*d[x|l|h]+, [dword|byte]+ [ptr]* \[[e]*d[x|l|h]*|^mov [e]*di, [dword|byte]+ [ptr]* \[[e]*di|^mov [e]*si, [dword|byte]+ [ptr]* \[[e]*si|^mov [e]*sp, [dword|byte]+ [ptr]* \[[e]*sp|^mov [e]*bp, [dword|byte]+ [ptr]* \[[e]*bp|mov [e]*a[x|l]+, [e]*a[x|l|h]+|mov [e]*b[x|l]+, [e]*b[x|l|h]+|mov [e]*c[x|l|h]+, [e]*c[x|l|h]+|mov [e]*d[x|l]+, [e]*d[x|l|h]+|mov [e]*di, [e]*di|mov [e]*si, [e]*si|mov [e]*bp, [e]*bp+|mov [e]*sp, [e]*sp|^mov [e]*a[x|l]+, [dword|byte]+ [ptr]* \[[e]*a[x|l|h] [+|-]+|^mov [dword|byte]+ ptr \[[e]*[abcdspb]+[x|l|h|i|p]+ [+|-]+ |^mov [e]*[abcdspb]+[x|l|i|p]+, [dword|byte]+ ptr \[0x|^mov [e]*a[x|l]+, [dword|byte]+ [ptr]* \[[e]*a[x|l|h]+ [+|-]+|^mov [e]*[abcdspb]+[x|l|i|p]+, es', val2[i-lGoBack], re.M|re.I)
									if not matchObj:

										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListBaseMovVal(saveq, numLines, NumOpsDis, modName)
											# addListBaseMovVal(save, lGoBack, NumOpsDis, modName) 

										#eax - saving add to specific registers -- far more useful.
																				
										matchObj = re.match( r'^mov [e]*a[x|l]+, [0x]*[0-9]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:

											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseMovValEAX(saveq, numLines, NumOpsDis, modName)
											# addListBaseMovValEAX(save, lGoBack, NumOpsDis, modName)
										#ebx
										matchObj = re.match( r'^mov [e]*b[x|l]+, [0x]*[0-9]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseMovValEBX(saveq, numLines, NumOpsDis, modName)
											# addListBaseMovValEBX(save, lGoBack, NumOpsDis, modName)
										#ecx
										matchObj = re.match( r'^mov [e]*c[x|l]+, [0x]*[0-9]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseMovValECX(saveq, numLines, NumOpsDis, modName)
											# addListBaseMovValECX(save, lGoBack, NumOpsDis, modName)
										#eDx
										matchObj = re.match( r'^mov [e]*d[x|l]+, [0x]*[0-9]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseMovValEDX(saveq, numLines, NumOpsDis, modName)
											# addListBaseMovValEDX(save, lGoBack, NumOpsDis, modName)

										#ESI 
										matchObj = re.match( r'^mov [e]*si, [0x]*[0-9]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseMovValESI(saveq, numLines, NumOpsDis, modName)
											# addListBaseMovValESI(save, lGoBack, NumOpsDis, modName)
										#EDI 
										matchObj = re.match( r'^mov [e]*di, [0x]*[0-9]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseMovValEDI(saveq, numLines, NumOpsDis, modName)
											# addListBaseMovValEDI(save, lGoBack, NumOpsDis, modName)
										#esp
										matchObj = re.match( r'^mov [e]*sp, [0x]*[0-9]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseMovValESP(saveq, numLines, NumOpsDis, modName)
											# addListBaseMovValESP(save, lGoBack, NumOpsDis, modName)
										#EBP
										matchObj = re.match( r'^mov [e]*bp, [0x]*[0-9]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseMovValEBP(saveq, numLines, NumOpsDis, modName)
											# addListBaseMovValEBP(save, lGoBack, NumOpsDis, modName)
							except IndexError:
								pass

						#now5
							try:
								matchObj = re.match( r'^mov dword ptr \[[e]*[abcdspbixfs]*\], [e]*[acbdps]+[x|p|i]+|^mov \[[e]*[abcdspbixfs]*\], [e]*[acbdps]+[x|p|i]+', val2[i-lGoBack], re.M|re.I)
								if matchObj:
									# print "magicalDeref"
									numLines= giveLineNum(val5,val2[i-lGoBack])
									z =stupidPreJ(val5, numLines)
									if z == True:
										addListMovDeref(saveq, numLines, NumOpsDis, modName)

									matchObj = re.match( r'^mov dword ptr \[[e]*a[x|l]+\], [e]*[cdspb]+[x|i|p]+|^mov dword ptr \[[e]*a[x|l]+\], [e]*[cdspb]+[x|i|p]+', val2[i-lGoBack], re.M|re.I)
									if matchObj:
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListMovDerefEAX(saveq, numLines, NumOpsDis, modName)


									matchObj = re.match( r'^mov dword ptr \[[e]*b[x|l]+\], [e]*[acdsp]+[x|i|p]+|^mov dword ptr \[[e]*b[x|l]+\], [e]*[acdsp]+[x|i|p]+', val2[i-lGoBack], re.M|re.I)
									if matchObj:
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListMovDerefEBX(saveq, numLines, NumOpsDis, modName)


									matchObj = re.match( r'^mov dword ptr \[[e]*c[x|l]+\], [e]*[adspb]+[x|i|p]+|^mov dword ptr \[[e]*c[x|l]+\], [e]*[adspb]+[x|i|p]+', val2[i-lGoBack], re.M|re.I)
									if matchObj:
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListMovDerefECX(saveq, numLines, NumOpsDis, modName)

									matchObj = re.match( r'^mov dword ptr \[[e]*d[x|l]+\], [e]*[acspb]+[x|i|p]+|^mov dword ptr \[[e]*d[x|l]+\], [e]*[acspb]+[x|i|p]+', val2[i-lGoBack], re.M|re.I)
									if matchObj:
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListMovDerefEDX(saveq, numLines, NumOpsDis, modName)
									matchObj = re.match( r'^mov dword ptr \[[e]*di+\], [e]*[acdspb]+[x|p]+ |^mov dword ptr \[[e]*di+\], esi|^mov \[[e]*di+\], [e]*[acdspb]+[x|p]+ |^mov \[[e]*di+\], esi', val2[i-lGoBack], re.M|re.I)
									if matchObj:
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListMovDerefEDI(saveq, numLines, NumOpsDis, modName)

									matchObj = re.match( r'^mov dword ptr \[[e]*si+\], [e]*[acsspb]+[x|p]+ |^mov dword ptr \[[e]*si+\], edi|^mov \[[e]*si+\], [e]*[acsspb]+[x|p]+ |^mov \[[e]*si+\], edi', val2[i-lGoBack], re.M|re.I)
									if matchObj:		
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListMovDerefESI(saveq, numLines, NumOpsDis, modName)
									matchObj = re.match( r'^mov dword ptr \[[e]*bp+\], [e]*[acsp]+[x|p|i]+ |^mov dword ptr \[[e]*bp+\], edi|^mov \[[e]*bp+\], [e]*[acsp]+[x|p|i]+ |^mov \[[e]*bp+\], edi', val2[i-lGoBack], re.M|re.I)
									if matchObj:
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListMovDerefEBP(saveq, numLines, NumOpsDis, modName)
									matchObj = re.match( r'^mov dword ptr \[[e]*sp+\], [e]*[acbp]+[x|p|i]+ |^mov dword ptr \[[e]*sp+\], esi|^mov \[[e]*sp+\], [e]*[acbp]+[x|p|i]+ |^mov \[[e]*sp+\], esi', val2[i-lGoBack], re.M|re.I)
									if matchObj:
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListMovDerefESP(saveq, numLines, NumOpsDis, modName)

							except:
								pass
							#searching for Push
							try: 
								matchObj = re.match( r'\bpush\b', val2[i-lGoBack], re.M|re.I)
							
								if matchObj: 
									numLines= giveLineNum(val5,val2[i-lGoBack])
									z =stupidPreJ(val5, numLines)
									if z == True:
										addListBasePush(saveq, numLines, NumOpsDis, modName)
									# addListBasePush(save, lGoBack, NumOpsDis, modName) 
									#eax - saving add to specific registers -- far more useful.	
									matchObj = re.match( r'^push [e]*a[x|l|h]+', val2[i-lGoBack], re.M|re.I)
									if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBasePushEAX(saveq, numLines, NumOpsDis, modName)
										# addListBasePushEAX(save, lGoBack, NumOpsDis, modName)
									#ebx
									matchObj = re.match( r'^push [e]*b[x|l|h]+', val2[i-lGoBack], re.M|re.I)
									if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBasePushEBX(saveq, numLines, NumOpsDis, modName)
										# addListBasePushEBX(save, lGoBack, NumOpsDis, modName)
									#ecx
									matchObj = re.match( r'^push [e]*c[x|l|h]+', val2[i-lGoBack], re.M|re.I)
									if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBasePushECX(saveq, numLines, NumOpsDis, modName)
										# addListBasePushECX(save, lGoBack, NumOpsDis, modName)
									#eDx
									matchObj = re.match( r'^push [e]*d[x|l|h]+', val2[i-lGoBack], re.M|re.I)
									if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBasePushEDX(saveq, numLines, NumOpsDis, modName)
										# addListBasePushEDX(save, lGoBack, NumOpsDis, modName)
									#ESI 
									matchObj = re.match( r'^push [e]*si', val2[i-lGoBack], re.M|re.I)
									if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBasePushESI(saveq, numLines, NumOpsDis, modName)
										# addListBasePushESI(save, lGoBack, NumOpsDis, modName)
									#EDI 
									matchObj = re.match( r'^push [e]*di', val2[i-lGoBack], re.M|re.I)
									if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBasePushEDI(saveq, numLines, NumOpsDis, modName)
										# addListBasePushEDI(save, lGoBack, NumOpsDis, modName)
									#esp
									matchObj = re.match( r'^push [e]*sp', val2[i-lGoBack], re.M|re.I)
									if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBasePushESP(saveq, numLines, NumOpsDis, modName)
										# addListBasePushESP(save, lGoBack, NumOpsDis, modName)
									#EBP
									matchObj = re.match( r'^push [e]*bp', val2[i-lGoBack], re.M|re.I)
									if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBasePushEBP(saveq, numLines, NumOpsDis, modName)
										# addListBasePushEBP(save, lGoBack, NumOpsDis, modName)					
							except IndexError:
								pass
							#searching for Pop
							try: 
								matchObj = re.match( r'\bpop\b', val2[i-lGoBack], re.M|re.I)
								if matchObj: 
									# addListBasePop(save, lGoBack, NumOpsDis, modName) 
									numLines= giveLineNum(val5,val2[i-lGoBack])
									z =stupidPreJ(val5, numLines)
									if z == True:
										# print "pop all"
										# for x in val5:
										# 	print x
										# print numLines
										addListBasePop(saveq, numLines, NumOpsDis, modName)
									#eax - saving add to specific registers -- far more useful.	
									matchObj = re.match( r'^pop [e]*a[x|l|h]+', val2[i-lGoBack], re.M|re.I)
									if matchObj:
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListBasePopEAX(saveq, numLines, NumOpsDis, modName)
										# addListBasePopEAX(save, lGoBack, NumOpsDis, modName)
									
									#ebx
									matchObj = re.match( r'^pop [e]*b[x|l|h]+', val2[i-lGoBack], re.M|re.I)
									if matchObj:
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListBasePopEBX(saveq, numLines, NumOpsDis, modName)
										# addListBasePopEBX(save, lGoBack, NumOpsDis, modName)
									
									#ecx
									matchObj = re.match( r'^pop [e]*c[x|l|h]+', val2[i-lGoBack], re.M|re.I)
									if matchObj:
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListBasePopECX(saveq, numLines, NumOpsDis, modName)
										# addListBasePopECX(save, lGoBack, NumOpsDis, modName)
									
									#eDx
									matchObj = re.match( r'^pop [e]*d[x|l|h]+', val2[i-lGoBack], re.M|re.I)
									if matchObj:
										# print "initialEDX"
										numLines= giveLineNum(val5,val2[i-lGoBack])
										# for x in val5:
										# 	print x
										# print numLines
										z =stupidPreJ(val5, numLines)
										if z == True:
											# print "saving edx"
											addListBasePopEDX(saveq, numLines, NumOpsDis, modName)
										# addListBasePopEDX(save, lGoBack, NumOpsDis, modName)
									#ESI 
									matchObj = re.match( r'^pop [e]*si', val2[i-lGoBack], re.M|re.I)
									if matchObj:
									
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListBasePopESI(saveq, numLines, NumOpsDis, modName)
										# addListBasePopESI(save, lGoBack, NumOpsDis, modName)
									#EDI 
									matchObj = re.match( r'^pop [e]*di', val2[i-lGoBack], re.M|re.I)
									if matchObj:
									
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListBasePopEDI(saveq, numLines, NumOpsDis, modName)
										# addListBasePopEDI(save, lGoBack, NumOpsDis, modName)
									#esp
									matchObj = re.match( r'^pop [e]*sp', val2[i-lGoBack], re.M|re.I)
									if matchObj:
									
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListBasePopESP(saveq, numLines, NumOpsDis, modName)
										# addListBasePopESP(save, lGoBack, NumOpsDis, modName)
									#EBP
									matchObj = re.match( r'^pop [e]*bp', val2[i-lGoBack], re.M|re.I)
									if matchObj:
									
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListBasePopEBP(saveq, numLines, NumOpsDis, modName)
										# addListBasePopEBP(save, lGoBack, NumOpsDis, modName)					
							except IndexError:
								pass
							try:   #bramw
								special = 0
								matchObj = re.match( r'\bpop\b|\badd esp\b|\badc esp\b|\badd sp\b|\badc esp\b', val2[i-lGoBack], re.M|re.I)
								temp = i - lGoBack
								if matchObj:
									sdone=0
									while (temp < i):
										#spec = re.match( r'\bpop\b', val2[temp], re.M|re.I)
										#specAddEsp = re.match( r'\badd esp\b', val2[temp], re.M|re.I)
										jcEAX = re.match( r'\bjmp eax\b|\bcall eax\b', val2[temp], re.M|re.I)
										jcEBX = re.match( r'\bjmp ebx\b|\bcall ebx\b', val2[temp], re.M|re.I)
										jcECX = re.match( r'\bjmp ecx\b|\bcall ecx\b', val2[temp], re.M|re.I)
										jcEDX = re.match( r'\bjmp edx\b|\bcall edx\b', val2[temp], re.M|re.I)
										jcEDI = re.match( r'\bjmp edi\b|\bcall edi\b', val2[temp], re.M|re.I)
										jcESI = re.match( r'\bjmp esi\b|\bcall esi\b', val2[temp], re.M|re.I)
										jcEBP = re.match( r'\bjmp ebp\b|\bcall ebp\b', val2[temp], re.M|re.I)
										jcESP = re.match( r'\bjmp esp\b|\bcall esp\b', val2[temp], re.M|re.I)
										if jcEAX:
											# print "saving eax`"
											if (temp==-1):
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListStackPivotEAX(saveq, numLines, NumOpsDis, modName,0)
												# addListStackPivotEAX(save, lGoBack, NumOpsDis, modName, 0) 
												# print "checking0"
												# print "save1: " + str(save)
												# print "temp " + str(temp)
												# print "i " + str(i)
												# for a in val2:
												# 	print a
										if jcEBX:
											# print "saving ebx`"
											# print val2[temp]
											if (temp==-1):
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListStackPivotEBX(saveq, numLines, NumOpsDis, modName,0)
												# addListStackPivotEBX(save, lGoBack, NumOpsDis, modName, 0) 
												sdone +=1
										if jcECX:
											if (temp==-1):
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListStackPivotECX(saveq, numLines, NumOpsDis, modName,0)
												# addListStackPivotECX(save, lGoBack, NumOpsDis, modName, 0) 
												sdone +=1
										if jcEDX:
											if (temp==-1):
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListStackPivotEDX(saveq, numLines, NumOpsDis, modName,0)
												# addListStackPivotEDX(save, lGoBack, NumOpsDis, modName, 0) 
												sdone +=1
										if jcEDI:
											if (temp==-1):
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListStackPivotEDI(saveq, numLines, NumOpsDis, modName,0)
												# addListStackPivotEDI(save, lGoBack, NumOpsDis, modName, 0) 
												sdone +=1
										if jcESI:
											if (temp==-1):
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListStackPivotESI(saveq, numLines, NumOpsDis, modName,0)
												# addListStackPivotESI(save, lGoBack, NumOpsDis, modName, 0) 
												sdone +=1
										if jcESP:
											if (temp==-1):
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListStackPivotESP(saveq, numLines, NumOpsDis, modName,0)
												# addListStackPivotESP(save, lGoBack, NumOpsDis, modName, 0) 
												sdone +=1
										if jcEBP:
											if (temp==-1):
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListStackPivotEBP(saveq, numLines, NumOpsDis, modName,0)
												# addListStackPivotEBP(save, lGoBack, NumOpsDis, modName, 0) 
												sdone +=1
										






											

										temp = temp + 1
									#current
									addListStackPivot(save, lGoBack, NumOpsDis, modName, 0) 
									#eax - saving add to specific registers -- far more useful.	
									#print "special count2 is " + str(special)
							except IndexError:
								pass
							#searching for Inc

							

							try: 
								matchObj = re.match( r'\binc\b', val2[i-lGoBack], re.M|re.I)
								if matchObj: 
									numLines= giveLineNum(val5,val2[i-lGoBack])
									z =stupidPreJ(val5, numLines)
									if z == True:
										addListBaseInc(saveq, numLines, NumOpsDis, modName)
									# addListBaseInc(save, lGoBack, NumOpsDis, modName) 
									#eax - saving add to specific registers -- far more useful.	
									matchObj = re.match( r'^inc [e]*a[x|l|h]+', val2[i-lGoBack], re.M|re.I)
									if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseIncEAX(saveq, numLines, NumOpsDis, modName)
										# addListBaseIncEAX(save, lGoBack, NumOpsDis, modName)
									#ebx
									matchObj = re.match( r'^inc [e]*b[x|l|h]+', val2[i-lGoBack], re.M|re.I)
									if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseIncEBX(saveq, numLines, NumOpsDis, modName)
										# addListBaseIncEBX(save, lGoBack, NumOpsDis, modName)
									#ecx
									matchObj = re.match( r'^inc [e]*c[x|l|h]+', val2[i-lGoBack], re.M|re.I)
									if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseIncECX(saveq, numLines, NumOpsDis, modName)
										# addListBaseIncECX(save, lGoBack, NumOpsDis, modName)
									#eDx
									matchObj = re.match( r'^inc [e]*d[x|l|h]+', val2[i-lGoBack], re.M|re.I)
									if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseIncEDX(saveq, numLines, NumOpsDis, modName)
										# addListBaseIncEDX(save, lGoBack, NumOpsDis, modName)
									#ESI 
									matchObj = re.match( r'^inc [e]*si', val2[i-lGoBack], re.M|re.I)
									if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseIncESI(saveq, numLines, NumOpsDis, modName)
										# addListBaseIncESI(save, lGoBack, NumOpsDis, modName)
									#EDI 
									matchObj = re.match( r'^inc [e]*di', val2[i-lGoBack], re.M|re.I)
									if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseIncEDI(saveq, numLines, NumOpsDis, modName)
										# addListBaseIncEDI(save, lGoBack, NumOpsDis, modName)
									#esp
									matchObj = re.match( r'^inc [e]*sp', val2[i-lGoBack], re.M|re.I)
									if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseIncESP(saveq, numLines, NumOpsDis, modName)
										# addListBaseIncESP(save, lGoBack, NumOpsDis, modName)
									#EBP
									matchObj = re.match( r'^inc [e]*bp', val2[i-lGoBack], re.M|re.I)
									if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseIncEBP(saveq, numLines, NumOpsDis, modName)
										# addListBaseIncEBP(save, lGoBack, NumOpsDis, modName)					
							except IndexError:
								pass
							#searching for Dec
							try: 
								matchObj = re.match( r'\bdec\b', val2[i-lGoBack], re.M|re.I)
								if matchObj: 
									numLines= giveLineNum(val5,val2[i-lGoBack])
									z =stupidPreJ(val5, numLines)
									if z == True:
										addListBaseDec(saveq, numLines, NumOpsDis, modName)
									# addListBaseDec(save, lGoBack, NumOpsDis, modName) 
									#eax - saving add to specific registers -- far more useful.	
									matchObj = re.match( r'^dec [e]*a[x|l|h]+', val2[i-lGoBack], re.M|re.I)
									if matchObj:
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListBaseDecEAX(saveq, numLines, NumOpsDis, modName)
										# addListBaseDecEAX(save, lGoBack, NumOpsDis, modName)
									#ebx
									matchObj = re.match( r'^dec [e]*b[x|l|h]+', val2[i-lGoBack], re.M|re.I)
									if matchObj:
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListBaseDecEBX(saveq, numLines, NumOpsDis, modName)
										# addListBaseDecEBX(save, lGoBack, NumOpsDis, modName)
									#ecx
									matchObj = re.match( r'^dec [e]*c[x|l|h]+', val2[i-lGoBack], re.M|re.I)
									if matchObj:
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListBaseDecECX(saveq, numLines, NumOpsDis, modName)
									# addListBaseDecECX(save, lGoBack, NumOpsDis, modName)
									#eDx
									matchObj = re.match( r'^dec [e]*d[x|l|h]+', val2[i-lGoBack], re.M|re.I)
									if matchObj:
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListBaseDecEDX(saveq, numLines, NumOpsDis, modName)
										# addListBaseDecEDX(save, lGoBack, NumOpsDis, modName)
									#ESI 
									matchObj = re.match( r'^dec [e]*si', val2[i-lGoBack], re.M|re.I)
									if matchObj:
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListBaseDecESI(saveq, numLines, NumOpsDis, modName)
										# addListBaseDecESI(save, lGoBack, NumOpsDis, modName)
									#EDI 
									matchObj = re.match( r'^dec [e]*di', val2[i-lGoBack], re.M|re.I)
									if matchObj:
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListBaseDecEDI(saveq, numLines, NumOpsDis, modName)
										# addListBaseDecEDI(save, lGoBack, NumOpsDis, modName)
									#esp
									matchObj = re.match( r'^dec [e]*sp', val2[i-lGoBack], re.M|re.I)
									if matchObj:
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListBaseDecESP(saveq, numLines, NumOpsDis, modName)
										# addListBaseDecESP(save, lGoBack, NumOpsDis, modName)
									#EBP
									matchObj = re.match( r'^dec [e]*bp', val2[i-lGoBack], re.M|re.I)
									if matchObj:
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListBaseDecEBP(saveq, numLines, NumOpsDis, modName)
									# addListBaseDecEBP(save, lGoBack, NumOpsDis, modName)					
							except IndexError:
								pass
							#searching for Xchg
							
							try: 	
								matchObj = re.match( r'\bxchg\b', val2[i-lGoBack], re.M|re.I)
								if matchObj:
									matchObj = re.match( r'^xchg eax, eax|^xchg ebx, ebx|^xchg ecx, ecx|^xchg edx, edx|^xchg esi, esi|^xchg edi, edi|^xchg esp, esp|^xchg ebp, ebp|^xchg ax, ax|^xchg bx, bx|^xchg cx, cx|^xchg dx, dx|^xchg si, si|^xchg di, di|^xchg sp, sp|^xchg bp, bp|^xchg al, al|^xchg bl, bl|^xchg cl, cl|^xchg dl, dl', val2[i-lGoBack], re.M|re.I)
								
									if not matchObj: 
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListBaseXchg(saveq, numLines, NumOpsDis, modName)
										# addListBaseXchg(save, lGoBack, NumOpsDis, modName) 
										#eax - saving add to specific registers -- far more useful.				
										matchObj = re.match( r'^xchg eax, e[abcdsb]+[xspi]+|^xchg e[abcdsb]+[xspi]+, eax|^xchg ax, [abcdsb]+[xspi]+|^xchg [abcdsb]+[xspi]+, ax', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseXchgEAX(saveq, numLines, NumOpsDis, modName)
											# addListBaseXchgEAX(save, lGoBack, NumOpsDis, modName)

										#ebx
										matchObj = re.match( r'^xchg ebx, e[abcdsb]+[xspi]+|^xchg e[abcdsb]+[xspi]+, ebx|^xchg bx, [abcdsb]+[xspi]+|^xchg [abcdsb]+[xspi]+, bx', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseXchgEBX(saveq, numLines, NumOpsDis, modName)
											# addListBaseXchgEBX(save, lGoBack, NumOpsDis, modName)
										#ecx
										matchObj = re.match( r'^xchg ecx, e[abcdsb]+[xspi]+|^xchg e[abcdsb]+[xspi]+, ecx|^xchg cx, [abcdsb]+[xspi]+|^xchg [abcdsb]+[xspi]+, cx', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseXchgECX(saveq, numLines, NumOpsDis, modName)
											# addListBaseXchgECX(save, lGoBack, NumOpsDis, modName)
										#eDx
										matchObj = re.match( r'^xchg edx, e[abcdsb]+[xspi]+|^xchg e[abcdsb]+[xspi]+, edx|^xchg dx, [abcdsb]+[xspi]+|^xchg [abcdsb]+[xspi]+, dx', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseXchgEDX(saveq, numLines, NumOpsDis, modName)
											# addListBaseXchgEDX(save, lGoBack, NumOpsDis, modName)
										#ESI 
										matchObj = re.match( r'^xchg esi, e[abcdsb]+[xspi]+|^xchg e[abcdsb]+[xspi]+, esi|^xchg si, [abcdsb]+[xspi]+|^xchg [abcdsb]+[xspi]+, si', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseXchgESI(saveq, numLines, NumOpsDis, modName)
											# addListBaseXchgESI(save, lGoBack, NumOpsDis, modName)
										#EDI 
										matchObj = re.match( r'^xchg edi, e[bcdsb]+[xspi]+|^xchg e[abcdsb]+[xspi]+, edi|^xchg di, [abcdsb]+[xspi]+|^xchg [abcdsb]+[xspi]+, di', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseXchgEDI(saveq, numLines, NumOpsDis, modName)
											# addListBaseXchgEDI(save, lGoBack, NumOpsDis, modName)
										#esp
										matchObj = re.match( r'^xchg esp, e[abcdsb]+[xspi]+|^xchg e[abcdsb]+[xspi]+, esp|^xchg sp, [abcdsb]+[xspi]+|^xchg [abcdsb]+[xspi]+, sp', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseXchgESP(saveq, numLines, NumOpsDis, modName)
											# addListBaseXchgESP(save, lGoBack, NumOpsDis, modName)
										#EBP
										matchObj = re.match( r'^xchg ebp, e[abcdsb]+[xspi]+|^xchg e[abcdsb]+[xspi]+, ebp|^xchg bp, [abcdsb]+[xspi]+|^xchg [abcdsb]+[xspi]+, bp', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseXchgEBP(saveq, numLines, NumOpsDis, modName)
											# addListBaseXchgEBP(save, lGoBack, NumOpsDis, modName)					
							except IndexError:
								pass
							#now7	
							#searching for Shift Left
							#not common, so no need to do by specific regs
							try: 
								matchObj = re.match( r'^s[a|h]l+[dwl]* [dword|byte]+ [ptr]* \[[e]*[abcdspb]+[x|l|h|i|p]+ [+|-]+|^salc ', val2[i-lGoBack], re.M|re.I)
								if not matchObj:
									matchObj = re.match( r'^shl|^sal', val2[i-lGoBack], re.M|re.I)
									if matchObj:
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListBaseShiftLeft(saveq, numLines, NumOpsDis, modName)
										# addListBaseShiftLeft(save, lGoBack, NumOpsDis, modName)
							except IndexError:
								pass
								#Shift Right
								#not common, so no need to do by specific regs
							try: 
								matchObj = re.match( r'^s[a|h]+r[dwl]* [dword|byte]+ [ptr]* \[[e]*[abcdspb]+[x|l|h|i|p]+ [+|-]+|^salc ', val2[i-lGoBack], re.M|re.I)
								if not matchObj:	
									matchObj = re.match( r'^shr|^sar', val2[i-lGoBack], re.M|re.I)
									if matchObj:
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListBaseShiftLeft(saveq, numLines, NumOpsDis, modName)
										# addListBaseShiftRight(save, lGoBack, NumOpsDis, modName)
							except IndexError:
								pass
								#Rotate Left 
								#not common, so no need to do by specific regs
							try: 
								matchObj = re.match( r'^r[o|c]+l [dword|byte]+ [ptr]* \[[e]*[abcdspb]+[x|l|h|i|p]+ [+|-]+ ', val2[i-lGoBack], re.M|re.I)
								if not matchObj:
									matchObj = re.match( r'^rol|^rcl', val2[i-lGoBack], re.M|re.I)
									if matchObj:
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListBaseShiftLeft(saveq, numLines, NumOpsDis, modName)
										# addListBaseRotLeft(save, lGoBack, NumOpsDis, modName)
							except IndexError:
								pass
								#Rotate Right
								#not common, so no need to do by specific regs
							try: 
								matchObj = re.match( r'^r[o|c]+r [dword|byte]+ [ptr]* \[[e]*[abcdspb]+[x|l|h|i|p]+ [+|-]+ ', val2[i-lGoBack], re.M|re.I)
								if not matchObj:	
									matchObj = re.match( r'^ror|^rcr', val2[i-lGoBack], re.M|re.I)
									if matchObj:
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListBaseShiftLeft(saveq, numLines, NumOpsDis, modName)
										# addListBaseRotRight(save, lGoBack, NumOpsDis, modName)
							except IndexError:
								pass
							#done
							lGoBack -= 1

						
def disHereCall(address, NumOpsDis):
	global modName
	global o
	w=0

	## Capstone does not seem to allow me to start disassemblying at a given point, so I copy out a chunk to  disassemble. I append a 0x00 because it does not always disassemble correctly (or at all) if just two bytes. I cause it not to be displayed through other means. It simply take the starting address of the jmp [reg], disassembles backwards, and copies it to a variable that I examine more closely.

	lGoBack = linesGoBackFindOP
	CODED2 = b""

	x = NumOpsDis
	for i in range (x, 0, -1):
		CODED2 += objs[o].data2[address-i]
	CODED2 += objs[o].data2[address]
	CODED2 += objs[o].data2[address+1]
	CODED2 += b"\x00"
					
	# I create the individual lines of code that will appear>
	val =""
	val2 = []
	val3 = []
	val5 =[]
	address2 = address + objs[o].startLoc + 1000
	
	for i in cs.disasm(CODED2, address-x):
		add = hex(int(i.address))
		addb = hex(int(i.address +  objs[o].VirtualAdd))
		add2 = str(add)
		add3 = hex (int(i.address + objs[o].startLoc	))
		add4 = str(add3)
		val =  i.mnemonic + " " + i.op_str + "\t\t\t\t"  + add4 + " (offset " + addb + ")\n"
		val2.append(val)
		val3.append(add2)
		val5.append(val)
		#print val
	

	tz = val2.__len__()
	tk=0
	save=0x00
	# I need to iterate through this in reverse, starting with the jmp [reg].  I contains index number and e is to enumerate, i.e. show what the value is. In this case, it is iterating through an array of  strings containing the disasembly. The goal is ultimately to cut this down by removing other control flow instructions. The end result will be I will know the address of the jmp [reg] and how many lines  to go back without encountering a control flow instruction.
	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = val3[i]   # This allows me to save the initial  address of the target jmp [reg] address.
			# saveq = int(save, 16)
		tk += 1

		# Use regular expressions to find lines that have control flow and other undesired instructions, so they and preceding lines can be excised. 
		# matchObj2 = re.compile( r"\bjo\b|\bjno\b|\bjsn\b|\bjs\b|\bje\b|\bjz\b|\bjne\b|\bjnz\b|\bjb\b|\bjnae\b|\bjc\b|\bjnb\bjae\b|\bjnc\b|\bjbe\bjna\b|\bja\b|\bjnben\b|\bjl\b|\bjnge\b|\bjge\bjnl\b|\bjle\b|\bjng\bjg\b|\bjnle\b|\bjp\b|\bjpe\b|\bjnp\b|\bjpo\bjczz\b|\bjecxz\b|\bjmp\b|\bint\b|\bdb\b", re.M|re.I)
		# if re.findall(matchObj2, e):   #if "ret"  in e:
		# 	if i != 1:
		# 		if i > val2.__len__():
		# 			break  # Gracefully break on unusual cases
		# 		else:
		# 			try: 
		# 				del val2[i]
		# 				del val3[i]
		# 			except IndexError:
		# 				pass
		# 		i = i-1
		# 		while i <= (val2.__len__()):
		# 			#print str(i) +", " 
		# 			if i <0:
		# 				break
		# 			else:
		# 				del val2[i]	
		# 				del val3[i]
		# 				i=i-1
		# 				if i == (val2.__len__()-1):
		# 					break
	tz = val2.__len__()
	tk=0
	save=0
	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = val3[i]   # This allows me to save the initial  address of the target jmp [reg] address.
			saveq = int(save, 16)
		tk += 1
# Here I search for excise ret's from JOP gadget. I had tried to incorporate this functionality into the
# above, but I would run into test cases that would cause errors. This seemed the best solution, even if
# inelegant.
		# matchObj2 = re.compile( r"\bret\b", re.M|re.I)
		# if re.findall(matchObj2, e):   #if "ret"  in e:
		# 	if i != 0:
		# 		if i > val2.__len__():
		# 			break  # Gracefully break on unusual cases
		# 		else:
		# 			try: 
		# 				del val2[i]
		# 				del val3[i]
		# 			except IndexError:
		# 				pass
		# 		i = i-1
		# 		while i <= (val2.__len__()):
		# 			if i <0:
		# 				break
		# 			else:
		# 				del val2[i]	
		# 				del val3[i]
		# 				i=i-1
		# 				if i == (val2.__len__()-1):
		# 					break

		matchObj = re.match( r'call [e]+', val, re.M|re.I)
		if matchObj:
			if save != 0:
				if val2.__len__() > 1:
					if val2.__len__() == 2:
						matchObj = re.match( r'\bnop\b|\bleave\b|\bcall\b|\bret\b|\bjmp\b|\bljmp\b|\bretf\b|\bhlt\b', val2[i-2], re.M|re.I)
						if matchObj:
							counter()
						else:
							save = int(save, 16)
							addListBase(save, val2.__len__(), NumOpsDis, modName) # fist parameter: address of target jmp [reg]; second parameter: number of lines to go back. third parameter: number of ops to go back.
		
					else:
						matchObj = re.match( r'\bnop\b|\bleave\b|\bcall\b|\bret\b|\bjmp\b|\bljmp\b|\bjo\b|\bjno\b|\bjsn\b|\bjs\b|\bje\b|\bjz\b|\bjne\b|\bjnz\b|\bjb\b|\bjnae\b|\bjc\b|\bjnb\bjae\b|\bjnc\b|\bjbe\bjna\b|\bja\b|\bjnben\b|\bjl\b|\bjnge\b|\bjge\bjnl\b|\bjle\b|\bjng\bjg\b|\bjnle\b|\bjp\b|\bjpe\b|\bjnp\b|\bjpo\bjczz\b|\bjecxz\b|\bcall\b|\bint\b|\bdb\b|\bretf\b|\bhltf\b|\bret\b', val2[i-2], re.M|re.I)
						if not matchObj:
							try:
								save = int(save, 16)
								addListBase(save, val2.__len__(), NumOpsDis, modName) # fist parameter: address of target jmp [reg]; second parameter: number of lines to go back. third parameter: number of ops to go back.
								# print "save addlist " + str(save) 

							except:
								# print "weird one1 "	+ str(save)

								save = int(save)
								addListBase(save, val2.__len__(), NumOpsDis, modName) # fist parameter: 
								# print "weird one2 "	+ str(save)
							while lGoBack > 1:
								try:
									matchObj = re.match( r'\badd\b|\badc\b', val2[i-lGoBack], re.M|re.I)
									if matchObj: 
										matchObj = re.match( r'^[add|adc]+ [byte|dword]+ ptr+ \[e[abcds]+[px]+ [+|-]+ 0x|^add [byte|dword]+ ptr+ \[e[abcds][px] \+ 0x|^add e[abcds][px], [dword|byte]+ ptr \[e[abcds][xp] \+ 0x|^add [byte|dword]+ ptr \[eax\], [al|eax]|^add [byte|dword]+ ptr \[ebx\], [bl|bx]|^add [byte|dword]+ ptr \[ecx\], [cl|ecx]|^add [byte|dword]+ ptr \[edx\], [dl|edx]|^[add|adc]+ eax, [dword|byte]+ ptr \[[e|a]+[a|l]+|^[add|adc]+ ebx, [dword|byte]+ ptr \[[e|b]+[b|l]+|^[add|adc]+ ecx, [dword|byte]+ ptr \[[e|c]+[c|l]+|^[add|adc]+ edx, [dword|byte]+ ptr \[[e|d]+[d|l]+|^[add|adc]+ edi, [dword|byte]+ ptr \[[e|d]+[d|i]+|^[add|adc]+ esi, [dword|byte]+ ptr \[[e|s]+[s|i]+|^[add|adc]+ ebp, [dword|byte]+ ptr \[[e|b]+[b|p]+|^[add|adc]+ esp, [dword|byte]+ ptr \[[e|s]+[s|p]+|^[add|adc]+ a[l|h]+, a[l|h]+|^[add|adc]+ b[l|h]+, b[l|h]+|^[add|adc]+ c[l|h]+, c[l|h]+|^[add|adc]+ d[l|h]+, d[l|h]+|^[add|adc]+ di, di|^[add|adc]+ si, si|^[add|adc]+ sp, sp|^[add|adc]+ bp, bp', val2[i-lGoBack], re.M|re.I)   
										# I am using regular expressions to eliminate what would be garbage gadgets, of which there would be countless, off the wall, unintended instructions that would do nothing of any practical value.
										if not matchObj:
											y = val2[i-lGoBack]
											if (y == val2[i-lGoBack]):
												numLines= giveLineNum(val5,y)
												y =stupidPre(val5, numLines)
												if y == True:
													addListBaseAdd(saveq, numLines, NumOpsDis, modName)

											#print "ADDDING************************************\n\n"
											#eax - saving add to specific registers -- far more useful.
											matchObj1 = re.match( r'^[add|adc]+ [dword|byte]* [ptr]* [\[]*[e]*a[x|l|h]+|[add|adc]+ [e]*a[x|l|h]+ ', val2[i-lGoBack], re.M|re.I)
											if matchObj1:
												# print "***************"
												# print "b: " + val2[i-lGoBack]
												y = val2[i-lGoBack]
												# print "y:" + y
												# addListRETPopEDI(saveq, giveLineNum(val5,y), NumOpsDis, modName)
												# print "popedi:"
												# print "all:"
												# print binaryToStr(CODED2)
												# print "i: " + str(i) + " lGoBack: " + str(lGoBack) +  " i-lGoBack: " + str(i-lGoBack)	
												# print "answer: " + str(giveLineNum(val5,val2[i-lGoBack]))
											
												# for x in val2:
												# 	print x
												# print "i-lGoBack: " + str(i-lGoBack)
												# print "a: " + val2[i-lGoBack]
												# if (y != val2[i-lGoBack]):
												# 	print "weird: " + y
												# 	print "  was: " +  val2[i-lGoBack]
												if (y == val2[i-lGoBack]):
												# 	print "REAL"
													# modName2 = Ct()


													numLines= giveLineNum(val5,y)
													y =stupidPreJ(val5, numLines)
													if y == True:
														# print "enter true"
														addListBaseAddEAX(saveq, numLines, NumOpsDis, modName)
														# print Ct()
														counter()

												# print val3[i-lGoBack]
												
												# print "lgoback: (below)"
												# print val2[lGoBack]
												# print val3[lGoBack]
												# print "answer: " + str(giveLineNum(val2))

												# numLines= giveLineNum(val5,val2[i-lGoBack])
												# z =stupidPreJ(val5, numLines)
												# if z == True:
												# 	addListBaseAddEAX(saveq, numLines, NumOpsDis, modName)
												# addListBaseAddEAX(save, lGoBack, NumOpsDis, modName)
											#	print "ADDDING************************************\n\n"
											
											#ebx
											matchObj1 = re.match( r'^[add|adc]+ [dword|byte]* [ptr]* [\[]*[e]*b[x|l|h]+|[add|adc]+ [e]*b[x|l|h]+', val2[i-lGoBack], re.M|re.I)

											
											if matchObj1:
												# print "***********************************************"
												# print "1ebx"
												# print "b: " + val2[i-lGoBack]
												y = val2[i-lGoBack]
												# print "y:" + y
												# # addListRETPopEDI(saveq, giveLineNum(val5,y), NumOpsDis, modName)
												# print "saveebx:"
												# print "all:"
												# print binaryToStr(CODED2)
												# print "i: " + str(i) + " lGoBack: " + str(lGoBack) +  " i-lGoBack: " + str(i-lGoBack)	
												# # print "answer: " + str(giveLineNum(val5,val2[i-lGoBack]))
											
												# for x in val2:
												# 	print x
												# print "i-lGoBack: " + str(i-lGoBack)
												# print "a: " + val2[i-lGoBack]
												# if (y != val2[i-lGoBack]):
												# 	print "weird: " + y
												# 	print "  was: " +  val2[i-lGoBack]
												if (y == val2[i-lGoBack]):
												# # 	print "REAL"
												# 	modName2 = Ct()

													
													# modName2= Ct()
													numLines= giveLineNum(val5,y)
													y =stupidPreJ(val5, numLines)
													if y == True:
														# print "savingebx"
														addListBaseAddEBX(saveq, numLines, NumOpsDis, modName)
														# print Ct()
														# counter()
												# print "***********************************************"


												# numLines= giveLineNum(val5,val2[i-lGoBack])
												# z =stupidPre(val5, numLines)
												# if z == True:
												# 	print "saveebx"
												# 	addListBaseAddEBX(saveq, numLines, NumOpsDis, modName)

												# addListBaseAddEBX(save, lGoBack, NumOpsDis, modName)
											#ecx
											matchObj = re.match( r'^[add|adc]+ [dword|byte]* [ptr]* [\[]*[e]*c[x|l|h]+|[add|adc]+ [e]*c[x|l|h]+', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "saveecx"
													addListBaseAddECX(saveq, numLines, NumOpsDis, modName)

												# addListBaseAddECX(save, lGoBack, NumOpsDis, modName)
											#eDx
											matchObj = re.match( r'^[add|adc]+ [dword|byte]* [ptr]* [\[]*[e]*d[x|l|h]+|[add|adc]+ [e]*d[x|l|h]+', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "saveedx"
													addListBaseAddEDX(saveq, numLines, NumOpsDis, modName)

												# addListBaseAddEDX(save, lGoBack, NumOpsDis, modName)
											#ESI 
											matchObj = re.match( r'^[add|adc]+ [dword|byte]* [ptr]* [\[]*[e]*si|[add|adc]+ [e]*si', val2[i-lGoBack], re.M|re.I)
											if matchObj:

												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "saveesi"
													addListBaseAddESI(saveq, numLines, NumOpsDis, modName)
												# addListBaseAddESI(save, lGoBack, NumOpsDis, modName)
											#EDI 
											matchObj = re.match( r'^[add|adc]+ [dword|byte]* [ptr]* [\[]*[e]*di|[add|adc]+ [e]*di', val2[i-lGoBack], re.M|re.I)
											if matchObj:

												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "saveedi"
													addListBaseAddEDI(saveq, numLines, NumOpsDis, modName)
												# addListBaseAddEDI(save, lGoBack, NumOpsDis, modName)
											#esp
											matchObj = re.match( r'^[add|adc]+ [dword|byte]* [ptr]* [\[]*[e]*sp|[add|adc]+ [e]*sp', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "saveesp"
													addListBaseAddESP(saveq, numLines, NumOpsDis, modName)

												# addListBaseAddESP(save, lGoBack, NumOpsDis, modName)
											#EBP
											matchObj = re.match( r'^[add|adc]+ [dword|byte]* [ptr]* [\[]*[e]*bp|[add|adc]+ [e]*bp', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "saveebp"
													addListBaseAddEBP(saveq, numLines, NumOpsDis, modName)

												# addListBaseAddEBP(save, lGoBack, NumOpsDis, modName)
								except IndexError:
									pass

								#Searching for Sub operations
								try:
									matchObj = re.match( r'\bsub\b|\bsbb\b', val2[i-lGoBack], re.M|re.I)
									if matchObj: 
										#print "**sub**"
										#print val2[i-lGoBack]
										matchObj = re.match( r'^[sub|sbb]+ [byte|dword]+ ptr+ \[e[abcds]+[px]+ [+|-]+ 0x|^[sub|sbb]+ [byte|dword]+ ptr+ \[e[abcds][px] \+ 0x|^[sub|sbb]+ e[abcds][px], [dword|byte]+ ptr \[e[abcds][xp] \+ 0x|^[sub|sbb]+ [byte|dword]+ ptr \[eax\], [al|eax]+|^[sub|sbb]+ [byte|dword]+ ptr \[ebx\], [bl|bx]+|^[sub|sbb]+ [byte|dword]+ ptr \[ecx\], [cl|ecx]+|^[sub|sbb]+ [byte|dword]+ ptr \[edx\], [dl|edx]+|^[sub|sbb]+ eax, [dword|byte]+ ptr \[[e|a]+[a|l]+|^[sub|sbb]+ ebx, [dword|byte]+ ptr \[[e|b]+[b|l]+|^[sub|sbb]+ ecx, [dword|byte]+ ptr \[[e|c]+[c|l]+|^[sub|sbb]+ edx, [dword|byte]+ ptr \[[e|d]+[d|l]+|^[sub|sbb]+ edi, [dword|byte]+ ptr \[[e|d]+[d|i]+|^[sub|sbb]+ esi, [dword|byte]+ ptr \[[e|s]+[s|i]+|^[sub|sbb]+ ebp, [dword|byte]+ ptr \[[e|b]+[b|p]+|^[sub|sbb]+ esp, [dword|byte]+ ptr \[[e|s]+[s|p]+|^[sub|sbb]+ a[l|h]+, a[l|h]+|^[sub|sbb]+ b[l|h]+, b[l|h]+|^[sub|sbb]+ c[l|h]+, c[l|h]+|^[sub|sbb]+ d[l|h]+, d[l|h]+|^[sub|sbb]+ di, di|^[sub|sbb]+ si, si|^[sub|sbb]+ sp, sp|^[sub|sbb]+ bp, bp', val2[i-lGoBack], re.M|re.I)  
										if not matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseSub(saveq, numLines, NumOpsDis, modName)
											# addListBaseSub(save, lGoBack, NumOpsDis, modName) 
											#eax - saving add to specific registers -- far more useful.
											matchObj = re.match( r'^[sub|sbb]+ [dword|byte]* [ptr]* [\[]*[e]*a[x|l|h]*|[sub|sbb]+ [e]*a[x|l|h]', val2[i-lGoBack], re.M|re.I)
											if matchObj:										
												numLines= giveLineNum(val5,val2[i-lGoBack])				
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseSubEAX(saveq, numLines, NumOpsDis, modName)
												# addListBaseSubEAX(save, lGoBack, NumOpsDis, modName)
											
											#ebx
											matchObj = re.match( r'^[sub|sbb]+ [dword|byte]* [ptr]* [\[]*[e]*b[x|l|h]*|[sub|sbb]+ [e]*b[x|l|h]*', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseSubEBX(saveq, numLines, NumOpsDis, modName)
												# addListBaseSubEBX(save, lGoBack, NumOpsDis, modName)
											#ecx
											matchObj = re.match( r'^[sub|sbb]+ [dword|byte]* [ptr]* [\[]*[e]*c[x|l|h]*|[sub|sbb]+ [e]*c[x|l|h]*', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseSubECX(saveq, numLines, NumOpsDis, modName)
												# addListBaseSubECX(save, lGoBack, NumOpsDis, modName)
											#eDx
											matchObj = re.match( r'^[sub|sbb]+ [dword|byte]* [ptr]* [\[]*[e]*d[x|l|h]*|[sub|sbb]+ [e]*d[x|l|h]*', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseSubEDX(saveq, numLines, NumOpsDis, modName)
												# addListBaseSubEDX(save, lGoBack, NumOpsDis, modName)
											#ESI 
											matchObj = re.match( r'^[sub|sbb]+ [dword|byte]* [ptr]* [\[]*[e]*si|[sub|sbb]+ [e]*si', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseSubESI(saveq, numLines, NumOpsDis, modName)
												# addListBaseSubESI(save, lGoBack, NumOpsDis, modName)
											#EDI 
											matchObj = re.match( r'^[sub|sbb]+ [dword|byte]* [ptr]* [\[]*[e]*di|[sub|sbb]+ [e]*di', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseSubEDI(saveq, numLines, NumOpsDis, modName)
												# addListBaseSubEDI(save, lGoBack, NumOpsDis, modName)
											#esp
											matchObj = re.match( r'^[sub|sbb]+ [dword|byte]* [ptr]* [\[]*[e]*sp|[sub|sbb]+ [e]*sp', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseSubESP(saveq, numLines, NumOpsDis, modName)
												# addListBaseSubESP(save, lGoBack, NumOpsDis, modName)
											#EBP
											matchObj = re.match( r'^[sub|sbb]+ [dword|byte]* [ptr]* [\[]*[e]*bp|[sub|sbb]+ [e]*bp', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseSubEBP(saveq, numLines, NumOpsDis, modName)											
												# addListBaseSubEBP(save, lGoBack, NumOpsDis, modName)
								except IndexError:
									pass
								#Searching for Mul operations
								#Some of the imul instructions I do not think would be very typical for a normal program, but feasible as uninteded instructions.
								try: 
									matchObj = re.match( r'\bmul\b|\bmulb\b|\bmulw\b|\bmull\b|\bmulwl\b|\bmulbwl\b|\bimul\b|\bimulb\b|\bimulw\b|\bimull\b|\bimulwl\b|\bimulbwl\b', val2[i-lGoBack], re.M|re.I)
								
									if matchObj: 
										matchObj = re.match( r'^[mul|imul]+ [e]*ax, [e]*ax|^[mul|imul]+ [e]*bx, [e]*bx|^[mul|imul]+ [e]*cx, [e]*cx|^[mul|imul]+ [e]*dx, [e]*dx|^[mul|imul]+ [e]*di, [e]*di|^[mul|imul]+ [e]*si, [e]*si|^[mul|imul]+ [e]*bp, [e]*bp|^[mul|imul]+ [e]*sp, [e]*sp', val2[i-lGoBack], re.M|re.I)
										if not matchObj:

											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseMul(saveq, numLines, NumOpsDis, modName)


											#eax - saving add to specific registers -- far more useful.
											matchObj = re.match( r'^mul', val2[i-lGoBack], re.M|re.I)  # mul will save in edx : eax or dx: ax by default, so any would work
											if matchObj:
												matchObj = re.match( r'^imul', val2[i-lGoBack], re.M|re.I)
												if not matchObj:

													numLines= giveLineNum(val5,val2[i-lGoBack])
													z =stupidPreJ(val5, numLines)
													if z == True:
														# print "savem"
														addListBaseMulEAX(saveq, numLines, NumOpsDis, modName)
														addListBaseMulEDX(saveq, numLines, NumOpsDis, modName)
													# addListBaseMulEAX(save, lGoBack, NumOpsDis, modName)
													# addListBaseMulEDX(save, lGoBack, NumOpsDis, modName)
											
											matchObj = re.match( r'^imul[b|w|l]* [e]*[abcdsp]+[xbpi]+', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												matchObj = re.match( r'^imul[b|w|l]* [e]*[abcdsp]+[xbpi]+,', val2[i-lGoBack], re.M|re.I)
												if not matchObj:
													numLines= giveLineNum(val5,val2[i-lGoBack])
													z =stupidPreJ(val5, numLines)
													if z == True:
														# print "savem"
														addListBaseMulEAX(saveq, numLines, NumOpsDis, modName)
														addListBaseMulEDX(saveq, numLines, NumOpsDis, modName)


													# addListBaseMulEAX(save, lGoBack, NumOpsDis, modName)
													# addListBaseMulEDX(save, lGoBack, NumOpsDis, modName)

											matchObj = re.match( r'^imul[b|w|l]* [e]*ax, [e]*[abcdsp]+[xbpi]+, |^imul[b|w|l]* [e]*ax, [dword|byte]+ ptr \[[e]*[abcdsp]+[xbpi]+\], ', val2[i-lGoBack], re.M|re.I)
											if matchObj:

												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "savem"
													addListBaseMulEAX(saveq, numLines, NumOpsDis, modName)
												# addListBaseMulEAX(save, lGoBack, NumOpsDis, modName)

												#two operand form
											matchObj = re.match( r'^imul[b|w|l]* [e]*ax, [e]*[abcdsp]+[xbpi]+', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												matchObj = re.match( r'^imul[b|w|l]* [e]*ax, [e]*[abcdsp]+[xbpi]+,', val2[i-lGoBack], re.M|re.I)
												if not matchObj:
													numLines= giveLineNum(val5,val2[i-lGoBack])
													z =stupidPreJ(val5, numLines)
													if z == True:
														# print "savem"
														addListBaseMulEAX(saveq, numLines, NumOpsDis, modName)
													# addListBaseMulEAX(save, lGoBack, NumOpsDis, modName)

											#ebx
											matchObj = re.match( r'^imul[b|w|l]* [e]*bx, [e]*[abcdsp]+[xbpi]+, |^imul[b|w|l]* [e]*bx, [dword|byte]+ ptr \[[e]*[abcdsp]+[xbpi]+\], ', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "savem"
													addListBaseMulEBX(saveq, numLines, NumOpsDis, modName)
												# addListBaseMulEBX(save, lGoBack, NumOpsDis, modName)

											#two operand form
											matchObj = re.match( r'^imul[b|w|l]* [e]*bx, [e]*[abcdsp]+[xbpi]+', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												matchObj = re.match( r'^imul[b|w|l]* [e]*bx, [e]*[abcdsp]+[xbpi]+,', val2[i-lGoBack], re.M|re.I)
												if not matchObj:
													numLines= giveLineNum(val5,val2[i-lGoBack])
													z =stupidPreJ(val5, numLines)
													if z == True:
														# print "savem"
														addListBaseMulEBX(saveq, numLines, NumOpsDis, modName)
													# addListBaseMulEBX(save, lGoBack, NumOpsDis, modName)
											#ecx
											matchObj = re.match( r'^imul[b|w|l]* [e]*cx, [e]*[abcdsp]+[xbpi]+, |^imul[b|w|l]* [e]*cx, [dword|byte]+ ptr \[[e]*[abcdsp]+[xbpi]+\], ', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "savem"
													addListBaseMulECX(saveq, numLines, NumOpsDis, modName)
												# addListBaseMulECX(save, lGoBack, NumOpsDis, modName)

											#two operand form
											matchObj = re.match( r'^imul[b|w|l]* [e]*cx, [e]*[abcdsp]+[xbpi]+', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												matchObj = re.match( r'^imul[b|w|l]* [e]*cx, [e]*[abcdsp]+[xbpi]+,', val2[i-lGoBack], re.M|re.I)
												if not matchObj:
													numLines= giveLineNum(val5,val2[i-lGoBack])
													z =stupidPreJ(val5, numLines)
													if z == True:
														# print "savem"
														addListBaseMulECX(saveq, numLines, NumOpsDis, modName)
													# addListBaseMulECX(save, lGoBack, NumOpsDis, modName)
											#eDx
											matchObj = re.match( r'^imul[b|w|l]* [e]*dx, [e]*[abcdsp]+[xbpi]+, |^imul[b|w|l]* [e]*dx, [dword|byte]+ ptr \[[e]*[abcdsp]+[xbpi]+\], ', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "savem"
													addListBaseMulEDX(saveq, numLines, NumOpsDis, modName)

												# addListBaseMulEDX(save, lGoBack, NumOpsDis, modName)

											#two operand form
											matchObj = re.match( r'^imul[b|w|l]* [e]*dx, [e]*[abcdsp]+[xbpi]+', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												matchObj = re.match( r'^imul[b|w|l]* [e]*dx, [e]*[abcdsp]+[xbpi]+,', val2[i-lGoBack], re.M|re.I)
												if not matchObj:
													numLines= giveLineNum(val5,val2[i-lGoBack])
													z =stupidPreJ(val5, numLines)
													if z == True:
														# print "savem"
														addListBaseMulEDX(saveq, numLines, NumOpsDis, modName)
														# addListBaseMulEDX(save, lGoBack, NumOpsDis, modName)

											#ESI 
											matchObj = re.match( r'^imul[b|w|l]* [e]*si, [e]*[abcdsp]+[xbpi]+, |^imul[b|w|l]* [e]*si, [dword|byte]+ ptr \[[e]*[abcdsp]+[xbpi]+\], ', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "savem"
													addListBaseMulESI(saveq, numLines, NumOpsDis, modName)
												# addListBaseMulESI(save, lGoBack, NumOpsDis, modName)

											#two operand form
											matchObj = re.match( r'^imul[b|w|l]* [e]*si, [e]*[abcdsp]+[xbpi]+', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												matchObj = re.match( r'^imul[b|w|l]* [e]*si, [e]*[abcdsp]+[xbpi]+,', val2[i-lGoBack], re.M|re.I)
												if not matchObj:
													numLines= giveLineNum(val5,val2[i-lGoBack])
													z =stupidPreJ(val5, numLines)
													if z == True:
														# print "savem"
														addListBaseMulESI(saveq, numLines, NumOpsDis, modName)
														# addListBaseMulESI(save, lGoBack, NumOpsDis, modName)

											#EDI 
											matchObj = re.match( r'^imul[b|w|l]* [e]*di, [e]*[abcdsp]+[xbpi]+, |^imul[b|w|l]* [e]*di, [dword|byte]+ ptr \[[e]*[abcdsp]+[xbpi]+\], ', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "savem"
													addListBaseMulEDI(saveq, numLines, NumOpsDis, modName)
												# addListBaseMulEDI(save, lGoBack, NumOpsDis, modName)

											#two operand form
											matchObj = re.match( r'^imul[b|w|l]* [e]*di, [e]*[abcdsp]+[xbpi]+', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												matchObj = re.match( r'^imul[b|w|l]* [e]*di, [e]*[abcdsp]+[xbpi]+,', val2[i-lGoBack], re.M|re.I)
												if not matchObj:
													numLines= giveLineNum(val5,val2[i-lGoBack])
													z =stupidPreJ(val5, numLines)
													if z == True:
														# print "savem"
														addListBaseMulEDI(saveq, numLines, NumOpsDis, modName)
														# addListBaseMulEDI(save, lGoBack, NumOpsDis, modName)
											
											#esp
											matchObj = re.match( r'^imul[b|w|l]* [e]*sp, [e]*[abcdsp]+[xbpi]+, |^imul[b|w|l]* [e]*sp, [dword|byte]+ ptr \[[e]*[abcdsp]+[xbpi]+\], ', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												#addListBaseMulESP(save, lGoBack, NumOpsDis, modName)
												pass

											#two operand form
											matchObj = re.match( r'^imul[b|w|l]* [e]*sp, [e]*[abcdsp]+[xbpi]+', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												matchObj = re.match( r'^imul[b|w|l]* [e]*sp, [e]*[abcdsp]+[xbpi]+,', val2[i-lGoBack], re.M|re.I)
												if not matchObj:
													#addListBaseMulESP(save, lGoBack, NumOpsDis, modName)
													pass
											#EBP
											matchObj = re.match( r'^imul[b|w|l]* [e]*bp, [e]*[abcdsp]+[xbpi]+, |^imul[b|w|l]* [e]*bp, [dword|byte]+ ptr \[[e]*[abcdsp]+[xbpi]+\], ', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "savem"
													addListBaseMulEBP(saveq, numLines, NumOpsDis, modName)
												# addListBaseMulEBP(save, lGoBack, NumOpsDis, modName)

											#two operand form
											matchObj = re.match( r'^imul[b|w|l]* [e]*bp, [e]*[abcdsp]+[xbpi]+', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												matchObj = re.match( r'^imul[b|w|l]* [e]*bp, [e]*[abcdsp]+[xbpi]+,', val2[i-lGoBack], re.M|re.I)
												if not matchObj:
													numLines= giveLineNum(val5,val2[i-lGoBack])
													z =stupidPreJ(val5, numLines)
													if z == True:
														# print "savem"
														addListBaseMulEBP(saveq, numLines, NumOpsDis, modName)
													# addListBaseMulEBP(save, lGoBack, NumOpsDis, modName)
								except IndexError:
									pass

								#####DIV/IDIV


								try: 
									matchObj = re.match( r'\bdiv\b|\bdivb\b|\bdivw\b|\bdivl\b|\bdivwl|\bdivbwl\b|\bidiv\b|\bidivb\b|\bidivw\b|\bidivl\b|\bidivwl|\bidivbwl\b', val2[i-lGoBack], re.M|re.I)
								
									if matchObj: 
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											# print "saveDiv"
											addListBaseDiv(saveq, numLines, NumOpsDis, modName)
											addListBaseDivEAX(saveq, numLines, NumOpsDis, modName)
											addListBaseDivEDX(saveq, numLines, NumOpsDis, modName)
										# addListBaseDiv(save, lGoBack, NumOpsDis, modName)
										# addListBaseDivEAX(save, lGoBack, NumOpsDis, modName)
										# addListBaseDivEDX(save, lGoBack, NumOpsDis, modName)
								except IndexError:
									pass

								#searching for mov
								try: 
									matchObj = re.match( r'\bmov\b', val2[i-lGoBack], re.M|re.I)
								
									if matchObj: 
										matchObj = re.match( r'^mov [e]*a[x|l|h]+, [dword|byte]+ [ptr]* \[[e]*a[x|l|h]|^mov [e]*b[x|l|h]+, [dword|byte]+ [ptr]* \[[e]*b[x|l|h]*|^mov [e]*c[x|l|h]+, [dword|byte]+ [ptr]* \[[e]*c[x|l|h]*|^mov [e]*d[x|l|h]+, [dword|byte]+ [ptr]* \[[e]*d[x|l|h]*|^mov [e]*di, [dword|byte]+ [ptr]* \[[e]*di|^mov [e]*si, [dword|byte]+ [ptr]* \[[e]*si|^mov [e]*sp, [dword|byte]+ [ptr]* \[[e]*sp|^mov [e]*bp, [dword|byte]+ [ptr]* \[[e]*bp|mov [e]*a[x|l|h]+, [e]*a[x|l|h]+|mov [e]*b[x|l|h]+, [e]*b[x|l|h]+|mov [e]*c[x|l|h]+, [e]*c[x|l|h]+|mov [e]*d[x|l|h]+, [e]*d[x|l|h]+|mov [e]*di, [e]*di|mov [e]*si, [e]*si|mov [e]*bp, [e]*bp+|mov [e]*sp, [e]*sp|^mov [e]*a[x|l|h]+, [dword|byte]+ [ptr]* \[[e]*a[x|l|h] [+|-]+|^mov [dword|byte]+ ptr \[[e]*[abcdspb]+[x|l|h|i|p]+ [+|-]+ |^mov [e]*[abcdspb]+[x|l|h|i|p]+, [dword|byte]+ ptr \[0x|^mov [e]*a[x|l|h]+, [dword|byte]+ [ptr]* \[[e]*a[x|l|h]+ [+|-]+|^mov [e]*[abcdspb]+[x|l|h|i|p]+, es|^mov [e]*[abcdsb]+[x|l|h|p|i]+, [dword|byte]+ [ptr]* \[[e]*[abcdsb]+[x|l|h|p|i]+ [-|+]+ 0x[0-9]*', val2[i-lGoBack], re.M|re.I)
										if not matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												# print "savem"
												addListBaseMov(saveq, numLines, NumOpsDis, modName)
											# addListBaseMov(save, lGoBack, NumOpsDis, modName) 
											#eax - saving add to specific registers -- far more useful.
																					
											matchObj = re.match( r'^mov [e]*a[x|l|h]+|^mov [dword|byte]+ ptr \[[e]*a[x|l|h]+', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "savem"
													addListBaseMovEAX(saveq, numLines, NumOpsDis, modName)
												# addListBaseMovEAX(save, lGoBack, NumOpsDis, modName)
											#ebx
											matchObj = re.match( r'^mov [e]*b[x|l|h]+|^mov [dword|byte]+ ptr \[[e]*b[x|l|h]+', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "savem"
													addListBaseMovEBX(saveq, numLines, NumOpsDis, modName)
												# addListBaseMovEBX(save, lGoBack, NumOpsDis, modName)
											#ecx
											matchObj = re.match( r'^mov [e]*c[x|l|h]+|^mov [dword|byte]+ ptr \[[e]*c[x|l|h]+', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "savem"
													addListBaseMovECX(saveq, numLines, NumOpsDis, modName)
												# addListBaseMovECX(save, lGoBack, NumOpsDis, modName)
												
											#eDx
											matchObj = re.match( r'^mov [e]*d[x|l|h]+|^mov [dword|byte]+ ptr \[[e]*d[x|l|h]+', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "savem"
													addListBaseMovEDX(saveq, numLines, NumOpsDis, modName)
												# addListBaseMovEDX(save, lGoBack, NumOpsDis, modName)

											#ESI 
											matchObj = re.match( r'^mov [e]*si|^mov [dword|byte]+ ptr \[[e]*si', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "savem"
													addListBaseMovESI(saveq, numLines, NumOpsDis, modName)
												# addListBaseMovESI(save, lGoBack, NumOpsDis, modName)
											#EDI 
											matchObj = re.match( r'^mov [e]*di|^mov [dword|byte]+ ptr \[[e]*di', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "savem"
													addListBaseMovEDI(saveq, numLines, NumOpsDis, modName)
												# addListBaseMovEDI(save, lGoBack, NumOpsDis, modName)
											#esp
											matchObj = re.match( r'^mov [e]*sp|^mov [dword|byte]+ ptr \[[e]*sp', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "savem"
													addListBaseMovESP(saveq, numLines, NumOpsDis, modName)
												# addListBaseMovESP(save, lGoBack, NumOpsDis, modName)
											#EBP
											matchObj = re.match( r'^mov [e]*bp|^mov [dword|byte]+ ptr \[[e]*bp', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "savem"
													addListBaseMovEBP(saveq, numLines, NumOpsDis, modName)
												# addListBaseMovEBP(save, lGoBack, NumOpsDis, modName)
								except IndexError:
									pass

								#searching for lea
								try: 
									matchObj = re.match( r'\blea\b', val2[i-lGoBack], re.M|re.I)
								
									if matchObj: 
										matchObj = re.match( r'^lea [e]*a[x|l|h]+, [dword|byte]+ [ptr]* \[[e]*a[x|l|h]*|^lea [e]*b[x|l|h]+, [dword|byte]+ [ptr]* \[[e]*b[x|l|h]*|^lea [e]*c[x|l|h]+, [dword|byte]+ [ptr]* \[[e]*c[x|l|h]*|^lea [e]*d[x|l|h]+, [dword|byte]+ [ptr]* \[[e]*d[x|l|h]*|^lea [e]*di, [dword|byte]+ [ptr]* \[[e]*di|^lea [e]*si, [dword|byte]+ [ptr]* \[[e]*si|^lea [e]*sp, [dword|byte]+ [ptr]* \[[e]*sp|^lea [e]*bp, [dword|byte]+ [ptr]* \[[e]*bp|lea [e]*a[x|l|h]+, [e]*a[x|l|h]+|lea [e]*b[x|l|h]+, [e]*b[x|l|h]+|lea [e]*c[x|l|h]+, [e]*c[x|l|h]+|lea [e]*d[x|l|h]+, [e]*d[x|l|h]+|lea [e]*di, [e]*di|lea [e]*si, [e]*si|lea [e]*bp, [e]*bp+|lea [e]*sp, [e]*sp|^lea [e]*a[x|l|h]+, [dword|byte]+ [ptr]* \[[e]*a[x|l|h] [+|-]+|^lea [dword|byte]+ ptr \[[e]*[abcdspb]+[x|l|h|i|p]+ [+|-]+ |^lea [e]*[abcdspb]+[x|l|h|i|p]+, [dword|byte]+ ptr \[0x|^lea [e]*a[x|l|h]+, [dword|byte]+ [ptr]* \[[e]*a[x|l|h]+ [+|-]+|^lea [e]*[abcdspb]+[x|l|h|i|p]+, es|^lea [e]*[abcdspb]+[x|l|h|i|p]+, [dword|byte]+ [ptr]* \[[e]*[abcdspb]+[x|l|h|i|p]+ [+|-]+ [e]*[abcdspb]+[x|l|h|i|p]+\*', val2[i-lGoBack], re.M|re.I)
										if not matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseLea(saveq, numLines, NumOpsDis, modName)
											# addListBaseLea(save, lGoBack, NumOpsDis, modName) 
											#eax - saving add to specific registers -- far more useful.
											
											
											matchObj = re.match( r'^lea [e]*a[x|l|h]+|^lea [dword|byte]+ ptr \[[e]*a[x|l|h]', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseLeaEAX(saveq, numLines, NumOpsDis, modName)
												# addListBaseLeaEAX(save, lGoBack, NumOpsDis, modName)
											#ebx
											matchObj = re.match( r'^lea [e]*b[x|l|h]+|^lea [dword|byte]+ ptr \[[e]*b[x|l|h]', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseLeaEBX(saveq, numLines, NumOpsDis, modName)
												# addListBaseLeaEBX(save, lGoBack, NumOpsDis, modName)
											#ecx
											matchObj = re.match( r'^lea [e]*c[x|l|h]+|^lea [dword|byte]+ ptr \[[e]*c[x|l|h]', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseLeaECX(saveq, numLines, NumOpsDis, modName)
												# addListBaseLeaECX(save, lGoBack, NumOpsDis, modName)
											#eDx
											matchObj = re.match( r'^lea [e]*d[x|l|h]+|^lea [dword|byte]+ ptr \[[e]*d[x|l|h]', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseLeaEDX(saveq, numLines, NumOpsDis, modName)
												# addListBaseLeaEDX(save, lGoBack, NumOpsDis, modName)

											#ESI 
											matchObj = re.match( r'^lea [e]*si|^lea [dword|byte]+ ptr \[[e]*si', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseLeaESI(saveq, numLines, NumOpsDis, modName)
												# addListBaseLeaESI(save, lGoBack, NumOpsDis, modName)
											#EDI 
											matchObj = re.match( r'^lea [e]*di|^lea [dword|byte]+ ptr \[[e]*di', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												# print "leaedi enter"
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													# print "leaedi true"
													addListBaseLeaEDI(saveq, numLines, NumOpsDis, modName)
												# addListBaseLeaEDI(save, lGoBack, NumOpsDis, modName)
											#esp
											matchObj = re.match( r'^lea [e]*sp|^lea [dword|byte]+ ptr \[[e]*sp', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseLeaESP(saveq, numLines, NumOpsDis, modName)
												# addListBaseLeaESP(save, lGoBack, NumOpsDis, modName)
											#EBP
											matchObj = re.match( r'^lea [e]*bp|^lea [dword|byte]+ ptr \[[e]*bp', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseLeaEBP(saveq, numLines, NumOpsDis, modName)
												# addListBaseLeaEBP(save, lGoBack, NumOpsDis, modName)
								except IndexError:
									pass
								#

								#mov shuffle
								try: 
									matchObj = re.match( r'\bmov\b', val2[i-lGoBack], re.M|re.I)
								
									if matchObj: 
										matchObj = re.match( r'^mov [e]*a[x|l]+, [dword|byte]+ [ptr]* \[[e]*a[x|l|h]*|^mov [e]*b[x|l]+, [dword|byte]+ [ptr]* \[[e]*b[x|l|h]*|^mov [e]*c[x|l]+, [dword|byte]+ [ptr]* \[[e]*c[x|l|h]*|^mov [e]*d[x|l|h]+, [dword|byte]+ [ptr]* \[[e]*d[x|l|h]*|^mov [e]*di, [dword|byte]+ [ptr]* \[[e]*di|^mov [e]*si, [dword|byte]+ [ptr]* \[[e]*si|^mov [e]*sp, [dword|byte]+ [ptr]* \[[e]*sp|^mov [e]*bp, [dword|byte]+ [ptr]* \[[e]*bp|mov [e]*a[x|l]+, [e]*a[x|l|h]+|mov [e]*b[x|l]+, [e]*b[x|l|h]+|mov [e]*c[x|l|h]+, [e]*c[x|l|h]+|mov [e]*d[x|l]+, [e]*d[x|l|h]+|mov [e]*di, [e]*di|mov [e]*si, [e]*si|mov [e]*bp, [e]*bp+|mov [e]*sp, [e]*sp|^mov [e]*a[x|l]+, [dword|byte]+ [ptr]* \[[e]*a[x|l|h] [+|-]+|^mov [dword|byte]+ ptr \[[e]*[abcdspb]+[x|l|h|i|p]+ [+|-]+ |^mov [e]*[abcdspb]+[x|l|i|p]+, [dword|byte]+ ptr \[0x|^mov [e]*a[x|l]+, [dword|byte]+ [ptr]* \[[e]*a[x|l|h]+ [+|-]+|^mov [e]*[abcdspb]+[x|l|i|p]+, es', val2[i-lGoBack], re.M|re.I)
										if not matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseMovShuf(saveq, numLines, NumOpsDis, modName)
												# addListBaseMovShuf(save, lGoBack, NumOpsDis, modName) 

											#eax - saving add to specific registers -- far more useful.
																					
											matchObj = re.match( r'^mov [e]*a[x|l]+, [e]*[abcdspb]+[x|l|h|i|p]+', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseMovShufEAX(saveq, numLines, NumOpsDis, modName)
												# addListBaseMovShufEAX(save, lGoBack, NumOpsDis, modName)
											#ebx
											matchObj = re.match( r'^mov [e]*b[x|l]+, [e]*[abcdspb]+[x|l|h|i|p]+', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseMovShufEBX(saveq, numLines, NumOpsDis, modName)
												# addListBaseMovShufEBX(save, lGoBack, NumOpsDis, modName)
											#ecx
											matchObj = re.match( r'^mov [e]*c[x|l]+, [e]*[abcdspb]+[x|l|h|i|p]+', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseMovShufECX(saveq, numLines, NumOpsDis, modName)
												# addListBaseMovShufECX(save, lGoBack, NumOpsDis, modName)
											#eDx
											matchObj = re.match( r'^mov [e]*d[x|l]+, [e]*[abcdspb]+[x|l|h|i|p]+', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseMovShufEDX(saveq, numLines, NumOpsDis, modName)
												# addListBaseMovShufEDX(save, lGoBack, NumOpsDis, modName)

											#ESI 
											matchObj = re.match( r'^mov [e]*si, [e]*[abcdspb]+[x|l|h|i|p]+', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseMovShufESI(saveq, numLines, NumOpsDis, modName)
												# addListBaseMovShufESI(save, lGoBack, NumOpsDis, modName)
											#EDI 
											matchObj = re.match( r'^mov [e]*di, [e]*[abcdspb]+[x|l|h|i|p]+', val2[i-lGoBack], re.M|re.I)
											
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseMovShufEDI(saveq, numLines, NumOpsDis, modName)
												# addListBaseMovShufEDI(save, lGoBack, NumOpsDis, modName)
											#esp
											matchObj = re.match( r'^mov [e]*sp, [e]*[abcdspb]+[x|l|h|i|p]+', val2[i-lGoBack], re.M|re.I)
											if matchObj:									
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseMovShufESP(saveq, numLines, NumOpsDis, modName)
												# addListBaseMovShufESP(save, lGoBack, NumOpsDis, modName)
											#EBP
											matchObj = re.match( r'^mov [e]*bp, [e]*[abcdspb]+[x|l|h|i|p]+', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseMovShufEBP(saveq, numLines, NumOpsDis, modName)
												# addListBaseMovShufEBP(save, lGoBack, NumOpsDis, modName)
								except IndexError:
									pass

								#mov value into registers
								try: 
									matchObj = re.match( r'\bmov\b', val2[i-lGoBack], re.M|re.I)
								
									if matchObj: 
										matchObj = re.match( r'^mov [e]*a[x|l]+, [dword|byte]+ [ptr]* \[[e]*a[x|l|h]*|^mov [e]*b[x|l]+, [dword|byte]+ [ptr]* \[[e]*b[x|l|h]*|^mov [e]*c[x|l]+, [dword|byte]+ [ptr]* \[[e]*c[x|l|h]*|^mov [e]*d[x|l|h]+, [dword|byte]+ [ptr]* \[[e]*d[x|l|h]*|^mov [e]*di, [dword|byte]+ [ptr]* \[[e]*di|^mov [e]*si, [dword|byte]+ [ptr]* \[[e]*si|^mov [e]*sp, [dword|byte]+ [ptr]* \[[e]*sp|^mov [e]*bp, [dword|byte]+ [ptr]* \[[e]*bp|mov [e]*a[x|l]+, [e]*a[x|l|h]+|mov [e]*b[x|l]+, [e]*b[x|l|h]+|mov [e]*c[x|l|h]+, [e]*c[x|l|h]+|mov [e]*d[x|l]+, [e]*d[x|l|h]+|mov [e]*di, [e]*di|mov [e]*si, [e]*si|mov [e]*bp, [e]*bp+|mov [e]*sp, [e]*sp|^mov [e]*a[x|l]+, [dword|byte]+ [ptr]* \[[e]*a[x|l|h] [+|-]+|^mov [dword|byte]+ ptr \[[e]*[abcdspb]+[x|l|h|i|p]+ [+|-]+ |^mov [e]*[abcdspb]+[x|l|i|p]+, [dword|byte]+ ptr \[0x|^mov [e]*a[x|l]+, [dword|byte]+ [ptr]* \[[e]*a[x|l|h]+ [+|-]+|^mov [e]*[abcdspb]+[x|l|i|p]+, es', val2[i-lGoBack], re.M|re.I)
										if not matchObj:

											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseMovVal(saveq, numLines, NumOpsDis, modName)
												# addListBaseMovVal(save, lGoBack, NumOpsDis, modName) 

											#eax - saving add to specific registers -- far more useful.
																					
											matchObj = re.match( r'^mov [e]*a[x|l]+, [0x]*[0-9]+', val2[i-lGoBack], re.M|re.I)
											if matchObj:

												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseMovValEAX(saveq, numLines, NumOpsDis, modName)
												# addListBaseMovValEAX(save, lGoBack, NumOpsDis, modName)
											#ebx
											matchObj = re.match( r'^mov [e]*b[x|l]+, [0x]*[0-9]+', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseMovValEBX(saveq, numLines, NumOpsDis, modName)
												# addListBaseMovValEBX(save, lGoBack, NumOpsDis, modName)
											#ecx
											matchObj = re.match( r'^mov [e]*c[x|l]+, [0x]*[0-9]+', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseMovValECX(saveq, numLines, NumOpsDis, modName)
												# addListBaseMovValECX(save, lGoBack, NumOpsDis, modName)
											#eDx
											matchObj = re.match( r'^mov [e]*d[x|l]+, [0x]*[0-9]+', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseMovValEDX(saveq, numLines, NumOpsDis, modName)
												# addListBaseMovValEDX(save, lGoBack, NumOpsDis, modName)

											#ESI 
											matchObj = re.match( r'^mov [e]*si, [0x]*[0-9]+', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseMovValESI(saveq, numLines, NumOpsDis, modName)
												# addListBaseMovValESI(save, lGoBack, NumOpsDis, modName)
											#EDI 
											matchObj = re.match( r'^mov [e]*di, [0x]*[0-9]+', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseMovValEDI(saveq, numLines, NumOpsDis, modName)
												# addListBaseMovValEDI(save, lGoBack, NumOpsDis, modName)
											#esp
											matchObj = re.match( r'^mov [e]*sp, [0x]*[0-9]+', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseMovValESP(saveq, numLines, NumOpsDis, modName)
												# addListBaseMovValESP(save, lGoBack, NumOpsDis, modName)
											#EBP
											matchObj = re.match( r'^mov [e]*bp, [0x]*[0-9]+', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseMovValEBP(saveq, numLines, NumOpsDis, modName)
												# addListBaseMovValEBP(save, lGoBack, NumOpsDis, modName)
								except IndexError:
									pass

							#now5
								
								try:
									matchObj = re.match( r'^mov dword ptr \[[e]*[abcdspbixfs]*\], [e]*[acbdps]+[x|p|i]+|^mov \[[e]*[abcdspbixfs]*\], [e]*[acbdps]+[x|p|i]+', val2[i-lGoBack], re.M|re.I)
									if matchObj:
										# print "magicalDeref"
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListMovDeref(saveq, numLines, NumOpsDis, modName)

										matchObj = re.match( r'^mov dword ptr \[[e]*a[x|l]+\], [e]*[cdspb]+[x|i|p]+|^mov dword ptr \[[e]*a[x|l]+\], [e]*[cdspb]+[x|i|p]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListMovDerefEAX(saveq, numLines, NumOpsDis, modName)


										matchObj = re.match( r'^mov dword ptr \[[e]*b[x|l]+\], [e]*[acdsp]+[x|i|p]+|^mov dword ptr \[[e]*b[x|l]+\], [e]*[acdsp]+[x|i|p]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListMovDerefEBX(saveq, numLines, NumOpsDis, modName)


										matchObj = re.match( r'^mov dword ptr \[[e]*c[x|l]+\], [e]*[adspb]+[x|i|p]+|^mov dword ptr \[[e]*c[x|l]+\], [e]*[adspb]+[x|i|p]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListMovDerefECX(saveq, numLines, NumOpsDis, modName)

										matchObj = re.match( r'^mov dword ptr \[[e]*d[x|l]+\], [e]*[acspb]+[x|i|p]+|^mov dword ptr \[[e]*d[x|l]+\], [e]*[acspb]+[x|i|p]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListMovDerefEDX(saveq, numLines, NumOpsDis, modName)
										matchObj = re.match( r'^mov dword ptr \[[e]*di+\], [e]*[acdspb]+[x|p]+ |^mov dword ptr \[[e]*di+\], esi|^mov \[[e]*di+\], [e]*[acdspb]+[x|p]+ |^mov \[[e]*di+\], esi', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListMovDerefEDI(saveq, numLines, NumOpsDis, modName)

										matchObj = re.match( r'^mov dword ptr \[[e]*si+\], [e]*[acsspb]+[x|p]+ |^mov dword ptr \[[e]*si+\], edi|^mov \[[e]*si+\], [e]*[acsspb]+[x|p]+ |^mov \[[e]*si+\], edi', val2[i-lGoBack], re.M|re.I)
										if matchObj:		
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListMovDerefESI(saveq, numLines, NumOpsDis, modName)
										matchObj = re.match( r'^mov dword ptr \[[e]*bp+\], [e]*[acsp]+[x|p|i]+ |^mov dword ptr \[[e]*bp+\], edi|^mov \[[e]*bp+\], [e]*[acsp]+[x|p|i]+ |^mov \[[e]*bp+\], edi', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListMovDerefEBP(saveq, numLines, NumOpsDis, modName)
										matchObj = re.match( r'^mov dword ptr \[[e]*sp+\], [e]*[acbp]+[x|p|i]+ |^mov dword ptr \[[e]*sp+\], esi|^mov \[[e]*sp+\], [e]*[acbp]+[x|p|i]+ |^mov \[[e]*sp+\], esi', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListMovDerefESP(saveq, numLines, NumOpsDis, modName)

								except:
									pass

								#searching for Push
								try: 
									matchObj = re.match( r'\bpush\b', val2[i-lGoBack], re.M|re.I)
								
									if matchObj: 
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListBasePush(saveq, numLines, NumOpsDis, modName)
										# addListBasePush(save, lGoBack, NumOpsDis, modName) 
										#eax - saving add to specific registers -- far more useful.	
										matchObj = re.match( r'^push [e]*a[x|l|h]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBasePushEAX(saveq, numLines, NumOpsDis, modName)
											# addListBasePushEAX(save, lGoBack, NumOpsDis, modName)
										#ebx
										matchObj = re.match( r'^push [e]*b[x|l|h]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBasePushEBX(saveq, numLines, NumOpsDis, modName)
											# addListBasePushEBX(save, lGoBack, NumOpsDis, modName)
										#ecx
										matchObj = re.match( r'^push [e]*c[x|l|h]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBasePushECX(saveq, numLines, NumOpsDis, modName)
											# addListBasePushECX(save, lGoBack, NumOpsDis, modName)
										#eDx
										matchObj = re.match( r'^push [e]*d[x|l|h]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBasePushEDX(saveq, numLines, NumOpsDis, modName)
											# addListBasePushEDX(save, lGoBack, NumOpsDis, modName)
										#ESI 
										matchObj = re.match( r'^push [e]*si', val2[i-lGoBack], re.M|re.I)
										if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBasePushESI(saveq, numLines, NumOpsDis, modName)
											# addListBasePushESI(save, lGoBack, NumOpsDis, modName)
										#EDI 
										matchObj = re.match( r'^push [e]*di', val2[i-lGoBack], re.M|re.I)
										if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBasePushEDI(saveq, numLines, NumOpsDis, modName)
											# addListBasePushEDI(save, lGoBack, NumOpsDis, modName)
										#esp
										matchObj = re.match( r'^push [e]*sp', val2[i-lGoBack], re.M|re.I)
										if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBasePushESP(saveq, numLines, NumOpsDis, modName)
											# addListBasePushESP(save, lGoBack, NumOpsDis, modName)
										#EBP
										matchObj = re.match( r'^push [e]*bp', val2[i-lGoBack], re.M|re.I)
										if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBasePushEBP(saveq, numLines, NumOpsDis, modName)
											# addListBasePushEBP(save, lGoBack, NumOpsDis, modName)					
								except IndexError:
									pass
								#searching for Pop
								try: 
									matchObj = re.match( r'\bpop\b', val2[i-lGoBack], re.M|re.I)
									if matchObj: 
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListBasePop(saveq, numLines, NumOpsDis, modName)										#eax - saving add to specific registers -- far more useful.
										
										matchObj = re.match( r'^pop [e]*a[x|l|h]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBasePopEAX(saveq, numLines, NumOpsDis, modName)

											# addListBasePopEAX(save, lGoBack, NumOpsDis, modName)
										#ebx
										matchObj = re.match( r'^pop [e]*b[x|l|h]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBasePopEBX(saveq, numLines, NumOpsDis, modName)

											# addListBasePopEBX(save, lGoBack, NumOpsDis, modName)
										#ecx
										matchObj = re.match( r'^pop [e]*c[x|l|h]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBasePopECX(saveq, numLines, NumOpsDis, modName)

											# addListBasePopECX(save, lGoBack, NumOpsDis, modName)
										#eDx
										matchObj = re.match( r'^pop [e]*d[x|l|h]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBasePopEDX(saveq, numLines, NumOpsDis, modName)

											# addListBasePopEDX(save, lGoBack, NumOpsDis, modName)
										#ESI 
										matchObj = re.match( r'^pop [e]*si', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBasePopESI(saveq, numLines, NumOpsDis, modName)

											# addListBasePopESI(save, lGoBack, NumOpsDis, modName)
										#EDI 
										matchObj = re.match( r'^pop [e]*di', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBasePopEDI(saveq, numLines, NumOpsDis, modName)

											# addListBasePopEDI(save, lGoBack, NumOpsDis, modName)
										#esp
										matchObj = re.match( r'^pop [e]*sp', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBasePopESP(saveq, numLines, NumOpsDis, modName)

											# addListBasePopESP(save, lGoBack, NumOpsDis, modName)
										#EBP
										matchObj = re.match( r'^pop [e]*bp', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBasePopEBP(saveq, numLines, NumOpsDis, modName)

											# addListBasePopEBP(save, lGoBack, NumOpsDis, modName)					
								except IndexError:
									pass
								

								try: 
									matchObj = re.match( r'\binc\b', val2[i-lGoBack], re.M|re.I)
									if matchObj: 
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListBaseInc(saveq, numLines, NumOpsDis, modName)
										# addListBaseInc(save, lGoBack, NumOpsDis, modName) 
										#eax - saving add to specific registers -- far more useful.	
										matchObj = re.match( r'^inc [e]*a[x|l|h]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseIncEAX(saveq, numLines, NumOpsDis, modName)
											# addListBaseIncEAX(save, lGoBack, NumOpsDis, modName)
										#ebx
										matchObj = re.match( r'^inc [e]*b[x|l|h]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseIncEBX(saveq, numLines, NumOpsDis, modName)
											# addListBaseIncEBX(save, lGoBack, NumOpsDis, modName)
										#ecx
										matchObj = re.match( r'^inc [e]*c[x|l|h]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseIncECX(saveq, numLines, NumOpsDis, modName)
											# addListBaseIncECX(save, lGoBack, NumOpsDis, modName)
										#eDx
										matchObj = re.match( r'^inc [e]*d[x|l|h]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseIncEDX(saveq, numLines, NumOpsDis, modName)
											# addListBaseIncEDX(save, lGoBack, NumOpsDis, modName)
										#ESI 
										matchObj = re.match( r'^inc [e]*si', val2[i-lGoBack], re.M|re.I)
										if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseIncESI(saveq, numLines, NumOpsDis, modName)
											# addListBaseIncESI(save, lGoBack, NumOpsDis, modName)
										#EDI 
										matchObj = re.match( r'^inc [e]*di', val2[i-lGoBack], re.M|re.I)
										if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseIncEDI(saveq, numLines, NumOpsDis, modName)
											# addListBaseIncEDI(save, lGoBack, NumOpsDis, modName)
										#esp
										matchObj = re.match( r'^inc [e]*sp', val2[i-lGoBack], re.M|re.I)
										if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseIncESP(saveq, numLines, NumOpsDis, modName)
											# addListBaseIncESP(save, lGoBack, NumOpsDis, modName)
										#EBP
										matchObj = re.match( r'^inc [e]*bp', val2[i-lGoBack], re.M|re.I)
										if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseIncEBP(saveq, numLines, NumOpsDis, modName)
											# addListBaseIncEBP(save, lGoBack, NumOpsDis, modName)					
								except IndexError:
									pass
								#searching for Dec
								try: 
									matchObj = re.match( r'\bdec\b', val2[i-lGoBack], re.M|re.I)
									if matchObj: 
										numLines= giveLineNum(val5,val2[i-lGoBack])
										z =stupidPreJ(val5, numLines)
										if z == True:
											addListBaseDec(saveq, numLines, NumOpsDis, modName)
										# addListBaseDec(save, lGoBack, NumOpsDis, modName) 
										#eax - saving add to specific registers -- far more useful.	
										matchObj = re.match( r'^dec [e]*a[x|l|h]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseDecEAX(saveq, numLines, NumOpsDis, modName)
											# addListBaseDecEAX(save, lGoBack, NumOpsDis, modName)
										#ebx
										matchObj = re.match( r'^dec [e]*b[x|l|h]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseDecEBX(saveq, numLines, NumOpsDis, modName)
											# addListBaseDecEBX(save, lGoBack, NumOpsDis, modName)
										#ecx
										matchObj = re.match( r'^dec [e]*c[x|l|h]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseDecECX(saveq, numLines, NumOpsDis, modName)
										# addListBaseDecECX(save, lGoBack, NumOpsDis, modName)
										#eDx
										matchObj = re.match( r'^dec [e]*d[x|l|h]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseDecEDX(saveq, numLines, NumOpsDis, modName)
											# addListBaseDecEDX(save, lGoBack, NumOpsDis, modName)
										#ESI 
										matchObj = re.match( r'^dec [e]*si', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseDecESI(saveq, numLines, NumOpsDis, modName)
											# addListBaseDecESI(save, lGoBack, NumOpsDis, modName)
										#EDI 
										matchObj = re.match( r'^dec [e]*di', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseDecEDI(saveq, numLines, NumOpsDis, modName)
											# addListBaseDecEDI(save, lGoBack, NumOpsDis, modName)
										#esp
										matchObj = re.match( r'^dec [e]*sp', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseDecESP(saveq, numLines, NumOpsDis, modName)
											# addListBaseDecESP(save, lGoBack, NumOpsDis, modName)
										#EBP
										matchObj = re.match( r'^dec [e]*bp', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseDecEBP(saveq, numLines, NumOpsDis, modName)
										# addListBaseDecEBP(save, lGoBack, NumOpsDis, modName)					
								except IndexError:
									pass
								#searching for Xchg
								
								try: 	
									matchObj = re.match( r'\bxchg\b', val2[i-lGoBack], re.M|re.I)
									if matchObj:
										matchObj = re.match( r'^xchg eax, eax|^xchg ebx, ebx|^xchg ecx, ecx|^xchg edx, edx|^xchg esi, esi|^xchg edi, edi|^xchg esp, esp|^xchg ebp, ebp|^xchg ax, ax|^xchg bx, bx|^xchg cx, cx|^xchg dx, dx|^xchg si, si|^xchg di, di|^xchg sp, sp|^xchg bp, bp|^xchg al, al|^xchg bl, bl|^xchg cl, cl|^xchg dl, dl', val2[i-lGoBack], re.M|re.I)
									
										if not matchObj: 
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseXchg(saveq, numLines, NumOpsDis, modName)
											# addListBaseXchg(save, lGoBack, NumOpsDis, modName) 
											#eax - saving add to specific registers -- far more useful.				
											matchObj = re.match( r'^xchg eax, e[abcdsb]+[xspi]+|^xchg e[abcdsb]+[xspi]+, eax|^xchg ax, [abcdsb]+[xspi]+|^xchg [abcdsb]+[xspi]+, ax', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseXchgEAX(saveq, numLines, NumOpsDis, modName)
												# addListBaseXchgEAX(save, lGoBack, NumOpsDis, modName)

											#ebx
											matchObj = re.match( r'^xchg ebx, e[abcdsb]+[xspi]+|^xchg e[abcdsb]+[xspi]+, ebx|^xchg bx, [abcdsb]+[xspi]+|^xchg [abcdsb]+[xspi]+, bx', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseXchgEBX(saveq, numLines, NumOpsDis, modName)
												# addListBaseXchgEBX(save, lGoBack, NumOpsDis, modName)
											#ecx
											matchObj = re.match( r'^xchg ecx, e[abcdsb]+[xspi]+|^xchg e[abcdsb]+[xspi]+, ecx|^xchg cx, [abcdsb]+[xspi]+|^xchg [abcdsb]+[xspi]+, cx', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseXchgECX(saveq, numLines, NumOpsDis, modName)
												# addListBaseXchgECX(save, lGoBack, NumOpsDis, modName)
											#eDx
											matchObj = re.match( r'^xchg edx, e[abcdsb]+[xspi]+|^xchg e[abcdsb]+[xspi]+, edx|^xchg dx, [abcdsb]+[xspi]+|^xchg [abcdsb]+[xspi]+, dx', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseXchgEDX(saveq, numLines, NumOpsDis, modName)
												# addListBaseXchgEDX(save, lGoBack, NumOpsDis, modName)
											#ESI 
											matchObj = re.match( r'^xchg esi, e[abcdsb]+[xspi]+|^xchg e[abcdsb]+[xspi]+, esi|^xchg si, [abcdsb]+[xspi]+|^xchg [abcdsb]+[xspi]+, si', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseXchgESI(saveq, numLines, NumOpsDis, modName)
												# addListBaseXchgESI(save, lGoBack, NumOpsDis, modName)
											#EDI 
											matchObj = re.match( r'^xchg edi, e[bcdsb]+[xspi]+|^xchg e[abcdsb]+[xspi]+, edi|^xchg di, [abcdsb]+[xspi]+|^xchg [abcdsb]+[xspi]+, di', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseXchgEDI(saveq, numLines, NumOpsDis, modName)
												# addListBaseXchgEDI(save, lGoBack, NumOpsDis, modName)
											#esp
											matchObj = re.match( r'^xchg esp, e[abcdsb]+[xspi]+|^xchg e[abcdsb]+[xspi]+, esp|^xchg sp, [abcdsb]+[xspi]+|^xchg [abcdsb]+[xspi]+, sp', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseXchgESP(saveq, numLines, NumOpsDis, modName)
												# addListBaseXchgESP(save, lGoBack, NumOpsDis, modName)
											#EBP
											matchObj = re.match( r'^xchg ebp, e[abcdsb]+[xspi]+|^xchg e[abcdsb]+[xspi]+, ebp|^xchg bp, [abcdsb]+[xspi]+|^xchg [abcdsb]+[xspi]+, bp', val2[i-lGoBack], re.M|re.I)
											if matchObj:
												numLines= giveLineNum(val5,val2[i-lGoBack])
												z =stupidPreJ(val5, numLines)
												if z == True:
													addListBaseXchgEBP(saveq, numLines, NumOpsDis, modName)
												# addListBaseXchgEBP(save, lGoBack, NumOpsDis, modName)					
								except IndexError:
									pass
								#now7	
								#searching for Shift Left
								#not common, so no need to do by specific regs
								try: 
									matchObj = re.match( r'^s[a|h]l+[dwl]* [dword|byte]+ [ptr]* \[[e]*[abcdspb]+[x|l|h|i|p]+ [+|-]+|^salc ', val2[i-lGoBack], re.M|re.I)
									if not matchObj:
										matchObj = re.match( r'^shl|^sal', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseShiftLeft(saveq, numLines, NumOpsDis, modName)
											# addListBaseShiftLeft(save, lGoBack, NumOpsDis, modName)
								except IndexError:
									pass
									#Shift Right
									#not common, so no need to do by specific regs
								try: 
									matchObj = re.match( r'^s[a|h]+r[dwl]* [dword|byte]+ [ptr]* \[[e]*[abcdspb]+[x|l|h|i|p]+ [+|-]+|^salc ', val2[i-lGoBack], re.M|re.I)
									if not matchObj:	
										matchObj = re.match( r'^shr|^sar', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseShiftLeft(saveq, numLines, NumOpsDis, modName)
											# addListBaseShiftRight(save, lGoBack, NumOpsDis, modName)
								except IndexError:
									pass
									#Rotate Left 
									#not common, so no need to do by specific regs
								try: 
									matchObj = re.match( r'^r[o|c]+l [dword|byte]+ [ptr]* \[[e]*[abcdspb]+[x|l|h|i|p]+ [+|-]+ ', val2[i-lGoBack], re.M|re.I)
									if not matchObj:
										matchObj = re.match( r'^rol|^rcl', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseShiftLeft(saveq, numLines, NumOpsDis, modName)
											# addListBaseRotLeft(save, lGoBack, NumOpsDis, modName)
								except IndexError:
									pass
									#Rotate Right
									#not common, so no need to do by specific regs
								try: 
									matchObj = re.match( r'^r[o|c]+r [dword|byte]+ [ptr]* \[[e]*[abcdspb]+[x|l|h|i|p]+ [+|-]+ ', val2[i-lGoBack], re.M|re.I)
									if not matchObj:	
										matchObj = re.match( r'^ror|^rcr', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListBaseShiftLeft(saveq, numLines, NumOpsDis, modName)
											# addListBaseRotRight(save, lGoBack, NumOpsDis, modName)
								except IndexError:
									pass
								#done
								lGoBack -= 1
	


def disHereJMPPTR(address, NumOpsDis, Reg):
	#print "ok2"
	#print  hex(int(address))
	sp()
	global o
	w=0
	CODED2 = b""

	x = NumOpsDis
	for i in range (x, 0, -1):
		CODED2 += objs[o].data2[address-i]
	CODED2 += objs[o].data2[address]
	CODED2 += objs[o].data2[address+1]
	CODED2 += b"\x00"

	val =""
	val2 = []
	val3 = []
	address2 = address + objs[o].startLoc + 1000
	for i in cs.disasm(CODED2, address-x):
		add = hex(int(i.address))
		addb = hex(int(i.address +  objs[o].VirtualAdd))
		add2 = str(add)
		add3 = hex (int(i.address + objs[o].startLoc	))
		add4 = str(add3)
		val =  i.mnemonic + " " + i.op_str + "\t\t\t\t"  + add4 + " (offset " + addb + ")\n"
		val2.append(val)
		val3.append(add2)
		#print val

# My method is to to detect if there is a ret, jmp or call in the gadget. If I find it, I cut out the offending lines and any leading up to it, leaving only safe gadgets that terminate in a jmp or call. The solution is a reversed for loop with enum and checking to see if jmp or call appears before the end of the gadget. If I do, I excise that line and all above it.  when I intially locate a desired sequence, e.g. jmp eax, I then capture the lines immediately before it. This is a way to ensure  that instructions petaining to control flow are not in the gadget.

	tz = val2.__len__()
	tk=0
	save=0x00
	# I need to iterate through this in reverse, starting with the jmp ptr [reg].  I contains index number and e is to enumerate, i.e. show what the value is. In this case, it is iterating through an array of  strings containing the disasembly. The goal is ultimately to cut this down by removing other control flow instructions. The end result will be I will know the address of the jmp [reg] and how many lines  to go back without encountering a control flow instruction.
	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__() 
		if tk < 1:
			save = val3[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1

		# Use regular expressions to find lines that have control flow and other undesired instructions, so they and preceding lines can be excised. 
		matchObj2 = re.compile( r"\bjo\b|\bjno\b|\bjsn\b|\bjs\b|\bje\b|\bjz\b|\bjne\b|\bjnz\b|\bjb\b|\bjnae\b|\bjc\b|\bjnb\bjae\b|\bjnc\b|\bjbe\bjna\b|\bja\b|\bjnben\b|\bjl\b|\bjnge\b|\bjge\bjnl\b|\bjle\b|\bjng\bjg\b|\bjnle\b|\bjp\b|\bjpe\b|\bjnp\b|\bjpo\bjczz\b|\bjecxz\b|\bcall\b|\bint\b|\bdb\b", re.M|re.I)
		if re.findall(matchObj2, e):   #if "ret"  in e:
			if i != 1:
				if i > val2.__len__():
					break  # Gracefully break on unusual cases
				else:
					try: 
						del val2[i]
						del val3[i]
					except IndexError:
						pass
				i = i-1
				while i <= (val2.__len__()):
					if i <0:
						break
					else:
						del val2[i]	
						del val3[i]
						i=i-1
						if i == (val2.__len__()-1):
							break
	tz = val2.__len__()
	tk=0
	save=0
	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = val3[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1
# Here I search for excise ret's from JOP gadget. I had tried to incorporate this functionality into the
# above, but I would run into test cases that would cause errors. This seemed the best solution, even if
# inelegant.
		matchObj2 = re.compile( r"\bret\b", re.M|re.I)
		if re.findall(matchObj2, e):   #if "ret"  in e:
			if i != 0:
				if i > val2.__len__():
					break  # Gracefully break on unusual cases
				else:
					try: 
						del val2[i]
						del val3[i]
					except IndexError:
						pass
				i = i-1
				while i <= (val2.__len__()):
					if i <0:
						break
					else:
						del val2[i]	
						del val3[i]
						i=i-1
						if i == (val2.__len__()-1):
							break

	lGoBack = linesGoBackFindOP
	matchObj = re.match( r'jmp', val, re.M|re.I)
	if matchObj:
		if save != 0:
			if val2.__len__() > 1:
				if val2.__len__() == 2:
					matchObj = re.match( r'\bnop\b|\bleave\b|\bcall\b|\bret\b|\bjmp\b|\bljmp\b|\bretf\b|\bhlt\b', val2[i-2], re.M|re.I)
					if matchObj:
						counter()
					else:
						save = int(save, 16)
						addListBase(save, val2.__len__(), NumOpsDis, modName) # fist parameter: address of target jmp [reg]; second parameter: number of lines to go back. third parameter: number of ops to go back.
						#print "alert"

						sp()
	
				else:
					matchObj = re.match( r'\bnop\b|\bleave\b|\bcall\b|\bret\b|\bjmp\b|\bljmp\b|\bjo\b|\bjno\b|\bjsn\b|\bjs\b|\bje\b|\bjz\b|\bjne\b|\bjnz\b|\bjb\b|\bjnae\b|\bjc\b|\bjnb\bjae\b|\bjnc\b|\bjbe\bjna\b|\bja\b|\bjnben\b|\bjl\b|\bjnge\b|\bjge\bjnl\b|\bjle\b|\bjng\bjg\b|\bjnle\b|\bjp\b|\bjpe\b|\bjnp\b|\bjpo\bjczz\b|\bjecxz\b|\bcall\b|\bint\b|\bdb\b|\bretf\b|\bhlt\b', val2[i-2], re.M|re.I)
					if not matchObj:
						save = int(save, 16)
						addListBase(save, val2.__len__(), NumOpsDis, modName) # fist parameter: address of target jmp [reg]; second parameter: number of lines to go back. third parameter: number of ops to go back.
						#print "alert"
						sp()




def disHereRet(address, NumOpsDis):
	global o
	w=0
	CODED2 = b""
	x = NumOpsDis
	for i in range (x, 0, -1):
		CODED2 += objs[o].data2[address-i]
	CODED2 += objs[o].data2[address]
	# CODED2 += objs[o].data2[address+1]
	CODED2 += b"\x00"
	val =""
	val2 = []
	val3 = []
	val5 =[]
	address2 = address + objs[o].startLoc + 1000
	for i in cs.disasm(CODED2, address-x):
		add = hex(int(i.address))
		addb = hex(int(i.address +  objs[o].VirtualAdd))
		add2 = str(add)
		add3 = hex (int(i.address + objs[o].startLoc	))
		add4 = str(add3)
		val =  i.mnemonic + " " + i.op_str + "\t\t\t\t"  + add4 + " (offset " + addb + ")\n"
		val2.append(val)
		val3.append(add2)
		val5.append(val)

	# print "finald"
	# for x in val2:
	# 	print x
# My method is to to detect if there is a ret, jmp or call in the gadget. If I find it, I cut out the offending lines and any leading up to it, leaving only safe gadgets that terminate in a jmp or call. The solution is a reversed for loop with enum and checking to see if jmp or call appears before the end of the gadget. If I do, I excise that line and all above it.  when I intially locate a desired sequence, e.g. jmp eax, I then capture the lines immediately before it. This is a way to ensure  that instructions petaining to control flow are not in the gadget.

	tz = val2.__len__()
	tk=0
	save=0x00
	# I need to iterate through this in reverse, starting with the jmp ptr [reg].  I contains index number and e is to enumerate, i.e. show what the value is. In this case, it is iterating through an array of  strings containing the disasembly. The goal is ultimately to cut this down by removing other control flow instructions. The end result will be I will know the address of the jmp [reg] and how many lines  to go back without encountering a control flow instruction.
	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__() 
		if tk < 1:
			save = val3[i]   # This allows me to save the initial  address of the target jmp [reg] address.

			saveq = int(save, 16)
			msg= "saving:" + str(val2[i]) + " first save: " + str(saveq)
		tk += 1

		# Use regular expressions to find lines that have control flow and other undesired instructions, so they and preceding lines can be excised. 
		# matchObj2 = re.compile( r"\bjo\b|\bjno\b|\bjsn\b|\bjs\b|\bje\b|\bjz\b|\bjne\b|\bjnz\b|\bjb\b|\bjnae\b|\bjc\b|\bjnb\bjae\b|\bjnc\b|\bjbe\bjna\b|\bja\b|\bjnben\b|\bjl\b|\bjnge\b|\bjge\bjnl\b|\bjle\b|\bjng\bjg\b|\bjnle\b|\bjp\b|\bjpe\b|\bjnp\b|\bjpo\bjczz\b|\bjecxz\b|\bcall\b|\bint\b|\bdb\b|\bret\b", re.M|re.I)
		# if re.findall(matchObj2, e):   
		# 	if i != 1:
		# 		if i > val2.__len__():
		# 			break  # Gracefully break on unusual cases
		# 		else:
		# 			try: 
		# 				del val2[i]
		# 				del val3[i]
		# 			except IndexError:
		# 				pass
		# 		i = i-1
		# 		while i <= (val2.__len__()):
		# 			if i <0:
		# 				break
		# 			else:
		# 				del val2[i]	
		# 				del val3[i]
		# 				i=i-1
		# 				if i == (val2.__len__()-1):
		# 					break
	tz = val2.__len__()
	tk=0
	save=0
#sa
	lGoBack = linesGoBackFindOP
	# if len(val2) < lGoBack:
	# 	print "reducing lg"
	# 	lgoback = (len(val2))

	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = val3[i]   #

			### IMPORTANT
			### Note, something very bizarre going on with save - unsure what - saveq works instead
		matchObj = re.match( r'ret', val, re.M|re.I)
		if matchObj:
			if save != 0:
				if val2.__len__() > 1:
					if val2.__len__() == 2:
						matchObj = re.match( r'\bnop\b|\bleave\b|\bcall\b|\bjmp\b|\bljmp\b|\bretf\b|\bhlt\b|\bret\b', val2[i-2], re.M|re.I)
						if matchObj:
							counter()
						else:
							save = int(save, 16)
							addListBase(saveq, val2.__len__(), NumOpsDis, modName) # fist parameter: address of target jmp [reg]; second parameter: number of lines to go back. third parameter: number of ops to go back.
							#print "alert"

							# print "ret1:"
							# for each in val2:
							# 	print each

							# sp()
		
					else:
						matchObj = re.match( r'\bnop\b|\bleave\b|\bcall\b|\bjmp\b|\bljmp\b|\bjo\b|\bjno\b|\bjsn\b|\bjs\b|\bje\b|\bjz\b|\bjne\b|\bjnz\b|\bjb\b|\bjnae\b|\bjc\b|\bjnb\bjae\b|\bjnc\b|\bjbe\bjna\b|\bja\b|\bjnben\b|\bjl\b|\bjnge\b|\bjge\bjnl\b|\bjle\b|\bjng\bjg\b|\bjnle\b|\bjp\b|\bjpe\b|\bjnp\b|\bjpo\bjczz\b|\bjecxz\b|\bcall\b|\bint\b|\bdb\b|\bretf\b|\bhlt\b|\bret\b', val2[i-2], re.M|re.I)
						if not matchObj:
							try:
								save = int(save, 16)
								addListBase(saveq, val2.__len__(), NumOpsDis, modName) # fist parameter: address of target jmp [reg]; second parameter: number of lines to go back. third parameter: number of ops to go back.
								#print "alert"
								# sp()
							except:
								save = 0
								# addListBase(saveq, val2.__len__(), NumOpsDis, modName) # 

							while lGoBack > 1:

								try:
									matchObj = re.match( r'\bpop\b', val2[i-lGoBack], re.M|re.I)
									if matchObj: 
										addListRETPop(saveq, lGoBack, NumOpsDis, modName) 
										#eax - saving add to specific registers -- far more useful.	
										matchObj = re.match( r'^pop [e]*a[x|l|h]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPreJ(val5, numLines)
											if z == True:
												addListRETPopEAX(saveq, numLines, NumOpsDis, modName)	
											q=lGoBack-1
											# try:
											# 	while(q>-10):
											# 		matchObj = re.match( r'^pop [e]*a[x|l|h]+', val2[q], re.M|re.I)
											# 		if matchObj:
											# 			numLines= giveLineNum(val5,val2[q])
											# 			z =stupidPreJ(val5, numLines)
											# 			if z == True:
											# 				print "verycool"
											# 				addListRETPopEAX(saveq, numLines, NumOpsDis, modName)	
											# 		q-=1
											# except:
											# 	pass
											try:
												pass
												# doublecheckPopRet(saveq,val2,q,val5,NumOpsDis,modName)
											except:
												pass
										#ebx
										matchObj = re.match( r'^pop [e]*b[x|l|h]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPre(val5, numLines)
											if z == True:
												addListRETPopEBX(saveq, numLines, NumOpsDis, modName)
												# doublecheckPopRet(saveq, val2,(lGoBack-1),val5,NumOpsDis,modName)
										#ecx
										matchObj = re.match( r'^pop [e]*c[x|l|h]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPre(val5, numLines)
											if z == True:
												addListRETPopECX(saveq, numLines, NumOpsDis, modName)
												# doublecheckPopRet(saveq, val2,(lGoBack-1),val5,NumOpsDis,modName)
										#eDx
										matchObj = re.match( r'^pop [e]*d[x|l|h]+', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPre(val5, numLines)
											if z == True:
												addListRETPopEDX(saveq, numLines, NumOpsDis, modName)
												# doublecheckPopRet(saveq, val2,(lGoBack-1),val5,NumOpsDis,modName)
										#ESI 
										matchObj = re.match( r'^pop [e]*si', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPre(val5, numLines)
											if z == True:
												addListRETPopESI(saveq, numLines, NumOpsDis, modName)
												# doublecheckPopRet(saveq, val2,(lGoBack-1),val5,NumOpsDis,modName)
										#retpopEDI 
										matchObj2 = re.match( r'^pop [e]*di', val2[i-lGoBack], re.M|re.I)
										if matchObj2:
											# print "***************"
											# print "b: " + val2[i-lGoBack]
											y = val2[i-lGoBack]
											# print "y:" + y
											# # addListRETPopEDI(saveq, giveLineNum(val5,y), NumOpsDis, modName)
											# print "popedi:"
											# print "all:"
											# print binaryToStr(CODED2)
											# print "i: " + str(i) + " lGoBack: " + str(lGoBack) +  " i-lGoBack: " + str(i-lGoBack)	
											# # print "answer: " + str(giveLineNum(val5,val2[i-lGoBack]))
										
											# for x in val2:
											# 	print x
											# print "i-lGoBack: " + str(i-lGoBack)
											# print "a: " + val2[i-lGoBack]
											# if (y != val2[i-lGoBack]):
											# 	print "weird: " + y
												# print "  was: " +  val2[i-lGoBack]
											if (y == val2[i-lGoBack]):
												# print "REAL"
												# modName2 = Ct()
												# print modName2


												numLines= giveLineNum(val5,y)
												y =stupidPre(val5, numLines)
												# modName2=str(numLines)
												if y == True:
													# print "enter true"
													addListRETPopEDI(saveq, numLines, NumOpsDis, modName)
													# print Ct()
													# counter()
													# doublecheckPopRet(saveq, val2,(lGoBack-1),val5,NumOpsDis,modName)

											# print val3[i-lGoBack]
											
											# print "lgoback: (below)"
											# print val2[lGoBack]
											# print val3[lGoBack]
											# print "answer: " + str(giveLineNum(val2))
										#now1
										#esp
										matchObj = re.match( r'^pop [e]*sp', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPre(val5, numLines)
											if z == True:
												addListRETPopESP(saveq, numLines, NumOpsDis, modName)
												# doublecheckPopRet(saveq, val2,(lGoBack-1),val5,NumOpsDis,modName)
										#EBP
										matchObj = re.match( r'^pop [e]*bp', val2[i-lGoBack], re.M|re.I)
										if matchObj:
											numLines= giveLineNum(val5,val2[i-lGoBack])
											z =stupidPre(val5, numLines)
											if z == True:
												addListRETPopEBP(saveq, numLines, NumOpsDis, modName)
												# doublecheckPopRet(saveq, val2,(lGoBack-1),val5,NumOpsDis,modName)
								except:
									pass
								lGoBack -= 1



def doublecheckPopRet(saveq,val2,q,val5, NumOpsDis, modName):
	print "val2: "
	for x in val2:
		print x
	try:
		while(q>-10):
			print "q: " + str(q)
			matcheax = re.match( r'^pop [e]*a[x|l|h]+', val2[q], re.M|re.I)
			matchebx = re.match( r'^pop [e]*b[x|l|h]+', val2[q], re.M|re.I)
			matchecx = re.match( r'^pop [e]*c[x|l|h]+', val2[q], re.M|re.I)
			matchedx = re.match( r'^pop [e]*d[x|l|h]+', val2[q], re.M|re.I)
			matchesi = re.match( r'^pop [e]*si', val2[q], re.M|re.I)
			matchedi = re.match( r'^pop [e]*di', val2[q], re.M|re.I)
			matchesp = re.match( r'^pop [e]*sp', val2[q], re.M|re.I)
			matchebp = re.match( r'^pop [e]*bp', val2[q], re.M|re.I)
			if matcheax:
				numLines= giveLineNum(val5,val2[q])
				z =stupidPre(val5, numLines)
				if z == True:
					print "verycool"
					addListRETPopEAX(saveq, numLines, NumOpsDis, modName)	
			if matchebx:
				numLines= giveLineNum(val5,val2[q])
				z =stupidPre(val5, numLines)
				if z == True:
					print "verycool2"
					print val2[q]
					addListRETPopEBX(saveq, numLines, NumOpsDis, modName)	
					print "saveq " + str(saveq) + " numlines " + str(numLines) + " nd: " + str(NumOpsDis) + " mod: " + modName
			if matchecx:
				numLines= giveLineNum(val5,val2[q])
				z =stupidPre(val5, numLines)
				if z == True:
					print "verycool3"
					addListRETPopECX(saveq, numLines, NumOpsDis, modName)	
			if matchedx:
				numLines= giveLineNum(val5,val2[q])
				z =stupidPre(val5, numLines)
				if z == True:
					print "verycool4"
					addListRETPopEDX(saveq, numLines, NumOpsDis, modName)	
			if matchesi:
				numLines= giveLineNum(val5,val2[q])
				z =stupidPre(val5, numLines)
				if z == True:
					addListRETPopESI(saveq, numLines, NumOpsDis, modName)	
					print "verycool5" 
					print val2[q]
					print "saveq " + str(saveq) + " numlines " + str(numLines) + " nd: " + str(NumOpsDis) + " mod: " + modName
			if matchedi:
				numLines= giveLineNum(val5,val2[q])
				z =stupidPre(val5, numLines)
				if z == True:
					print "verycool6"
					print val2[q]
					addListRETPopEDI(saveq, numLines, NumOpsDis, modName)	
					print "saveq " + str(saveq) + " numlines " + str(numLines) + " nd: " + str(NumOpsDis) + " mod: " + modName
			if matchesp:
				numLines= giveLineNum(val5,val2[q])
				z =stupidPre(val5, numLines)
				if z == True:
					print "verycool7"
					addListRETPopESP(saveq, numLines, NumOpsDis, modName)	
			if matchebp:
				numLines= giveLineNum(val5,val2[q])
				z =stupidPre(val5, numLines)
				if z == True:
					print "verycool8"
					addListRETPopEBP(saveq, numLines, NumOpsDis, modName)	
			q-=1
	except:
		pass
def disHereCALLPTR(address, NumOpsDis, Reg):
	#print "ok2"
	#print  hex(int(address))
	sp()
	global o
	lGoBack = linesGoBackFindOP

	w=0
	CODED2 = b""

	x = NumOpsDis
	for i in range (x, 0, -1):
		CODED2 += objs[o].data2[address-i]
	CODED2 += objs[o].data2[address]
	CODED2 += objs[o].data2[address+1]
	CODED2 += b"\x00"

	val =""
	val2 = []
	val3 = []
	address2 = address + objs[o].startLoc + 1000
	for i in cs.disasm(CODED2, address-x):
		add = hex(int(i.address))
		addb = hex(int(i.address +  objs[o].VirtualAdd))
		add2 = str(add)
		add3 = hex (int(i.address + objs[o].startLoc	))
		add4 = str(add3)
		val =  i.mnemonic + " " + i.op_str + "\t\t\t\t"  + add4 + " (offset " + addb + ")\n"
		val2.append(val)
		val3.append(add2)
		#print val

# My method is to to detect if there is a ret, jmp or call in the gadget. If I find it, I cut out the offending lines and any leading up to it, leaving only safe gadgets that terminate in a jmp or call. The solution is a reversed for loop with enum and checking to see if jmp or call appears before the end of the gadget. If I do, I excise that line and all above it.  when I intially locate a desired sequence, e.g. jmp eax, I then capture the lines immediately before it. This is a way to ensure  that instructions petaining to control flow are not in the gadget.

	tz = val2.__len__()
	tk=0
	save=0x00
	# I need to iterate through this in reverse, starting with the jmp ptr [reg].  I contains index number and e is to enumerate, i.e. show what the value is. In this case, it is iterating through an array of  strings containing the disasembly. The goal is ultimately to cut this down by removing other control flow instructions. The end result will be I will know the address of the jmp [reg] and how many lines  to go back without encountering a control flow instruction.
	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__() 
		if tk < 1:
			save = val3[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1

		# Use regular expressions to find lines that have control flow and other undesired instructions, so they and preceding lines can be excised. 
		matchObj2 = re.compile( r"\bjo\b|\bjno\b|\bjsn\b|\bjs\b|\bje\b|\bjz\b|\bjne\b|\bjnz\b|\bjb\b|\bjnae\b|\bjc\b|\bjnb\bjae\b|\bjnc\b|\bjbe\bjna\b|\bja\b|\bjnben\b|\bjl\b|\bjnge\b|\bjge\bjnl\b|\bjle\b|\bjng\bjg\b|\bjnle\b|\bjp\b|\bjpe\b|\bjnp\b|\bjpo\bjczz\b|\bjecxz\b|\bjmp\b|\bint\b|\bdb\b", re.M|re.I)
		if i == 0:
			break
		if re.findall(matchObj2, e):   #if "ret"  in e:
			if i != 1:
				if i > val2.__len__():
					break  # Gracefully break on unusual cases
				else:
					try: 
						del val2[i]
						del val3[i]
					except IndexError:
						pass
				i = i-1
				while i <= (val2.__len__()):
					if i <0:
						break
					else:
						del val2[i]	
						del val3[i]
						i=i-1
						if i == (val2.__len__()-1):
							break
	tz = val2.__len__()
	tk=0
	save=0
	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = val3[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1
# Here I search for excise ret's from JOP gadget. I had tried to incorporate this functionality into the
# above, but I would run into test cases that would cause errors. This seemed the best solution, even if
# inelegant.
		matchObj2 = re.compile( r"\bret\b", re.M|re.I)
		if re.findall(matchObj2, e):   #if "ret"  in e:
			if i != 0:
				if i > val2.__len__():
					break  # Gracefully break on unusual cases
				else:
					try: 
						del val2[i]
						del val3[i]
					except IndexError:
						pass
				i = i-1
				while i <= (val2.__len__()):
					if i <0:
						break
					else:
						del val2[i]	
						del val3[i]
						i=i-1
						if i == (val2.__len__()-1):
							break

	lGoBack = linesGoBackFindOP
	matchObj = re.match( r'call', val, re.M|re.I)
	if matchObj:
		if save != 0:
			if val2.__len__() > 1:
				if val2.__len__() == 2:
					matchObj = re.match( r'\bnop\b|\bleave\b|\bcall\b|\bret\b|\bjmp\b|\bljmp\b|\bretf\b|\bhlt\b', val2[i-2], re.M|re.I)
					if matchObj:
						counter()
					else:
						save = int(save, 16)
						addListBase(save, val2.__len__(), NumOpsDis, modName) # fist parameter: address of target jmp [reg]; second parameter: number of lines to go back. third parameter: number of ops to go back.
						
	
				else:
					matchObj = re.match( r'\bnop\b|\bleave\b|\bcall\b|\bret\b|\bjmp\b|\bljmp\b|\bjo\b|\bjno\b|\bjsn\b|\bjs\b|\bje\b|\bjz\b|\bjne\b|\bjnz\b|\bjb\b|\bjnae\b|\bjc\b|\bjnb\bjae\b|\bjnc\b|\bjbe\bjna\b|\bja\b|\bjnben\b|\bjl\b|\bjnge\b|\bjge\bjnl\b|\bjle\b|\bjng\bjg\b|\bjnle\b|\bjp\b|\bjpe\b|\bjnp\b|\bjpo\bjczz\b|\bjecxz\b|\bcall\b|\bint\b|\bdb\b|\bretf\b|\bhlt\b', val2[i-2], re.M|re.I)
					if not matchObj:

						save = int(save, 16)
						#if searchListBase(save, NumOpsDis) != 1:
						
						#print "alert"	
						#print "SVAL:" + str(searchListBase(save, NumOpsDis))
						addListBase(save, val2.__len__(), NumOpsDis, modName) # fist parameter: address of target jmp [reg]; second parameter: number of lines to go back. third parameter: number of ops to go back.
					
						#searchListBase2(save, NumOpsDis)

						#print save
						#print val2[i-2]
						sp()
						#print listOP_Base
						#searchListBase(save, NumOpsDis)


globalOuts =[]

def clearGOuts():
	global globalOuts
	globalOuts [:] = []

def disHereClean(address, valCount, NumOpsDis, mode):
	global globalOuts
	CODED2 = b""
	x = NumOpsDis
	for i in range (x, 0, -1):
		CODED2 += objs[o].data2[address-i]
	CODED2 += objs[o].data2[address]
	if (mode=="jmp"):
		CODED2 += objs[o].data2[address+1]
	# CODED2 += objs[o].data2[address+1]
	CODED2 += b"\x00"

	val =""
	val2 = []
	val3 = []
	address2 = address + objs[o].startLoc + 1000

	#now2
	for i in cs.disasm(CODED2, address-x):
		add = hex(int(i.address))
		addb = hex(int(i.address +  objs[o].VirtualAdd))
		add2 = str(add)
		add3 = hex (int(i.address + objs[o].startLoc	))
		add4 = str(add3)
		val =  i.mnemonic + " " + i.op_str + "\t\t\t\t"  + add4 + " (offset " + addb + ")\n"
		val2.append(val)
		val3.append(add2)
	print "dis:"
	for x in val2:
		print x
	print binaryToStr(CODED2)
	
	returnVal = ""
	trueVal2Cnt = val2.__len__()
	if trueVal2Cnt == valCount:
		for i in range (valCount):
			#print val2[i]
			returnVal += str(val2[i]) 
	else:
		while trueVal2Cnt > valCount:
			del val2[0]
			trueVal2Cnt -= 1
			if trueVal2Cnt == valCount:
				for i in range (valCount):
			#		print val2[i]
					returnVal += str(val2[i])

	return returnVal  #"\n"+binaryToStr(CODED2) + " val: " +str(valCount)
	

def disHereClean3(address, valCount, NumOpsDis, mode):
	global globalOuts
	CODED2 = b""
	x = NumOpsDis
	for i in range (x, 0, -1):
		CODED2 += objs[o].data2[address-i]
	CODED2 += objs[o].data2[address]
	if (mode=="jmp"):
		CODED2 += objs[o].data2[address+1]
	CODED2 += b"\x00"

	# print "enter dishere3"

	val =""
	val2 = []
	val3 = []
	address2 = address + objs[o].startLoc + 1000

	#now2
	for i in cs.disasm(CODED2, address-x):
		add = hex(int(i.address))
		addb = hex(int(i.address +  objs[o].VirtualAdd))
		add2 = str(add)
		add3 = hex (int(i.address + objs[o].startLoc	))
		add4 = str(add3)
		val =  i.mnemonic + " " + i.op_str + "\t\t\t\t"  + add4 + " (offset " + addb + ")\n"
		val2.append(val)
		val3.append(add2)
	# print "dis:"
	# for x in val2:
	# 	print x
	# print binaryToStr(CODED2)
	
	returnVal = ""
	trueVal2Cnt = val2.__len__()
	if trueVal2Cnt == valCount:
		for i in range (valCount):
			#print val2[i]
			returnVal += str(val2[i]) 
	else:
		while trueVal2Cnt > valCount:
			del val2[0]
			trueVal2Cnt -= 1
			if trueVal2Cnt == valCount:
				for i in range (valCount):
			#		print val2[i]
					returnVal += str(val2[i])

	globalOuts.append(" ")
	if returnVal not in globalOuts:
		globalOuts.append(returnVal)
		# print "global"
		return returnVal #"\n"+binaryToStr(CODED2) + " val: " +str(valCount)
	if returnVal  in globalOuts:
		return " "
	# return returnVal

hashchecker = []
hashcheckerPre = []

def disHereClean2(address, valCount, NumOpsDis, mode):
	global hashCheckVal

	CODED2 = b""
	x = NumOpsDis
	for i in range (x, 0, -1):
		try: 
			CODED2 += objs[o].data2[address-i]
		except IndexError:
			pass
	try:
		CODED2 += objs[o].data2[address]
	except IndexError:
		print ""#"index error"
	if (mode=="jmp"):
		try:
			CODED2 += objs[o].data2[address+1]
		except IndexError:
			pass

	CODED2 += b"\x00"

	val =""
	val2 = []
	val3 = []
	address2 = address + objs[o].startLoc + 1000

	for i in cs.disasm(CODED2, address-x):
		add = hex(int(i.address))
		addb = hex(int(i.address +  objs[o].VirtualAdd))
		add2 = str(add)
		add3 = hex (int(i.address + objs[o].startLoc	))
		add4 = str(add3)
		val =  i.mnemonic + " " + i.op_str + "\t\t\t\t"  + add4 + " (offset " + addb + ")\n"
		val2.append(val)
		val3.append(add2)
		# print val
	
	trueVal2Cnt = val2.__len__()

	z = 0
	while (val2.__len__() < valCount):
		z = z + 1
		valCount = valCount -1
	trueVal2Cnt = val2.__len__()
	
	

	val2.reverse()
	# for i in val2:
	# 	#print i
	# 	pass
	

	returnVal = ""
	begin = trueVal2Cnt - valCount
	bad =0
	val2b = []
	#Stops bad stuff that I wasn't smart enough to stop from getting in the list from printing
	#Have written and rewritten this code in a number of ways.
	for i in val2: #   #was +1
		matchObj = re.match( r'^call|^jmp|^jo|^jno|^jsn|^js|^je|^jz|^jne|^jnz|^jb|^jnae|^jc|^jnb|^jae|^jnc|^jbe|^jna|^ja|^jnben|^jl|^jnge|^jge|^jnl|^jle|^jng|^jg|^jnle|^jp|^jpe|^jnp|^jpo|^jczz|^jecxz|^jmp|^int|^retf|^db|^hlt', i, re.M|re.I)
		if matchObj:
			bad = bad + 1
			if bad < 2:
				val2b.append(str(i))
			if bad > 1: 
				#bad = 0
				#val2b.append("break")
				break
		else:	
			if bad < 2 : 
				val2b.append(i)	

	#print "magic"
	sp()
	
	# for i in val2b:
	# 	#print i
	# 	pass

	val333 = []
	for i in val2[begin:valCount+1]:   		
		val333.append(i)

	# for i in val333:
	# 	#print i
	# 	pass
	val2b.reverse()
	trueVal2Cnt = val2b.__len__()
	begin = trueVal2Cnt - valCount

# Evil opcode-splitting means we may get some gadgets that are essentially the same, 4 lines versus 5 lines. That is  not useful, so I hash 5 lines and check to make sure none have 5 that are the same

	counterForHash = 0 # checks to see if 5 
	returnVal2 =""
	for i in val2b:   #
		returnVal = returnVal + i
		
	val2c = []
	val2b.reverse()

	for i in val2b:
		val2c.append(i)
		counterForHash = counterForHash + 1
		if counterForHash == hashCheckVal:
			break

	val2c.reverse()

	for i in val2c:   #
		returnVal2 = returnVal2 + i

	# print "r val1"
	# print returnVal
	# print "r val2"
	# print returnVal2
	# print val2b
	# print val2c
	# print "entering final"
	sp()
	if h(returnVal2) not in hashcheckerPre:
		hashcheckerPre.append(h(returnVal2))
		#return returnVal
		#print "got one*************************"
		if h(returnVal) not in hashchecker:
			hashchecker.append(h(returnVal))
			return returnVal
		else:
			#print "no1				not in it not in"
			return " "

	else:
		#print "no2"
		return " "

	# if h(returnVal) not in hashchecker:
	# 	hashchecker.append(h(returnVal))
	# 	return returnVal
	# else:
	# 	print "no"
	# 	return " "

def h(word):
	hash_object = hashlib.md5(word)
	val =str(hash_object.hexdigest())
	return val

cutting  = 0 
def stupid(val2):
	global cutting
	res = []
	#print val2
	sp()
	bad = 0
	cnt=0
	for i in val2: #   #was +1
	#	print i
		sp()
		matchObj3 = re.compile( r'call|jmp|jo|jno|jsn|js|je|jz|jne|jnz|jb|jnae|jc|jnb|jae|jnc|jbe|jna|ja|jnben|jl|jnge|jge|jnl|jle|jng|jg|jnle|jp|jpe|jnp|jpo|jczz|jecxz|jmp|int|retf|db|hlt|loop|leave')
		if matchObj3.search(i):
			bad = bad + 1
			if bad < 2:
				res.append(str(i))
			if bad > 1: 
				cutting = cutting + cnt
				break
		else:	
			if bad < 2 : 
				res.append(i)
		cnt = cnt +1	
	return res




def doit(val2):	
	#for i,e in reversed(list(enumerate(val2))):
	temp = 0
	lim=len(val2)
	#print "lim " + str(lim)
	#print val2[temp]
	special =0
	specAddEsp = re.match( r'\badd esp\b|\badc esp\b|\bsub esp\b|\bsbb esp\b', val2[temp], re.M|re.I)
	spec = re.match( r'\bpop\b|\bpush\b|\bpushad\b|\bpusha\b|\bpusha\b', val2[temp], re.M|re.I)
	if (spec or specAddEsp):
		while (temp < lim):
			spec = re.match( r'\bpop\b', val2[temp], re.M|re.I)
			popad= re.match( r'\bpopad\b|\bpopal\b', val2[temp], re.M|re.I)
			popa= re.match( r'\bpopa\b', val2[temp], re.M|re.I)
			specAddEsp = re.match( r'\badd esp\b|\badc esp\b', val2[temp], re.M|re.I)
			specSubEsp = re.match( r'\bsub esp\b|\bsbb esp\b', val2[temp], re.M|re.I)
			push= re.match( r'\bpush\b', val2[temp], re.M|re.I)
			pushad= re.match( r'\bpushal\b|\bpushad\b', val2[temp], re.M|re.I)
			pusha= re.match( r'\bpusha\b', val2[temp], re.M|re.I)
			stop=pusha= re.match( r'\bpusha\b', val2[temp], re.M|re.I)
			if spec:
				if not (popa or popad):
					#print "spec" + val2[temp]
					special = special +0x4	
					#print  " POP result: " + " temp: " + str(temp) + " special: " + str(special)
			if specAddEsp:
				specAddEsp = re.search( r'0x[0-9A-F]*', val2[temp], re.M|re.I)
				specAddEsp2 = re.search( r'\d', val2[temp], re.M|re.I)
				if (specAddEsp):
					result = specAddEsp.group()
					special = special + int(result,16)
				if specAddEsp2:
					if not specAddEsp:
						result = specAddEsp2.group()
						special = special + int(result)
			if specSubEsp:
				specSubEsp = re.search( r'0x[0-9A-F]*', val2[temp], re.M|re.I)
				specSubEsp2 = re.search( r'\d', val2[temp], re.M|re.I)
				if (specSubEsp):
					result = specSubEsp.group()
					special = special - int(result,16)
				if specSubEsp2:
					if not specSubEsp:
						result = specSubEsp2.group()
						special = special - int(result)
			if push:
				if not (pusha or pushad):
					special = special -0x4	
					#print  " PUSH result: " + " temp: " + str(temp) + " special: " + str(special)
			if popad:
				#print "popad"
				special = special + 32
			if popa:
				#print "popa"
				special = special +16
			if pushad:
				#print "pushad"
				special = special -32
			if pusha:
				#print "pusha"
				special = special -16
			temp = temp +1
	return  special

def checkItOLD(val2,r1,r2):	
	#for i,e in reversed(list(enumerate(val2))):
	temp = 0
	lim=len(val2)
	#print "lim " + str(lim)
	#print val2[temp]
	special =0
	specAddEsp = re.match( r'\badd esp\b|\badc esp\b|\bsub esp\b|\bsbb esp\b', val2[temp], re.M|re.I)
	spec = re.match( r'\bpop\b|\bpush\b|\bpushad\b|\bpusha\b|\bpusha\b', val2[temp], re.M|re.I)
	if (spec or specAddEsp):
		while (temp < lim):
			spec = re.match( r'\bpop\b', val2[temp], re.M|re.I)
			popad= re.match( r'\bpopad\b|\bpopal\b', val2[temp], re.M|re.I)
			popa= re.match( r'\bpopa\b', val2[temp], re.M|re.I)
			specAddEsp = re.match( r'\badd esp\b|\badc esp\b', val2[temp], re.M|re.I)
			specSubEsp = re.match( r'\bsub esp\b|\bsbb esp\b', val2[temp], re.M|re.I)
			push= re.match( r'\bpush\b', val2[temp], re.M|re.I)
			pushad= re.match( r'\bpushal\b|\bpushad\b', val2[temp], re.M|re.I)
			pusha= re.match( r'\bpusha\b', val2[temp], re.M|re.I)
			if spec:
				if not (popa or popad):
					#print "spec" + val2[temp]
					special = special +0x4	
					#print  " POP result: " + " temp: " + str(temp) + " special: " + str(special)
			if specAddEsp:
				specAddEsp = re.search( r'0x[0-9A-F]*', val2[temp], re.M|re.I)
				specAddEsp2 = re.search( r'\d', val2[temp], re.M|re.I)
				if (specAddEsp):
					result = specAddEsp.group()
					special = special + int(result,16)
				if specAddEsp2:
					if not specAddEsp:
						result = specAddEsp2.group()
						special = special + int(result)
			if specSubEsp:
				specSubEsp = re.search( r'0x[0-9A-F]*', val2[temp], re.M|re.I)
				specSubEsp2 = re.search( r'\d', val2[temp], re.M|re.I)
				if (specSubEsp):
					result = specSubEsp.group()
					special = special + int(result,16)
				if specSubEsp2:
					if not specSubEsp:
						result = specSubEsp2.group()
						special = special + int(result)
			if push:
				if not (pusha or pushad):
					special = special -0x4	
					#print  " PUSH result: " + " temp: " + str(temp) + " special: " + str(special)
			if popad:
				#print "popad"d
				special = special + 32
			if popa:
				#print "popa"
				special = special +16
			if pushad:
				#print "pushad"
				special = special -32
			if pusha:
				#print "pusha"
				special = special -16
			temp = temp +1
	return  special

def disHereCleanSP(address, valCount, NumOpsDis, special, Reg, mod):
	global cutting
	CODED2 = b""
	x = NumOpsDis
	for i in range (x, 0, -1):
		try: 
			CODED2 += objs[o].data2[address-i]
		except IndexError:
			pass
	try:
		CODED2 += objs[o].data2[address]
	except IndexError:
		pass
	try:
		CODED2 += objs[o].data2[address+1]
	except IndexError:
		pass

	# CODED2 += b"\x00"
	# val =""
	# val2 = []
	# val3 = []
	# addArray =[]
	# address2 = address + objs[o].startLoc + 1000

	# for i in cs.disasm(CODED2, address-x):
	# 	add = hex(int(i.address))
	# 	addb = hex(int(i.address +  objs[o].VirtualAdd))
	# 	add2 = str(add)
	# 	add3 = hex (int(i.address + objs[o].startLoc	))
	# 	add4 = str(add3)
	# 	val=""
	# 	#addArray.append(add4 + " # " + "(base + " + addb + ") ")
	# 	addArray.append(fixHexAddy(add4) + ", # " + "(base + " + addb + "), # ")
	# 	val2.append(i.mnemonic + " " + i.op_str  + " # ")
	# 	val3.append(add2)
	# 	#print val
	CODED2 += b"\x00"
	val =""
	val2 = []
	val3 = []
	val4=[]
	addArray =[]
	address2 = address + objs[o].startLoc + 1000

	TotalNumLines=0
	for i in cs.disasm(CODED2, address-x):
		TotalNumLines+=1
	startingPoint = TotalNumLines - valCount
	if TotalNumLines == 0:    # some ff ff (Bad) (bad) cause this to not work? gives 0 as TotalNumLines
		return False, " ",0
	ip =0
	first=0
	for i in cs.disasm(CODED2, address-x):
		if ip >= startingPoint:
			add = hex(int(i.address))
			addb = hex(int(i.address +  objs[o].VirtualAdd))
			add2 = str(add)
			add3 = hex (int(i.address + objs[o].startLoc	))
			add4 = str(add3)
			val=""
			if first ==0:
				val4.append(fixHexAddy(add4) + ", # " + "(base + " + addb + "), # ")
				first +=1
			val2.append(i.mnemonic + " " + i.op_str  + " # ")
			val4.append(i.mnemonic + " " + i.op_str  + " # ")
			val3.append(add2)
		ip +=1

	returnVal =""
	for i in val4:   #
		returnVal += i
	r2="eax"
	returnVal += "" + mod +" "

	if returnVal not in globalOuts:
		globalOuts.append(returnVal)
		valNew=splitterRetval2(returnVal)
		return True, returnVal, doit(valNew)# checkIt(val2c,"eax","eax")
	else:
		# print "repeat"
		return False, " ",0

def disHereCleanJMPPTR(address, valCount, NumOpsDis, mod):
	# print "disHereCleanJMPPTR"

	# print address
	# print valCount
	# print NumOpsDis
	# print mod
	global cutting
	CODED2 = b""
	x = NumOpsDis
	for i in range (x, 0, -1):
		try: 
			CODED2 += objs[o].data2[address-i]
		except IndexError:
			pass
	try:
		CODED2 += objs[o].data2[address]
	except IndexError:
		pass
	try:
		CODED2 += objs[o].data2[address+1]
	except IndexError:
		pass

	CODED2 += b"\x00"
	val =""
	val2 = []
	val3 = []
	addArray =[]
	address2 = address + objs[o].startLoc + 1000

	end=0
	for i in cs.disasm(CODED2, address-x):
		add = hex(int(i.address))
		addb = hex(int(i.address +  objs[o].VirtualAdd))
		add2 = str(add)
		add3 = hex (int(i.address + objs[o].startLoc	))
		add4 = str(add3)
		val=""
		addArray.append(fixHexAddy(add4) + ", # " + "(base + " + addb + "), # ")

		out1=i.mnemonic + " " + i.op_str
		matchObj2 = re.match( r'^jmp dword ptr \[eax \+ eax]+', out1, re.M|re.I)
		if matchObj2: 
			out1 = " jmp dword ptr [esp]* "
		val2.append(out1 + " # ")
		# val2.append(i.mnemonic + " " + i.op_str  + " # ")
		val3.append(add2)
		end +=1
	val2.reverse()
	addArray.reverse()
	returnVal2 = str(addArray[0]) + str(val2[0]) + " " + mod
	# print "returnval2" + returnVal2

	return True, returnVal2
	

def disHereCleanPopR1(address, valCount, NumOpsD, r1, mod, mode):#, best):
	# print "cleanpop inside  pop is" + r1
	global cutting
	global globalOuts
	# print "address: " +  str(address) + " valcount: " + str(valCount)

	CODED2 = b""
	x = NumOpsD
	for i in range (x, 0, -1):
		try: 
			CODED2 += objs[o].data2[address-i]
		except IndexError:
			pass
	try:
		CODED2 += objs[o].data2[address]
	except IndexError:
		pass
	# try:
	# 	CODED2 += objs[o].data2[address+1]
	# except IndexError:
	# 	pass

	CODED2 += b"\x00"
	val =""
	val2 = []
	val3 = []
	val4=[]
	addArray =[]
	address2 = address + objs[o].startLoc + 1000

	TotalNumLines=0
	for i in cs.disasm(CODED2, address-x):
		TotalNumLines+=1
	startingPoint = TotalNumLines - valCount
	if TotalNumLines == 0:    # some ff ff (Bad) (bad) cause this to not work? gives 0 as TotalNumLines
		return False, " ",0
	ip =0
	first=0
	for i in cs.disasm(CODED2, address-x):
		if ip >= startingPoint:
			add = hex(int(i.address))
			addb = hex(int(i.address +  objs[o].VirtualAdd))
			add2 = str(add)
			add3 = hex (int(i.address + objs[o].startLoc	))
			add4 = str(add3)
			val=""
			#addArray.append(add4 + " # " + "(base + " + addb + ") ")
			if first ==0:
				val4.append(fixHexAddy(add4) + ", # " + "(base + " + addb + "), # ")
				first +=1
			val2.append(i.mnemonic + " " + i.op_str  + " # ")
			val4.append(i.mnemonic + " " + i.op_str  + " # ")
			val3.append(add2)
		
		ip +=1

	returnVal =""
	for i in val4:   #
		returnVal += i
	r2="eax"
	returnVal += "" + mod +" "
	# print "finalR: " + returnVal

	if mode =="ok":
		boolCheck,  specCheck =checkItRet(val2,r1)
		# print "g2: addy: " + str(address) + " lines: " + str(valCount)

		# print "CheckIt " + r1 + " " 
	if mode =="best":
		boolCheck, specCheck = checkItRetBest(val2,r1, best)
		# print "checkitBest " + r1 + " " + " " + str(boolCheck)
	if  boolCheck:
		# print " dishere found FOUND " + r1 
		# print specCheck
		if returnVal not in globalOuts:
			globalOuts.append(returnVal)
			return boolCheck, returnVal, specCheck# checkIt(val2c,"eax","eax")
		else:
			# print "repeat"
			return False, " ",0

	else:
		return False, " ",0
	
	

def disHereCleanPop(address, valCount, NumOpsDis, r1, r2, mode, best, mod):
	# print "cleanpop inside  pop is" + r1
	global cutting
	CODED2 = b""
	x = NumOpsDis
	for i in range (x, 0, -1):
		try: 
			CODED2 += objs[o].data2[address-i]
		except IndexError:
			pass
	try:
		CODED2 += objs[o].data2[address]
	except IndexError:
		pass
	try:
		CODED2 += objs[o].data2[address+1]
	except IndexError:
		pass

	CODED2 += b"\x00"
	val =""
	val2 = []
	val3 = []
	addArray =[]
	address2 = address + objs[o].startLoc + 1000

	# print "disherecleanpop valCount " + str(valCount)

	for i in cs.disasm(CODED2, address-x):
		add = hex(int(i.address))
		addb = hex(int(i.address +  objs[o].VirtualAdd))
		add2 = str(add)
		add3 = hex (int(i.address + objs[o].startLoc	))
		add4 = str(add3)
		val=""
		#addArray.append(add4 + " # " + "(base + " + addb + ") ")
		addArray.append(fixHexAddy(add4) + ", # " + "(base + " + addb + "), # ")
		val2.append(i.mnemonic + " " + i.op_str  + " # ")
		val3.append(add2)
	
	trueVal2Cnt = val2.__len__()
	z = 0
	while (val2.__len__() < valCount):
		z = z + 1
		valCount = valCount -1
	trueVal2Cnt = val2.__len__()
	
	val2.reverse()

	returnVal = ""
	begin = trueVal2Cnt - valCount

	test2 = []
	cutter = 3
	test2 = val2
	cutting = 0
	while (cutter > 0):
		test2 =	stupid(test2)
		cutter = cutter -1


	val2b = test2
	val2b.reverse()
	trueVal2Cnt = val2b.__len__()
	begin = trueVal2Cnt - valCount
	returnVal2 =""
	# print val2b

	d=cutting
	first =0
	d = len(addArray) - len(test2)
	for i in val2b:   #
		if first ==0:
			returnVal =  addArray[d] + i + returnVal  
			first = first +1
		else:
			returnVal = returnVal + i
	val2c = []

	returnVal += "" + mod +" "
	# val2b.reverse()

	# counterForHash = 0 # checks to see if 5 
	# returnVal2 =""
	# for i in val2b:   #
	# 	returnVal2 = returnVal2 + i

	# for i in val2b:
	# 	val2c.append(i)
	# 	counterForHash = counterForHash + 1
	# 	if counterForHash == hashCheckVal:
	# 		break
	# val2c.reverse()

	# for i in val2c:   #
	# 	returnVal2 = returnVal2 + i

	# print "val2c"
	# for x in val2c:
	# 	print x
	# if h(returnVal2) not in hashcheckerPre:
	# 	hashcheckerPre.append(h(returnVal2))
	# 	if h(returnVal) not in hashchecker:
	# 		hashchecker.append(h(returnVal))
	# 		ans2=  returnVal
	if mode =="ok":
		boolCheck,  specCheck =checkIt(val2b,r1,r2)
		# print "jCheckIt " + r1 + " " + r2
	if mode =="best":
		boolCheck, specCheck = checkItBest(val2b,r1,r2, best)
		# print "jcheckitBest " + r1 + " " +r2 + " " + str(boolCheck)
	if  boolCheck:
		# print " jmpdishere found FOUND " + r1 + r2
		# print specCheck
		return boolCheck, returnVal, specCheck# checkIt(val2c,"eax","eax")

	else:
		return False," ", 0



def disHereCleanNewDG(address, valCount, NumOpsDis, mod):
	# print "cleanpop inside  pop is" + r1
	global cutting
	CODED2 = b""
	x = NumOpsDis
	for i in range (x, 0, -1):
		try: 
			CODED2 += objs[o].data2[address-i]
		except IndexError:
			pass
	try:
		CODED2 += objs[o].data2[address]
	except IndexError:
		pass
	try:
		CODED2 += objs[o].data2[address+1]
	except IndexError:
		pass

	CODED2 += b"\x00"
	val =""
	val2 = []
	val3 = []
	addArray =[]
	address2 = address + objs[o].startLoc + 1000
	forCount=[]

	t=0
	for i in cs.disasm(CODED2, address-x):
		t+=1

	start = (t) - valCount

	y=0
	for i in cs.disasm(CODED2, address-x):
		if y >= start:
			add = hex(int(i.address))
			addb = hex(int(i.address +  objs[o].VirtualAdd))
			add2 = str(add)
			add3 = hex (int(i.address + objs[o].startLoc	))
			add4 = str(add3)
			val=""
			#addArray.append(add4 + " # " + "(base + " + addb + ") ")
			addArray.append(fixHexAddy(add4) + ", # (base + " + addb + ") # ")
			val2.append(i.mnemonic + " " + i.op_str  + " # ")
			forCount.append(i.mnemonic + " " + i.op_str)
			val3.append(add2)
		y+=1
	trueVal2Cnt = val2.__len__()
	z = 0
	while (val2.__len__() < valCount):
		z = z + 1
		valCount = valCount -1
	trueVal2Cnt = val2.__len__()
	
	val2.reverse()

	returnVal = ""
	begin = trueVal2Cnt - valCount

	test2 = []
	cutter = 3
	test2 = val2
	cutting = 0
	while (cutter > 0):
		test2 =	stupid(test2)
		cutter = cutter -1


	val2b = test2
	val2b.reverse()
	trueVal2Cnt = val2b.__len__()
	begin = trueVal2Cnt - valCount
	returnVal2 =""


	d=cutting
	first =0
	d = len(addArray) - len(test2)
	for i in val2b:   #
		if first ==0:
			returnVal =  addArray[d] + i + returnVal  
			first = first +1
		else:
			returnVal = returnVal + i
	val2c = []

	returnVal += "" + mod +" "
	last=len(forCount)-1
	word = forCount[0]
	special =0
	try:
		word2=splitterDG(returnVal)
	except:
		word2="ok"

	 # word2
	# print word2
	dispatchAmt = re.search( r'0x[0-9A-F]*', word2, re.M|re.I)
	dispatchAmtHex = re.search( r'\d', word2, re.M|re.I)
	if (dispatchAmt):
		result = dispatchAmt.group()
		special = special + int(result,16)
	if dispatchAmtHex:
		if not dispatchAmt:
			result = dispatchAmtHex.group()
			special = special + int(result)
	# return special
	# print "return " + returnVal
	# print "valCount " + str(valCount)
	# print "dAmount " + str(special) 
	# print word2
	return returnVal, special

def disHereCleanSP2(address, valCount, NumOpsDis, special, Reg, mod):
	spbytes =0
	SPSuccess=False
	SPSuccess, spgadget, spbytes= disHereCleanSP(address, valCount, NumOpsDis, special, Reg, mod)

	if SPSuccess:
		# print "reg: " +  Reg + " " + spgadget

		if Reg == "ALL":
			addListSPAll(spgadget,spbytes)
		if Reg == "EAX":
			addListSPEAX(spgadget,spbytes)
		if Reg == "EBX":
			addListSPEBX(spgadget,spbytes)
		if Reg == "ECX":
			addListSPECX(spgadget,spbytes)
		if Reg == "EDX":
			addListSPEDX(spgadget,spbytes)
		if Reg == "ESI":
			addListSPESI(spgadget,spbytes)
		if Reg == "EDI":
			addListSPEDI(spgadget,spbytes)
		if Reg == "EBP":
			addListSPEBP(spgadget,spbytes)
		if Reg == "ESP":
			addListSPESP(spgadget,spbytes)
	return SPSuccess, spgadget, spbytes



def disHereCleanPopRet2Best (address, valCount, NumOpsDis, mod, Reg):
	global spPopOutsEAX
	global spPopOutsEBX
	global spPopOutsECX
	global spPopOutsEDX
	global spPopOutsEDI
	global spPopOutsESI
	global spPopOutsESP
	global spPopOutsEBP
	spbytes =0
	SPSuccess=False
	# tupInfo = (address, valCount, NumOpsDis, mod)
	SPSuccess, spgadget, spbytes= disHereCleanPopR1(address, valCount, NumOpsDis, Reg, mod, "best")
	# print "output: " + str(SPSuccess) + "  " + spgadget
	if SPSuccess:
		Reg=Reg.upper()
		if Reg == "EAX":
			if spgadget not in objs[o].specialPOPGadgetRetBestEAX:
				addSpecialPOPRetBestEAX(spgadget,spbytes)
		if Reg == "EBX":
			if spgadget not in objs[o].specialPOPGadgetRetBestEBX:
				addSpecialPOPRetBestEBX(spgadget,spbytes)
		if Reg == "ECX":
			if spgadget not in objs[o].specialPOPGadgetRetBestECX:
				# SpOutGadgetECX.appen
				addSpecialPOPRetBestECX(spgadget,spbytes)			
		if Reg == "EDX":
			if spgadget not in objs[o].specialPOPGadgetRetBestEDX:
				addSpecialPOPRetBestEDX(spgadget,spbytes)			
		if Reg == "ESI":
			if spgadget not in objs[o].specialPOPGadgetRetBestESI:
				addSpecialPOPRetBestESI(spgadget,spbytes)			
		if Reg == "EDI":
			if spgadget not in objs[o].specialPOPGadgetRetBestEDI:
				addSpecialPOPRetBestEDI(spgadget,spbytes)			
		if Reg == "EBP":
			if spgadget not in objs[o].specialPOPGadgetRetBestEBP:
				addSpecialPOPRetBestEBP(spgadget,spbytes)			
		if Reg == "ESP":
			if spgadget not in objs[o].specialPOPGadgetRetBestESP:
				addSpecialPOPRetBestESP(spgadget,spbytes)	
	return SPSuccess, spgadget, spbytes


def disHereCleanPopRet2 (address, valCount, NumOpsDis, mod, Reg):
	spbytes =0
	SPSuccess=False
	# tupInfo = (address, valCount, NumOpsDis, mod)
	SPSuccess, spgadget, spbytes= disHereCleanPopR1(address, valCount, NumOpsDis, Reg, mod, "ok")
	# print "output: " + str(SPSuccess) + "  " + spgadget
	if SPSuccess:
		# addSpecialPOP(spgadget,spbytes)
		Reg=Reg.upper()
		if Reg == "EAX":
			if spgadget not in objs[o].specialPOPGadgetRetEAX:
				addSpecialPOP_RETEAX(spgadget,spbytes)
		if Reg == "EBX":
			if spgadget not in objs[o].specialPOPGadgetRetEBX:
				addSpecialPOP_RETEBX(spgadget,spbytes)
		if Reg == "ECX":
			if spgadget not in objs[o].specialPOPGadgetRetECX:
				addSpecialPOP_RETECX(spgadget,spbytes)			
		if Reg == "EDX":
			if spgadget not in objs[o].specialPOPGadgetRetEDX:
				addSpecialPOP_RETEDX(spgadget,spbytes)			
		if Reg == "ESI":
			if spgadget not in objs[o].specialPOPGadgetRetESI:
				addSpecialPOP_RETESI(spgadget,spbytes)			
		if Reg == "EDI":
			if spgadget not in objs[o].specialPOPGadgetRetEDI:
				addSpecialPOP_RETEDI(spgadget,spbytes)			
		if Reg == "EBP":
			if spgadget not in objs[o].specialPOPGadgetRetEBP:
				addSpecialPOP_RETEBP(spgadget,spbytes)			
		if Reg == "ESP":
			if spgadget not in objs[o].specialPOPGadgetRetESP:
				addSpecialPOP_RETESP(spgadget,spbytes)	

	return SPSuccess, spgadget, spbytes

def disHereCleanPop2(address, valCount, NumOpsDis,popReg, Reg, mod):
	spbytes =0
	SPSuccess=False
	SPSuccess, spgadget, spbytes= disHereCleanPop(address, valCount, NumOpsDis, popReg, Reg, "ok",999, mod)
	# print "output: " + str(SPSuccess) + "  " + spgadget
	if SPSuccess:
		# addSpecialPOP(spgadget,spbytes)
		Reg=Reg.upper()
		if Reg == "ALL":
			addSpecialPOP(spgadget,spbytes)
		if Reg == "EAX":
			addSpecialPOP_EAX(spgadget,spbytes)
		if Reg == "EBX":
			addSpecialPOP_EBX(spgadget,spbytes)
		if Reg == "ECX":
			addSpecialPOP_ECX(spgadget,spbytes)			
		if Reg == "EDX":
			addSpecialPOP_EDX(spgadget,spbytes)			
		if Reg == "ESI":
			addSpecialPOP_ESI(spgadget,spbytes)			
		if Reg == "EDI":
			addSpecialPOP_EDI(spgadget,spbytes)			
		if Reg == "EBP":
			addSpecialPOP_EBP(spgadget,spbytes)			
		if Reg == "ESP":
			addSpecialPOP_ESP(spgadget,spbytes)	

	return SPSuccess, spgadget, spbytes

def disHereCleanPop2Best(address, valCount, NumOpsDis, popReg, Reg,best, mod):
	spbytes =0
	SPSuccess=False
	# print "disherecleanpop2best " + popReg + " " + Reg
	SPSuccess, spgadget, spbytes= disHereCleanPop(address, valCount, NumOpsDis, popReg, Reg,"best",best, mod)
	if SPSuccess:
		Reg = Reg.upper()
		# print "we got it " + Reg + " "  + popReg 
		# print Reg
		# print spgadget
	# 	addSpecialPOPBest(spgadget,spbytes)
	# return SPSuccess, spgadget, spbytes
		if Reg == "ALL":
			addSpecialPOPBest(spgadget,spbytes)
		if Reg == "EAX":
			addSpecialPOPBestEAX(spgadget,spbytes)
			# print "saved"
		if Reg == "EBX":
			addSpecialPOPBestEBX(spgadget,spbytes)
		if Reg == "ECX":
			addSpecialPOPBestECX(spgadget,spbytes)			
		if Reg == "EDX":
			addSpecialPOPBestEDX(spgadget,spbytes)			
		if Reg == "ESI":
			addSpecialPOPBestESI(spgadget,spbytes)			
		if Reg == "EDI":
			addSpecialPOPBestEDI(spgadget,spbytes)			
		if Reg == "EBP":
			addSpecialPOPBestEBP(spgadget,spbytes)			
		if Reg == "ESP":
			addSpecialPOPBestESP(spgadget,spbytes)			
	return SPSuccess, spgadget, spbytes


def disHereCleanDG(address, valCount, NumOpsDis):
	#print hex(address)	
	#print " "
	#print valCount	
	CODED2 = b""
	x = NumOpsDis
	for i in range (x, 0, -1):
		try: 
			CODED2 += objs[o].data2[address-i]
		except IndexError:
			pass
	try:
		CODED2 += objs[o].data2[address]
	except IndexError:
		pass
	try:
		CODED2 += objs[o].data2[address+1]
	except IndexError:
		pass

	CODED2 += b"\x00"

	val =""
	val2 = []
	val3 = []
	address2 = address + objs[o].startLoc + 1000

	for i in cs.disasm(CODED2, address-x):
		add = hex(int(i.address))
		addb = hex(int(i.address +  objs[o].VirtualAdd))
		add2 = str(add)
		add3 = hex (int(i.address + objs[o].startLoc	))
		add4 = str(add3)
		val =  i.mnemonic + " " + i.op_str + "\t\t\t\t"  + add4 + " (offset " + addb + ")\n"
		val2.append(val)
		val3.append(add2)
		#print val
	
	#print "\n\n"

	returnVal = ""
	trueVal2Cnt = val2.__len__()
	z = 0
	#print "valCount method: \n"
	while (val2.__len__() < valCount):
	#	print val2[z]
		z = z + 1
		valCount = valCount -1
	##print "\n\n"
	####
	##print "\nAlernate method\n"
	trueVal2Cnt = val2.__len__()
	#print "trueVal2Cnt & valcount " + str(trueVal2Cnt) + " " + str(valCount)
	begin = trueVal2Cnt - valCount
	for i in val2[begin:valCount+1]:   #was +1
		print i
		returnVal += str(i)
	return returnVal
	####

def sortBytes(main,cnt,numOps, mod, byt):
	n = len(byt) 
	byt
	for i in range(n): 
		# Last i elements are already in place 
		for j in range(0, n-i-1): 
			# traverse the array from 0 to n-i-1 
			# Swap if the element found is greater 
			# than the next element 
			if byt[j] > byt[j+1] : 
				byt[j], byt[j+1] = byt[j+1], byt[j] 
				cnt[j], cnt[j+1] = cnt[j+1], cnt[j] 
				numOps[j], numOps[j+1] = numOps[j+1], numOps[j] 
				mod[j], mod[j+1] = mod[j+1], mod[j] 
				main[j], main[j+1] = main[j+1], main[j] 
	print byt  
	return main, cnt, numOps, mod, byt

def sortBytes2(main, byt):
	n = len(byt) 
	for i in range(n): 
		# Last i elements are already in place 
		for j in range(0, n-i-1): 
			# traverse the array from 0 to n-i-1 
			# Swap if the element found is greater 
			# than the next element 
			if byt[j] > byt[j+1] : 
				byt[j], byt[j+1] = byt[j+1], byt[j] 
				main[j], main[j+1] = main[j+1], main[j] 
	#print byt  
	return main, byt

def sortBytesSPAll():
	global o
	for obj in objs:
		main=objs[o].SpOutGadgetEAX
		byt=objs[o].SpOutNumBytesEAX
		main, byt = sortBytes2(main,byt)
		
		main=objs[o].SpOutGadgetEBX
		byt=objs[o].SpOutNumBytesEBX
		main, byt = sortBytes2(main,byt)

		main=objs[o].SpOutGadgetECX
		byt=objs[o].SpOutNumBytesECX
		main, byt = sortBytes2(main,byt)

		main=objs[o].SpOutGadgetEDX
		byt=objs[o].SpOutNumBytesEDX
		main, byt = sortBytes2(main,byt)

		main=objs[o].SpOutGadgetEDI
		byt=objs[o].SpOutNumBytesEDI
		main, byt = sortBytes2(main,byt)

		main=objs[o].SpOutGadgetESI
		byt=objs[o].SpOutNumBytesESI
		main, byt = sortBytes2(main,byt)

		main=objs[o].SpOutGadgetEBP
		byt=objs[o].SpOutNumBytesEBP
		main, byt = sortBytes2(main,byt)

		main=objs[o].SpOutGadgetESP
		byt=objs[o].SpOutNumBytesESP
		main, byt = sortBytes2(main,byt)

		print "\nSORTING ALL\nEAX stack pivots: " + str(len(objs[o].SpOutGadgetEAX))
		print "EBX stack pivots: " + str(len(objs[o].SpOutGadgetEBX))
		print "ECX stack pivots: " + str(len(objs[o].SpOutGadgetECX))
		print "EDX stack pivots: " + str(len(objs[o].SpOutGadgetEDX))
		print "EDI stack pivots: " + str(len(objs[o].SpOutGadgetEDI))
		print "ESI stack pivots: " + str(len(objs[o].SpOutGadgetESI))
		print "ESP stack pivots: " + str(len(objs[o].SpOutGadgetESP))
		print "EBP stack pivots: " + str(len(objs[o].SpOutGadgetEBP))
		print len(main)
		o = o + 1
	o=0
	#ok=raw_input()
	
vaNewCounter=1
vpNewCounter=1	
def counter ():
	global NewCounter
	NewCounter = NewCounter + 1
def counterMinus ():
	global NewCounter
	NewCounter = NewCounter -1
def counterReset ():
	global NewCounter
	NewCounter = 0


def vacounter ():
	global vaNewCounter
	vaNewCounter = vaNewCounter + 1
def vacounterReset ():
	global vaNewCounter
	vaNewCounter = 1
def vaCt():
	global vaNewCounter
	return "#" + str(vaNewCounter)


def vpcounter ():
	global vpNewCounter
	vpNewCounter = vpNewCounter + 1
def vpcounterReset ():
	global vpNewCounter
	vpNewCounter = 1
def vpCt():
	return "#" + str(vpNewCounter)

def Ct():
	return "#" + str(NewCounter)

def Ct2():
	return str(NewCounter)

def counterShow ():
	global NewCounter
	print "Counter: " + str(NewCounter)

def disHereDG(address, valCount, NumOpsDis, linesGoBack, HowDeep, Reg):
	w=0

	## Capstone does not seem to allow me to start disassemblying at a given point, so I copy out a chunk to  disassemble. I append a 0x00 because it does not always disassemble correctly (or at all) if just two bytes. I cause it not to be displayed through other means. It simply take the starting address of the jmp [reg], disassembles backwards, and copies it to a variable that I examine more closely.
	CODED2 = b""

	numOps = NumOpsDis # was x
	for i in range (numOps, 0, -1):  #was x
		CODED2 += objs[o].data2[address-i]
	CODED2 += objs[o].data2[address]
	CODED2 += objs[o].data2[address+1]
	CODED2 += b"\x00"

	val =""
	val2 = []
	valAdd = []
	address2 = address + objs[o].startLoc + 1000
	for i in cs.disasm(CODED2, address-numOps):  # was x
		
		add = hex(int(i.address))
		add2 = str(add)
		add3 = hex (int(i.address + objs[o].startLoc	+ objs[o].VirtualAdd))
		add4 = str(add3)
		val =  i.mnemonic + " " + i.op_str + "\t\t\t\t"  + add4 + " (offset " + add2 + ")\n"
		val2.append(val)
		valAdd.append(add2)

	tz = val2.__len__()
	#print tz
	tk=0
	save=0x00
	save2=0x00
	LinesSave=0
	for i, e in reversed(list(enumerate(val2))):
	    #print i, e
		tt = val2.__len__()   
		if tk < 1:
			save = valAdd[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1

		# Use regular expressions to find lines that have control flow and other undesired instructions, so they and preceding lines can be excised. 
		matchObj2 = re.compile( r"\badd\b|\badc\b|\bsub\b|\bsbb", re.M|re.I)
		if re.findall(matchObj2, e):   #if "ret"  in e:
			#print "ADD ******************\nfound: " + e
			if Reg == "JMP EAX" or Reg == "CALL EAX":
				matchObj2 = re.compile( r"\beax\b|\bax\b|\bal\b", re.M|re.I)
			if Reg == "JMP EBX" or Reg == "CALL EBX":
				matchObj2 = re.compile( r"\bebx\b|\bbx\b|\bbl\b", re.M|re.I)
			if Reg == "JMP ECX" or Reg == "CALL ECX":
				matchObj2 = re.compile( r"\becx\b|\bcx\b|\bcl\b", re.M|re.I)
			if Reg == "JMP EDX" or Reg == "CALL EDX":
				matchObj2 = re.compile( r"\bedx\b|\bdx\b|\bdl\b", re.M|re.I)
			if Reg == "JMP EDI" or Reg == "CALL EDI":
				matchObj2 = re.compile( r"\bedi\b|\bdi\b", re.M|re.I)
			if Reg == "JMP ESI" or Reg == "CALL ESI":
				matchObj2 = re.compile( r"\besi\b|\bsi\b", re.M|re.I)
			if Reg == "JMP EBP" or Reg == "CALL EBP":
				matchObj2 = re.compile( r"\bebp\b|\bbp\b", re.M|re.I)
			
			if re.findall(matchObj2, e):   #if "ret"  in e:
				#print "DG: add ******************\nfound: " + e 
				save2 = hex(address)
				LinesSave = i+linesGoBack  # was 3
				#print "DG: save2: " + str(save2)
				#print "DG: save3: " +  str(LinesSave)
				save2 = str(save2)   # Not sure why this is necessary, except for the absurdity of Python.
				save2 = int(save2, 16)
				#print "DG: save 2 & save 3 " + str(hex(save2)) + " " + str(LinesSave)
				addListBaseDG(save2, LinesSave, numOps, modName) # fist parameter: address of target jmp [reg]; second parameter: number of lines to go back.
				counter()
		if tk == HowDeep:   #This determines how far deep it goes searching for the Dispatcher gadget. That is, how many lines can be between the jmp/call [reg] and the add/sub
			break

def findDG_EAX(address, valCount, NumOpsDis, modName, linesGoBack, HowDeep):
	global w
	CODED2 = b""
	numOps = NumOpsDis # was x
	for i in range (numOps, 0, -1):  #was x
		CODED2 += objs[o].data2[address-i]
	CODED2 += objs[o].data2[address]
	CODED2 += objs[o].data2[address+1]
	CODED2 += b"\x00"
	val =""
	val2 = []
	valAdd = []
	val5 =[]

	for i in cs.disasm(CODED2, address-numOps):  # was x
		add = hex(int(i.address))
		add2 = str(add)
		add3 = hex (int(i.address + objs[o].startLoc	+ objs[o].VirtualAdd))
		add4 = str(add3)
		val =  i.mnemonic + " " + i.op_str + "\t\t\t\t"  + add4 + " (offset " + add2 + ")\n"
		val2.append(val)
		valAdd.append(add2)
		val5.append(val)
	tz = val2.__len__()
	tk=0
	save=0x00
	save2=0x00
	LinesSave=0
	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = valAdd[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1
		# Use regular expressions to find lines that have control flow and other undesired instructions, so they and preceding lines can be excised. 
		matchObj = re.match( r'\badd\b|\badc\b|\bsub\b|\bsbb\b', e, re.M|re.I)  #do inc or dec separate
		if matchObj: 
			matchObj = re.match( r'^[add|adc|sub|sbb]+ [e]*a[x|l|h]+|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[eax\]', e, re.M|re.I)
			if matchObj:
				matchObj2 = re.match( r'^[add|adc|sub|sbb]+ [e]*a[x|l|h]+, [e]*a[x|l|h]+|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[eax\], [e]*a[x|h|l]+|^[add|adc|sub|sbb]+ [e]*a[x|l|h]+, [byte|dword]+ ptr \[[e]*a[x|l|h]+|^[add|adc|sub|sbb]+ [e]*a[x|l|h]+[0-9a-fx] \t', e, re.M|re.I)
				if not matchObj2: 
					save2 = address
					LinesSave = i+linesGoBack  


					numLines= giveLineNum(val5,e)
					z =stupidPreJ(val5, numLines)
					if z == True:
						addListBaseDG_EAX(save2, numLines, NumOpsDis, modName)
					# addListBaseDG_EAX(save2, LinesSave, numOps, modName) 
					#print "bestbestbestbest\n\n\n"
					sp()
					counter()
					searchListBaseM(save2, numOps, objs[o].listOP_BaseDG_EAX, objs[o].listOP_BaseDG_NumOps_EAX, objs[o].listOP_BaseDG_CNT_EAX, objs[o].listOP_BaseDG_Module_EAX)
					matchObj3 = re.match( r'^[add|adc|sub|sbb]+ [e]*ax, [0x]*[0-9a-f]+[0-9a-f]*|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[eax\],[0x]*[0-9a-f]+[0-9a-f]*', e, re.M|re.I)
					if matchObj3:
						matchObj3 = re.match( r'^[add|adc|sub|sbb]+ [e]*ax, [0x]*[0-9a-f]+[0-9a-f]+[0-9a-f]+[0-9a-f]+|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[eax\], [0x]*[0-9a-f]+[0-9a-f]+[0-9a-f]+[0-9a-f]+', e, re.M|re.I)   
						if not matchObj3:

							numLines= giveLineNum(val5,e)
							z =stupidPreJ(val5, numLines)
							if z == True:
								addListBaseDG_EAX_Best(save2, numLines, NumOpsDis, modName)
							# addListBaseDG_EAX_Best(save2, LinesSave, numOps, modName) 
							#print "bestbestbestbest\n\n\n"

							sp()
		if tk == HowDeep:   #This determines how far deep it goes searching for the Dispatcher gadget. That is, how many lines can be between the jmp/call [reg] and the add/sub
			break

	#Mult/Div via Shifting - This way is very sub-par but  feasible in some circumstances. Sub-par for obvious reasons. There would need to be a separate way to add or dec the target register, as you can only shift left or shift right a few times. The intermediate changer could be a part of a functional gadget. These can also act on just 16 or 8 bit registers, which makes them far more viable. This is a way to do mult/div; both are these are very rare in JOP gadgets.

	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = valAdd[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1
		matchObj = re.match( r'\bshl\b|\bshr\b|\bsar\b|\bsal\b|\bshlb\b|\bshrb\b|\bsarb\b|\bsalb\b|\bshlw\b|\bshrw\b|\bsarw\b|\bsalw\b|\b', e, re.M|re.I)  #do inc or dec separate
		if matchObj: 
			matchObj = re.match( r'^s[h|a]+[l|r]+[dwl]* [e]*a[x|l|h]+, [1|2]+', e, re.M|re.I) #only 1 or 2 because anything else is too inconcievable, and shift left / shift right can provide can provide other options. 
			if matchObj:
				save2 = address
				LinesSave = i+linesGoBack
				addListBaseDG_EAX_Other(save2, LinesSave, numOps, modName)
		if tk == HowDeep:   #This determines how far deep it goes searching for the Dispatcher gadget. That is, how many lines can be between the jmp/call [reg] and the add/sub
			break

	#Multiplication - very rare for jop
	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = valAdd[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1
		matchObj = re.match( r'^imul[b|w|l]* [e]*ax, [e]*[abcdsp]+[xbpi]+', e, re.M|re.I)
		if matchObj:
			matchObj = re.match( r'^imul[b|w|l]* [e]*ax, [e]*[abcdsp]+[xbpi]+,', e, re.M|re.I)
			if not matchObj:
				save2 = address
				LinesSave = i+linesGoBack
				addListBaseDG_EAX_Other(save2, LinesSave, numOps, modName)
		if tk == HowDeep:   #This determines how far deep it goes searching for the Dispatcher gadget. That is, how many lines can be between the jmp/call [reg] and the add/sub
			break

		#Multiplication - very rare for jop - automatically saved in eax / edx
	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = valAdd[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1
		matchObj = re.match( r'^mul', e, re.M|re.I)  # mul will save in edx : eax or dx: ax by default, so any would work
		if matchObj:
			matchObj = re.match( r'^imul', e, re.M|re.I)
			if not matchObj:
				save2 = address
				LinesSave = i+linesGoBack
				addListBaseDG_EAX_Other(save2, LinesSave, numOps, modName)
		matchObj = re.match( r'^imul[b|w|l]* [e]*[abcdsp]+[xbpi]+', e, re.M|re.I)
		if matchObj:
			matchObj = re.match( r'^imul[b|w|l]* [e]*[abcdsp]+[xbpi]+,', e, re.M|re.I)
			if not matchObj:
				save2 = address
				LinesSave = i+linesGoBack
				addListBaseDG_EAX_Other(save2, LinesSave, numOps, modName)	
		if tk == HowDeep:   #This determines how far deep it goes searching for the Dispatcher gadget. That is, how many lines can be between the jmp/call [reg] and the add/sub
			break

def findDG_EBX(address, valCount, NumOpsDis, modName, linesGoBack, HowDeep):
	CODED2 = b""
	numOps = NumOpsDis # was x
	for i in range (numOps, 0, -1):  #was x
		CODED2 += objs[o].data2[address-i]
	CODED2 += objs[o].data2[address]
	CODED2 += objs[o].data2[address+1]
	CODED2 += b"\x00"
	val =""
	val2 = []
	valAdd = []
	val5 =[]

	for i in cs.disasm(CODED2, address-numOps):  # was x
		
		add = hex(int(i.address))
		add2 = str(add)
		add3 = hex (int(i.address + objs[o].startLoc	+ objs[o].VirtualAdd))
		add4 = str(add3)
		val =  i.mnemonic + " " + i.op_str + "\t\t\t\t"  + add4 + " (offset " + add2 + ")\n"
		val2.append(val)
		valAdd.append(add2)
		val5.append(val)
	tz = val2.__len__()
	tk=0
	save=0x00
	save2=0x00
	LinesSave=0
	
	# print "start"
	# for x, in reversed(list(enumerate(val2))):
	# 	print x
	z=0
	for i, e in reversed(list(enumerate(val2))):

		# tt = val2.__len__()   
		# if tk < 1:
		# 	save = valAdd[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		# tk += 1
		# Use regular expressions to find lines that have control flow and other undesired instructions, so they and preceding lines can be excised. 
		# print "y " +str(i)  + " z  " + str(z) + "  "  + val2[i] + " i " 
		matchObj = re.match( r'\badd\b|\badc\b|\bsub\b|\bsbb\b', val2[i], re.M|re.I)  #do inc or dec separate

		if matchObj: 
			matchObj = re.match( r'^[add|adc|sub|sbb]+ [e]*b[x|l|h]+|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[ebx\]', val2[i], re.M|re.I)
			if matchObj:
			#	print "step2"
			#	print e				
				matchObj2 = re.match( r'^[add|adc|sub|sbb]+ [e]*b[x|l|h]+, [e]*b[x|l|h]+|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[ebx\], [e]*b[x|h|l]+|^[add|adc|sub|sbb]+ [e]*b[x|l|h]+, [byte|dword]+ ptr \[[e]*b[x|l|h]+|^[add|adc|sub|sbb]+ [e]*b[x|l|h]+[0-9a-fx] \t', val2[i], re.M|re.I)
				if not matchObj2: 
		
					save2 = address
					LinesSave = i
					# print "debug:"
					# print valCount
					# print linesGoBack
					# print i
					# print LinesSave
					# modName=val2[i]

					numLines= giveLineNum(val5,e)
					z =stupidPreJ(val5, numLines)
					if z == True:
						addListBaseDG_EBX(save2, numLines, NumOpsDis, modName)
					# addListBaseDG_EBX(save2, LinesSave, numOps, modName) # fist parameter: address of target jmp [reg]; second parameter: number of lines to go back.
					#addListBaseDG(save2, LinesSave, numOps, modName)
					# print "DG save " + str(save) + " i " + str(i) + " numops " + str(numOps) + "" + val2[i]
  					counter()
					searchListBaseM(save2, numOps, objs[o].listOP_BaseDG_EBX, objs[o].listOP_BaseDG_NumOps_EBX, objs[o].listOP_BaseDG_CNT_EBX, objs[o].listOP_BaseDG_Module_EBX)
					matchObj3 = re.match( r'^[add|adc|sub|sbb]+ [e]*bx, [0x]*[0-9a-f]+[0-9a-f]*|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[ebx\],[0x]*[0-9a-f]+[0-9a-f]*', e, re.M|re.I)
					if matchObj3:
						matchObj3 = re.match( r'^[add|adc|sub|sbb]+ [e]*bx, [0x]*[0-9a-f]+[0-9a-f]+[0-9a-f]+[0-9a-f]+|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[ebx\], [0x]*[0-9a-f]+[0-9a-f]+[0-9a-f]+[0-9a-f]+', e, re.M|re.I)   #It is defined as really good if it is 0x01- 0xfff. I found this necessary to express in two nested lines.
						if not matchObj3:
							# print "DG best save " + str(save) + " i " + str(i) + " numops " + str(numOps) + "" + val2[i]


							numLines= giveLineNum(val5,e)
							z =stupidPreJ(val5, numLines)
							if z == True:
								addListBaseDG_EBX_Best(save2, numLines, NumOpsDis, modName)

							# addListBaseDG_EBX_Best(save2, LinesSave, numOps, modName) # fist parameter: address of 
		z+=1
		if tk == HowDeep:   #This determines how far deep it goes searching for the Dispatcher gadget. That is, how many lines can be between the jmp/call [reg] and the add/sub
			break

	#Mult/Div via Shifting - This way is very sub-par but  feasible in some circumstances. Sub-par for obvious reasons. There would need to be a separate way to add or dec the target register, as you can only shift left or shift right a few times. The intermediate changer could be a part of a functional gadget. These can also act on just 16 or 8 bit registers, which makes them far more viable. This is a way to do mult/div; both are these are very rare in JOP gadgets.

	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = valAdd[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1
		matchObj = re.match( r'\bshl\b|\bshr\b|\bsar\b|\bsal\b|\bshlb\b|\bshrb\b|\bsarb\b|\bsalb\b|\bshlw\b|\bshrw\b|\bsarw\b|\bsalw\b|\b', e, re.M|re.I)  #do inc or dec separate
		if matchObj: 
			matchObj = re.match( r'^s[h|a]+[l|r]+[dwl]* [e]*b[x|l|h]+, [1|2]+', e, re.M|re.I) #only 1 or 2 because anything else is too inconcievable, and shift left / shift right can provide can provide other options. 
			if matchObj:
				save2 = address
				LinesSave = i+linesGoBack
				addListBaseDG_EBX_Other(save2, LinesSave, numOps, modName)
				# print "DG save other " + str(save) + " i " + str(i) + " numops " + str(numOps) + "" + val2[i]
		if tk == HowDeep:   #This determines how far deep it goes searching for the Dispatcher gadget. That is, how many lines can be between the jmp/call [reg] and the add/sub
			break

	#Multiplication - very rare for jop
	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = valAdd[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1
		matchObj = re.match( r'^imul[b|w|l]* [e]*bx, [e]*[abcdsp]+[xbpi]+', e, re.M|re.I)
		if matchObj:
			matchObj = re.match( r'^imul[b|w|l]* [e]*bx, [e]*[abcdsp]+[xbpi]+,', e, re.M|re.I)
			if not matchObj:
				save2 = address
				LinesSave = i+linesGoBack
				addListBaseDG_EBX_Other(save2, LinesSave, numOps, modName)
				# print "DG save other2" + str(save) + " i " + str(i) + " numops " + str(numOps) + "" + val2[i]
		if tk == HowDeep:   #This determines how far deep it goes searching for the Dispatcher gadget. That is, how many lines can be between the jmp/call [reg] and the add/sub
			break

def searchListBase(address, NumOpsDis):
	global o 
	t=0
	for i, each in enumerate(objs[o].listOP_BaseDG_ECX):
		#print "i " + str(i)
		if address == objs[o].listOP_BaseDG_ECX[i]:
			if NumOpsDis == objs[o].listOP_BaseDG_NumOps_ECX[i]:
		#		print "i " + str(i)
				#print "cool\n\n\n"
				t=t + 1
				if t > 1:
					del objs[o].listOP_BaseDG_ECX[i]
					del objs[o].listOP_BaseDG_CNT_ECX[i]
					del objs[o].listOP_BaseDG_NumOps_ECX[i]
					del objs[o].listOP_BaseDG_Module_ECX[i]
					#print "cool\n\n\n"
		i = i + 1


def searchListBaseM(address, NumOpsDis, b,bN, bC, bM):
	global o 
	t=0
	for i, each in enumerate(b):
		if address == b[i]:
			if NumOpsDis == bN[i]:
				t=t + 1
				if t > 1:
					del b[i]
					del bC[i]
					del bN[i]
					del bM[i]
					#print "cool\n\n\n"
					#print b
		i = i + 1
	#return msg
def searchListBase1(address, NumOpsDis):
	global o 
#	i=0
	t=0
	for i, each in enumerate(listOP_Base):
		if address == listOP_Base[i]:
			if NumOpsDis == listOP_Base_NumOps[i]:
				#print "cool1\n\n\n"
				t=t + 1
				if t > 1:
					del listOP_Base[i]
					del listOP_Base_NumOps[i]
					del listOP_Base_CNT[i]
					del listOP_Base_Module[i]
					#print "cool11\n\n\n"
					#print listOP_Base
		i = i + 1
	#return msg
def findDG_ECX(address, valCount, NumOpsDis, modName, linesGoBack, HowDeep):
	#print "find"
	CODED2 = b""
	numOps = NumOpsDis # was x
	for i in range (numOps, 0, -1):  #was x
		CODED2 += objs[o].data2[address-i]
	CODED2 += objs[o].data2[address]
	CODED2 += objs[o].data2[address+1]
	CODED2 += b"\x00"
	val =""
	val2 = []
	valAdd = []
	val5 =[]

	sp()
	for i in cs.disasm(CODED2, address-numOps):  # was x
		
		add = hex(int(i.address))
		add2 = str(add)
		add3 = hex (int(i.address + objs[o].startLoc	+ objs[o].VirtualAdd))
		add4 = str(add3)
		val =  i.mnemonic + " " + i.op_str + "\t\t\t\t"  + add4 + " (offset " + add2 + ")\n"
		val2.append(val)
		valAdd.append(add2)
		val5.append(val)
	tz = val2.__len__()
	tk=0
	save=0x00
	save2=0x00
	LinesSave=0
	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = valAdd[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1
		# Use regular expressions to find lines that have control flow and other undesired instructions, so they and preceding lines can be excised. 
		matchObj = re.match( r'\badd\b|\badc\b|\bsub\b|\bsbb\b', e, re.M|re.I)  #do inc or dec separate
		
		if matchObj: 
			matchObj = re.match( r'^[add|adc|sub|sbb]+ [e]*c[x|l|h]+|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[ecx\]', e, re.M|re.I)
			if matchObj:
		
				#print e				
				matchObj2 = re.match( r'^[add|adc|sub|sbb]+ [e]*c[x|l|h]+, [e]*c[x|l|h]+|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[ecx\], [e]*c[x|h|l]+|^[add|adc|sub|sbb]+ [e]*c[x|l|h]+, [byte|dword]+ ptr \[[e]*c[x|l|h]+|^[add|adc|sub|sbb]+ [e]*c[x|l|h]+[0-9a-fx] \t', e, re.M|re.I)
				if not matchObj2: 
				#	print "Found DG2"
		#			print e				
					save2 = address
					LinesSave = i+linesGoBack

					numLines= giveLineNum(val5,e)
					z =stupidPreJ(val5, numLines)
					if z == True:
						addListBaseDG_ECX(save2, numLines, NumOpsDis, modName)
					# addListBaseDG_ECX(save2, LinesSave, numOps, modName) # fist parameter: address of target jmp [reg]; second parameter: number of lines to go back.
					#addListBaseDG(save2, LinesSave, numOps, modName)
					#searchListBase(save2, numOps)
					searchListBaseM(save2, numOps, objs[o].listOP_BaseDG_ECX, objs[o].listOP_BaseDG_NumOps_ECX, objs[o].listOP_BaseDG_CNT_ECX, objs[o].listOP_BaseDG_Module_ECX)
					#print "adding"
					sp()
					counter()
					matchObj3 = re.match( r'^[add|adc|sub|sbb]+ [e]*cx, [0x]*[0-9a-f]+[0-9a-f]*|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[ecx\],[0x]*[0-9a-f]+[0-9a-f]*', e, re.M|re.I)
					if matchObj3:
						matchObj3 = re.match( r'^[add|adc|sub|sbb]+ [e]*cx, [0x]*[0-9a-f]+[0-9a-f]+[0-9a-f]+[0-9a-f]+|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[ecx\], [0x]*[0-9a-f]+[0-9a-f]+[0-9a-f]+[0-9a-f]+', e, re.M|re.I)   #It is defined as really good if it is 0x01- 0xfff. I found this necessary to express in two nested lines.
						if not matchObj3:

							numLines= giveLineNum(val5,e)
							z =stupidPreJ(val5, numLines)
							if z == True:
								addListBaseDG_ECX_Best(save2, numLines, NumOpsDis, modName)
							# addListBaseDG_ECX_Best(save2, LinesSave, numOps, modName) # fist parameter: address of 
		if tk == HowDeep:   #This determines how far deep it goes searching for the Dispatcher gadget. That is, how many lines can be between the jmp/call [reg] and the add/sub
			break

	#Mult/Div via Shifting - This way is very sub-par but  feasible in some circumstances. Sub-par for obvious reasons. There would need to be a separate way to add or dec the target register, as you can only shift left or shift right a few times. The intermediate changer could be a part of a functional gadget. These can also act on just 16 or 8 bit registers, which makes them far more viable. This is a way to do mult/div; both are these are very rare in JOP gadgets.

	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = valAdd[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1
		matchObj = re.match( r'\bshl\b|\bshr\b|\bsar\b|\bsal\b|\bshlb\b|\bshrb\b|\bsarb\b|\bsalb\b|\bshlw\b|\bshrw\b|\bsarw\b|\bsalw\b|\b', e, re.M|re.I)  #do inc or dec separate
		if matchObj: 
			matchObj = re.match( r'^s[h|a]+[l|r]+[dwl]* [e]*c[x|l|h]+, [1|2]+', e, re.M|re.I) #only 1 or 2 because anything else is too inconcievable, and shift left / shift right can provide can provide other options. 
			if matchObj:
				save2 = address
				LinesSave = i+linesGoBack
				addListBaseDG_ECX_Other(save2, LinesSave, numOps, modName)
		if tk == HowDeep:   #This determines how far deep it goes searching for the Dispatcher gadget. That is, how many lines can be between the jmp/call [reg] and the add/sub
			break

	#Multiplication - very rare for jop
	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = valAdd[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1
		matchObj = re.match( r'^imul[b|w|l]* [e]*cx, [e]*[abcdsp]+[xbpi]+', e, re.M|re.I)
		if matchObj:
			matchObj = re.match( r'^imul[b|w|l]* [e]*cx, [e]*[abcdsp]+[xbpi]+,', e, re.M|re.I)
			if not matchObj:
				save2 = address
				LinesSave = i+linesGoBack
				addListBaseDG_ECX_Other(save2, LinesSave, numOps, modName)
		if tk == HowDeep:   #This determines how far deep it goes searching for the Dispatcher gadget. That is, how many lines can be between the jmp/call [reg] and the add/sub
			break


def findDG_EDX(address, valCount, NumOpsDis, modName, linesGoBack, HowDeep):
	CODED2 = b""
	numOps = NumOpsDis # was x
	for i in range (numOps, 0, -1):  #was x
		CODED2 += objs[o].data2[address-i]
	CODED2 += objs[o].data2[address]
	CODED2 += objs[o].data2[address+1]
	CODED2 += b"\x00"
	val =""
	val2 = []
	valAdd = []
	val5 =[]

	
	for i in cs.disasm(CODED2, address-numOps):  # was x
		
		add = hex(int(i.address))
		add2 = str(add)
		add3 = hex (int(i.address + objs[o].startLoc	+ objs[o].VirtualAdd))
		add4 = str(add3)
		val =  i.mnemonic + " " + i.op_str + "\t\t\t\t"  + add4 + " (offset " + add2 + ")\n"
		val2.append(val)
		valAdd.append(add2)
		val5.append(val)
	tz = val2.__len__()
	tk=0
	save=0x00
	save2=0x00
	LinesSave=0
	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = valAdd[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1
		# Use regular expressions to find lines that have control flow and other undesired instructions, so they and preceding lines can be excised. 
		matchObj = re.match( r'\badd\b|\badc\b|\bsub\b|\bsbb\b', e, re.M|re.I)  #do inc or dec separate
			
		if matchObj: 
			matchObj = re.match( r'^[add|adc|sub|sbb]+ [e]*d[x|l|h]+|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[edx\]', e, re.M|re.I)
			if matchObj:
				matchObj2 = re.match( r'^[add|adc|sub|sbb]+ [e]*d[x|l|h]+, [e]*d[x|l|h]+|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[edx\], [e]*d[x|h|l]+|^[add|adc|sub|sbb]+ [e]*d[x|l|h]+, [byte|dword]+ ptr \[[e]*d[x|l|h]+|^[add|adc|sub|sbb]+ [e]*d[x|l|h]+[0-9a-fx] \t', e, re.M|re.I)
				if not matchObj2: 
					#print "Found DG2"
					#print e				
					save2 = address
					LinesSave = i+linesGoBack

					numLines= giveLineNum(val5,e)
					z =stupidPreJ(val5, numLines)
					if z == True:
						addListBaseDG_EDX(save2, numLines, NumOpsDis, modName)
					# addListBaseDG_EDX(save2, LinesSave, numOps, modName) # fist parameter: address of target jmp [reg]; second parameter: number of lines to go back.
					#addListBaseDG(save2, LinesSave, numOps, modName)
					searchListBaseM(save2, numOps, objs[o].listOP_BaseDG_EDX, objs[o].listOP_BaseDG_NumOps_EDX, objs[o].listOP_BaseDG_CNT_EDX, objs[o].listOP_BaseDG_Module_EDX)
					counter()
					matchObj3 = re.match( r'^[add|adc|sub|sbb]+ [e]*dx, [0x]*[0-9a-f]+[0-9a-f]*|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[edx\],[0x]*[0-9a-f]+[0-9a-f]*', e, re.M|re.I)
					if matchObj3:
						matchObj3 = re.match( r'^[add|adc|sub|sbb]+ [e]*dx, [0x]*[0-9a-f]+[0-9a-f]+[0-9a-f]+[0-9a-f]+|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[edx\], [0x]*[0-9a-f]+[0-9a-f]+[0-9a-f]+[0-9a-f]+', e, re.M|re.I)   #It is defined as really good if it is 0x01- 0xfff. I found this necessary to express in two nested lines.
						if not matchObj3:

							numLines= giveLineNum(val5,e)
							z =stupidPreJ(val5, numLines)
							if z == True:
								addListBaseDG_EDX_Best(save2, numLines, NumOpsDis, modName)
							# addListBaseDG_EDX_Best(save2, LinesSave, numOps, modName) # fist parameter: address of 
		if tk == HowDeep:   #This determines how far deep it goes searching for the Dispatcher gadget. That is, how many lines can be between the jmp/call [reg] and the add/sub
			break

	#Mult/Div via Shifting - This way is very sub-par but  feasible in some circumstances. Sub-par for obvious reasons. There would need to be a separate way to add or dec the target register, as you can only shift left or shift right a few times. The intermediate changer could be a part of a functional gadget. These can also act on just 16 or 8 bit registers, which makes them far more viable. This is a way to do mult/div; both are these are very rare in JOP gadgets.

	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = valAdd[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1
		matchObj = re.match( r'\bshl\b|\bshr\b|\bsar\b|\bsal\b|\bshlb\b|\bshrb\b|\bsarb\b|\bsalb\b|\bshlw\b|\bshrw\b|\bsarw\b|\bsalw\b|\b', e, re.M|re.I)  #do inc or dec separate
		if matchObj: 
			matchObj = re.match( r'^s[h|a]+[l|r]+[dwl]* [e]*d[x|l|h]+, [1|2]+', e, re.M|re.I) #only 1 or 2 because anything else is too inconcievable, and shift left / shift right can provide can provide other options. 
			if matchObj:
				save2 = address
				LinesSave = i+linesGoBack
				addListBaseDG_EDX_Other(save2, LinesSave, numOps, modName)
		if tk == HowDeep:   #This determines how far deep it goes searching for the Dispatcher gadget. That is, how many lines can be between the jmp/call [reg] and the add/sub
			break

	#Multiplication - very rare for jop
	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = valAdd[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1
		matchObj = re.match( r'^imul[b|w|l]* [e]*dx, [e]*[abcdsp]+[xbpi]+', e, re.M|re.I)
		if matchObj:
			matchObj = re.match( r'^imul[b|w|l]* [e]*dx, [e]*[abcdsp]+[xbpi]+,', e, re.M|re.I)
			if not matchObj:
				save2 = address
				LinesSave = i+linesGoBack
				addListBaseDG_EDX_Other(save2, LinesSave, numOps, modName)
		if tk == HowDeep:   #This determines how far deep it goes searching for the Dispatcher gadget. That is, how many lines can be between the jmp/call [reg] and the add/sub
			break

		#Multiplication - very rare for jop - automatically saved in eax / edx
	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = valAdd[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1
		matchObj = re.match( r'^mul', e, re.M|re.I)  # mul will save in edx : eax or dx: ax by default, so any would work
		if matchObj:
			matchObj = re.match( r'^imul', e, re.M|re.I)
			if not matchObj:
				save2 = address
				LinesSave = i+linesGoBack
				addListBaseDG_EDX_Other(save2, LinesSave, numOps, modName)
		matchObj = re.match( r'^imul[b|w|l]* [e]*[abcdsp]+[xbpi]+', e, re.M|re.I)
		if matchObj:
			matchObj = re.match( r'^imul[b|w|l]* [e]*[abcdsp]+[xbpi]+,', e, re.M|re.I)
			if not matchObj:
				save2 = address
				LinesSave = i+linesGoBack
				addListBaseDG_EDX_Other(save2, LinesSave, numOps, modName)	
		if tk == HowDeep:   #This determines how far deep it goes searching for the Dispatcher gadget. That is, how many lines can be between the jmp/call [reg] and the add/sub
			break
def findDG_EDI(address, valCount, NumOpsDis, modName, linesGoBack, HowDeep):
	CODED2 = b""
	numOps = NumOpsDis # was x
	for i in range (numOps, 0, -1):  #was x
		CODED2 += objs[o].data2[address-i]
	CODED2 += objs[o].data2[address]
	CODED2 += objs[o].data2[address+1]
	CODED2 += b"\x00"
	val =""
	val2 = []
	valAdd = []
	val5 =[]

	
	for i in cs.disasm(CODED2, address-numOps):  # was x
		
		add = hex(int(i.address))
		add2 = str(add)
		add3 = hex (int(i.address + objs[o].startLoc	+ objs[o].VirtualAdd))
		add4 = str(add3)
		val =  i.mnemonic + " " + i.op_str + "\t\t\t\t"  + add4 + " (offset " + add2 + ")\n"
		val2.append(val)
		valAdd.append(add2)
		val5.append(val)
	tz = val2.__len__()
	tk=0
	save=0x00
	save2=0x00
	LinesSave=0
	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = valAdd[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1
		# Use regular expressions to find lines that have control flow and other undesired instructions, so they and preceding lines can be excised. 
		matchObj = re.match( r'\badd\b|\badc\b|\bsub\b|\bsbb\b', e, re.M|re.I)  #do inc or dec separate
			
		if matchObj: 
			matchObj = re.match( r'^[add|adc|sub|sbb]+ [e]*di|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[edi\]', e, re.M|re.I)
			if matchObj:
				#print "step2"
				#print e				
				matchObj2 = re.match( r'^[add|adc|sub|sbb]+ [e]*di, [e]*di|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[edi\], [e]*di|^[add|adc|sub|sbb]+ [e]*di, [byte|dword]+ ptr \[[e]*di|^[add|adc|sub|sbb]+ [e]*di[0-9a-fx] \t', e, re.M|re.I)
				if not matchObj2: 
					#print "Found DG2"
					#print e				
					save2 = address
					LinesSave = i+linesGoBack

					numLines= giveLineNum(val5,e)
					z =stupidPreJ(val5, numLines)
					if z == True:
						addListBaseDG_EDI(save2, numLines, NumOpsDis, modName)
					# addListBaseDG_EDI(save2, LinesSave, numOps, modName) # fist parameter: address of target jmp [reg]; second parameter: number of lines to go back.
					#addListBaseDG(save2, LinesSave, numOps, modName)
					searchListBaseM(save2, numOps, objs[o].listOP_BaseDG_EDI, objs[o].listOP_BaseDG_NumOps_EDI, objs[o].listOP_BaseDG_CNT_EDI, objs[o].listOP_BaseDG_Module_EDI)
					counter()

					matchObj3 = re.match( r'^[add|adc|sub|sbb]+ [e]*di, [0x]*[0-9a-f]+[0-9a-f]*|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[edi\],[0x]*[0-9a-f]+[0-9a-f]*', e, re.M|re.I)
					if matchObj3:
						matchObj3 = re.match( r'^[add|adc|sub|sbb]+ [e]*di, [0x]*[0-9a-f]+[0-9a-f]+[0-9a-f]+[0-9a-f]+|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[edi\], [0x]*[0-9a-f]+[0-9a-f]+[0-9a-f]+[0-9a-f]+', e, re.M|re.I)   #It is defined as really good if it is 0x01- 0xfff. I found this necessary to express in two nested lines.
						if not matchObj3:

							numLines= giveLineNum(val5,e)
							z =stupidPreJ(val5, numLines)
							if z == True:
								addListBaseDG_EDI_Best(save2, numLines, NumOpsDis, modName)
							# addListBaseDG_EDI_Best(save2, LinesSave, numOps, modName) # fist parameter: address of 
		if tk == HowDeep:   #This determines how far deep it goes searching for the Dispatcher gadget. That is, how many lines can be between the jmp/call [reg] and the add/sub
			break
	#Mult/Div via Shifting - This way is very sub-par but  feasible in some circumstances. Sub-par for obvious reasons. There would need to be a separate way to add or dec the target register, as you can only shift left or shift right a few times. The intermediate changer could be a part of a functional gadget. These can also act on just 16 or 8 bit registers, which makes them far more viable. This is a way to do mult/div; both are these are very rare in JOP gadgets.

	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = valAdd[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1
		matchObj = re.match( r'\bshl\b|\bshr\b|\bsar\b|\bsal\b|\bshlb\b|\bshrb\b|\bsarb\b|\bsalb\b|\bshlw\b|\bshrw\b|\bsarw\b|\bsalw\b|\b', e, re.M|re.I)  #do inc or dec separate
		if matchObj: 
			matchObj = re.match( r'^s[h|a]+[l|r]+[dwl]* [e]*di+, [1|2]+', e, re.M|re.I) #only 1 or 2 because anything else is too inconcievable, and shift left / shift right can provide can provide other options. 
			if matchObj:
				save2 = address
				LinesSave = i+linesGoBack
				addListBaseDG_EDI_Other(save2, LinesSave, numOps, modName)
		if tk == HowDeep:   #This determines how far deep it goes searching for the Dispatcher gadget. That is, how many lines can be between the jmp/call [reg] and the add/sub
			break

	#Multiplication - very rare for jop
	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = valAdd[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1
		matchObj = re.match( r'^imul[b|w|l]* [e]*di, [e]*[abcdsp]+[xbpi]+', e, re.M|re.I)
		if matchObj:
			matchObj = re.match( r'^imul[b|w|l]* [e]*di, [e]*[abcdsp]+[xbpi]+,', e, re.M|re.I)
			if not matchObj:
				save2 = address
				LinesSave = i+linesGoBack
				addListBaseDG_EDI_Other(save2, LinesSave, numOps, modName)
		if tk == HowDeep:   #This determines how far deep it goes searching for the Dispatcher gadget. That is, how many lines can be between the jmp/call [reg] and the add/sub
			break

def findDG_ESI(address, valCount, NumOpsDis, modName, linesGoBack, HowDeep):
	CODED2 = b""
	numOps = NumOpsDis # was x
	for i in range (numOps, 0, -1):  #was x
		CODED2 += objs[o].data2[address-i]
	CODED2 += objs[o].data2[address]
	CODED2 += objs[o].data2[address+1]
	CODED2 += b"\x00"
	val =""
	val2 = []
	valAdd = []
	val5 =[]

	for i in cs.disasm(CODED2, address-numOps):  # was x
		
		add = hex(int(i.address))
		add2 = str(add)
		add3 = hex (int(i.address + objs[o].startLoc	+ objs[o].VirtualAdd))
		add4 = str(add3)
		val =  i.mnemonic + " " + i.op_str + "\t\t\t\t"  + add4 + " (offset " + add2 + ")\n"
		val2.append(val)
		valAdd.append(add2)
		val5.append(val)
	tz = val2.__len__()
	tk=0
	save=0x00
	save2=0x00
	LinesSave=0
	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = valAdd[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1
		# Use regular expressions to find lines that have control flow and other undesired instructions, so they and preceding lines can be excised. 
		matchObj = re.match( r'\badd\b|\badc\b|\bsub\b|\bsbb\b', e, re.M|re.I)  #do inc or dec separate
			
		if matchObj: 
			matchObj = re.match( r'^[add|adc|sub|sbb]+ [e]*si|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[esi\]', e, re.M|re.I)
			if matchObj:
				#print "step2"
				#print e				
				matchObj2 = re.match( r'^[add|adc|sub|sbb]+ [e]*si, [e]*si|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[esi\], [e]*si|^[add|adc|sub|sbb]+ [e]*si, [byte|dword]+ ptr \[[e]*si|^[add|adc|sub|sbb]+ [e]*si[0-9a-fx] \t', e, re.M|re.I)
				if not matchObj2: 
					#print "Found DG2"
				#	print e				
					save2 = address
					numLines= giveLineNum(val5,e)
					z =stupidPreJ(val5, numLines)
					if z == True:
						addListBaseDG_ESI(save2, numLines, NumOpsDis, modName)
					# addListBaseDG_ESI(save2, LinesSave, numOps, modName) # fist parameter: address of target jmp [reg]; second parameter: number of lines to go back.
					#addListBaseDG(save2, LinesSave, numOps, modName)
					searchListBaseM(save2, numOps, objs[o].listOP_BaseDG_ESI, objs[o].listOP_BaseDG_NumOps_ESI, objs[o].listOP_BaseDG_CNT_ESI, objs[o].listOP_BaseDG_Module_ESI)
					counter()
					matchObj3 = re.match( r'^[add|adc|sub|sbb]+ [e]*si, [0x]*[0-9a-f]+[0-9a-f]*|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[esi\],[0x]*[0-9a-f]+[0-9a-f]*', e, re.M|re.I)
					if matchObj3:
						matchObj3 = re.match( r'^[add|adc|sub|sbb]+ [e]*si, [0x]*[0-9a-f]+[0-9a-f]+[0-9a-f]+[0-9a-f]+|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[esi\], [0x]*[0-9a-f]+[0-9a-f]+[0-9a-f]+[0-9a-f]+', e, re.M|re.I)   #It is defined as really good if it is 0x01- 0xfff. I found this necessary to express in two nested lines.
						if not matchObj3:

							numLines= giveLineNum(val5,e)
							z =stupidPreJ(val5, numLines)
							if z == True:
								addListBaseDG_ESI_Best(save2, numLines, NumOpsDis, modName)
							# addListBaseDG_ESI_Best(save2, LinesSave, numOps, modName) # fist parameter: address of 
		if tk == HowDeep:   #This determines how far deep it goes searching for the Dispatcher gadget. That is, how many lines can be between the jmp/call [reg] and the add/sub
			break

	#Mult/Div via Shifting - This way is very sub-par but  feasible in some circumstances. Sub-par for obvious reasons. There would need to be a separate way to add or dec the target register, as you can only shift left or shift right a few times. The intermediate changer could be a part of a functional gadget. These can also act on just 16 or 8 bit registers, which makes them far more viable. This is a way to do mult/div; both are these are very rare in JOP gadgets.

	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = valAdd[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1
		matchObj = re.match( r'\bshl\b|\bshr\b|\bsar\b|\bsal\b|\bshlb\b|\bshrb\b|\bsarb\b|\bsalb\b|\bshlw\b|\bshrw\b|\bsarw\b|\bsalw\b|\b', e, re.M|re.I)  #do inc or dec separate
		if matchObj: 
			matchObj = re.match( r'^s[h|a]+[l|r]+[dwl]* [e]*si, [1|2]+', e, re.M|re.I) #only 1 or 2 because anything else is too inconcievable, and shift left / shift right can provide can provide other options. 
			if matchObj:
				save2 = address
				LinesSave = i+linesGoBack
				addListBaseDG_ESI_Other(save2, LinesSave, numOps, modName)
		if tk == HowDeep:   #This determines how far deep it goes searching for the Dispatcher gadget. That is, how many lines can be between the jmp/call [reg] and the add/sub
			break

	#Multiplication - very rare for jop
	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = valAdd[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1
		matchObj = re.match( r'^imul[b|w|l]* [e]*si, [e]*[abcdsp]+[xbpi]+', e, re.M|re.I)
		if matchObj:
			matchObj = re.match( r'^imul[b|w|l]* [e]*si, [e]*[abcdsp]+[xbpi]+,', e, re.M|re.I)
			if not matchObj:
				save2 = address
				LinesSave = i+linesGoBack
				addListBaseDG_ESI_Other(save2, LinesSave, numOps, modName)
		if tk == HowDeep:   #This determines how far deep it goes searching for the Dispatcher gadget. That is, how many lines can be between the jmp/call [reg] and the add/sub
			break

def findDG_EBP(address, valCount, NumOpsDis, modName, linesGoBack, HowDeep):
	CODED2 = b""
	numOps = NumOpsDis # was x
	for i in range (numOps, 0, -1):  #was x
		CODED2 += objs[o].data2[address-i]
	CODED2 += objs[o].data2[address]
	CODED2 += objs[o].data2[address+1]
	CODED2 += b"\x00"
	val =""
	val2 = []
	valAdd = []
	val5 =[]

	
	for i in cs.disasm(CODED2, address-numOps):  # was x
		
		add = hex(int(i.address))
		add2 = str(add)
		add3 = hex (int(i.address + objs[o].startLoc	+ objs[o].VirtualAdd))
		add4 = str(add3)
		val =  i.mnemonic + " " + i.op_str + "\t\t\t\t"  + add4 + " (offset " + add2 + ")\n"
		val2.append(val)
		valAdd.append(add2)
		val5.append(val)
	tz = val2.__len__()
	tk=0
	save=0x00
	save2=0x00
	LinesSave=0
	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = valAdd[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1
		# Use regular expressions to find lines that have control flow and other undesired instructions, so they and preceding lines can be excised. 
		matchObj = re.match( r'\badd\b|\badc\b|\bsub\b|\bsbb\b', e, re.M|re.I)  #do inc or dec separate
			
		if matchObj: 
			matchObj = re.match( r'^[add|adc|sub|sbb]+ [e]*bp|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[ebp\]', e, re.M|re.I)
			if matchObj:
				#print "step2"
				#print e				
				matchObj2 = re.match( r'^[add|adc|sub|sbb]+ [e]*bp, [e]*bp|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[ebp\], [e]*bp|^[add|adc|sub|sbb]+ [e]*bp, [byte|dword]+ ptr \[[e]*bp|^[add|adc|sub|sbb]+ [e]*bp[0-9a-fx] \t', e, re.M|re.I)
				if not matchObj2: 
					#print "Found DG2"
					#print e				
					save2 = address
					LinesSave = i+linesGoBack

					numLines= giveLineNum(val5,e)
					z =stupidPreJ(val5, numLines)
					if z == True:
						addListBaseDG_EBP(save2, numLines, NumOpsDis, modName)
					# addListBaseDG_EBP(save2, LinesSave, numOps, modName) # fist parameter: address of target jmp [reg]; second parameter: number of lines to go back.
					#addListBaseDG(save2, LinesSave, numOps, modName)
					searchListBaseM(save2, numOps, objs[o].listOP_BaseDG_EBP, objs[o].listOP_BaseDG_NumOps_EBP, objs[o].listOP_BaseDG_CNT_EBP, objs[o].listOP_BaseDG_Module_EBP)
					counter()
					matchObj3 = re.match( r'^[add|adc|sub|sbb]+ [e]*bp, [0x]*[0-9a-f]+[0-9a-f]*|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[ebp\],[0x]*[0-9a-f]+[0-9a-f]*', e, re.M|re.I)
					if matchObj3:
						matchObj3 = re.match( r'^[add|adc|sub|sbb]+ [e]*bp, [0x]*[0-9a-f]+[0-9a-f]+[0-9a-f]+[0-9a-f]+|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[ebp\], [0x]*[0-9a-f]+[0-9a-f]+[0-9a-f]+[0-9a-f]+', e, re.M|re.I)   #It is defined as really good if it is 0x01- 0xfff. I found this necessary to express in two nested lines.
						if not matchObj3:

							numLines= giveLineNum(val5,e)
							z =stupidPreJ(val5, numLines)
							if z == True:
								addListBaseDG_EBP_Best(save2, numLines, NumOpsDis, modName)
							# addListBaseDG_EBP_Best(save2, LinesSave, numOps, modName) # fist parameter: address of 
		if tk == HowDeep:   #This determines how far deep it goes searching for the Dispatcher gadget. That is, how many lines can be between the jmp/call [reg] and the add/sub
			break
	#Mult/Div via Shifting - This way is very sub-par but  feasible in some circumstances. Sub-par for obvious reasons. There would need to be a separate way to add or dec the target register, as you can only shift left or shift right a few times. The intermediate changer could be a part of a functional gadget. These can also act on just 16 or 8 bit registers, which makes them far more viable. This is a way to do mult/div; both are these are very rare in JOP gadgets.

	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = valAdd[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1
		matchObj = re.match( r'\bshl\b|\bshr\b|\bsar\b|\bsal\b|\bshlb\b|\bshrb\b|\bsarb\b|\bsalb\b|\bshlw\b|\bshrw\b|\bsarw\b|\bsalw\b|\b', e, re.M|re.I)  #do inc or dec separate
		if matchObj: 
			matchObj = re.match( r'^s[h|a]+[l|r]+[dwl]* [e]*bp, [1|2]+', e, re.M|re.I) #only 1 or 2 because anything else is too inconcievable, and shift left / shift right can provide can provide other options. 
			if matchObj:
				save2 = address
				LinesSave = i+linesGoBack
				addListBaseDG_EBP_Other(save2, LinesSave, numOps, modName)
		if tk == HowDeep:   #This determines how far deep it goes searching for the Dispatcher gadget. That is, how many lines can be between the jmp/call [reg] and the add/sub
			break

	#Multiplication - very rare for jop
	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = valAdd[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1
		matchObj = re.match( r'^imul[b|w|l]* [e]*bp, [e]*[abcdsp]+[xbpi]+', e, re.M|re.I)
		if matchObj:
			matchObj = re.match( r'^imul[b|w|l]* [e]*bp, [e]*[abcdsp]+[xbpi]+,', e, re.M|re.I)
			if not matchObj:
				save2 = address
				LinesSave = i+linesGoBack
				addListBaseDG_EBP_Other(save2, LinesSave, numOps, modName)
		if tk == HowDeep:   #This determines how far deep it goes searching for the Dispatcher gadget. That is, how many lines can be between the jmp/call [reg] and the add/sub
			break

def findDG_ESP(address, valCount, NumOpsDis, modName, linesGoBack, HowDeep):
	CODED2 = b""
	numOps = NumOpsDis # was x
	for i in range (numOps, 0, -1):  #was x
		CODED2 += objs[o].data2[address-i]
	CODED2 += objs[o].data2[address]
	CODED2 += objs[o].data2[address+1]
	CODED2 += b"\x00"
	val =""
	val2 = []
	valAdd = []
	val5 =[]

	for i in cs.disasm(CODED2, address-numOps):  # was x
		
		add = hex(int(i.address))
		add2 = str(add)
		add3 = hex (int(i.address + objs[o].startLoc	+ objs[o].VirtualAdd))
		add4 = str(add3)
		val =  i.mnemonic + " " + i.op_str + "\t\t\t\t"  + add4 + " (offset " + add2 + ")\n"
		val2.append(val)
		valAdd.append(add2)
		val5.append(val)
	tz = val2.__len__()
	tk=0
	save=0x00
	save2=0x00
	LinesSave=0
	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = valAdd[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1
		# Use regular expressions to find lines that have control flow and other undesired instructions, so they and preceding lines can be excised. 
		matchObj = re.match( r'\badd\b|\badc\b|\bsub\b|\bsbb\b', e, re.M|re.I)  #do inc or dec separate
			
		if matchObj: 
			matchObj = re.match( r'^[add|adc|sub|sbb]+ [e]*sp|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[ESP\]', e, re.M|re.I)
			if matchObj:

				matchObj2 = re.match( r'^[add|adc|sub|sbb]+ [e]*sp, [e]*sp|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[ESP\], [e]*sp|^[add|adc|sub|sbb]+ [e]*sp, [byte|dword]+ ptr \[[e]*sp|^[add|adc|sub|sbb]+ [e]*sp[0-9a-fx] \t', e, re.M|re.I)
				if not matchObj2: 
					save2 = address
					LinesSave = i+linesGoBack

					numLines= giveLineNum(val5,e)
					z =stupidPreJ(val5, numLines)
					if z == True:
						addListBaseDG_ESP(save2, numLines, NumOpsDis, modName)
					# addListBaseDG_EBX(save2, LinesSave, numOps, modName) # fist parameter: address of target jmp [reg]; second parameter: number of lines to go back.
					#addListBaseDG(save2, LinesSave, numOps, modName)
					searchListBaseM(save2, numOps, objs[o].listOP_BaseDG_ESP, objs[o].listOP_BaseDG_NumOps_ESP, objs[o].listOP_BaseDG_CNT_ESP, objs[o].listOP_BaseDG_Module_ESP)
					counter()
					matchObj3 = re.match( r'^[add|adc|sub|sbb]+ [e]*sp, [0x]*[0-9a-f]+[0-9a-f]*|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[ESP\],[0x]*[0-9a-f]+[0-9a-f]*', e, re.M|re.I)
					if matchObj3:
						matchObj3 = re.match( r'^[add|adc|sub|sbb]+ [e]*sp, [0x]*[0-9a-f]+[0-9a-f]+[0-9a-f]+[0-9a-f]+|^[add|adc|sub|sbb]+ [byte|dword]+ ptr \[ESP\], [0x]*[0-9a-f]+[0-9a-f]+[0-9a-f]+[0-9a-f]+', e, re.M|re.I)   #It is defined as really good if it is 0x01- 0xfff. I found this necessary to express in two nested lines.
						if not matchObj3:

							numLines= giveLineNum(val5,e)
							z =stupidPreJ(val5, numLines)
							if z == True:
								addListBaseDG_ESP_Best(save2, numLines, NumOpsDis, modName)
							# addListBaseDG_ESP_Best(save2, LinesSave, numOps, modName) # fist parameter: address of 
		if tk == HowDeep:   #This determines how far deep it goes searching for the Dispatcher gadget. That is, how many lines can be between the jmp/call [reg] and the add/sub
			break
	#Mult/Div via Shifting - This way is very sub-par but  feasible in some circumstances. Sub-par for obvious reasons. There would need to be a separate way to add or dec the target register, as you can only shift left or shift right a few times. The intermediate changer could be a part of a functional gadget. These can also act on just 16 or 8 bit registers, which makes them far more viable. This is a way to do mult/div; both are these are very rare in JOP gadgets.

	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = valAdd[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1
		matchObj = re.match( r'\bshl\b|\bshr\b|\bsar\b|\bsal\b|\bshlb\b|\bshrb\b|\bsarb\b|\bsalb\b|\bshlw\b|\bshrw\b|\bsarw\b|\bsalw\b|\b', e, re.M|re.I)  #do inc or dec separate
		if matchObj: 
			matchObj = re.match( r'^s[h|a]+[l|r]+[dwl]* [e]*sp, [1|2]+', e, re.M|re.I) #only 1 or 2 because anything else is too inconcievable, and shift left / shift right can provide can provide other options. 
			if matchObj:
				save2 = address
				LinesSave = i+linesGoBack
				addListBaseDG_ESP_Other(save2, LinesSave, numOps, modName)
		if tk == HowDeep:   #This determines how far deep it goes searching for the Dispatcher gadget. That is, how many lines can be between the jmp/call [reg] and the add/sub
			break

	#Multiplication - very rare for jop
	for i, e in reversed(list(enumerate(val2))):
		tt = val2.__len__()   
		if tk < 1:
			save = valAdd[i]   # This allows me to save the initial  address of the target jmp [reg] address.
		tk += 1
		matchObj = re.match( r'^imul[b|w|l]* [e]*sp, [e]*[abcdsp]+[xbpi]+', e, re.M|re.I)
		if matchObj:
			matchObj = re.match( r'^imul[b|w|l]* [e]*sp, [e]*[abcdsp]+[xbpi]+,', e, re.M|re.I)
			if not matchObj:
				save2 = address
				LinesSave = i+linesGoBack
				addListBaseDG_ESP_Other(save2, LinesSave, numOps, modName)
		if tk == HowDeep:   #This determines how far deep it goes searching for the Dispatcher gadget. That is, how many lines can be between the jmp/call [reg] and the add/sub
			break

def runIt():
	global PE_DLLS
	global peName
	global modName
	global o
	global index
	o = 0
	print "Running algorithm to obtain gadgets..."
	sp()
	if not CheckallModules:
		runGetRegs()
		

	if CheckallModules:
		runGetRegs()
		print "Checking all modules..."
		sp()
		zy = 0
		index = 0
		for dll in PE_DLLS:
			o = zy + 1
			#print "o " + str(o)
			#extractDLL_Min(PE_DLLS[zy])
			extractDLL_MinNew(PE_DLLS[zy])
			runGetRegs()
			#runGetRegsDG()
			#finalPrintSub2()
			zy+=1
			print "PE: " + str(peName)
			sp()
		modName = peName
		o = 0
	runGetRegsDGNew()
	#print "\n**Completed gadget search"
def runGetRegs():
	global o
	global NumOpsD
	#print ""#"in runGetRegs"
	#print getDG
	sp
	if getJMP:
		for reg in Regs:
			if reg == "EAX":
				print "Getting JMP EAX"
				sp()
				get_OP_JMP_EAX(NumOpsD)
				get_OP_JMP_PTR_EAX(NumOpsD)
				print "Done getting EAX"
				sp()
			if reg == "EBX":
				print "Getting JMP EBX"
				sp()
				get_OP_JMP_EBX(NumOpsD)
				get_OP_JMP_PTR_EBX(NumOpsD)
				print "Done getting EBX"
			if reg == "ECX":
				print "Getting JMP ECX"
				sp()
				get_OP_JMP_ECX(NumOpsD)
				get_OP_JMP_PTR_ECX(NumOpsD)
				print "Done getting ECX"
			if reg == "EDX":
				print "Getting JMP EDX"
				sp()
				get_OP_JMP_EDX(NumOpsD)
				get_OP_JMP_PTR_EDX(NumOpsD)
				print "Done getting EDX"
			if reg == "EDI":
				print "Getting JMP EDI"
				sp()
				get_OP_JMP_EDI(NumOpsD)
				get_OP_JMP_PTR_EDI(NumOpsD)
				print "Done getting EDI"
			if reg == "ESI":
				print "Getting JMP ESI"
				sp()
				get_OP_JMP_ESI(NumOpsD)
				get_OP_JMP_PTR_ESI(NumOpsD)
				print "Done getting ESI"
			if reg == "EBP":
				print "Getting JMP EBP"
				sp()
				get_OP_JMP_EBP(NumOpsD)
				get_OP_JMP_PTR_EBP(NumOpsD)
				print "Done getting EBP"
			if reg == "ESP":
				print "Getting JMP ESP"
				sp()
				get_OP_JMP_ESP(NumOpsD)
				get_OP_JMP_PTR_ESP(NumOpsD)
				print "Done getting ESP"
	if getCALL:
		for reg in Regs:
			if reg == "EAX":
				print "Getting CALL EAX"
				sp()
				get_OP_CALL_EAX(NumOpsD)
				get_OP_CALL_PTR_EAX(NumOpsD)				
				print "Done getting EAX"
			if reg == "EBX":
				print "Getting CALL EBX"
				sp()
				get_OP_CALL_EBX(NumOpsD)
				get_OP_CALL_PTR_EBX(NumOpsD)				
				print "Done getting EBX"
			if reg == "ECX":
				print "Getting CALL ECX"
				sp()
				get_OP_CALL_ECX(NumOpsD)				
				get_OP_CALL_PTR_ECX(NumOpsD)
				print "Done getting ECX"
			if reg == "EDX":
				print "Getting CALL EDX"
				sp()
				get_OP_CALL_EDX(NumOpsD)
				get_OP_CALL_PTR_EDX(NumOpsD)
				print "Done getting EDX"
			if reg == "EDI":
				print "Getting CALL EDI"
				sp()
				get_OP_CALL_EDI(NumOpsD)
				get_OP_CALL_PTR_EDI(NumOpsD)
				print "Done getting EDI"
			if reg == "ESI":
				print "Getting CALL ESI"
				sp()
				get_OP_CALL_ESI(NumOpsD)
				get_OP_CALL_PTR_ESI(NumOpsD)
				print "Done getting ESI"
			if reg == "EBP":
				print "Getting CALL EBP"
				sp()
				get_OP_CALL_EBP(NumOpsD)
				get_OP_CALL_PTR_EBP(NumOpsD)
				print "Done getting EBP"
			if reg == "ESP":
				print "Getting CALL ESP"
				sp()
				get_OP_CALL_ESP(NumOpsD)
				get_OP_CALL_PTR_ESP(NumOpsD)
				print "Done getting ESP"
	#if getDG:
	#	print ""#"in getDG"
	#	sp()
	#	runGetRegsDG()
	#print it

def binaryToStr(binary):
	OP_SPECIAL = b"\x8d\x4c\xff\xe2\x01\xd8\x81\xc6\x34\x12\x00\x00"
	newop=""
	try:
		for v in binary:
			i = ord(v) 
			newop += "\\x"+show1(i)
		# print newop
		return newop
	except:
		print "*Not valid format"
def showOrdTest():
	OP_JMP_EDX = b"\xff\xe2"
	OP_SPECIAL = b"\x8d\x4c\xff\xe2\x01\xd8\x81\xc6\x34\x12\x00\x00"
	newop=""
	for v in OP_JMP_EDX:
		i = ord(v) 
		newop += "\\x"+show1(i)

	print newop 

	print "newop"
	print binaryToStr(OP_SPECIAL)

	k=400
	i = ord(objs[o].data2[k]) 
	show = "{0:02x}".format(i) # hexadecimal: ff
	print (show)
	print hex(k)
	test = ord(b'\x8b')
	test2 = ord(b'\xe8')
	if (ord(objs[o].data2[k]) == test):
		print "\tequals"
		if (ord(objs[o].data2[k+1]) == test2):
			print "\t\tequals"
	else:
		print "\tfalse"
	print "size of data array: "
	num = len(objs[o].data2)
	print(num)

#entryBase = objs[o].startLoc + entryPoint
#VirtualAdd = objs[o].VirtualAdd
#ImageBase = pe.OPTIONAL_HEADER.ImageBase
#vSize = objs[o].pe.sections[0].Misc_VirtualSize
#objs[o].startLoc = VirtualAdd + ImageBase
#print "vadd " + str(VirtualAdd)
#print " imagebase " + str(ImageBase )
#print " vsize "  + str(vSize )
#print " start add " + str(objs[o].startLoc )
#print " endAddy  " + str(endAddy)
#print " entryPoint " + str(entryPoint)

def showPEInfo():
	print "start address:", hex(objs[o].startLoc) 
	print "entry point:", hex(entryPoint)
	print "entry base:", hex(entryBase)
	print "VirtualAdd:", hex(VirtualAdd)
	print "Image Base:", hex(ImageBase)
	print "Virtual Size:", hex(vSize)
	print "end address:", hex(endAddy)

	#print "\n\n" 
	print hex(VirtualAdd)
	#print "\n\n\nImageBase: %s\nentry point %s\nobjs[o].startLoc "  % (ImageBase, entryPoint)
	print hex(objs[o].startLoc)
	#print "\nVirtualSize: "
	print vSize
	print "end address: "
	print hex(endAddy)


def cutDown(l1, l2):
	ct = 0
	for r in l1:
		r = r.strip()
		l1[ct] = r
		ct += 1
	unique=[]
	for x in l1:
		if x in l2:
		    if x not in unique:
	        	unique.append(x)
	return unique

def changeNumOps():
	global NumOpsD
	print "Change number of opcodes:" 
	sp()
	NumOpsD = raw_input()
	print NumOpsD
def changePE():
	global peName
	global peNameSkip
	global modName
	print "Current PE: %s\nNew PE:" % peName
	sp()
	fi = raw_input() #get filename
	if fi != "":
		peNameSkip = False
		modName = fi
		print "not"
		print peNameSkip
		sp()
		return fi
	if fi == "":
		peNameSkip = True
		print so
		print peNameSkip
		sp()
		return peName
def changeCF():
	global getJMP
	global getCALL
	print "1 - Obtain both JMP and CALL.\n2 - Obtain CALL\n3 - Obtain JMP"
	sp()
	cf = raw_input()
	if cf == "1":
		getCALL = True
		getJMP = True
	if cf == "2":
		getCALL = True
		getJMP = False
	if cf == "3":
		getCALL = False
		getJMP = True	
#dg
def checkForDG():
	global RegsDG
	global getDG
	print "Which registers do you wish to search for dispatcher gadgets? \nE.g. All, EAX, EBX, etc."

	sp()
	reg = raw_input()
	reg = reg.upper()	
	skip = False
	if reg == "ALL":
		RegsDG = copy.copy(IA86)
		skip = True
		getDG = True
	if reg == "all":
		RegsDG = copy.copy(IA86)
		skip = True
		getDG = True
	if not skip:
		RegsDG = reg.split(',')
		RegsDG = cutDown(RegsDG,IA86)
		getDG = True
	display = ""
	for r in RegsDG:
		display = display + r + "    "
		sp()
	print "Registers selected: " + display
	sp()
def changeReg():
	global Regs
	print "Gadgets that end in a call/jmp to these registers will be found.\n"
	print "Enter registers to search, delimited by comma"
	sp()
	reg = raw_input()
	reg = reg.upper()	
	skip = False
	if (reg == "ALL") or (reg == "EACH"):
		Regs = copy.copy(IA86)
		skip = True
		#print "Registers selected: " + display
		sp()
	if (reg == "all") or (reg == "each"):
		Regs = copy.copy(IA86)
		skip = True
		#print "Registers selected: " + display
		sp()
	if not skip:
		Regs = reg.split(',')
		Regs = cutDown(Regs,IA86)
		display = ""
	display =""
	for r in Regs:
		display += r + "    "
		sp()
	print "Registers selected: " + display
	sp()
def getPrintInput():
	global Input
	print "Enter operations, delimited by comma:"
	sp()
	val = raw_input()
	val = val.lower()	
	skip = False
	if val == "ALL":
		Input = copy.copy(InputAcceptable)
		skip = True
		print skip
		sp()
	if not skip:
		#print "entering not skip"
		#sp()
		Input = val.split(',')
		Input = cutDown(Input,InputAcceptable)
		#print Input

	# display = ""
	# for r in Input:
	# 	display = display + r + "    "
	# print "Registers to print selected: \n\t" + str(display)
	# sp()
def changeRegsPrint():
	global RegsPrint
	print "Registers to print:"
	# sp()
	# reg = raw_input()
	# reg = reg.upper()	
	# skip = False
	# if reg == "EACH":
	# 	RegsPrint = copy.copy(IA862)
	# 	skip = True
	# if not skip:
	# 	RegsPrint = reg.split(',')
	# 	RegsPrint = cutDown(RegsPrint,IA862)
	# 	display = ""
	# for r in RegsPrint:
	# 	display = display + r + "    "
	# 	sp()
	# print "Registers to print selected: " + display





	reg = raw_input()
	reg = reg.upper()	
	skip = False
	if (reg == "ALL") or (reg == "EACH"):
		RegsPrint = copy.copy(IA86)
		skip = True
		#print "Registers selected: " + display
		sp()
	if (reg == "all") or (reg == "each"):
		RegsPrint = copy.copy(IA86)
		skip = True
		#print "Registers selected: " + display
		sp()
	if not skip:
		RegsPrint = reg.split(',')
		RegsPrint = cutDown(Regs,IA86)
		display = ""
	display =""
	for r in RegsPrint:
		display += r + "    "
		sp()
	print "Registers to print selected: " + display


def changeRegsVP():
	global RegsVP
	print "Default: EAX, EBX, ECX, EDX, EDI, ESI, EBP"
	print "Enter registers delimited by commas or ALL.\n"
	print "Enter registers to obtain JOP chains for:"
	reg = raw_input()
	reg = reg.upper()	
	skip = False
	if (reg == "ALL") or (reg == "EACH"):
		RegsVP = copy.copy(IA86)
		skip = True
		#print "Registers selected: " + display
		sp()
	if (reg == "all") or (reg == "each"):
		RegsVP = copy.copy(IA86)
		skip = True
		#print "Registers selected: " + display
		sp()
	if not skip:
		RegsVP = reg.split(',')
		RegsVP = cutDown(Regs,IA86)
		display = ""
	display =""
	for r in RegsPrint:
		display += r + "    "
		sp()
	print "Registers to print selected: " + display	
def changelinesGoBack():
	global linesGoBackFindOP
	print "New lines go back value:"
	sp()
	linesGoBackFindOP = raw_input()
def changeCheckAllModules():
	global CheckallModules
	print "1 - Check only PE"
	print "2 - Check all modules\n"
	print "3 - Check all modules and more\n"
	print "Note: If option 2 is selected, printing and extraction will occur simultaneous. Thus print settings must be set prior to extraction.\n"
	sp()
	ans = raw_input()
	if ans == "2":
		CheckallModules = True
	if ans == "1":
		CheckallModules = False
	if ans == "3":
		levelTwo = True
		CheckallModules = True
def checkForHelpD(val):
	
	try:
	  	check = val[0:2]
	  	command = val[2:3]
	  #	print check
	  #	print "checking"
	except: 
		pass
	if check == "-h":
		helpDetailed(val)
	if check == "h ":  
		sp()
		helpDetailed(command)
	return False

def dummy():
	pass

imBase=0x400000
def testDiss():
	global data2
	global imBase

	imBase = objs[o].startLoc
	# im=objs[o].startLoc
	ans = []
	print "Enter offset to unasssemble. Default is 16 bytes. To enlarge or reduce, \ndelimit input with comma. E.g. 0x4062, 18    OR     0x4062       h=help\nInput:"
	sp()
	while (2>1):
		# print imBase
		address=0
		address2 = raw_input()
		if address2=="x":
			break
		if address2=="b":
			print "Enter new image base, e.g. 0x500000"
			enter=raw_input()
			imBase=int(enter,16)
		if address2=="h":
			# print "test"
			out = "x: exit\nYou can also enter an address with the image base, e.g. 0x401628.\n"
			# out += "\tIt assumes the default image base, " + hex(imBase) +", but you can change it.\n"
			# out += "b: changes image base for PE file (not retained after leaving function).\n"
			out += "\nWhen looking at a gadget, look at the offset at the bottom, e.g. jmp edx\n"
			out += "\tEnter that offset to reproduce the gadget you found, and to see 'more' \n"
			out += "\t infront of it. You can adjust the opcodes used as well, to see how \n\tdiassembly changes.\n"
			print out

		ans = address2.split(',')
		
		# d=0
		# try:
		# 	ans=int(d)
		# 	# print "ok3"
		# except:
		# 	ans=int(d,16)
		# 	# print "ok1"
		try:

			address = int(ans[0], 16)

			address = address - 0x1000
			# print "address: " + str(address)
		except:
			pass
		try:
			if address > 0:
			


				if address > imBase:
					address -= imBase
				CODED2 = b""
				# print address


				if len(ans) > 1:
					x = int(ans[1])
				else:
					x = 16
				for i in range (x, 0, -1):
					CODED2 += objs[o].data2[address-i]
				CODED2 += objs[o].data2[address]
				CODED2 += objs[o].data2[address+1]
				CODED2 += b"\x00"

				# I create the individual lines of code that will appear>
				val =""
				val2 = []
				val3 = []
				address2 = address + objs[o].startLoc + 1000

				for i in cs.disasm(CODED2, address-x):
					add = hex(int(i.address))
					addb = hex(int(i.address +  objs[o].VirtualAdd))
					add2 = str(add)
					add3 = hex (int(i.address + imBase	))
					add4 = str(add3)
					val =  i.mnemonic + " " + i.op_str + "\t\t\t\t"  + add4 + " (offset " + addb + ")\n"
					val2.append(val)
					val3.append(add2)
					print val
		except:
			pass


def runGetRegsDGNew():
	global o
	o=0
	print "in RunGetRegsDG"
	sp()
	print "Getting EAX dispatcher gadgets"
	sp()
	try:

		get_Dispatcher_G(NumOpsD, Depth, "EAX")
		print "Getting EAX dispatcher gadgets"
	except:
		print "No EAX dispatcher gadgets"
		sp()

	try:
		get_Dispatcher_G(NumOpsD, Depth, "EBX")
		print "Getting EBX dispatcher gadgets"
		sp()
	except:
		print "No EBX dispatcher gadgets"
		sp()

	try:
		get_Dispatcher_G(NumOpsD, Depth, "ECX")
		print "Getting ECX dispatcher gadgets"
		sp()
	except:
		print "No ECX dispatcher gadgets"
		sp()

	try:
		get_Dispatcher_G(NumOpsD, Depth, "EDX")
		print "Getting EDX dispatcher gadgets"
		sp()
	except:
		print "No EDX dispatcher gadgets"
		sp()

	try:
		get_Dispatcher_G(NumOpsD, Depth, "EDI")
		print "Getting EDI dispatcher gadgets"
		sp()
	except:
		print "No EDI dispatcher gadgets"
		sp()

	try:
		get_Dispatcher_G(NumOpsD, Depth, "ESI")
		print "Getting ESI dispatcher gadgets"
		sp()
	except:
		print "No ESI dispatcher gadgets"
		sp()

	try:
		get_Dispatcher_G(NumOpsD, Depth, "EBP")
		print "Getting EBP dispatcher gadgets"
		sp()
	except:
		print "No EBP dispatcher gadgets"
		sp()

	try:
		get_Dispatcher_G(NumOpsD, Depth, "ESP")
		print "Getting ESP dispatcher gadgets"
		#print "done"#"in RunGetRegsDG"
		sp()
	except:
		print "No ESP dispatcher gadgets"
		sp()


def runGetRegsDG():
	global o
	o=0
	print "in RunGetRegsDG"
	sp()
	for reg in RegsDG:
		if reg == "EAX":
			print "Getting EAX dispatcher gadgets"
			sp()
			get_Dispatcher_G(NumOpsD, Depth, "EAX")
		if reg == "EBX":
			print "Getting EBX dispatcher gadgets"
			sp()
			get_Dispatcher_G(NumOpsD, Depth, "EBX")
		if reg == "ECX":
			print "Getting ECX dispatcher gadgets"
			sp()
			get_Dispatcher_G(NumOpsD, Depth, "ECX")
		if reg == "EDX":
			print "Getting EDX dispatcher gadgets"
			sp()
			get_Dispatcher_G(NumOpsD, Depth, "EDX")
		if reg == "EDI":
			print "Getting EDI dispatcher gadgets"
			sp()
			get_Dispatcher_G(NumOpsD, Depth, "EDI")
		if reg == "ESI":
			print "Getting ESI dispatcher gadgets"
			sp()
			get_Dispatcher_G(NumOpsD, Depth, "ESI")
		if reg == "EBP":
			print "Getting EBP dispatcher gadgets"
			sp()
			get_Dispatcher_G(NumOpsD, Depth, "EBP")
		if reg == "ESP":
			print "Getting ESP dispatcher gadgets"
			sp()
			get_Dispatcher_G(NumOpsD, Depth, "ESP")
	#print "done"#"in RunGetRegsDG"
	sp()
def runPrintIt():
	showPrintOptions()
	x = ""
	
	while x is not "e":
	
	#	print "hello!"
		print "..........."
		sp()
		try:
		    print "Print Menu.\n..........."
		    sp()
		    r = raw_input()
		    if r == "r":
		    	changeRegsPrint()
		    if r == "x":
		    	print "Leaving print sub-menu..."
		    	break		    
		    if r == "check":
		    	print "Checking settings..."
		    	DebugCheck()
		    if r == "g":
		    	getPrintInput()
		    	runPrintS()
		    if r == "C":
		    	clearallPrint()
		    if r == "ap": #apply runPrintS - internal debug
		    	runPrintS()
		    if r == "de": #debug
		    	DebugCheck()
		    if r == "z":
		    	print "Printing..."
		    	sp()
		    	runPrintS()
		    	finalPrintSub2()
		    	print "\tWRITTEN to disk."
		    	sp()
		    if r == "h":
		    	showPrintOptions()
	 	except:
		    pass

def changeNumChains():
	global numVPAA
	print "Default: 5"
	print "Change number of different JOP chains to generate per register:" 
	d = raw_input()
	# print d
	try:
		ans=int(d)
		# print "ok3"
	except:
		ans=int(d,16)
		# print "ok1"
	print str(ans)+ " or " +  hex(ans) #str(int(d, 16))
	numVPAA=ans



def showVPOptions():
	out =""
	out +="g or z: generate prebuild JOP chains!\n"
	out +="\tUse s first if you have not discovered JOP gadgets yet.\n"
	out +="n: change number of prebuilt JOP chains to attempt per register. \n"
	out +="p: change number of bytes desired in stack pivots.\n"
	out +="s: clear all settings and rebuild for all registers for JOP\n"
	out +="\tYou only need to do this once per PE file.\n"
	out +="u: Using gadgets already found; do not clear.\n"
	out +="\tYou only need to do this once per PE file. Do s *or* u.\n"
	out +="h: display options\n"
	out +="x or X: return to previous menu\n"
	print out
def c():
	global numVPAA
	initVPVA()
	doFinalVA(numVPAA)

def vpvaSubMenu():
	global numVPAA
	showVPOptions()
	x = ""
	
	while x is not "e":
		try:
		#	print "hello!"
			print "..........."
			# sp()
			# try:
			print "JOP Chain Sub-menu"
			sp()
			r = raw_input()
			if r == "r":
				changeRegsVP()
			if r == "x":
				print "Leaving JOP Chain sub-menu...\n\n"
				showOptions()
				break		
			if r == "X":
				print "Leaving JOP Chain sub-menu...\n\n"
				showOptions()
				break		  		    	    
			# if r == "check":
			# 	print "Checking settings..."
			# 	DebugCheck()
			if r == "g":
				doFinalVA(numVPAA)
			if r == "z":
				doFinalVA(numVPAA)		    	
			if r == "n":
				changeNumChains()
			# if r == "ap": #apply runPrintS - internal debug
			# 	runPrintS()
			if r == "p": #debug
				changeStackPivotNum()
			if r == "u":
				initVPVA_Use_Existing()
			if r == "s":   
				print "Rebuilding..."
				initVPVA()
			# 	sp()
			# 	runPrintS()
			# 	finalPrintSub2()
			# 	print "\tPRINTED to disk."
			# 	sp()
			if r == "h":
				showVPOptions()
		except:
			pass
	#get input
	#do it/print it
	#loop back and say:
	#do you want to see options again/furhter input/chance to exit loop
def DebugCheck():
	print "JMP EAX all:\t" + str(printja) +"\t" +"JMP EBX all:\t" + str(printjb)
	print "JMP ECX all:\t" + str(printjc)+"\t"+ "JMP EDX all:\t" + str(printjd)
	print "JMP EDI all:\t" + str(printjdi)+"\t" +"JMP ESI all:\t" + str(printjsi)
	print "JMP EBP all:\t" + str(printjbp)+"\t" +"CALL EAX all:\t" + str(printca)
	print "CALL EBX all:\t" + str(printcb)+"\t" +"CALL ECX all:\t" + str(printcc)
	print "CALL EDX all:\t" + str(printcd)+"\t"+ "CALL EDI all:\t" + str(printdi)
	print "CALL ESI all:\t" + str(printsi)+"\t" + "CALL EBP all:\t" + str(printcbp)
	print "CALL ESP all:\t" + str(printcsp)+"\t" + "JMP ESP all:\t" + str(printjsp)
	print "ADD:\t\t" + str(printAdd)+"\t"+ "SUB:\t\t" + str(printSub)
	print "MUL:\t\t" + str(printMul)+"\t"+ "DIV:\t\t" + str(printDiv)
	print "MOV:\t\t" + str(printMov)+"\t"+ "MOV Val:\t" + str(printMovV)
	print "Deref:\t\t" + str(printDeref)
	print "MOV Val:\t" + str(printMovS)+"\t"+ "XCHG:\t\t" + str(printXchg)
	print "POP:\t\t" + str(printPop)+"\t"+ "POP:\t\t" + str(printPush)
	print "DEC:\t\t" + str(printDec)+"\t"+ "INC:\t\t" + str(printInc)
	print "SHIFT LEFT:\t" + str(printShiftLeft)+"\t"+ "SHIFT RIGHT:\t" + str(printShiftRight)
	print "ROTATE RIGHT:\t" + str(printRotateRight)+"\t"+ "ROTATE LEFT:\t" + str(printRotateLeft)

	#print "\nRegs to print:" 
	print RegsPrint
	print "Regs selected:"
	print Regs

def runPrintS():
	global printja
	global printjb
	global printjc
	global printjd
	global printjdi
	global printjsi
	global printjbp
	global printjsp
	global printptrja
	global printptrjb
	global printptrjc
	global printptrjd
	global printptrjdi
	global printptrjsi
	global printptrjbp
	global printptrjsp
	global printca
	global printcb
	global printcc
	global printcd
	global printdi
	global printsi
	global printcbp
	global printcsp
	global printptrca
	global printptrcb
	global printptrcc
	global printptrcd
	global printptrdi
	global printptrsi
	global printptrcbp
	global printptrcsp    
	global printAdd
	global printStack
	global printSub
	global printMul
	global printDiv
	global printMov
	global printMovV
	global printMovS
	global printDeref
	global printLea
	global printXchg
	global printPop
	global printPush
	global printDec
	global printInc
	global printShiftLeft
	global printShiftRight
	global printRotateRight
	global printRotateLeft
	global printDispatcherEAX
	global printDispatcherEBX
	global printDispatcherECX
	global printDispatcherEDX
	global printDispatcherEDI
	global printDispatcherESI
	global printDispatcherEBP
	global printDispatcherEAXBest
	global printDispatcherEBXBest 
	global printDispatcherECXBest
	global printDispatcherEDXBest
	global printDispatcherEDIBest
	global printDispatcherESIBest
	global printDispatcherEBPBest
	global printDispatcherEAXOther
	global printDispatcherEBXOther 
	global printDispatcherECXOther
	global printDispatcherEDXOther
	global printDispatcherEDIOther
	global printDispatcherESIOther
	global printDispatcherEBPOther

	print "Setting print settings..."
	display = ""
	for r in Input:
		display = display + r + "    "
	print "Operations selected: \n\t" + str(display)
	sp()
	for r in Input:
		if r == "j":
			printja = True
			printjb = True
			printjc = True
			printjd = True
			printjdi = True
			printjsi = True
			printjbp = True
			printjsp = True
		if r == "ja":
			printja = True
		if r == "jb":
			printjb = True
		if r == "jc":
			printjc = True
		if r == "jd":
			printjd = True
		if r == "jdi":
			printjdi = True
		if r == "jsi":
			printjsi = True
		if r == "jbp":
			printjbp = True
		if r == "jsp":
			printjsp = True	    	
		if r == "pj":
			printptrja = True
			printptrjb = True
			printptrjc = True
			printptrjd = True
			printptrjdi = True
			printptrjsi = True
			printptrjbp = True
			printptrjsp = True
		if r == "pja":
			printptrja = True
		if r == "pjb":
			printptrjb = True
		if r == "pjc":
			printptrjc = True
		if r == "pjd":
			printptrjd = True
		if r == "pjdi":
			printptrjdi = True
		if r == "pjsi":
			printptrjsi = True
		if r == "pjbp":
			printptrjbp = True
		if r == "pjsp":
			printptrjbp = True	    	
		if r == "cbp":
			printcbp = True

		if r == "c":
			printca = True
			printcb = True
			printcc = True
			printcd = True
			printdi = True
			printsi = True
			printcbp = True
			printcsp = True
		if r == "ca":
			printca = True
		if r == "cb":
			printcb = True
		if r == "cc":
			printcc = True
		if r == "cd":
			printcd = True
		if r == "cdi":
			printdi = True
		if r == "csi":
			printsi = True
		if r == "cbp":
			printcbp = True
		if r == "csp":
			printcsp = True
		if r == "pc":
			printptrca = True
			printptrcb = True
			printptrcc = True
			printptrcd = True
			printptrdi = True
			printptrsi = True
			printptrcbp = True
			printptrcsp = True
		if r == "pca":
			printptrca = True
		if r == "pcb":
			printptrcb = True
		if r == "pcc":
			printptrcc = True
		if r == "pcd":
			printptrcd = True
		if r == "pcdi":
			printptrdi = True
		if r == "pcsi":
			printptrsi = True
		if r == "pcbp":
			printptrcbp = True
		if r == "pcsp":
			printptrcsp = True
		if r == "ma":
			printAdd = True
			printSub = True
			printMul = True
			printDiv = True
		if r == "a":
			printAdd = True
		if r == "s":
			printSub = True
		if r == "m":
			printMul = True
		if r == "deref":
			printDeref = True	
		if r == "d":
			printDiv = True
		if r == "move":
			printMov = True
			printMovV = True
			printMovS = True
			printLea = True
			printXchg = True
			printDeref = True
		if r == "stack":
			printStack = True
		if r == "mov":
			printMov = True
		if r == "movv":
			printMovV = True
		if r == "movs":
			printMovS = True
		if r == "l":
			printLea = True
		if r == "xc":
			printXchg = True
		if r == "st":
			printPop = True
			printPush = True
			printStack = True
		if r == "po":
			printPop = True
		if r == "pu":
			printPush = True
		if r == "id":
			printDec = True
			printInc = True
		if r == "inc":
			printDec = True
		if r == "dec":
			printInc = True
		if r == "bit":
			printShiftLeft = True
			printShiftRight = True
			printRotateRight = True
			printRotateLeft = True
		if r == "sl":
			printShiftLeft = True
		if r == "sr":
			printShiftRight = True
		if r == "rr":
			printRotateRight = True
		if r == "rl":
			printRotateLeft = True
		if r == "all":
			printStack = True
			printja = True
			printjb = True
			printjc = True
			printjd = True
			printjdi = True
			printjsi = True
			printjbp = True
			printjsp = True
			printca = True
			printcb = True
			printcc = True
			printcd = True
			printdi = True
			printsi = True
			printcbp = True
			printcsp = True
			printptrja = True
			printptrjb = True
			printptrjc = True
			printptrjd = True
			printptrjdi = True
			printptrjsi = True
			printptrjbp = True
			printptrjsp = True
			printptrca = True
			printptrcb = True
			printptrcc = True
			printptrcd = True
			printptrdi = True
			printptrsi = True
			printptrcbp = True
			printptrcsp = True			
			printAdd = True
			printSub = True
			printMul = True
			printDiv = True
			printMov = True
			printMovV = True
			printDeref = True
			printMovS = True
			printLea = True
			printXchg = True
			printPop = True
			printPush = True
			printDec = True
			printInc = True
			printShiftLeft = True
			printShiftRight = True
			printRotateRight = True
			printRotateLeft = True
			printDispatcherEAX = True
			printDispatcherEBX = True
			printDispatcherECX = True
			printDispatcherEDX = True
			printDispatcherEDI = True
			printDispatcherESI = True
			printDispatcherEBP = True
			printDispatcherEAXBest = True
			printDispatcherEBXBest = True
			printDispatcherECXBest = True
			printDispatcherEDXBest = True
			printDispatcherEDIBest = True
			printDispatcherESIBest = True
			printDispatcherEBPBest = True
			printDispatcherEAXOther = True
			printDispatcherEBXOther = True
			printDispatcherECXOther = True
			printDispatcherEDXOther = True
			printDispatcherEDIOther = True
			printDispatcherESIOther = True
			printDispatcherEBPOther = True
		if r == "rec":
			printAdd = True
			printSub = True
			printMul = True
			printDiv = True
			printMov = True
			printMovV = True
			printDeref = True
			printMovS = True
			printLea = True
			printXchg = True
			printPop = True
			printPush = True
			printDec = True
			printInc = True
			printShiftLeft = True
			printShiftRight = True
			printRotateRight = True
			printRotateLeft = True
		if r == "da":
			printDispatcherEAX = True
		if r == "db":
			printDispatcherEBX = True
		if r == "dc":
			printDispatcherECX = True
		if r == "dd":
			printDispatcherEDX = True
		if r == "ddi":
			printDispatcherEDI = True
		if r == "dsi":
			printDispatcherESI = True
		if r == "dbp":
			printDispatcherEBP = True
		if r == "dis":
			printDispatcherEAX = True
			printDispatcherEBX = True
			printDispatcherECX = True
			printDispatcherEDX = True
			printDispatcherEDI = True
			printDispatcherESI = True
			printDispatcherEBP = True
		if r == "ba":
			printDispatcherEAXBest = True
		if r == "bb":
			printDispatcherEBXBest = True
		if r == "bc":
			printDispatcherECXBest = True
		if r == "bd":
			printDispatcherEDXBest = True
		if r == "bdi":
			printDispatcherEDIBest = True
		if r == "bsi":
			printDispatcherESIBest = True
		if r == "bbp":
			printDispatcherEBPBest = True
		if r == "bdis":
			printDispatcherEAXBest = True
			printDispatcherEBXBest = True
			printDispatcherECXBest = True
			printDispatcherEDXBest = True
			printDispatcherEDIBest = True
			printDispatcherESIBest = True
			printDispatcherEBPBest = True
		if r == "oa":
			printDispatcherEAXOther = True
		if r == "ob":
			printDispatcherEBXOther = True
		if r == "oc":
			printDispatcherECXOther = True
		if r == "od":
			printDispatcherEDXOther = True
		if r == "odi":
			printDispatcherEDIOther = True
		if r == "osi":
			printDispatcherESIOther = True
		if r == "obp":
			printDispatcherEBPOther = True
		if r == "odis":
			printDispatcherEAXOther = True
			printDispatcherEBXOther = True
			printDispatcherECXOther = True
			printDispatcherEDXOther = True
			printDispatcherEDIOther = True
			printDispatcherESIOther = True
			printDispatcherEBPOther = True
def clearallDLLs(): #5
	global w
	global PE_DLLS
	global DLL_Protect
	global PE_Protect
	PE_DLLS[:] = []
	DLL_Protect[:] = []
	PE_Protect =""
	#Destroy objects beyond the PE,i.e. the DLLs. Convoluted source code because it kept breaking and missing some oddly when implemented as just a simple for loop
	num = len(objs)
	w = 1
	while num > 1:
		for obj in objs:
			try:
				del objs[w]
			except:
				pass
			print "deleted "  + str(w)
			sp()
			w = w+ 1
		w=1
		num = len(objs)

def clearallPrint():
    global printja
    global printjb
    global printjc
    global printjd
    global printjdi
    global printjsi
    global printjbp
    global printjsp
    global printptrja
    global printptrjb
    global printptrjc
    global printptrjd
    global printptrjdi
    global printptrjsi
    global printptrjbp
    global printptrjsp
    global printca
    global printcb
    global printcc
    global printcd
    global printdi
    global printsi
    global printcbp
    global printcsp
    global printptrca
    global printptrcb
    global printptrcc
    global printptrcd
    global printptrdi
    global printptrsi
    global printptrcbp
    global printptrcsp 
    global printStack   
    global printAdd
    global printSub
    global printMul
    global printDiv
    global printMov
    global printMovV
    global printDeref
    global printMovS
    global printLea
    global printXchg
    global printPop
    global printPush
    global printDec
    global printInc
    global printShiftLeft
    global printShiftRight
    global printRotateRight
    global printRotateLeft
    global printDispatcherEAX
    global printDispatcherEBX
    global printDispatcherECX
    global printDispatcherEDX
    global printDispatcherEDI
    global printDispatcherESI
    global printDispatcherEBP
    global printDispatcherEAXBest
    global printDispatcherEBXBest 
    global printDispatcherECXBest
    global printDispatcherEDXBest
    global printDispatcherEDIBest
    global printDispatcherESIBest
    global printDispatcherEBPBest
    global printDispatcherEAXOther
    global printDispatcherEBXOther 
    global printDispatcherECXOther
    global printDispatcherEDXOther
    global printDispatcherEDIOther
    global printDispatcherESIOther
    global printDispatcherEBPOther
    printja = False
    printjb = False
    printjc = False
    printjd = False
    printjdi = False
    printjsi = False
    printjbp = False
    printjsp = False
    printca = False
    printcb = False
    printcc = False
    printcd = False
    printdi = False
    printsi = False
    printcbp = False
    printcsp = False
    printptrja = False
    printptrjb = False
    printptrjc = False
    printptrjd = False
    printptrjdi = False
    printptrjsi = False
    printptrjbp = False
    printptrjsp = False
    printptrca = False
    printptrcb = False
    printptrcc = False
    printptrcd = False
    printptrdi = False
    printptrsi = False
    printptrcbp = False
    printptrcsp = False
    printAdd = False
    printSub = False
    printMul = False
    printDiv = False
    printMov = False
    printMovV = False
    printDeref = False
    printMovS = False
    printLea = False
    printXchg = False
    printPop = False
    printPush = False
    printDec = False
    printInc = False
    printShiftLeft = False
    printShiftRight = False
    printRotateRight = False
    printRotateLeft = False
    printDispatcherEAX = False
    printDispatcherEBX = False
    printDispatcherECX = False
    printDispatcherEDX = False
    printDispatcherEDI = False
    printDispatcherESI = False
    printDispatcherEBP = False
    printDispatcherEAXBest = False
    printDispatcherEBXBest = False
    printDispatcherECXBest = False
    printDispatcherEDXBest = False
    printDispatcherEDIBest = False
    printDispatcherESIBest = False
    printDispatcherEBPBest = False
    printDispatcherEAXOther = False
    printDispatcherEBXOther = False
    printDispatcherECXOther = False
    printDispatcherEDXOther = False
    printDispatcherEDIOther = False
    printDispatcherESIOther = False
    printDispatcherEBPOther = False

    DebugCheck()

def finalPrintSubold(): 
	global printja
	global printjb
	global printjc
	global printjd
	global printjdi
	global printjsi
	global printjbp
	global printjsp
	global printptrja
	global printptrjb
	global printptrjc
	global printptrjd
	global printptrjdi
	global printptrjsi
	global printptrjbp
	global printptrjsp
	global printca
	global printcb
	global printcc
	global printcd
	global printdi
	global printsi
	global printcbp
	global printcsp
	global printptrca
	global printptrcb
	global printptrcc
	global printptrcd
	global printptrdi
	global printptrsi
	global printptrcbp
	global printptrcsp 
	global printStack   
	global printAdd
	global printSub
	global printMul
	global printDiv
	global printMov
	global printMovV
	global printDeref
	global printMovS
	global printLea
	global printXchg
	global printPop
	global printPush
	global printDec
	global printInc
	global printShiftLeft
	global printShiftRight
	global printRotateRight
	global printRotateLeft
	global printDispatcherEAX
	global printDispatcherEBX
	global printDispatcherECX
	global printDispatcherEDX
	global printDispatcherEDI
	global printDispatcherESI
	global printDispatcherEBP
	global printDispatcherEAXBest
	global printDispatcherEBXBest 
	global printDispatcherECXBest
	global printDispatcherEDXBest
	global printDispatcherEDIBest
	global printDispatcherESIBest
	global printDispatcherEBPBest
	global printDispatcherEAXOther
	global printDispatcherEBXOther 
	global printDispatcherECXOther
	global printDispatcherEDXOther
	global printDispatcherEDIOther
	global printDispatcherESIOther
	global printDispatcherEBPOther
	global o
	global printStack
	global printDeref
	global RegsPrint
	o =0
	#print "o " + str(o)
	#print "Final print setings..."
	#print RegsPrint

	sp()
	count = 0
	try:
		if printStack == True:
			printlistOP_SP(NumOpsD, "All")
			# printlistOP_SP3(NumOpsD, "All")
			print "done"
	except:
		pass

	for Reg in RegsPrint:  #For loop does not work properly without the try's. That is, if one subrountine cannot rune, the for loop would break, thereby not letting me do all it is supposed to do.
		
		try:
			print "try add " +  str(printAdd)
			if printAdd == True:
				print "in addd is true"
				sp()
				printlistOP_Add(NumOpsD, Reg)
		except:
			pass
		try:
			if printSub == True:
				printlistOP_Sub(NumOpsD, Reg)
		except:
			pass
		try:
			if printMul == True:
				printlistOP_Mul(NumOpsD, Reg)
		except:
			pass
		try:
			if printDiv == True:
				printlistOP_Div(NumOpsD, Reg)
		except:
			pass
		try:
			if printMov == True:
				printlistOP_Mov(NumOpsD, Reg)
		except:
			pass
		try:
			if printMovV == True:
				printlistOP_MovVal(NumOpsD, Reg)
		except:
			pass
		try:
			global printDeref
			if printDeref == True:
				printlistOP_MovDeref(NumOpsD, Reg)
		except:
			pass
		try:
			if printMovS == True:
				printlistOP_MovShuf(NumOpsD, Reg)
		except:
			pass
		try:
			if printLea == True:
				printlistOP_Lea(NumOpsD, Reg)
		except:
			pass
		try:
			if printXchg == True:
				printlistOP_Xchg(NumOpsD, Reg)
		except:
			pass
		try:
			if printPop == True:
				printlistOP_Pop(NumOpsD, Reg)
		except:
			pass
		try:
			if printPush == True:
				printlistOP_Push(NumOpsD, Reg)
		except:
			pass
		try:
			if printDec == True:
				printlistOP_Dec(NumOpsD, Reg)
		except:
			pass
		try:
			if printInc == True:
				printlistOP_Inc(NumOpsD, Reg)
		except:
			pass
		try:
			if printShiftLeft == True:
				printlistOP_ShiftLeft(NumOpsD, Reg)
		except:
			pass
		try:
			if printShiftRight == True:
				printlistOP_ShiftRight(NumOpsD, Reg)
		except:
			pass
		try:
			if printRotateRight == True:
				printlistOP_RotRight(NumOpsD, Reg)
		except:
			pass
		try:
			if printRotateLeft == True:
				printlistOP_RotLeft(NumOpsD, Reg)
		except:
			pass
		count = count +1

		####
	try:
		if printDispatcherEAX == True:
			printListDG_EAX(NumOpsD)		
	except:
		pass
	try:
		if printDispatcherEBX == True:
			printListDG_EBX(NumOpsD)
	except:
		pass
	try:
		if printDispatcherECX == True:
			printListDG_ECX(NumOpsD)
	except:
		pass
	try:
		if printDispatcherEDX == True:
			printListDG_EDX(NumOpsD)
	except:
		pass
	try:
		if printDispatcherEDI == True:
			printListDG_EDI(NumOpsD)
	except:
		pass
	try:
		if printDispatcherESI == True:
			printListDG_ESI(NumOpsD)
	except:
		pass
	try:
		if printDispatcherEBP == True:
			printListDG_EBP(NumOpsD)
	except:
		pass
	try:
		if printDispatcherEAXBest == True:
			printListDG_BEST_EAX(NumOpsD)    
	except:
		pass
	try:
		if printDispatcherEBXBest == True:
			printListDG_BEST_EBX(NumOpsD)    
	except:
		pass
	try:
		if printDispatcherECXBest == True:
			printListDG_BEST_ECX(NumOpsD)    
	except:
		pass
	try:
		if printDispatcherEDXBest == True:
			printListDG_BEST_EDX(NumOpsD)    
	except:
		pass
	try:
		if printDispatcherEDIBest == True:
			printListDG_BEST_EDI(NumOpsD)    
	except:
		pass
	try:
		if printDispatcherESIBest == True:
			printListDG_BEST_ESI(NumOpsD)    
	except:
		pass
	try:
		if printDispatcherEBPBest == True:
			printListDG_BEST_EBP(NumOpsD)    
	except:
		pass
	try:
		if printDispatcherEAXOther == True:
			printListDG_Other_EAX(NumOpsD)    
	except:
		pass
	try:
		if printDispatcherEBXOther == True:
			printListDG_Other_EBX(NumOpsD)    
	except:
		pass
	try:
		if printDispatcherECXOther == True:
			printListDG_Other_ECX(NumOpsD)    
	except:
		pass
	try:
		if printDispatcherEDXOther == True:
			printListDG_Other_EDX(NumOpsD)    
	except:
		pass
	try:
		if printDispatcherEDIOther == True:
			printListDG_Other_EDI(NumOpsD)    
	except:
		pass
	try:
		if printDispatcherESIOther == True:
			printListDG_Other_ESI(NumOpsD)    
	except:
		pass
	try:
		if printDispatcherEBPOther == True:
			printListDG_Other_EBP(NumOpsD)    
	except:
		pass

	try:
		if printja == True:
			printlistOP_JMP_EAX(NumOpsD)
			#
			#
			#	o = o + 1
	except:
		pass
	try:
		if printjb == True:
			#objs[o].printlistOP_JMP_EBX(NumOpsD)
			printlistOP_JMP_EBX(NumOpsD)
	except:
		pass
	try:
		if printjc == True:
			printlistOP_JMP_ECX(NumOpsD)
	except:
		pass
	try:
		if printjd == True:
			printlistOP_JMP_EDX(NumOpsD)
	except:
		pass
	try:
		if printjdi == True:
			printlistOP_JMP_EDI(NumOpsD)
	except:
		pass
	try:
		if printjsi == True:
			printlistOP_JMP_ESI(NumOpsD)
	except:
		pass
	try:
		if printjbp == True:
			printlistOP_JMP_EBP(NumOpsD)
	except:
		pass
	try:
		if printjsp == True:
			printlistOP_JMP_ESP(NumOpsD)
	except:
		pass
	try:
		if printca == True:
			printlistOP_CALL_EAX(NumOpsD)
	except:
		pass
	try:
		if printcb == True:
			printlistOP_CALL_EBX(NumOpsD)
	except:
		pass
	try:
		if printcc == True:
			printlistOP_CALL_ECX(NumOpsD)
	except:
		pass
	try:
		if printcd == True:
			printlistOP_CALL_EDX(NumOpsD)
	except:
		pass
	try:
		if printdi == True:
			printlistOP_CALL_EDI(NumOpsD)
	except:
		pass
	try:
		if printsi == True:
			printlistOP_CALL_ESI(NumOpsD)
	except:
		pass
	try:
		if printcbp == True:
			printlistOP_CALL_EBP(NumOpsD)
	except:
		pass
	try:
		if printcsp == True:
			printlistOP_CALL_ESP(NumOpsD)
	except:
		pass

	try:
		if printptrjb == True:
			#objs[o].printlistOP_JMP_PTR_EBX(NumOpsD)
			printlistOP_JMP_PTR_EBX(NumOpsD)
	except:
		pass
	try:
		if printptrjc == True:
			printlistOP_JMP_PTR_ECX(NumOpsD)
	except:
		pass
	try:
		if printptrjd == True:
			printlistOP_JMP_PTR_EDX(NumOpsD)
	except:
		pass
	try:
		if printptrjdi == True:
			printlistOP_JMP_PTR_EDI(NumOpsD)
	except:
		pass
	try:
		if printptrjsi == True:
			printlistOP_JMP_PTR_ESI(NumOpsD)
	except:
		pass
	try:
		if printptrjbp == True:
			printlistOP_JMP_PTR_EBP(NumOpsD)
	except:
		pass
	try:
		if printptrjsp == True:
			printlistOP_JMP_PTR_ESP(NumOpsD)
	except:
		pass
	try:
		if printptrca == True:
			printlistOP_CALL_PTR_EAX(NumOpsD)
	except:
		pass
	try:
		if printptrcb == True:
			printlistOP_CALL_PTR_EBX(NumOpsD)
	except:
		pass
	try:
		if printptrcc == True:
			printlistOP_CALL_PTR_ECX(NumOpsD)
	except:
		pass
	try:
		if printptrcd == True:
			printlistOP_CALL_PTR_EDX(NumOpsD)
	except:
		pass
	try:
		if printptrdi == True:
			printlistOP_CALL_PTR_EDI(NumOpsD)
	except:
		pass
	try:
		if printptrsi == True:
			printlistOP_CALL_PTR_ESI(NumOpsD)
	except:
		pass
	try:
		if printptrcbp == True:
			printlistOP_CALL_PTR_EBP(NumOpsD)
	except:
		pass
	try:
		if printptrcsp == True:
			printlistOP_CALL_PTR_ESP(NumOpsD)
	except:
		pass

def ObtainAndExtractDlls():
	getDLLs()
	global peName
	global PE_DLLS
	global o
	global index
	global modName
	global CheckallModules
	CheckallModules = True

	test = ""
	i = 0
	index = 0
	for dll in PE_DLLS:
		test = extractDLLNew(PE_DLLS[i])
		head, tail = os.path.split(test)
		modName = tail
		i +=1
	PE_DLLS = listReducer(PE_DLLS)
	moreDLLs()
	noApi_MS(PE_DLLS)
	Answer	= set(PE_DLLS) - set(Remove)
	PE_DLLS = list(Answer)
	
	display = ""
	for r in PE_DLLS:
		display = display + r + ", "
	print "DLLs: " + display
	print len(PE_DLLS)

	# index = 0
	# i = 0
	# o = o+1
	# for dll in PE_DLLS:
	# 	print "hi"
	# 	sp()
	# 	test = extractDLLNew(PE_DLLS[i])
	# 	print "hi"
	# 	sp()
	# 	pe = pefile.PE(test)
	# 	print "hi"
	# 	sp()
	# 	objs[o].protect = str(dllName) + "\t"
	# 	objs[o].depStatus = "\tDEP: " + str(dep())
	# 	objs[o].aslrStatus = "\tASLR: " + str(aslr())
	# 	objs[o].sehSTATUS = "\tSAFESEH: " + str(seh())
	# 	objs[o].CFGstatus = "\tCFG: " + str(CFG())
	# 	objs[o].protect = objs[o].protect + objs[o].depStatus + objs[o].aslrStatus + objs[o].sehSTATUS + objs[o].CFGstatus
	# 	DLL_Protect.append(objs[o].protect)
	# 	protect = objs[o].protect
	# 	#print module_path.value
	# 	print "coola"
	# 	print protect
	# 	print "cool"
	# 	sp()
	# 	#getProtectStatus(dll)
	# 	i +=1
	# 	o = o + 1
	# 	print "cool2"
	# 	sp()

	o = 0
	
	modName = peName
	###old
	#zy =0 
	#PE_DLLS = []
	#for dll in PE_DLLS:
		#print "dll " + str(dll)
	#	sp()

		#extractDLL(PE_DLLS[zy])
		#modName = dll
		#print "dll"
		#sp()
		#print peName
	#	zy+=1
		#objs[o].get_OP_CALL_EBX(NumOpsD)
		#print "pename" + str(peName)
	#modName = peName
	#objs[o].get_OP_CALL_EBX(NumOpsD)
	#o = 0
def UI():
	global peName
	global peNameSkip
	global Regs

	#print "\nWhat is your choice?"
	sp()
	#print peName
	x = ""
	
	while x is not "e":
	
	#	print "hello!"
		print "..."
		sp()
		try:
		    r = raw_input()
		    if r[0:1] == "x":
		    	#sys.exit(0)
		     	break
		    if r[0:1] == "f":
		    	if not checkForHelpD(r):
		     		peName = changePE()
		     		if peNameSkip == False:
		     			clearAll()
		     			clearAllObject()
		     			Extraction()
		     			modName = pefile
		     			print "PE change complete..."
		     			sp()
		    if r == "exit":
		    	#sys.exit(0)
		     	break
		    if r[0:1] == "r":
		    	if not checkForHelpD(r):
		     		changeReg()
		    if r[0:1] == "l":
		    	if not checkForHelpD(r):
			     	changelinesGoBack()
		    if r[0:1] == "t":
		    	if not checkForHelpD(r):
		     		changeCF()
		    if r[0:1] == "d": #dispatcher gadet
		    	if not checkForHelpD(r):
		     		checkForDG()
		     		runGetRegsDG()
		    if r[0:1] == "d": #dispatcher gadet
		    	if not checkForHelpD(r):
		     		checkForDG()
		     		runGetRegsDG()
		    if r[0:1] == "j": #dispatcher gadet
		    	# if not checkForHelpD(r):
		     	vpvaSubMenu()
		    if r[0:1] == "p": #printing
		    	if not checkForHelpD(r):
		     		runPrintIt()
		    if r[0:1] == "s": #scope - all of exe or all of exe and modules
		    	if not checkForHelpD(r):
		     		changeCheckAllModules()
		     	print "Setting changed.\nUse the m command to enumerate modules."
		    if r == "m": #debug
		    	ObtainAndExtractDlls()
		    	print "\nEnumeration of modules complete."
		    	sp()
		    if r[0:1] == "c": #4
		    	if not checkForHelpD(r):
		     		clearAllObject()
		     		clearAll()
		    if r[0:1] == "k": # clear
		    	if not checkForHelpD(r):
		     		clearallDLLs()
		     		print "DLLs cleared"
		    if r[0:1] == "n": # Num Ops
		    	if not checkForHelpD(r):
		    		changeNumOps()
		    if r[0:1] == "w": # Num Ops
		    	if not checkForHelpD(r):
		    		showProtectStatus()
		    if (r[0:1] == "g") or (r[0:1] == "z"): # Num Ops
		    	print "Getting it"
		    	sp()
		    	runIt()
		    if (r[0:1] == "G"): # Num Ops
		    	global Regs
		    	print "Getting it"
		    	Regs=["EAX", "EBX", "ECX", "EDX", "EDI", "ESI", "EDI", "EBP", "ESP"]
		    	sp()
		    	runIt()		    	
		    # if r[0:1] == "G": # Num Ops
		    # 	print "DGrun it"
		    # 	sp()
		    # 	runGetRegsDG()
		    if (r[0:1] == "Z"): # Num Ops
		    	global getCALL
		    	global getJMP
		    	getCALL=True
		    	getJMP=True
		    	print "Getting it"
		    	Regs=["EAX", "EBX", "ECX", "EDX", "EDI", "ESI", "EDI", "EBP", "ESP"]
		    	sp()
		    	runIt()		    	
		    # if r[0:1] == "G": # Num Ops
		    # 	print "DGrun it"
		    # 	sp()
		    # 	runGetRegsDG()
		    if r[0:1] == "b": # Num Ops
		    	setHashCheck()
		    if r[0:1] == "u": # 
		    	if not checkForHelpD(r):
		        	testDiss()
		    if r[0:1] == "a": # 
		    	if not checkForHelpD(r):	
		    		DoEverythingFunc()
		    		CheckDoEverything()
		    if r[0:2] == "h ": # 
		    	if not checkForHelpD(r):
		        	break
		    if r[0:1] == "v": # 
		    	if not checkForHelpD(r):
		    		clearAll()
		     		clearAllObject()
		        	generateCSV()
		    if r[0:1] == "y": # 
		    	if not checkForHelpD(r):
		    		usefulInfo()		        	
		    if r[0:1] == "i": # 
		    	if not checkForHelpD(r):
		        	setImageBase()
		    if r[0:1] == "h":
		    	showOptions()
		    # if r[0:1] == "Z":
		    # 	b()
		    if r[0:1] == "T":
		    	testtest2()
		    if r[0:1] == "W":
		    	print "hello"
		    	testtest3()
		except:
		    pass

def b():


	levelTwo = False
	getCALL = False
	getJMP = True
	RegsDG = ["EAX"]
	#RegsDG = ["EAX" ] #, "EBX", "ECX", "EDX", "ESI", "EDI", "EBP"]
	get_OP_JMP_EAX(NumOpsD)
	get_OP_JMP_EBX(NumOpsD)
	get_OP_JMP_ECX(NumOpsD)
	get_OP_JMP_EDX(NumOpsD)
	get_OP_JMP_EDI(NumOpsD)
	get_OP_JMP_ESI(NumOpsD)
	get_OP_JMP_EBP(NumOpsD)
	get_OP_JMP_ESP(NumOpsD)
	get_OP_JMP_PTR_EAX(NumOpsD)
	get_OP_JMP_PTR_EBX(NumOpsD)
	get_OP_JMP_PTR_ECX(NumOpsD)
	get_OP_JMP_PTR_EDX(NumOpsD)
	get_OP_JMP_PTR_EDI(NumOpsD)
	get_OP_JMP_PTR_ESP(NumOpsD)
	get_OP_JMP_PTR_EBP(NumOpsD)
	get_OP_JMP_PTR_ESI(NumOpsD)
	runGetRegsDGNew()



	CheckallModules = False
	Regs =["EAX", "EBX", "ECX"]

	RegsPrint = ["EAX", "EBX", "ECX", "EDX", "EDI", "ESI", "EBP","ESP"]
	#RegsPrint =["ALL"]
	printStack == True
	#s = raw_input()
	for x in range(1):
		print "printing"
		sp()
		preprocessOP_SP(NumOpsD, "EAX")
		sortBytesSPAll()
#		test=raw_input()

	Reg = "EDX"
	buildPopRets()
#now9
	#doStackPivotTasks(s1,s2,"\n0x11223344 #\n")
	#printOutputs()
	testtest2()

def initVPVA():
	print "Clearing previous settings"
	clearAll()
	clearAllObject()
	print "Getting JMP EAX"
	get_OP_JMP_EAX(NumOpsD)
	print "Done getting EAX"
	print "Getting JMP EBX"
	get_OP_JMP_EBX(NumOpsD)
	print "Done getting EBX"
	print "Getting JMP ECX"
	get_OP_JMP_ECX(NumOpsD)
	print "Done getting ECX"
	print "Getting JMP EDX"
	get_OP_JMP_EDX(NumOpsD)
	print "Done getting EDX"
	print "Getting JMP EDI"
	get_OP_JMP_EDI(NumOpsD)
	print "Done getting EDI"
	print "Getting JMP ESI"
	get_OP_JMP_ESI(NumOpsD)
	print "Done getting ESI"
	print "Getting JMP EBP"
	get_OP_JMP_EBP(NumOpsD)
	print "Done getting EBP"
	print "Getting JMP ESP"
	get_OP_JMP_ESP(NumOpsD)
	print "Done getting ESP"
	
	get_OP_JMP_PTR_EAX(NumOpsD)
	get_OP_JMP_PTR_EBX(NumOpsD)
	get_OP_JMP_PTR_ECX(NumOpsD)
	get_OP_JMP_PTR_EDX(NumOpsD)
	get_OP_JMP_PTR_EDI(NumOpsD)
	get_OP_JMP_PTR_ESP(NumOpsD)
	get_OP_JMP_PTR_EBP(NumOpsD)
	get_OP_JMP_PTR_ESI(NumOpsD)
	runGetRegsDGNew()
	preprocessOP_SP(NumOpsD, "EAX")
	sortBytesSPAll()
	Regs=["EAX", "EBX", "ECX", "EDX", "EDI", "ESI", "EDI", "EBP", "ESP"]
	RegsDG=["EAX", "EBX", "ECX", "EDX", "EDI", "ESI", "EDI", "EBP", "ESP"]
	buildPopRets()

def initVPVA_Use_Existing():
	clearListSpecialPOP()
	clearGlobalOutputs()
	clearAllSPSpecialArrays()
	preprocessOP_SP(NumOpsD, "EAX")
	sortBytesSPAll()
	Regs=["EAX", "EBX", "ECX", "EDX", "EDI", "ESI", "EDI", "EBP", "ESP"]
	RegsDG=["EAX", "EBX", "ECX", "EDX", "EDI", "ESI", "EDI", "EBP", "ESP"]
	buildPopRets()
def buildPopRets():
	get_OP_RET(NumOpsD)
	
	# printlistOP_Ret_Pop(NumOpsD, "EAX")
	# # printlistOP_Ret_Pop(NumOpsD, "EBX")
	# # printlistOP_Ret_Pop(NumOpsD, "ECX")
	# # printlistOP_Ret_Pop(NumOpsD, "EBP")
	# # printlistOP_Ret_Pop(NumOpsD, "EBP")
	# # printlistOP_Ret_Pop(NumOpsD, "ESP")
	preprocessOP_PopRet(NumOpsD, best, "ok")
	preprocessOP_PopRet(NumOpsD, best, "best")

	# print "\n\nspecial"
	# t2, g2, b2=returnPopEAX()
	# print "ok? eAx: " + g2
	# t2, g2, b2=returnPopEBX()
	# print "ok? ebx: " + g2
	# t2, g2, b2=returnPopECX()
	# print "ok? ecx: " + g2
	# print b2
	# t2, g2, b2=returnPopEDX()
	# print "ok? edx: " + g2
	# t2, g2, b2=returnPopEDI()
	# print "ok? edi: " + g2
	# t2, g2, b2=returnPopESI()
	# print "ok? eSI: " + g2
	# t2, g2, b2=returnPopEBP()
	# print "ok? eBP: " + g2
	# t2, g2, b2=returnPopESP()
	# print "ok? eSP: " + g2


	# print "special2"
	# g, b = calcRegforDispatcher("EBX")
	# print g
	# print b

	# # print "preload "
	# print preLoad("EBX")

	# g,b, dt =  calcRegforDispatchTable("EAX")	
	# print "dispatch table"
	# print g
	# print b
	# print dt

	# callstoVP()

def resetAfterVAPACalls():
	clearSave()
	vacounterReset()
	vpcounterReset()

def testtest2():
	# printOutputs()

	levelTwo = False
	getCALL = False
	getJMP = True
	RegsDG = ["EAX"]
	#RegsDG = ["EAX" ] #, "EBX", "ECX", "EDX", "ESI", "EDI", "EBP"]
#	get_OP_JMP_EAX(NumOpsD)
	#get_OP_JMP_EBX(NumOpsD)
	#get_OP_JMP_ECX(NumOpsD)
	#get_OP_JMP_EDX(NumOpsD)
	CheckallModules = False
	Regs =["EAX", "ECX","EBX","EDI","ESI", "EBP","ESP"]

	RegsPrint = ["EDX"]
	printStack == True

	doFinalVA(5)
	# callstoVP()
	# print FinalVA("EAX",0)
	# print "vp1:"
	# for x in range(5):
	# 	print FinalVA("EAX",0)
	# 	# print FinalVP("EDX",0)
	# resetAfterVAPACalls()
	# for x in range(5):

	# 	print "vp3:"
	# 	print FinalVA("EBX",0)
	# resetAfterVAPACalls()
	# for x in range(5):
	# 	print "vp3:"
	# 	print FinalVA("ECX",0)
	# resetAfterVAPACalls()
	# # print FinalVA("ECX",0)
	# print FinalVA("EDX",0)
	# print FinalVA("EDI",0)
	# print FinalVA("ESI",0)
	# print FinalVA("ESP",0)
	# print FinalVA("EBP",0)

	# print "find DG"
	# print preprocessOP_DG(NumOpsD, "EAX")


def doFinalVA(z):
	global RegsVP
	outVA=""
	outVP=""
	for Reg in RegsVP:
		if Reg=="EAX":
			for x in range(z):
				outVA+= FinalVA("EAX",0)
				outVP+= FinalVP("EAX",0)
				# print outVA
			resetAfterVAPACalls()
		if Reg=="EBX":	
			for x in range(z):
				outVA+=  FinalVA("EBX",0)
				outVP+= FinalVP("EBX",0)
				# print outVA
			resetAfterVAPACalls()
		if Reg=="ECX":	
			for x in range(z):
				outVA+= FinalVA("ECX",0)
				outVP+= FinalVP("ECX",0)
				# print outVA
			resetAfterVAPACalls()
		if Reg=="EDX"	:
			for x in range(z):
				outVA+=  FinalVA("EDX",0)
				outVP+= FinalVP("EDX",0)
				# print outVA
			resetAfterVAPACalls()
		if Reg=="EDI":	
			for x in range(z):
				outVA+=  FinalVA("EDI",0)
				outVP+= FinalVP("EDI",0)
				# print outVA
			resetAfterVAPACalls()
		if Reg=="ESI":	
			for x in range(z):
				outVA+=  FinalVA("ESI",0)
				outVP+= FinalVP("ESI",0)
				# print outVA
			resetAfterVAPACalls()
		if Reg=="EBP":	
			for x in range(z):
				outVA+= FinalVA("EBP",0)
				outVP+= FinalVP("EBP",0)
				# print outVA
			resetAfterVAPACalls()
	idval=1
	while os.path.exists("%s-JOP_CHAINS-%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-JOP_CHAINS-" + str(idval) + ".txt"
	# print outVP
	# print outVA
	with open(filename, 'a') as f:
		print >> f, outVA
		print >> f, outVP
		print "\t"+filename + " has been written to disk"

diffEach=0
def differentEachTime():
	global diffEach
	diffEach +=1
	return diffEach

def testtest3():

	levelTwo = False
	getCALL = False
	getJMP = True
	RegsDG = ["EAX"]
	#RegsDG = ["EAX" ] #, "EBX", "ECX", "EDX", "ESI", "EDI", "EBP"]
	get_OP_JMP_EAX(NumOpsD)
	get_OP_JMP_EBX(NumOpsD)
	get_OP_JMP_ECX(NumOpsD)
	get_OP_JMP_EDX(NumOpsD)
	CheckallModules = False
	Regs =["EAX", "EBX", "ECX", "EDX"]

	RegsPrint = ["EAX"]
	#RegsPrint =["ALL"]
	printStack == True
	#s = raw_input()
	r1="eax"
	r2="eax"
	best=2
	for Reg in RegsPrint:
		print "printing"
		sp()
		#preprocessOP_Pop(NumOpsD, r1,r2, best)
		print "done"
		sp()
		#sortBytesSPAll()
#		test=raw_input()
		# printlistOP_SP3(NumOpsD, Reg)

		#s1, s2=getStackPivotAsLists(NumOpsD, Reg)

def get_OP_RET( numOps):
	global o
	while numOps > 6:   # Num of Ops to go back
		t=0;		
		for v in objs[o].data2:
			test = ord(OP_RET[0])
			if (ord(objs[o].data2[t]) == test):
						disHereRet(t, numOps)
			t=t+1
		numOps = numOps -1
	objs[o].listOP_RET = copy.copy(listOP_Base)
	objs[o].listOP_RET_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_RET_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_RET_Module = copy.copy(listOP_Base_Module)
	
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_JMP_EAX( NumOpsDis):
	global o

	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;		
		for v in objs[o].data2:
			test = ord(OP_JMP_EAX[0])
			test2 = ord(OP_JMP_EAX[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
						disHereJmp(t, numOps, "ALL")
			t=t+1
		numOps = numOps -1
	# print "specAnswer"
	# print len(listOP_Base)	

	# ok=raw_input()
	objs[o].listOP_JMP_EAX2 = copy.copy(listOP_Base)
	objs[o].listOP_JMP_EAX_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_JMP_EAX_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_JMP_EAX_Module = copy.copy(listOP_Base_Module)
	
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_JMP_EBX(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_JMP_EBX[0])
			test2 = ord(OP_JMP_EBX[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereJmp(t, numOps, "ALL")
			t=t+1
		numOps = numOps -1
	objs[o].listOP_JMP_EBX = copy.copy(listOP_Base)
	objs[o].listOP_JMP_EBX_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_JMP_EBX_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_JMP_EBX_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []
def get_OP_JMP_ECX(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_JMP_ECX[0])
			test2 = ord(OP_JMP_ECX[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereJmp(t, numOps, "ALL")
			t=t+1
		numOps = numOps -1
	objs[o].listOP_JMP_ECX = copy.copy(listOP_Base)
	objs[o].listOP_JMP_ECX_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_JMP_ECX_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_JMP_ECX_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_JMP_EDX(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_JMP_EDX[0])
			test2 = ord(OP_JMP_EDX[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereJmp(t, numOps, "ALL")
			t=t+1
		numOps = numOps -1
	objs[o].listOP_JMP_EDX = copy.copy(listOP_Base)
	objs[o].listOP_JMP_EDX_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_JMP_EDX_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_JMP_EDX_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_JMP_EDI(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_JMP_EDI[0])
			test2 = ord(OP_JMP_EDI[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereJmp(t, numOps, "ALL")
			t=t+1
		numOps = numOps -1
	objs[o].listOP_JMP_EDI = copy.copy(listOP_Base)
	objs[o].listOP_JMP_EDI_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_JMP_EDI_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_JMP_EDI_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []
def get_OP_JMP_ESI(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_JMP_ESI[0])
			test2 = ord(OP_JMP_ESI[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereJmp(t, numOps, "ALL")
			t=t+1
		numOps = numOps -1
	objs[o].listOP_JMP_ESI = copy.copy(listOP_Base)
	objs[o].listOP_JMP_ESI_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_JMP_ESI_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_JMP_ESI_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_JMP_EBP(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_JMP_EBP[0])
			test2 = ord(OP_JMP_EBP[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereJmp(t, numOps, "ALL")
			t=t+1
		numOps = numOps -1
	objs[o].listOP_JMP_EBP = copy.copy(listOP_Base)
	objs[o].listOP_JMP_EBP_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_JMP_EBP_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_JMP_EBP_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_JMP_ESP(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_JMP_ESP[0])
			test2 = ord(OP_JMP_ESP[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereJmp(t, numOps, "ALL")
			t=t+1
		numOps = numOps -1
	objs[o].listOP_JMP_ESP = copy.copy(listOP_Base)
	objs[o].listOP_JMP_ESP_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_JMP_ESP_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_JMP_ESP_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_CALL_EAX(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_CALL_EAX[0])
			test2 = ord(OP_CALL_EAX[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereCall(t, numOps)
			t=t+1
		numOps = numOps -1
	objs[o].listOP_CALL_EAX = copy.copy(listOP_Base)
	objs[o].listOP_CALL_EAX_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_CALL_EAX_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_CALL_EAX_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_CALL_EBX(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_CALL_EBX[0])
			test2 = ord(OP_CALL_EBX[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereCall(t, numOps)
			t=t+1
		numOps = numOps -1
	objs[o].listOP_CALL_EBX = copy.copy(listOP_Base)
	objs[o].listOP_CALL_EBX_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_CALL_EBX_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_CALL_EBX_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []
def get_OP_CALL_ECX(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_CALL_ECX[0])
			test2 = ord(OP_CALL_ECX[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereCall(t, numOps)
			t=t+1
		numOps = numOps -1
	objs[o].listOP_CALL_ECX = copy.copy(listOP_Base)
	objs[o].listOP_CALL_ECX_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_CALL_ECX_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_CALL_ECX_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_CALL_EDX(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_CALL_EDX[0])
			test2 = ord(OP_CALL_EDX[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereCall(t, numOps)
			t=t+1
		numOps = numOps -1
	objs[o].listOP_CALL_EDX = copy.copy(listOP_Base)
	objs[o].listOP_CALL_EDX_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_CALL_EDX_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_CALL_EDX_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_CALL_EDI(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_CALL_EDI[0])
			test2 = ord(OP_CALL_EDI[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereCall(t, numOps)
			t=t+1
		numOps = numOps -1
	objs[o].listOP_CALL_EDI = copy.copy(listOP_Base)
	objs[o].listOP_CALL_EDI_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_CALL_EDI_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_CALL_EDI_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_CALL_ESI(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_CALL_ESI[0])
			test2 = ord(OP_CALL_ESI[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereCall(t, numOps)
			t=t+1
		numOps = numOps -1
	objs[o].listOP_CALL_ESI = copy.copy(listOP_Base)
	objs[o].listOP_CALL_ESI_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_CALL_ESI_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_CALL_ESI_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_CALL_EBP(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_CALL_EBP[0])
			test2 = ord(OP_CALL_EBP[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereCall(t, numOps)
			t=t+1
		numOps = numOps -1
	objs[o].listOP_CALL_EBP = copy.copy(listOP_Base)
	objs[o].listOP_CALL_EBP_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_CALL_EBP_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_CALL_EBP_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_CALL_ESP(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_CALL_ESP[0])
			test2 = ord(OP_CALL_ESP[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereCall(t, numOps)
			t=t+1
		numOps = numOps -1
	objs[o].listOP_CALL_ESP = copy.copy(listOP_Base)
	objs[o].listOP_CALL_ESP_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_CALL_ESP_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_CALL_ESP_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

#n2
def get_OP_CALL_PTR_EAX(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_CALL_PTR_EAX[0])
			test2 = ord(OP_CALL_PTR_EAX[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereCallPTR(t, numOps)
			t=t+1
		numOps = numOps -1
	#print listOP_Base
	#print "-test-"
	objs[o].listOP_CALL_PTR_EAX = copy.copy(listOP_Base)
	objs[o].listOP_CALL_PTR_EAX_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_CALL_PTR_EAX_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_CALL_PTR_EAX_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_CALL_PTR_EBX(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_CALL_PTR_EBX[0])
			test2 = ord(OP_CALL_PTR_EBX[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereCallPTR(t, numOps)
			t=t+1
		numOps = numOps -1
	objs[o].listOP_CALL_PTR_EBX = copy.copy(listOP_Base)
	objs[o].listOP_CALL_PTR_EBX_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_CALL_PTR_EBX_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_CALL_PTR_EBX_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_CALL_PTR_ECX(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_CALL_PTR_ECX[0])
			test2 = ord(OP_CALL_PTR_ECX[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereCallPTR(t, numOps)
			t=t+1
		numOps = numOps -1
	print "basebase\n\n"
	print listOP_Base
	sp()
	objs[o].listOP_CALL_PTR_ECX = copy.copy(listOP_Base)
	objs[o].listOP_CALL_PTR_ECX_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_CALL_PTR_ECX_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_CALL_PTR_ECX_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_CALL_PTR_EDX(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_CALL_PTR_EDX[0])
			test2 = ord(OP_CALL_PTR_EDX[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereCallPTR(t, numOps)
			t=t+1
		numOps = numOps -1
	objs[o].listOP_CALL_PTR_EDX = copy.copy(listOP_Base)
	objs[o].listOP_CALL_PTR_EDX_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_CALL_PTR_EDX_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_CALL_PTR_EDX_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_CALL_PTR_EDI(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_CALL_PTR_EDI[0])
			test2 = ord(OP_CALL_PTR_EDI[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereCallPTR(t, numOps)
			t=t+1
		numOps = numOps -1
	objs[o].listOP_CALL_PTR_EDI = copy.copy(listOP_Base)
	objs[o].listOP_CALL_PTR_EDI_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_CALL_PTR_EDI_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_CALL_PTR_EDI_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_CALL_PTR_ESI(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_CALL_PTR_ESI[0])
			test2 = ord(OP_CALL_PTR_ESI[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereCallPTR(t, numOps)
			t=t+1
		numOps = numOps -1
	objs[o].listOP_CALL_PTR_ESI = copy.copy(listOP_Base)
	objs[o].listOP_CALL_PTR_ESI_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_CALL_PTR_ESI_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_CALL_PTR_ESI_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_CALL_PTR_EBP(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_CALL_PTR_EBP[0])
			test2 = ord(OP_CALL_PTR_EBP[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereCallPTR(t, numOps)
			t=t+1
		numOps = numOps -1
	objs[o].listOP_CALL_PTR_EBP = copy.copy(listOP_Base)
	objs[o].listOP_CALL_PTR_EBP_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_CALL_PTR_EBP_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_CALL_PTR_EBP_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_CALL_PTR_ESP(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_CALL_PTR_ESP[0])
			test2 = ord(OP_CALL_PTR_ESP[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereCallPTR(t, numOps)
			t=t+1
		numOps = numOps -1
	objs[o].listOP_CALL_PTR_ESP = copy.copy(listOP_Base)
	objs[o].listOP_CALL_PTR_ESP_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_CALL_PTR_ESP_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_CALL_PTR_ESP_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_JMP_PTR_EAX(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_JMP_PTR_EAX[0])
			test2 = ord(OP_JMP_PTR_EAX[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereJMPPTR(t, numOps, "all")
					#print "okay"
					#sp()
			t=t+1
		numOps = numOps -1
	
	objs[o].listOP_JMP_PTR_EAX = copy.copy(listOP_Base)
	objs[o].listOP_JMP_PTR_EAX_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_JMP_PTR_EAX_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_JMP_PTR_EAX_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_JMP_PTR_EBX(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_JMP_PTR_EBX[0])
			test2 = ord(OP_JMP_PTR_EBX[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereJMPPTR(t, numOps, "all")
			t=t+1
		numOps = numOps -1
	
	objs[o].listOP_JMP_PTR_EBX = copy.copy(listOP_Base)
	objs[o].listOP_JMP_PTR_EBX_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_JMP_PTR_EBX_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_JMP_PTR_EBX_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_JMP_PTR_ECX(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_JMP_PTR_ECX[0])
			test2 = ord(OP_JMP_PTR_ECX[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereJMPPTR(t, numOps, "all")
			t=t+1
		numOps = numOps -1
	
	objs[o].listOP_JMP_PTR_ECX = copy.copy(listOP_Base)
	objs[o].listOP_JMP_PTR_ECX_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_JMP_PTR_ECX_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_JMP_PTR_ECX_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []
def get_OP_JMP_PTR_EDX(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_JMP_PTR_EDX[0])
			test2 = ord(OP_JMP_PTR_EDX[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereJMPPTR(t, numOps, "all")
			t=t+1
		numOps = numOps -1
	objs[o].listOP_JMP_PTR_EDX = copy.copy(listOP_Base)
	objs[o].listOP_JMP_PTR_EDX_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_JMP_PTR_EDX_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_JMP_PTR_EDX_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_JMP_PTR_EDI(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_JMP_PTR_EDI[0])
			test2 = ord(OP_JMP_PTR_EDI[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereJMPPTR(t, numOps, "all")
			t=t+1
		numOps = numOps -1
	objs[o].listOP_JMP_PTR_EDI = copy.copy(listOP_Base)
	objs[o].listOP_JMP_PTR_EDI_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_JMP_PTR_EDI_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_JMP_PTR_EDI_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_JMP_PTR_ESI(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_JMP_PTR_ESI[0])
			test2 = ord(OP_JMP_PTR_ESI[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereJMPPTR(t, numOps, "all")
			t=t+1
		numOps = numOps -1
	objs[o].listOP_JMP_PTR_ESI = copy.copy(listOP_Base)
	objs[o].listOP_JMP_PTR_ESI_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_JMP_PTR_ESI_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_JMP_PTR_ESI_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_JMP_PTR_EBP(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_JMP_PTR_EBP[0])
			test2 = ord(OP_JMP_PTR_EBP[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereJMPPTR(t, numOps, "all")
			t=t+1
		numOps = numOps -1
	objs[o].listOP_JMP_PTR_EBP = copy.copy(listOP_Base)
	objs[o].listOP_JMP_PTR_EBP_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_JMP_PTR_EBP_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_JMP_PTR_EBP_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_JMP_PTR_ESP(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_JMP_PTR_ESP[0])
			test2 = ord(OP_JMP_PTR_ESP[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereJMPPTR(t, numOps, "all")
			t=t+1
		numOps = numOps -1
	objs[o].listOP_JMP_PTR_ESP = copy.copy(listOP_Base)
	objs[o].listOP_JMP_PTR_ESP_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_JMP_PTR_ESP_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_JMP_PTR_ESP_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_CALL_PTR_EAX(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_CALL_PTR_EAX[0])
			test2 = ord(OP_CALL_PTR_EAX[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereCALLPTR(t, numOps, "all")
					#print "okay"
					#sp()
			t=t+1
		numOps = numOps -1

	objs[o].listOP_CALL_PTR_EAX = copy.copy(listOP_Base)
	objs[o].listOP_CALL_PTR_EAX_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_CALL_PTR_EAX_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_CALL_PTR_EAX_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []


def get_OP_CALL_PTR_EBX(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_CALL_PTR_EBX[0])
			test2 = ord(OP_CALL_PTR_EBX[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereCALLPTR(t, numOps, "all")
			t=t+1
		numOps = numOps -1
	
	objs[o].listOP_CALL_PTR_EBX = copy.copy(listOP_Base)
	objs[o].listOP_CALL_PTR_EBX_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_CALL_PTR_EBX_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_CALL_PTR_EBX_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_CALL_PTR_ECX(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_CALL_PTR_ECX[0])
			test2 = ord(OP_CALL_PTR_ECX[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereCALLPTR(t, numOps, "all")
			t=t+1
		numOps = numOps -1
	objs[o].listOP_CALL_PTR_ECX = copy.copy(listOP_Base)
	objs[o].listOP_CALL_PTR_ECX_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_CALL_PTR_ECX_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_CALL_PTR_ECX_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []
	
def get_OP_CALL_PTR_EDX(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_CALL_PTR_EDX[0])
			test2 = ord(OP_CALL_PTR_EDX[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereCALLPTR(t, numOps, "all")
			t=t+1
		numOps = numOps -1
	objs[o].listOP_CALL_PTR_EDX = copy.copy(listOP_Base)
	objs[o].listOP_CALL_PTR_EDX_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_CALL_PTR_EDX_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_CALL_PTR_EDX_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_CALL_PTR_EDI(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_CALL_PTR_EDI[0])
			test2 = ord(OP_CALL_PTR_EDI[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereCALLPTR(t, numOps, "all")
			t=t+1
		numOps = numOps -1
	objs[o].listOP_CALL_PTR_EDI = copy.copy(listOP_Base)
	objs[o].listOP_CALL_PTR_EDI_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_CALL_PTR_EDI_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_CALL_PTR_EDI_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_CALL_PTR_ESI(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_CALL_PTR_ESI[0])
			test2 = ord(OP_CALL_PTR_ESI[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereCALLPTR(t, numOps, "all")
			t=t+1
		numOps = numOps -1
	objs[o].listOP_CALL_PTR_ESI = copy.copy(listOP_Base)
	objs[o].listOP_CALL_PTR_ESI_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_CALL_PTR_ESI_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_CALL_PTR_ESI_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_CALL_PTR_EBP(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_CALL_PTR_EBP[0])
			test2 = ord(OP_CALL_PTR_EBP[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereCALLPTR(t, numOps, "all")
			t=t+1
		numOps = numOps -1
	objs[o].listOP_CALL_PTR_EBP = copy.copy(listOP_Base)
	objs[o].listOP_CALL_PTR_EBP_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_CALL_PTR_EBP_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_CALL_PTR_EBP_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []

def get_OP_CALL_PTR_ESP(NumOpsDis):
	numOps = NumOpsDis
	while numOps > 6:   # Num of Ops to go back
		t=0;
		for v in objs[o].data2:
			test = ord(OP_CALL_PTR_ESP[0])
			test2 = ord(OP_CALL_PTR_ESP[1])
			if (ord(objs[o].data2[t]) == test):
				if (ord(objs[o].data2[t+1]) == test2):
					disHereCALLPTR(t, numOps, "all")
			t=t+1
		numOps = numOps -1
	objs[o].listOP_CALL_PTR_ESP = copy.copy(listOP_Base)
	objs[o].listOP_CALL_PTR_ESP_CNT = copy.copy(listOP_Base_CNT)
	objs[o].listOP_CALL_PTR_ESP_NumOps = copy.copy(listOP_Base_NumOps)
	objs[o].listOP_CALL_PTR_ESP_Module = copy.copy(listOP_Base_Module)
	listOP_Base_CNT[:] = []
	listOP_Base[:] = []
	listOP_Base_NumOps[:] = []
	listOP_Base_Module[:] = []



def printlistOP_JMP_EAX(NumOpsDis):
	global o
	idval = 1
	clearHashChecker()
	while os.path.exists("%s-JMP EAX ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"JMP EAX ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_JMP_EAX2.__len__()
			for i in range (cnt):
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_JMP_EAX2[i]
				cnt = objs[o].listOP_JMP_EAX_CNT[i]
				num = objs[o].listOP_JMP_EAX_NumOps[i]
				mod = objs[o].listOP_JMP_EAX_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean2(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			val =objs[o].listOP_JMP_EAX2.__len__()
			total = val + total
			counterReset()
			o = o + 1
		out = "JOP ROCKET"
		print >> f, out
	o = 0
	if total == 0:
		nope(filename, total)
	# nope2(filename, total, objs[0].listOP_JMP_EAX2[0])


def printlistOP_JMP_EBX(NumOpsDis):
	global o
	idval = 1
	clearHashChecker()
	while os.path.exists("%s-JMP EBX ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"JMP EBX ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_JMP_EBX.__len__()
			for i in range (cnt):
				#print "\n*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^\n"
				#print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"

				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_JMP_EBX[i]
				cnt = objs[o].listOP_JMP_EBX_CNT[i]
				num = objs[o].listOP_JMP_EBX_NumOps[i]
				mod = objs[o].listOP_JMP_EBX_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				#print str(addy) + "\t" +str(cnt)+ "\t" +str(num)+ "\t" + str(mod)
				sp()
				cat = disHereClean2(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			val =objs[o].listOP_JMP_EBX.__len__()
			total = val + total
			out = "JOP ROCKET" # JMP EBX total: " + str(val)
			#print out
			print >> f, out
			counterReset()
			o = o + 1
		out = ""#"# Grand total JMP EBX total: " + str(total)
		#print out
		#print >> f, out
	o = 0
	if total == 0:
		nope(filename, total)
	nope2(filename, total, objs[0].listOP_JMP_EBX[0])


def printlistOP_JMP_ECX(NumOpsDis):
	global o
	idval = 1
	while os.path.exists("%s-JMP ECX ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"JMP ECX ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_JMP_ECX.__len__()
			for i in range (cnt):
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_JMP_ECX[i]
				cnt = objs[o].listOP_JMP_ECX_CNT[i]
				num = objs[o].listOP_JMP_ECX_NumOps[i]
				mod = objs[o].listOP_JMP_ECX_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean2(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			val =objs[o].listOP_JMP_ECX.__len__()
			total = val + total
			counterReset()
			o = o + 1
		out = "JOP ROCKET"
		print >> f, out
	o = 0
	if total == 0:
		nope(filename, total)
	nope2(filename, total, objs[0].listOP_JMP_ECX[0])


def printlistOP_JMP_EDX(NumOpsDis):
	global o
	idval = 1
	while os.path.exists("%s-JMP EDX ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"JMP EDX ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_JMP_EDX.__len__()
			for i in range (cnt):
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_JMP_EDX[i]
				cnt = objs[o].listOP_JMP_EDX_CNT[i]
				num = objs[o].listOP_JMP_EDX_NumOps[i]
				mod = objs[o].listOP_JMP_EDX_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean2(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			val =objs[o].listOP_JMP_EDX.__len__()
			total = val + total
			counterReset()
			o = o + 1
		out = "JOP ROCKET"
		print >> f, out
	o = 0
	if total == 0:
		nope(filename, total)
	nope2(filename, total, objs[0].listOP_JMP_EDX[0])


def printlistOP_JMP_EDI(NumOpsDis):
	global o
	idval = 1
	while os.path.exists("%s-JMP EDI ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"JMP EDI ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_JMP_EDI.__len__()
			for i in range (cnt):
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_JMP_EDI[i]
				cnt = objs[o].listOP_JMP_EDI_CNT[i]
				num = objs[o].listOP_JMP_EDI_NumOps[i]
				mod = objs[o].listOP_JMP_EDI_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean2(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			val =objs[o].listOP_JMP_EDI.__len__()
			total = val + total
			counterReset()
			o = o + 1
		out = "JOP ROCKET"
		print >> f, out
	o = 0
	if total == 0:
		nope(filename, total)
	nope2(filename, total, objs[0].listOP_JMP_EDI[0])

def printlistOP_JMP_ESI(NumOpsDis):
	global o
	idval = 1
	while os.path.exists("%s-JMP ESI ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"JMP ESI ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_JMP_ESI.__len__()
			for i in range (cnt):
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_JMP_ESI[i]
				cnt = objs[o].listOP_JMP_ESI_CNT[i]
				num = objs[o].listOP_JMP_ESI_NumOps[i]
				mod = objs[o].listOP_JMP_ESI_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean2(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			val =objs[o].listOP_JMP_ESI.__len__()
			total = val + total
			counterReset()
			o = o + 1
		out = "JOP ROCKET"
		print >> f, out
	o = 0
	if total == 0:
		nope(filename, total)
	nope2(filename, total, objs[0].listOP_JMP_ESI[0])

def printlistOP_JMP_EBP(NumOpsDis):
	global o
	idval = 1
	while os.path.exists("%s-JMP EBP ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"JMP EBP ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_JMP_EBP.__len__()
			for i in range (cnt):
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_JMP_EBP[i]
				cnt = objs[o].listOP_JMP_EBP_CNT[i]
				num = objs[o].listOP_JMP_EBP_NumOps[i]
				mod = objs[o].listOP_JMP_EBP_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean2(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			val =objs[o].listOP_JMP_EBP.__len__()
			total = val + total
			counterReset()
			o = o + 1
		out = "JOP ROCKET"
		print >> f, out
	o = 0
	if total == 0:
		nope(filename, total)
	nope2(filename, total, objs[0].listOP_JMP_EBP[0])

def printlistOP_JMP_ESP(NumOpsDis):
	global o
	idval = 1
	while os.path.exists("%s-JMP ESP ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"JMP ESP ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_JMP_ESP.__len__()
			for i in range (cnt):
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_JMP_ESP[i]
				cnt = objs[o].listOP_JMP_ESP_CNT[i]
				num = objs[o].listOP_JMP_ESP_NumOps[i]
				mod = objs[o].listOP_JMP_ESP_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean2(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			val =objs[o].listOP_JMP_ESP.__len__()
			total = val + total
			counterReset()
			o = o + 1
		out = "JOP ROCKET"
		print >> f, out
	o = 0
	if total == 0:
		nope(filename, total)
	nope2(filename, total, objs[0].listOP_JMP_ESP[0])

def printlistOP_JMP_PTR_EAX(NumOpsDis):
	global o
	idval = 1
	clearHashChecker()
	counterReset()
	while os.path.exists("%s-JMP PTR EAX ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"JMP PTR EAX ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_JMP_PTR_EAX.__len__()
			for i in range (cnt):

				print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
				counter()
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_JMP_PTR_EAX[i]
				cnt = objs[o].listOP_JMP_PTR_EAX_CNT[i]
				num = objs[o].listOP_JMP_PTR_EAX_NumOps[i]
				mod = objs[o].listOP_JMP_PTR_EAX_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)

				print >> f, Ct () + "\t" + out
				#print disHereClean(addy, cnt, num, "jmp")
				print >> f, disHereClean2(addy, cnt, num, "jmp")
			val =objs[o].listOP_JMP_PTR_EAX.__len__()
			total = val + total
			out = "# JMP PTR [EAX] total" " + str(val)"
			#print out
			print >> f, out
			counterReset()
			o = o + 1
		out = ""#"# Grand total JMP PTR [EAX] total" " + str(total)
		#print out
		print >> f, out
	o = 0
	nope(filename, total)


def printlistOP_RET(NumOpsDis):
	global o
	idval = 1
	clearHashChecker()
	counterReset()
	while os.path.exists("%s-RET ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"RET ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_RET.__len__()
			for i in range (cnt):

				print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
				counter()
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_RET[i]
				cnt = objs[o].listOP_RET_CNT[i]
				num = objs[o].listOP_RET_NumOps[i]
				mod = objs[o].listOP_RET_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)

				print >> f, Ct () + "\t" + out
				#print disHereClean(addy, cnt, num, "jmp")
				print >> f, disHereClean3(addy, cnt, num, "ret")
			val =objs[o].listOP_RET.__len__()
			total = val + total
			out = "# Ret total" " + str(val)"
			#print out
			print >> f, out
			counterReset()
			o = o + 1
		out = ""#"# Grand total JMP PTR [EAX] total" " + str(total)
		#print out
		print >> f, out
	o = 0
	nope(filename, total)

def printlistOP_RET_POP_EDI(NumOpsDis):
	global o
	idval = 1
	clearHashChecker()
	counterReset()
	while os.path.exists("%s-RET_EDI_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"RET_EDI_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_RET_Pop_EDI.__len__()
			for i in range (cnt):

				print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
				counter()
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_RET_Pop_EDI[i]
				cnt = objs[o].listOP_RET_Pop_EDI_CNT[i]
				num = objs[o].listOP_RET_Pop_EDI_NumOps[i]
				mod = objs[o].listOP_RET_Pop_EDI_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)

				print >> f, Ct () + "\t" + out
				#print disHereClean(addy, cnt, num, "jmp")
				print >> f, disHereClean3(addy, cnt, num, "ret")
				# print >> f, disHereClean2(addy, cnt, num, "jmp")
				
			val =objs[o].listOP_RET_Pop_EDI.__len__()
			total = val + total
			out = "# Ret total" " + str(val)"
			#print out
			print >> f, out
			counterReset()
			o = o + 1
			clearGOuts()
		out = ""#"# Grand total JMP PTR [EAX] total" " + str(total)
		#print out
		print >> f, out
	o = 0
	# nope(filename, total)

def printlistOP_Ret_Pop(NumOpsDis, Reg):
	global o
	clearHashChecker()
	idval = 1
	while os.path.exists("%s-RET_POP_OP_%s_%s.txt" % (peName, Reg, idval)):
	    idval += 1
	filename = peName +"-"+"RET_POP_OP_"+Reg+"_" + str( idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		i=0
		total = 0
		temp = []
		for obj in objs:
			# if Reg == "ALL":
			# 	cnt1 = objs[o].listOP_RET_Pop.__len__()

			if Reg == "EAX":
				cnt1 = objs[o].listOP_RET_Pop_EAX.__len__()
				print "real out: " + str(cnt1)
			if Reg == "EBX":
				cnt1 = objs[o].listOP_RET_Pop_EBX.__len__()
			if Reg == "ECX":
				cnt1 = objs[o].listOP_RET_Pop_ECX.__len__()
			if Reg == "EDX":
				cnt1 = objs[o].listOP_RET_Pop_EDX.__len__()
			if Reg == "ESI":
				cnt1 = objs[o].listOP_RET_Pop_ESI.__len__()
			if Reg == "EDI":
				cnt1 = objs[o].listOP_RET_Pop_EDI.__len__()
			if Reg == "ESP":
				cnt1 = objs[o].listOP_RET_Pop_ESP.__len__()
			if Reg == "EBP":
				cnt1 = objs[o].listOP_RET_Pop_EBP.__len__()
			for i in range (cnt1):
				addy =0
				cnt = 0   #
				num = 0
				# if Reg == "ALL":
				# 	addy = objs[o].listOP_RET_Pop[i]
				# 	cnt = objs[o].listOP_RET_Pop_CNT[i]
				# 	num = objs[o].listOP_RET_Pop_NumOps[i]
				# 	mod = objs[o].listOP_RET_Pop_Module[i]
				if Reg == "EAX":
					addy = objs[o].listOP_RET_Pop_EAX[i]
					cnt = objs[o].listOP_RET_Pop_EAX_CNT[i]
					num = objs[o].listOP_RET_Pop_EAX_NumOps[i]
					mod = objs[o].listOP_RET_Pop_EAX_Module[i]
				if Reg == "EBX":
					addy = objs[o].listOP_RET_Pop_EBX[i]
					cnt = objs[o].listOP_RET_Pop_EBX_CNT[i]
					num = objs[o].listOP_RET_Pop_EBX_NumOps[i]
					mod = objs[o].listOP_RET_Pop_EBX_Module[i]
				if Reg == "ECX":
					addy = objs[o].listOP_RET_Pop_ECX[i]
					cnt = objs[o].listOP_RET_Pop_ECX_CNT[i]
					num = objs[o].listOP_RET_Pop_ECX_NumOps[i]
					mod = objs[o].listOP_RET_Pop_ECX_Module[i]
				if Reg == "EDX":
					addy = objs[o].listOP_RET_Pop_EDX[i]
					cnt = objs[o].listOP_RET_Pop_EDX_CNT[i]
					num = objs[o].listOP_RET_Pop_EDX_NumOps[i]
					mod = objs[o].listOP_RET_Pop_EDX_Module[i]
				if Reg == "ESI":
					addy = objs[o].listOP_RET_Pop_ESI[i]
					cnt = objs[o].listOP_RET_Pop_ESI_CNT[i]
					num = objs[o].listOP_RET_Pop_ESI_NumOps[i]
					mod = objs[o].listOP_RET_Pop_ESI_Module[i]
				if Reg == "EDI":
					addy = objs[o].listOP_RET_Pop_EDI[i]
					cnt = objs[o].listOP_RET_Pop_EDI_CNT[i]
					num = objs[o].listOP_RET_Pop_EDI_NumOps[i]
					mod = objs[o].listOP_RET_Pop_EDI_Module[i]
				if Reg == "EBP":
					addy = objs[o].listOP_RET_Pop_EBP[i]
					cnt = objs[o].listOP_RET_Pop_EBP_CNT[i]
					num = objs[o].listOP_RET_Pop_EBP_NumOps[i]
					mod = objs[o].listOP_RET_Pop_EBP_Module[i]
				if Reg == "ESP":
					addy = objs[o].listOP_RET_Pop_ESP[i]
					cnt = objs[o].listOP_RET_Pop_ESP_CNT[i]
					num = objs[o].listOP_RET_Pop_ESP_NumOps[i]
					mod = objs[o].listOP_RET_Pop_ESP_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod) 
				##print out
				cat = disHereClean3(addy, cnt, num, "ret")

				# outs=[]
				if not cat == " ":
					# if  cat not in outs:
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
					# outs.append(cat)
					# print "outs"
					# print outs
			if cnt1 > 0:
			#	out = "# Add " + str(Reg) + " " + str(mod) + " total: " + str(cnt1) 
				temp.append(out)
			total = total + cnt1	
			clearGOuts()
			o = o + 1
		for out in temp:
			#print out
			#print >> f, out
			pass
		out = "\nJOP ROCKET" #out = ""#"# Grand total ADD "  + str(Reg) + " : " + str(total)
		#print out
		#print total
		#print out
		print >> f, out
	o = 0
	nope(filename, total)

def printlistOP_RET_POPold(NumOpsDis):
	global o
	idval = 1
	clearHashChecker()
	counterReset()
	while os.path.exists("%s-RET_POP_ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"RET_POP_ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_RET_Pop.__len__()
			for i in range (cnt):

				print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
				counter()
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_RET_Pop[i]
				cnt = objs[o].listOP_RET_Pop_CNT[i]
				num = objs[o].listOP_RET_Pop_NumOps[i]
				mod = objs[o].listOP_RET_Pop_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)

				print >> f, Ct () + "\t" + out
				#print disHereClean(addy, cnt, num, "jmp")
				print >> f, disHereClean3(addy, cnt, num, "jmp")
			val =objs[o].listOP_RET_Pop.__len__()
			total = val + total
			# out = "# Ret total" " + str(val)
			#print out
			print >> f, out
			counterReset()
			o = o + 1
		out = ""#"# Grand total JMP PTR [EAX] total" " + str(total)
		#print out
		print >> f, out
	o = 0
	nope(filename, total)

def printlistOP_JMP_PTR_EBX(NumOpsDis):
	global o
	idval = 1
	clearHashChecker()
	counterReset()
	while os.path.exists("%s-JMP PTR EBX ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"JMP PTR EBX ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_JMP_PTR_EBX.__len__()
			for i in range (cnt):

				print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
				counter()
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_JMP_PTR_EBX[i]
				cnt = objs[o].listOP_JMP_PTR_EBX_CNT[i]
				num = objs[o].listOP_JMP_PTR_EBX_NumOps[i]
				mod = objs[o].listOP_JMP_PTR_EBX_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)

				print >> f, Ct () + "\t" + out
				#print disHereClean(addy, cnt, num, "jmp")
				print >> f, disHereClean2(addy, cnt, num, "jmp")
			val =objs[o].listOP_JMP_PTR_EBX.__len__()
			total = val + total
			out = "# JMP PTR [EBX] total" " + str(val)"
			#print out
			print >> f, out
			counterReset()
			o = o + 1
		out = ""#"# Grand total JMP PTR [EBX] total" " + str(total)
		#print out
		print >> f, out
	o = 0
	nope(filename, total)

def printlistOP_JMP_PTR_ECX(NumOpsDis):
	global o
	idval = 1
	clearHashChecker()
	counterReset()
	while os.path.exists("%s-JMP PTR ECX ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"JMP PTR ECX ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_JMP_PTR_ECX.__len__()
			for i in range (cnt):

				print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
				counter()
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_JMP_PTR_ECX[i]
				cnt = objs[o].listOP_JMP_PTR_ECX_CNT[i]
				num = objs[o].listOP_JMP_PTR_ECX_NumOps[i]
				mod = objs[o].listOP_JMP_PTR_ECX_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)

				print >> f, Ct () + "\t" + out
				#print disHereClean(addy, cnt, num, "jmp")
				print >> f, disHereClean2(addy, cnt, num, "jmp")
			val =objs[o].listOP_JMP_PTR_ECX.__len__()
			total = val + total
			out = "# JMP PTR [ECX] total" " + str(val)"
			#print out
			print >> f, out
			counterReset()
			o = o + 1
		out = ""#"# Grand total JMP PTR [ECX] total" " + str(total)
		#print out
		print >> f, out
	o = 0
	nope(filename, total)

def printlistOP_JMP_PTR_EDX(NumOpsDis):
	global o
	idval = 1
	clearHashChecker()
	counterReset()
	while os.path.exists("%s-JMP PTR EDX ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"JMP PTR EDX ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_JMP_PTR_EDX.__len__()
			for i in range (cnt):

				print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
				counter()
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_JMP_PTR_EDX[i]
				cnt = objs[o].listOP_JMP_PTR_EDX_CNT[i]
				num = objs[o].listOP_JMP_PTR_EDX_NumOps[i]
				mod = objs[o].listOP_JMP_PTR_EDX_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)

				print >> f, Ct () + "\t" + out
				print >> f, disHereClean2(addy, cnt, num, "jmp")
			val =objs[o].listOP_JMP_PTR_EDX.__len__()
			total = val + total
			out = "# JMP PTR [EDX] total" " + str(val)"
			#print out
			print >> f, out
			counterReset()
			o = o + 1

	o = 0
	nope(filename, total)

def printlistOP_JMP_PTR_ESI(NumOpsDis):
	global o
	idval = 1
	clearHashChecker()
	counterReset()
	while os.path.exists("%s-JMP PTR ESI ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"JMP PTR ESI ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_JMP_PTR_ESI.__len__()
			for i in range (cnt):

				print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
				counter()
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_JMP_PTR_ESI[i]
				cnt = objs[o].listOP_JMP_PTR_ESI_CNT[i]
				num = objs[o].listOP_JMP_PTR_ESI_NumOps[i]
				mod = objs[o].listOP_JMP_PTR_ESI_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)

				print >> f, Ct () + "\t" + out
				print >> f, disHereClean2(addy, cnt, num, "jmp")
			val =objs[o].listOP_JMP_PTR_ESI.__len__()
			total = val + total
			out = "# JMP PTR [ESI] total" " + str(val)"
			#print out
			print >> f, out
			counterReset()
			o = o + 1
		out = ""#"# Grand total JMP PTR [ESI] total" " + str(total)
		#print out
		print >> f, out
	o = 0
	nope(filename, total)

def printlistOP_JMP_PTR_EDI(NumOpsDis):
	global o
	idval = 1
	clearHashChecker()
	counterReset()
	while os.path.exists("%s-JMP PTR EDI ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"JMP PTR EDI ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_JMP_PTR_EDI.__len__()
			for i in range (cnt):

				print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
				counter()
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_JMP_PTR_EDI[i]
				cnt = objs[o].listOP_JMP_PTR_EDI_CNT[i]
				num = objs[o].listOP_JMP_PTR_EDI_NumOps[i]
				mod = objs[o].listOP_JMP_PTR_EDI_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)

				print >> f, Ct () + "\t" + out
				print >> f, disHereClean2(addy, cnt, num, "jmp")
			val =objs[o].listOP_JMP_PTR_EDI.__len__()
			total = val + total
			out = "# JMP PTR [EDI] total" " + str(val)"
			#print out
			print >> f, out
			counterReset()
			o = o + 1
		out = ""#"# Grand total JMP PTR [EDI] total" " + str(total)
		#print out
		print >> f, out
	o = 0
	nope(filename, total)

def printlistOP_JMP_PTR_EBP(NumOpsDis):
	global o
	idval = 1
	clearHashChecker()
	counterReset()
	while os.path.exists("%s-JMP PTR EBP ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"JMP PTR EBP ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_JMP_PTR_EBP.__len__()
			for i in range (cnt):

				print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
				counter()
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_JMP_PTR_EBP[i]
				cnt = objs[o].listOP_JMP_PTR_EBP_CNT[i]
				num = objs[o].listOP_JMP_PTR_EBP_NumOps[i]
				mod = objs[o].listOP_JMP_PTR_EBP_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)

				print >> f, Ct () + "\t" + out
				print >> f, disHereClean2(addy, cnt, num, "jmp")
			val =objs[o].listOP_JMP_PTR_EBP.__len__()
			total = val + total
			out = "# JMP PTR [EBP] total" " + str(val)"
			#print out
			print >> f, out
			counterReset()
			o = o + 1
		out = ""#"# Grand total JMP PTR [EBP] total" " + str(total)
		#print out
		print >> f, out
	o = 0
	nope(filename, total)


def printlistOP_JMP_PTR_ESP(NumOpsDis):
	global o
	idval = 1
	clearHashChecker()
	counterReset()
	while os.path.exists("%s-JMP PTR ESP ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"JMP PTR ESP ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_JMP_PTR_ESP.__len__()
			for i in range (cnt):

				print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
				counter()
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_JMP_PTR_ESP[i]
				cnt = objs[o].listOP_JMP_PTR_ESP_CNT[i]
				num = objs[o].listOP_JMP_PTR_ESP_NumOps[i]
				mod = objs[o].listOP_JMP_PTR_ESP_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)

				print >> f, Ct () + "\t" + out
				print >> f, disHereClean2(addy, cnt, num, "jmp")
			val =objs[o].listOP_JMP_PTR_ESP.__len__()
			total = val + total
			out = "# JMP PTR [ESP] total" " + str(val)"
			#print out
			print >> f, out
			counterReset()
			o = o + 1
		out = ""#"# Grand total JMP PTR [ESP] total" " + str(total)
		#print out
		print >> f, out
	o = 0
	nope(filename, total)



def printlistOP_CALL_EAX(NumOpsDis):
	global o
	idval = 1
	clearHashChecker()
	while os.path.exists("%s-CALL EAX ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"CALL EAX ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_CALL_EAX.__len__()
			for i in range (cnt):
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_CALL_EAX[i]
				cnt = objs[o].listOP_CALL_EAX_CNT[i]
				num = objs[o].listOP_CALL_EAX_NumOps[i]
				mod = objs[o].listOP_CALL_EAX_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean2(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			val =objs[o].listOP_CALL_EAX.__len__()
			total = val + total
			counterReset()
			o = o + 1
		out = "JOP ROCKET"
		print >> f, out
	o = 0
	if total == 0:
		nope(filename, total)
	nope2(filename, total, objs[0].listOP_CALL_EAX[0])


def printlistOP_CALL_EBX(NumOpsDis):
	global o
	idval = 1
	clearHashChecker()
	while os.path.exists("%s-CALL EBX ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"CALL EBX ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_CALL_EBX.__len__()
			for i in range (cnt):
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_CALL_EBX[i]
				cnt = objs[o].listOP_CALL_EBX_CNT[i]
				num = objs[o].listOP_CALL_EBX_NumOps[i]
				mod = objs[o].listOP_CALL_EBX_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean2(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			val =objs[o].listOP_CALL_EBX.__len__()
			total = val + total
			print >> f, out
			counterReset()
			o = o + 1
		out = "JOP ROCKET"#"# Grand total CALL EBX total: " + str(total)
		print >> f, out
	o = 0
	if total == 0:
		nope(filename, total)
	nope2(filename, total, objs[0].listOP_CALL_EBX[0])

def printlistOP_CALL_ECX(NumOpsDis):
	global o
	idval = 1
	while os.path.exists("%s-CALL ECX ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"CALL ECX ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_CALL_ECX.__len__()
			for i in range (cnt):
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_CALL_ECX[i]
				cnt = objs[o].listOP_CALL_ECX_CNT[i]
				num = objs[o].listOP_CALL_ECX_NumOps[i]
				mod = objs[o].listOP_CALL_ECX_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean2(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			val =objs[o].listOP_CALL_ECX.__len__()
			total = val + total
			counterReset()
			o = o + 1
		out = "JOP ROCKET"
		print >> f, out
	o = 0
	if total == 0:
		nope(filename, total)
	nope2(filename, total, objs[0].listOP_CALL_ECX[0])


def printlistOP_CALL_EDX(NumOpsDis):
	global o
	idval = 1
	while os.path.exists("%s-CALL EDX ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"CALL EDX ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_CALL_EDX.__len__()
			for i in range (cnt):
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_CALL_EDX[i]
				cnt = objs[o].listOP_CALL_EDX_CNT[i]
				num = objs[o].listOP_CALL_EDX_NumOps[i]
				mod = objs[o].listOP_CALL_EDX_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean2(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			val =objs[o].listOP_CALL_EDX.__len__()
			total = val + total
			counterReset()
			o = o + 1
		out = "JOP ROCKET"
		print >> f, out
	o = 0
	if total == 0:
		nope(filename, total)
	nope2(filename, total, objs[0].listOP_CALL_EDX[0])


def printlistOP_CALL_EDI(NumOpsDis):
	global o
	idval = 1
	while os.path.exists("%s-CALL EDI ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"CALL EDI ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_CALL_EDI.__len__()
			for i in range (cnt):
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_CALL_EDI[i]
				cnt = objs[o].listOP_CALL_EDI_CNT[i]
				num = objs[o].listOP_CALL_EDI_NumOps[i]
				mod = objs[o].listOP_CALL_EDI_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean2(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			val =objs[o].listOP_CALL_EDI.__len__()
			total = val + total
			counterReset()
			o = o + 1
		out = "JOP ROCKET"
		print >> f, out
	o = 0
	if total == 0:
		nope(filename, total)
	nope2(filename, total, objs[0].listOP_CALL_EDI[0])

def printlistOP_CALL_ESI(NumOpsDis):
	global o
	idval = 1
	while os.path.exists("%s-CALL ESI ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"CALL ESI ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_CALL_ESI.__len__()
			for i in range (cnt):
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_CALL_ESI[i]
				cnt = objs[o].listOP_CALL_ESI_CNT[i]
				num = objs[o].listOP_CALL_ESI_NumOps[i]
				mod = objs[o].listOP_CALL_ESI_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean2(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			val =objs[o].listOP_CALL_ESI.__len__()
			total = val + total
			counterReset()
			o = o + 1
		out = "JOP ROCKET"
		print >> f, out
	o = 0
	if total == 0:
		nope(filename, total)
	nope2(filename, total, objs[0].listOP_CALL_ESI[0])

def printlistOP_CALL_EBP(NumOpsDis):
	global o
	idval = 1
	while os.path.exists("%s-CALL EBP ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"CALL EBP ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_CALL_EBP.__len__()
			for i in range (cnt):
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_CALL_EBP[i]
				cnt = objs[o].listOP_CALL_EBP_CNT[i]
				num = objs[o].listOP_CALL_EBP_NumOps[i]
				mod = objs[o].listOP_CALL_EBP_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean2(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			val =objs[o].listOP_CALL_EBP.__len__()
			total = val + total
			counterReset()
			o = o + 1
		out = "JOP ROCKET"
		print >> f, out
	o = 0
	if total == 0:
		nope(filename, total)
	nope2(filename, total, objs[0].listOP_CALL_EBP[0])

def printlistOP_CALL_ESP(NumOpsDis):
	global o
	idval = 1
	while os.path.exists("%s-CALL ESP ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"CALL ESP ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_CALL_ESP.__len__()
			for i in range (cnt):
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_CALL_ESP[i]
				cnt = objs[o].listOP_CALL_ESP_CNT[i]
				num = objs[o].listOP_CALL_ESP_NumOps[i]
				mod = objs[o].listOP_CALL_ESP_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean2(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			val =objs[o].listOP_CALL_ESP.__len__()
			total = val + total
			counterReset()
			o = o + 1
		out = "JOP ROCKET"
		print >> f, out
	o = 0
	if total == 0:
		nope(filename, total)
	nope2(filename, total, objs[0].listOP_CALL_ESP[0])



def printlistOP_CALL_PTR_EAX(NumOpsDis):
	global o
	idval = 1
	clearHashChecker()
	while os.path.exists("%s-CALL PTR EAX ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"CALL PTR EAX ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_CALL_PTR_EAX.__len__()
			for i in range (cnt):

				print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
				counter()
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_CALL_PTR_EAX[i]
				cnt = objs[o].listOP_CALL_PTR_EAX_CNT[i]
				num = objs[o].listOP_CALL_PTR_EAX_NumOps[i]
				mod = objs[o].listOP_CALL_PTR_EAX_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)

				print >> f, Ct () + "\t" + out
				#print disHereClean(addy, cnt, num, "jmp")
				print >> f, disHereClean2(addy, cnt, num, "jmp")
			val =objs[o].listOP_CALL_PTR_EAX.__len__()
			total = val + total
			#out = "# CALL PTR [EAX] total" " + str(val)"
			#print out
			#print >> f, out
			counterReset()
			o = o + 1
		out = ""#"# Grand total CALL PTR [EAX] total" " + str(total)
		#print out
		print >> f, out
	o = 0
	nope(filename, total)

def printlistOP_CALL_PTR_EBX(NumOpsDis):
	global o
	idval = 1
	clearHashChecker()
	while os.path.exists("%s-CALL PTR EBX ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"CALL PTR EBX ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_CALL_PTR_EBX.__len__()
			for i in range (cnt):

				print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
				counter()
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_CALL_PTR_EBX[i]
				cnt = objs[o].listOP_CALL_PTR_EBX_CNT[i]
				num = objs[o].listOP_CALL_PTR_EBX_NumOps[i]
				mod = objs[o].listOP_CALL_PTR_EBX_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)

				print >> f, Ct () + "\t" + out
				#print disHereClean(addy, cnt, num, "jmp")
				print >> f, disHereClean2(addy, cnt, num, "jmp")
			val =objs[o].listOP_CALL_PTR_EBX.__len__()
			total = val + total
			out = "# CALL PTR [EBX] total" " + str(val)"
			#print out
			print >> f, out
			counterReset()
			o = o + 1
		out = ""#"# Grand total CALL PTR [EBX] total" " + str(total)
		#print out
		print >> f, out
	o = 0
	nope(filename, total)

def printlistOP_CALL_PTR_ECX(NumOpsDis):
	global o
	idval = 1
	clearHashChecker()
	while os.path.exists("%s-CALL PTR ECX ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"CALL PTR ECX ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_CALL_PTR_ECX.__len__()
			for i in range (cnt):

				print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
				counter()
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_CALL_PTR_ECX[i]
				cnt = objs[o].listOP_CALL_PTR_ECX_CNT[i]
				num = objs[o].listOP_CALL_PTR_ECX_NumOps[i]
				mod = objs[o].listOP_CALL_PTR_ECX_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)

				print >> f, Ct () + "\t" + out
				#print disHereClean(addy, cnt, num, "jmp")
				print >> f, disHereClean2(addy, cnt, num, "jmp")
			val =objs[o].listOP_CALL_PTR_ECX.__len__()
			total = val + total
			out = "# CALL PTR [ECX] total" " + str(val)"
			#print out
			print >> f, out
			counterReset()
			o = o + 1
		out = ""#"# Grand total CALL PTR [ECX] total" " + str(total)
		#print out
		print >> f, out
	o = 0
	nope(filename, total)

def printlistOP_CALL_PTR_EDX(NumOpsDis):
	global o
	idval = 1
	clearHashChecker()
	while os.path.exists("%s-CALL PTR EDX ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"CALL PTR EDX ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_CALL_PTR_EDX.__len__()
			for i in range (cnt):

				print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
				counter()
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_CALL_PTR_EDX[i]
				cnt = objs[o].listOP_CALL_PTR_EDX_CNT[i]
				num = objs[o].listOP_CALL_PTR_EDX_NumOps[i]
				mod = objs[o].listOP_CALL_PTR_EDX_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)

				print >> f, Ct () + "\t" + out
				print >> f, disHereClean2(addy, cnt, num, "jmp")
			val =objs[o].listOP_CALL_PTR_EDX.__len__()
			total = val + total
			out = ""# CALL PTR [EDX] total" " + str(val)"
			#print out
			print >> f, out
			counterReset()
			o = o + 1

	o = 0
	nope(filename, total)

def printlistOP_CALL_PTR_ESI(NumOpsDis):
	global o
	idval = 1
	clearHashChecker()
	while os.path.exists("%s-CALL PTR ESI ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"CALL PTR ESI ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_CALL_PTR_ESI.__len__()
			for i in range (cnt):

				print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
				counter()
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_CALL_PTR_ESI[i]
				cnt = objs[o].listOP_CALL_PTR_ESI_CNT[i]
				num = objs[o].listOP_CALL_PTR_ESI_NumOps[i]
				mod = objs[o].listOP_CALL_PTR_ESI_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)

				print >> f, Ct () + "\t" + out
				print >> f, disHereClean2(addy, cnt, num, "jmp")
			val =objs[o].listOP_CALL_PTR_ESI.__len__()
			total = val + total
			out = ""# CALL PTR [ESI] total" " + str(val)"
			#print out
			print >> f, out
			counterReset()
			o = o + 1
		out = ""#"# Grand total CALL PTR [ESI] total" " + str(total)
		#print out
		print >> f, out
	o = 0
	nope(filename, total)

def printlistOP_CALL_PTR_EDI(NumOpsDis):
	global o
	idval = 1
	clearHashChecker()
	while os.path.exists("%s-CALL PTR EDI ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"CALL PTR EDI ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_CALL_PTR_EDI.__len__()
			for i in range (cnt):

				print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
				counter()
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_CALL_PTR_EDI[i]
				cnt = objs[o].listOP_CALL_PTR_EDI_CNT[i]
				num = objs[o].listOP_CALL_PTR_EDI_NumOps[i]
				mod = objs[o].listOP_CALL_PTR_EDI_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)

				print >> f, Ct () + "\t" + out
				print >> f, disHereClean2(addy, cnt, num, "jmp")
			val =objs[o].listOP_CALL_PTR_EDI.__len__()
			total = val + total
			out = ""# CALL PTR [EDI] total" " + str(val)"
			#print out
			print >> f, out
			counterReset()
			o = o + 1
		out = ""#"# Grand total CALL PTR [EDI] total" " + str(total)
		#print out
		print >> f, out
	o = 0
	nope(filename, total)

def printlistOP_CALL_PTR_EBP(NumOpsDis):
	global o
	idval = 1
	clearHashChecker()
	while os.path.exists("%s-CALL PTR EBP ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"CALL PTR EBP ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_CALL_PTR_EBP.__len__()
			for i in range (cnt):

				print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
				counter()
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_CALL_PTR_EBP[i]
				cnt = objs[o].listOP_CALL_PTR_EBP_CNT[i]
				num = objs[o].listOP_CALL_PTR_EBP_NumOps[i]
				mod = objs[o].listOP_CALL_PTR_EBP_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)

				print >> f, Ct () + "\t" + out
				print >> f, disHereClean2(addy, cnt, num, "jmp")
			val =objs[o].listOP_CALL_PTR_EBP.__len__()
			total = val + total
			out = ""# CALL PTR [EBP] total" " + str(val)"
			#print out
			print >> f, out
			counterReset()
			o = o + 1
		out = ""#"# Grand total CALL PTR [EBP] total" " + str(total)
		#print out
		print >> f, out
	o = 0
	nope(filename, total)


def printlistOP_CALL_PTR_ESP(NumOpsDis):
	global o
	idval = 1
	clearHashChecker()
	while os.path.exists("%s-CALL PTR ESP ALL_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"CALL PTR ESP ALL_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		total = 0
		for obj in objs:
			i=0
			cnt = objs[o].listOP_CALL_PTR_ESP.__len__()
			for i in range (cnt):

				print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
				counter()
				addy =0
				cnt = 0   #
				num = 0
				addy = objs[o].listOP_CALL_PTR_ESP[i]
				cnt = objs[o].listOP_CALL_PTR_ESP_CNT[i]
				num = objs[o].listOP_CALL_PTR_ESP_NumOps[i]
				mod = objs[o].listOP_CALL_PTR_ESP_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)

				print >> f, Ct () + "\t" + out
				print >> f, disHereClean2(addy, cnt, num, "jmp")
			val =objs[o].listOP_CALL_PTR_ESP.__len__()
			total = val + total
			out = "# CALL PTR [ESP] total" " + str(val)"
			#print out
			print >> f, out
			counterReset()
			o = o + 1
		out = ""#"# Grand total CALL PTR [ESP] total" " + str(total)
		#print out
		print >> f, out
	o = 0
	nope(filename, total)

def cleaner(addy, Cnt, numOps):
	clearHashChecker()
	for a, c, n in zip(addy, Cnt, numOps):
		cat = disHereClean2(a,c, n)
	return str(len(hashchecker))

#sphere
def printlistOP_SP(NumOpsDis, Reg):
	global o
	clearHashChecker()
	idval = 1

	while os.path.exists("%s-S_PIVOT%s-%s.txt" % (peName, Reg, idval)):
	    idval += 1
	filename = peName +"-S_PIVOT" + Reg + "-" + str(idval) + ".txt"
	fname= filename

	with open(filename, 'a') as f:
		counterReset()
		i=0
		total = 0
		temp = []

		out1 = []
		out2 =[]

		for obj in objs:

			preRegs = ["EAX", "EBX", "ECX","EDX","EDI","ESI","EBP","ESP"]

			for Reg in preRegs:

				if Reg == "ALL":
					cnt1 = objs[o].listOP_BaseStackPivot.__len__()

				if Reg == "EAX":
					cnt1 = objs[o].listOP_BaseStackPivotEAX.__len__()
				if Reg == "EBX":
					cnt1 = objs[o].listOP_BaseStackPivotEBX.__len__()
				if Reg == "ECX":
					cnt1 = objs[o].listOP_BaseStackPivotECX.__len__()
				if Reg == "EDX":
					cnt1 = objs[o].listOP_BaseStackPivotEDX.__len__()
				if Reg == "ESI":
					cnt1 = objs[o].listOP_BaseStackPivotESI.__len__()
				if Reg == "EDI":
					cnt1 = objs[o].listOP_BaseStackPivotEDI.__len__()
				if Reg == "ESP":
					cnt1 = objs[o].listOP_BaseStackPivotESP.__len__()
				if Reg == "EBP":
					cnt1 = objs[o].listOP_BaseStackPivotEBP.__len__()
				for i in range (cnt1):
					addy =0
					cnt = 0   #
					num = 0
					if Reg == "ALL":
						addy = objs[o].listOP_BaseStackPivot[i]
						cnt = objs[o].listOP_BaseStackPivot_CNT[i]
						num = objs[o].listOP_BaseStackPivot_NumOps[i]
						mod = objs[o].listOP_BaseStackPivot_Module[i]
						spe = objs[o].listOP_BaseStackPivot_Special[i]
					if Reg == "EAX":
						addy = objs[o].listOP_BaseStackPivotEAX[i]
						cnt = objs[o].listOP_BaseStackPivotEAX_CNT[i]
						num = objs[o].listOP_BaseStackPivotEAX_NumOps[i]
						mod = objs[o].listOP_BaseStackPivotEAX_Module[i]
						spe = objs[o].listOP_BaseStackPivotEAX_Special[i]
						
					if Reg == "EBX":
						addy = objs[o].listOP_BaseStackPivotEBX[i]
						cnt = objs[o].listOP_BaseStackPivotEBX_CNT[i]
						num = objs[o].listOP_BaseStackPivotEBX_NumOps[i]
						mod = objs[o].listOP_BaseStackPivotEBX_Module[i]
						spe = objs[o].listOP_BaseStackPivotEBX_Special[i]
					if Reg == "ECX":
						addy = objs[o].listOP_BaseStackPivotECX[i]
						cnt = objs[o].listOP_BaseStackPivotECX_CNT[i]
						num = objs[o].listOP_BaseStackPivotECX_NumOps[i]
						mod = objs[o].listOP_BaseStackPivotECX_Module[i]
						spe = objs[o].listOP_BaseStackPivotECX_Special[i]
					if Reg == "EDX":
						addy = objs[o].listOP_BaseStackPivotEDX[i]
						cnt = objs[o].listOP_BaseStackPivotEDX_CNT[i]
						num = objs[o].listOP_BaseStackPivotEDX_NumOps[i]
						mod = objs[o].listOP_BaseStackPivotEDX_Module[i]
						spe = objs[o].listOP_BaseStackPivotEDX_Special[i]
					if Reg == "ESI":
						addy = objs[o].listOP_BaseStackPivotESI[i]
						cnt = objs[o].listOP_BaseStackPivotESI_CNT[i]
						num = objs[o].listOP_BaseStackPivotESI_NumOps[i]
						mod = objs[o].listOP_BaseStackPivotESI_Module[i]
						spe = objs[o].listOP_BaseStackPivotESI_Special[i]
					if Reg == "EDI":
						addy = objs[o].listOP_BaseStackPivotEDI[i]
						cnt = objs[o].listOP_BaseStackPivotEDI_CNT[i]
						num = objs[o].listOP_BaseStackPivotEDI_NumOps[i]
						mod = objs[o].listOP_BaseStackPivotEDI_Module[i]
						spe = objs[o].listOP_BaseStackPivotEDI_Special[i]
					if Reg == "EBP":
						addy = objs[o].listOP_BaseStackPivotEBP[i]
						cnt = objs[o].listOP_BaseStackPivotEBP_CNT[i]
						num = objs[o].listOP_BaseStackPivotEBP_NumOps[i]
						mod = objs[o].listOP_BaseStackPivotEBP_Module[i]
						spe = objs[o].listOP_BaseStackPivotEBP_Special[i]
					if Reg == "ESP":
						addy = objs[o].listOP_BaseStackPivotESP[i]
						cnt = objs[o].listOP_BaseStackPivotESP_CNT[i]
						num = objs[o].listOP_BaseStackPivotESP_NumOps[i]
						mod = objs[o].listOP_BaseStackPivotESP_Module[i]
						spe = objs[o].listOP_BaseStackPivotESP_Special[i]
					out = "Ops: " + str(num) + "\tMod: " + str(mod)  + "\t"  + str(spe) + " bytes "
					spbytes =0
					SPSuccess=False
					SPSuccess, spgadget, spbytes= disHereCleanSP(addy, cnt, num, spe, Reg, mod) 
					spgadget= spgadget+ "\t" + str(mod)  

					if SPSuccess:
						out1.append(spgadget)
						out2.append(spbytes)
					if SPSuccess:
						counter()
						print >> f, Ct () + "\t" + out
						print >> f, spgadget

				if cnt1 > 0:
					temp.append(out)
				x=0
				out1, out2= sortBytes2(out1,out2)
				#sortBytesSPAll()
				print >> f, "\n\n\n\n"
				print >> f, Reg	
				first = False
				for each in out1:
					if not first:
						print >> f, str(out2[x]) + " bytes"
						first = True
					#if each != " ":
					nBytes = 0
					if nBytes != out2[x]:
							print >> f, str(out2[x]) + " bytes"
					nBytes = out2[x]
					print >> f,  "\t" + each + " - " + str(out2[x]) + " bytes" 
					x+=1
				first = False
				total = total + cnt1	
			o = o + 1
			clearGOuts()
		out = "\nJOP ROCKET" #out = ""#"# Grand total ADD "  + str(Reg) + " : " + str(total)
		print >> f, out
	o = 0
	nope(filename, total)

def printlistOP_SP3(NumOpsDis, Reg):
	global skipZero
	global o
	clearHashChecker()
	idval = 1
	while os.path.exists("%s-S_PIVOTS3-%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-S_PIVOTS3-" + str(idval) + ".txt"
	fname= filename

	with open(filename, 'a') as f:
		counterReset()
		i=0
		total = 0
		temp = []
		out1 = []
		out2 =[]
		for obj in objs:
			preRegs = ["EAX", "EBX", "ECX","EDX","EDI","ESI","EBP","ESP"]
			for Reg in preRegs:
				if Reg == "ALL":
					cnt1 = objs[o].SpOutGadgetAll.__len__()
				if Reg == "EAX":
					cnt1 = objs[o].SpOutGadgetEAX.__len__()
				if Reg == "EBX":
					cnt1 = objs[o].SpOutGadgetEBX.__len__()
				if Reg == "ECX":
					cnt1 = objs[o].SpOutGadgetECX.__len__()
				if Reg == "EDX":
					cnt1 = objs[o].SpOutGadgetEDX.__len__()
				if Reg == "ESI":
					cnt1 = objs[o].SpOutGadgetESI.__len__()
				if Reg == "EDI":
					cnt1 = objs[o].SpOutGadgetEDI.__len__()
				if Reg == "ESP":
					cnt1 = objs[o].SpOutGadgetESP.__len__()
				if Reg == "EBP":
					cnt1 = objs[o].SpOutGadgetEBP.__len__()
				for i in range (cnt1):
					addy =0
					cnt = 0   #
					num = 0
					if Reg == "ALL":
						spgadget = objs[o].SpOutGadgetAll[i]
						spbytes = objs[o].SpOutNumBytesAll[i]
					if Reg == "EAX":
						spgadget = objs[o].SpOutGadgetEAX[i]
						spbytes = objs[o].SpOutNumBytesEAX[i]
					if Reg == "EBX":
						spgadget = objs[o].SpOutGadgetEBX[i]
						spbytes = objs[o].SpOutNumBytesEBX[i]
					if Reg == "ECX":
						spgadget = objs[o].SpOutGadgetECX[i]
						spbytes = objs[o].SpOutNumBytesECX[i]
					if Reg == "EDX":
						spgadget = objs[o].SpOutGadgetEDX[i]
						spbytes = objs[o].SpOutNumBytesEDX[i]
					if Reg == "EDI":
						spgadget = objs[o].SpOutGadgetEDI[i]
						spbytes = objs[o].SpOutNumBytesEDI[i]
					if Reg == "ESI":
						spgadget = objs[o].SpOutGadgetESI[i]
						spbytes = objs[o].SpOutNumBytesESI[i]
					if Reg == "EBP":
						spgadget = objs[o].SpOutGadgetEBP[i]
						spbytes = objs[o].SpOutNumBytesEBP[i]
					if Reg == "ESP":
						spgadget = objs[o].SpOutGadgetESP[i]
						spbytes = objs[o].SpOutNumBytesESP[i]
					#out = "Ops: " + str(num) + "\tMod: " + str(mod)  + "\t"  + str(spe) + " bytes "
					#spbytes =0
					SPSuccess=True
					spgadget= spgadget #+ "\t" + str(mod)  
					if SPSuccess:
						out1.append(spgadget)
						out2.append(spbytes)
				x=0
				
				if cnt1 > 0:
						print >> f, Reg	
				first = False
				for each in out1:
					#global skipZero
					#if skipZero:
					skipZero=True
					skipMe = False
					if ((out2[x] ==0) and  skipZero):
						skipMe=True
					if not first:
						if not skipMe:
							print >> f, str(out2[x]) + " bytes"
							first = True
					#if each != " ":
					nBytes = 0
					if nBytes != out2[x]:
						if not skipMe:
							print >> f, str(out2[x]) + " bytes"
					nBytes = out2[x]
					if not skipMe:
							print >> f,   " \t" + each + " (" + str(out2[x]) + " bytes)" 
					x = x + 1
					
				#print >> f, out2
				first = False
				
				total = total + cnt1
				out1[:] = []	
				out2[:] = []	
			o = o + 1
	
		out = "\nJOP ROCKET" #out = ""#"# Grand total ADD "  + str(Reg) + " : " + str(total)
		print >> f, out

	o = 0
	nope(filename, total)


def getStackPivotAsLists(NumOpsDis, Reg):
	global skipZero
	global o
	clearHashChecker()
	i=0
	total = 0
	temp = []
	out1 = []
	out2 =[]
	for obj in objs:
		# preRegs = ["EAX", "EBX", "ECX","EDX","EDI","ESI","EBP","ESP"]
		# for Reg in preRegs:
		if Reg == "ALL":
			cnt1 = objs[o].SpOutGadgetAll.__len__()
		if Reg == "EAX":
			cnt1 = objs[o].SpOutGadgetEAX.__len__()
		if Reg == "EBX":
			cnt1 = objs[o].SpOutGadgetEBX.__len__()
		if Reg == "ECX":
			cnt1 = objs[o].SpOutGadgetECX.__len__()
		if Reg == "EDX":
			cnt1 = objs[o].SpOutGadgetEDX.__len__()
		if Reg == "ESI":
			cnt1 = objs[o].SpOutGadgetESI.__len__()
		if Reg == "EDI":
			cnt1 = objs[o].SpOutGadgetEDI.__len__()
		if Reg == "ESP":
			cnt1 = objs[o].SpOutGadgetESP.__len__()
		if Reg == "EBP":
			cnt1 = objs[o].SpOutGadgetEBP.__len__()
		# print Reg
		# print "cnt1 here " + str(cnt1)
		for i in range (cnt1):
			addy =0
			cnt = 0   #
			num = 0
			if Reg == "ALL":
				spgadget = objs[o].SpOutGadgetAll[i]
				spbytes = objs[o].SpOutNumBytesAll[i]
			if Reg == "EAX":
				spgadget = objs[o].SpOutGadgetEAX[i]
				spbytes = objs[o].SpOutNumBytesEAX[i]
			if Reg == "EBX":
				spgadget = objs[o].SpOutGadgetEBX[i]
				spbytes = objs[o].SpOutNumBytesEBX[i]
			if Reg == "ECX":
				spgadget = objs[o].SpOutGadgetECX[i]
				spbytes = objs[o].SpOutNumBytesECX[i]
			if Reg == "EDX":
				spgadget = objs[o].SpOutGadgetEDX[i]
				spbytes = objs[o].SpOutNumBytesEDX[i]
			if Reg == "EDI":
				spgadget = objs[o].SpOutGadgetEDI[i]
				spbytes = objs[o].SpOutNumBytesEDI[i]
			if Reg == "ESI":
				spgadget = objs[o].SpOutGadgetESI[i]
				spbytes = objs[o].SpOutNumBytesESI[i]
			if Reg == "EBP":
				spgadget = objs[o].SpOutGadgetEBP[i]
				spbytes = objs[o].SpOutNumBytesEBP[i]
			if Reg == "ESP":
				spgadget = objs[o].SpOutGadgetESP[i]
				spbytes = objs[o].SpOutNumBytesESP[i]
			#out = "Ops: " + str(num) + "\tMod: " + str(mod)  + "\t"  + str(spe) + " bytes "
			#spbytes =0
			SPSuccess=True
			spgadget= spgadget #+ "\t" + str(mod)  
			if SPSuccess:
				out1.append(spgadget)
				out2.append(spbytes)
			# x=0
			# if cnt1 > 0:
			# 		print Reg	
			# first = False
			# for each in out1:
			# 	skipZero=True
			# 	skipMe = False
			# 	if ((out2[x] ==0) and  skipZero):
			# 		skipMe=True
			# 	if not first:
			# 		if not skipMe:
			# 			print  str(out2[x]) + " bytes"
			# 			first = True
			# 	#if each != " ":
			# 	nBytes = 0
			# 	if nBytes != out2[x]:
			# 		if not skipMe:
			# 			print  str(out2[x]) + " bytes"
			# 	nBytes = out2[x]
			# 	if not skipMe:
			# 			print  " \t" + each + " (" + str(out2[x]) + " bytes)" 
			# 	x = x + 1
			first = False
			total = total + cnt1
			# out1[:] = []	
			# out2[:] = []	
		o = o + 1
		# for o in out1:
		# 	print o
	o = 0
	return out1, out2

def preprocessOP_SP(NumOpsDis, Reg2):
	global o
	clearHashChecker()
	i=0
	total = 0
	temp = []
	out1 = []
	out2 =[]
	for obj in objs:
		preRegs = ["EAX", "EBX", "ECX","EDX","EDI","ESI","EBP","ESP","ALL"]

		for Reg in preRegs:

			if Reg == "ALL":
				cnt1 = objs[o].listOP_BaseStackPivot.__len__()
			if Reg == "EAX":
				cnt1 = objs[o].listOP_BaseStackPivotEAX.__len__()
			if Reg == "EBX":
				cnt1 = objs[o].listOP_BaseStackPivotEBX.__len__()
			if Reg == "ECX":
				cnt1 = objs[o].listOP_BaseStackPivotECX.__len__()
			if Reg == "EDX":
				cnt1 = objs[o].listOP_BaseStackPivotEDX.__len__()
			if Reg == "ESI":
				cnt1 = objs[o].listOP_BaseStackPivotESI.__len__()
			if Reg == "EDI":
				cnt1 = objs[o].listOP_BaseStackPivotEDI.__len__()
			if Reg == "ESP":
				cnt1 = objs[o].listOP_BaseStackPivotESP.__len__()
			if Reg == "EBP":
				cnt1 = objs[o].listOP_BaseStackPivotEBP.__len__()
			for i in range (cnt1):
				addy =0
				cnt = 0   #
				num = 0
				if Reg == "ALL":
					addy = objs[o].listOP_BaseStackPivot[i]
					cnt = objs[o].listOP_BaseStackPivot_CNT[i]
					num = objs[o].listOP_BaseStackPivot_NumOps[i]
					mod = objs[o].listOP_BaseStackPivot_Module[i]
					spe = objs[o].listOP_BaseStackPivot_Special[i]
				if Reg == "EAX":
					addy = objs[o].listOP_BaseStackPivotEAX[i]
					cnt = objs[o].listOP_BaseStackPivotEAX_CNT[i]
					num = objs[o].listOP_BaseStackPivotEAX_NumOps[i]
					mod = objs[o].listOP_BaseStackPivotEAX_Module[i]
					spe = objs[o].listOP_BaseStackPivotEAX_Special[i]
				if Reg == "EBX":
					addy = objs[o].listOP_BaseStackPivotEBX[i]
					cnt = objs[o].listOP_BaseStackPivotEBX_CNT[i]
					num = objs[o].listOP_BaseStackPivotEBX_NumOps[i]
					mod = objs[o].listOP_BaseStackPivotEBX_Module[i]
					spe = objs[o].listOP_BaseStackPivotEBX_Special[i]
				if Reg == "ECX":
					addy = objs[o].listOP_BaseStackPivotECX[i]
					cnt = objs[o].listOP_BaseStackPivotECX_CNT[i]
					num = objs[o].listOP_BaseStackPivotECX_NumOps[i]
					mod = objs[o].listOP_BaseStackPivotECX_Module[i]
					spe = objs[o].listOP_BaseStackPivotECX_Special[i]
				if Reg == "EDX":
					addy = objs[o].listOP_BaseStackPivotEDX[i]
					cnt = objs[o].listOP_BaseStackPivotEDX_CNT[i]
					num = objs[o].listOP_BaseStackPivotEDX_NumOps[i]
					mod = objs[o].listOP_BaseStackPivotEDX_Module[i]
					spe = objs[o].listOP_BaseStackPivotEDX_Special[i]
				if Reg == "ESI":
					addy = objs[o].listOP_BaseStackPivotESI[i]
					cnt = objs[o].listOP_BaseStackPivotESI_CNT[i]
					num = objs[o].listOP_BaseStackPivotESI_NumOps[i]
					mod = objs[o].listOP_BaseStackPivotESI_Module[i]
					spe = objs[o].listOP_BaseStackPivotESI_Special[i]
				if Reg == "EDI":
					addy = objs[o].listOP_BaseStackPivotEDI[i]
					cnt = objs[o].listOP_BaseStackPivotEDI_CNT[i]
					num = objs[o].listOP_BaseStackPivotEDI_NumOps[i]
					mod = objs[o].listOP_BaseStackPivotEDI_Module[i]
					spe = objs[o].listOP_BaseStackPivotEDI_Special[i]
				if Reg == "EBP":
					addy = objs[o].listOP_BaseStackPivotEBP[i]
					cnt = objs[o].listOP_BaseStackPivotEBP_CNT[i]
					num = objs[o].listOP_BaseStackPivotEBP_NumOps[i]
					mod = objs[o].listOP_BaseStackPivotEBP_Module[i]
					spe = objs[o].listOP_BaseStackPivotEBP_Special[i]
				if Reg == "ESP":
					addy = objs[o].listOP_BaseStackPivotESP[i]
					cnt = objs[o].listOP_BaseStackPivotESP_CNT[i]
					num = objs[o].listOP_BaseStackPivotESP_NumOps[i]
					mod = objs[o].listOP_BaseStackPivotESP_Module[i]
					spe = objs[o].listOP_BaseStackPivotESP_Special[i]
				spbytes =0
				SPSuccess=False
				SPSuccess, spgadget, spbytes= disHereCleanSP2(addy, cnt, num, spe, Reg, mod) 
			clearGOuts()
				# print "reg2: " + Reg + " " + spgadget


		sortBytesSPAll()
#		print objs[o].SpOutGadgetEAX
		
#		print "checking preprocessing"
#		sp()
#		test=raw_input()
		o = o + 1
	o = 0


def preprocessOP_DG(NumOpsDis, Reg):
	Reg = Reg.upper()
	global o
	clearHashChecker()
	i=0
	results =[]
	specials=[]
	for obj in objs:
		# print "Regg " + Reg
		cnt1=0
		if Reg == "EAX":
			cnt1 = objs[o].listOP_BaseDG_EAX.__len__()
		if Reg == "EBX":
			cnt1 = objs[o].listOP_BaseDG_EBX.__len__()
		if Reg == "ECX":
			cnt1 = objs[o].listOP_BaseDG_ECX.__len__()
		if Reg == "EDX":
			cnt1 = objs[o].listOP_BaseDG_EDX.__len__()
		if Reg == "ESI":
			cnt1 = objs[o].listOP_BaseDG_ESI.__len__()
		if Reg == "EDI":
			cnt1 = objs[o].listOP_BaseDG_EDI.__len__()
		if Reg == "ESP":
			cnt1 = objs[o].listOP_BaseDG_ESP.__len__()
		if Reg == "EBP":
			cnt1 = objs[o].listOP_BaseDG_EBP.__len__()
		for i in range (cnt1):
			addy =0
			cnt = 0   #
			num = 0
			mod=""
			if Reg == "EAX":
				addy = objs[o].listOP_BaseDG_EAX[i]
				cnt = objs[o].listOP_BaseDG_CNT_EAX[i]
				num =objs[o].listOP_BaseDG_NumOps_EAX[i]
				mod = objs[o].listOP_BaseDG_Module_EAX[i]
			if Reg == "EBX":
				addy = objs[o].listOP_BaseDG_EBX[i]
				cnt = objs[o].listOP_BaseDG_CNT_EBX[i]
				num =objs[o].listOP_BaseDG_NumOps_EBX[i]
				mod = objs[o].listOP_BaseDG_Module_EBX[i]
			if Reg == "ECX":
				addy = objs[o].listOP_BaseDG_ECX[i]
				cnt = objs[o].listOP_BaseDG_CNT_ECX[i]
				num =objs[o].listOP_BaseDG_NumOps_ECX[i]
				mod = objs[o].listOP_BaseDG_Module_ECX[i]
			if Reg == "EDX":
				addy = objs[o].listOP_BaseDG_EDX[i]
				cnt = objs[o].listOP_BaseDG_CNT_EDX[i]
				num =objs[o].listOP_BaseDG_NumOps_EDX[i]
				mod = objs[o].listOP_BaseDG_Module_EDX[i]
			if Reg == "EDI":
				addy = objs[o].listOP_BaseDG_EDI[i]
				cnt = objs[o].listOP_BaseDG_CNT_EDI[i]
				num =objs[o].listOP_BaseDG_NumOps_EDI[i]
				mod = objs[o].listOP_BaseDG_Module_EDI[i]
			if Reg == "ESI":
				addy = objs[o].listOP_BaseDG_ESI[i]
				cnt = objs[o].listOP_BaseDG_CNT_ESI[i]
				num =objs[o].listOP_BaseDG_NumOps_ESI[i]
				mod = objs[o].listOP_BaseDG_Module_ESI[i]
			if Reg == "EBP":
				addy = objs[o].listOP_BaseDG_EBP[i]
				cnt = objs[o].listOP_BaseDG_CNT_EBP[i]
				num =objs[o].listOP_BaseDG_NumOps_EBP[i]
				mod = objs[o].listOP_BaseDG_Module_EBP[i]
			if Reg == "ESP":
				addy = objs[o].listOP_BaseDG_ESP[i]
				cnt = objs[o].listOP_BaseDG_CNT_ESP[i]
				num =objs[o].listOP_BaseDG_NumOps_ESP[i]
				mod = objs[o].listOP_BaseDG_Module_ESP[i]
			if cnt == 0:
				return False, "",0
			spbytes =0
			SPSuccess=False
			#mjmp
			spgadget2, special= disHereCleanNewDG(addy, cnt, num, mod) 
			# spgadget2+= " " + mod
			results.append(spgadget2)
			specials.append(special)
		o = o + 1
	o = 0
	try:
		output1 = ""
		output1=results[0]
		return True,output1, specials[0]
	except:
		return False,"",0

def preprocessOP_Popold(NumOpsDis, popReg, jmpReg,best, mode):
	global o
	clearHashChecker()
	i=0    
	total = 0
	temp = []
	out1 = []
	out2 =[]
	# print "preproce " + popReg
	for obj in objs:
		# preRegs = ["EAX", "EBX", "ECX","EDX","EDI","ESI","EBP","ESP","ALL"]
		preRegs = ["ALL"]

		for Reg in preRegs:

			if Reg == "ALL":
				cnt1 = objs[o].listOP_BasePop.__len__()
			for i in range (cnt1):
				addy =0
				cnt = 0   #
				num = 0
				### probably needs to just be all by default for how it is set up????
				if Reg == "ALL":
					addy = objs[o].listOP_BasePop[i]
					cnt = objs[o].listOP_BasePop_CNT[i]
					num = objs[o].listOP_BasePop_NumOps[i]
					mod = objs[o].listOP_BasePop_Module[i]
				spbytes =0
				SPSuccess=False
				if mode=="best":
					# print "i am checking " + jmpReg + popReg



											# preprocessOP_Pop(NumOpsD, popReg, Reg, best, "best")
					SPSuccess2, spgadget2, spbytes2= disHereCleanPop2Best(addy, cnt, num, popReg, jmpReg,best, mod) 
					if SPSuccess2==True:
						# print "jfound gadget-best:"
						sp()
						# print spgadget2
				if mode=="ok":
					# print "trying to find"
					SPSuccess, spgadget, spbytes= disHereCleanPop2(addy, cnt, num, popReg, jmpReg, mod) 
					if SPSuccess==True:
						# print "jfound gadget:"
						sp()
						# print spgadget
				
		o = o + 1
	o = 0
	#debug
	# print objs[0].specialPOPGadget
	# print objs[0].specialPOPBytes

	# print "Best1"
	# print objs[0].specialPOPGadgetBest
	# print objs[0].specialPOPBytesBest

#mag2

#now7
	# preprocessOP_PopRet(NumOpsD, best, cMode, Reg)

def preprocessOP_Pop(NumOpsDis, popReg, jmpReg,best, mode):
	global o
	clearHashChecker()
	i=0    
	total = 0
	temp = []
	out1 = []
	out2 =[]
	# print "preproce " + popReg
	for obj in objs:
		Reg=popReg.upper()
		if Reg == "ALL":
			cnt1 = objs[o].listOP_BasePop.__len__()

		if Reg == "EAX":
			cnt1 = objs[o].listOP_BasePopEAX.__len__()
		if Reg == "EBX":
			cnt1 = objs[o].listOP_BasePopEBX.__len__()
		if Reg == "ECX":
			cnt1 = objs[o].listOP_BasePopECX.__len__()
		if Reg == "EDX":
			cnt1 = objs[o].listOP_BasePopEDX.__len__()
		if Reg == "ESI":
			cnt1 = objs[o].listOP_BasePopESI.__len__()
		if Reg == "EDI":
			cnt1 = objs[o].listOP_BasePopEDI.__len__()
		if Reg == "ESP":
			cnt1 = objs[o].listOP_BasePopESP.__len__()
		if Reg == "EBP":
			cnt1 = objs[o].listOP_BasePopEBP.__len__()
		for i in range (cnt1):
			#print "\n@POP: ^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^\n"
			#print >> f, "@POP: ^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"

			mod=""
			addy =0
			cnt = 0   #
			num = 0
			if Reg == "ALL":
				addy = objs[o].listOP_BasePop[i]
				cnt = objs[o].listOP_BasePop_CNT[i]
				num = objs[o].listOP_BasePop_NumOps[i]
				mod = objs[o].listOP_BasePop_Module[i]
			if Reg == "EAX":
				addy = objs[o].listOP_BasePopEAX[i]
				cnt = objs[o].listOP_BasePopEAX_CNT[i]
				num = objs[o].listOP_BasePopEAX_NumOps[i]
				mod = objs[o].listOP_BasePopEAX_Module[i]
			if Reg == "EBX":
				addy = objs[o].listOP_BasePopEBX[i]
				cnt = objs[o].listOP_BasePopEBX_CNT[i]
				num = objs[o].listOP_BasePopEBX_NumOps[i]
				mod = objs[o].listOP_BasePopEBX_Module[i]
			if Reg == "ECX":
				addy = objs[o].listOP_BasePopECX[i]
				cnt = objs[o].listOP_BasePopECX_CNT[i]
				num = objs[o].listOP_BasePopECX_NumOps[i]
				mod = objs[o].listOP_BasePopECX_Module[i]
			if Reg == "EDX":
				addy = objs[o].listOP_BasePopEDX[i]
				cnt = objs[o].listOP_BasePopEDX_CNT[i]
				num = objs[o].listOP_BasePopEDX_NumOps[i]
				mod = objs[o].listOP_BasePopEDX_Module[i]
			if Reg == "ESI":
				addy = objs[o].listOP_BasePopESI[i]
				cnt = objs[o].listOP_BasePopESI_CNT[i]
				num = objs[o].listOP_BasePopESI_NumOps[i]
				mod = objs[o].listOP_BasePopESI_Module[i]
			if Reg == "EDI":
				addy = objs[o].listOP_BasePopEDI[i]
				cnt = objs[o].listOP_BasePopEDI_CNT[i]
				num = objs[o].listOP_BasePopEDI_NumOps[i]
				mod = objs[o].listOP_BasePopEDI_Module[i]
			if Reg == "EBP":
				addy = objs[o].listOP_BasePopEBP[i]
				cnt = objs[o].listOP_BasePopEBP_CNT[i]
				num = objs[o].listOP_BasePopEBP_NumOps[i]
				mod = objs[o].listOP_BasePopEBP_Module[i]
			if Reg == "ESP":
				addy = objs[o].listOP_BasePopESP[i]
				cnt = objs[o].listOP_BasePopESP_CNT[i]
				num = objs[o].listOP_BasePopESP_NumOps[i]
				mod = objs[o].listOP_BasePopESP_Module[i]

										# preprocessOP_Pop(NumOpsD, popReg, Reg, best, "best")
				SPSuccess2, spgadget2, spbytes2= disHereCleanPop2Best(addy, cnt, num, popReg, jmpReg,best,mod) 
				if SPSuccess2==True:
					# print "jfound gadget-best:"
					sp()
					# print spgadget2
			if mode=="ok":
				# print "trying to find"
				SPSuccess, spgadget, spbytes= disHereCleanPop2(addy, cnt, num, popReg, jmpReg,mod) 
				if SPSuccess==True:
					# print "jfound gadget:"
					sp()
					# print spgadget
				
		o = o + 1
	o = 0


def preprocessOP_PopRet(NumOpsDis,best, mode):
	# print "this is my mode: " +  mode
	global o
	clearHashChecker()
	i=0    
	total = 0
	temp = []
	out1 = []
	out2 =[]
	# print "preproce " + popReg
	for obj in objs:
		preRegs =["EAX", "EBX", "ECX","EDX","EDI","ESI","EBP","ESP"]
		# preRegs = ["EBX"]

		for Reg in preRegs:

			if Reg == "ALL":
				cnt1 = objs[o].listOP_RET_Pop.__len__()
			if Reg == "EAX":
				cnt1 = objs[o].listOP_RET_Pop_EAX.__len__()
			if Reg == "EBX":
				cnt1 = objs[o].listOP_RET_Pop_EBX.__len__()				
			if Reg == "ECX":
				cnt1 = objs[o].listOP_RET_Pop_ECX.__len__()
			if Reg == "EDX":
				cnt1 = objs[o].listOP_RET_Pop_EDX.__len__()				
			if Reg == "EDI":
				cnt1 = objs[o].listOP_RET_Pop_EDI.__len__()
			if Reg == "ESI":
				cnt1 = objs[o].listOP_RET_Pop_ESI.__len__()				
			if Reg == "ESP":
				cnt1 = objs[o].listOP_RET_Pop_ESP.__len__()
			if Reg == "EBP":
				cnt1 = objs[o].listOP_RET_Pop_EBP.__len__()				
				
			for i in range (cnt1):
				addy =0
				cnt = 0   #
				num = 0
				### probably needs to just be all by default for how it is set up????
				if Reg == "ALL":
					addy = objs[o].listOP_RET_Pop[i]
					cnt = objs[o].listOP_RET_Pop_CNT[i]
					num = objs[o].listOP_RET_Pop_NumOps[i]
					mod = objs[o].listOP_RET_Pop_Module[i]
				if Reg == "EAX":
					addy = objs[o].listOP_RET_Pop_EAX[i]
					cnt = objs[o].listOP_RET_Pop_EAX_CNT[i]
					num = objs[o].listOP_RET_Pop_EAX_NumOps[i]
					mod = objs[o].listOP_RET_Pop_EAX_Module[i]
				if Reg == "EBX":
					addy = objs[o].listOP_RET_Pop_EBX[i]
					cnt = objs[o].listOP_RET_Pop_EBX_CNT[i]
					num = objs[o].listOP_RET_Pop_EBX_NumOps[i]
					mod = objs[o].listOP_RET_Pop_EBX_Module[i]
				if Reg == "ECX":
					addy = objs[o].listOP_RET_Pop_ECX[i]
					cnt = objs[o].listOP_RET_Pop_ECX_CNT[i]
					num = objs[o].listOP_RET_Pop_ECX_NumOps[i]
					mod = objs[o].listOP_RET_Pop_ECX_Module[i]
				if Reg == "EDX":
					addy = objs[o].listOP_RET_Pop_EDX[i]
					cnt = objs[o].listOP_RET_Pop_EDX_CNT[i]
					num = objs[o].listOP_RET_Pop_EDX_NumOps[i]
					mod = objs[o].listOP_RET_Pop_EDX_Module[i]
				if Reg == "EDI":
					addy = objs[o].listOP_RET_Pop_EDI[i]
					cnt = objs[o].listOP_RET_Pop_EDI_CNT[i]
					num = objs[o].listOP_RET_Pop_EDI_NumOps[i]
					mod = objs[o].listOP_RET_Pop_EDI_Module[i]
				if Reg == "ESI":
					addy = objs[o].listOP_RET_Pop_ESI[i]
					cnt = objs[o].listOP_RET_Pop_ESI_CNT[i]
					num = objs[o].listOP_RET_Pop_ESI_NumOps[i]
					mod = objs[o].listOP_RET_Pop_ESI_Module[i]
				if Reg == "ESP":
					addy = objs[o].listOP_RET_Pop_ESP[i]
					cnt = objs[o].listOP_RET_Pop_ESP_CNT[i]
					num = objs[o].listOP_RET_Pop_ESP_NumOps[i]
					mod = objs[o].listOP_RET_Pop_ESP_Module[i]
				if Reg == "EBP":
					addy = objs[o].listOP_RET_Pop_EBP[i]
					cnt = objs[o].listOP_RET_Pop_EBP_CNT[i]
					num = objs[o].listOP_RET_Pop_EBP_NumOps[i]
					mod = objs[o].listOP_RET_Pop_EBP_Module[i]
				spbytes =0
				SPSuccess=False
				clearGOuts()
				if mode=="best":
					SPSuccess2, spgadget2, spbytes2= disHereCleanPopRet2Best(addy, cnt, num, mod, Reg) 
					if SPSuccess2==True:
						# print "found gadget-best:"
						sp()
						# print spgadget2
				clearGOuts()						
				if mode=="ok":
					# print "g1: addy: " + str(addy) + " lines: " + str(cnt)
					SPSuccess, spgadget, spbytes= disHereCleanPopRet2(addy, cnt, num, mod, Reg) 
					if SPSuccess==True:
						# print "Popfound gadget:"
						sp()
						# print spgadget
				
		o = o + 1
	o = 0

#now3
def calcRegforDispatcher(Reg):
	if Reg == "EAX":
		t2, g2, b2=returnPopEAX()
	if Reg == "EBX":
		t2, g2, b2=returnPopEBX()
	if Reg == "ECX":
		t2, g2, b2=returnPopECX()
	if Reg == "EDX":
		t2, g2, b2=returnPopEDX()
	if Reg == "EDI":
		t2, g2, b2=returnPopEDI()
	if Reg == "ESI":
		t2, g2, b2=returnPopESI()
	if Reg == "EBP":
		t2, g2, b2=returnPopEBP()
	if Reg == "ESP":
		t2, g2, b2=returnPopESP()
	return g2, b2

def calcRegforDispatchTable(Reg):
	IA86 =["EAX", "EBX", "ECX", "EDX", "EDI", "ESI", "EDI", "EBP", "ESP"]
	IA86 =["EAX",  "EDX", "EDI", "ESI", "EDI", "EBP", "ESP"]

	currentRegs=[]

	z=0
	for x in IA86:
		if IA86[z] != Reg:
			currentRegs.append(IA86[z])
		z+=1
	x=0			# FIND  *FIRST* ONE THAT IS NOT DESIRED REG!
	while (x<8):
		try:
			Reg = currentRegs[x]
		except:
			Reg=""
		if Reg == "EAX ":
			t2, g2, b2=returnPopEAX()
			if t2:
				break
		if Reg == "EBX ":
			t2, g2, b2=returnPopEBX()
			if t2:
				break
		if Reg == "ECX ":
			t2, g2, b2=returnPopECX()
			if t2:
				break
		if Reg == "EDX":
			t2, g2, b2=returnPopEDX()
			if t2:
				break
		if Reg == "EDI":
			t2, g2, b2=returnPopEDI()
			if t2:
				break
		if Reg == "ESI":
			t2, g2, b2=returnPopESI()
			if t2:
				break
		if Reg == "EBP":
			t2, g2, b2=returnPopEBP()
			if t2:
				break
		if Reg == "ESP":
			t2, g2, b2=returnPopESP()
			if t2:
				break
		x+=1
	return g2, b2, Reg
def returnPopEAX():
	length = len(objs[o].specialPOPGadgetRetBestEAX) -1
	try:
		for x in objs[o].specialPOPGadgetRetBestEAX:
			gadget=x
		for x in objs[o].specialPOPBytesRetBestEAX:
			bytesPop=x
			if (countLines(gadget) <3):
				return True, gadget, bytesPop
		i=0				
		for x in objs[o].specialPOPGadgetRetBestEAX:
			i+=1
			if (countLines(objs[o].specialPOPGadgetRetBestEAX[i]) < 3):
				gadget2 = objs[o].specialPOPGadgetRetBestEAX[i]
				bytesPop2 = objs[o].specialPOPBytesRetBestEAX[i]
				return True, gadget2, bytesPop2
		i=0				
		for x in objs[o].specialPOPGadgetRetBestEAX:
			i+=1
			if (countLines(objs[o].specialPOPGadgetRetBestEAX[i]) < 4):
				gadget2 = objs[o].specialPOPGadgetRetBestEAX[i]
				bytesPop2 = objs[o].specialPOPBytesRetBestEAX[i]
				return True, gadget2, bytesPop2
			if i == length:
				return True, gadget, bytesPop			
		return True, gadget, bytesPop
	except:
		try:
			for x in objs[o].specialPOPGadgetRetEAX:
				gadget=x
			for x in objs[o].specialPOPBytesRetEAX:
				bytesPop=x
			return True, gadget, bytesPop
		except:
			# print "# No gadget found."
			return False, "",0


def returnPopEBX():
	length = len(objs[o].specialPOPGadgetRetBestEBX) -1
	try:
		for x in objs[o].specialPOPGadgetRetBestEBX:
			gadget=x
		for x in objs[o].specialPOPBytesRetBestEBX:
			bytesPop=x
			if (countLines(gadget) <3):
				return True, gadget, bytesPop
		i=0				
		for x in objs[o].specialPOPGadgetRetBestEBX:
			i+=1
			if (countLines(objs[o].specialPOPGadgetRetBestEBX[i]) < 3):
				gadget2 = objs[o].specialPOPGadgetRetBestEBX[i]
				bytesPop2 = objs[o].specialPOPBytesRetBestEBX[i]
				return True, gadget2, bytesPop2
		i=0				
		for x in objs[o].specialPOPGadgetRetBestEBX:
			i+=1
			if (countLines(objs[o].specialPOPGadgetRetBestEBX[i]) < 4):
				gadget2 = objs[o].specialPOPGadgetRetBestEBX[i]
				bytesPop2 = objs[o].specialPOPBytesRetBestEBX[i]
				return True, gadget2, bytesPop2
			if i == length:
				return True, gadget, bytesPop			
		return True, gadget, bytesPop
	except:
		try:
			for x in objs[o].specialPOPGadgetRetEBX:
				gadget=x
			for x in objs[o].specialPOPBytesRetEBX:
				bytesPop=x
			return True, gadget, bytesPop
		except:
			# print "# No gadget found"
			return False, "",0

def returnPopECX():
	length = len(objs[o].specialPOPGadgetRetBestECX) -1
	try:
		for x in objs[o].specialPOPGadgetRetBestECX:
			gadget=x
		for x in objs[o].specialPOPBytesRetBestECX:
			bytesPop=x
			if (countLines(gadget) <3):
				return True, gadget, bytesPop
		i=0				
		for x in objs[o].specialPOPGadgetRetBestECX:
			i+=1
			if (countLines(objs[o].specialPOPGadgetRetBestECX[i]) < 3):
				gadget2 = objs[o].specialPOPGadgetRetBestECX[i]
				bytesPop2 = objs[o].specialPOPBytesRetBestECX[i]
				return True, gadget2, bytesPop2
		i=0				
		for x in objs[o].specialPOPGadgetRetBestECX:
			i+=1
			if (countLines(objs[o].specialPOPGadgetRetBestECX[i]) < 4):
				gadget2 = objs[o].specialPOPGadgetRetBestECX[i]
				bytesPop2 = objs[o].specialPOPBytesRetBestECX[i]
				return True, gadget2, bytesPop2
			if i == length:
				return True, gadget, bytesPop			
		return True, gadget, bytesPop
	except:
		try:
			for x in objs[o].specialPOPGadgetRetECX:
				gadget=x
			for x in objs[o].specialPOPBytesRetECX:
				bytesPop=x
			return True, gadget, bytesPop
		except:
			# print "# No gadget found."
			return False, "",0


def returnPopEDX():
	length = len(objs[o].specialPOPGadgetRetBestEDX) -1
	try:
		for x in objs[o].specialPOPGadgetRetBestEDX:
			gadget=x
		for x in objs[o].specialPOPBytesRetBestEDX:
			bytesPop=x
			if (countLines(gadget) <3):
				return True, gadget, bytesPop
		i=0				
		for x in objs[o].specialPOPGadgetRetBestEDX:
			i+=1
			if (countLines(objs[o].specialPOPGadgetRetBestEDX[i]) < 3):
				gadget2 = objs[o].specialPOPGadgetRetBestEDX[i]
				bytesPop2 = objs[o].specialPOPBytesRetBestEDX[i]
				return True, gadget2, bytesPop2
		i=0				
		for x in objs[o].specialPOPGadgetRetBestEDX:
			i+=1
			if (countLines(objs[o].specialPOPGadgetRetBestEDX[i]) < 4):
				gadget2 = objs[o].specialPOPGadgetRetBestEDX[i]
				bytesPop2 = objs[o].specialPOPBytesRetBestEDX[i]
				return True, gadget2, bytesPop2
			if i == length:
				return True, gadget, bytesPop			
		return True, gadget, bytesPop
	except:
		try:
			for x in objs[o].specialPOPGadgetRetEDX:
				gadget=x
			for x in objs[o].specialPOPBytesRetEDX:
				bytesPop=x
			return True, gadget, bytesPop
		except:
			# print "# No gadget found."
			return False, "",0

def returnPopEDI():
	length = len(objs[o].specialPOPGadgetRetBestEDI) -1
	try:
		for x in objs[o].specialPOPGadgetRetBestEDI:
			gadget=x
		for x in objs[o].specialPOPBytesRetBestEDI:
			bytesPop=x
			if (countLines(gadget) <3):
				return True, gadget, bytesPop
		i=0				
		for x in objs[o].specialPOPGadgetRetBestEDI:
			i+=1
			if (countLines(objs[o].specialPOPGadgetRetBestEDI[i]) < 3):
				gadget2 = objs[o].specialPOPGadgetRetBestEDI[i]
				bytesPop2 = objs[o].specialPOPBytesRetBestEDI[i]
				return True, gadget2, bytesPop2
		i=0				
		for x in objs[o].specialPOPGadgetRetBestEDI:
			i+=1
			if (countLines(objs[o].specialPOPGadgetRetBestEDI[i]) < 4):
				gadget2 = objs[o].specialPOPGadgetRetBestEDI[i]
				bytesPop2 = objs[o].specialPOPBytesRetBestEDI[i]
				return True, gadget2, bytesPop2
			if i == length:
				return True, gadget, bytesPop			
		return True, gadget, bytesPop
	except:
		try:
			for x in objs[o].specialPOPGadgetRetEDI:
				gadget=x
			for x in objs[o].specialPOPBytesRetEDI:
				bytesPop=x
			return True, gadget, bytesPop
		except:
			# print "# No gadget found."
			return False, "",0

def returnPopESI():
	length = len(objs[o].specialPOPGadgetRetBestESI) -1
	try:
		for x in objs[o].specialPOPGadgetRetBestESI:
			gadget=x
		for x in objs[o].specialPOPBytesRetBestESI:
			bytesPop=x
			if (countLines(gadget) <3):
				return True, gadget, bytesPop
		i=0				
		for x in objs[o].specialPOPGadgetRetBestESI:
			i+=1
			if (countLines(objs[o].specialPOPGadgetRetBestESI[i]) < 3):
				gadget2 = objs[o].specialPOPGadgetRetBestESI[i]
				bytesPop2 = objs[o].specialPOPBytesRetBestESI[i]
				return True, gadget2, bytesPop2
		i=0				
		for x in objs[o].specialPOPGadgetRetBestESI:
			i+=1
			if (countLines(objs[o].specialPOPGadgetRetBestESI[i]) < 4):
				gadget2 = objs[o].specialPOPGadgetRetBestESI[i]
				bytesPop2 = objs[o].specialPOPBytesRetBestESI[i]
				return True, gadget2, bytesPop2
			if i == length:
				return True, gadget, bytesPop			
		return True, gadget, bytesPop
	except:
		try:
			for x in objs[o].specialPOPGadgetRetESI:
				gadget=x
			for x in objs[o].specialPOPBytesRetESI:
				bytesPop=x
			return True, gadget, bytesPop
		except:
			# print "# No gadget found."
			return False, "",0

def returnPopEBP():
	length = len(objs[o].specialPOPGadgetRetBestEBP) -1
	try:
		for x in objs[o].specialPOPGadgetRetBestEBP:
			gadget=x
		for x in objs[o].specialPOPBytesRetBestEBP:
			bytesPop=x
			if (countLines(gadget) <3):
				return True, gadget, bytesPop
		i=0				
		for x in objs[o].specialPOPGadgetRetBestEBP:
			i+=1
			if (countLines(objs[o].specialPOPGadgetRetBestEBP[i]) < 3):
				gadget2 = objs[o].specialPOPGadgetRetBestEBP[i]
				bytesPop2 = objs[o].specialPOPBytesRetBestEBP[i]
				return True, gadget2, bytesPop2
		i=0				
		for x in objs[o].specialPOPGadgetRetBestEBP:
			i+=1
			if (countLines(objs[o].specialPOPGadgetRetBestEBP[i]) < 4):
				gadget2 = objs[o].specialPOPGadgetRetBestEBP[i]
				bytesPop2 = objs[o].specialPOPBytesRetBestEBP[i]
				return True, gadget2, bytesPop2
			if i == length:
				return True, gadget, bytesPop			
		return True, gadget, bytesPop
	except:
		try:
			for x in objs[o].specialPOPGadgetRetEBP:
				gadget=x
			for x in objs[o].specialPOPBytesRetEBP:
				bytesPop=x
			return True, gadget, bytesPop
		except:
			# print "# No gadget found."
			return False, "",0


def returnPopESP():
	length = len(objs[o].specialPOPGadgetRetBestESP) -1
	try:
		for x in objs[o].specialPOPGadgetRetBestESP:
			gadget=x
		for x in objs[o].specialPOPBytesRetBestESP:
			bytesPop=x
			if (countLines(gadget) <3):
				return True, gadget, bytesPop
		i=0				
		for x in objs[o].specialPOPGadgetRetBestESP:
			i+=1
			if (countLines(objs[o].specialPOPGadgetRetBestESP[i]) < 3):
				gadget2 = objs[o].specialPOPGadgetRetBestESP[i]
				bytesPop2 = objs[o].specialPOPBytesRetBestESP[i]
				return True, gadget2, bytesPop2
		i=0				
		for x in objs[o].specialPOPGadgetRetBestESP:
			i+=1
			if (countLines(objs[o].specialPOPGadgetRetBestESP[i]) < 4):
				gadget2 = objs[o].specialPOPGadgetRetBestESP[i]
				bytesPop2 = objs[o].specialPOPBytesRetBestESP[i]
				return True, gadget2, bytesPop2
			if i == length:
				return True, gadget, bytesPop			
		return True, gadget, bytesPop
	except:
		try:
			for x in objs[o].specialPOPGadgetRetESP:
				gadget=x
			for x in objs[o].specialPOPBytesRetESP:
				bytesPop=x
			return True, gadget, bytesPop
		except:
			# print "# No gadget found."
			return False, "",0
def preprocessOP_JMPPTR(NumOpsDis, Reg):
	Reg = Reg.upper()
	global o
	clearHashChecker()
	i=0
	results =[]
	for obj in objs:
		# print "Regg " + Reg
		cnt1=0
		if Reg == "EAX":
			cnt1 = objs[o].listOP_JMP_PTR_EAX.__len__()
		if Reg == "EBX":
			cnt1 = objs[o].listOP_JMP_PTR_EBX.__len__()
		if Reg == "ECX":
			cnt1 = objs[o].listOP_JMP_PTR_ECX.__len__()
		if Reg == "EDX":
			cnt1 = objs[o].listOP_JMP_PTR_EDX.__len__()
		if Reg == "ESI":
			cnt1 = objs[o].listOP_JMP_PTR_ESI.__len__()
		if Reg == "EDI":
			cnt1 = objs[o].listOP_JMP_PTR_EDI.__len__()
		if Reg == "ESP":
			cnt1 = objs[o].listOP_JMP_PTR_ESP.__len__()
		if Reg == "EBP":
			cnt1 = objs[o].listOP_JMP_PTR_EBP.__len__()
		for i in range (cnt1):
			addy =0
			cnt = 0   #
			num = 0
			if Reg == "EAX":
				addy = objs[o].listOP_JMP_PTR_EAX[i]
				cnt = objs[o].listOP_JMP_PTR_EAX_CNT[i]
				num = objs[o].listOP_JMP_PTR_EAX_NumOps[i]
				mod = objs[o].listOP_JMP_PTR_EAX_Module[i]
			if Reg == "EBX":
				addy = objs[o].listOP_JMP_PTR_EBX[i]
				cnt = objs[o].listOP_JMP_PTR_EBX_CNT[i]
				num = objs[o].listOP_JMP_PTR_EBX_NumOps[i]
				mod = objs[o].listOP_JMP_PTR_EBX_Module[i]
			if Reg == "ECX":
				addy = objs[o].listOP_JMP_PTR_ECX[i]
				cnt = objs[o].listOP_JMP_PTR_ECX_CNT[i]
				num = objs[o].listOP_JMP_PTR_ECX_NumOps[i]
				mod = objs[o].listOP_JMP_PTR_ECX_Module[i]
			if Reg == "EDX":
				addy = objs[o].listOP_JMP_PTR_EDX[i]
				cnt = objs[o].listOP_JMP_PTR_EDX_CNT[i]
				num = objs[o].listOP_JMP_PTR_EDX_NumOps[i]
				mod = objs[o].listOP_JMP_PTR_EDX_Module[i]
			if Reg == "ESI":
				addy = objs[o].listOP_JMP_PTR_ESI[i]
				cnt = objs[o].listOP_JMP_PTR_ESI_CNT[i]
				num = objs[o].listOP_JMP_PTR_ESI_NumOps[i]
				mod = objs[o].listOP_JMP_PTR_ESI_Module[i]
			if Reg == "EDI":
				addy = objs[o].listOP_JMP_PTR_EDI[i]
				cnt = objs[o].listOP_JMP_PTR_EDI_CNT[i]
				num = objs[o].listOP_JMP_PTR_EDI_NumOps[i]
				mod = objs[o].listOP_JMP_PTR_EDI_Module[i]
			if Reg == "EBP":
				addy = objs[o].listOP_JMP_PTR_EBP[i]
				cnt = objs[o].listOP_JMP_PTR_EBP_CNT[i]
				num = objs[o].listOP_JMP_PTR_EBP_NumOps[i]
				mod = objs[o].listOP_JMP_PTR_EBP_Module[i]
			if Reg == "ESP":
				addy = objs[o].listOP_JMP_PTR_ESP[i]
				cnt = objs[o].listOP_JMP_PTR_ESP_CNT[i]
				num = objs[o].listOP_JMP_PTR_ESP_NumOps[i]
				mod = objs[o].listOP_JMP_PTR_ESP_Module[i]
			spbytes =0
			SPSuccess=False
			#mjmp
			SPSuccess2, spgadget2= disHereCleanJMPPTR(addy, cnt, num, mod) 
			# spgadget2+= " " + mod

		
			if SPSuccess2==True:
				# print "Found JMP PTR:"
				# print spgadget2
				results.append(spgadget2)
		o = o + 1
	o = 0
	output = ""

	try:
		output1=results[0]
		output = output1.split("#")
		# print "did split"
		# print output1

	except:
		# print "exception" + Reg
		pass
		# pass
	new = ""
	note =""
	# print "before for loop"
	# print "output " + output1
	# for word in output:
	# 	matchObj2 = re.match( r'^ jmp dword ptr \[eax \+ eax]+', word, re.M|re.I)
	# 	if matchObj2: 
	# 		word = " jmp dword ptr [esp]* "
	# 		# note = " # (Capstone returned jmp dword ptr [eax + eax}, but this was changed to jmp dword ptr [esp]) "
	# 		new += "#" + word
	# 		output = new +note
	# print "giving output " + output
	return output1

def preprocessOP_JMP(NumOpsDis, Reg):
	# print "fpopreg " +  Reg 
	Reg = Reg.upper()
	global o
	clearHashChecker()
	i=0
	results =[]
	for obj in objs:
		# print "Regg " + Reg
		cnt1=0
		if Reg == "EAX":
			cnt1 = objs[o].listOP_JMP_EAX2.__len__()
		if Reg == "EBX":
			cnt1 = objs[o].listOP_JMP_EBX.__len__()
		if Reg == "ECX":
			cnt1 = objs[o].listOP_JMP_ECX.__len__()
		if Reg == "EDX":
			cnt1 = objs[o].listOP_JMP_EDX.__len__()
		if Reg == "ESI":
			cnt1 = objs[o].listOP_JMP_ESI.__len__()
		if Reg == "EDI":
			cnt1 = objs[o].listOP_JMP_EDI.__len__()
		if Reg == "ESP":
			cnt1 = objs[o].listOP_JMP_ESP.__len__()
		if Reg == "EBP":
			cnt1 = objs[o].listOP_JMP_EBP.__len__()
		for i in range (cnt1):
			addy =0
			cnt = 0   #
			num = 0
			mod = ""
			if Reg == "EAX":
				addy = objs[o].listOP_JMP_EAX2[i]
				cnt = objs[o].listOP_JMP_EAX_CNT[i]
				num = objs[o].listOP_JMP_EAX_NumOps[i]
				mod = objs[o].listOP_JMP_EAX_Module[i]
			if Reg == "EBX":
				addy = objs[o].listOP_JMP_EBX[i]
				cnt = objs[o].listOP_JMP_EBX_CNT[i]
				num = objs[o].listOP_JMP_EBX_NumOps[i]
				mod = objs[o].listOP_JMP_EBX_Module[i]
			if Reg == "ECX":
				addy = objs[o].listOP_JMP_ECX[i]
				cnt = objs[o].listOP_JMP_ECX_CNT[i]
				num = objs[o].listOP_JMP_ECX_NumOps[i]
				mod = objs[o].listOP_JMP_ECX_Module[i]
			if Reg == "EDX":
				addy = objs[o].listOP_JMP_EDX[i]
				cnt = objs[o].listOP_JMP_EDX_CNT[i]
				num = objs[o].listOP_JMP_EDX_NumOps[i]
				mod = objs[o].listOP_JMP_EDX_Module[i]
			if Reg == "ESI":
				addy = objs[o].listOP_JMP_ESI[i]
				cnt = objs[o].listOP_JMP_ESI_CNT[i]
				num = objs[o].listOP_JMP_ESI_NumOps[i]
				mod = objs[o].listOP_JMP_ESI_Module[i]
			if Reg == "EDI":
				addy = objs[o].listOP_JMP_EDI[i]
				cnt = objs[o].listOP_JMP_EDI_CNT[i]
				num = objs[o].listOP_JMP_EDI_NumOps[i]
				mod = objs[o].listOP_JMP_EDI_Module[i]
			if Reg == "EBP":
				addy = objs[o].listOP_JMP_EBP[i]
				cnt = objs[o].listOP_JMP_EBP_CNT[i]
				num = objs[o].listOP_JMP_EBP_NumOps[i]
				mod = objs[o].listOP_JMP_EBP_Module[i]
			if Reg == "ESP":
				addy = objs[o].listOP_JMP_ESP[i]
				cnt = objs[o].listOP_JMP_ESP_CNT[i]
				num = objs[o].listOP_JMP_ESP_NumOps[i]
				mod = objs[o].listOP_JMP_ESP_Module[i]
			spbytes =0
			SPSuccess2=False
			spgadget2=""
			try:
				SPSuccess2, spgadget2= disHereCleanJMPPTR(addy, cnt, num, mod) 
			except:
				pass
			spgadget2+= " " + mod

			if SPSuccess2==True:
				# print "Found JMP:"
				# print spgadget2
				results.append(spgadget2)
		o = o + 1
	o = 0
	output1 = ""
	try:
		output1=results[0]
		# output = output1.split("#")
	except:
		try:
			output1 = spgadget2
		except:
			pass
	return output1

def printlistOP_SP2(NumOpsDis, Reg):
	global o
	clearHashChecker()
	idval = 1
	while os.path.exists("%s-S_PIVOT__%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"S_PIVOT__" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		i=0
		total = 0
		temp = []
		out1 = []
		out2 =[]
		for obj in objs:
			if Reg == "ALL":
				cnt1 = objs[o].listOP_BaseStackPivot.__len__()
			if Reg == "EAX":
				cnt1 = objs[o].listOP_BaseStackPivotEAX.__len__()
			if Reg == "EBX":
				cnt1 = objs[o].listOP_BaseStackPivotEBX.__len__()
			if Reg == "ECX":
				cnt1 = objs[o].listOP_BaseStackPivotECX.__len__()
			if Reg == "EDX":
				cnt1 = objs[o].listOP_BaseStackPivotEDX.__len__()
			if Reg == "ESI":
				cnt1 = objs[o].listOP_BaseStackPivotESI.__len__()
			if Reg == "EDI":
				cnt1 = objs[o].listOP_BaseStackPivotEDI.__len__()
			if Reg == "ESP":
				cnt1 = objs[o].listOP_BaseStackPivotESP.__len__()
			if Reg == "EBP":
				cnt1 = objs[o].listOP_BaseStackPivotEBP.__len__()
			for i in range (cnt1):
				addy =0
				cnt = 0   #
				num = 0
				if Reg == "ALL":
					addy = objs[o].listOP_BaseStackPivot[i]
					cnt = objs[o].listOP_BaseStackPivot_CNT[i]
					num = objs[o].listOP_BaseStackPivot_NumOps[i]
					mod = objs[o].listOP_BaseStackPivot_Module[i]
					spe = objs[o].listOP_BaseStackPivot_Special[i]
				if Reg == "EAX":
					addy = objs[o].listOP_BaseStackPivotEAX[i]
					cnt = objs[o].listOP_BaseStackPivotEAX_CNT[i]
					num = objs[o].listOP_BaseStackPivotEAX_NumOps[i]
					mod = objs[o].listOP_BaseStackPivotEAX_Module[i]
					spe = objs[o].listOP_BaseStackPivotEAX_Special[i]
					
				if Reg == "EBX":
					addy = objs[o].listOP_BaseStackPivotEBX[i]
					cnt = objs[o].listOP_BaseStackPivotEBX_CNT[i]
					num = objs[o].listOP_BaseStackPivotEBX_NumOps[i]
					mod = objs[o].listOP_BaseStackPivotEBX_Module[i]
					spe = objs[o].listOP_BaseStackPivotEBX_Special[i]
				if Reg == "ECX":
					addy = objs[o].listOP_BaseStackPivotECX[i]
					cnt = objs[o].listOP_BaseStackPivotECX_CNT[i]
					num = objs[o].listOP_BaseStackPivotECX_NumOps[i]
					mod = objs[o].listOP_BaseStackPivotECX_Module[i]
					spe = objs[o].listOP_BaseStackPivotECX_Special[i]
				if Reg == "EDX":
					addy = objs[o].listOP_BaseStackPivotEDX[i]
					cnt = objs[o].listOP_BaseStackPivotEDX_CNT[i]
					num = objs[o].listOP_BaseStackPivotEDX_NumOps[i]
					mod = objs[o].listOP_BaseStackPivotEDX_Module[i]
					spe = objs[o].listOP_BaseStackPivotEDX_Special[i]
				if Reg == "ESI":
					addy = objs[o].listOP_BaseStackPivotESI[i]
					cnt = objs[o].listOP_BaseStackPivotESI_CNT[i]
					num = objs[o].listOP_BaseStackPivotESI_NumOps[i]
					mod = objs[o].listOP_BaseStackPivotESI_Module[i]
					spe = objs[o].listOP_BaseStackPivotESI_Special[i]
				if Reg == "EDI":
					addy = objs[o].listOP_BaseStackPivotEDI[i]
					cnt = objs[o].listOP_BaseStackPivotEDI_CNT[i]
					num = objs[o].listOP_BaseStackPivotEDI_NumOps[i]
					mod = objs[o].listOP_BaseStackPivotEDI_Module[i]
					spe = objs[o].listOP_BaseStackPivotEDI_Special[i]
				if Reg == "EBP":
					addy = objs[o].listOP_BaseStackPivotEBP[i]
					cnt = objs[o].listOP_BaseStackPivotEBP_CNT[i]
					num = objs[o].listOP_BaseStackPivotEBP_NumOps[i]
					mod = objs[o].listOP_BaseStackPivotEBP_Module[i]
					spe = objs[o].listOP_BaseStackPivotEBP_Special[i]
				if Reg == "ESP":
					addy = objs[o].listOP_BaseStackPivotESP[i]
					cnt = objs[o].listOP_BaseStackPivotESP_CNT[i]
					num = objs[o].listOP_BaseStackPivotESP_NumOps[i]
					mod = objs[o].listOP_BaseStackPivotESP_Module[i]
					spe = objs[o].listOP_BaseStackPivotESP_Special[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)  + "\t"  + str(spe) + " bytes "
				spbytes =0
				SPSuccess=False
				SPSuccess, spgadget, spbytes= disHereCleanSP(addy, cnt, num, spe, Reg, mod) 
				spgadget= spgadget+ "\t" + str(mod)  
				if SPSuccess:
					out1.append(spgadget)
					out2.append(spbytes)
				if SPSuccess:
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, spgadget
			if cnt1 > 0:
				temp.append(out)

			x=0
			#out1, out2= sortBytes2(out1,out2)
			#sortBytesSPAll()


			print >> f, "\n\n\n\n"
			print >> f, Reg	
			for each in out1:
				#if each != " ":
				print >> f,  "\t" + str(out2[x]) + " bytes - " + each
				x+=1

			total = total + cnt1	
			o = o + 1
			clearGOuts()
		for out in temp:
			#print out
			#print >> f, out
			pass
		out = "\nJOP ROCKET" #out = ""#"# Grand total ADD "  + str(Reg) + " : " + str(total)
		#print out
		print >> f, out
	o = 0
	nope(filename, total)


def printlistOP_StackPivot(NumOpsDis, Reg):
	global o
	idval = 1
	clearHashChecker()
	while os.path.exists("%s-STACK_PIVOT_%s-%s.txt" % (peName, Reg, idval)):
	    idval += 1
	filename = peName +"-STACK_PIVOT_" + Reg + "-" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		i=0
		temp = []
		total = 0
		for obj in objs:
			if Reg != "0":
				cnt1 = objs[o].listOP_BaseStackPivot_NumOps.__len__()
			for i in range (cnt1):
				addy =0
				cnt = 0   #
				num = 0
				if Reg != "0":
						addy = objs[o].listOP_BaseStackPivot = []
						cnt = objs[o].listOP_BaseStackPivot_CNT = []
						num = objs[o].listOP_BaseStackPivot_NumOps = []
						mod = objs[o].listOP_BaseStackPivot_Module = []
						spe = objs[o].listOP_BaseStackPivot_Special = []
				
				out = "Ops: " + str(num) + "\tMod: " + str(mod) + "\tPivot: " + str(spec)
				cat = disHereClean3(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if cnt1 > 0:
				temp.append(out)
			total = total + cnt1	
			o = o + 1
			clearGOuts()
		for out in temp:
			#print out
			pass#print >> f, out
		out = "JOP ROCKET"#"# Grand total ROTATE RIGHT "  + str(Reg) + " : " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)
	print "bye"
	sp()


def printlistOP_Add(NumOpsDis, Reg):
	global printAdd
	global filename
	if printAdd:
	

		global o
		clearHashChecker()
		idval = 1
		# print "in printlistop_add"
		while os.path.exists("%s-ADD_OP_%s_%s.txt" % (peName, Reg, idval)):
		    idval += 1
		filename = peName +"-"+"ADD_OP_"+Reg+"_" + str(idval) + ".txt"
		
		fname = filename
		with open(filename, 'a') as f:
			counterReset()
			i=0
			total = 0
			temp = []
			for obj in objs:
				if Reg == "ALL":
					cnt1 = objs[o].listOP_BaseAdd.__len__()
				if Reg == "EAX":
					cnt1 = objs[o].listOP_BaseAddEAX.__len__()
				if Reg == "EBX":
					cnt1 = objs[o].listOP_BaseAddEBX.__len__()
				if Reg == "ECX":
					cnt1 = objs[o].listOP_BaseAddECX.__len__()
				if Reg == "EDX":
					cnt1 = objs[o].listOP_BaseAddEDX.__len__()
				if Reg == "ESI":
					cnt1 = objs[o].listOP_BaseAddESI.__len__()
				if Reg == "EDI":
					cnt1 = objs[o].listOP_BaseAddEDI.__len__()
				if Reg == "ESP":
					cnt1 = objs[o].listOP_BaseAddESP.__len__()
				if Reg == "EBP":
					cnt1 = objs[o].listOP_BaseAddEBP.__len__()

				for i in range (cnt1):
					##print "\n@ADD^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^\n"
					#print >> f, "@ADD*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					#counter()
					##counterShow()

					addy =0
					cnt = 0   #
					num = 0
					if Reg == "ALL":
						addy = objs[o].listOP_BaseAdd[i]
						cnt = objs[o].listOP_BaseAdd_CNT[i]
						num = objs[o].listOP_BaseAdd_NumOps[i]
						mod = objs[o].listOP_BaseAdd_Module[i]
					if Reg == "EAX":
						addy = objs[o].listOP_BaseAddEAX[i]
						cnt = objs[o].listOP_BaseAddEAX_CNT[i]
						num = objs[o].listOP_BaseAddEAX_NumOps[i]
						mod = objs[o].listOP_BaseAddEAX_Module[i]
					if Reg == "EBX":
						addy = objs[o].listOP_BaseAddEBX[i]
						cnt = objs[o].listOP_BaseAddEBX_CNT[i]
						num = objs[o].listOP_BaseAddEBX_NumOps[i]
						mod = objs[o].listOP_BaseAddEBX_Module[i]
					if Reg == "ECX":
						addy = objs[o].listOP_BaseAddECX[i]
						cnt = objs[o].listOP_BaseAddECX_CNT[i]
						num = objs[o].listOP_BaseAddECX_NumOps[i]
						mod = objs[o].listOP_BaseAddECX_Module[i]
					if Reg == "EDX":
						addy = objs[o].listOP_BaseAddEDX[i]
						cnt = objs[o].listOP_BaseAddEDX_CNT[i]
						num = objs[o].listOP_BaseAddEDX_NumOps[i]
						mod = objs[o].listOP_BaseAddEDX_Module[i]
					if Reg == "ESI":
						addy = objs[o].listOP_BaseAddESI[i]
						cnt = objs[o].listOP_BaseAddESI_CNT[i]
						num = objs[o].listOP_BaseAddESI_NumOps[i]
						mod = objs[o].listOP_BaseAddESI_Module[i]
					if Reg == "EDI":
						addy = objs[o].listOP_BaseAddEDI[i]
						cnt = objs[o].listOP_BaseAddEDI_CNT[i]
						num = objs[o].listOP_BaseAddEDI_NumOps[i]
						mod = objs[o].listOP_BaseAddEDI_Module[i]
					if Reg == "EBP":
						addy = objs[o].listOP_BaseAddEBP[i]
						cnt = objs[o].listOP_BaseAddEBP_CNT[i]
						num = objs[o].listOP_BaseAddEBP_NumOps[i]
						mod = objs[o].listOP_BaseAddEBP_Module[i]
					if Reg == "ESP":
						addy = objs[o].listOP_BaseAddESP[i]
						cnt = objs[o].listOP_BaseAddESP_CNT[i]
						num = objs[o].listOP_BaseAddESP_NumOps[i]
						mod = objs[o].listOP_BaseAddESP_Module[i]
					out = "Ops: " + str(num) + "\tMod: " + str(mod) 
					##print out
					cat = disHereClean3(addy, cnt, num,"jmp")
					if not cat == " ":
						print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
						counter()
						print >> f, Ct () + "\t" + out
						print >> f, cat

				if cnt1 > 0:
				#	out = "# Add " + str(Reg) + " " + str(mod) + " total: " + str(cnt1) 
					temp.append(out)
				total = total + cnt1	
				# cnteax = objs[0].listOP_BaseAddEAX.__len__()
				# print  "eax: " + str(cnteax)
				# cntebx = objs[0].listOP_BaseAddEBX.__len__()
				# print  "ebx: " + str(cntebx)
				# cntecx = objs[0].listOP_BaseAddECX.__len__()
				# print  "ecx: " + str(cntecx)
				# cntedx = objs[0].listOP_BaseAddEDX.__len__()
				# print  "edx: " + str(cntedx)
				# cntesi = objs[0].listOP_BaseAddESI.__len__()
				# print  "esi: " + str(cntesi)
				# cntedi = objs[0].listOP_BaseAddEDI.__len__()
				# print  "edi: " + str(cntedi)
				# cntesp = objs[0].listOP_BaseAddESP.__len__()
				# print  "esp: " + str(cntesp)
				# cntebp = objs[0].listOP_BaseAddEBP.__len__()
				# print  "ebp: " + str(cntebp)
				
				o = o + 1
				clearGOuts()
				# print "after cleargouts"
			out = "\nJOP ROCKET" #out = ""#"# Grand total ADD "  + str(Reg) + " : " + str(total)
			print >> f, out
		# print "trying to reset to o??"
		o = 0
		f.close()
		# print "after f.close"
		nope(filename, total)


def nope(filename, total):
	
	size = os.stat(filename).st_size
	# print "nope " + filename
	if total == 0:
		try:
			# print "remove " + filename
			os.remove(filename)
			#print "removing " + str(filename)
		except OSError:
			pass
	if size < 20:
		try:
			# print "cutting down " + filename
			os.remove(filename)
			#print "removing " + str(filename)
		except OSError:
			pass
	else:
		# print "\t" + str(filename)  + " " +str(size) + " bytes"
		# print size
		pass

oldFilename=""
def nope3(filename):
	global oldFilename
	try:
		size = os.stat(filename).st_size

		# print "nope3 " + filename
		if size < 10:
			try:
				# print "n3 cutting down " + filename
				os.remove(filename)
				#print "removing " + str(filename)
			except OSError:
				pass
		else:
			if (oldFilename != filename):
				print "\t" + str(filename)  + " \t" +str(float(size)/1000.0) + " kb"
			oldFilename=filename

			# print size
	except:
		oldFilename=filename
		pass
# Prevents files from being printed if empty or have no results - just removes them.


def nope2(filename, total, index):
	if total < 1:  
		try:
			os.remove(filename)
#			print "removing " + str(filename)
			sp()
		except OSError:
			pass

	else:
		if index == 0:
			if total == 1:
				os.remove(filename)
				sp()
			else:
				# print "\t" + str(filename)
				sp()
		else:
			# print "\t" + str(filename)
			sp()

def printlistOP_Sub(NumOpsDis, Reg):
	global o
	idval = 1
	clearHashChecker()
	while os.path.exists("%s-SUB_OP_%s-%s.txt" % (peName, Reg, idval)):
	    idval += 1
	filename = peName +"-SUB_OP_" + Reg + "-" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		i=0
		temp = []
		total = 0
		for obj in objs:
			if Reg == "ALL":
				cnt1 = objs[o].listOP_BaseSub.__len__()

			if Reg == "EAX":
				cnt1 = objs[o].listOP_BaseSubEAX.__len__()
			if Reg == "EBX":
				cnt1 = objs[o].listOP_BaseSubEBX.__len__()
			if Reg == "ECX":
				cnt1 = objs[o].listOP_BaseSubECX.__len__()
			if Reg == "EDX":
				cnt1 = objs[o].listOP_BaseSubEDX.__len__()
			if Reg == "ESI":
				cnt1 = objs[o].listOP_BaseSubESI.__len__()
			if Reg == "EDI":
				cnt1 = objs[o].listOP_BaseSubEDI.__len__()
			if Reg == "ESP":
				cnt1 = objs[o].listOP_BaseSubESP.__len__()
			if Reg == "EBP":
				cnt1 = objs[o].listOP_BaseSubEBP.__len__()
			for i in range (cnt1):

				addy =0
				cnt = 0   #
				num = 0
				if Reg == "ALL":
					addy = objs[o].listOP_BaseSub[i]
					cnt = objs[o].listOP_BaseSub_CNT[i]
					num = objs[o].listOP_BaseSub_NumOps[i]
					mod = objs[o].listOP_BaseSub_Module[i]
				if Reg == "EAX":
					addy = objs[o].listOP_BaseSubEAX[i]
					cnt = objs[o].listOP_BaseSubEAX_CNT[i]
					num = objs[o].listOP_BaseSubEAX_NumOps[i]
					mod = objs[o].listOP_BaseSubEAX_Module[i]
				if Reg == "EBX":
					addy = objs[o].listOP_BaseSubEBX[i]
					cnt = objs[o].listOP_BaseSubEBX_CNT[i]
					num = objs[o].listOP_BaseSubEBX_NumOps[i]
					mod = objs[o].listOP_BaseSubEBX_Module[i]
				if Reg == "ECX":
					addy = objs[o].listOP_BaseSubECX[i]
					cnt = objs[o].listOP_BaseSubECX_CNT[i]
					num = objs[o].listOP_BaseSubECX_NumOps[i]
					mod = objs[o].listOP_BaseSubECX_Module[i]
				if Reg == "EDX":
					addy = objs[o].listOP_BaseSubEDX[i]
					cnt = objs[o].listOP_BaseSubEDX_CNT[i]
					num = objs[o].listOP_BaseSubEDX_NumOps[i]
					mod = objs[o].listOP_BaseSubEDX_Module[i]
				if Reg == "ESI":
					addy = objs[o].listOP_BaseSubESI[i]
					cnt = objs[o].listOP_BaseSubESI_CNT[i]
					num = objs[o].listOP_BaseSubESI_NumOps[i]
					mod = objs[o].listOP_BaseSubESI_Module[i]
				if Reg == "EDI":
					addy = objs[o].listOP_BaseSubEDI[i]
					cnt = objs[o].listOP_BaseSubEDI_CNT[i]
					num = objs[o].listOP_BaseSubEDI_NumOps[i]
					mod = objs[o].listOP_BaseSubEDI_Module[i]
				if Reg == "EBP":
					addy = objs[o].listOP_BaseSubEBP[i]
					cnt = objs[o].listOP_BaseSubEBP_CNT[i]
					num = objs[o].listOP_BaseSubEBP_NumOps[i]
					mod = objs[o].listOP_BaseSubEBP_Module[i]
				if Reg == "ESP":
					addy = objs[o].listOP_BaseSubESP[i]
					cnt = objs[o].listOP_BaseSubESP_CNT[i]
					num = objs[o].listOP_BaseSubESP_NumOps[i]
					mod = objs[o].listOP_BaseSubESP_Module[i]
				
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if cnt1 > 0:
				#out = "# SUB " + str(Reg) + " " + str(mod) + " total: " + str(cnt1) 
				temp.append(out)
			total = total + cnt1	
			o = o + 1
			clearGOuts()
		for out in temp:
			#print out
			print >> f, out
		out = "\nJOP ROCKET"#"# Grand total SUB "  + str(Reg) + " : " + str(total)
		#print out
		print >> f, out
	o = 0
	nope(filename, total)

def printlistOP_Mul(NumOpsDis, Reg):  
	global o
	idval = 1
	clearHashChecker()
	while os.path.exists("%s-MUL_OP_%s-%s.txt" % (peName, Reg, idval)):
	    idval += 1
	filename = peName +"-MUL_OP_" + Reg + "-" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		i=0
		temp = []
		total = 0
		for obj in objs:
			if Reg == "ALL":
				cnt1 = objs[o].listOP_BaseMul.__len__()

			if Reg == "EAX":
				cnt1 = objs[o].listOP_BaseMulEAX.__len__()
			if Reg == "EBX":
				cnt1 = objs[o].listOP_BaseMulEBX.__len__()
			if Reg == "ECX":
				cnt1 = objs[o].listOP_BaseMulECX.__len__()
			if Reg == "EDX":
				cnt1 = objs[o].listOP_BaseMulEDX.__len__()
			if Reg == "ESI":
				cnt1 = objs[o].listOP_BaseMulESI.__len__()
			if Reg == "EDI":
				cnt1 = objs[o].listOP_BaseMulEDI.__len__()
			if Reg == "ESP":
				cnt1 = objs[o].listOP_BaseMulESP.__len__()
			if Reg == "EBP":
				cnt1 = objs[o].listOP_BaseMulEBP.__len__()
			for i in range (cnt1):

				addy =0
				cnt = 0   #
				num = 0
				if Reg == "ALL":
					addy = objs[o].listOP_BaseMul[i]
					cnt = objs[o].listOP_BaseMul_CNT[i]
					num = objs[o].listOP_BaseMul_NumOps[i]
					mod = objs[o].listOP_BaseMul_Module[i]

				if Reg == "EAX":
					addy = objs[o].listOP_BaseMulEAX[i]
					cnt = objs[o].listOP_BaseMulEAX_CNT[i]
					num = objs[o].listOP_BaseMulEAX_NumOps[i]
					mod = objs[o].listOP_BaseMulEAX_Module[i]
				if Reg == "EBX":
					addy = objs[o].listOP_BaseMulEBX[i]
					cnt = objs[o].listOP_BaseMulEBX_CNT[i]
					num = objs[o].listOP_BaseMulEBX_NumOps[i]
					mod = objs[o].listOP_BaseMulEBX_Module[i]
				if Reg == "ECX":
					addy = objs[o].listOP_BaseMulECX[i]
					cnt = objs[o].listOP_BaseMulECX_CNT[i]
					num = objs[o].listOP_BaseMulECX_NumOps[i]
					mod = objs[o].listOP_BaseMulECX_Module[i]
				if Reg == "EDX":
					addy = objs[o].listOP_BaseMulEDX[i]
					cnt = objs[o].listOP_BaseMulEDX_CNT[i]
					num = objs[o].listOP_BaseMulEDX_NumOps[i]
					mod = objs[o].listOP_BaseMulEDX_Module[i]
				if Reg == "ESI":
					addy = objs[o].listOP_BaseMulESI[i]
					cnt = objs[o].listOP_BaseMulESI_CNT[i]
					num = objs[o].listOP_BaseMulESI_NumOps[i]
					mod = objs[o].listOP_BaseMulESI_Module[i]
				if Reg == "EDI":
					addy = objs[o].listOP_BaseMulEDI[i]
					cnt = objs[o].listOP_BaseMulEDI_CNT[i]
					num = objs[o].listOP_BaseMulEDI_NumOps[i]
					mod = objs[o].listOP_BaseMulEDI_Module[i]
				if Reg == "EBP":
					addy = objs[o].listOP_BaseMulEBP[i]
					cnt = objs[o].listOP_BaseMulEBP_CNT[i]
					num = objs[o].listOP_BaseMulEBP_NumOps[i]
					mod = objs[o].listOP_BaseMulEBP_Module[i]
				if Reg == "ESP":
					addy = objs[o].listOP_BaseMulESP[i]
					cnt = objs[o].listOP_BaseMulESP_CNT[i]
					num = objs[o].listOP_BaseMulESP_NumOps[i]
					mod = objs[o].listOP_BaseMulESP_Module[i]
				
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if cnt1 > 0:
				#out = "# MUL " + str(Reg) + " " + str(mod) + " total: " + str(cnt1) 
				temp.append(out)
			total = total + cnt1	
			o = o + 1
			clearGOuts()
		for out in temp:
			pass#print out
			#print >> f, out
		out = "JOP ROCKET"#"# Grand total MUL "  + str(Reg) + " : " + str(total)
		#print total
		#print out
		print >> f, out
	o = 0
	nope(filename, total)

def printlistOP_Div(NumOpsDis, Reg): #6
	global o
	global fname
	idval = 1
	clearHashChecker()
	while os.path.exists("%s-DIV_OP_%s-%s.txt" % (peName, Reg, idval)):
	    idval += 1
	filename = peName +"-DIV_OP_" + Reg + "-" + str(idval) + ".txt"
	fname = filename

	with open(filename, 'a') as f:
		counterReset()
		i=0
		temp = []
		total = 0
		for obj in objs:
			if Reg == "ALL":
				cnt1 = objs[o].listOP_BaseDiv.__len__()
			if Reg == "EAX":
				cnt1 = objs[o].listOP_BaseDivEAX.__len__()
			if Reg == "EDX":
				cnt1 = objs[o].listOP_BaseDivEDX.__len__()
			for i in range (cnt1):
				#print "\n@DIV^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^\n"
				#print >> f, "@DIV*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"

				addy =0
				cnt = 0   #
				num = 0
				if Reg == "ALL":
					addy = objs[o].listOP_BaseDiv[i]
					cnt = objs[o].listOP_BaseDiv_CNT[i]
					num = objs[o].listOP_BaseDiv_NumOps[i]
					mod = objs[o].listOP_BaseDiv_Module[i]
				if Reg == "EAX":
					addy = objs[o].listOP_BaseDivEAX[i]
					cnt = objs[o].listOP_BaseDivEAX_CNT[i]
					num = objs[o].listOP_BaseDivEAX_NumOps[i]
					mod = objs[o].listOP_BaseDivEAX_Module[i]
				if Reg == "EDX":
					addy = objs[o].listOP_BaseDivEDX[i]
					cnt = objs[o].listOP_BaseDivEDX_CNT[i]
					num = objs[o].listOP_BaseDivEDX_NumOps[i]
					mod = objs[o].listOP_BaseDivEDX_Module[i]
				
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if cnt1 > 0:
				out = "# DIV " + str(Reg) + " " + str(mod) + " total: " + str(cnt1) 
				temp.append(out)
			total = total + cnt1	
			o = o + 1
			clearGOuts()
		for out in temp:
			#print out
			pass#print >> f, out
		# out = "\nJOP ROCKET"#"# Grand total DIV "  + str(Reg) + " : " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)


def printlistOP_MovDeref(NumOpsDis, Reg):
	global o
	idval = 1
	clearHashChecker()
	while os.path.exists("%s-MOV_DEREF_OP_%s-%s.txt" % (peName, Reg, idval)):
	    idval += 1
	filename = peName +"-MOV_DEREF_OP_" + Reg + "-" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		i=0
		temp = []
		total = 0
		for obj in objs:
			if Reg == "ALL":
				cnt1 = objs[o].listOP_BaseMovDeref.__len__()

			if Reg == "EAX":
				cnt1 = objs[o].listOP_BaseMovDerefEAX.__len__()
			if Reg == "EBX":
				cnt1 = objs[o].listOP_BaseMovDerefEBX.__len__()
			if Reg == "ECX":
				cnt1 = objs[o].listOP_BaseMovDerefECX.__len__()
			if Reg == "EDX":
				cnt1 = objs[o].listOP_BaseMovDerefEDX.__len__()
			if Reg == "ESI":
				cnt1 = objs[o].listOP_BaseMovDerefESI.__len__()
			if Reg == "EDI":
				cnt1 = objs[o].listOP_BaseMovDerefEDI.__len__()
			if Reg == "ESP":
				cnt1 = objs[o].listOP_BaseMovDerefESP.__len__()
			if Reg == "EBP":
				cnt1 = objs[o].listOP_BaseMovDerefEBP.__len__()
			for i in range (cnt1):
				#print "\n@Mov^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^\n"
				#print >> f, "@Mov*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"


				addy =0
				cnt = 0   #
				num = 0
				if Reg == "ALL":
					addy = objs[o].listOP_BaseMovDeref[i]
					cnt = objs[o].listOP_BaseMovDeref_CNT[i]
					num = objs[o].listOP_BaseMovDeref_NumOps[i]
					mod = objs[o].listOP_BaseMovDeref_Module[i]
				if Reg == "EAX":
					addy = objs[o].listOP_BaseMovDerefEAX[i]
					cnt = objs[o].listOP_BaseMovDerefEAX_CNT[i]
					num = objs[o].listOP_BaseMovDerefEAX_NumOps[i]
					mod = objs[o].listOP_BaseMovDerefEAX_Module[i]
				if Reg == "EBX":
					addy = objs[o].listOP_BaseMovDerefEBX[i]
					cnt = objs[o].listOP_BaseMovDerefEBX_CNT[i]
					num = objs[o].listOP_BaseMovDerefEBX_NumOps[i]
					mod = objs[o].listOP_BaseMovDerefEBX_Module[i]
				if Reg == "ECX":
					addy = objs[o].listOP_BaseMovDerefECX[i]
					cnt = objs[o].listOP_BaseMovDerefECX_CNT[i]
					num = objs[o].listOP_BaseMovDerefECX_NumOps[i]
					mod = objs[o].listOP_BaseMovDerefECX_Module[i]
				if Reg == "EDX":
					addy = objs[o].listOP_BaseMovDerefEDX[i]
					cnt = objs[o].listOP_BaseMovDerefEDX_CNT[i]
					num = objs[o].listOP_BaseMovDerefEDX_NumOps[i]
					mod = objs[o].listOP_BaseMovDerefEDX_Module[i]
				if Reg == "ESI":
					addy = objs[o].listOP_BaseMovDerefESI[i]
					cnt = objs[o].listOP_BaseMovDerefESI_CNT[i]
					num = objs[o].listOP_BaseMovDerefESI_NumOps[i]
					mod = objs[o].listOP_BaseMovDerefESI_Module[i]
				if Reg == "EDI":
					addy = objs[o].listOP_BaseMovDerefEDI[i]
					cnt = objs[o].listOP_BaseMovDerefEDI_CNT[i]
					num = objs[o].listOP_BaseMovDerefEDI_NumOps[i]
					mod = objs[o].listOP_BaseMovDerefEDI_Module[i]
				if Reg == "EBP":
					addy = objs[o].listOP_BaseMovDerefEBP[i]
					cnt = objs[o].listOP_BaseMovDerefEBP_CNT[i]
					num = objs[o].listOP_BaseMovDerefEBP_NumOps[i]
					mod = objs[o].listOP_BaseMovDerefEBP_Module[i]
				if Reg == "ESP":
					addy = objs[o].listOP_BaseMovDerefESP[i]
					cnt = objs[o].listOP_BaseMovDerefESP_CNT[i]
					num = objs[o].listOP_BaseMovDerefESP_NumOps[i]
					mod = objs[o].listOP_BaseMovDerefESP_Module[i]
				
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if cnt1 > 0:
				#out = "# MOV " + str(Reg) + " " + str(mod) + " total: " + str(cnt1) 
				temp.append(out)
			total = total + cnt1	
			o = o + 1
			clearGOuts()
		for out in temp:
			#print out
			pass#print >> f, out
		out = "\nJOP ROCKET"#"# Grand total MOV "  + str(Reg) + " : " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)

def printlistOP_Mov(NumOpsDis, Reg):
	global o
	idval = 1
	clearHashChecker()
	while os.path.exists("%s-MOV_OP_%s-%s.txt" % (peName, Reg, idval)):
	    idval += 1
	filename = peName +"-MOV_OP_" + Reg + "-" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		i=0
		temp = []
		total = 0
		for obj in objs:
			if Reg == "ALL":
				cnt1 = objs[o].listOP_BaseMov.__len__()

			if Reg == "EAX":
				cnt1 = objs[o].listOP_BaseMovEAX.__len__()
			if Reg == "EBX":
				cnt1 = objs[o].listOP_BaseMovEBX.__len__()
			if Reg == "ECX":
				cnt1 = objs[o].listOP_BaseMovECX.__len__()
			if Reg == "EDX":
				cnt1 = objs[o].listOP_BaseMovEDX.__len__()
			if Reg == "ESI":
				cnt1 = objs[o].listOP_BaseMovESI.__len__()
			if Reg == "EDI":
				cnt1 = objs[o].listOP_BaseMovEDI.__len__()
			if Reg == "ESP":
				cnt1 = objs[o].listOP_BaseMovESP.__len__()
			if Reg == "EBP":
				cnt1 = objs[o].listOP_BaseMovEBP.__len__()
			for i in range (cnt1):
				#print "\n@Mov^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^\n"
				#print >> f, "@Mov*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"


				addy =0
				cnt = 0   #
				num = 0
				if Reg == "ALL":
					addy = objs[o].listOP_BaseMov[i]
					cnt = objs[o].listOP_BaseMov_CNT[i]
					num = objs[o].listOP_BaseMov_NumOps[i]
					mod = objs[o].listOP_BaseMov_Module[i]
				if Reg == "EAX":
					addy = objs[o].listOP_BaseMovEAX[i]
					cnt = objs[o].listOP_BaseMovEAX_CNT[i]
					num = objs[o].listOP_BaseMovEAX_NumOps[i]
					mod = objs[o].listOP_BaseMovEAX_Module[i]
				if Reg == "EBX":
					addy = objs[o].listOP_BaseMovEBX[i]
					cnt = objs[o].listOP_BaseMovEBX_CNT[i]
					num = objs[o].listOP_BaseMovEBX_NumOps[i]
					mod = objs[o].listOP_BaseMovEBX_Module[i]
				if Reg == "ECX":
					addy = objs[o].listOP_BaseMovECX[i]
					cnt = objs[o].listOP_BaseMovECX_CNT[i]
					num = objs[o].listOP_BaseMovECX_NumOps[i]
					mod = objs[o].listOP_BaseMovECX_Module[i]
				if Reg == "EDX":
					addy = objs[o].listOP_BaseMovEDX[i]
					cnt = objs[o].listOP_BaseMovEDX_CNT[i]
					num = objs[o].listOP_BaseMovEDX_NumOps[i]
					mod = objs[o].listOP_BaseMovEDX_Module[i]
				if Reg == "ESI":
					addy = objs[o].listOP_BaseMovESI[i]
					cnt = objs[o].listOP_BaseMovESI_CNT[i]
					num = objs[o].listOP_BaseMovESI_NumOps[i]
					mod = objs[o].listOP_BaseMovESI_Module[i]
				if Reg == "EDI":
					addy = objs[o].listOP_BaseMovEDI[i]
					cnt = objs[o].listOP_BaseMovEDI_CNT[i]
					num = objs[o].listOP_BaseMovEDI_NumOps[i]
					mod = objs[o].listOP_BaseMovEDI_Module[i]
				if Reg == "EBP":
					addy = objs[o].listOP_BaseMovEBP[i]
					cnt = objs[o].listOP_BaseMovEBP_CNT[i]
					num = objs[o].listOP_BaseMovEBP_NumOps[i]
					# print "infos"
					sp()
					# print addy
					# print cnt
					# print num
					# print len(objs[o].listOP_BaseMovEBP_Module)
					mod = objs[o].listOP_BaseMovEBP_Module[i]
				if Reg == "ESP":
					addy = objs[o].listOP_BaseMovESP[i]
					cnt = objs[o].listOP_BaseMovESP_CNT[i]
					num = objs[o].listOP_BaseMovESP_NumOps[i]
					mod = objs[o].listOP_BaseMovESP_Module[i]
				
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if cnt1 > 0:
				#out = "# MOV " + str(Reg) + " " + str(mod) + " total: " + str(cnt1) 
				temp.append(out)
			total = total + cnt1	
			o = o + 1
			clearGOuts()
		for out in temp:
			#print out
			pass#print >> f, out
		out = "\nJOP ROCKET"#"# Grand total MOV "  + str(Reg) + " : " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)

def printlistOP_MovShuf(NumOpsDis, Reg):
	global o
	idval = 1
	clearHashChecker()
	while os.path.exists("%s-MOV_Shuf_OP_%s-%s.txt" % (peName, Reg, idval)):
	    idval += 1
	filename = peName +"-MOV_SHUF_OP_" + Reg + "-" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		i=0
		temp = []
		total = 0
		for obj in objs:
			if Reg == "ALL":
				cnt1 = objs[o].listOP_BaseMovShuf.__len__()

			if Reg == "EAX":
				cnt1 = objs[o].listOP_BaseMovShufEAX.__len__()
			if Reg == "EBX":
				cnt1 = objs[o].listOP_BaseMovShufEBX.__len__()
			if Reg == "ECX":
				cnt1 = objs[o].listOP_BaseMovShufECX.__len__()
			if Reg == "EDX":
				cnt1 = objs[o].listOP_BaseMovShufEDX.__len__()
			if Reg == "ESI":
				cnt1 = objs[o].listOP_BaseMovShufESI.__len__()
			if Reg == "EDI":
				cnt1 = objs[o].listOP_BaseMovShufEDI.__len__()
			if Reg == "ESP":
				cnt1 = objs[o].listOP_BaseMovShufESP.__len__()
			if Reg == "EBP":
				cnt1 = objs[o].listOP_BaseMovShufEBP.__len__()
			for i in range (cnt1):
				#print "\n@MOV_SHUF^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^\n"
				#print >> f, "@MOV_SHUF*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"


				addy =0
				cnt = 0   #
				num = 0
				if Reg == "ALL":
					addy = objs[o].listOP_BaseMovShuf[i]
					cnt = objs[o].listOP_BaseMovShuf_CNT[i]
					num = objs[o].listOP_BaseMovShuf_NumOps[i]
					mod = objs[o].listOP_BaseMovShuf_Module[i]
				if Reg == "EAX":
					addy = objs[o].listOP_BaseMovShufEAX[i]
					cnt = objs[o].listOP_BaseMovShufEAX_CNT[i]
					num = objs[o].listOP_BaseMovShufEAX_NumOps[i]
					mod = objs[o].listOP_BaseMovShufEAX_Module[i]
				if Reg == "EBX":
					addy = objs[o].listOP_BaseMovShufEBX[i]
					cnt = objs[o].listOP_BaseMovShufEBX_CNT[i]
					num = objs[o].listOP_BaseMovShufEBX_NumOps[i]
					mod = objs[o].listOP_BaseMovShufEBX_Module[i]
				if Reg == "ECX":
					addy = objs[o].listOP_BaseMovShufECX[i]
					cnt = objs[o].listOP_BaseMovShufECX_CNT[i]
					num = objs[o].listOP_BaseMovShufECX_NumOps[i]
					mod = objs[o].listOP_BaseMovShufECX_Module[i]
				if Reg == "EDX":
					addy = objs[o].listOP_BaseMovShufEDX[i]
					cnt = objs[o].listOP_BaseMovShufEDX_CNT[i]
					num = objs[o].listOP_BaseMovShufEDX_NumOps[i]
					mod = objs[o].listOP_BaseMovShufEDX_Module[i]
				if Reg == "ESI":
					addy = objs[o].listOP_BaseMovShufESI[i]
					cnt = objs[o].listOP_BaseMovShufESI_CNT[i]
					num = objs[o].listOP_BaseMovShufESI_NumOps[i]
					mod = objs[o].listOP_BaseMovShufESI_Module[i]
				if Reg == "EDI":
					addy = objs[o].listOP_BaseMovShufEDI[i]
					cnt = objs[o].listOP_BaseMovShufEDI_CNT[i]
					num = objs[o].listOP_BaseMovShufEDI_NumOps[i]
					mod = objs[o].listOP_BaseMovShufEDI_Module[i]
				if Reg == "EBP":
					addy = objs[o].listOP_BaseMovShufEBP[i]
					cnt = objs[o].listOP_BaseMovShufEBP_CNT[i]
					num = objs[o].listOP_BaseMovShufEBP_NumOps[i]
					mod = objs[o].listOP_BaseMovShufEBP_Module[i]
				if Reg == "ESP":
					addy = objs[o].listOP_BaseMovShufESP[i]
					cnt = objs[o].listOP_BaseMovShufESP_CNT[i]
					num = objs[o].listOP_BaseMovShufESP_NumOps[i]
					mod = objs[o].listOP_BaseMovShufESP_Module[i]
				
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if cnt1 > 0:
				#out = "# MOV Shuffle " + str(Reg) + " " + str(mod) + " total: " + str(cnt1) 
				temp.append(out)
			total = total + cnt1	
			o = o + 1
			clearGOuts()
		for out in temp:
			#print out
			pass#print >> f, out
		out = "\n JOP ROCKET"#"# Grand total MOV Shuffle "  + str(Reg) + " : " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)

# print mov values into registers
def printlistOP_MovVal(NumOpsDis, Reg):
	global o
	idval = 1
	clearHashChecker()
	while os.path.exists("%s-MOV_VAL_OP_%s-%s.txt" % (peName, Reg, idval)):
	    idval += 1
	filename = peName +"-MOV_VAL_OP_" + Reg + "-" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		temp = []
		total = 0
		for obj in objs:
			if Reg == "ALL":
				cnt1 = objs[o].listOP_BaseMovVal.__len__()

			if Reg == "EAX":
				cnt1 = objs[o].listOP_BaseMovValEAX.__len__()
			if Reg == "EBX":
				cnt1 = objs[o].listOP_BaseMovValEBX.__len__()
			if Reg == "ECX":
				cnt1 = objs[o].listOP_BaseMovValECX.__len__()
			if Reg == "EDX":
				cnt1 = objs[o].listOP_BaseMovValEDX.__len__()
			if Reg == "ESI":
				cnt1 = objs[o].listOP_BaseMovValESI.__len__()
			if Reg == "EDI":
				cnt1 = objs[o].listOP_BaseMovValEDI.__len__()
			if Reg == "ESP":
				cnt1 = objs[o].listOP_BaseMovValESP.__len__()
			if Reg == "EBP":
				cnt1 = objs[o].listOP_BaseMovValEBP.__len__()
			# print "printing count " + Reg + " " + str(cnt1)

			for i in range (cnt1):
				#print "\n@MOV Val^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^\n"
				#print >> f, "@MOV Val*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"

				addy =0
				cnt = 0   #
				num = 0
				if Reg == "ALL":
					addy = objs[o].listOP_BaseMovVal[i]
					cnt = objs[o].listOP_BaseMovVal_CNT[i]
					num = objs[o].listOP_BaseMovVal_NumOps[i]
					mod = objs[o].listOP_BaseMovVal_Module[i]
				if Reg == "EAX":
					addy = objs[o].listOP_BaseMovValEAX[i]
					cnt = objs[o].listOP_BaseMovValEAX_CNT[i]
					num = objs[o].listOP_BaseMovValEAX_NumOps[i]
					mod = objs[o].listOP_BaseMovValEAX_Module[i]
				if Reg == "EBX":
					addy = objs[o].listOP_BaseMovValEBX[i]
					cnt = objs[o].listOP_BaseMovValEBX_CNT[i]
					num = objs[o].listOP_BaseMovValEBX_NumOps[i]
					mod = objs[o].listOP_BaseMovValEBX_Module[i]
				if Reg == "ECX":
					addy = objs[o].listOP_BaseMovValECX[i]
					cnt = objs[o].listOP_BaseMovValECX_CNT[i]
					num = objs[o].listOP_BaseMovValECX_NumOps[i]
					mod = objs[o].listOP_BaseMovValECX_Module[i]
				if Reg == "EDX":
					addy = objs[o].listOP_BaseMovValEDX[i]
					cnt = objs[o].listOP_BaseMovValEDX_CNT[i]
					num = objs[o].listOP_BaseMovValEDX_NumOps[i]
					mod = objs[o].listOP_BaseMovValEDX_Module[i]
				if Reg == "ESI":
					addy = objs[o].listOP_BaseMovValESI[i]
					cnt = objs[o].listOP_BaseMovValESI_CNT[i]
					num = objs[o].listOP_BaseMovValESI_NumOps[i]
					mod = objs[o].listOP_BaseMovValESI_Module[i]
				if Reg == "EDI":
					addy = objs[o].listOP_BaseMovValEDI[i]
					cnt = objs[o].listOP_BaseMovValEDI_CNT[i]
					num = objs[o].listOP_BaseMovValEDI_NumOps[i]
					mod = objs[o].listOP_BaseMovValEDI_Module[i]
				if Reg == "EBP":
					addy = objs[o].listOP_BaseMovValEBP[i]
					cnt = objs[o].listOP_BaseMovValEBP_CNT[i]
					num = objs[o].listOP_BaseMovValEBP_NumOps[i]
					mod = objs[o].listOP_BaseMovValEBP_Module[i]
				if Reg == "ESP":
					addy = objs[o].listOP_BaseMovValESP[i]
					cnt = objs[o].listOP_BaseMovValESP_CNT[i]
					num = objs[o].listOP_BaseMovValESP_NumOps[i]
					mod = objs[o].listOP_BaseMovValESP_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, num, "jmp")

				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if cnt1 > 0:
				#out = "# MOV Value " + str(Reg) + " " + str(mod) + " total: " + str(cnt1) 
				temp.append(out)
			total = total + cnt1	
			o = o + 1
			clearGOuts()
		for out in temp:
			#print out
			pass#print >> f, out
		out = "\nJOP ROCKET"#"# Grand total MOV Value "  + str(Reg) + " : " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)

def printlistOP_Lea(NumOpsDis, Reg):
	global o
	idval = 1
	clearHashChecker()
	while os.path.exists("%s-LEA_OP_%s-%s.txt" % (peName, Reg, idval)):
	    idval += 1
	filename = peName +"-LEA_OP_" + Reg + "-" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		i=0
		temp = []
		total = 0
		for obj in objs:
			if Reg == "ALL":
				cnt1 = objs[o].listOP_BaseLea.__len__()

			if Reg == "EAX":
				cnt1 = objs[o].listOP_BaseLeaEAX.__len__()
			if Reg == "EBX":
				cnt1 = objs[o].listOP_BaseLeaEBX.__len__()
			if Reg == "ECX":
				cnt1 = objs[o].listOP_BaseLeaECX.__len__()
			if Reg == "EDX":
				cnt1 = objs[o].listOP_BaseLeaEDX.__len__()
			if Reg == "ESI":
				cnt1 = objs[o].listOP_BaseLeaESI.__len__()
			if Reg == "EDI":
				cnt1 = objs[o].listOP_BaseLeaEDI.__len__()
			if Reg == "ESP":
				cnt1 = objs[o].listOP_BaseLeaESP.__len__()
			if Reg == "EBP":
				cnt1 = objs[o].listOP_BaseLeaEBP.__len__()
			for i in range (cnt1):
				#print "\n@Lea^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^\n"
				#print >> f, "@Lea*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"


				addy =0
				cnt = 0   #
				num = 0
				if Reg == "ALL":
					addy = objs[o].listOP_BaseLea[i]
					cnt = objs[o].listOP_BaseLea_CNT[i]
					num = objs[o].listOP_BaseLea_NumOps[i]
					mod = objs[o].listOP_BaseLea_Module[i]
				if Reg == "EAX":
					addy = objs[o].listOP_BaseLeaEAX[i]
					cnt = objs[o].listOP_BaseLeaEAX_CNT[i]
					num = objs[o].listOP_BaseLeaEAX_NumOps[i]
					mod = objs[o].listOP_BaseLeaEAX_Module[i]
				if Reg == "EBX":
					addy = objs[o].listOP_BaseLeaEBX[i]
					cnt = objs[o].listOP_BaseLeaEBX_CNT[i]
					num = objs[o].listOP_BaseLeaEBX_NumOps[i]
					mod = objs[o].listOP_BaseLeaEBX_Module[i]
				if Reg == "ECX":
					addy = objs[o].listOP_BaseLeaECX[i]
					cnt = objs[o].listOP_BaseLeaECX_CNT[i]
					num = objs[o].listOP_BaseLeaECX_NumOps[i]
					mod = objs[o].listOP_BaseLeaECX_Module[i]
				if Reg == "EDX":
					addy = objs[o].listOP_BaseLeaEDX[i]
					cnt = objs[o].listOP_BaseLeaEDX_CNT[i]
					num = objs[o].listOP_BaseLeaEDX_NumOps[i]
					mod = objs[o].listOP_BaseLeaEDX_Module[i]
				if Reg == "ESI":
					addy = objs[o].listOP_BaseLeaESI[i]
					cnt = objs[o].listOP_BaseLeaESI_CNT[i]
					num = objs[o].listOP_BaseLeaESI_NumOps[i]
					mod = objs[o].listOP_BaseLeaESI_Module[i]
				if Reg == "EDI":
					addy = objs[o].listOP_BaseLeaEDI[i]
					cnt = objs[o].listOP_BaseLeaEDI_CNT[i]
					num = objs[o].listOP_BaseLeaEDI_NumOps[i]
					mod = objs[o].listOP_BaseLeaEDI_Module[i]
				if Reg == "EBP":
					addy = objs[o].listOP_BaseLeaEBP[i]
					cnt = objs[o].listOP_BaseLeaEBP_CNT[i]
					num = objs[o].listOP_BaseLeaEBP_NumOps[i]
					mod = objs[o].listOP_BaseLeaEBP_Module[i]
				if Reg == "ESP":
					addy = objs[o].listOP_BaseLeaESP[i]
					cnt = objs[o].listOP_BaseLeaESP_CNT[i]
					num = objs[o].listOP_BaseLeaESP_NumOps[i]
					mod = objs[o].listOP_BaseLeaESP_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if cnt1 > 0:
				#out = "# LEA " + str(Reg) + " " + str(mod) + " total: " + str(cnt1) 
				temp.append(out)
			total = total + cnt1	
			o = o + 1
			clearGOuts()
		for out in temp:
			#print out
			pass#print >> f, out
		out = "JOP ROCKET"#"# Grand total LEA "  + str(Reg) + " : " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)

def printlistOP_Push(NumOpsDis, Reg):
	global o
	idval = 1
	clearHashChecker()
	while os.path.exists("%s-PUSH_OP_%s-%s.txt" % (peName, Reg, idval)):
	    idval += 1
	filename = peName +"-PUSH_OP_" + Reg + "-" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		i=0
		temp = []
		total = 0
		for obj in objs:
			if Reg == "ALL":
				cnt1 = objs[o].listOP_BasePush.__len__()

			if Reg == "EAX":
				cnt1 = objs[o].listOP_BasePushEAX.__len__()
			if Reg == "EBX":
				cnt1 = objs[o].listOP_BasePushEBX.__len__()
			if Reg == "ECX":
				cnt1 = objs[o].listOP_BasePushECX.__len__()
			if Reg == "EDX":
				cnt1 = objs[o].listOP_BasePushEDX.__len__()
			if Reg == "ESI":
				cnt1 = objs[o].listOP_BasePushESI.__len__()
			if Reg == "EDI":
				cnt1 = objs[o].listOP_BasePushEDI.__len__()
			if Reg == "ESP":
				cnt1 = objs[o].listOP_BasePushESP.__len__()
			if Reg == "EBP":
				cnt1 = objs[o].listOP_BasePushEBP.__len__()
			for i in range (cnt1):
				#print "\n@PUSH: ^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^\n"
				#print >> f, "@PUSH: ^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"


				addy =0
				cnt = 0   #
				num = 0
				if Reg == "ALL":
					addy = objs[o].listOP_BasePush[i]
					cnt = objs[o].listOP_BasePush_CNT[i]
					num = objs[o].listOP_BasePush_NumOps[i]
					mod = objs[o].listOP_BasePush_Module[i]
				if Reg == "EAX":
					addy = objs[o].listOP_BasePushEAX[i]
					cnt = objs[o].listOP_BasePushEAX_CNT[i]
					num = objs[o].listOP_BasePushEAX_NumOps[i]
					mod = objs[o].listOP_BasePushEAX_Module[i]
				if Reg == "EBX":
					addy = objs[o].listOP_BasePushEBX[i]
					cnt = objs[o].listOP_BasePushEBX_CNT[i]
					num = objs[o].listOP_BasePushEBX_NumOps[i]
					mod = objs[o].listOP_BasePushEBX_Module[i]
				if Reg == "ECX":
					addy = objs[o].listOP_BasePushECX[i]
					cnt = objs[o].listOP_BasePushECX_CNT[i]
					num = objs[o].listOP_BasePushECX_NumOps[i]
					mod = objs[o].listOP_BasePushECX_Module[i]
				if Reg == "EDX":
					addy = objs[o].listOP_BasePushEDX[i]
					cnt = objs[o].listOP_BasePushEDX_CNT[i]
					num = objs[o].listOP_BasePushEDX_NumOps[i]
					mod = objs[o].listOP_BasePushEDX_Module[i]
				if Reg == "ESI":
					addy = objs[o].listOP_BasePushESI[i]
					cnt = objs[o].listOP_BasePushESI_CNT[i]
					num = objs[o].listOP_BasePushESI_NumOps[i]
					mod = objs[o].listOP_BasePushESI_Module[i]
				if Reg == "EDI":
					addy = objs[o].listOP_BasePushEDI[i]
					cnt = objs[o].listOP_BasePushEDI_CNT[i]
					num = objs[o].listOP_BasePushEDI_NumOps[i]
					mod = objs[o].listOP_BasePushEDI_Module[i]
				if Reg == "EBP":
					addy = objs[o].listOP_BasePushEBP[i]
					cnt = objs[o].listOP_BasePushEBP_CNT[i]
					num = objs[o].listOP_BasePushEBP_NumOps[i]
					mod = objs[o].listOP_BasePushEBP_Module[i]
				if Reg == "ESP":
					addy = objs[o].listOP_BasePushESP[i]
					cnt = objs[o].listOP_BasePushESP_CNT[i]
					num = objs[o].listOP_BasePushESP_NumOps[i]
					mod = objs[o].listOP_BasePushESP_Module[i]
				
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if cnt1 > 0:
				#out = "# PUSH " + str(Reg) + " " + str(mod) + " total: " + str(cnt1) 
				temp.append(out)
			total = total + cnt1	
			o = o + 1
			clearGOuts()
		for out in temp:
			#print out
			pass#print >> f, out
		out = "JOP ROCKET"#"# Grand total PUSH "  + str(Reg) + " : " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)

def printlistOP_Pop(NumOpsDis, Reg):
	global o
	idval = 1
	clearHashChecker()
	while os.path.exists("%s-POP_OP_%s-%s.txt" % (peName, Reg, idval)):
	    idval += 1
	filename = peName +"-POP_OP_" + Reg + "-" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		i=0
		temp = []
		total = 0
		for obj in objs:
			if Reg == "ALL":
				cnt1 = objs[o].listOP_BasePop.__len__()

			if Reg == "EAX":
				cnt1 = objs[o].listOP_BasePopEAX.__len__()
			if Reg == "EBX":
				cnt1 = objs[o].listOP_BasePopEBX.__len__()
			if Reg == "ECX":
				cnt1 = objs[o].listOP_BasePopECX.__len__()
			if Reg == "EDX":
				cnt1 = objs[o].listOP_BasePopEDX.__len__()
			if Reg == "ESI":
				cnt1 = objs[o].listOP_BasePopESI.__len__()
			if Reg == "EDI":
				cnt1 = objs[o].listOP_BasePopEDI.__len__()
			if Reg == "ESP":
				cnt1 = objs[o].listOP_BasePopESP.__len__()
			if Reg == "EBP":
				cnt1 = objs[o].listOP_BasePopEBP.__len__()
			for i in range (cnt1):
				#print "\n@POP: ^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^\n"
				#print >> f, "@POP: ^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"


				addy =0
				cnt = 0   #
				num = 0
				if Reg == "ALL":
					addy = objs[o].listOP_BasePop[i]
					cnt = objs[o].listOP_BasePop_CNT[i]
					num = objs[o].listOP_BasePop_NumOps[i]
					mod = objs[o].listOP_BasePop_Module[i]
				if Reg == "EAX":
					addy = objs[o].listOP_BasePopEAX[i]
					cnt = objs[o].listOP_BasePopEAX_CNT[i]
					num = objs[o].listOP_BasePopEAX_NumOps[i]
					mod = objs[o].listOP_BasePopEAX_Module[i]
				if Reg == "EBX":
					addy = objs[o].listOP_BasePopEBX[i]
					cnt = objs[o].listOP_BasePopEBX_CNT[i]
					num = objs[o].listOP_BasePopEBX_NumOps[i]
					mod = objs[o].listOP_BasePopEBX_Module[i]
				if Reg == "ECX":
					addy = objs[o].listOP_BasePopECX[i]
					cnt = objs[o].listOP_BasePopECX_CNT[i]
					num = objs[o].listOP_BasePopECX_NumOps[i]
					mod = objs[o].listOP_BasePopECX_Module[i]
				if Reg == "EDX":
					addy = objs[o].listOP_BasePopEDX[i]
					cnt = objs[o].listOP_BasePopEDX_CNT[i]
					num = objs[o].listOP_BasePopEDX_NumOps[i]
					mod = objs[o].listOP_BasePopEDX_Module[i]
				if Reg == "ESI":
					addy = objs[o].listOP_BasePopESI[i]
					cnt = objs[o].listOP_BasePopESI_CNT[i]
					num = objs[o].listOP_BasePopESI_NumOps[i]
					mod = objs[o].listOP_BasePopESI_Module[i]
				if Reg == "EDI":
					addy = objs[o].listOP_BasePopEDI[i]
					cnt = objs[o].listOP_BasePopEDI_CNT[i]
					num = objs[o].listOP_BasePopEDI_NumOps[i]
					mod = objs[o].listOP_BasePopEDI_Module[i]
				if Reg == "EBP":
					addy = objs[o].listOP_BasePopEBP[i]
					cnt = objs[o].listOP_BasePopEBP_CNT[i]
					num = objs[o].listOP_BasePopEBP_NumOps[i]
					mod = objs[o].listOP_BasePopEBP_Module[i]
				if Reg == "ESP":
					addy = objs[o].listOP_BasePopESP[i]
					cnt = objs[o].listOP_BasePopESP_CNT[i]
					num = objs[o].listOP_BasePopESP_NumOps[i]
					mod = objs[o].listOP_BasePopESP_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if cnt1 > 0:
				#out = "# POP " + str(Reg) + " " + str(mod) + " total: " + str(cnt1) 
				temp.append(out)
			total = total + cnt1	
			o = o + 1
			clearGOuts()
		for out in temp:
			#print out
			pass#print >> f, out
		out = "JOP ROCKET"#"# Grand total POP "  + str(Reg) + " : " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)

def printlistOP_Inc(NumOpsDis, Reg):
	global o
	idval = 1
	clearHashChecker()
	while os.path.exists("%s-INC_OP_%s-%s.txt" % (peName, Reg, idval)):
	    idval += 1
	filename = peName +"-INC_OP_" + Reg + "-" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		i=0
		temp = []
		total = 0
		for obj in objs:
			if Reg == "ALL":
				cnt1 = objs[o].listOP_BaseInc.__len__()

			if Reg == "EAX":
				cnt1 = objs[o].listOP_BaseIncEAX.__len__()
			if Reg == "EBX":
				cnt1 = objs[o].listOP_BaseIncEBX.__len__()
			if Reg == "ECX":
				cnt1 = objs[o].listOP_BaseIncECX.__len__()
			if Reg == "EDX":
				cnt1 = objs[o].listOP_BaseIncEDX.__len__()
			if Reg == "ESI":
				cnt1 = objs[o].listOP_BaseIncESI.__len__()
			if Reg == "EDI":
				cnt1 = objs[o].listOP_BaseIncEDI.__len__()
			if Reg == "ESP":
				cnt1 = objs[o].listOP_BaseIncESP.__len__()
			if Reg == "EBP":
				cnt1 = objs[o].listOP_BaseIncEBP.__len__()
			for i in range (cnt1):
				#print "\n@INC: ^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^\n"
				#print >> f, "@INC: ^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"


				addy =0
				cnt = 0   #
				num = 0
				if Reg == "ALL":
					addy = objs[o].listOP_BaseInc[i]
					cnt = objs[o].listOP_BaseInc_CNT[i]
					num = objs[o].listOP_BaseInc_NumOps[i]
					mod = objs[o].listOP_BaseInc_Module[i]
				if Reg == "EAX":
					addy = objs[o].listOP_BaseIncEAX[i]
					cnt = objs[o].listOP_BaseIncEAX_CNT[i]
					num = objs[o].listOP_BaseIncEAX_NumOps[i]
					mod = objs[o].listOP_BaseIncEAX_Module[i]
				if Reg == "EBX":
					addy = objs[o].listOP_BaseIncEBX[i]
					cnt = objs[o].listOP_BaseIncEBX_CNT[i]
					num = objs[o].listOP_BaseIncEBX_NumOps[i]
					mod = objs[o].listOP_BaseIncEBX_Module[i]
				if Reg == "ECX":
					addy = objs[o].listOP_BaseIncECX[i]
					cnt = objs[o].listOP_BaseIncECX_CNT[i]
					num = objs[o].listOP_BaseIncECX_NumOps[i]
					mod = objs[o].listOP_BaseIncECX_Module[i]
				if Reg == "EDX":
					addy = objs[o].listOP_BaseIncEDX[i]
					cnt = objs[o].listOP_BaseIncEDX_CNT[i]
					num = objs[o].listOP_BaseIncEDX_NumOps[i]
					mod = objs[o].listOP_BaseIncEDX_Module[i]
				if Reg == "ESI":
					addy = objs[o].listOP_BaseIncESI[i]
					cnt = objs[o].listOP_BaseIncESI_CNT[i]
					num = objs[o].listOP_BaseIncESI_NumOps[i]
					mod = objs[o].listOP_BaseIncESI_Module[i]
				if Reg == "EDI":
					addy = objs[o].listOP_BaseIncEDI[i]
					cnt = objs[o].listOP_BaseIncEDI_CNT[i]
					num = objs[o].listOP_BaseIncEDI_NumOps[i]
					mod = objs[o].listOP_BaseIncEDI_Module[i]
				if Reg == "EBP":
					addy = objs[o].listOP_BaseIncEBP[i]
					cnt = objs[o].listOP_BaseIncEBP_CNT[i]
					num = objs[o].listOP_BaseIncEBP_NumOps[i]
					mod = objs[o].listOP_BaseIncEBP_Module[i]
				if Reg == "ESP":
					addy = objs[o].listOP_BaseIncESP[i]
					cnt = objs[o].listOP_BaseIncESP_CNT[i]
					num = objs[o].listOP_BaseIncESP_NumOps[i]
					mod = objs[o].listOP_BaseIncESP_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if cnt1 > 0:
				out = "# INC " + str(Reg) + " " + str(mod) + " total: " + str(cnt1) 
				temp.append(out)
			total = total + cnt1	
			o = o + 1
			clearGOuts()
		for out in temp:
			#print out
			pass#print >> f, out
		out = "JOP ROCKET"#"# Grand total INC "  + str(Reg) + " : " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)

def printlistOP_Dec(NumOpsDis, Reg):
	global o
	idval = 1
	clearHashChecker()
	while os.path.exists("%s-DEC_OP_%s-%s.txt" % (peName, Reg, idval)):
	    idval += 1
	filename = peName +"-DEC_OP_" + Reg + "-" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		i=0
		temp = []
		total = 0
		for obj in objs:
			if Reg == "ALL":
				cnt1 = objs[o].listOP_BaseDec.__len__()

			if Reg == "EAX":
				cnt1 = objs[o].listOP_BaseDecEAX.__len__()
			if Reg == "EBX":
				cnt1 = objs[o].listOP_BaseDecEBX.__len__()
			if Reg == "ECX":
				cnt1 = objs[o].listOP_BaseDecECX.__len__()
			if Reg == "EDX":
				cnt1 = objs[o].listOP_BaseDecEDX.__len__()
			if Reg == "ESI":
				cnt1 = objs[o].listOP_BaseDecESI.__len__()
			if Reg == "EDI":
				cnt1 = objs[o].listOP_BaseDecEDI.__len__()
			if Reg == "ESP":
				cnt1 = objs[o].listOP_BaseDecESP.__len__()
			if Reg == "EBP":
				cnt1 = objs[o].listOP_BaseDecEBP.__len__()
			for i in range (cnt1):
				#print "\n@DEC: ^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^\n"
				#print >> f, "@DEC: ^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"


				addy =0
				cnt = 0   #
				num = 0
				if Reg == "ALL":
					addy = objs[o].listOP_BaseDec[i]
					cnt = objs[o].listOP_BaseDec_CNT[i]
					num = objs[o].listOP_BaseDec_NumOps[i]
					mod = objs[o].listOP_BaseDec_Module[i]
				if Reg == "EAX":
					addy = objs[o].listOP_BaseDecEAX[i]
					cnt = objs[o].listOP_BaseDecEAX_CNT[i]
					num = objs[o].listOP_BaseDecEAX_NumOps[i]
					mod = objs[o].listOP_BaseDecEAX_Module[i]
				if Reg == "EBX":
					addy = objs[o].listOP_BaseDecEBX[i]
					cnt = objs[o].listOP_BaseDecEBX_CNT[i]
					num = objs[o].listOP_BaseDecEBX_NumOps[i]
					mod = objs[o].listOP_BaseDecEBX_Module[i]
				if Reg == "ECX":
					addy = objs[o].listOP_BaseDecECX[i]
					cnt = objs[o].listOP_BaseDecECX_CNT[i]
					num = objs[o].listOP_BaseDecECX_NumOps[i]
					mod = objs[o].listOP_BaseDecECX_Module[i]
				if Reg == "EDX":
					addy = objs[o].listOP_BaseDecEDX[i]
					cnt = objs[o].listOP_BaseDecEDX_CNT[i]
					num = objs[o].listOP_BaseDecEDX_NumOps[i]
					mod = objs[o].listOP_BaseDecEDX_Module[i]
				if Reg == "ESI":
					addy = objs[o].listOP_BaseDecESI[i]
					cnt = objs[o].listOP_BaseDecESI_CNT[i]
					num = objs[o].listOP_BaseDecESI_NumOps[i]
					mod = objs[o].listOP_BaseDecESI_Module[i]
				if Reg == "EDI":
					addy = objs[o].listOP_BaseDecEDI[i]
					cnt = objs[o].listOP_BaseDecEDI_CNT[i]
					num = objs[o].listOP_BaseDecEDI_NumOps[i]
					mod = objs[o].listOP_BaseDecEDI_Module[i]
				if Reg == "EBP":
					addy = objs[o].listOP_BaseDecEBP[i]
					cnt = objs[o].listOP_BaseDecEBP_CNT[i]
					num = objs[o].listOP_BaseDecEBP_NumOps[i]
					mod = objs[o].listOP_BaseDecEBP_Module[i]
				if Reg == "ESP":
					addy = objs[o].listOP_BaseDecESP[i]
					cnt = objs[o].listOP_BaseDecESP_CNT[i]
					num = objs[o].listOP_BaseDecESP_NumOps[i]
					mod = objs[o].listOP_BaseDecESP_Module[i]
				
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if cnt1 > 0:
				out = "# DEC " + str(Reg) + " " + str(mod) + " total: " + str(cnt1) 
				temp.append(out)
			total = total + cnt1	
			o = o + 1
			clearGOuts()
		for out in temp:
			#print out
			pass#print >> f, out
		out = "JOP ROCKET"#"# Grand total DEC "  + str(Reg) + " : " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)


def printlistOP_Xchg(NumOpsDis, Reg):
	global o
	idval = 1
	clearHashChecker()
	while os.path.exists("%s-XCHG_OP_%s-%s.txt" % (peName, Reg, idval)):
	    idval += 1
	filename = peName +"-XCHG_OP_" + Reg + "-" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		i=0
		temp = []
		total = 0
		for obj in objs:
			if Reg == "ALL":
				cnt1 = objs[o].listOP_BaseXchg.__len__()

			if Reg == "EAX":
				cnt1 = objs[o].listOP_BaseXchgEAX.__len__()
			if Reg == "EBX":
				cnt1 = objs[o].listOP_BaseXchgEBX.__len__()
			if Reg == "ECX":
				cnt1 = objs[o].listOP_BaseXchgECX.__len__()
			if Reg == "EDX":
				cnt1 = objs[o].listOP_BaseXchgEDX.__len__()
			if Reg == "ESI":
				cnt1 = objs[o].listOP_BaseXchgESI.__len__()
			if Reg == "EDI":
				cnt1 = objs[o].listOP_BaseXchgEDI.__len__()
			if Reg == "ESP":
				cnt1 = objs[o].listOP_BaseXchgESP.__len__()
			if Reg == "EBP":
				cnt1 = objs[o].listOP_BaseXchgEBP.__len__()
			for i in range (cnt1):
				#print "\n@XCHG: ^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^\n"
				#print >> f, "@XCHG: ^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"


				addy =0
				cnt = 0   #
				num = 0
				if Reg == "ALL":
					addy = objs[o].listOP_BaseXchg[i]
					cnt = objs[o].listOP_BaseXchg_CNT[i]
					num = objs[o].listOP_BaseXchg_NumOps[i]
					mod = objs[o].listOP_BaseXchg_Module[i]
				if Reg == "EAX":
					addy = objs[o].listOP_BaseXchgEAX[i]
					cnt = objs[o].listOP_BaseXchgEAX_CNT[i]
					num = objs[o].listOP_BaseXchgEAX_NumOps[i]
					mod = objs[o].listOP_BaseXchgEAX_Module[i]
				if Reg == "EBX":
					addy = objs[o].listOP_BaseXchgEBX[i]
					cnt = objs[o].listOP_BaseXchgEBX_CNT[i]
					num = objs[o].listOP_BaseXchgEBX_NumOps[i]
					mod = objs[o].listOP_BaseXchgEBX_Module[i]
				if Reg == "ECX":
					addy = objs[o].listOP_BaseXchgECX[i]
					cnt = objs[o].listOP_BaseXchgECX_CNT[i]
					num = objs[o].listOP_BaseXchgECX_NumOps[i]
					mod = objs[o].listOP_BaseXchgECX_Module[i]
				if Reg == "EDX":
					addy = objs[o].listOP_BaseXchgEDX[i]
					cnt = objs[o].listOP_BaseXchgEDX_CNT[i]
					num = objs[o].listOP_BaseXchgEDX_NumOps[i]
					mod = objs[o].listOP_BaseXchgEDX_Module[i]
				if Reg == "ESI":
					addy = objs[o].listOP_BaseXchgESI[i]
					cnt = objs[o].listOP_BaseXchgESI_CNT[i]
					num = objs[o].listOP_BaseXchgESI_NumOps[i]
					mod = objs[o].listOP_BaseXchgESI_Module[i]
				if Reg == "EDI":
					addy = objs[o].listOP_BaseXchgEDI[i]
					cnt = objs[o].listOP_BaseXchgEDI_CNT[i]
					num = objs[o].listOP_BaseXchgEDI_NumOps[i]
					mod = objs[o].listOP_BaseXchgEDI_Module[i]
				if Reg == "EBP":
					addy = objs[o].listOP_BaseXchgEBP[i]
					cnt = objs[o].listOP_BaseXchgEBP_CNT[i]
					num = objs[o].listOP_BaseXchgEBP_NumOps[i]
					mod = objs[o].listOP_BaseXchgEBP_Module[i]
				if Reg == "ESP":
					addy = objs[o].listOP_BaseXchgESP[i]
					cnt = objs[o].listOP_BaseXchgESP_CNT[i]
					num = objs[o].listOP_BaseXchgESP_NumOps[i]
					mod = objs[o].listOP_BaseXchgESP_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if cnt1 > 0:
			#	out = "# XCHG " + str(Reg) + " " + str(mod) + " total: " + str(cnt1) 
				temp.append(out)
			total = total + cnt1	
			o = o + 1
			clearGOuts()
		for out in temp:
			#print out
			pass#print >> f, out
		out = "JOP ROCKET"#"# Grand total XCHG "  + str(Reg) + " : " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)

def printlistOP_ShiftLeft(NumOpsDis, Reg):
	global o
	idval = 1
	clearHashChecker()
	while os.path.exists("%s-SHIFT_LEFT_%s-%s.txt" % (peName, Reg, idval)):
	    idval += 1
	filename = peName +"-SHIFT_LEFT_" + Reg + "-" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		i=0
		temp = []
		total = 0
		for obj in objs:
			if Reg != "0":
				cnt1 = objs[o].listOP_BaseShiftLeft.__len__()

			for i in range (cnt1):
				#print "\n@Shift_Left: ^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^\n"
				#print >> f, "@Shift_Left: ^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"

				addy =0
				cnt = 0   #
				num = 0
				if Reg != "0":
					addy = objs[o].listOP_BaseShiftLeft[i]
					cnt = objs[o].listOP_BaseShiftLeft_CNT[i]
					num = objs[o].listOP_BaseShiftLeft_NumOps[i]
					mod = objs[o].listOP_BaseShiftLeft_Module[i]
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if cnt1 > 0:
				#out = "# SHIFT LEFT " + str(Reg) + " " + str(mod) + " total: " + str(cnt1) 
				temp.append(out)
			total = total + cnt1	
			o = o + 1
			clearGOuts()
		for out in temp:
			#print out
			pass#print >> f, out
		out = "JOP ROCKET"#"# Grand total SHIFT LEFT "  + str(Reg) + " : " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)

def printlistOP_ShiftRight(NumOpsDis, Reg):
	global o
	idval = 1
	clearHashChecker()
	while os.path.exists("%s-SHIFT_RIGHT_OP_%s-%s.txt" % (peName, Reg, idval)):
	    idval += 1
	filename = peName +"-SHIFT_RIGHT_OP_" + Reg + "-" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		i=0
		temp = []
		total = 0
		for obj in objs:
			if Reg != "0":
				cnt1 = objs[o].listOP_BaseShiftRight.__len__()
			for i in range (cnt1):
				#print "\n@SHIFT_RIGHT: ^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^\n"
				#print >> f, "@SHIFT_RIGHT: ^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"


				addy =0
				cnt = 0   #
				num = 0
				if Reg != "0":
					addy = objs[o].listOP_BaseShiftRight[i]
					cnt = objs[o].listOP_BaseShiftRight_CNT[i]
					num = objs[o].listOP_BaseShiftRight_NumOps[i]
					mod = objs[o].listOP_BaseShiftRight_Module[i]
				
				
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if cnt1 > 0:
				#out = "# SHIFT RIGHT " + str(Reg) + " " + str(mod) + " total: " + str(cnt1) 
				temp.append(out)
			total = total + cnt1	
			o = o + 1
			clearGOuts()
		for out in temp:
			#print out
			pass#print >> f, out
		out = "JOP ROCKET"#"# Grand total SHIFT RIGHT "  + str(Reg) + " : " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)

def printlistOP_RotRight(NumOpsDis, Reg):
	global o
	idval = 1
	clearHashChecker()
	while os.path.exists("%s-ROTATE_RIGHT_OP_%s-%s.txt" % (peName, Reg, idval)):
	    idval += 1
	filename = peName +"-ROTATE_RIGHT_OP_" + Reg + "-" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		i=0
		temp = []
		total = 0
		for obj in objs:
			if Reg != "0":
				cnt1 = objs[o].listOP_BaseRotRight.__len__()
			for i in range (cnt1):
				#print "\n@ROTATE_RIGHT: ^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^\n"
				#print >> f, "@ROTATE_RIGHT: ^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"

				addy =0
				cnt = 0   #
				num = 0
				if Reg != "0":
					addy = objs[o].listOP_BaseRotRight[i]
					cnt = objs[o].listOP_BaseRotRight_CNT[i]
					num = objs[o].listOP_BaseRotRight_NumOps[i]
					mod = objs[o].listOP_BaseRotRight_Module[i]
				
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if cnt1 > 0:
				#out = "# ROTATE RIGHT " + str(Reg) + " " + str(mod) + " total: " + str(cnt1) 
				temp.append(out)
			total = total + cnt1	
			o = o + 1
			clearGOuts()
		for out in temp:
			#print out
			pass#print >> f, out
		out = "JOP ROCKET"#"# Grand total ROTATE RIGHT "  + str(Reg) + " : " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)

def printlistOP_RotLeft(NumOpsDis, Reg):
	global o
	idval = 1
	clearHashChecker()
	while os.path.exists("%s-ROTATE_LEFT_OP_%s-%s.txt" % (peName, Reg, idval)):
	    idval += 1
	filename = peName +"-ROTATE_LEFT_OP_" + Reg + "-" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		i=0
		temp = []
		total = 0
		for obj in objs:
			if Reg != "0":
				cnt1 = objs[o].listOP_BaseRotLeft.__len__()

			for i in range (cnt1):
				#print "\n@ROTATE_LEFT: ^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^\n"
				#print >> f,"@ROTATE_LEFT: ^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"


				addy =0
				cnt = 0   #
				num = 0
				if Reg != "0":
					addy = objs[o].listOP_BaseRotLeft[i]
					cnt = objs[o].listOP_BaseRotLeft_CNT[i]
					num = objs[o].listOP_BaseRotLeft_NumOps[i]
					mod = objs[o].listOP_BaseRotLeft_Module[i]
				
				out = "Ops: " + str(num) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, num, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if cnt1 > 0:
				#out = "# ROTATE LEFT " + str(Reg) + " " + str(mod) + " total: " + str(cnt1) 
				temp.append(out)
			total = total + cnt1	
			o = o + 1
			clearGOuts()
		for out in temp:
			#print out
			pass#print >> f, out
		out = "JOP ROCKET"#"# Grand total ROTATE LEFT "  + str(Reg) + " : " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)


#now3
def get_Dispatcher_G(NumOpsDis, howDeep, Reg):
	global o
	for obj in objs:
		t=0
		if Reg == "EAX":
			for v in objs[o].listOP_JMP_PTR_EAX:
				findDG_EAX(objs[o].listOP_JMP_PTR_EAX[t], objs[o].listOP_JMP_PTR_EAX_CNT[t], objs[o].listOP_JMP_PTR_EAX_NumOps[t], objs[o].listOP_JMP_PTR_EAX_Module[t],linesGoBack, howDeep)
				t=t+1
			t=0
			for v in objs[o].listOP_CALL_PTR_EAX:
				findDG_EAX(objs[o].listOP_CALL_PTR_EAX[t], objs[o].listOP_CALL_PTR_EAX_CNT[t], objs[o].listOP_CALL_PTR_EAX_NumOps[t], objs[o].listOP_CALL_PTR_EAX_Module[t],linesGoBack, howDeep)
				t=t+1
			t=0
		if Reg == "EBX":
			for v in objs[o].listOP_JMP_PTR_EBX:
				findDG_EBX(objs[o].listOP_JMP_PTR_EBX[t], objs[o].listOP_JMP_PTR_EBX_CNT[t], objs[o].listOP_JMP_PTR_EBX_NumOps[t], objs[o].listOP_JMP_PTR_EBX_Module[t],linesGoBack, howDeep)  
				t=t+1
			t=0
			for v in objs[o].listOP_CALL_PTR_EBX:
				findDG_EBX(objs[o].listOP_CALL_PTR_EBX[t], objs[o].listOP_CALL_PTR_EBX_CNT[t], objs[o].listOP_CALL_PTR_EBX_NumOps[t], objs[o].listOP_CALL_PTR_EBX_Module[t],linesGoBack, howDeep)  
				t=t+1
			t=0
		if Reg == "ECX":
			for v in objs[o].listOP_JMP_PTR_ECX:
				findDG_ECX(objs[o].listOP_JMP_PTR_ECX[t], objs[o].listOP_JMP_PTR_ECX_CNT[t], objs[o].listOP_JMP_PTR_ECX_NumOps[t], objs[o].listOP_JMP_PTR_ECX_Module[t],linesGoBack, howDeep)  
				t=t+1
			t=0
			for v in objs[o].listOP_CALL_PTR_ECX:
				findDG_ECX(objs[o].listOP_CALL_PTR_ECX[t], objs[o].listOP_CALL_PTR_ECX_CNT[t], objs[o].listOP_CALL_PTR_ECX_NumOps[t], objs[o].listOP_CALL_PTR_ECX_Module[t],linesGoBack, howDeep)
				t=t+1
			t=0
		if Reg == "EDX":
			for v in objs[o].listOP_JMP_PTR_EDX:
				findDG_EDX(objs[o].listOP_JMP_PTR_EDX[t], objs[o].listOP_JMP_PTR_EDX_CNT[t], objs[o].listOP_JMP_PTR_EDX_NumOps[t], objs[o].listOP_JMP_PTR_EDX_Module[t],linesGoBack, howDeep)  
				t=t+1
			t=0
			for v in objs[o].listOP_CALL_PTR_EDX:
				findDG_EDX(objs[o].listOP_CALL_PTR_EDX[t], objs[o].listOP_CALL_PTR_EDX_CNT[t], objs[o].listOP_CALL_PTR_EDX_NumOps[t], objs[o].listOP_CALL_PTR_EDX_Module[t],linesGoBack, howDeep)
				t=t+1
			t=0
		if Reg == "EDI":
			for v in objs[o].listOP_JMP_PTR_EDI:
				findDG_EDI(objs[o].listOP_JMP_PTR_EDI[t], objs[o].listOP_JMP_PTR_EDI_CNT[t], objs[o].listOP_JMP_PTR_EDI_NumOps[t], objs[o].listOP_JMP_PTR_EDI_Module[t],linesGoBack, howDeep)  
				t=t+1
			t=0
			for v in objs[o].listOP_CALL_PTR_EDI:
				findDG_EDI(objs[o].listOP_CALL_PTR_EDI[t], objs[o].listOP_CALL_PTR_EDI_CNT[t], objs[o].listOP_CALL_PTR_EDI_NumOps[t], objs[o].listOP_CALL_PTR_EDI_Module[t],linesGoBack, howDeep)  
				t=t+1
			t=0
		if Reg == "ESI":
			for v in objs[o].listOP_JMP_PTR_ESI:
				findDG_ESI(objs[o].listOP_JMP_PTR_ESI[t], objs[o].listOP_JMP_PTR_ESI_CNT[t], objs[o].listOP_JMP_PTR_ESI_NumOps[t], objs[o].listOP_JMP_PTR_ESI_Module[t],linesGoBack, howDeep)  
				t=t+1
			t=0
			for v in objs[o].listOP_CALL_PTR_ESI:
				findDG_ESI(objs[o].listOP_CALL_PTR_ESI[t], objs[o].listOP_CALL_PTR_ESI_CNT[t], objs[o].listOP_CALL_PTR_ESI_NumOps[t], objs[o].listOP_CALL_PTR_ESI_Module[t],linesGoBack, howDeep)  
				t=t+1
			t=0
		if Reg == "EBP":
			for v in objs[o].listOP_JMP_PTR_EBP:
				findDG_EBP(objs[o].listOP_JMP_PTR_EBP[t], objs[o].listOP_JMP_PTR_EBP_CNT[t], objs[o].listOP_JMP_PTR_EBP_NumOps[t], objs[o].listOP_JMP_PTR_EBP_Module[t],linesGoBack, howDeep)  
				t=t+1
			t=0
			for v in objs[o].listOP_CALL_PTR_EBP:
				findDG_EBP(objs[o].listOP_CALL_PTR_EBP[t], objs[o].listOP_CALL_PTR_EBP_CNT[t], objs[o].listOP_CALL_PTR_EBP_NumOps[t], objs[o].listOP_CALL_PTR_EBP_Module[t],linesGoBack, howDeep)  
				t=t+1
			t=0
		
		if Reg == "ESP":
			for v in objs[o].listOP_JMP_PTR_ESP:
				findDG_ESP(objs[o].listOP_JMP_PTR_ESP[t], objs[o].listOP_JMP_PTR_ESP_CNT[t], objs[o].listOP_JMP_PTR_ESP_NumOps[t], objs[o].listOP_JMP_PTR_ESP_Module[t],linesGoBack, howDeep)  
				t=t+1
			t=0
			for v in objs[o].listOP_CALL_PTR_ESP:
				findDG_ESP(objs[o].listOP_CALL_PTR_ESP[t], objs[o].listOP_CALL_PTR_ESP_CNT[t], objs[o].listOP_CALL_PTR_ESP_NumOps[t], objs[o].listOP_CALL_PTR_ESP_Module[t],linesGoBack, howDeep)  
				t=t+1
			t=0
		clearGOuts()
		o = o + 1
	o = 0

def printListDG_EAX(NumOpsDis):	
	global o
	clearHashChecker()
	idval = 1
	while os.path.exists("%s-DG_DISPATCHER_EAX_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-DG_DISPATCHER_EAX_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		i=0
		temp = []
		total = 0
		for obj in objs:
			num = objs[o].listOP_BaseDG_Module_EAX.__len__()  #was cnt
			for i in range (num): #ibid
				#print "\n*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^\n"
				
				
				#counterShow()
				addy =0x00
				cnt = 0    #
				addy = objs[o].listOP_BaseDG_EAX[i]
				cnt = objs[o].listOP_BaseDG_CNT_EAX[i]
				nOppsVal = objs[o].listOP_BaseDG_NumOps_EAX[i]
				mod = objs[o].listOP_BaseDG_Module_EAX[i]
				out = "Ops: " + str(nOppsVal) + "\tMod: " + str(mod)
				#print out
				sp()
				
				cat = disHereClean3(addy, cnt, nOppsVal, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if num > 0:
				out = "\nJOP ROCKET" #out = "\nJOP ROCKET" #out = "# Dispatcher Gadgets for EAX "  + str(mod) + " total: " + Ct2()
				temp.append(out)
			total = total + num	
			o = o + 1
		for out in temp:
			#print out
			print >> f, out
		out = ""#out = ""#"# Grand total Dispatcher Gadgets for EAX: " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)

#now9
def printListDG_EBX(NumOpsDis):	
	global o
	clearHashChecker()
	idval = 1
	while os.path.exists("%s-DG_DISPATCHER_EBX_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-DG_DISPATCHER_EBX_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		i=0
		temp = []
		total = 0
		for obj in objs:
			num = objs[o].listOP_BaseDG_Module_EBX.__len__()  #was cnt
			for i in range (num): #ibid
				addy =0x00
				cnt = 0    #
				addy = objs[o].listOP_BaseDG_EBX[i]
				cnt = objs[o].listOP_BaseDG_CNT_EBX[i]
				nOppsVal = objs[o].listOP_BaseDG_NumOps_EBX[i]
				mod = objs[o].listOP_BaseDG_Module_EBX[i]
				out = "Ops: " + str(nOppsVal) + "\tMod: " + str(mod)
				#print out
				sp()
				cat = disHereClean3(addy, cnt, nOppsVal, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			out = "\nJOP ROCKET" #out = "\nJOP ROCKET" #out = "# Dispatcher Gadgets for EBX total: " + str(num)
			if num > 0:
				out = "\nJOP ROCKET" #out = "# Dispatcher Gadgets for EBX "  + str(mod) + " total: " + Ct2()
				temp.append(out)
			total = total + num	
			o = o + 1
		for out in temp:
			#print out
			print >> f, out
		out = ""#out = ""#"# Grand total Dispatcher Gadgets for EBX: " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)

def printListDG_ECX(NumOpsDis):	
	global o
	clearHashChecker()
	idval = 1
	while os.path.exists("%s-DG_DISPATCHER_ECX_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-DG_DISPATCHER_ECX_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		i=0
		temp = []
		total = 0
		for obj in objs:
			num = objs[o].listOP_BaseDG_Module_ECX.__len__()  #was cnt
			for i in range (num): #ibid
				addy =0x00
				cnt = 0    #
				addy = objs[o].listOP_BaseDG_ECX[i]
				cnt = objs[o].listOP_BaseDG_CNT_ECX[i]
				nOppsVal = objs[o].listOP_BaseDG_NumOps_ECX[i]
				mod = objs[o].listOP_BaseDG_Module_ECX[i]
				out = "Ops: " + str(nOppsVal) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, nOppsVal, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if num > 0:
				out = "\nJOP ROCKET" #out = "# Dispatcher Gadgets for ECX "  + str(mod) + " total: " + Ct2()
				temp.append(out)
			total = total + num	
			o = o + 1
		for out in temp:
			#print out
			print >> f, out
		out = ""#out = ""#"# Grand total Dispatcher Gadgets for ECX: " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)

def printListDG_EDX(NumOpsDis):	
	global o
	clearHashChecker()
	idval = 1
	while os.path.exists("%s-DG_DISPATCHER_EDX_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-DG_DISPATCHER_EDX_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		i=0
		temp = []
		total = 0
		for obj in objs:
			num = objs[o].listOP_BaseDG_Module_EDX.__len__()  #was cnt
			for i in range (num): #ibid
				addy =0x00
				cnt = 0    #
				addy = objs[o].listOP_BaseDG_EDX[i]
				cnt = objs[o].listOP_BaseDG_CNT_EDX[i]
				nOppsVal = objs[o].listOP_BaseDG_NumOps_EDX[i]
				mod = objs[o].listOP_BaseDG_Module_EDX[i]
				out = "Ops: " + str(nOppsVal) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, nOppsVal, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if num > 0:
				out = "\nJOP ROCKET" #out = "# Dispatcher Gadgets for EDX "  + str(mod) + " total: " + Ct2()
				temp.append(out)
			total = total + num	
			o = o + 1
		for out in temp:
			#print out
			print >> f, out
		out = ""#out = ""#"# Grand total Dispatcher Gadgets for EDX: " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)

def printListDG_EDI(NumOpsDis):	
	global o
	clearHashChecker()
	idval = 1
	while os.path.exists("%s-DG_DISPATCHER_EDI_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-DG_DISPATCHER_EDI_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		i=0
		temp = []
		total = 0
		for obj in objs:
			num = objs[o].listOP_BaseDG_Module_EDI.__len__()  #was cnt
			for i in range (num): #ibid
				addy =0x00
				cnt = 0    #
				addy = objs[o].listOP_BaseDG_EDI[i]
				cnt = objs[o].listOP_BaseDG_CNT_EDI[i]
				nOppsVal = objs[o].listOP_BaseDG_NumOps_EDI[i]
				mod = objs[o].listOP_BaseDG_Module_EDI[i]
				out = "Ops: " + str(nOppsVal) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, nOppsVal, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if num > 0:
				out = "\nJOP ROCKET" #out = "# Dispatcher Gadgets for EDI "  + str(mod) + " total: " + Ct2()
				temp.append(out)
			total = total + num	
			o = o + 1
		for out in temp:
			#print out
			print >> f, out
		out = ""#out = ""#"# Grand total Dispatcher Gadgets for EDI: " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)

def printListDG_ESI(NumOpsDis):	
	global o
	clearHashChecker()
	idval = 1
	while os.path.exists("%s-DG_DISPATCHER_ESI_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-DG_DISPATCHER_ESI_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		i=0
		temp = []
		total = 0
		for obj in objs:
			num = objs[o].listOP_BaseDG_Module_ESI.__len__()  #was cnt
			for i in range (num): #ibid
				addy =0x00
				cnt = 0    #
				addy = objs[o].listOP_BaseDG_ESI[i]
				cnt = objs[o].listOP_BaseDG_CNT_ESI[i]
				nOppsVal = objs[o].listOP_BaseDG_NumOps_ESI[i]
				mod = objs[o].listOP_BaseDG_Module_ESI[i]
				out = "Ops: " + str(nOppsVal) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, nOppsVal, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if num > 0:
				out = "\nJOP ROCKET" #out = "# Dispatcher Gadgets for ESI "  + str(mod) + " total: " + Ct2()
				temp.append(out)
			total = total + num	
			o = o + 1
		for out in temp:
			#print out
			print >> f, out
		out = ""#out = ""#"# Grand total Dispatcher Gadgets for ESI: " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)

def printListDG_EBP(NumOpsDis):	
	global o
	clearHashChecker()
	idval = 1
	while os.path.exists("%s-DG_DISPATCHER_EBP_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-DG_DISPATCHER_EBP_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		i=0
		temp = []
		total = 0
		for obj in objs:
			num = objs[o].listOP_BaseDG_Module_EBP.__len__()  #was cnt
			for i in range (num): #ibid
				addy =0x00
				cnt = 0    #
				addy = objs[o].listOP_BaseDG_EBP[i]
				cnt = objs[o].listOP_BaseDG_CNT_EBP[i]
				nOppsVal = objs[o].listOP_BaseDG_NumOps_EBP[i]
				mod = objs[o].listOP_BaseDG_Module_EBP[i]
				out = "Ops: " + str(nOppsVal) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, nOppsVal, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if num > 0:
				out = "\nJOP ROCKET" #out = "# Dispatcher Gadgets for EBP "  + str(mod) + " total: " + Ct2()
				temp.append(out)
			total = total + num	
			o = o + 1
		for out in temp:
			#print out
			print >> f, out
		out = ""#out = ""#"# Grand total Dispatcher Gadgets for EBP: " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)

def printListDG_ESP(NumOpsDis):	
	global o
	clearHashChecker()
	idval = 1
	while os.path.exists("%s-DG_DISPATCHER_ESP_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-DG_DISPATCHER_ESP_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		i=0
		temp = []
		total = 0
		for obj in objs:
			num = objs[o].listOP_BaseDG_Module_ESP.__len__()  #was cnt
			for i in range (num): #ibid
				addy =0x00
				cnt = 0    #
				addy = objs[o].listOP_BaseDG_ESP[i]
				cnt = objs[o].listOP_BaseDG_CNT_ESP[i]
				nOppsVal = objs[o].listOP_BaseDG_NumOps_ESP[i]
				mod = objs[o].listOP_BaseDG_Module_ESP[i]
				out = "Ops: " + str(nOppsVal) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, nOppsVal, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if num > 0:
				out = "\nJOP ROCKET" #out = "# Dispatcher Gadgets for ESP "  + str(mod) + " total: " + Ct2()
				temp.append(out)
			total = total + num	
			o = o + 1
		for out in temp:
			#print out
			print >> f, out
		out = ""#out = ""#"# Grand total Dispatcher Gadgets for ESP: " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)


def printListDG_BEST_EAX(NumOpsDis):	
	global o
	idval = 1
	clearHashChecker()
	counterReset()
	while os.path.exists("%s-DG_DISPATCHER_BEST_EAX_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName  +"-DG_DISPATCHER_BEST_EAX_" + str(idval) + ".txt"
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		i=0
		temp = []
		total = 0
		for obj in objs:
			num = objs[o].listOP_BaseDG_CNT_EAX_Best.__len__()  #was cnt
			for i in range (num): #ibid
				addy =0x00
				cnt = 0    #
				addy = objs[o].listOP_BaseDG_EAX_Best[i]
				cnt = objs[o].listOP_BaseDG_CNT_EAX_Best[i]
				nOppsVal = objs[o].listOP_BaseDG_NumOps_EAX_Best[i]
				mod = objs[o].listOP_BaseDG_Module_EAX_Best[i]
				out = "Ops: " + str(nOppsVal) + "\tMod: " + str(mod)
				#print out
				sp()
				
				cat = disHereClean3(addy, cnt, nOppsVal, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if num > 0:
				out = "\nJOP ROCKET" #out = "# Best Dispatcher Gadgets for EAX "  + str(mod) + " total: " + Ct2()
				temp.append(out)
			total = total + num	
			o = o + 1
		for out in temp:
			#print out
			print >> f, out
		out = ""#"# Grand total Beset Dispatcher Gadgets for EAX: " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)

def printListDG_BEST_EBX(NumOpsDis):	
	global o
	idval = 1
	clearHashChecker()
	counterReset()
	while os.path.exists("%s-DG_DISPATCHER_BEST_EBX_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName  +"-DG_DISPATCHER_BEST_EBX_" + str(idval) + ".txt"
	global fname
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		i=0
		temp = []
		total = 0
		for obj in objs:
			num = objs[o].listOP_BaseDG_Module_EBX_Best.__len__()  #was cnt
			for i in range (num): #ibid
				addy =0x00
				cnt = 0    #
				addy = objs[o].listOP_BaseDG_EBX_Best[i]
				cnt = objs[o].listOP_BaseDG_CNT_EBX_Best[i]
				nOppsVal = objs[o].listOP_BaseDG_NumOps_EBX_Best[i]
				mod = objs[o].listOP_BaseDG_Module_EBX_Best[i]
				out = "Ops: " + str(nOppsVal) + "\tMod: " + str(mod)
				#print out
				sp()
				
				cat = disHereClean3(addy, cnt, nOppsVal, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if num > 0:
				out = "\nJOP ROCKET" #out = "# Best Dispatcher Gadgets for EBX "  + str(mod) + " total: " + Ct2()
				temp.append(out)
			total = total + num	
			o = o + 1
		for out in temp:
			#print out
			print >> f, out
		out = ""#"# Grand total Best Dispatcher Gadgets for EBX: " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset() 
	nope(filename, total)

def printListDG_BEST_ECX(NumOpsDis):	
	global o
	idval = 1
	clearHashChecker()
	counterReset()
	while os.path.exists("%s-DG_DISPATCHER_BEST_ECX_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName  +"-DG_DISPATCHER_BEST_ECX_" + str(idval) + ".txt"
	global fname
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		i=0
		temp = []
		total = 0
		for obj in objs:
			num = objs[o].listOP_BaseDG_Module_ECX_Best.__len__()  #was cnt
			for i in range (num): #ibid
				addy =0x00
				cnt = 0    #
				addy = objs[o].listOP_BaseDG_ECX_Best[i]
				cnt = objs[o].listOP_BaseDG_CNT_ECX_Best[i]
				nOppsVal = objs[o].listOP_BaseDG_NumOps_ECX_Best[i]
				mod = objs[o].listOP_BaseDG_Module_ECX_Best[i]
				out = "Ops: " + str(nOppsVal) + "\tMod: " + str(mod)
				#print out
				sp()
				
				cat = disHereClean3(addy, cnt, nOppsVal, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if num > 0:
				out = "\nJOP ROCKET" #out = "# Best Dispatcher Gadgets for ECX "  + str(mod) + " total: " + Ct2()
				temp.append(out)
			total = total + num	
			o = o + 1
		for out in temp:
			#print out
			print >> f, out
		out = ""#"# Grand total Best Dispatcher Gadgets for ECX: " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)
 
def printListDG_BEST_EDX(NumOpsDis):	
	global o
	idval = 1
	clearHashChecker()
	counterReset()
	while os.path.exists("%s-DG_DISPATCHER_BEST_EDX_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName  +"-DG_DISPATCHER_BEST_EDX_" + str(idval) + ".txt"
	global fname
	global fname
	fname= filename
	with open(filename, 'a') as f:
		counterReset()
		i=0
		temp = []
		total = 0
		for obj in objs:
			num = objs[o].listOP_BaseDG_Module_EDX_Best.__len__()  #was cnt
			for i in range (num): #ibid
				addy =0x00
				cnt = 0    #
				addy = objs[o].listOP_BaseDG_EDX_Best[i]
				cnt = objs[o].listOP_BaseDG_CNT_EDX_Best[i]
				nOppsVal = objs[o].listOP_BaseDG_NumOps_EDX_Best[i]
				mod = objs[o].listOP_BaseDG_Module_EDX_Best[i]
				out = "Ops: " + str(nOppsVal) + "\tMod: " + str(mod)
				#print out
				sp()
				
				cat = disHereClean3(addy, cnt, nOppsVal, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if num > 0:
				out = "\nJOP ROCKET" #out = "# Best Dispatcher Gadgets for EDX "  + str(mod) + " total: " + Ct2()
				temp.append(out)
			total = total + num	
			o = o + 1
		for out in temp:
			#print out
			print >> f, out
		out = ""#"# Grand total Best Dispatcher Gadgets for EDX: " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
 
def printListDG_BEST_EDI( NumOpsDis):	
	global o
	clearHashChecker()
	counterReset()
	idval = 1
	while os.path.exists("%s-DG_DISPATCHER_BEST_EDI_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName  +"-DG_DISPATCHER_BEST_EDI_" + str(idval) + ".txt"
	global fname
	global fname
	fname= filename
	with open(filename, 'a') as f:
		i=0
		temp = []
		total = 0
		for obj in objs:
			num = objs[o].listOP_BaseDG_Module_EDI_Best.__len__()  #was cnt
			for i in range (num): #ibid
				addy =0x00
				cnt = 0    #
				addy = objs[o].listOP_BaseDG_EDI_Best[i]
				cnt = objs[o].listOP_BaseDG_CNT_EDI_Best[i]
				nOppsVal = objs[o].listOP_BaseDG_NumOps_EDI_Best[i]
				mod = objs[o].listOP_BaseDG_Module_EDI_Best[i]
				out = "Ops: " + str(nOppsVal) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, nOppsVal, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if num > 0:
				out = "\nJOP ROCKET" #out = "# Best Dispatcher Gadgets for EDI "  + str(mod) + " total: " + Ct2()
				temp.append(out)
			total = total + num	
			o = o + 1
		for out in temp:
			#print out
			print >> f, out
		out = ""#"# Grand total BEST Dispatcher Gadgets for EDI: " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)
 
def printListDG_BEST_ESI( NumOpsDis):	
	global o
	clearHashChecker()
	counterReset()
	idval = 1
	while os.path.exists("%s-DG_DISPATCHER_BEST_ESI_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName  +"-DG_DISPATCHER_BEST_ESI_" + str(idval) + ".txt"
	global fname
	global fname
	fname= filename
	with open(filename, 'a') as f:
		i=0
		temp = []
		total = 0
		for obj in objs:
			num = objs[o].listOP_BaseDG_Module_ESI_Best.__len__()  #was cnt
			for i in range (num): #ibid
				addy =0x00
				cnt = 0    #
				addy = objs[o].listOP_BaseDG_ESI_Best[i]
				cnt = objs[o].listOP_BaseDG_CNT_ESI_Best[i]
				nOppsVal = objs[o].listOP_BaseDG_NumOps_ESI_Best[i]
				mod = objs[o].listOP_BaseDG_Module_ESI_Best[i]
				out = "Ops: " + str(nOppsVal) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, nOppsVal, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if num > 0:
				out = "\nJOP ROCKET" #out = "# Best Dispatcher Gadgets for ESI "  + str(mod) + " total: " + Ct2()
				temp.append(out)
			total = total + num	
			o = o + 1
		for out in temp:
			#print out
			print >> f, out
		out = ""#"# Grand total BEST Dispatcher Gadgets for ESI: " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)
 
def printListDG_BEST_EBP( NumOpsDis):	
	global o
	clearHashChecker()
	counterReset()
	idval = 1
	while os.path.exists("%s-DG_DISPATCHER_BEST_EBP_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName  +"-DG_DISPATCHER_BEST_EBP_" + str(idval) + ".txt"
	global fname
	global fname
	fname= filename
	with open(filename, 'a') as f:
		i=0
		temp = []
		total = 0
		for obj in objs:
			num = objs[o].listOP_BaseDG_Module_EBP_Best.__len__()  #was cnt
			for i in range (num): #ibid
				addy =0x00
				cnt = 0    #
				addy = objs[o].listOP_BaseDG_EBP_Best[i]
				cnt = objs[o].listOP_BaseDG_CNT_EBP_Best[i]
				nOppsVal = objs[o].listOP_BaseDG_NumOps_EBP_Best[i]
				mod = objs[o].listOP_BaseDG_Module_EBP_Best[i]
				out = "Ops: " + str(nOppsVal) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, nOppsVal, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if num > 0:
				out = "\nJOP ROCKET" #out = "# Best Dispatcher Gadgets for EBP "  + str(mod) + " total: " + Ct2()
				temp.append(out)
			total = total + num	
			o = o + 1
		for out in temp:
			#print out
			print >> f, out
		out = ""#"# Grand total BEST Dispatcher Gadgets for EBP: " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)


def printListDG_BEST_ESP( NumOpsDis):	
	global o
	clearHashChecker()
	counterReset()
	idval = 1
	while os.path.exists("%s-DG_DISPATCHER_BEST_ESP_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName  +"-DG_DISPATCHER_BEST_ESP_" + str(idval) + ".txt"
	global fname
	global fname
	fname= filename
	with open(filename, 'a') as f:
		i=0
		temp = []
		total = 0
		for obj in objs:
			num = objs[o].listOP_BaseDG_Module_ESP_Best.__len__()  #was cnt
			for i in range (num): #ibid
				addy =0x00
				cnt = 0    #
				addy = objs[o].listOP_BaseDG_ESP_Best[i]
				cnt = objs[o].listOP_BaseDG_CNT_ESP_Best[i]
				nOppsVal = objs[o].listOP_BaseDG_NumOps_ESP_Best[i]
				mod = objs[o].listOP_BaseDG_Module_ESP_Best[i]
				out = "Ops: " + str(nOppsVal) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, nOppsVal, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if num > 0:
				out = "\nJOP ROCKET" #out = "# Best Dispatcher Gadgets for ESP "  + str(mod) + " total: " + Ct2()
				temp.append(out)
			total = total + num	
			o = o + 1
		for out in temp:
			#print out
			print >> f, out
		out = ""#"# Grand total BEST Dispatcher Gadgets for ESP: " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)

def printListDG_Other_EAX( NumOpsDis):	
	global o
	clearHashChecker()
	counterReset()
	idval = 1
	while os.path.exists("%s-DG_DISPATCHER_Other_EAX_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName  +"-DG_DISPATCHER_Other_EAX_" + str(idval) + ".txt"
	global fname
	global fname
	fname= filename
	with open(filename, 'a') as f:
		i=0
		temp = []
		total = 0
		for obj in objs:
			num = objs[o].listOP_BaseDG_Module_EAX_Other.__len__()  #was cnt
			for i in range (num): #ibid
				addy =0x00
				cnt = 0    #
				addy = objs[o].listOP_BaseDG_EAX_Other[i]
				cnt = objs[o].listOP_BaseDG_CNT_EAX_Other[i]
				nOppsVal = objs[o].listOP_BaseDG_NumOps_EAX_Other[i]
				mod = objs[o].listOP_BaseDG_Module_EAX_Other[i]
				out = "Ops: " + str(nOppsVal) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, nOppsVal, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if num > 0:
				out = "\nJOP ROCKET" #"# Other Dispatcher Gadgets for EAX "  + str(mod) + " total: " + Ct2()
				temp.append(out)
			total = total + num	
			o = o + 1
		for out in temp:
			#print out
			print >> f, out
		out = ""#"# Grand total Other Dispatcher Gadgets for EAX: " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)

def printListDG_Other_EBX( NumOpsDis):	
	global o
	clearHashChecker()
	counterReset()
	idval = 1
	while os.path.exists("%s-DG_DISPATCHER_Other_EBX_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName  +"-DG_DISPATCHER_Other_EBX_" + str(idval) + ".txt"
	global fname
	global fname
	fname= filename
	with open(filename, 'a') as f:
		i=0
		temp = []
		total = 0
		for obj in objs:
			num = objs[o].listOP_BaseDG_Module_EBX_Other.__len__()  #was cnt
			for i in range (num): #ibid
				addy =0x00
				cnt = 0    #
				addy = objs[o].listOP_BaseDG_EBX_Other[i]
				cnt = objs[o].listOP_BaseDG_CNT_EBX_Other[i]
				nOppsVal = objs[o].listOP_BaseDG_NumOps_EBX_Other[i]
				mod = objs[o].listOP_BaseDG_Module_EBX_Other[i]
				out = "Ops: " + str(nOppsVal) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, nOppsVal, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if num > 0:
				out = "\nJOP ROCKET" #"# Other Dispatcher Gadgets for EBX "  + str(mod) + " total: " + Ct2()
				temp.append(out)
			total = total + num	
			o = o + 1
		for out in temp:
			#print out
			print >> f, out
		out = ""#"# Grand total Other Dispatcher Gadgets for EBX: " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)
 
def printListDG_Other_ECX( NumOpsDis):	
	global o
	clearHashChecker()
	counterReset()
	idval = 1
	while os.path.exists("%s-DG_DISPATCHER_Other_ECX_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName  +"-DG_DISPATCHER_Other_ECX_" + str(idval) + ".txt"
	global fname
	global fname
	fname= filename
	with open(filename, 'a') as f:
		i=0
		temp = []
		total = 0
		for obj in objs:
			num = objs[o].listOP_BaseDG_Module_ECX_Other.__len__()  #was cnt
			for i in range (num): #ibid
				addy =0x00
				cnt = 0    #
				addy = objs[o].listOP_BaseDG_ECX_Other[i]
				cnt = objs[o].listOP_BaseDG_CNT_ECX_Other[i]
				nOppsVal = objs[o].listOP_BaseDG_NumOps_ECX_Other[i]
				mod = objs[o].listOP_BaseDG_Module_ECX_Other[i]
				out = "Ops: " + str(nOppsVal) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, nOppsVal, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if num > 0:
				out = "\nJOP ROCKET" #"# Other Dispatcher Gadgets for ECX "  + str(mod) + " total: " + Ct2()
				temp.append(out)
			total = total + num	
			o = o + 1
		for out in temp:
			#print out
			print >> f, out
		out = ""#"# Grand total Other Dispatcher Gadgets for ECX: " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)
 
def printListDG_Other_EDX( NumOpsDis):	
	global o
	clearHashChecker()
	counterReset()
	idval = 1
	while os.path.exists("%s-DG_DISPATCHER_Other_EDX_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName  +"-DG_DISPATCHER_Other_EDX_" + str(idval) + ".txt"
	global fname
	global fname
	fname= filename
	with open(filename, 'a') as f:
		i=0
		temp = []
		total = 0
		for obj in objs:
			num = objs[o].listOP_BaseDG_Module_EDX_Other.__len__()  #was cnt
			for i in range (num): #ibid
				addy =0x00
				cnt = 0    #
				addy = objs[o].listOP_BaseDG_EDX_Other[i]
				cnt = objs[o].listOP_BaseDG_CNT_EDX_Other[i]
				nOppsVal = objs[o].listOP_BaseDG_NumOps_EDX_Other[i]
				mod = objs[o].listOP_BaseDG_Module_EDX_Other[i]
				out = "Ops: " + str(nOppsVal) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, nOppsVal, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if num > 0:
				out = "\nJOP ROCKET" #"# Other Dispatcher Gadgets for EDX "  + str(mod) + " total: " + Ct2()
				temp.append(out)
			total = total + num	
			o = o + 1
		for out in temp:
			#print out
			print >> f, out
		out = ""#"# Grand total Other Dispatcher Gadgets for EDX: " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)
 
def printListDG_Other_EDI( NumOpsDis):	
	global o
	clearHashChecker()
	counterReset()
	idval = 1
	while os.path.exists("%s-DG_DISPATCHER_Other_EDI_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName  +"-DG_DISPATCHER_Other_EDI_" + str(idval) + ".txt"
	global fname
	global fname
	fname= filename
	with open(filename, 'a') as f:
		i=0
		temp = []
		total = 0
		for obj in objs:
			num = objs[o].listOP_BaseDG_Module_EDI_Other.__len__()  #was cnt
			for i in range (num): #ibid
				addy =0x00
				cnt = 0    #
				addy = objs[o].listOP_BaseDG_EDI_Other[i]
				cnt = objs[o].listOP_BaseDG_CNT_EDI_Other[i]
				nOppsVal = objs[o].listOP_BaseDG_NumOps_EDI_Other[i]
				mod = objs[o].listOP_BaseDG_Module_EDI_Other[i]
				out = "Ops: " + str(nOppsVal) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, nOppsVal, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if num > 0:
				out = "\nJOP ROCKET" #"# Other Dispatcher Gadgets for EDI "  + str(mod) + " total: " + Ct2()
				temp.append(out)
			total = total + num	
			o = o + 1
		for out in temp:
			#print out
			print >> f, out
		out = ""#"# Grand total Other Dispatcher Gadgets for EDI: " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)
 
def printListDG_Other_ESI( NumOpsDis):	
	global o
	clearHashChecker()
	counterReset()
	idval = 1
	while os.path.exists("%s-DG_DISPATCHER_Other_ESI_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName  +"-DG_DISPATCHER_Other_ESI_" + str(idval) + ".txt"
	global fname
	global fname
	fname= filename
	with open(filename, 'a') as f:
		i=0
		temp = []
		total = 0
		for obj in objs:
			num = objs[o].listOP_BaseDG_Module_ESI_Other.__len__()  #was cnt
			for i in range (num): #ibid
				addy =0x00
				cnt = 0    #
				addy = objs[o].listOP_BaseDG_ESI_Other[i]
				cnt = objs[o].listOP_BaseDG_CNT_ESI_Other[i]
				nOppsVal = objs[o].listOP_BaseDG_NumOps_ESI_Other[i]
				mod = objs[o].listOP_BaseDG_Module_ESI_Other[i]
				out = "Ops: " + str(nOppsVal) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, nOppsVal, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if num > 0:
				out = "\nJOP ROCKET" #"# Other Dispatcher Gadgets for ESI "  + str(mod) + " total: " + Ct2()
				temp.append(out)
			total = total + num	
			o = o + 1
		for out in temp:
			#print out
			print >> f, out
		out = ""#"# Grand total Other Dispatcher Gadgets for ESI: " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)
 
def printListDG_Other_EBP( NumOpsDis):	
	global o
	clearHashChecker()
	counterReset()
	idval = 1
	while os.path.exists("%s-DG_DISPATCHER_Other_EBP_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName  +"-DG_DISPATCHER_Other_EBP_" + str(idval) + ".txt"
	global fname
	global fname
	fname= filename
	with open(filename, 'a') as f:
		i=0
		temp = []
		total = 0
		for obj in objs:
			num = objs[o].listOP_BaseDG_Module_EBP_Other.__len__()  #was cnt
			for i in range (num): #ibid
				addy =0x00
				cnt = 0    #
				addy = objs[o].listOP_BaseDG_EBP_Other[i]
				cnt = objs[o].listOP_BaseDG_CNT_EBP_Other[i]
				nOppsVal = objs[o].listOP_BaseDG_NumOps_EBP_Other[i]
				mod = objs[o].listOP_BaseDG_Module_EBP_Other[i]
				out = "Ops: " + str(nOppsVal) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, nOppsVal, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if num > 0:
				out = "\nJOP ROCKET" #"# Other Dispatcher Gadgets for EBP "  + str(mod) + " total: " + Ct2()
				temp.append(out)
			total = total + num	
			o = o + 1
		for out in temp:
			#print out
			print >> f, out
		out = ""#"# Grand total Other Dispatcher Gadgets for EBP: " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)

def printListDG_Other_ESP( NumOpsDis):	
	global o
	clearHashChecker()
	counterReset()
	idval = 1
	while os.path.exists("%s-DG_DISPATCHER_Other_ESP_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName  +"-DG_DISPATCHER_Other_ESP_" + str(idval) + ".txt"
	global fname
	global fname
	fname= filename
	with open(filename, 'a') as f:
		i=0
		temp = []
		total = 0
		for obj in objs:
			num = objs[o].listOP_BaseDG_Module_ESP_Other.__len__()  #was cnt
			for i in range (num): #ibid
				addy =0x00
				cnt = 0    #
				addy = objs[o].listOP_BaseDG_ESP_Other[i]
				cnt = objs[o].listOP_BaseDG_CNT_ESP_Other[i]
				nOppsVal = objs[o].listOP_BaseDG_NumOps_ESP_Other[i]
				mod = objs[o].listOP_BaseDG_Module_ESP_Other[i]
				out = "Ops: " + str(nOppsVal) + "\tMod: " + str(mod)
				cat = disHereClean3(addy, cnt, nOppsVal, "jmp")
				if not cat == " ":
					print >> f, "*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^*^"
					counter()
					print >> f, Ct () + "\t" + out
					print >> f, cat
			if num > 0:
				out = "\nJOP ROCKET" #"# Other Dispatcher Gadgets for ESP "  + str(mod) + " total: " + Ct2()
				temp.append(out)
			total = total + num	
			o = o + 1
		for out in temp:
			#print out
			print >> f, out
		out = ""#"# Grand total Other Dispatcher Gadgets for ESP: " + str(total)
		#print out
		print >> f, out
	o = 0
	counterReset()
	clearGOuts()
	nope(filename, total)

def get_Total_ADD_EAX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "ADD EAX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseAddEAX, objs[t].listOP_BaseAddEAX_CNT,  objs[t].listOP_BaseAddEAX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_SUB_EAX():
	global total2
	#print "sub"
	sp()
	total2 = 0
	out = ""
	t = 0
	out2 = "SUB EAX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseSUBEAX, objs[t].listOP_BaseSubEAX_CNT,  objs[t].listOP_BaseSubEAX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
			sp()
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_MUL_EAX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MUL EAX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMulEAX, objs[t].listOP_BaseMulEAX_CNT,  objs[t].listOP_BaseMulEAX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DIV_EAX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DIV EAX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDivEAX, objs[t].listOP_BaseDivEAX_CNT,  objs[t].listOP_BaseDivEAX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_MOV_EAX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MOV EAX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMovEAX, objs[t].listOP_BaseMovEAX_CNT,  objs[t].listOP_BaseAddMov_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out


def get_Total_MOVSHUF_EAX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MOV SHUFFLE EAX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMovShufEAX, objs[t].listOP_BaseMovShufEAX_CNT,  objs[t].listOP_BaseMovShufEAX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_MOVVAL_EAX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MOV VALUE EAX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMovValEAX, objs[t].listOP_BaseMovValEAX_CNT,  objs[t].listOP_BaseMovValEAX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_LEA_EAX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "LEA EAX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseLeaEAX, objs[t].listOP_BaseLeaEAX_CNT,  objs[t].listOP_BaseAddLea_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_PUSH_EAX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "PUSH EAX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BasePushEAX, objs[t].listOP_BasePushEAX_CNT,  objs[t].listOP_BasePushEAX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_POP_EAX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "POP EAX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BasePopEAX, objs[t].listOP_BaseAddPop_CNT,  objs[t].listOP_BasePopEAX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_INC_EAX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "INC EAX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseIncEAX, objs[t].listOP_BaseIncEAX_CNT,  objs[t].listOP_BaseIncEAX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_DEC_EAX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DEC EAX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDecEAX, objs[t].listOP_BaseDecEAX_CNT,  objs[t].listOP_BaseDecEAX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_XCHG_EAX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "XCHG EAX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseXchgEAX, objs[t].listOP_BaseXchgEAX_CNT,  objs[t].listOP_BaseXchgEAX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_OP_JMP_EAX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "JMP EAX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_JMP_EAX2, objs[t].listOP_JMP_EAX_CNT,  objs[t].listOP_JMP_EAX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_OP_CALL_EAX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "CALL EAX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_CALL_EAX, objs[t].listOP_CALL_EAX_CNT,  objs[t].listOP_CALL_EAX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DG_EAX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DG EAX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDG_EAX, objs[t].listOP_BaseDG_CNT_EAX,  objs[t].listOP_BaseDG_NumOps_EAX)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DG_Other_EAX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DG OTHER EAX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDG_EAX_Other, objs[t].listOP_BaseDG_CNT_EAX_Other,  objs[t].listOP_BaseDG_NumOps_EAX_Other)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DG_BEST_EAX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DG BEST EAX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDG_EAX_Best, objs[t].listOP_BaseDG_CNT_EAX_Best,  objs[t].listOP_BaseDG_NumOps_EAX_Best)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_ADD_EBX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "ADD EBX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseAddEBX, objs[t].listOP_BaseAddEBX_CNT,  objs[t].listOP_BaseAddEBX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_SUB_EBX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "SUB EBX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseSUBEBX, objs[t].listOP_BaseSubEBX_CNT,  objs[t].listOP_BaseSubEBX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_MUL_EBX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MUL EBX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMulEBX, objs[t].listOP_BaseMulEBX_CNT,  objs[t].listOP_BaseMulEBX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DIV_EBX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DIV EBX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDivEBX, objs[t].listOP_BaseDivEBX_CNT,  objs[t].listOP_BaseDivEBX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_MOV_EBX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MOV EBX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMovEBX, objs[t].listOP_BaseMovEBX_CNT,  objs[t].listOP_BaseAddMov_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out


def get_Total_MOVSHUF_EBX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MOV SHUFFLE EBX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMovShufEBX, objs[t].listOP_BaseMovShufEBX_CNT,  objs[t].listOP_BaseMovShufEBX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_MOVVAL_EBX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MOV VALUE EBX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMovValEBX, objs[t].listOP_BaseMovValEBX_CNT,  objs[t].listOP_BaseMovValEBX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_LEA_EBX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "LEA EBX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseLeaEBX, objs[t].listOP_BaseLeaEBX_CNT,  objs[t].listOP_BaseAddLea_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_PUSH_EBX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "PUSH EBX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BasePushEBX, objs[t].listOP_BasePushEBX_CNT,  objs[t].listOP_BasePushEBX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_POP_EBX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "POP EBX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BasePopEBX, objs[t].listOP_BaseAddPop_CNT,  objs[t].listOP_BasePopEBX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_INC_EBX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "INC EBX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseIncEBX, objs[t].listOP_BaseIncEBX_CNT,  objs[t].listOP_BaseIncEBX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_DEC_EBX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DEC EBX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDecEBX, objs[t].listOP_BaseDecEBX_CNT,  objs[t].listOP_BaseDecEBX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_XCHG_EBX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "XCHG EBX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseXchgEBX, objs[t].listOP_BaseXchgEBX_CNT,  objs[t].listOP_BaseXchgEBX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_OP_JMP_EBX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "JMP EBX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_JMP_EBX, objs[t].listOP_JMP_EBX_CNT,  objs[t].listOP_JMP_EBX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_OP_CALL_EBX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "CALL EBX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_CALL_EBX, objs[t].listOP_CALL_EBX_CNT,  objs[t].listOP_CALL_EBX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DG_EBX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DG EBX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDG_EBX, objs[t].listOP_BaseDG_CNT_EBX,  objs[t].listOP_BaseDG_NumOps_EBX)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DG_Other_EBX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DG OTHER EBX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDG_EBX_Other, objs[t].listOP_BaseDG_CNT_EBX_Other,  objs[t].listOP_BaseDG_NumOps_EBX_Other)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DG_BEST_EBX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DG BEST EBX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDG_EBX_Best, objs[t].listOP_BaseDG_CNT_EBX_Best,  objs[t].listOP_BaseDG_NumOps_EBX_Best)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_ADD_ECX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "ADD ECX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseAddECX, objs[t].listOP_BaseAddECX_CNT,  objs[t].listOP_BaseAddECX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_SUB_ECX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "SUB ECX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseSUBECX, objs[t].listOP_BaseSubECX_CNT,  objs[t].listOP_BaseSubECX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_MUL_ECX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MUL ECX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMulECX, objs[t].listOP_BaseMulECX_CNT,  objs[t].listOP_BaseMulECX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DIV_ECX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DIV ECX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDivECX, objs[t].listOP_BaseDivECX_CNT,  objs[t].listOP_BaseDivECX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_MOV_ECX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MOV ECX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMovECX, objs[t].listOP_BaseMovECX_CNT,  objs[t].listOP_BaseAddMov_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out


def get_Total_MOVSHUF_ECX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MOV SHUFFLE ECX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMovShufECX, objs[t].listOP_BaseMovShufECX_CNT,  objs[t].listOP_BaseMovShufECX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_MOVVAL_ECX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MOV VALUE ECX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMovValECX, objs[t].listOP_BaseMovValECX_CNT,  objs[t].listOP_BaseMovValECX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_LEA_ECX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "LEA ECX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseLeaECX, objs[t].listOP_BaseLeaECX_CNT,  objs[t].listOP_BaseAddLea_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_PUSH_ECX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "PUSH ECX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BasePushECX, objs[t].listOP_BasePushECX_CNT,  objs[t].listOP_BasePushECX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_POP_ECX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "POP ECX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BasePopECX, objs[t].listOP_BaseAddPop_CNT,  objs[t].listOP_BasePopECX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_INC_ECX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "INC ECX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseIncECX, objs[t].listOP_BaseIncECX_CNT,  objs[t].listOP_BaseIncECX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_DEC_ECX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DEC ECX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDecECX, objs[t].listOP_BaseDecECX_CNT,  objs[t].listOP_BaseDecECX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_XCHG_ECX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "XCHG ECX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseXchgECX, objs[t].listOP_BaseXchgECX_CNT,  objs[t].listOP_BaseXchgECX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_OP_JMP_ECX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "JMP ECX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_JMP_ECX, objs[t].listOP_JMP_ECX_CNT,  objs[t].listOP_JMP_ECX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_OP_CALL_ECX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "CALL ECX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_CALL_ECX, objs[t].listOP_CALL_ECX_CNT,  objs[t].listOP_CALL_ECX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DG_ECX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DG ECX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDG_ECX, objs[t].listOP_BaseDG_CNT_ECX,  objs[t].listOP_BaseDG_NumOps_ECX)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DG_Other_ECX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DG OTHER ECX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDG_ECX_Other, objs[t].listOP_BaseDG_CNT_ECX_Other,  objs[t].listOP_BaseDG_NumOps_ECX_Other)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DG_BEST_ECX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DG BEST ECX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDG_ECX_Best, objs[t].listOP_BaseDG_CNT_ECX_Best,  objs[t].listOP_BaseDG_NumOps_ECX_Best)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_ADD_EDX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "ADD EDX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseAddEDX, objs[t].listOP_BaseAddEDX_CNT,  objs[t].listOP_BaseAddEDX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_SUB_EDX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "SUB EDX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseSUBEDX, objs[t].listOP_BaseSubEDX_CNT,  objs[t].listOP_BaseSubEDX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_MUL_EDX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MUL EDX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMulEDX, objs[t].listOP_BaseMulEDX_CNT,  objs[t].listOP_BaseMulEDX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DIV_EDX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DIV EDX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDivEDX, objs[t].listOP_BaseDivEDX_CNT,  objs[t].listOP_BaseDivEDX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_MOV_EDX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MOV EDX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMovEDX, objs[t].listOP_BaseMovEDX_CNT,  objs[t].listOP_BaseAddMov_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out


def get_Total_MOVSHUF_EDX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MOV SHUFFLE EDX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMovShufEDX, objs[t].listOP_BaseMovShufEDX_CNT,  objs[t].listOP_BaseMovShufEDX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_MOVVAL_EDX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MOV VALUE EDX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMovValEDX, objs[t].listOP_BaseMovValEDX_CNT,  objs[t].listOP_BaseMovValEDX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_LEA_EDX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "LEA EDX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseLeaEDX, objs[t].listOP_BaseLeaEDX_CNT,  objs[t].listOP_BaseAddLea_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_PUSH_EDX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "PUSH EDX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BasePushEDX, objs[t].listOP_BasePushEDX_CNT,  objs[t].listOP_BasePushEDX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_POP_EDX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "POP EDX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BasePopEDX, objs[t].listOP_BaseAddPop_CNT,  objs[t].listOP_BasePopEDX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_INC_EDX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "INC EDX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseIncEDX, objs[t].listOP_BaseIncEDX_CNT,  objs[t].listOP_BaseIncEDX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_DEC_EDX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DEC EDX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDecEDX, objs[t].listOP_BaseDecEDX_CNT,  objs[t].listOP_BaseDecEDX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_XCHG_EDX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "XCHG EDX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseXchgEDX, objs[t].listOP_BaseXchgEDX_CNT,  objs[t].listOP_BaseXchgEDX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_OP_JMP_EDX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "JMP EDX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_JMP_EDX, objs[t].listOP_JMP_EDX_CNT,  objs[t].listOP_JMP_EDX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_OP_CALL_EDX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "CALL EDX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_CALL_EDX, objs[t].listOP_CALL_EDX_CNT,  objs[t].listOP_CALL_EDX_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DG_EDX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DG EDX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDG_EDX, objs[t].listOP_BaseDG_CNT_EDX,  objs[t].listOP_BaseDG_NumOps_EDX)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DG_Other_EDX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DG OTHER EDX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDG_EDX_Other, objs[t].listOP_BaseDG_CNT_EDX_Other,  objs[t].listOP_BaseDG_NumOps_EDX_Other)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DG_BEST_EDX():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DG BEST EDX"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDG_EDX_Best, objs[t].listOP_BaseDG_CNT_EDX_Best,  objs[t].listOP_BaseDG_NumOps_EDX_Best)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_ADD_EDI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "ADD EDI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseAddEDI, objs[t].listOP_BaseAddEDI_CNT,  objs[t].listOP_BaseAddEDI_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_SUB_EDI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "SUB EDI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseSUBEDI, objs[t].listOP_BaseSubEDI_CNT,  objs[t].listOP_BaseSubEDI_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_MUL_EDI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MUL EDI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMulEDI, objs[t].listOP_BaseMulEDI_CNT,  objs[t].listOP_BaseMulEDI_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DIV_EDI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DIV EDI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDivEDI, objs[t].listOP_BaseDivEDI_CNT,  objs[t].listOP_BaseDivEDI_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_MOV_EDI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MOV EDI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMovEDI, objs[t].listOP_BaseMovEDI_CNT,  objs[t].listOP_BaseAddMov_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out


def get_Total_MOVSHUF_EDI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MOV SHUFFLE EDI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMovShufEDI, objs[t].listOP_BaseMovShufEDI_CNT,  objs[t].listOP_BaseMovShufEDI_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_MOVVAL_EDI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MOV VALUE EDI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMovValEDI, objs[t].listOP_BaseMovValEDI_CNT,  objs[t].listOP_BaseMovValEDI_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_LEA_EDI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "LEA EDI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseLeaEDI, objs[t].listOP_BaseLeaEDI_CNT,  objs[t].listOP_BaseAddLea_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_PUSH_EDI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "PUSH EDI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BasePushEDI, objs[t].listOP_BasePushEDI_CNT,  objs[t].listOP_BasePushEDI_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_POP_EDI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "POP EDI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BasePopEDI, objs[t].listOP_BaseAddPop_CNT,  objs[t].listOP_BasePopEDI_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_INC_EDI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "INC EDI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseIncEDI, objs[t].listOP_BaseIncEDI_CNT,  objs[t].listOP_BaseIncEDI_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_DEC_EDI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DEC EDI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDecEDI, objs[t].listOP_BaseDecEDI_CNT,  objs[t].listOP_BaseDecEDI_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_XCHG_EDI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "XCHG EDI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseXchgEDI, objs[t].listOP_BaseXchgEDI_CNT,  objs[t].listOP_BaseXchgEDI_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_OP_JMP_EDI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "JMP EDI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_JMP_EDI, objs[t].listOP_JMP_EDI_CNT,  objs[t].listOP_JMP_EDI_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_OP_CALL_EDI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "CALL EDI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_CALL_EDI, objs[t].listOP_CALL_EDI_CNT,  objs[t].listOP_CALL_EDI_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DG_EDI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DG EDI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDG_EDI, objs[t].listOP_BaseDG_CNT_EDI,  objs[t].listOP_BaseDG_NumOps_EDI)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DG_Other_EDI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DG OTHER EDI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDG_EDI_Other, objs[t].listOP_BaseDG_CNT_EDI_Other,  objs[t].listOP_BaseDG_NumOps_EDI_Other)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DG_BEST_EDI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DG BEST EDI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDG_EDI_Best, objs[t].listOP_BaseDG_CNT_EDI_Best,  objs[t].listOP_BaseDG_NumOps_EDI_Best)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_ADD_ESI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "ADD ESI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseAddESI, objs[t].listOP_BaseAddESI_CNT,  objs[t].listOP_BaseAddESI_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_SUB_ESI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "SUB ESI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseSUBESI, objs[t].listOP_BaseSubESI_CNT,  objs[t].listOP_BaseSubESI_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_MUL_ESI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MUL ESI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMulESI, objs[t].listOP_BaseMulESI_CNT,  objs[t].listOP_BaseMulESI_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DIV_ESI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DIV ESI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BasESIvESI, objs[t].listOP_BasESIvESI_CNT,  objs[t].listOP_BasESIvESI_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_MOV_ESI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MOV ESI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMovESI, objs[t].listOP_BaseMovESI_CNT,  objs[t].listOP_BaseAddMov_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out


def get_Total_MOVSHUF_ESI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MOV SHUFFLE ESI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMovShufESI, objs[t].listOP_BaseMovShufESI_CNT,  objs[t].listOP_BaseMovShufESI_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_MOVVAL_ESI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MOV VALUE ESI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMovValESI, objs[t].listOP_BaseMovValESI_CNT,  objs[t].listOP_BaseMovValESI_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_LEA_ESI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "LEA ESI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseLeaESI, objs[t].listOP_BaseLeaESI_CNT,  objs[t].listOP_BaseAddLea_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_PUSH_ESI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "PUSH ESI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BasePushESI, objs[t].listOP_BasePushESI_CNT,  objs[t].listOP_BasePushESI_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_POP_ESI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "POP ESI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BasePopESI, objs[t].listOP_BaseAddPop_CNT,  objs[t].listOP_BasePopESI_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_INC_ESI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "INC ESI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseIncESI, objs[t].listOP_BaseIncESI_CNT,  objs[t].listOP_BaseIncESI_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_DEC_ESI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DEC ESI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDecESI, objs[t].listOP_BaseDecESI_CNT,  objs[t].listOP_BaseDecESI_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_XCHG_ESI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "XCHG ESI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseXchgESI, objs[t].listOP_BaseXchgESI_CNT,  objs[t].listOP_BaseXchgESI_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_OP_JMP_ESI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "JMP ESI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_JMP_ESI, objs[t].listOP_JMP_ESI_CNT,  objs[t].listOP_JMP_ESI_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_OP_CALL_ESI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "CALL ESI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_CALL_ESI, objs[t].listOP_CALL_ESI_CNT,  objs[t].listOP_CALL_ESI_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DG_ESI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DG ESI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDG_ESI, objs[t].listOP_BaseDG_CNT_ESI,  objs[t].listOP_BaseDG_NumOps_ESI)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DG_Other_ESI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DG OTHER ESI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDG_ESI_Other, objs[t].listOP_BaseDG_CNT_ESI_Other,  objs[t].listOP_BaseDG_NumOps_ESI_Other)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DG_BEST_ESI():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DG BEST ESI"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDG_ESI_Best, objs[t].listOP_BaseDG_CNT_ESI_Best,  objs[t].listOP_BaseDG_NumOps_ESI_Best)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_ADD_ESP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "ADD ESP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseAddESP, objs[t].listOP_BaseAddESP_CNT,  objs[t].listOP_BaseAddESP_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_SUB_ESP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "SUB ESP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseSUBESP, objs[t].listOP_BaseSubESP_CNT,  objs[t].listOP_BaseSubESP_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_MUL_ESP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MUL ESP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMulESP, objs[t].listOP_BaseMulESP_CNT,  objs[t].listOP_BaseMulESP_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DIV_ESP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DIV ESP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BasESPvESP, objs[t].listOP_BasESPvESP_CNT,  objs[t].listOP_BasESPvESP_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_MOV_ESP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MOV ESP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMovESP, objs[t].listOP_BaseMovESP_CNT,  objs[t].listOP_BaseAddMov_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out


def get_Total_MOVSHUF_ESP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MOV SHUFFLE ESP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMovShufESP, objs[t].listOP_BaseMovShufESP_CNT,  objs[t].listOP_BaseMovShufESP_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_MOVVAL_ESP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MOV VALUE ESP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMovValESP, objs[t].listOP_BaseMovValESP_CNT,  objs[t].listOP_BaseMovValESP_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_LEA_ESP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "LEA ESP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseLeaESP, objs[t].listOP_BaseLeaESP_CNT,  objs[t].listOP_BaseAddLea_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_PUSH_ESP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "PUSH ESP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BasePushESP, objs[t].listOP_BasePushESP_CNT,  objs[t].listOP_BasePushESP_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_POP_ESP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "POP ESP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BasePopESP, objs[t].listOP_BaseAddPop_CNT,  objs[t].listOP_BasePopESP_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_INC_ESP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "INC ESP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseIncESP, objs[t].listOP_BaseIncESP_CNT,  objs[t].listOP_BaseIncESP_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_DEC_ESP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DEC ESP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDecESP, objs[t].listOP_BaseDecESP_CNT,  objs[t].listOP_BaseDecESP_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_XCHG_ESP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "XCHG ESP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseXchgESP, objs[t].listOP_BaseXchgESP_CNT,  objs[t].listOP_BaseXchgESP_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_OP_JMP_ESP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "JMP ESP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_JMP_ESP, objs[t].listOP_JMP_ESP_CNT,  objs[t].listOP_JMP_ESP_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_OP_CALL_ESP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "CALL ESP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_CALL_ESP, objs[t].listOP_CALL_ESP_CNT,  objs[t].listOP_CALL_ESP_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DG_ESP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DG ESP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDG_ESP, objs[t].listOP_BaseDG_CNT_ESP,  objs[t].listOP_BaseDG_NumOps_ESP)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DG_Other_ESP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DG OTHER ESP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDG_ESP_Other, objs[t].listOP_BaseDG_CNT_ESP_Other,  objs[t].listOP_BaseDG_NumOps_ESP_Other)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DG_BEST_ESP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DG BEST ESP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDG_ESP_Best, objs[t].listOP_BaseDG_CNT_ESP_Best,  objs[t].listOP_BaseDG_NumOps_ESP_Best)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_ADD_EBP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "ADD EBP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseAddEBP, objs[t].listOP_BaseAddEBP_CNT,  objs[t].listOP_BaseAddEBP_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_SUB_EBP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "SUB EBP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseSUBEBP, objs[t].listOP_BaseSubEBP_CNT,  objs[t].listOP_BaseSubEBP_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_MUL_EBP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MUL EBP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMulEBP, objs[t].listOP_BaseMulEBP_CNT,  objs[t].listOP_BaseMulEBP_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DIV_EBP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DIV EBP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BasEBPvEBP, objs[t].listOP_BasEBPvEBP_CNT,  objs[t].listOP_BasEBPvEBP_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_MOV_EBP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MOV EBP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMovEBP, objs[t].listOP_BaseMovEBP_CNT,  objs[t].listOP_BaseAddMov_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out


def get_Total_MOVSHUF_EBP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MOV SHUFFLE EBP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMovShufEBP, objs[t].listOP_BaseMovShufEBP_CNT,  objs[t].listOP_BaseMovShufEBP_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_MOVVAL_EBP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MOV VALUE EBP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMovValEBP, objs[t].listOP_BaseMovValEBP_CNT,  objs[t].listOP_BaseMovValEBP_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_LEA_EBP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "LEA EBP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseLeaEBP, objs[t].listOP_BaseLeaEBP_CNT,  objs[t].listOP_BaseAddLea_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_PUSH_EBP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "PUSH EBP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BasePushEBP, objs[t].listOP_BasePushEBP_CNT,  objs[t].listOP_BasePushEBP_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_POP_EBP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "POP EBP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BasePopEBP, objs[t].listOP_BaseAddPop_CNT,  objs[t].listOP_BasePopEBP_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_INC_EBP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "INC EBP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseIncEBP, objs[t].listOP_BaseIncEBP_CNT,  objs[t].listOP_BaseIncEBP_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_DEC_EBP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DEC EBP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDecEBP, objs[t].listOP_BaseDecEBP_CNT,  objs[t].listOP_BaseDecEBP_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_XCHG_EBP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "XCHG EBP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseXchgEBP, objs[t].listOP_BaseXchgEBP_CNT,  objs[t].listOP_BaseXchgEBP_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_OP_JMP_EBP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "JMP EBP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_JMP_EBP, objs[t].listOP_JMP_EBP_CNT,  objs[t].listOP_JMP_EBP_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_OP_CALL_EBP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "CALL EBP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_CALL_EBP, objs[t].listOP_CALL_EBP_CNT,  objs[t].listOP_CALL_EBP_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DG_EBP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DG EBP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDG_EBP, objs[t].listOP_BaseDG_CNT_EBP,  objs[t].listOP_BaseDG_NumOps_EBP)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DG_Other_EBP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DG OTHER EBP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDG_EBP_Other, objs[t].listOP_BaseDG_CNT_EBP_Other,  objs[t].listOP_BaseDG_NumOps_EBP_Other)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DG_BEST_EBP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DG BEST EBP"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDG_EBP_Best, objs[t].listOP_BaseDG_CNT_EBP_Best,  objs[t].listOP_BaseDG_NumOps_EBP_Best)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_ADD():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "ADD "
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseAdd, objs[t].listOP_BaseAdd_CNT,  objs[t].listOP_BaseAdd_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_SUB():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "SUB "
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseSUB, objs[t].listOP_BaseSub_CNT,  objs[t].listOP_BaseSub_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_MUL():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MUL "
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMul, objs[t].listOP_BaseMul_CNT,  objs[t].listOP_BaseMul_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_DIV():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DIV "
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_Basv, objs[t].listOP_Basv_CNT,  objs[t].listOP_Basv_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_MOV():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MOV "
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMov, objs[t].listOP_BaseMov_CNT,  objs[t].listOP_BaseAddMov_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out


def get_Total_MOVSHUF():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MOV SHUFFLE "
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMovShuf, objs[t].listOP_BaseMovShuf_CNT,  objs[t].listOP_BaseMovShuf_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_MOVVAL():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "MOV VALUE "
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseMovVal, objs[t].listOP_BaseMovVal_CNT,  objs[t].listOP_BaseMovVal_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_LEA():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "LEA "
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseLea, objs[t].listOP_BaseLea_CNT,  objs[t].listOP_BaseAddLea_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_PUSH():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "PUSH "
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BasePush, objs[t].listOP_BasePush_CNT,  objs[t].listOP_BasePush_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_POP():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "POP "
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BasePop, objs[t].listOP_BaseAddPop_CNT,  objs[t].listOP_BasePop_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def get_Total_INC():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "INC "
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseInc, objs[t].listOP_BaseInc_CNT,  objs[t].listOP_BaseInc_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_DEC():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "DEC "
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseDec, objs[t].listOP_BaseDec_CNT,  objs[t].listOP_BaseDec_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_XCHG():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "XCHG "
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseXchg, objs[t].listOP_BaseXchg_CNT,  objs[t].listOP_BaseXchg_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out






def get_Total_ROTATE_RIGHT():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "ROTATE RIGHT"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseRotRight, objs[t].listOP_BaseRotRight_CNT,  objs[t].listOP_BaseRotRight_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_ROTATE_LEFT():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "ROTATE LEFT"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseRotLeft, objs[t].listOP_BaseRotLeft_CNT,  objs[t].listOP_BaseRotLeft_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_SHIFT_RIGHT():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "SHIFT RIGHT"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseShiftRight, objs[t].listOP_BaseShiftRight_CNT,  objs[t].listOP_BaseShiftRight_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out

def get_Total_SHIFT_LEFT():
	global total2
	total2 = 0
	out = ""
	t = 0
	out2 = "SHIFT LEFT"
	for obj in objs:
		try:  
			val = cleaner(objs[t].listOP_BaseShiftLeft, objs[t].listOP_BaseShiftLeft_CNT,  objs[t].listOP_BaseShiftLeft_NumOps)
			out += ", " + val
			total2 += int(val)
			t=t+1
		except:
			out += ", 0"
			t=t+1
			pass
	out = out2 + ", " + str(total2) + out
	return out
def getAllModules():
	t = 0
	out = "Module"
	out += ", " + peName + " all"
	# for dll in PE_DLLS:
	# 	try:
	# 		out += ", " + str(PE_DLLS[t]) 
	# 		t=t+1
	# 	except:
	# 		out += ", [module]"
	# 		t=t+1
	# 		pass
	# # return out

	# for obj in objs:
	# 	try:
	# 		out += ", " + str(objs[t].listOP_JMP_EAX_Module[0]) 
	# 		t=t+1
	# 	except:
	# 		try:
	# 			out += ", " + str(objs[t].listOP_JMP_EBX_Module[0])
	# 			t=t+1
	# 		except:
	# 			try:
	# 				out += ", " + str(objs[t].listOP_JMP_ECX_Module[0])
	# 				t=t+1
	# 			except:
	# 				try:
	# 					out += ", " + str(objs[t].listOP_JMP_EDX_Module[0])
	# 					t=t+1
	# 				except:
	# 					try:
	# 						out += ", " + str(objs[t].listOP_JMP_ESI_Module[0])
	# 						t=t+1
	# 					except:
	# 						try:
	# 							out += ", " + str(objs[t].listOP_JMP_EBP_Module[0])
	# 							t=t+1
	# 						except:
	# 							try:
	# 								out += ", " + str(objs[t].listOP_JMP_EDI_Module[0])
	# 								t=t+1
	# 							except:
	# 								out += ", [module]"
	# 								t=t+1
	# 								pass
	# return out

	for obj in objs:
		try:
			out += ", " + str(objs[t].modName2)
			t=t+1
		except:
			try:
				out += ", " + objs[t].modName2
				t=t+1
			except:
				out += ", [module]"
				t=t+1
	
	return out



def getStatisticalResults():
	#print "enter"
	sp()
	idval = 1
	while os.path.exists("%s-statistical output_%s.csv" % (peName, idval)):
	    idval += 1
	filename =  peName +"-"+"statistical output_" + str(idval) + ".csv"
	with open(filename, 'w') as f:
		out = peName + "\n"
		out =  getAllModules() + "\n"
		out +=  get_Total_OP_JMP_EAX() + "\n"
		out +=  get_Total_OP_JMP_EBX() + "\n"
		out +=  get_Total_OP_JMP_ECX() + "\n"
		out +=  get_Total_OP_JMP_EDX() + "\n"
		out +=  get_Total_OP_JMP_EDI() + "\n"
		out +=  get_Total_OP_JMP_ESI() + "\n"
		out +=  get_Total_OP_JMP_EBP() + "\n"
		out +=  get_Total_OP_CALL_EAX() + "\n"
		out +=  get_Total_OP_CALL_EBX() + "\n"
		out +=  get_Total_OP_CALL_ECX() + "\n"
		out +=  get_Total_OP_CALL_EDX() + "\n"
		out +=  get_Total_OP_CALL_EDI() + "\n"
		out +=  get_Total_OP_CALL_ESI() + "\n"
		out +=  get_Total_OP_CALL_EBP() + "\n"
		out +=  get_Total_DG_EAX() + "\n"
		out +=  get_Total_DG_EBX() + "\n"
		out +=  get_Total_DG_ECX() + "\n"
		out +=  get_Total_DG_EDX() + "\n"
		out +=  get_Total_DG_EDI() + "\n"
		out +=  get_Total_DG_ESI() + "\n"
		out +=  get_Total_DG_EBP() + "\n"
		out +=  get_Total_DG_BEST_EAX() + "\n"
		out +=  get_Total_DG_BEST_EBX() + "\n"
		out +=  get_Total_DG_BEST_ECX() + "\n"
		out +=  get_Total_DG_BEST_EDX() + "\n"
		out +=  get_Total_DG_BEST_EDI() + "\n"
		out +=  get_Total_DG_BEST_ESI() + "\n"
		out +=  get_Total_DG_BEST_EBP() + "\n"

		out +=  get_Total_DG_Other_EAX() + "\n"
		out +=  get_Total_DG_Other_EBX() + "\n"
		out +=  get_Total_DG_Other_ECX() + "\n"
		out +=  get_Total_DG_Other_EDX() + "\n"
		out +=  get_Total_DG_Other_EDI() + "\n"
		out +=  get_Total_DG_Other_ESI() + "\n"
		out +=  get_Total_DG_Other_EBP() + "\n"


		out +=  get_Total_ADD() + "\n"
		out +=  get_Total_ADD_EAX() + "\n"
		out +=  get_Total_ADD_EBX() + "\n"
		out +=  get_Total_ADD_ECX() + "\n"
		out +=  get_Total_ADD_EDX() + "\n"
		out +=  get_Total_ADD_EDI() + "\n"
		out +=  get_Total_ADD_ESI() + "\n"
		out +=  get_Total_ADD_EBP() + "\n"

		out +=  get_Total_SUB() + "\n"
		out +=  get_Total_SUB_EAX() + "\n"
		out +=  get_Total_SUB_EBX() + "\n"
		out +=  get_Total_SUB_ECX() + "\n"
		out +=  get_Total_SUB_EDX() + "\n"
		out +=  get_Total_SUB_EDI() + "\n"
		out +=  get_Total_SUB_ESI() + "\n"
		out +=  get_Total_SUB_EBP() + "\n"


		out +=  get_Total_MUL() + "\n"
		out +=  get_Total_MUL_EAX() + "\n"
		out +=  get_Total_MUL_EBX() + "\n"
		out +=  get_Total_MUL_ECX() + "\n"
		out +=  get_Total_MUL_EDX() + "\n"
		out +=  get_Total_MUL_EDI() + "\n"
		out +=  get_Total_MUL_ESI() + "\n"
		out +=  get_Total_MUL_EBP() + "\n"

		out +=  get_Total_DIV() + "\n"
		out +=  get_Total_DIV_EAX() + "\n"
		out +=  get_Total_DIV_EBX() + "\n"
		out +=  get_Total_DIV_ECX() + "\n"
		out +=  get_Total_DIV_EDX() + "\n"
		out +=  get_Total_DIV_EDI() + "\n"
		out +=  get_Total_DIV_ESI() + "\n"
		out +=  get_Total_DIV_EBP() + "\n"

		out +=  get_Total_MOV() + "\n"
		out +=  get_Total_MOV_EAX() + "\n"
		out +=  get_Total_MOV_EBX() + "\n"
		out +=  get_Total_MOV_ECX() + "\n"
		out +=  get_Total_MOV_EDX() + "\n"
		out +=  get_Total_MOV_EDI() + "\n"
		out +=  get_Total_MOV_ESI() + "\n"
		out +=  get_Total_MOV_EBP() + "\n"

		out +=  get_Total_MOVSHUF() + "\n"
		out +=  get_Total_MOVSHUF_EAX() + "\n"
		out +=  get_Total_MOVSHUF_EBX() + "\n"
		out +=  get_Total_MOVSHUF_ECX() + "\n"
		out +=  get_Total_MOVSHUF_EDX() + "\n"
		out +=  get_Total_MOVSHUF_EDI() + "\n"
		out +=  get_Total_MOVSHUF_ESI() + "\n"
		out +=  get_Total_MOVSHUF_EBP() + "\n"

		out +=  get_Total_MOVVAL() + "\n"
		out +=  get_Total_MOVVAL_EAX() + "\n"
		out +=  get_Total_MOVVAL_EBX() + "\n"
		out +=  get_Total_MOVVAL_ECX() + "\n"
		out +=  get_Total_MOVVAL_EDX() + "\n"
		out +=  get_Total_MOVVAL_EDI() + "\n"
		out +=  get_Total_MOVVAL_ESI() + "\n"
		out +=  get_Total_MOVVAL_EBP() + "\n"

		out +=  get_Total_LEA() + "\n"
		out +=  get_Total_LEA_EAX() + "\n"
		out +=  get_Total_LEA_EBX() + "\n"
		out +=  get_Total_LEA_ECX() + "\n"
		out +=  get_Total_LEA_EDX() + "\n"
		out +=  get_Total_LEA_EDI() + "\n"
		out +=  get_Total_LEA_ESI() + "\n"
		out +=  get_Total_LEA_EBP() + "\n"

		out +=  get_Total_PUSH() + "\n"
		out +=  get_Total_PUSH_EAX() + "\n"
		out +=  get_Total_PUSH_EBX() + "\n"
		out +=  get_Total_PUSH_ECX() + "\n"
		out +=  get_Total_PUSH_EDX() + "\n"
		out +=  get_Total_PUSH_EDI() + "\n"
		out +=  get_Total_PUSH_ESI() + "\n"
		out +=  get_Total_PUSH_EBP() + "\n"

		out +=  get_Total_POP() + "\n"
		out +=  get_Total_POP_EAX() + "\n"
		out +=  get_Total_POP_EBX() + "\n"
		out +=  get_Total_POP_ECX() + "\n"
		out +=  get_Total_POP_EDX() + "\n"
		out +=  get_Total_POP_EDI() + "\n"
		out +=  get_Total_POP_ESI() + "\n"
		out +=  get_Total_POP_EBP() + "\n"

		out +=  get_Total_INC() + "\n"
		out +=  get_Total_INC_EAX() + "\n"
		out +=  get_Total_INC_EBX() + "\n"
		out +=  get_Total_INC_ECX() + "\n"
		out +=  get_Total_INC_EDX() + "\n"
		out +=  get_Total_INC_EDI() + "\n"
		out +=  get_Total_INC_ESI() + "\n"
		out +=  get_Total_INC_EBP() + "\n"

		out +=  get_Total_DEC() + "\n"
		out +=  get_Total_DEC_EAX() + "\n"
		out +=  get_Total_DEC_EBX() + "\n"
		out +=  get_Total_DEC_ECX() + "\n"
		out +=  get_Total_DEC_EDX() + "\n"
		out +=  get_Total_DEC_EDI() + "\n"
		out +=  get_Total_DEC_ESI() + "\n"
		out +=  get_Total_DEC_EBP() + "\n"

		out +=  get_Total_XCHG() + "\n"
		out +=  get_Total_XCHG_EAX() + "\n"
		out +=  get_Total_XCHG_EBX() + "\n"
		out +=  get_Total_XCHG_ECX() + "\n"
		out +=  get_Total_XCHG_EDX() + "\n"
		out +=  get_Total_XCHG_EDI() + "\n"
		out +=  get_Total_XCHG_ESI() + "\n"
		out +=  get_Total_XCHG_EBP() + "\n"

		out +=  get_Total_SHIFT_LEFT() + "\n"
		out +=  get_Total_SHIFT_RIGHT() + "\n"
		out +=  get_Total_ROTATE_LEFT() + "\n"
		out +=  get_Total_ROTATE_RIGHT() + "\n"
		#print out
		print >> f, out
		print "CSV written to disk."
		print "\t" + filename
		sp()

def initMods(dll):
	global modName
	global o
	objs[o].modName2 = dll
	objs[o].listOP_JMP_EAX_Module.append(dll)
	objs[o].listOP_JMP_EBX_Module.append(dll)
	objs[o].listOP_JMP_ECX_Module.append(dll)
	objs[o].listOP_JMP_EDX_Module.append(dll)
	objs[o].listOP_JMP_ESI_Module.append(dll)
	objs[o].listOP_JMP_EDI_Module.append(dll)
	objs[o].listOP_JMP_ESP_Module.append(dll)
	objs[o].listOP_JMP_EBP_Module.append(dll)
	objs[o].listOP_JMP_EAX2.append(0)
	objs[o].listOP_JMP_EBX.append(0)
	objs[o].listOP_JMP_ECX.append(0)
	objs[o].listOP_JMP_EDX.append(0)
	objs[o].listOP_JMP_ESI.append(0)
	objs[o].listOP_JMP_EDI.append(0)
	objs[o].listOP_JMP_ESP.append(0)  
	objs[o].listOP_JMP_EBP.append(0)
	objs[o].listOP_JMP_EAX_CNT.append(0)
	objs[o].listOP_JMP_EBX_CNT.append(0)
	objs[o].listOP_JMP_ECX_CNT.append(0)
	objs[o].listOP_JMP_EDX_CNT.append(0)
	objs[o].listOP_JMP_ESI_CNT.append(0)
	objs[o].listOP_JMP_EDI_CNT.append(0)
	objs[o].listOP_JMP_ESP_CNT.append(0)  
	objs[o].listOP_JMP_EBP_CNT.append(0)
	objs[o].listOP_JMP_EAX_NumOps.append(0)
	objs[o].listOP_JMP_EBX_NumOps.append(0)
	objs[o].listOP_JMP_ECX_NumOps.append(0)
	objs[o].listOP_JMP_EDX_NumOps.append(0)
	objs[o].listOP_JMP_ESI_NumOps.append(0)
	objs[o].listOP_JMP_EDI_NumOps.append(0)
	objs[o].listOP_JMP_ESP_NumOps.append(0)  
	objs[o].listOP_JMP_EBP_NumOps.append(0)

def DoEverythingFunc():
	global numPE
	global levelTwo
	global getCALL
	global getJMP
	global RegsDG
	global Regs
	global CheckallModules
	global InputAcceptable
	global Input
	global RegsPrint
	global modName
	Input = copy.copy(InputAcceptable)
	#Input = ["ja", "jb", "jc", "jd", "jdi","jsi", "jbp", "j", "c", "ca","cb", "cc", "cd", "cdi", "csi","cbp", "ma", "a", "s", "m","d", "move", "mov", "movv", "movs","l", "xc", "st", "po", "pu","id", "inc", "dec", "bit", "sl","sr", "rr", "rl", "all", "rec","da", "db", "dc", "dd", "ddi","dsi", "dbp", "dis","ba", "bb", "bc", "bd", "bdi","bsi", "bbp", "bdis","oa", "ob", "oc", "od", "odi","osi", "obp", "odis"]
	
	levelTwo = False
	getCALL = True
	getJMP = True
	RegsDG = ["EAX", "EBX", "ECX", "EDX", "ESI", "EDI", "EBP", "ESP"]
	#RegsDG = ["EAX" ] #, "EBX", "ECX", "EDX", "ESI", "EDI", "EBP"]
	get_OP_JMP_EAX(NumOpsD)
	get_OP_JMP_EBX(NumOpsD)
	get_OP_JMP_ECX(NumOpsD)
	get_OP_JMP_EDX(NumOpsD)
	get_OP_JMP_EDI(NumOpsD)
	get_OP_JMP_ESI(NumOpsD)
	get_OP_JMP_ESP(NumOpsD)
	get_OP_JMP_EBP(NumOpsD)
	get_OP_CALL_EAX(NumOpsD)
	get_OP_CALL_EBX(NumOpsD)
	get_OP_CALL_ECX(NumOpsD)
	get_OP_CALL_EDX(NumOpsD)
	get_OP_CALL_EDI(NumOpsD)
	get_OP_CALL_ESI(NumOpsD)
	get_OP_CALL_EBP(NumOpsD)
	get_OP_CALL_ESP(NumOpsD)
	get_OP_JMP_PTR_EAX(NumOpsD)
	get_OP_JMP_PTR_EBX(NumOpsD)
	get_OP_JMP_PTR_ECX(NumOpsD)
	get_OP_JMP_PTR_EDX(NumOpsD)
	get_OP_JMP_PTR_ESI(NumOpsD)
	get_OP_JMP_PTR_EDI(NumOpsD)
	get_OP_JMP_PTR_EBP(NumOpsD)
	get_OP_JMP_PTR_ESP(NumOpsD)
	get_OP_CALL_PTR_EAX(NumOpsD)
	get_OP_CALL_PTR_EBX(NumOpsD)
	get_OP_CALL_PTR_ECX(NumOpsD)
	get_OP_CALL_PTR_EDX(NumOpsD)
	get_OP_CALL_PTR_ESI(NumOpsD)
	get_OP_CALL_PTR_EDI(NumOpsD)
	get_OP_CALL_PTR_EBP(NumOpsD)
	get_OP_CALL_PTR_ESP(NumOpsD)
	CheckallModules = True
	Regs = ["EAX" , "EBX", "ECX", "EDX", "ESI", "EDI", "EBP", "ESP"]
	#Regs = ["EAX" ] #, "EBX", "ECX", "EDX", "ESI", "EDI", "EBP"]
	RegsPrint = ["EAX" , "EBX", "ECX", "EDX", "ESI", "EDI", "EBP", "ESP"]
	#RegsPrint = ["EAX"] # , "EBX", "ECX", "EDX", "ESI", "EDI", "EBP", "ALL"]
	ObtainAndExtractDlls()
	runIt() 
	# runGetRegsDG()  # runGetRegsDGNew built into RunIt now
	getStatisticalResults()
	runPrintS()
	finalPrintSub2()
	clearAllObject()
	clearAll()
	numPE -= 1


def generateCSV():
	global numPE
	global levelTwo
	global getCALL
	global getJMP
	global RegsDG
	global Regs
	global CheckallModules
	global InputAcceptable
	global Input
	global RegsPrint
	global modName
	Input = copy.copy(InputAcceptable)
	#Input = ["ja", "jb", "jc", "jd", "jdi","jsi", "jbp", "j", "c", "ca","cb", "cc", "cd", "cdi", "csi","cbp", "ma", "a", "s", "m","d", "move", "mov", "movv", "movs","l", "xc", "st", "po", "pu","id", "inc", "dec", "bit", "sl","sr", "rr", "rl", "all", "rec","da", "db", "dc", "dd", "ddi","dsi", "dbp", "dis","ba", "bb", "bc", "bd", "bdi","bsi", "bbp", "bdis","oa", "ob", "oc", "od", "odi","osi", "obp", "odis"]
	
	levelTwo = False
	getCALL = True
	getJMP = True
	RegsDG = ["EAX", "EBX", "ECX", "EDX", "ESI", "EDI", "EBP"]
	#RegsDG = ["EAX" ] #, "EBX", "ECX", "EDX", "ESI", "EDI", "EBP"]
	get_OP_JMP_EAX(NumOpsD)
	get_OP_JMP_EBX(NumOpsD)
	get_OP_JMP_ECX(NumOpsD)
	get_OP_JMP_EDX(NumOpsD)
	get_OP_JMP_EDI(NumOpsD)
	get_OP_JMP_ESI(NumOpsD)
	get_OP_JMP_ESP(NumOpsD)
	get_OP_JMP_EBP(NumOpsD)
	get_OP_CALL_EAX(NumOpsD)
	get_OP_CALL_EBX(NumOpsD)
	get_OP_CALL_ECX(NumOpsD)
	get_OP_CALL_EDX(NumOpsD)
	get_OP_CALL_EDI(NumOpsD)
	get_OP_CALL_ESI(NumOpsD)
	get_OP_CALL_EBP(NumOpsD)
	get_OP_CALL_ESP(NumOpsD)
	get_OP_JMP_PTR_EAX(NumOpsD)
	get_OP_JMP_PTR_EBX(NumOpsD)
	get_OP_JMP_PTR_ECX(NumOpsD)
	get_OP_JMP_PTR_EDX(NumOpsD)
	get_OP_JMP_PTR_ESI(NumOpsD)
	get_OP_JMP_PTR_EDI(NumOpsD)
	get_OP_JMP_PTR_EBP(NumOpsD)
	get_OP_JMP_PTR_ESP(NumOpsD)
	get_OP_CALL_PTR_EAX(NumOpsD)
	get_OP_CALL_PTR_EBX(NumOpsD)
	get_OP_CALL_PTR_ECX(NumOpsD)
	get_OP_CALL_PTR_EDX(NumOpsD)
	get_OP_CALL_PTR_ESI(NumOpsD)
	get_OP_CALL_PTR_EDI(NumOpsD)
	get_OP_CALL_PTR_EBP(NumOpsD)
	get_OP_CALL_PTR_ESP(NumOpsD)
	CheckallModules = True
	Regs = ["EAX" , "EBX", "ECX", "EDX", "ESI", "EDI", "EBP"]
	# Regs = ["EAX" ] #, "EBX", "ECX", "EDX", "ESI", "EDI", "EBP"]
	RegsPrint = ["EAX" , "EBX", "ECX", "EDX", "ESI", "EDI", "EBP", "ESP"]
	# RegsPrint = ["EAX"] # , "EBX", "ECX", "EDX", "ESI", "EDI", "EBP", "ALL"]
	ObtainAndExtractDlls()
	runIt()
	# runGetRegsDG() # runGetRegsDGNew built into runit now
	getStatisticalResults()
	clearAllObject()
	clearAll()
	numPE -= 1

def CheckDoEverything():
	global peName
	global PE_path
	global numPE
	global modName
	global PEsList
	global PEsList_Index
	while numPE > 0:
		print "num pe: " + str(numPE)
		sp()
		PEsList_Index += 1

		peName = PEsList[PEsList_Index]
		head, tail = os.path.split(peName)
		peName = tail
		modName = tail
		PE_path = head
		print "pe name: " + str(peName)
		sp()
		Extraction()
		DoEverythingFunc()
		#numPE -= 1
		print "num pe: " + str(numPE)
		sp()
def findEvilImports():
	global FoundApisAddress
	for item in pe.DIRECTORY_ENTRY_IMPORT:
		for i in item.imports:
			FoundApisName.append(str(i.name))
			saveAPI = hex(i.address)
			FoundApisAddress.append(saveAPI)



def findVirtualProtect(a):
	global VPl
	for i, each in enumerate(FoundApisName):
		matchObj = re.match( r'VirtualProtect', FoundApisName[i] , re.M|re.I)
		if  matchObj:
			if  checkBadChar(fixHexAddy(FoundApisAddress[i])):
				VP =  fixHexAddy(FoundApisAddress[i])  + " # (ptr to " + FoundApisName[i] + ")"
				VPl.append(fixHexAddy(FoundApisAddress[i]))
				if a == 1:
					return VP
				if a == 0:
					return str(fixHexAddy(FoundApisAddress[i]) )
			else:
				if a == 1:
					return "0xdeadc0de # (ptr to VirtualProtect not found)"
				if a == 0:
					return "0xdeadc0de"
	if a == 1:
		return "0xdeadc0de # (ptr to VirtualProtect not found)*"
	if a == 0:
		return "0xdeadc0de"



def findVirtualAlloc(a):
	global VAl
	for i, each in enumerate(FoundApisName):
		matchObj = re.match( r'VirtualAlloc', FoundApisName[i] , re.M|re.I)
		if  matchObj:
			if  checkBadChar(fixHexAddy(FoundApisAddress[i])):
				VA =  fixHexAddy(FoundApisAddress[i])  + " # (ptr to " + FoundApisName[i] + ")"
				VAl.append(fixHexAddy(FoundApisAddress[i]))
				if a == 1:
					return VA, True
				if a == 0:
					return str(fixHexAddy(FoundApisAddress[i]) ), True
	t, truth = findVirtualAllocEx(a)
	if a == 1:
		return t, False
	if a == 0:
		return t, False
def findVirtualAllocEx(a):
	global VAl
	for i, each in enumerate(FoundApisName):
		matchObj = re.match( r'VirtualAllocex', FoundApisName[i] , re.M|re.I)
		if  matchObj:
			if  checkBadChar(fixHexAddy(FoundApisAddress[i])):
				VA =  fixHexAddy(FoundApisAddress[i])  + " # (ptr to " + FoundApisName[i] + ")"
				VAl.append(fixHexAddy(FoundApisAddress[i]))
				if a == 1:
					return VA, True
				if a == 0:
					return str(fixHexAddy(FoundApisAddress[i]) ), True
	if a == 1:
		return "0xdeadc0de # (ptr to VirtualAlloc not found)**", False
	if a == 0:
		return "0xdeadc0de", False

def findMemcpy(a):
	global MA1
	global MA
	for i, each in enumerate(FoundApisName):
		matchObj = re.match( r'memcpy', FoundApisName[i] , re.M|re.I)
		if  matchObj:
			if  checkBadChar(fixHexAddy(FoundApisAddress[i])):
				MA =  fixHexAddy(FoundApisAddress[i])  + " # (ptr to " + FoundApisName[i] + ")"
				MAl.append(fixHexAddy(FoundApisAddress[i]))
				if a == 1:
					return MA, True
				if a == 0:
					return str(fixHexAddy(FoundApisAddress[i]) ), True
	t, truth = findwMemcpy(a)
	
	if a == 1:
		return t, False
	if a == 0:
		return t, False

def findwMemcpy(a):
	global MAl
	global MA
	for i, each in enumerate(FoundApisName):
		matchObj = re.match( r'wmemcpy', FoundApisName[i] , re.M|re.I)
		if  matchObj:
			if  checkBadChar(fixHexAddy(FoundApisAddress[i])):
				MA =  fixHexAddy(FoundApisAddress[i])  + " # (ptr to " + FoundApisName[i] + ")"
				MAl.append(fixHexAddy(FoundApisAddress[i]))
				if a == 1:
					return MA, True
				if a == 0:
					return str(fixHexAddy(FoundApisAddress[i]) ), True
	t, truth = findMemmove(a)
	if a == 1:
		return t, False
	if a == 0:
		return t, False

def findMemmove(a):
	global MAl
	global MA
	for i, each in enumerate(FoundApisName):
		matchObj = re.match( r'_memmove', FoundApisName[i] , re.M|re.I)
		if  matchObj:
			if  checkBadChar(fixHexAddy(FoundApisAddress[i])):
				MA =  fixHexAddy(FoundApisAddress[i])  + " # (ptr to " + FoundApisName[i] + ")"
				MAl.append(fixHexAddy(FoundApisAddress[i]))
				if a == 1:
					return MA, True
				if a == 0:
					return str(fixHexAddy(FoundApisAddress[i]) ), True
	t, truth = findwwmemmove(a)
	if a == 1:
		return t, False
	if a == 0:
		return t, False
def findwwmemmove(a):
	global MAl
	global MA
	for i, each in enumerate(FoundApisName):
		matchObj = re.match( r'wmemmove', FoundApisName[i] , re.M|re.I)
		if  matchObj:
			if  checkBadChar(fixHexAddy(FoundApisAddress[i])):
				MA =  fixHexAddy(FoundApisAddress[i])  + " # (ptr to " + FoundApisName[i] + ")"
				MAl.append(fixHexAddy(FoundApisAddress[i]))
				if a == 1:
					return MA, True
				if a == 0:
					return str(fixHexAddy(FoundApisAddress[i]) ), True

	t= "0xdeadc0de, # Pointers to memcpy, wmemcpy not found"
	if a == 1:
		return t, False
	if a == 0:
		return t, False

def fixHexAddy(addy):
	str_hexnum =  addy.rstrip("L").lstrip("0x") or "0"
	return '0x' + '0'* (8 - len(str_hexnum)) + str_hexnum

def findGetProcessAddress(a):
	global GPAl
	for i, each in enumerate(FoundApisName):
		matchObj = re.match( r'GetProcAddress', FoundApisName[i] , re.M|re.I)
		if  matchObj:
			if  checkBadChar(fixHexAddy(FoundApisAddress[i])):
				GPA =  fixHexAddy(FoundApisAddress[i])  + " # (ptr to " + FoundApisName[i] + ")"
				GPAl.append(fixHexAddy(FoundApisAddress[i]))
				if a == 1:
					return GPA
				if a == 0:
					return str(fixHexAddy(FoundApisAddress[i]) )
			else:
				if a == 1:
					return "0xdeadc0de # (ptr to GetProcAddress not found)"
				if a == 0:
					return "0xdeadc0de"
	if a == 1:
		return "0xdeadc0de # (ptr to GetProcAddress not found)*"
	if a == 0:
		return "0xdeadc0de"

def paddingMaker4Bytes(a, num):
	a = a-1
	pad0=num*"\t"
	if (a==0):
		pad =  "\n"+pad0+"0x41414141 "
	elif (a>0):
		pad =  "\n"+pad0+"0x41414141, "
	pad2 = a * "0x41414141, "
	x=(len(pad2))
	pad2=pad2[0:(x-2)] # fix my
	return pad + pad2 + " # padding for dispatch table (" + str(hex((a+1)*4)) + " bytes)\n"
	#		addArray.append(fixHexAddy(add4) + " # " + "(base + " + addb + ") ")

def oldpaddingMakerVP_Stack(a):

	b=a/4
	instr="42"*a
	text="vp_stack = struct.pack('<L', 0x00427008) # ptr -> VirtualProtect()"



def pivotToEsp(a):
	add = "\t\t0xdeadc0de, # pivot esp # placeholder for more complicated code\n"
	return add

	#nowesp




def paddingMakerVP_Stack(a):
	try:
		b=a/4
	except:
		b=0
		a=0
	try:
		modb= a % 4  # modulo, remainder
	except:
		modb=0
	instr="42"*int(a)
	text=b*"vp_stack = struct.pack('<L', 0x42424242) # filler | 4 bytes\n"
	if modb >0:
		text2=modb*"vp_stack = struct.pack('<L', 0x"+modb*"43"+") \t# filler | " + str(modb) + " bytes\n"
		text +=text2
	return text
def paddingMakerDG_Stack(a):
	try:
		b=a/4
	except:
		b=0
		a=0
	try:
		modb= a % 4  # modulo, remainder
	except:
		modb=0
	text=b*"\t\t0x43434343, # compensatory filler | 4 bytes\n"
	if modb >0:
		text2=modb*"\t\t0x"+modb*"43"+", \t# filler | " + str(modb) + " bytes\n"
		text +=text2
	return text	

#fvp

def StartDEPBypass():

	### Need to do only once!!!
	buildPopRets()



	####PER REGISTER - needs to be run once for each search for a reg
	prepTasksVP(Reg)
	FinalVP()
def prepTasksVP(Reg, numDistinctPivots):
	# printlistOP_SP3(NumOpsD, Reg)
	s1, s2=getStackPivotAsLists(NumOpsD, Reg)
	# doStackPivotTasks(s1,s2,paddingMaker4Bytes(2,2))

	doStackPivotTasks(s1,s2, Reg)
	# out += paddingMaker1(6)
def FinalVP(Reg, numDistinctPivots):
	# vpcounter()
	truth=False
	###make it so you only have to do calls once??? 
	global save3
	prepTasksVP(Reg,0)
	# out = "\nSet up for Register: " + Reg
	out="\n* * * * * * * * * * * * * * * * * * * * * * * * * * * *\nVirtualProtect() JOP chain set up for functional gadgets ending in Jmp/Call " + Reg+ " " + vpCt()+"\n"
	out+="\n\nimport struct\n"
	# out+="\n\n\t#Need set up for JOP dispatcher gadget -- not provided\n\n"
	dgOut,dgBytesNeeded=preLoad(Reg)
	out += ""+ dgOut
	
	# print "dbytes " + str(dgBytesNeeded)
	try:
		stackFiller=dgBytesNeeded
		if dgBytesNeeded==0:
			stackFiller=4
		# print "yes"
	except:
		# print ""
		stackFiller=4
	stackPivotInsertFiller(paddingMaker1(stackFiller))

	out += "\n\ndef create_jop_chain():\n"
	out += "\tjop_gadgets = [\n"
	try:
		outVPtasks, truth = doVPVAtasks(numDistinctPivots)
		# print "huh33: " + outVPtasks
		out += "\t"+outVPtasks
		if truth:
		# print "vcount"
			vpcounter()
	except:
		out += "# Need stack pivots - none were found"
	# out += paddingMaker4Bytes(2,2)
	out +=""+paddingMaker1(stackFiller)
	gadget, gadgetBytesNeeded, popReg = findVPVAPop(Reg)
	# print "findvpgadget"
	# print gadget
	out += "\t\t"+gadget + "# Set up pop for VP "
	out += "\t\t# Need " + str(gadgetBytesNeeded) +" bytes filler, for what was done after pop " + popReg + "\n"
	# do do -- compensatory pop
	try:
		out +=  "\t\t"+preprocessOP_JMPPTR(NumOpsD, popReg) + " # JMP to ptr for VirtualProtect\n"
	except:
		out +=  "\t\t 0xdeadc0de,# NOT found - JMP to ptr for VirtualProtect\n"
	out += "\t\t# JOP Chain gadgets are checked *only* to generate the desired stack pivot\n"
	out += "\t]\n"
	out += "\treturn ''.join(struct.pack('<I', _) for _ in jop_gadgets)\n\n"
	out += "rop_chain=create_rop_chain()\n"
	out += "jop_chain=create_jop_chain()\n\n"

	out += "vp_stack = struct.pack('<L', " + findVirtualProtect(0) + ") # ptr -> VirtualProtect()\n" 

	if (gadgetBytesNeeded > 0):
		out +=  paddingMakerVP_Stack(gadgetBytesNeeded) + " Padding for extra pop(s)"
	out += "vp_stack += struct.pack('<L', 0x0042DEAD) # return address  <-- where on the stack you want it to return\n" 
	out += "vp_stack += struct.pack('<L', 0x00425000) # lpAddress  <-- Where on the stack you want to start modifying proctection\n"  
	out += "vp_stack += struct.pack('<L', 0x000003e8) # dwsize  <-- Size: 1000\n" 
	out += "vp_stack += struct.pack('<L', 0x00000040) # flNewProtect <-- RWX\n" 
	out += "vp_stack += struct.pack('<L', 0x00420000) # lpflOldProtect <--  MUST be writable location\n\n"
	out += "shellcode = '\\xcc\\xcc\\xcc\\xcc'\n" 
	out += "nops = '\\x90' * 1\n" 
	out += "padding = '\\x41' * 1\n\n" 
	out += "payload = padding + ropchain + jop_chain + vp_stack + nops + shellcode\t# Payload set up may vary greatly\n\nThis was created by the JOP ROCKET\n\n"


	if (truth == False) & (save3 > 0):
		out="\t# JOP chain generation skipped--No stack pivots found"
		out += "svae3 " + str(save3)
		if (save3 > 0):
			out=""

	save3+=1
	# out += "svae3 " + str(save3)
	
	clearListSpecialPOP()
	clearGlobalOutputs()
	clearAllSPSpecialArrays()
	return out

def callstoVP():
	Regs =["EAX", "ECX","EBX","EDI"]
	RegsPrint = ["EDX"]
	findEvilImports()
	print "GetProcAddress: " + str(findGetProcessAddress(1))
	print "VA: " + str(findVirtualAlloc(1))
	print "VP: " + str(findVirtualProtect(1))

	idval=1
	while os.path.exists("%s-VirtualProtect_%s.txt" % (peName, idval)):
	    idval += 1
	filename = peName +"-"+"VirtualProtect_" + str(idval) + ".txt"

	with open(filename, 'a') as f:
		# print >> f, FinalVP(Reg)
		# final = "vp1: "+FinalVP("EAX",1)
		# final += "vp3: "+FinalVP("EAX",2)
		# # preprocessOP_SP(NumOpsD, "ECX")
		# final += "vp6: "+FinalVP("EDX",0)

		# final += "vp4: "+FinalVP("EAX",1)
		# final += "vp5: "+FinalVP("EAX",2)

		outs =""
		for each in Regs:
			t=1
			for x in range(2):
				outs +="vp6: "+FinalVP(each,0)
				t+-1
			clearSave()  # Need clear save to help reset
		outs +="vp7: "+FinalVP("EBX",0)
			# clearPStart()
		# print final
	print outs

def preLoad(Reg):
	# print "preload reg "  + Reg
	out=""
	out += "\ndef create_rop_chain():\n"
	out += "\trop_gadgets = [\n"
	dispatcherReg, drbytes = calcRegforDispatcher(Reg)
	dTable, dtbytes, dtReg =  calcRegforDispatchTable(Reg)	
	truth, DG, dgBytes = preprocessOP_DG(NumOpsD, dtReg)

	# Set up dispatcher gadget
	out +=  "\t\t"+dispatcherReg + "  Load " + Reg +  " with address for dispatcher gadget!\n"  # pop REG / ret -> load dispatcher
	if truth:
		out +=  "\t\t"+ DG + "\t#This is one possible dispatcher gadget, which may or may not be viable, with " +  str(dgBytes) +  " bytes between dispatch table slots!\n" #"0xdeadc0de) # Address for your dispatcher gadget!\n"
	else:
		out += "\t\t0xdeadc0de, # Address for your dispatcher gadget!\n"
	if (drbytes > 0):
		out += 	""+paddingMaker1(drbytes)

	# set up dispatch table

	out += "\t\t" + dTable + "Load " + dtReg + " with address of dispatch table\n"	# pop REG  / ret -> load table address
	out += "\t\t0xdeadbeef, # Address for your dispatcher table!\n"
	if (dtbytes > 0):
		out +=  ""+paddingMaker1(dtbytes)	


	# jump to dispatcher gadget!
	out +=  "\t\t"+preprocessOP_JMP(NumOpsD, Reg) + " # JMP to dispatcher gadget; start the JOP!\n"
	out += "\t]\n"
	out += "\treturn ''.join(struct.pack('<I', _) for _ in rop_gadgets)\n\n"


	
	return out, dgBytes

	

def FinalVA(Reg, numDistinctPivots):
	
	truth=False
	###make it so you only have to do calls once??? 
	global save3
	prepTasksVP(Reg,0)
	# out = "\nSet up for Register: " + Reg
	out="\n* * * * * * * * * * * * * * * * * * * * * * * * * * * *\nVirtualAlloc() JOP chain set up for functional gadgets ending in Jmp/Call " + Reg+ " " + vaCt() + "\n"
	out+="\n\nimport struct\n"
	# out+="\n\n\t#Need set up for JOP dispatcher gadget -- not provided\n\n"
	dgOut,dgBytesNeeded=preLoad(Reg)
	out += ""+ dgOut
	
	# print "dbytes " + str(dgBytesNeeded)
	try:
		stackFiller=dgBytesNeeded
		if dgBytesNeeded==0:
			stackFiller=4
		# print "yes"
	except:
		# print ""
		stackFiller=4
	stackPivotInsertFiller(paddingMaker1(stackFiller))

	out += "\n\ndef create_jop_chain():\n"
	out += "\tjop_gadgets = [\n"
	try:
		outVPtasks, truth = doVPVAtasks(numDistinctPivots)
		# print "huh33: " + outVPtasks
		out += "\t"+outVPtasks
		if truth:
			# print "vcount"
			vacounter()
		
	except:
		out += "# Need stack pivots - none were found"
	out +=""+paddingMaker1(stackFiller)
	gadget, gadgetBytesNeeded, popReg = findVPVAPop(Reg)
	# print "findvpgadget"
	# print gadget
	out += "\t\t"+gadget + "# Set up pop for VP "
	out += "\t\t# Need " + str(gadgetBytesNeeded) +" bytes filler, for what was done after pop " + popReg + "\n"
	# do do -- compensatory pop
	try:
		out +=  "\t\t"+preprocessOP_JMPPTR(NumOpsD, popReg) + " # JMP to ptr for VirtualAlloc\n"
	except:
		out +=  "\t\t0xdeadc0de,# NOT found - JMP to ptr for VirtualAlloc\n"
	out += "\t\t# JOP Chain gadgets are checked *only* to generate the desired stack pivot\n"
	out += "\t]\n"
	out += "\treturn ''.join(struct.pack('<I', _) for _ in jop_gadgets)\n\n"
	out += "rop_chain=create_rop_chain()\n"
	out += "jop_chain=create_jop_chain()\n\n"

	tempVA, tr1 = findVirtualAlloc(0)
	tempMem, tr2 =findMemcpy(0)

	out += "vp_stack = struct.pack('<L', " +tempVA + ") # ptr -> VirtualAlloc()\n" 

	if (gadgetBytesNeeded > 0):
		out += ""	+ paddingMakerVP_Stack(gadgetBytesNeeded) + " Padding for extra pop(s)"

	out += "vp_stack += struct.pack('<L', " + tempMem + ") # return address  <-- where on the stack you want it to return - here we are chaining it together with memcpy\n" 
	out += "vp_stack += struct.pack('<L', 0x00625000) # lpAddress  <-- Where on the stack you want to start modifying protection\n"  
	out += "vp_stack += struct.pack('<L', 0x000003e8) # dwsize  <-- Size: 1000\n" 
	out += "vp_stack += struct.pack('<L', 0x00001000) # flAllocationType <-- 100, MEM_COMMIT\n" 
	out += "vp_stack += struct.pack('<L', 0x00000040) # flProtect <--RWX, PAGE_EXECUTE_READWRITE\n"
	out += "vp_stack += struct.pack('<L', 0x00625000) # *Same* address as lpAddress--where the execution jumps after memcpy()\n"
	out += "vp_stack += struct.pack('<L', 0x00625000) # *Same* address as lpAddress--i.e. desination address for memcpy()"
	out += "vp_stack += struct.pack('<L', 0xffffdddd) # memcpy() destination address--i.e. Source address for shellcode\n" 
	out += "vp_stack += struct.pack('<L', 0x00002000) # mempcpy() size parameter--size of shellcode \n#This is one possible VirtualAlloc() chain; other possibilities exist!\n\n" 
	out += "shellcode = '\\xcc\\xcc\\xcc\\xcc # '\\xcc' is a breakpoint.\n"  
	out += "nops = '\\x90' * 1\n" 
	out += "padding = '\\x41' * 1\n\n" 
	out += "payload = padding + ropchain + jop_chain + vp_stack + nops + shellcode\t# Payload set up may vary greatly\n\nThis was created by the JOP ROCKET.\n\n"

	if (truth == False) & (save3 > 0):
		out="\t# JOP chain generation skipped for VirtualAlloc--No stack pivots found"
		out += "svae3 " + str(save3)
		if (save3 > 0):
			out=""
	save3+=1
	# out += "svae3 " + str(save3)
	
	clearListSpecialPOP()
	clearGlobalOutputs()
	clearAllSPSpecialArrays()
	# print out
	# print "here"+Reg+"6"
	return out
	
def findVPVAPop(Reg):
	# Reg = "ebx"
	# print "vppop "  + Reg
	# print checkPtrEAX()
	# print checkPtrEBX()
	# print checkPtrECX()
	# print checkPtrEDX()
	# print checkPtrEDI()
	# print checkPtrESI()
	# print checkPtrEBP()
	# print checkPtrESP()
	
	# print "answer"
	boolStart, popReg, cMode= startPreProcessOp(Reg)

	# print "boolstart " + str(boolStart)
	# print "answer2"
	Reg = Reg.lower()
	# popReg = "ecx"
	best=3
	gadget=""
	gadgetBytesNeeded=""
	# print "eax: " + str(len(objs[0].specialPOPGadgetEAX))
	# print "ebx: " + str(len(objs[0].specialPOPGadgetEBX))
	# print "ecx: " + str(len(objs[0].specialPOPGadgetECX))
	# print "edx: " + str(len(objs[0].specialPOPGadgetEDX))
	# print "esi: " + str(len(objs[0].specialPOPGadgetESI))
	# print "edi: " + str(len(objs[0].specialPOPGadgetEDI))
	# print "ebp: " + str(len(objs[0].specialPOPGadgetEBP))
	# print "esp: " + str(len(objs[0].specialPOPGadgetESP))
	

	if Reg == "eax":
		try:
			gadget = objs[o].specialPOPGadgetBestEAX[0]
			gadgetBytesNeeded =  objs[o].specialPOPBytesBestEAX[0]
			# print gadget
			# print "besteax"
		except:
			try:
				gadget=objs[o].specialPOPGadgetEAX[0]
				gadgetBytesNeeded=objs[o].specialPOPBytesEAX[0]
				# print gadget
				# print "notbesteax"
			except:
				# print "We ain't got nothing"
				gadget="0xdeadc0de, # Pop " + popReg + " not found "
				gadgetBytesNeeded=0
	if Reg == "ebx":
		try:
			gadget = objs[o].specialPOPGadgetBestEBX[0]
			gadgetBytesNeeded =  objs[o].specialPOPBytesBestEBX[0]
			# print gadget
		except:
			try:
				gadget=objs[o].specialPOPGadgetEBX[0]
				gadgetBytesNeeded=objs[o].specialPOPBytesEBX[0]			
				# print gadget
			except:
				# print "We ain't got nothing"
				gadget="0xdeadc0de, # Pop " + popReg + " not found "
				gadgetBytesNeeded=0
	if Reg == "ecx":
		try:
			gadget = objs[o].specialPOPGadgetBestECX[0]
			gadgetBytesNeeded =  objs[o].specialPOPBytesBestECX[0]
			# print gadget
		except:
			try:
				gadget=objs[o].specialPOPGadgetECX[0]
				gadgetBytesNeeded=objs[o].specialPOPBytesECX[0]			
				# print gadget
			except:
				# print "We ain't got nothing"
				gadget="0xdeadc0de, # Pop " + popReg + " not found "
				gadgetBytesNeeded=0
	if Reg == "edx":
		try:
			gadget = objs[o].specialPOPGadgetBestEDX[0]
			gadgetBytesNeeded =  objs[o].specialPOPBytesBestEDX[0]
			# print gadget
		except:
			try:
				gadget=objs[o].specialPOPGadgetEDX[0]
				gadgetBytesNeeded=objs[o].specialPOPBytesEDX[0]			
				# print gadget
			except:
				# print "We ain't got nothing"
				gadget="0xdeadc0de, # Pop " + popReg + " not found "
				gadgetBytesNeeded=0
	if Reg == "esi":
		try:
			gadget = objs[o].specialPOPGadgetBestESI[0]
			gadgetBytesNeeded =  objs[o].specialPOPBytesBestESI[0]
			# print gadget
		except:
			try:
				gadget=objs[o].specialPOPGadgetESI[0]
				gadgetBytesNeeded=objs[o].specialPOPBytesESI[0]			
				# print gadget
			except:
				# print "We ain't got nothing"
				gadget="0xdeadc0de, # Pop " + popReg + " not found "
				gadgetBytesNeeded=0
	if Reg == "edi":
		try:
			gadget = objs[o].specialPOPGadgetBestEDI[0]
			gadgetBytesNeeded =  objs[o].specialPOPBytesBestEDI[0]
			# print gadget
		except:
			try:
				gadget=objs[o].specialPOPGadgetEDI[0]
				gadgetBytesNeeded=objs[o].specialPOPBytesEDI[0]			
				# print gadget
			except:
				# print "We ain't got nothing"
				gadget="0xdeadc0de, # Pop " + popReg + " not found "
				gadgetBytesNeeded=0
	if Reg == "esp":
		try:
			gadget = objs[o].specialPOPGadgetBestESP[0]
			gadgetBytesNeeded =  objs[o].specialPOPBytesBestESP[0]
			# print gadget
		except:
			try:
				gadget=objs[o].specialPOPGadgetESP[0]
				gadgetBytesNeeded=objs[o].specialPOPBytesESP[0]			
				# print gadget
			except:
				# print "We ain't got nothing"
				gadget="0xdeadc0de, # Pop " + popReg + " not found "
				gadgetBytesNeeded=0
	if Reg == "ebp":
		try:
			gadget = objs[o].specialPOPGadgetBestEBP[0]
			gadgetBytesNeeded =  objs[o].specialPOPBytesBestEBP[0]
			# print gadget
		except:
			try:
				gadget=objs[o].specialPOPGadgetEBP[0]
				gadgetBytesNeeded=objs[o].specialPOPBytesEBP[0]	
				# print gadget
			except:
				# print "We ain't got nothing"
				gadget="0xdeadc0de, # Pop " + popReg + " not found "
				gadgetBytesNeeded=0		


	# print "True final:"
	# print gadget
	# print gadgetBytesNeeded
	return gadget, gadgetBytesNeeded, popReg


#pre
def startPreProcessOp(Reg):
	# print "my reg " +  Reg 
	# print "start"
	# print checkPtrEAX()
	cMode="best"
	Reg=Reg.lower()
	popReg = "eax"
	if checkPtrEAX() & (Reg != popReg):
		# print "here2"
		preprocessOP_Pop(NumOpsD, popReg, Reg, best, cMode)
		# print "here2b"
		# print len(objs[o].specialPOPGadgetBestEAX)
		# for e in objs[o].specialPOPGadgetBestEAX:
			# print e
		if checkSpPop(Reg, "best"):
			# print "1found eax"
			# print "returning " + popReg + " which is not "  + Reg
			return True, popReg,cMode
		else:
			# print "clearing special pop"
			clearListSpecialPOP()
	# print "start2"
	popReg = "ebx"
	if checkPtrEBX()& (Reg != popReg):
		# print "here3"
		preprocessOP_Pop(NumOpsD, popReg, Reg, best, cMode)
		# print "ebx-f3"
		#now44
		# for e in objs[o].specialPOPGadgetBestEBX:
			# print e
		if checkSpPop(Reg, cMode):
			# print "1found ebx"
			return True, popReg,cMode
		else:
			clearListSpecialPOP()
	# print "start3"
	popReg = "ecx"
	if checkPtrECX() & (Reg != popReg):
		preprocessOP_Pop(NumOpsD, popReg, Reg, best, cMode)
		if checkSpPop(Reg, cMode):
			# print "1found ecx"
			return True, popReg,cMode
		else:
			clearListSpecialPOP()
	# print "start4"			
	popReg = "edx"
	if checkPtrEDX() & (Reg != popReg):
		
		preprocessOP_Pop(NumOpsD, popReg, Reg, best, cMode)
		if checkSpPop(Reg, cMode):
			# print "1found edx"
			return True, popReg,cMode
		else:
			clearListSpecialPOP()
	popReg = "edi"
	# print "start5"
	if checkPtrEDI() & (Reg != popReg):
		preprocessOP_Pop(NumOpsD, popReg, Reg, best, cMode)
		if checkSpPop(Reg, cMode):
			# print "1found edi"
			return True, popReg,cMode
		else:
			clearListSpecialPOP()
	# print "start6"
	popReg = "esi"
	if checkPtrESI() & (Reg != popReg):
		preprocessOP_Pop(NumOpsD, popReg, Reg, best, cMode)
		if checkSpPop(Reg, cMode):
			# print "1found esi"
			return True, popReg,cMode
		else:
			clearListSpecialPOP()
	# print "start7"
	popReg = "ebp"
	if checkPtrEBP() & (Reg != popReg):
		preprocessOP_Pop(NumOpsD, popReg, Reg, best, cMode)
		if checkSpPop(Reg, cMode):
			# print "1found ebp"
			return True, popReg,cMode
		else:
			clearListSpecialPOP()
	# print "start8"
	popReg = "esp"
	if checkPtrESP() & (Reg != popReg):
		preprocessOP_Pop(NumOpsD, popReg, Reg, best, cMode)
		if checkSpPop(Reg, cMode):
			# print "1found esp"
			return True, popReg,cMode
		else:
			clearListSpecialPOP()


	cMode="ok"
	popReg = "eax"
	if checkPtrEAX()  & (Reg != popReg):
		preprocessOP_Pop(NumOpsD, popReg, Reg, best, cMode)
		if checkSpPop(Reg, cMode):
			# print "2found eax"
			return True, popReg,cMode
		else:
			# print "clearing special pop"
			clearListSpecialPOP()
	popReg = "ebx"
	if checkPtrEBX() & (Reg != popReg):
		preprocessOP_Pop(NumOpsD, popReg, Reg, best, cMode)
		if checkSpPop(Reg, cMode):
			# print "2found ebx"
			return True, popReg,cMode
		else:
			clearListSpecialPOP()
	popReg = "ecx"
	if checkPtrECX() & (Reg != popReg):
		# print "popecx"
		preprocessOP_Pop(NumOpsD, popReg, Reg, best, cMode)
		if checkSpPop(Reg, cMode):
			# print "2found ecx"
			return True, popReg,cMode
		else:
			clearListSpecialPOP()
	popReg = "edx"
	# print "checkedx"
	if checkPtrEDX() & (Reg != popReg):
		preprocessOP_Pop(NumOpsD, popReg, Reg, best, cMode)
		if checkSpPop(Reg, cMode):
			# print "2found edx"
			return True, popReg,cMode
		else:
			clearListSpecialPOP()
	popReg = "edi"
	if checkPtrEDI() & (Reg != popReg):
		preprocessOP_Pop(NumOpsD, popReg, Reg, best, cMode)
		if checkSpPop(Reg, cMode):
			# print "2found edi"
			return True, popReg,cMode
		else:
			clearListSpecialPOP()
	popReg = "esi"
	if checkPtrESI() & (Reg != popReg):
		preprocessOP_Pop(NumOpsD, popReg, Reg, best, cMode)
		if checkSpPop(Reg, cMode):
			# print "2found esi"
			return True, popReg,cMode
		else:
			clearListSpecialPOP()
	popReg = "ebp"
	if checkPtrEBP() & (Reg != popReg):
		preprocessOP_Pop(NumOpsD, popReg, Reg, best, cMode)
		if checkSpPop(Reg, cMode):
			# print "2found ebp"
			return True, popReg,cMode
		else:
			clearListSpecialPOP()
	# print "star/tFINAL"			
	popReg = "esp"
	if checkPtrESP() & (Reg != popReg):
		preprocessOP_Pop(NumOpsD, popReg, Reg, best, cMode)
		if checkSpPop(Reg, cMode):
			# print "2found esp"
			return True, popReg,cMode
		else:
			clearListSpecialPOP()
	return False, "",""

def checkSpPop(Reg, mode):
	Reg=Reg.lower()
	# print "checksppop " + Reg + "  " + mode
	if (Reg == "eax") & (mode == "best"):
		if len(objs[o].specialPOPGadgetBestEAX) > 0:
			# print "ceax true "
			return True
		else:
			# print "ceax false"
			return False
	if (Reg == "ebx") & (mode == "best"):
		if len(objs[o].specialPOPGadgetBestEBX) > 0:
			return True
		else:
			return False

	if (Reg == "ecx") & (mode == "best"):
		if len(objs[o].specialPOPGadgetBestECX) > 0:
			return True
		else:
			return False
	if (Reg == "edx") & (mode == "best"):
		if len(objs[o].specialPOPGadgetBestEDX) > 0:
			return True
		else:
			return False

	if (Reg == "edi") & (mode == "best"):
		if len(objs[o].specialPOPGadgetBestEDI) > 0:
			return True
		else:
			return False
	if (Reg == "esi") & (mode == "best"):
		if len(objs[o].specialPOPGadgetBestESI) > 0:
			return True
		else:
			return False

	if (Reg == "ebp") & (mode == "best"):
		if len(objs[o].specialPOPGadgetBestEBP) > 0:
			return True
		else:
			return False
	if (Reg == "esp") & (mode == "best"):
		if len(objs[o].specialPOPGadgetBestESP) > 0:
			return True
		else:
			return False
	if (Reg == "eax") & (mode == "ok"):
		if len(objs[o].specialPOPGadgetEAX) > 0:
			return True
		else:
			return False
	if (Reg == "ebx") & (mode == "ok"):
		if len(objs[o].specialPOPGadgetEBX) > 0:
			return True
		else:
			return False

	if (Reg == "ecx") & (mode == "ok"):
		if len(objs[o].specialPOPGadgetECX) > 0:
			return True
		else:
			return False
	if (Reg == "edx") & (mode == "ok"):
		if len(objs[o].specialPOPGadgetEDX) > 0:
			return True
		else:
			return False

	if (Reg == "edi") & (mode == "ok"):
		if len(objs[o].specialPOPGadgetEDI) > 0:
			return True
		else:
			return False
	if (Reg == "esi") & (mode == "ok"):
		if len(objs[o].specialPOPGadgetESI) > 0:
			return True
		else:
			return False

	if (Reg == "ebp") & (mode == "ok"):
		if len(objs[o].specialPOPGadgetEBP) > 0:
			return True
		else:
			return False
	if (Reg == "esp") & (mode == "ok"):
		if len(objs[o].specialPOPGadgetESP) > 0:
			return True
		else:
			return False
def checkPtrEAX():
	if len(objs[o].listOP_JMP_PTR_EAX_CNT) > 0:
		return True
	else:
		return False
def checkPtrEBX():
	if len(objs[o].listOP_JMP_PTR_EBX_CNT) > 0:
		return True
	else:
		return False

def checkPtrECX():
	# print "checkptrecx"
	# print len(objs[o].listOP_JMP_PTR_ECX_CNT) 
	if len(objs[o].listOP_JMP_PTR_ECX_CNT) > 0:
		return True
	else:
		return False
def checkPtrEDX():
	if len(objs[o].listOP_JMP_PTR_EDX_CNT) > 0:
		return True
	else:
		return False

def checkPtrEDI():
	if len(objs[o].listOP_JMP_PTR_EDI_CNT) > 0:
		return True
	else:
		return False
def checkPtrESI():
	if len(objs[o].listOP_JMP_PTR_ESI_CNT) > 0:
		return True
	else:
		return False

def checkPtrEBP():
	if len(objs[o].listOP_JMP_PTR_EBP_CNT) > 0:
		return True
	else:
		return False
def checkPtrESP():
	if len(objs[o].listOP_JMP_PTR_ESP_CNT) > 0:
		return True
	else:
		return False

def more():
	# print "Ebx"
	# print objs[o].listOP_JMP_PTR_EBX_CNT
	# print "Ecx"
	# print objs[o].listOP_JMP_PTR_ECX_CNT
	# print "Edx"
	# print objs[o].listOP_JMP_PTR_EDX_CNT
	pass
def checkBadChar(addy):
	global badChars
	x=0
	for each in badChars:
#		print "bad char " + str( badChars[x])
		badChar1 = re.match( badChars[x], addy[2:4] , re.M|re.I)
		if badChar1:
#			print "ending 0"
			return False
		else:
			badChar2 = re.match( badChars[x], addy[4:6] , re.M|re.I)
			if badChar2:
#				print "ending 2"
				return False
			else:
				badChar3 = re.match( badChars[x], addy[6:8] , re.M|re.I)
				if badChar3:
#					print "ending 3"
					return False
				else:
					badChar4 = re.match( badChars[x], addy[8:10] , re.M|re.I)
					if badChar4:
						#print "ending 4"
						return False
					else:
					#	print "No bad"
						answer = False 
		x +=1
	# print "bad char debugging output:"
	# print addy[0:2] 
	# print addy[2:4]
	# print addy[4:6] 
	# print addy[6:8]
	# print addy[8:10]

	#prints True if FREE of all bad chars
	return True
def finalPrintSub2(): 
	global printja
	global printjb
	global printjc
	global printjd
	global printjdi
	global printjsi
	global printjbp
	global printjsp
	global printptrja
	global printptrjb
	global printptrjc
	global printptrjd
	global printptrjdi
	global printptrjsi
	global printptrjbp
	global printptrjsp
	global printca
	global printcb
	global printcc
	global printcd
	global printdi
	global printsi
	global printcbp
	global printcsp
	global printptrca
	global printptrcb
	global printptrcc
	global printptrcd
	global printptrdi
	global printptrsi
	global printptrcbp
	global printptrcsp 
	global printStack   
	global printAdd
	global printSub
	global printMul
	global printDiv
	global printMov
	global printMovV
	global printDeref
	global printMovS
	global printLea
	global printXchg
	global printPop
	global printPush
	global printDec
	global printInc
	global printShiftLeft
	global printShiftRight
	global printRotateRight
	global printRotateLeft
	global printDispatcherEAX
	global printDispatcherEBX
	global printDispatcherECX
	global printDispatcherEDX
	global printDispatcherEDI
	global printDispatcherESI
	global printDispatcherEBP
	global printDispatcherEAXBest
	global printDispatcherEBXBest 
	global printDispatcherECXBest
	global printDispatcherEDXBest
	global printDispatcherEDIBest
	global printDispatcherESIBest
	global printDispatcherEBPBest
	global printDispatcherEAXOther
	global printDispatcherEBXOther 
	global printDispatcherECXOther
	global printDispatcherEDXOther
	global printDispatcherEDIOther
	global printDispatcherESIOther
	global printDispatcherEBPOther
	global o
	global printStack
	global printDeref
	global RegsPrint
	global fname
	o =0
	#print "o " + str(o)
	#print "Final print setings..."
	#print RegsPrint

	count = 0
	t=0
	try:
		if printStack == True:
			printlistOP_SP(NumOpsD, "All")
			# printlistOP_SP3(NumOpsD, "All")
			# print "done"
	except:
		nope3(fname)

	for Reg in RegsPrint:  #For loop does not work properly without the try's. That is, if one subrountine cannot rune, the for loop would break, thereby not letting me do all it is supposed to do.
		# print "global Reg: "  + Reg
		printlistOP_Add(NumOpsD, Reg)
		nope3(fname)
		# try:
		# 	print "try add " +  str(printAdd)
		# 	if printAdd == True:
		# 		print "in addd is true"
		# 		sp()
		# 		printlistOP_Add(NumOpsD, Reg)
		# except:
		# 	nope3(fname)
		try:
			if printSub == True:
				printlistOP_Sub(NumOpsD, Reg)
				nope3(fname)
		except:
			nope3(fname)
		try:
			if printMul == True:
				printlistOP_Mul(NumOpsD, Reg)
				nope3(fname)
		except:
			nope3(fname)
		try:
			if printDiv == True:
				printlistOP_Div(NumOpsD, Reg)
				nope3(fname)
		except:
			nope3(fname)
		try:
			if printMov == True:
				printlistOP_Mov(NumOpsD, Reg)
				nope3(fname)

		except:
			nope3(fname)
		try:
			if printMovV == True:
				printlistOP_MovVal(NumOpsD, Reg)
				nope3(fname)

		except:
			# print "movval"
			nope3(fname)
		try:
			global printDeref
			if printDeref == True:
				printlistOP_MovDeref(NumOpsD, Reg)
				# print "regular"
				nope3(fname)


		except:
			# print "exception"
			nope3(fname)
		try:
			if printMovS == True:
				printlistOP_MovShuf(NumOpsD, Reg)
				nope3(fname)

		except:
			# print "movshuf"
			nope3(fname)
		try:
			if printLea == True:
				printlistOP_Lea(NumOpsD, Reg)
				nope3(fname)

		except:
			nope3(fname)
		try:
			if printXchg == True:
				printlistOP_Xchg(NumOpsD, Reg)
				nope3(fname)

		except:
			nope3(fname)
		try:
			if printPop == True:
				printlistOP_Pop(NumOpsD, Reg)
				nope3(fname)

		except:
			nope3(fname)
		try:
			if printPush == True:
				printlistOP_Push(NumOpsD, Reg)
				nope3(fname)

		except:
			nope3(fname)
		try:
			if printDec == True:
				printlistOP_Dec(NumOpsD, Reg)
				nope3(fname)

		except:
			nope3(fname)
		try:
			if printInc == True:
				printlistOP_Inc(NumOpsD, Reg)
				nope3(fname)

		except:
			nope3(fname)
		try:
			if printShiftLeft == True:
				printlistOP_ShiftLeft(NumOpsD, Reg)
				nope3(fname)

		except:
			nope3(fname)
		try:
			if printShiftRight == True:
				printlistOP_ShiftRight(NumOpsD, Reg)
				nope3(fname)

		except:
			nope3(fname)
		try:
			if printRotateRight == True:
				printlistOP_RotRight(NumOpsD, Reg)
				nope3(fname)

		except:
			nope3(fname)
		try:
			if printRotateLeft == True:
				printlistOP_RotLeft(NumOpsD, Reg)
				nope3(fname)

		except:
			nope3(fname)
		count = count +1

		o=0

		####
	try:
		if printDispatcherEAX == True:
			printListDG_EAX(NumOpsD)		
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printDispatcherEBX == True:
			printListDG_EBX(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printDispatcherECX == True:
			printListDG_ECX(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printDispatcherEDX == True:
			printListDG_EDX(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printDispatcherEDI == True:
			printListDG_EDI(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printDispatcherESI == True:
			printListDG_ESI(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printDispatcherEBP == True:
			printListDG_EBP(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printDispatcherEAXBest == True:
			printListDG_BEST_EAX(NumOpsD)
			nope3(fname)
    
	except:
		nope3(fname)
	try:
		if printDispatcherEBXBest == True:
			printListDG_BEST_EBX(NumOpsD)   
			nope3(fname)
 
	except:
		nope3(fname)
	try:
		if printDispatcherECXBest == True:
			printListDG_BEST_ECX(NumOpsD)   
			nope3(fname)
 
	except:
		nope3(fname)
	try:
		if printDispatcherEDXBest == True:
			printListDG_BEST_EDX(NumOpsD)    
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printDispatcherEDIBest == True:
			printListDG_BEST_EDI(NumOpsD)   
			nope3(fname)
 
	except:
		nope3(fname)
	try:
		if printDispatcherESIBest == True:
			printListDG_BEST_ESI(NumOpsD)
			nope3(fname)
    
	except:
		nope3(fname)
	try:
		if printDispatcherEBPBest == True:
			printListDG_BEST_EBP(NumOpsD)
			nope3(fname)
    
	except:
		nope3(fname)
	try:
		if printDispatcherEAXOther == True:
			printListDG_Other_EAX(NumOpsD)
			nope3(fname)
    
	except:
		nope3(fname)
	try:
		if printDispatcherEBXOther == True:
			printListDG_Other_EBX(NumOpsD)
			nope3(fname)
    
	except:
		nope3(fname)
	try:
		if printDispatcherECXOther == True:
			printListDG_Other_ECX(NumOpsD)
			nope3(fname)
    
	except:
		nope3(fname)
	try:
		if printDispatcherEDXOther == True:
			printListDG_Other_EDX(NumOpsD) 
			nope3(fname)
   
	except:
		nope3(fname)
	try:
		if printDispatcherEDIOther == True:
			printListDG_Other_EDI(NumOpsD)
			nope3(fname)
    
	except:
		nope3(fname)
	try:
		if printDispatcherESIOther == True:
			printListDG_Other_ESI(NumOpsD)
			nope3(fname)
    
	except:
		nope3(fname)
	try:
		if printDispatcherEBPOther == True:
			printListDG_Other_EBP(NumOpsD)
			nope3(fname)
    
	except:
		nope3(fname)

	try:
		if printja == True:
			printlistOP_JMP_EAX(NumOpsD)
			nope3(fname)

			#
			#
			#	o = o + 1
	except:
		nope3(fname)
	try:
		if printjb == True:
			#objs[o].printlistOP_JMP_EBX(NumOpsD)
			printlistOP_JMP_EBX(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printjc == True:
			printlistOP_JMP_ECX(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printjd == True:
			printlistOP_JMP_EDX(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printjdi == True:
			printlistOP_JMP_EDI(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printjsi == True:
			printlistOP_JMP_ESI(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printjbp == True:
			printlistOP_JMP_EBP(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printjsp == True:
			printlistOP_JMP_ESP(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printca == True:
			printlistOP_CALL_EAX(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printcb == True:
			printlistOP_CALL_EBX(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printcc == True:
			printlistOP_CALL_ECX(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printcd == True:
			printlistOP_CALL_EDX(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printdi == True:
			printlistOP_CALL_EDI(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printsi == True:
			printlistOP_CALL_ESI(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printcbp == True:
			printlistOP_CALL_EBP(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printcsp == True:
			printlistOP_CALL_ESP(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)

	try:
		if printptrjb == True:
			#objs[o].printlistOP_JMP_PTR_EBX(NumOpsD)
			printlistOP_JMP_PTR_EBX(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printptrjc == True:
			printlistOP_JMP_PTR_ECX(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printptrjd == True:
			printlistOP_JMP_PTR_EDX(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printptrjdi == True:
			printlistOP_JMP_PTR_EDI(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printptrjsi == True:
			printlistOP_JMP_PTR_ESI(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printptrjbp == True:
			printlistOP_JMP_PTR_EBP(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printptrjsp == True:
			printlistOP_JMP_PTR_ESP(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printptrca == True:
			printlistOP_CALL_PTR_EAX(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printptrcb == True:
			printlistOP_CALL_PTR_EBX(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printptrcc == True:
			printlistOP_CALL_PTR_ECX(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printptrcd == True:
			printlistOP_CALL_PTR_EDX(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printptrdi == True:
			printlistOP_CALL_PTR_EDI(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printptrsi == True:
			printlistOP_CALL_PTR_ESI(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printptrcbp == True:
			printlistOP_CALL_PTR_EBP(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)
	try:
		if printptrcsp == True:
			printlistOP_CALL_PTR_ESP(NumOpsD)
			nope3(fname)

	except:
		nope3(fname)


def d():
	global Regs
	global RegsPrint
	global Input
	global InputAcceptable

	print "Getting it"
	Regs=["EAX", "EBX", "ECX", "EDX", "EDI", "ESI", "EDI", "EBP", "ESP"]
	Input = ["ja", "jb", "jc", "jd", "jdi","jsi", "jbp", "jsp", "j", "c", "ca","cb", "cc", "cd", "cdi", "csi","cbp", "csp", "pja", "pjb", "pjc", "pjd", "pjdi","pjsi", "pjbp", "pjsp", "pj", "pc", "pca","pcb", "pcc", "pcd", "pcdi", "pcsi","pcbp", "pcsp","ma", "a", "s", "m","d", "move", "mov", "movv", "movs","l", "xc", "st", "po", "pu","id", "inc", "dec", "bit", "sl","sr", "rr", "rl", "all", "rec","da", "db", "dc", "dd", "ddi","dsi", "dbp", "dis","ba", "bb", "bc", "bd", "bdi","bsi", "bbp", "bdis","oa", "ob", "oc", "od", "odi","osi", "obp", "odis", "stack", "deref"]
	# Input = ["ma", "a", "s", "m","d", "move", "mov", "movv", "movs","stack", "deref"]
	# Input = [ "a", "s", "mov", "m", "d"]#, "m","d"]
	# Input = [ "deref"]

	sp()
	runIt()
	print "Printing..."
	sp()

	# Input = copy.copy(InputAcceptable)
	# Input = ["a"]
	RegsPrint = copy.copy(IA86)
	
	runPrintS()
	DebugCheck()
	finalPrintSub2()
#go

def splash():
	cat="________________ _______    _______ _______ _______ _       ________________\n"
	cat+="\__    _(  ___  |  ____ )  (  ____ |  ___  |  ____ \ \    /(  ____ \__   __/\n"
	cat+="   )  ( | (   ) | (    )|  | (    )| (   ) | (    \/  \  / / (    \/  ) (   \n"
	cat+="   |  | | |   | | (____)|  | (____)| |   | | |     |  (_/ /| (__      | |   \n"
	cat+="   |  | | |   | |  _____)  |     __) |   | | |     |   _ ( |  __)     | |   \n"
	cat+="   |  | | |   | | (        | (\ (  | |   | | |     |  ( \ \| (        | |   \n"
	cat+="|\_)  ) | (___) | )        | ) \ \_| (___) | (____/\  /  \ \ (____/\  | |   \n"
	cat+="(____/  (_______)/         |/   \__(_______|_______/_/    \(_______/  )_(   \n"
	cat+="\tJOP ROCKET: Honoring Ancient Rocket Cats Everywhere"
	
	print cat
	
Extraction()
#DoEverythingFunc()
#CheckDoEverything()
# d()
# testingDG()
#print PEsList

# UI()
# c()
splash()
showOptions()
UI()
# sp()
# 
#start
# findEvilImports()
# # findMS()

# a1, a2 = findMemcpy(1)
# a3, a4 = findVirtualAlloc(1)
# print a1
# print a3


# UI()

# get_OP_RET(NumOpsD)
# newteste()
# print len(	objs[o].listOP_RET)

# printlistOP_RET(NumOpsD)

# printlistOP_RET_POP(NumOpsD)
# printlistOP_RET_POP_EDI(NumOpsD)
# printlistOP_Ret_Pop(NumOpsD, "EAX")
# printlistOP_Ret_Pop(NumOpsD, "EDI")
# printlistOP_Ret_Pop(NumOpsD, "EAX")
# printlistOP_Ret_Pop(NumOpsD, "EBX")
# printlistOP_Ret_Pop(NumOpsD, "ECX")
# printlistOP_Ret_Pop(NumOpsD, "EDX")
# printlistOP_Ret_Pop(NumOpsD, "ESI")
# printlistOP_Ret_Pop(NumOpsD, "EDI")
# printlistOP_Ret_Pop(NumOpsD, "ECX")
# printlistOP_Ret_Pop(NumOpsD, "EDI")

# printlistOP_Ret_Pop(NumOpsD, "EBP")
# printlistOP_Ret_Pop(NumOpsD, "ECX")

# b()
# c()
# get_OP_JMP_EAX(NumOpsD)
# get_OP_JMP_EBX(NumOpsD)
# get_OP_JMP_ECX(NumOpsD)
# get_OP_JMP_EDX(NumOpsD)
# get_OP_JMP_EDI(NumOpsD)
# get_OP_JMP_ESI(NumOpsD)
# get_OP_JMP_ESP(NumOpsD)


# get_OP_JMP_PTR_EAX (NumOpsD)
# get_OP_JMP_PTR_EBX(NumOpsD)
# get_OP_JMP_PTR_ECX(NumOpsD)
# get_OP_JMP_PTR_EDX(NumOpsD)
# get_OP_JMP_PTR_EDI(NumOpsD)
# get_OP_JMP_PTR_ESI(NumOpsD)
# get_OP_JMP_PTR_EBP(NumOpsD)
# get_OP_JMP_PTR_ESP(NumOpsD)

# testtest()
# # printlistOP_Add
# printlistOP_Pop(NumOpsD, "EAX")
# printlistOP_Pop(NumOpsD, "EBX")
# printlistOP_Pop(NumOpsD, "ECX")
# printlistOP_Pop(NumOpsD, "EDX")
# printlistOP_Pop(NumOpsD, "EDI")
# printlistOP_Pop(NumOpsD, "ESI")
# printlistOP_Pop(NumOpsD, "EBP")
# printlistOP_Sub(NumOpsD, "EBP")
# # printlistOP_Sub

# # printlistOP_Xchg (NumOpsD, "ALL")
# # # printlistOP_Xchg(NumOpsD, "ALL")

# # printlistOP_Xchg(NumOpsD, "EAX")
# # printlistOP_Xchg(NumOpsD, "EBX")
# # printlistOP_Xchg(NumOpsD, "ECX")
# # printlistOP_Xchg(NumOpsD, "EDX")
# # printlistOP_Xchg(NumOpsD, "EDI")
# # printlistOP_Xchg(NumOpsD, "ESI")
# # printlistOP_Xchg(NumOpsD, "EBP")
# # printlistOP_Xchg(NumOpsD, "ESP")


# printlistOP_Mov(NumOpsD, "EAX")
# printlistOP_Mov(NumOpsD, "EBX")
# printlistOP_Mov(NumOpsD, "ECX")
# printlistOP_Mov(NumOpsD, "EDX")
# printlistOP_Mov(NumOpsD, "EDI")
# printlistOP_Mov(NumOpsD, "ESI")
# printlistOP_Mov(NumOpsD, "EBP")
# printlistOP_Mov(NumOpsD, "ESP")


# printlistOP_Inc(NumOpsD, "EAX")
# printlistOP_Inc(NumOpsD, "EBX")
# printlistOP_Inc(NumOpsD, "ECX")
# printlistOP_Inc(NumOpsD, "EDX")
# printlistOP_Inc(NumOpsD, "EDI")
# printlistOP_Inc(NumOpsD, "ESI")
# printlistOP_Inc(NumOpsD, "EBP")
# printlistOP_Inc(NumOpsD, "ESP")


# printlistOP_Dec(NumOpsD, "EAX")
# printlistOP_Dec(NumOpsD, "EBX")
# printlistOP_Dec(NumOpsD, "ECX")
# printlistOP_Dec(NumOpsD, "EDX")
# printlistOP_Dec(NumOpsD, "EDI")
# printlistOP_Dec(NumOpsD, "ESI")
# printlistOP_Dec(NumOpsD, "EBP")
# printlistOP_Dec(NumOpsD, "ESP")

# printlistOP_ShiftLeft(NumOpsD, "ESP")
# printlistOP_ShiftRight(NumOpsD, "ESP")
# printlistOP_RotLeft(NumOpsD, "ESP")
# printlistOP_RotRight(NumOpsD, "ESP")
# # printlistOP_Dec
# showOrdTest()
# UI()
# for each in FoundApisName:
# 	print each
#pre process test
#get_OP_JMP_PTR_EBX(NumOpsD)


# get_OP_JMP_EAX(NumOpsD)
# printlistOP_JMP_EAX(NumOpsD)
# printlistOP_Sub(NumOpsD, "EAX")
# UI()
# get_OP_JMP_ESP(NumOpsD)
# get_OP_CALL_ESP	(NumOpsD)
# printlistOP_JMP_ESP(NumOpsD)
# printlistOP_CALL_ESP(NumOpsD)
# UI()
# get_OP_JMP_EAX(NumOpsD)
# get_OP_CALL_EAX	(NumOpsD)
# get_OP_JMP_PTR_EAX(NumOpsD)
# printlistOP_JMP_PTR_EAX(NumOpsD)
# UI()
# printlistOP_Sub(NumOpsD, "EAX")
# print get_Total_SUB_EAX()

# 

# print "final answer:"
# preprocessOP_JMP(NumOpsD, "EAX")

# 

