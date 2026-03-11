/* ANALYSIS_REPORT_START_JUSTIFICATION (2024/08/07 : uif04469) !-->
TOOL_NUMBER(qac:5002) GUIDELINE(cert_c_2016:recommendation:PRE08) Inclusion checked safe, code can be kept, No risk.
TOOL_NUMBER(qac:3132) GUIDELINE(cert_c_2016:recommendation:DCL06) Magic number is safe, code can be kept, No risk.
TOOL_NUMBER(qac:0776) GUIDELINE(cert_c_2016:recommendation:DCL23) Naming checked safe, code can be kept, No risk. 
TOOL_NUMBER(qac:0288) GUIDELINE(cert_c_2016:recommendation:MSC09) Usage checked safe, code can be kept. No risk. 
TOOL_NUMBER(qac:0778) GUIDELINE(cert_c_2016:recommendation:DCL23) Naming checked safe, code can be kept, No risk. 
<--! */
#ifndef STORE_RESET_REASON_H
#define STORE_RESET_REASON_H

#include "HwErrHdl_Cfg.h"
#include "Os.h"
#include "NvM.h"
#include "Sbc.h"

typedef enum
{
    STORE_FAULT_FROM_UNDEFINE = 0,
    STORE_FAULT_FROM_HardFaultCallout_MainCore,
    STORE_FAULT_FROM_MemManageCallout_MainCore,
    STORE_FAULT_FROM_BusFaultCallout_MainCore,
    STORE_FAULT_FROM_UsageFaultCallout_MainCore,
    STORE_FAULT_FROM_HardFaultCallout_SlaveCore,
    STORE_FAULT_FROM_MemManageCallout_SlaveCore,
    STORE_FAULT_FROM_BusFaultCallout_SlaveCore,
    STORE_FAULT_FROM_UsageFaultCallout_SlaveCore,
    STORE_FAULT_FROM_ShutdownHook,
    STORE_FAULT_FROM_ErrorHook,
    STORE_FAULT_FROM_StackOverrunHook,
    STORE_FAULT_FROM_RstMon,
    STORE_FAULT_FROM_UnusedISRTrap,
    STORE_FAULT_FROM_FblReprogram,
    STORE_FAULT_FROM_NEXT_CATEGORY = 0x80,
    STORE_FAULT_FROM_INIT,
    STORE_FAULT_FROM_POR,
    STORE_FAULT_FROM_WDG,
    STORE_FAULT_FROM_SAFETYERRMGR,
    STORE_FAULT_FROM_SLEEP_REVERT,
    STORE_FAULT_FROM_FBL,
    STORE_FAULT_FROM_EOL,
    STORE_FAULT_FROM_11RESET,
    STORE_FAULT_FROM_Wdg_66_IA,
    STORE_FAULT_FROM_MCWDT1
} Reset_LogFaultFromType;

extern uint32 __memsection_warm_ninit_os_stack0_start;
extern uint32 __memsection_warm_ninit_os_stack0_end;  
extern uint32 __memsection_warm_ninit_os_stack1_start;
extern uint32 __memsection_warm_ninit_os_stack1_end;
extern uint32 __memsection_warm_ninit_os_stack0_size;
extern uint32 __memsection_warm_ninit_os_stack1_size;

#define RESET_LOG_OS_STACK0_SIZE                    (uint32)&__memsection_warm_ninit_os_stack0_size
#define RESET_LOG_OS_STACK1_SIZE                    (uint32)&__memsection_warm_ninit_os_stack1_size
#define RESET_LOG_CALLSTACK_SP_C0_MIN               (uint32)&__memsection_warm_ninit_os_stack0_start
#define RESET_LOG_CALLSTACK_SP_C0_MAX               (uint32)&__memsection_warm_ninit_os_stack0_end
#define RESET_LOG_CALLSTACK_SP_C1_MIN               (uint32)&__memsection_warm_ninit_os_stack1_start
#define RESET_LOG_CALLSTACK_SP_C1_MAX               (uint32)&__memsection_warm_ninit_os_stack1_end

