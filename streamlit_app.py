import streamlit as st
import ctypes
import classType

# --- 工具函数 ---
def space_separated_to_bytes(s):
    clean_s = s.replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '').strip()
    return bytes.fromhex(clean_s)

def bytes_to_cstruct(struct_type, byte_stream):
    if len(byte_stream) != ctypes.sizeof(struct_type):
        raise ValueError(
            f"字节流长度 ({len(byte_stream)}) 与结构体大小 ({ctypes.sizeof(struct_type)}) 不匹配"
        )
    return struct_type.from_buffer_copy(byte_stream)

# --- Streamlit UI 设置 ---
st.set_page_config(page_title="GEE LZCU ResetLog Parser", layout="wide")
st.title("📂 GEE LZCU ResetLog 解析工具")

with st.sidebar:
    st.header("项目配置")
    project_type = st.selectbox("选择 Micro 类型：", ["ZCUD_M", "ZCUP", "ZCUD_S"])
    st.divider()
    st.caption("适配最新 classType 结构体定义")

col_in, col_out = st.columns([1, 1.3])

with col_in:
    st.subheader("📥 输入窗口 (Input)")
    raw_hex_input = st.text_area("请粘贴 Hex 数据:", height=450, placeholder="01 02 0A...")
    analyze_btn = st.button("开始分析 🚀", type="primary", use_container_width=True)

with col_out:
    st.subheader("📑 显示窗口 (Result)")
    result_area = st.empty()

