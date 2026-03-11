/* ANALYSIS_REPORT_START_JUSTIFICATION (2024/08/07 : uif04469) !-->
TOOL_NUMBER(qac:5002) GUIDELINE(cert_c_2016:recommendation:PRE08) Inclusion checked safe, code can be kept, No risk.
TOOL_NUMBER(qac:3132) GUIDELINE(cert_c_2016:recommendation:DCL06) Magic number is safe, code can be kept, No risk.
TOOL_NUMBER(qac:0776) GUIDELINE(cert_c_2016:recommendation:DCL23) Naming checked safe, code can be kept, No risk. 
TOOL_NUMBER(qac:0288) GUIDELINE(cert_c_2016:recommendation:MSC09) Usage checked safe, code can be kept. No risk. 
<--! */
#ifndef STORE_RESET_REASON_H
#define STORE_RESET_REASON_H

#include "HwErrHdl_Cfg.h"
#include "Os.h"
#include "NvM.h"
#include "Rte_Type.h"
#include "Sbc.h"

typedef enum
{
    STORE_FAULT_FROM_UNDEFINE = 0,
    STORE_FAULT_FROM_HardFaultCallout,
    STORE_FAULT_FROM_MemManageCallout,
    STORE_FAULT_FROM_BusFaultCallout,
    STORE_FAULT_FROM_UsageFaultCallout,
    STORE_FAULT_FROM_ShutdownHook,
    STORE_FAULT_FROM_ErrorHook,
    STORE_FAULT_FROM_StackOverrunHook,
    STORE_FAULT_FROM_RstMon,
    STORE_FAULT_FROM_UnusedISRTrap,
    STORE_FAULT_FROM_FblReprogram,
    STORE_FAULT_FROM_NEXT_CATEGORY = 0x80,
    STORE_FAULT_FROM_POR,
    STORE_FAULT_FROM_WDG,
    STORE_FAULT_FROM_SAFETYERRMGR,
    STORE_FAULT_FROM_FBL,
    STORE_FAULT_FROM_EOL,
    STORE_FAULT_FROM_11RESET,
    STORE_FAULT_FROM_Wdg_66_IA
} Reset_LogFaultFromType;

#define RESET_LOG_TEST                              0

#define STORE_RESET_INFO_SUB_NUM                    5u
#define RESET_LOG_CORE_NUM                          1u
#define STORE_RESET_REASON_NUM_MAX                  (uint32)5
#define RESET_LOG_CALL_STACK_HIERARCHY              (uint32)5
#define RESET_LOG_SW_VERSION_LENGTH 9u

#define MAX_ERRORTYPE_NUM (uint8)12u

#pragma pack(1)
typedef struct
{
    uint16 index;
    uint32 timeX;
} Reset_LogDataType;

typedef struct
{    
    Reset_LogDataType runnableIn;
    Reset_LogDataType runnableOut;
    Reset_LogDataType anormalRunnable[STORE_RESET_INFO_SUB_NUM];
    Reset_LogDataType anormalTask[STORE_RESET_INFO_SUB_NUM];
    Reset_LogDataType isrIn;
    Reset_LogDataType isrOut;
    uint16 runnableSubIndex;
    uint16 taskSubIndex;
} Reset_LogWdgInfoType;

typedef struct
{
    uint32 mmfsr;
    uint32 bfsr;
    uint32 ufsr;
    uint32 hfsr;
    uint32 mmfar;
    uint32 bfar;
    uint32 cfsr;
    uint32 sp;
    uint32 lr;
    uint32 pc;
} Store_RstFsrType;

typedef struct
{
    Store_RstFsrType fsr;
    StatusType status;
    uint32 callStack[RESET_LOG_CALL_STACK_HIERARCHY];
    uint16 isrIndex;
    uint16 taskIndex;
} Reset_LogFaultInfoType;

typedef struct
{
    uint32 cause;
    uint32 cause2;
    DateTi30 globalTime;
    Reset_LogFaultFromType faultFrom;
} Reset_LogBaseType;

typedef union
{
    Reset_LogWdgInfoType rstWdgInfo[RESET_LOG_CORE_NUM];
    Reset_LogFaultInfoType rstFaultInfo[RESET_LOG_CORE_NUM];
} Reset_LogUnionType;

typedef struct
{
    uint32 Para;
    uint32 Subpara;
    uint8 Errortype;
}Reset_LogSafetyErrType;

typedef struct
{
    Reset_LogBaseType base;
    uint32 feedWdg;
    Reset_LogUnionType rstInfoUnion;
    SbcStatusInfoType sbcReg;
    Reset_LogSafetyErrType safetyErrLog;
    uint16 osLimit;
    uint8 cpuAvg;
    uint8 swVersion[RESET_LOG_SW_VERSION_LENGTH];
} Reset_LogReasonType;

typedef struct
{
    uint8 State;
    uint8 ResetCnt[MAX_ERRORTYPE_NUM];
    uint32 Errortype;
    uint32 Para;
    uint32 Subpara;
}Reset_LogSafetyStateType;

typedef struct
{
    uint8 D05C44_Flag;  //1:fail trigger,    0:no fail  , other:reserved;
    uint8 D05C45_Flag;  //1:fail trigger,    0:no fail  , other:reserved;
}Reset_LogDTCMgrFlashType;

typedef struct
{
    Reset_LogReasonType resetLog[STORE_RESET_REASON_NUM_MAX];
    uint8 nextIndex;
    uint8 count;
} Reset_LogType;

typedef union
{
    uint8 dummy[700];
    Reset_LogType log;
} Reset_LogRamType;
#pragma pack()

extern Reset_LogRamType Reset_LogRam;

extern Reset_LogSafetyStateType Reset_LogSafetyState;

extern Reset_LogDTCMgrFlashType Reset_LogDTCMgrFlash_Flag;

extern boolean Reset_Log_isEnable;

extern Reset_LogReasonType Reset_LogReten;

extern uint8 PerfCalc_AvgCpuLoad;

void Reset_LogInit(void);

void Reset_LogFault(Reset_LogFaultFromType faultFrom, uint32 const *faultStackAddr, uint32 needReset);

Std_ReturnType Reset_LogRamInit(void);

void Reset_LogFeedWdgOk(void);

Std_ReturnType Reset_LogNvMCbk(uint8 ServiceId, NvM_RequestResultType JobResult);

void Reset_LogSbcReadReg(void);

void Reset_LogShutdownHook(
Reset_LogFaultFromType faultFrom,
uint32 const *faultStackAddr,
StatusType status,
uint32 needReset);

void Reset_LogErrorHook(
Reset_LogFaultFromType faultFrom,
uint32 const *faultStackAddr,
StatusType status,
uint32 needReset);

void Reset_LogStackOverrunHook(
Reset_LogFaultFromType faultFrom,
uint32 const *faultStackAddr,
StatusType status,
uint32 needReset);

void Reset_LogGeneralCallout(Reset_LogFaultFromType faultFrom);

void Reset_LogMainFunction(void);

void Reset_LogPutAnormalRunnable(uint16 index, uint32 timeSpan);

void Reset_LogPutAnormalTask(uint16 index, uint32 timeSpan);

void Reset_LogPutRunnable(uint32 inOut, uint16 index, uint32 timestamp);

void Reset_LogPutIsr(uint32 inOut, uint16 index);

#if RESET_LOG_TEST
void Reset_LogFaultTest(uint32 type);
#endif

#endif /* STORE_RESET_REASON_H */
/*  ANALYSIS_REPORT_END_JUSTIFICATION */