#define RESET_LOG_OS_STACK_SIZE                     (RESET_LOG_OS_STACK0_SIZE + RESET_LOG_OS_STACK1_SIZE)
#define RESET_LOG_OS_STACK_STEP_COUNT               50
#define RESET_LOG_OS_STACK_STEP_C0                  (uint32)(((RESET_LOG_OS_STACK0_SIZE / RESET_LOG_OS_STACK_STEP_COUNT) / 4) * 4)
#define RESET_LOG_OS_STACK_STEP_C1                  (uint32)(((RESET_LOG_OS_STACK1_SIZE / RESET_LOG_OS_STACK_STEP_COUNT) / 4) * 4)

#define RESET_LOG_TEST                              0

#define RESET_LOG_CORE_NUM                          2u
#define STORE_RESET_REASON_NUM_MAX                  (uint32)3
#define RESET_LOG_CALL_STACK_HIERARCHY              (uint32)5
#define RESET_LOG_SW_VERSION_LENGTH                 9u
#define PERF_CALC_SUM_No                            10u
#define STORE_CALL_STACK_DATA_LENGTH                240u
#define STORE_CALL_STACK_NUM_MAX                    (uint32)3

#define  MAX_ERRORTYPE_NUM                          (uint8)14u

extern boolean Reset_Log_isEnable;
extern uint16 Reset_Log_Task_Appl_5ms_Heart_C0;

#pragma pack(1)
/*below for call stack*/
typedef struct
{
    uint32 pc;
    uint32 sp;
    uint8 data[STORE_CALL_STACK_DATA_LENGTH];
    uint8 count;
} Reset_LogstackDataType;

typedef struct
{
    Reset_LogstackDataType stackData[STORE_CALL_STACK_NUM_MAX - 1u];
    uint8 stackNextIndex;
} Reset_LogCallStackType;

typedef struct
{
    uint16 index;
    uint32 timeX;
} Reset_LogDataType;

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
    uint16 isrIndex;
    uint16 taskIndex;
} Reset_LogFaultInfoType;

typedef struct
{
    uint32 cause;
    uint32 cause2;
    DateTi30_0 globalTime;
    Reset_LogFaultFromType faultFrom;
} Reset_LogBaseType;

typedef struct
{
    uint32 Errortype;
    uint32 Para;
    uint32 Subpara;
}Reset_LogSafetyErrType;

typedef struct
{
    Reset_LogBaseType base;
    uint32 feedWdg;
    Reset_LogFaultInfoType rstFaultInfo[RESET_LOG_CORE_NUM];
    CddTcanSbcStatusInfoType sbcReg;
    Reset_LogSafetyErrType safetyErrLog;
    uint16 osLimit[RESET_LOG_CORE_NUM];
    uint8 cpuAvg[RESET_LOG_CORE_NUM];
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
    Reset_LogstackDataType stackData;
    uint8 nextIndex;
    uint8 count;
} Reset_LogType;

typedef union
{
    uint8 dummy[700];
    Reset_LogType log;
} Reset_LogRamType;

typedef union
{
    uint8 dummy[500];
    Reset_LogCallStackType callStack;
} Reset_LogCallStackRamType;
#pragma pack()

extern Reset_LogRamType Reset_LogRam;

extern Reset_LogSafetyStateType Reset_LogSafetyState;

extern Reset_LogDTCMgrFlashType Reset_LogDTCMgrFlash_Flag;

extern Reset_LogReasonType Reset_LogReten;

void Reset_LogInit(void);

void Reset_LogFault(Reset_LogFaultFromType faultFrom, uint32 const *faultStackAddr, uint32 needReset);

Std_ReturnType Reset_LogRamInit(void);

Std_ReturnType Reset_LogCallStackRamInit(void);

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

#if RESET_LOG_TEST
void Reset_LogFaultTest_C0(uint32 type);

void Reset_LogFaultTest_C1(uint32 type);
#endif

#endif /* STORE_RESET_REASON_H */
/*  ANALYSIS_REPORT_END_JUSTIFICATION */