# --- 解析与输出逻辑 ---
if analyze_btn:
    if not raw_hex_input:
        st.warning("请输入数据")
    else:
        try:
            original_bytes = space_separated_to_bytes(raw_hex_input)
            outPutInfo = []
            
            # 1. 根据项目确定结构体
            if project_type == "ZCUD_M":
                resetLog = bytes_to_cstruct(classType.M_Reset_LogRamType, original_bytes)
                log_data = resetLog.log
                reasons_max = classType.M_STORE_RESET_REASON_NUM_MAX
                core_num = classType.M_RESET_LOG_CORE_NUM
                fault_dict = classType.MFaultFromInfoDict
                fault_enum = classType.MFaultFromInfo
                outPutInfo.append("ZCUD_M")
            elif project_type == "ZCUP":
                resetLog = bytes_to_cstruct(classType.P_Reset_LogRamType, original_bytes)
                log_data = resetLog.log
                reasons_max = classType.P_STORE_RESET_REASON_NUM_MAX
                core_num = classType.P_RESET_LOG_CORE_NUM
                fault_dict = classType.PFaultFromInfoDict
                fault_enum = classType.PFaultFromInfo
                outPutInfo.append("ZCUP")
            else: # ZCUD_S
                resetLog = bytes_to_cstruct(classType.S_Reset_LogRamType, original_bytes)
                log_data = resetLog.log
                reasons_max = classType.S_STORE_RESET_REASON_NUM_MAX
                core_num = classType.S_RESET_LOG_CORE_NUM
                fault_dict = classType.SFaultFromInfoDict
                fault_enum = classType.SFaultFromInfo
                outPutInfo.append("ZCUD_S")

            # 2. 循环解析每一个 Index
            for index in range(reasons_max):
                entry = log_data.resetLog[index]
                outPutInfo.append(f"#####################################-Index<{index}>-###########################################")
                outPutInfo.append(f"cause:{hex(entry.base.cause)}")
                outPutInfo.append(f"cause2:{hex(entry.base.cause2)}")
                
                # 时间
                t = entry.base.globalTime
                outPutInfo.append(f"复位发生时间：20{t.Yr1}年{t.Mth1}月{t.Day1}日{t.Hr1}时{t.Mins1}分{t.Sec1}秒, 时间可信度:{t.NoYes1}")
                
                # FaultFrom
                f_val = entry.base.faultFrom
                f_name = fault_dict.get(fault_enum(f_val), "UNKNOWN")
                outPutInfo.append(f"faultFrom:{f_name}({hex(f_val)})")
                
                outPutInfo.append(f"feedWdg:{hex(entry.feedWdg)}")
                
                # SBC 寄存器完整输出
                sbc = entry.sbcReg
                outPutInfo.append(f"sbcReg.FSM_RSRT_CNTR:{hex(sbc.FSM_RSRT_CNTR)}")
                outPutInfo.append(f"sbcReg.REV_ID:{hex(sbc.REV_ID)}")
                outPutInfo.append(f"sbcReg.FSM_SLP_STAT:{hex(sbc.FSM_SLP_STAT)}")
                outPutInfo.append(f"sbcReg.NVM_REV:{hex(sbc.NVM_REV)}")
                outPutInfo.append(f"sbcReg.INT_1:{hex(sbc.INT_1)}")
                outPutInfo.append(f"sbcReg.INT_2:{hex(sbc.INT_2)}")
                outPutInfo.append(f"sbcReg.INT_3:{hex(sbc.INT_3)}")
                outPutInfo.append(f"sbcReg.INT_6:{hex(sbc.INT_6)}")
                outPutInfo.append(f"sbcReg.RESERVED:{hex(sbc.RESERVED)}")
                
                # 核心故障信息 (rstFaultInfo)
                for c in range(core_num):
                    f_info = entry.rstFaultInfo[c]
                    outPutInfo.append(f"rstFaultInfo[{c}].fsr.mmfsr:{hex(f_info.fsr.mmfsr)}")
                    outPutInfo.append(f"rstFaultInfo[{c}].fsr.bfsr:{hex(f_info.fsr.bfsr)}")
                    outPutInfo.append(f"rstFaultInfo[{c}].fsr.ufsr:{hex(f_info.fsr.ufsr)}")
                    outPutInfo.append(f"rstFaultInfo[{c}].fsr.hfsr:{hex(f_info.fsr.hfsr)}")
                    outPutInfo.append(f"rstFaultInfo[{c}].fsr.mmfar:{hex(f_info.fsr.mmfar)}")
                    outPutInfo.append(f"rstFaultInfo[{c}].fsr.bfar:{hex(f_info.fsr.bfar)}")
                    outPutInfo.append(f"rstFaultInfo[{c}].fsr.cfsr:{hex(f_info.fsr.cfsr)}")
                    outPutInfo.append(f"rstFaultInfo[{c}].fsr.sp:{hex(f_info.fsr.sp)}")
                    outPutInfo.append(f"rstFaultInfo[{c}].fsr.lr:{hex(f_info.fsr.lr)}")
                    outPutInfo.append(f"rstFaultInfo[{c}].fsr.pc:{hex(f_info.fsr.pc)}")
                    outPutInfo.append(f"rstFaultInfo[{c}].status:{hex(f_info.status)}")
                    outPutInfo.append(f"rstFaultInfo[{c}].isrIndex:{hex(f_info.isrIndex)}")
                    outPutInfo.append(f"rstFaultInfo[{c}].taskIndex:{hex(f_info.taskIndex)}")

                # 安全日志 (根据 ZCUD_M/ZCUP/ZCUD_S 结构略有差异，统一按期望格式输出)
                outPutInfo.append(f"safetyErrLog.Errortype:{hex(entry.safetyErrLog.Errortype)}")
                outPutInfo.append(f"safetyErrLog.Para:{hex(entry.safetyErrLog.Para)}")
                outPutInfo.append(f"safetyErrLog.Subpara:{hex(entry.safetyErrLog.Subpara)}")
                
                # OS 和 CPU 信息 (数组处理)
                # 假设对应的 osLimit 和 cpuAvg 按照 core_num 循环
                try:
                    # 如果结构体定义中这些是单值或数组，这里做兼容处理
                    if hasattr(entry, 'osLimit') and isinstance(entry.osLimit, (list, ctypes.Array)):
                        for i in range(len(entry.osLimit)):
                            outPutInfo.append(f"osLimit[{i}]:{hex(entry.osLimit[i])}")
                            outPutInfo.append(f"cpuAvg[{i}]:{hex(entry.cpuAvg[i])}")
                    else:
                        outPutInfo.append(f"osLimit[0]:{hex(entry.osLimit)}")
                        outPutInfo.append(f"cpuAvg[0]:{hex(entry.cpuAvg)}")
                except:
                    pass

                # 软件版本
                sw_ver = "".join([chr(b) for b in entry.swVersion if 32 <= b <= 126])
                outPutInfo.append(f"ContiSwVersion: {sw_ver}")
                outPutInfo.append("")

            outPutInfo.append("########################################-END-##############################################")
            outPutInfo.append(f"nextIndex:{hex(log_data.nextIndex)}")
            outPutInfo.append(f"count:{hex(log_data.count)}")

            # 渲染结果
            result_area.code("\n".join(outPutInfo), language="text")

        except Exception as e:
            st.error(f"解析出错: {str(e)}")