# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 16:35:54 2024

@author: Xin.Wang41
"""

import ctypes
from enum import Enum

############Common config############
STORE_RESET_INFO_SUB_NUM = 5
RESET_LOG_CALL_STACK_HIERARCHY = 5
RESET_LOG_SW_VERSION_LENGTH = 9
STORE_CALL_STACK_DATA_LENGTH = 226
CALLSTACK_SW_VERSION_LENGTH = 14
############ZCUD-M config############
M_STORE_RESET_REASON_NUM_MAX = 3
M_RESET_LOG_CORE_NUM = 2

############ZCUP config############
P_STORE_RESET_REASON_NUM_MAX = 3
P_RESET_LOG_CORE_NUM = 2

############ZCUD_S config############
S_STORE_RESET_REASON_NUM_MAX = 5
S_RESET_LOG_CORE_NUM = 1

class MFaultFromInfo(Enum):
    STORE_FAULT_FROM_UNDEFINE = 0
    STORE_FAULT_FROM_HardFaultCallout_MainCore = 1
    STORE_FAULT_FROM_MemManageCallout_MainCore = 2
    STORE_FAULT_FROM_BusFaultCallout_MainCore = 3
    STORE_FAULT_FROM_UsageFaultCallout_MainCore = 4
    STORE_FAULT_FROM_HardFaultCallout_SlaveCore = 5
    STORE_FAULT_FROM_MemManageCallout_SlaveCore = 6
    STORE_FAULT_FROM_BusFaultCallout_SlaveCore = 7
    STORE_FAULT_FROM_UsageFaultCallout_SlaveCore = 8
    STORE_FAULT_FROM_ShutdownHook = 9
    STORE_FAULT_FROM_ErrorHook = 10
    STORE_FAULT_FROM_StackOverrunHook = 11
    STORE_FAULT_FROM_RstMon = 12
    STORE_FAULT_FROM_UnusedISRTrap = 13
    STORE_FAULT_FROM_FblReprogram = 14
    STORE_FAULT_FROM_NEXT_CATEGORY = 0x80
    STORE_FAULT_FROM_INIT = 0x81
    STORE_FAULT_FROM_POR = 0x82
    STORE_FAULT_FROM_WDG = 0x83
    STORE_FAULT_FROM_SAFETYERRMGR = 0x84
    STORE_FAULT_FROM_SLEEP_REVERT = 0x85
    STORE_FAULT_FROM_FBL = 0x86
    STORE_FAULT_FROM_EOL = 0x87
    STORE_FAULT_FROM_11RESET = 0x88
    STORE_FAULT_FROM_Wdg_66_IA_C0 = 0x89
    STORE_FAULT_FROM_Wdg_66_IA_C1 = 0x8A

MFaultFromInfoDict = {
    MFaultFromInfo.STORE_FAULT_FROM_UNDEFINE: "STORE_FAULT_FROM_UNDEFINE",
    MFaultFromInfo.STORE_FAULT_FROM_HardFaultCallout_MainCore: "STORE_FAULT_FROM_HardFaultCallout_MainCore",
    MFaultFromInfo.STORE_FAULT_FROM_MemManageCallout_MainCore: "STORE_FAULT_FROM_MemManageCallout_MainCore",
    MFaultFromInfo.STORE_FAULT_FROM_BusFaultCallout_MainCore: "STORE_FAULT_FROM_BusFaultCallout_MainCore",
    MFaultFromInfo.STORE_FAULT_FROM_UsageFaultCallout_MainCore: "STORE_FAULT_FROM_UsageFaultCallout_MainCore",
    MFaultFromInfo.STORE_FAULT_FROM_HardFaultCallout_SlaveCore: "STORE_FAULT_FROM_HardFaultCallout_SlaveCore",
    MFaultFromInfo.STORE_FAULT_FROM_MemManageCallout_SlaveCore: "STORE_FAULT_FROM_MemManageCallout_SlaveCore",
    MFaultFromInfo.STORE_FAULT_FROM_BusFaultCallout_SlaveCore: "STORE_FAULT_FROM_BusFaultCallout_SlaveCore",
    MFaultFromInfo.STORE_FAULT_FROM_UsageFaultCallout_SlaveCore: "STORE_FAULT_FROM_UsageFaultCallout_SlaveCore",
    MFaultFromInfo.STORE_FAULT_FROM_ShutdownHook: "STORE_FAULT_FROM_ShutdownHook",
    MFaultFromInfo.STORE_FAULT_FROM_ErrorHook: "STORE_FAULT_FROM_ErrorHook",
    MFaultFromInfo.STORE_FAULT_FROM_StackOverrunHook: "STORE_FAULT_FROM_StackOverrunHook",
    MFaultFromInfo.STORE_FAULT_FROM_RstMon: "STORE_FAULT_FROM_RstMon",
    MFaultFromInfo.STORE_FAULT_FROM_UnusedISRTrap: "STORE_FAULT_FROM_UnusedISRTrap",
    MFaultFromInfo.STORE_FAULT_FROM_FblReprogram: "STORE_FAULT_FROM_FblReprogram",
    MFaultFromInfo.STORE_FAULT_FROM_NEXT_CATEGORY: "STORE_FAULT_FROM_NEXT_CATEGORY",
    MFaultFromInfo.STORE_FAULT_FROM_INIT: "STORE_FAULT_FROM_INIT",
    MFaultFromInfo.STORE_FAULT_FROM_POR: "STORE_FAULT_FROM_POR",
    MFaultFromInfo.STORE_FAULT_FROM_WDG: "STORE_FAULT_FROM_WDG",
    MFaultFromInfo.STORE_FAULT_FROM_SAFETYERRMGR: "STORE_FAULT_FROM_SAFETYERRMGR",
    MFaultFromInfo.STORE_FAULT_FROM_SLEEP_REVERT: "STORE_FAULT_FROM_SLEEP_REVERT",
    MFaultFromInfo.STORE_FAULT_FROM_FBL: "STORE_FAULT_FROM_FBL",
    MFaultFromInfo.STORE_FAULT_FROM_EOL: "STORE_FAULT_FROM_EOL",
    MFaultFromInfo.STORE_FAULT_FROM_11RESET: "STORE_FAULT_FROM_11RESET",
    MFaultFromInfo.STORE_FAULT_FROM_Wdg_66_IA_C0: "STORE_FAULT_FROM_Wdg_66_IA_C0",
    MFaultFromInfo.STORE_FAULT_FROM_Wdg_66_IA_C1: "STORE_FAULT_FROM_Wdg_66_IA_C1"
}

class PFaultFromInfo(Enum):
    STORE_FAULT_FROM_UNDEFINE = 0
    STORE_FAULT_FROM_HardFaultCallout_MainCore = 1
    STORE_FAULT_FROM_MemManageCallout_MainCore = 2
    STORE_FAULT_FROM_BusFaultCallout_MainCore = 3
    STORE_FAULT_FROM_UsageFaultCallout_MainCore = 4
    STORE_FAULT_FROM_HardFaultCallout_SlaveCore = 5
    STORE_FAULT_FROM_MemManageCallout_SlaveCore = 6
    STORE_FAULT_FROM_BusFaultCallout_SlaveCore = 7
    STORE_FAULT_FROM_UsageFaultCallout_SlaveCore = 8
    STORE_FAULT_FROM_ShutdownHook = 9
    STORE_FAULT_FROM_ErrorHook = 10
    STORE_FAULT_FROM_StackOverrunHook = 11
    STORE_FAULT_FROM_RstMon = 12
    STORE_FAULT_FROM_UnusedISRTrap = 13
    STORE_FAULT_FROM_FblReprogram = 14
    STORE_FAULT_FROM_NEXT_CATEGORY = 0x80
    STORE_FAULT_FROM_INIT = 0x81
    STORE_FAULT_FROM_POR = 0x82
    STORE_FAULT_FROM_WDG = 0x83
    STORE_FAULT_FROM_SAFETYERRMGR = 0x84
    STORE_FAULT_FROM_SLEEP_REVERT = 0x85
    STORE_FAULT_FROM_FBL = 0x86
    STORE_FAULT_FROM_EOL = 0x87
    STORE_FAULT_FROM_11RESET = 0x88
    STORE_FAULT_FROM_Wdg_66_IA_C0 = 0x89
    STORE_FAULT_FROM_Wdg_66_IA_C1 = 0x8A

PFaultFromInfoDict = {
    PFaultFromInfo.STORE_FAULT_FROM_UNDEFINE: "STORE_FAULT_FROM_UNDEFINE",
    PFaultFromInfo.STORE_FAULT_FROM_HardFaultCallout_MainCore: "STORE_FAULT_FROM_HardFaultCallout_MainCore",
    PFaultFromInfo.STORE_FAULT_FROM_MemManageCallout_MainCore: "STORE_FAULT_FROM_MemManageCallout_MainCore",
    PFaultFromInfo.STORE_FAULT_FROM_BusFaultCallout_MainCore: "STORE_FAULT_FROM_BusFaultCallout_MainCore",
    PFaultFromInfo.STORE_FAULT_FROM_UsageFaultCallout_MainCore: "STORE_FAULT_FROM_UsageFaultCallout_MainCore",
    PFaultFromInfo.STORE_FAULT_FROM_HardFaultCallout_SlaveCore: "STORE_FAULT_FROM_HardFaultCallout_SlaveCore",
    PFaultFromInfo.STORE_FAULT_FROM_MemManageCallout_SlaveCore: "STORE_FAULT_FROM_MemManageCallout_SlaveCore",
    PFaultFromInfo.STORE_FAULT_FROM_BusFaultCallout_SlaveCore: "STORE_FAULT_FROM_BusFaultCallout_SlaveCore",
    PFaultFromInfo.STORE_FAULT_FROM_UsageFaultCallout_SlaveCore: "STORE_FAULT_FROM_UsageFaultCallout_SlaveCore",
    PFaultFromInfo.STORE_FAULT_FROM_ShutdownHook: "STORE_FAULT_FROM_ShutdownHook",
    PFaultFromInfo.STORE_FAULT_FROM_ErrorHook: "STORE_FAULT_FROM_ErrorHook",
    PFaultFromInfo.STORE_FAULT_FROM_StackOverrunHook: "STORE_FAULT_FROM_StackOverrunHook",
    PFaultFromInfo.STORE_FAULT_FROM_RstMon: "STORE_FAULT_FROM_RstMon",
    PFaultFromInfo.STORE_FAULT_FROM_UnusedISRTrap: "STORE_FAULT_FROM_UnusedISRTrap",
    PFaultFromInfo.STORE_FAULT_FROM_FblReprogram: "STORE_FAULT_FROM_FblReprogram",
    PFaultFromInfo.STORE_FAULT_FROM_NEXT_CATEGORY: "STORE_FAULT_FROM_NEXT_CATEGORY",
    PFaultFromInfo.STORE_FAULT_FROM_INIT: "STORE_FAULT_FROM_INIT",
    PFaultFromInfo.STORE_FAULT_FROM_POR: "STORE_FAULT_FROM_POR",
    PFaultFromInfo.STORE_FAULT_FROM_WDG: "STORE_FAULT_FROM_WDG",
    PFaultFromInfo.STORE_FAULT_FROM_SAFETYERRMGR: "STORE_FAULT_FROM_SAFETYERRMGR",
    PFaultFromInfo.STORE_FAULT_FROM_SLEEP_REVERT: "STORE_FAULT_FROM_SLEEP_REVERT",
    PFaultFromInfo.STORE_FAULT_FROM_FBL: "STORE_FAULT_FROM_FBL",
    PFaultFromInfo.STORE_FAULT_FROM_EOL: "STORE_FAULT_FROM_EOL",
    PFaultFromInfo.STORE_FAULT_FROM_11RESET: "STORE_FAULT_FROM_11RESET",
    PFaultFromInfo.STORE_FAULT_FROM_Wdg_66_IA_C0: "STORE_FAULT_FROM_Wdg_66_IA_C0",
    PFaultFromInfo.STORE_FAULT_FROM_Wdg_66_IA_C1: "STORE_FAULT_FROM_Wdg_66_IA_C1"
}

class SFaultFromInfo(Enum):
    STORE_FAULT_FROM_UNDEFINE = 0
    STORE_FAULT_FROM_HardFaultCallout = 1
    STORE_FAULT_FROM_MemManageCallout = 2
    STORE_FAULT_FROM_BusFaultCallout = 3
    STORE_FAULT_FROM_UsageFaultCallout = 4
    STORE_FAULT_FROM_ShutdownHook = 5
    STORE_FAULT_FROM_ErrorHook = 6
    STORE_FAULT_FROM_StackOverrunHook = 7
    STORE_FAULT_FROM_RstMon = 8
    STORE_FAULT_FROM_UnusedISRTrap = 9
    STORE_FAULT_FROM_FblReprogram = 10
    STORE_FAULT_FROM_NEXT_CATEGORY = 0x80
    STORE_FAULT_FROM_INIT = 0x81
    STORE_FAULT_FROM_POR = 0x82
    STORE_FAULT_FROM_WDG = 0x83
    STORE_FAULT_FROM_SAFETYERRMGR = 0x84
    STORE_FAULT_FROM_FBL = 0x85
    STORE_FAULT_FROM_EOL = 0x86
    STORE_FAULT_FROM_11RESET = 0x87
    STORE_FAULT_FROM_Wdg_66_IA = 0x88
    STORE_FAULT_FROM_Wdg_66_SELF_TEST = 0x89

SFaultFromInfoDict = {
    SFaultFromInfo.STORE_FAULT_FROM_UNDEFINE: "STORE_FAULT_FROM_UNDEFINE",
    SFaultFromInfo.STORE_FAULT_FROM_HardFaultCallout: "STORE_FAULT_FROM_HardFaultCallout",
    SFaultFromInfo.STORE_FAULT_FROM_MemManageCallout: "STORE_FAULT_FROM_MemManageCallout",
    SFaultFromInfo.STORE_FAULT_FROM_BusFaultCallout: "STORE_FAULT_FROM_BusFaultCallout",
    SFaultFromInfo.STORE_FAULT_FROM_UsageFaultCallout: "STORE_FAULT_FROM_UsageFaultCallout",
    SFaultFromInfo.STORE_FAULT_FROM_ShutdownHook: "STORE_FAULT_FROM_ShutdownHook",
    SFaultFromInfo.STORE_FAULT_FROM_ErrorHook: "STORE_FAULT_FROM_ErrorHook",
    SFaultFromInfo.STORE_FAULT_FROM_StackOverrunHook: "STORE_FAULT_FROM_StackOverrunHook",
    SFaultFromInfo.STORE_FAULT_FROM_RstMon: "STORE_FAULT_FROM_RstMon",
    SFaultFromInfo.STORE_FAULT_FROM_UnusedISRTrap: "STORE_FAULT_FROM_UnusedISRTrap",
    SFaultFromInfo.STORE_FAULT_FROM_FblReprogram: "STORE_FAULT_FROM_FblReprogram",
    SFaultFromInfo.STORE_FAULT_FROM_NEXT_CATEGORY: "STORE_FAULT_FROM_NEXT_CATEGORY",
    SFaultFromInfo.STORE_FAULT_FROM_INIT: "STORE_FAULT_FROM_INIT",
    SFaultFromInfo.STORE_FAULT_FROM_POR: "STORE_FAULT_FROM_POR",
    SFaultFromInfo.STORE_FAULT_FROM_WDG: "STORE_FAULT_FROM_WDG",
    SFaultFromInfo.STORE_FAULT_FROM_SAFETYERRMGR: "STORE_FAULT_FROM_SAFETYERRMGR",
    SFaultFromInfo.STORE_FAULT_FROM_FBL: "STORE_FAULT_FROM_FBL",
    SFaultFromInfo.STORE_FAULT_FROM_EOL: "STORE_FAULT_FROM_EOL",
    SFaultFromInfo.STORE_FAULT_FROM_11RESET: "STORE_FAULT_FROM_11RESET",
    SFaultFromInfo.STORE_FAULT_FROM_Wdg_66_IA: "STORE_FAULT_FROM_Wdg_66_IA",
    SFaultFromInfo.STORE_FAULT_FROM_Wdg_66_SELF_TEST: "STORE_FAULT_FROM_Wdg_66_SELF_TEST"
}
class CddTcanSbcStatusInfoType(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('FSM_RSRT_CNTR', ctypes.c_uint8),
        ('REV_ID', ctypes.c_uint8),
        ('FSM_SLP_STAT', ctypes.c_uint8),
        ('NVM_REV', ctypes.c_uint8),
        ('INT_1', ctypes.c_uint8),
        ('INT_2', ctypes.c_uint8),
        ('INT_3', ctypes.c_uint8),
        ('INT_6', ctypes.c_uint8),
        ('RESERVED', ctypes.c_uint8),
    ]

class Reset_LogstackDataType(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('pc', ctypes.c_uint32),
        ('sp', ctypes.c_uint32),
        ('release_SWversion', ctypes.c_uint8 * CALLSTACK_SW_VERSION_LENGTH),
        ('data', ctypes.c_uint8 * STORE_CALL_STACK_DATA_LENGTH),
        ('count', ctypes.c_uint8),
    ]

class Reset_LogSafetyErrType(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('Errortype', ctypes.c_uint32),
        ('Para', ctypes.c_uint32),
        ('Subpara', ctypes.c_uint32),
    ]

class P_Reset_LogSafetyErrType(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('Para', ctypes.c_uint32),
        ('Subpara', ctypes.c_uint32),
        ('Errortype', ctypes.c_uint32),
    ]

class S_Reset_LogSafetyErrType(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('Para', ctypes.c_uint32),
        ('Subpara', ctypes.c_uint32),
        ('Errortype', ctypes.c_uint32),
    ]

class Reset_LogDataType(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('index', ctypes.c_uint16),
        ('timeX', ctypes.c_uint32),
    ]


class Store_RstFsrType(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('mmfsr', ctypes.c_uint32),
        ('bfsr', ctypes.c_uint32),
        ('ufsr', ctypes.c_uint32),
        ('hfsr', ctypes.c_uint32),
        ('mmfar', ctypes.c_uint32),
        ('bfar', ctypes.c_uint32),
        ('cfsr', ctypes.c_uint32),
        ('sp', ctypes.c_uint32),
        ('lr', ctypes.c_uint32),
        ('pc', ctypes.c_uint32),
    ]


class Reset_LogWdgInfoType(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('runnableIn', Reset_LogDataType),
        ('runnableOut', Reset_LogDataType),
        ('anormalRunnable', Reset_LogDataType * STORE_RESET_INFO_SUB_NUM),
        ('anormalTask', Reset_LogDataType * STORE_RESET_INFO_SUB_NUM),
        ('isrIn', Reset_LogDataType),
        ('isrOut', Reset_LogDataType),
        ('runnableSubIndex', ctypes.c_uint16),
        ('taskSubIndex', ctypes.c_uint16),
    ]

class Reset_LogFaultInfoType(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('fsr', Store_RstFsrType),
        ('status', ctypes.c_uint8),
        # ('callStack', ctypes.c_uint32 * RESET_LOG_CALL_STACK_HIERARCHY),
        ('isrIndex', ctypes.c_uint16),
        ('taskIndex', ctypes.c_uint16),
    ]


# class M_Reset_LogUnionType(ctypes.Union):
#     _pack_ = 1
#     _fields_ = [
#         ("rstWdgInfo", Reset_LogWdgInfoType * M_RESET_LOG_CORE_NUM),
#         ("rstFaultInfo", Reset_LogFaultInfoType * M_RESET_LOG_CORE_NUM)
#     ]

# class P_Reset_LogUnionType(ctypes.Union):
#     _pack_ = 1
#     _fields_ = [
#         ("rstWdgInfo", Reset_LogWdgInfoType * P_RESET_LOG_CORE_NUM),
#         ("rstFaultInfo", Reset_LogFaultInfoType * P_RESET_LOG_CORE_NUM)
#     ]

class Cur_Time(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('Yr1', ctypes.c_ubyte),
        ('Mth1', ctypes.c_ubyte),
        ('Day1', ctypes.c_ubyte),
        ('Hr1', ctypes.c_ubyte),
        ('Mins1', ctypes.c_ubyte),
        ('Sec1', ctypes.c_ubyte),
        ('NoYes1', ctypes.c_ubyte),
    ]

class Reset_LogBaseType(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('cause', ctypes.c_uint32),
        ('cause2', ctypes.c_uint32),
        ('globalTime', Cur_Time),
        ('faultFrom', ctypes.c_uint8),
    ]

class M_Reset_LogReasonType(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('base', Reset_LogBaseType),
        ('feedWdg', ctypes.c_uint32),
        # ('rstInfoUnion', M_Reset_LogUnionType),
        ("rstFaultInfo", Reset_LogFaultInfoType * M_RESET_LOG_CORE_NUM),
        ('sbcReg', CddTcanSbcStatusInfoType),
        ('safetyErrLog', Reset_LogSafetyErrType),
        ("osLimit", ctypes.c_uint16 * M_RESET_LOG_CORE_NUM),
        ("cpuAvg", ctypes.c_uint8 * M_RESET_LOG_CORE_NUM),
        ("swVersion", ctypes.c_uint8 * RESET_LOG_SW_VERSION_LENGTH),
    ]

class P_Reset_LogReasonType(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('base', Reset_LogBaseType),
        ('feedWdg', ctypes.c_uint32),
        # ('rstInfoUnion', P_Reset_LogUnionType),
        ("rstFaultInfo", Reset_LogFaultInfoType * P_RESET_LOG_CORE_NUM),
		('sbcReg', CddTcanSbcStatusInfoType),
        ('safetyErrLog', P_Reset_LogSafetyErrType),
        ('osLimit', ctypes.c_uint16),
        ('cpuAvg', ctypes.c_uint8),
        ("swVersion", ctypes.c_uint8 * RESET_LOG_SW_VERSION_LENGTH),
    ]

class S_Reset_LogReasonType(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('base', Reset_LogBaseType),
        ('feedWdg', ctypes.c_uint32),
        # ('rstInfoUnion', P_Reset_LogUnionType),
        ("rstFaultInfo", Reset_LogFaultInfoType * S_RESET_LOG_CORE_NUM),
        ('safetyErrLog', S_Reset_LogSafetyErrType),
        ('osLimit', ctypes.c_uint16),
        ('cpuAvg', ctypes.c_uint8),
        ("swVersion", ctypes.c_uint8 * RESET_LOG_SW_VERSION_LENGTH),
    ]

class M_Reset_LogType(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('resetLog', M_Reset_LogReasonType * M_STORE_RESET_REASON_NUM_MAX),
        ('stackData', Reset_LogstackDataType),
        ('nextIndex', ctypes.c_uint8),
        ('count', ctypes.c_uint8),
    ]

class S_Reset_LogType(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('resetLog', S_Reset_LogReasonType * S_STORE_RESET_REASON_NUM_MAX),
        ('stackData', Reset_LogstackDataType),
        ('nextIndex', ctypes.c_uint8),
        ('count', ctypes.c_uint8),
    ]

class P_Reset_LogType(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('resetLog', P_Reset_LogReasonType * P_STORE_RESET_REASON_NUM_MAX),
        ('stackData', Reset_LogstackDataType),
        ('nextIndex', ctypes.c_uint8),
        ('count', ctypes.c_uint8),
    ]

class M_Reset_LogRamType(ctypes.Union):
    _pack_ = 1
    _fields_ = [
        ("dummy", ctypes.c_uint8 * 700),
        ("log", M_Reset_LogType)
    ]

class P_Reset_LogRamType(ctypes.Union):
    _pack_ = 1
    _fields_ = [
        ("dummy", ctypes.c_uint8 * 700),
        ("log", P_Reset_LogType)
    ]

class S_Reset_LogRamType(ctypes.Union):
    _pack_ = 1
    _fields_ = [
        ("dummy", ctypes.c_uint8 * 700),
        ("log", S_Reset_LogType)
    ]
