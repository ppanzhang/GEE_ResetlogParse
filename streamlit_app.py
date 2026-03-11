import streamlit as st
import ctypes
import classType

# --- 核心工具函数 (适配自 main.py) ---
def space_separated_to_bytes(s):
    # 移除空格、换行符等，确保 hex 转换正常
    clean_s = s.replace(' ', '').replace('\n', '').replace('\t', '').strip()
    return bytes.fromhex(clean_s)

def bytes_to_cstruct(struct_type, byte_stream):
    if len(byte_stream) != ctypes.sizeof(struct_type):
        raise ValueError(
            f"字节流长度 ({len(byte_stream)}) 与 C 结构体大小 ({ctypes.sizeof(struct_type)}) 不匹配"
        )
    return struct_type.from_buffer_copy(byte_stream)

# --- Streamlit UI 配置 ---
st.set_page_config(page_title="GEE LZCU ResetLog Parser", layout="wide")

st.title("📂 GEE LZCU ResetLog 解析工具")
st.markdown("---")

# 侧边栏：项目选择与说明
with st.sidebar:
    st.header("项目配置")
    project_type = st.selectbox(
        "选择 Geely LZCU Micro 类型：",
        ["ZCUD_M", "ZCUP", "ZCUD_S"]
    )
    st.divider()
    st.info("💡 提示：\n- ZCUD_ID = 1D01\n- ZCUP_ID = 1D02")
    st.caption("Version: V0.1 (Web Edition)")

# 主界面布局：左侧输入，右侧输出
col_in, col_out = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 输入窗口 (Input A01C)")
    raw_hex_input = st.text_area(
        "请粘贴 Hex 数据 (支持空格/换行分隔):",
        height=450,
        placeholder="例如: 01 02 0A BB ..."
    )
    
    analyze_btn = st.button("开始分析 🚀", type="primary", use_container_width=True)

with col_out:
    st.subheader("📑 显示窗口 (Result)")
    result_area = st.empty() # 用于动态更新内容

# --- 处理点击逻辑 ---
if analyze_btn:
    if not raw_hex_input:
        st.warning("请先输入 Hex 数据再点击分析。")
    else:
        try:
            # 1. 转换字节流
            original_bytes = space_separated_to_bytes(raw_hex_input)
            
            # 2. 长度校验 (main.py 中固定为 700)
            if len(original_bytes) != 700:
                st.error(f"❌ 字节长度错误！预期 700 字节，实际收到 {len(original_bytes)} 字节。")
            else:
                outPutInfo = [f"Selected Project: {project_type}"]
                
                # 3. 根据项目类型选择对应的结构体和配置
                if project_type == "ZCUD_M" or project_type == "ZCUP":
                    # 注意：根据你的 main.py，ZCUD_M 和 ZCUP 共用 M_Reset_LogRamType
                    resetLog = bytes_to_cstruct(classType.M_Reset_LogRamType, original_bytes)
                    reasons_max = classType.M_STORE_RESET_REASON_NUM_MAX
                    fault_dict = classType.MFaultFromInfoDict
                    fault_enum = classType.MFaultFromInfo
                    log_data = resetLog.log
                elif project_type == "ZCUD_S":
                    resetLog = bytes_to_cstruct(classType.S_Reset_LogRamType, original_bytes)
                    reasons_max = classType.S_STORE_RESET_REASON_NUM_MAX
                    fault_dict = classType.SFaultFromInfoDict
                    fault_enum = classType.SFaultFromInfo
                    log_data = resetLog.log
                
                # 4. 解析循环 (复用 main.py 的格式化逻辑)
                for index in range(reasons_max):
                    entry = log_data.resetLog[index]
                    
                    outPutInfo.append(f"{'#'*30} Index <{index}> {'#'*30}")
                    outPutInfo.append(f"cause: {hex(entry.base.cause)}")
                    outPutInfo.append(f"cause2: {hex(entry.base.cause2)}")
                    
                    # 时间解析
                    t = entry.base.globalTime
                    time_str = f"复位发生时间：20{t.Yr1}年{t.Mth1}月{t.Day1}日{t.Hr1}时{t.Mins1}分{t.Sec1}秒, 时间可信度:{t.NoYes1}"
                    outPutInfo.append(time_str)
                    
                    # FaultFrom 解析
                    try:
                        f_val = entry.base.faultFrom
                        f_name = fault_dict.get(fault_enum(f_val), "UNKNOWN_FAULT")
                        outPutInfo.append(f"faultFrom: {f_name} ({hex(f_val)})")
                    except:
                        outPutInfo.append(f"faultFrom: 解析失败 ({hex(entry.base.faultFrom)})")
                        
                    outPutInfo.append(f"feedWdg: {hex(entry.feedWdg)}")
                    
                    # SBC 寄存器
                    sbc = entry.sbcReg
                    outPutInfo.append(f"sbcReg.FSM_RSRT_CNTR: {hex(sbc.FSM_RSRT_CNTR)}")
                    outPutInfo.append(f"sbcReg.INT_1: {hex(sbc.INT_1)}")
                    outPutInfo.append(f"sbcReg.INT_2: {hex(sbc.INT_2)}")
                    
                    # 针对 ZCUD_M/ZCUP 的额外 Core 信息解析 (如果需要可以取消注释)
                    if project_type != "ZCUD_S":
                        for i in range(classType.M_RESET_LOG_CORE_NUM):
                            core_info = entry.rstFaultInfo[i]
                            outPutInfo.append(f"core[{i}] mmfsr: {hex(core_info.fsr.mmfsr)}")
                    
                    outPutInfo.append("") # 换行

                outPutInfo.append(f"{'#'*30} -END- {'#'*30}")
                outPutInfo.append(f"nextIndex: {hex(log_data.nextIndex)}")
                outPutInfo.append(f"count: {hex(log_data.count)}")

                # 5. 输出到界面
                result_area.code("\n".join(outPutInfo), language="text")
                st.success("解析完成！")

        except Exception as e:
            st.error(f"解析过程中出错: {str(e)}")