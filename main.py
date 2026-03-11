import sys
import ctypes
import classType

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox


def space_separated_to_bytes(s):
    return bytes.fromhex(s.replace(' ', ''))

def bytes_to_cstruct(Reset_LogRamType, byte_stream):
    print(len(byte_stream))
    # print(ctypes.sizeof(Reset_LogRamType))
    if len(byte_stream) != ctypes.sizeof(Reset_LogRamType):
        raise ValueError(
            "Byte stream length does not match the size of the C structure")

    cstruct_instance = Reset_LogRamType.from_buffer_copy(byte_stream)
    return cstruct_instance

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(760, 547)
        self.contents = QtWidgets.QTextEdit(parent=Dialog)
        self.contents.setGeometry(QtCore.QRect(30, 210, 701, 311))
        self.contents.setObjectName("contents")
        self.textEdit = QtWidgets.QTextEdit(parent=Dialog)
        self.textEdit.setGeometry(QtCore.QRect(30, 70, 701, 101))
        self.textEdit.setObjectName("textEdit")
        self.comboBox = QtWidgets.QComboBox(parent=Dialog)
        self.comboBox.setGeometry(QtCore.QRect(320, 10, 140, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        # self.comboBox.addItem("")
        self.label = QtWidgets.QLabel(parent=Dialog)
        self.label.setGeometry(QtCore.QRect(30, 50, 81, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 190, 81, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=Dialog)
        # self.label_3.setGeometry(QtCore.QRect(220, 10, 54, 16))
        self.label_3.setGeometry(QtCore.QRect(200, 10, 165, 22))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(parent=Dialog)
        self.pushButton.setGeometry(QtCore.QRect(590, 10, 75, 24))
        self.pushButton.setObjectName("pushButton")
        # self.label_4 = QtWidgets.QLabel(parent=Dialog)
        # self.label_4.setGeometry(QtCore.QRect(110, 50, 54, 16))
        # self.label_4.setObjectName("label_4")
        # self.D94BLineEdit = QtWidgets.QLineEdit(parent=Dialog)
        # self.D94BLineEdit.setGeometry(QtCore.QRect(150, 50, 181, 20))
        # self.D94BLineEdit.setObjectName("D94BLineEdit")
        # self.label_5 = QtWidgets.QLabel(parent=Dialog)
        # self.label_5.setGeometry(QtCore.QRect(370, 50, 54, 16))
        # self.label_5.setObjectName("label_5")
        # self.VersionLineEdit = QtWidgets.QLineEdit(parent=Dialog)
        # self.VersionLineEdit.setGeometry(QtCore.QRect(420, 50, 211, 21))
        # self.VersionLineEdit.setObjectName("VersionLineEdit")
        self.label_6 = QtWidgets.QLabel(parent=Dialog)
        self.label_6.setGeometry(QtCore.QRect(540, 45, 220, 22))
        self.label_6.setObjectName("label_6")

        self.pushButton.clicked.connect(self.clickButton)

        # self.D94BLineEdit.textChanged.connect(self.parseText)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "GEE_SZCU_VAVE_ResetLogParser_FullVersion-V0.1"))
        self.comboBox.setItemText(0, _translate("Dialog", "ZCUD_M"))
        self.comboBox.setItemText(1, _translate("Dialog", "ZCUP"))
        self.comboBox.setItemText(2, _translate("Dialog", "ZCUD_S"))
        self.label.setText(_translate("Dialog", "Input(A01C)："))
        self.label_2.setText(_translate("Dialog", "Result(A01C)："))
        #self.label_3.setText(_translate("Dialog", "Project:"))
        self.label_3.setText(_translate("Dialog", "Geely LZCU Micro ："))
        self.pushButton.setText(_translate("Dialog", "Analysis"))
        # self.label_4.setText(_translate("Dialog", "D94B:"))
        # self.label_5.setText(_translate("Dialog", "Version:"))
        self.label_6.setText(_translate("Dialog", "ZCUD_ID = 1D01; ZCUP_ID = 1D02"))
		
    def outputListToTextEdit(self, list_data):
        output_text = '\n'.join(list_data)
        self.contents.setText(output_text)

    # def parseText(self):
    #     d94bByteStream = self.D94BLineEdit.text()
    #     if len(d94bByteStream) >0:
    #         originalBytes = space_separated_to_bytes(d94bByteStream)
    #         ascii_str = originalBytes.decode('ascii')
    #         self.VersionLineEdit.setText(ascii_str)
    #         self.VersionLineEdit.show()
    #     else:
    #         print("d94bByteStream:" + d94bByteStream)

    def clickButton(self):
        byte_stream = self.textEdit.toPlainText()
        original_bytes = space_separated_to_bytes(byte_stream)
        if len(original_bytes) == 700:
            try:
                curPro = self.comboBox.currentText()
                outPutInfo = []
                outPutInfo.clear()
                outPutInfo.append(curPro)
                if curPro == "ZCUD_M" or curPro == "ZCUP":
                    resetLog = bytes_to_cstruct(classType.M_Reset_LogRamType, original_bytes)
                    for index in range(classType.M_STORE_RESET_REASON_NUM_MAX):                    
                        message = "#####################################-Index<{}>-###########################################"                                
                        formatted_message = message.format(index)
                        outPutInfo.append(formatted_message)
                        message = "cause:{}"
                        formatted_message = message.format(hex(resetLog.log.resetLog[index].base.cause))
                        outPutInfo.append(formatted_message)
                        message = "cause2:{}"
                        formatted_message = message.format(hex(resetLog.log.resetLog[index].base.cause2))
                        outPutInfo.append(formatted_message)

                        message = "复位发生时间：20{}年{}月{}日{}时{}分{}秒, 时间可信度:{}"
                        formatted_message = message.format(resetLog.log.resetLog[index].base.globalTime.Yr1,
                                                           resetLog.log.resetLog[index].base.globalTime.Mth1,
                                                           resetLog.log.resetLog[index].base.globalTime.Day1,
                                                           resetLog.log.resetLog[index].base.globalTime.Hr1,
                                                           resetLog.log.resetLog[index].base.globalTime.Mins1,
                                                           resetLog.log.resetLog[index].base.globalTime.Sec1,
                                                           resetLog.log.resetLog[index].base.globalTime.NoYes1)
                        outPutInfo.append(formatted_message)
                        message = "faultFrom:{}({})"
                        formatted_message = message.format(
                            classType.MFaultFromInfoDict[classType.MFaultFromInfo(resetLog.log.resetLog[index].base.faultFrom)], hex(resetLog.log.resetLog[index].base.faultFrom))
                        outPutInfo.append(formatted_message)
                        message = "feedWdg:{}"
                        formatted_message = message.format(hex(resetLog.log.resetLog[index].feedWdg))
                        outPutInfo.append(formatted_message)

                        # for i in range(classType.RESET_LOG_CORE_NUM):
                        #     if int(resetLog.log.resetLog[index].base.faultFrom) < 0x80:
                        #         message = "rstFaultInfo[{0}].RESET_LOG_CORE_NUM.mmRESET_LOG_CORE_NUM:{1}"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstFaultInfo[i].RESET_LOG_CORE_NUM.mmRESET_LOG_CORE_NUM))
                        #         outPutInfo.append(formatted_message)

                        #         message = "rstFaultInfo[{0}].RESET_LOG_CORE_NUM.bRESET_LOG_CORE_NUM:{1}"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstFaultInfo[i].RESET_LOG_CORE_NUM.bRESET_LOG_CORE_NUM))
                        #         outPutInfo.append(formatted_message)

                        #         message = "rstFaultInfo[{0}].RESET_LOG_CORE_NUM.uRESET_LOG_CORE_NUM:{1}"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstFaultInfo[i].RESET_LOG_CORE_NUM.uRESET_LOG_CORE_NUM))
                        #         outPutInfo.append(formatted_message)

                        #         message = "rstFaultInfo[{0}].RESET_LOG_CORE_NUM.hRESET_LOG_CORE_NUM:{1}"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstFaultInfo[i].RESET_LOG_CORE_NUM.hRESET_LOG_CORE_NUM))
                        #         outPutInfo.append(formatted_message)

                        #         message = "rstFaultInfo[{0}].RESET_LOG_CORE_NUM.mmfar:{1}"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstFaultInfo[i].RESET_LOG_CORE_NUM.mmfar))
                        #         outPutInfo.append(formatted_message)

                        #         message = "rstFaultInfo[{0}].RESET_LOG_CORE_NUM.bfar:{1}"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstFaultInfo[i].RESET_LOG_CORE_NUM.bfar))
                        #         outPutInfo.append(formatted_message)

                        #         message = "rstFaultInfo[{0}].RESET_LOG_CORE_NUM.cRESET_LOG_CORE_NUM:{1}"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstFaultInfo[i].RESET_LOG_CORE_NUM.cRESET_LOG_CORE_NUM))
                        #         outPutInfo.append(formatted_message)

                        #         message = "rstFaultInfo[{0}].RESET_LOG_CORE_NUM.sp:{1}"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstFaultInfo[i].RESET_LOG_CORE_NUM.sp))
                        #         outPutInfo.append(formatted_message)

                        #         message = "rstFaultInfo[{0}].RESET_LOG_CORE_NUM.lr:{1}"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstFaultInfo[i].RESET_LOG_CORE_NUM.lr))
                        #         outPutInfo.append(formatted_message)

                        #         message = "rstFaultInfo[{0}].RESET_LOG_CORE_NUM.pc:{1}"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstFaultInfo[i].RESET_LOG_CORE_NUM.pc))
                        #         outPutInfo.append(formatted_message)
                        #         message = "rstFaultInfo[{0}].status:[{1}]"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstFaultInfo[i].status))
                        #         outPutInfo.append(formatted_message)
                        #         for j in range(classType.RESET_LOG_CALL_STACK_HIERARCHY):
                        #             message = "rstFaultInfo[{0}].callStack[{1}]:{2}"
                        #             formatted_message = message.format(i, j, hex(
                        #                 resetLog.log.resetLog[index].rstInfoUnion.rstFaultInfo[i].callStack[j]))
                        #             outPutInfo.append(formatted_message)

                        #         message = "rstFaultInfo[{0}].isrIndex:[{1}]"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstFaultInfo[i].isrIndex))
                        #         outPutInfo.append(formatted_message)
                        #         message = "rstFaultInfo[{0}].taskIndex:[{1}]"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstFaultInfo[i].taskIndex))
                        #         outPutInfo.append(formatted_message)
                        #     else:
                        #         message = "rstWdgInfo[{0}].runnableIn:[index={1}, timeX={2}]"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstWdgInfo[i].runnableIn.index), hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstWdgInfo[i].runnableIn.timeX))
                        #         outPutInfo.append(formatted_message)
                        #         message = "rstWdgInfo[{0}].runnableOut:[index={1}, timeX={2}]"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstWdgInfo[i].runnableOut.index), hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstWdgInfo[i].runnableOut.timeX))
                        #         outPutInfo.append(formatted_message)
                        #         for j in range(classType.STORE_RESET_INFO_SUB_NUM):
                        #             message = "rstWdgInfo[{0}].anormalRunnable[{1}]:[index={2}, timeX={3}]"
                        #             formatted_message = message.format(i, j, hex(
                        #                 resetLog.log.resetLog[index].rstInfoUnion.rstWdgInfo[i].anormalRunnable[j].index),
                        #                                                hex(resetLog.log.resetLog[
                        #                                                        index].rstInfoUnion.rstWdgInfo[
                        #                                                        i].anormalRunnable[j].timeX))
                        #             outPutInfo.append(formatted_message)
                        #             message = "rstWdgInfo[{0}].anormalTask[{1}]:[index={2}, timeX={3}]"
                        #             formatted_message = message.format(i, j, hex(
                        #                 resetLog.log.resetLog[index].rstInfoUnion.rstWdgInfo[i].anormalTask[j].index), hex(
                        #                 resetLog.log.resetLog[index].rstInfoUnion.rstWdgInfo[i].anormalTask[j].timeX))
                        #             outPutInfo.append(formatted_message)

                        #         message = "rstWdgInfo[{0}].isrIn:[index={1}, timeX={2}]"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstWdgInfo[i].isrIn.index), hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstWdgInfo[i].isrIn.timeX))
                        #         outPutInfo.append(formatted_message)
                        #         message = "rstWdgInfo[{0}].isrOut:[index={1}, timeX={2}]"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstWdgInfo[i].isrOut.index), hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstWdgInfo[i].isrOut.timeX))
                        #         outPutInfo.append(formatted_message)
                        #         message = "rstWdgInfo[{0}].runnableSubIndex:[{1}]"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstWdgInfo[i].runnableSubIndex))
                        #         outPutInfo.append(formatted_message)
                        #         message = "rstWdgInfo[{0}].taskSubIndex:[{1}]"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstWdgInfo[i].taskSubIndex))
                        #         outPutInfo.append(formatted_message)

                        message = "sbcReg.FSM_RSRT_CNTR:{}"
                        formatted_message = message.format(hex(resetLog.log.resetLog[index].sbcReg.FSM_RSRT_CNTR))
                        outPutInfo.append(formatted_message)
                        message = "sbcReg.REV_ID:{}"
                        formatted_message = message.format(hex(resetLog.log.resetLog[index].sbcReg.REV_ID))
                        outPutInfo.append(formatted_message)
                        message = "sbcReg.FSM_SLP_STAT:{}"
                        formatted_message = message.format(hex(resetLog.log.resetLog[index].sbcReg.FSM_SLP_STAT))
                        outPutInfo.append(formatted_message)
                        message = "sbcReg.NVM_REV:{}"
                        formatted_message = message.format(hex(resetLog.log.resetLog[index].sbcReg.NVM_REV))
                        outPutInfo.append(formatted_message)
                        message = "sbcReg.INT_1:{}"
                        formatted_message = message.format(hex(resetLog.log.resetLog[index].sbcReg.INT_1))
                        outPutInfo.append(formatted_message)
                        message = "sbcReg.INT_2:{}"
                        formatted_message = message.format(hex(resetLog.log.resetLog[index].sbcReg.INT_2))
                        outPutInfo.append(formatted_message)
                        message = "sbcReg.INT_3:{}"
                        formatted_message = message.format(hex(resetLog.log.resetLog[index].sbcReg.INT_3))
                        outPutInfo.append(formatted_message)
                        message = "sbcReg.INT_6:{}"
                        formatted_message = message.format(hex(resetLog.log.resetLog[index].sbcReg.INT_6))
                        outPutInfo.append(formatted_message)
                        message = "sbcReg.RESERVED:{}"
                        formatted_message = message.format(hex(resetLog.log.resetLog[index].sbcReg.RESERVED))
                        outPutInfo.append(formatted_message)                    

                        for i in range(classType.M_RESET_LOG_CORE_NUM):                            
                            message = "rstFaultInfo[{0}].fsr.mmfsr:{1}"
                            formatted_message = message.format(i, hex(resetLog.log.resetLog[index].rstFaultInfo[i].fsr.mmfsr))
                            outPutInfo.append(formatted_message)
                            message = "rstFaultInfo[{0}].fsr.bfsr:{1}"
                            formatted_message = message.format(i, hex(resetLog.log.resetLog[index].rstFaultInfo[i].fsr.bfsr))
                            outPutInfo.append(formatted_message)
                            message = "rstFaultInfo[{0}].fsr.ufsr:{1}"
                            formatted_message = message.format(i, hex(resetLog.log.resetLog[index].rstFaultInfo[i].fsr.ufsr))
                            outPutInfo.append(formatted_message)
                            message = "rstFaultInfo[{0}].fsr.hfsr:{1}"
                            formatted_message = message.format(i, hex(resetLog.log.resetLog[index].rstFaultInfo[i].fsr.hfsr))
                            outPutInfo.append(formatted_message)
                            message = "rstFaultInfo[{0}].fsr.mmfar:{1}"
                            formatted_message = message.format(i, hex(resetLog.log.resetLog[index].rstFaultInfo[i].fsr.mmfar))
                            outPutInfo.append(formatted_message)
                            message = "rstFaultInfo[{0}].fsr.bfar:{1}"
                            formatted_message = message.format(i, hex(resetLog.log.resetLog[index].rstFaultInfo[i].fsr.bfar))
                            outPutInfo.append(formatted_message)
                            message = "rstFaultInfo[{0}].fsr.cfsr:{1}"
                            formatted_message = message.format(i, hex(resetLog.log.resetLog[index].rstFaultInfo[i].fsr.cfsr))
                            outPutInfo.append(formatted_message)
                            message = "rstFaultInfo[{0}].fsr.sp:{1}"
                            formatted_message = message.format(i, hex(resetLog.log.resetLog[index].rstFaultInfo[i].fsr.sp))
                            outPutInfo.append(formatted_message)
                            message = "rstFaultInfo[{0}].fsr.lr:{1}"
                            formatted_message = message.format(i, hex(resetLog.log.resetLog[index].rstFaultInfo[i].fsr.lr))
                            outPutInfo.append(formatted_message)
                            message = "rstFaultInfo[{0}].fsr.pc:{1}"
                            formatted_message = message.format(i, hex(resetLog.log.resetLog[index].rstFaultInfo[i].fsr.pc))
                            outPutInfo.append(formatted_message)

                            message = "rstFaultInfo[{0}].status:{1}"
                            formatted_message = message.format(i, hex(resetLog.log.resetLog[index].rstFaultInfo[i].status))
                            outPutInfo.append(formatted_message)
                            message = "rstFaultInfo[{0}].isrIndex:{1}"
                            formatted_message = message.format(i, hex(resetLog.log.resetLog[index].rstFaultInfo[i].isrIndex))
                            outPutInfo.append(formatted_message)
                            message = "rstFaultInfo[{0}].taskIndex:{1}"
                            formatted_message = message.format(i, hex(resetLog.log.resetLog[index].rstFaultInfo[i].taskIndex))
                            outPutInfo.append(formatted_message)  

                        message = "safetyErrLog.Errortype:{}"
                        formatted_message = message.format(hex(resetLog.log.resetLog[index].safetyErrLog.Errortype))
                        outPutInfo.append(formatted_message)
                        message = "safetyErrLog.Para:{}"
                        formatted_message = message.format(hex(resetLog.log.resetLog[index].safetyErrLog.Para))
                        outPutInfo.append(formatted_message)
                        message = "safetyErrLog.Subpara:{}"
                        formatted_message = message.format(hex(resetLog.log.resetLog[index].safetyErrLog.Subpara))
                        outPutInfo.append(formatted_message)

                        for i in range(classType.M_RESET_LOG_CORE_NUM):  
                            message = "osLimit[{0}]:{1}"
                            formatted_message = message.format(i, hex(resetLog.log.resetLog[index].osLimit[i]))
                            outPutInfo.append(formatted_message)
                            message = "cpuAvg[{0}]:{1}"
                            formatted_message = message.format(i, hex(resetLog.log.resetLog[index].cpuAvg[i]))
                            outPutInfo.append(formatted_message)                     

                        message = "ContiSwVersion: XXRX{}{}{}{}{}{}{}{}{}"
                        formatted_message = message.format(chr(resetLog.log.resetLog[index].swVersion[0]),
                                                           chr(resetLog.log.resetLog[index].swVersion[1]), 
                                                           chr(resetLog.log.resetLog[index].swVersion[2]), 
                                                           chr(resetLog.log.resetLog[index].swVersion[3]), 
                                                           chr(resetLog.log.resetLog[index].swVersion[4]), 
                                                           chr(resetLog.log.resetLog[index].swVersion[5]), 
                                                           chr(resetLog.log.resetLog[index].swVersion[6]), 
                                                           chr(resetLog.log.resetLog[index].swVersion[7]), 
                                                           chr(resetLog.log.resetLog[index].swVersion[8]))
                        outPutInfo.append(formatted_message)
                        message = ""
                        formatted_message = message.format()
                        outPutInfo.append(formatted_message)
                      
                    message = "########################################-END-##############################################" 
                    formatted_message = message.format()
                    outPutInfo.append(formatted_message)

                    message = "nextIndex:{}"
                    formatted_message = message.format(hex(resetLog.log.nextIndex))
                    outPutInfo.append(formatted_message)
                    message = "count:{}"
                    formatted_message = message.format(hex(resetLog.log.count))
                    outPutInfo.append(formatted_message)

                elif curPro == "ZCUD_S":
                    resetLog = bytes_to_cstruct(classType.S_Reset_LogRamType, original_bytes)
                    for index in range(classType.S_STORE_RESET_REASON_NUM_MAX):
                        message = "#####################################-Index<{}>-###########################################"   
                        formatted_message = message.format(index)
                        outPutInfo.append(formatted_message)
                        message = "cause:{}"
                        formatted_message = message.format(hex(resetLog.log.resetLog[index].base.cause))
                        outPutInfo.append(formatted_message)
                        message = "cause2:{}"
                        formatted_message = message.format(hex(resetLog.log.resetLog[index].base.cause2))
                        outPutInfo.append(formatted_message)

                        message = "复位发生时间：20{}年{}月{}日{}时{}分{}秒, 时间可信度:{}"
                        formatted_message = message.format(resetLog.log.resetLog[index].base.globalTime.Yr1,
                                                           resetLog.log.resetLog[index].base.globalTime.Mth1,
                                                           resetLog.log.resetLog[index].base.globalTime.Day1,
                                                           resetLog.log.resetLog[index].base.globalTime.Hr1,
                                                           resetLog.log.resetLog[index].base.globalTime.Mins1,
                                                           resetLog.log.resetLog[index].base.globalTime.Sec1,
                                                           resetLog.log.resetLog[index].base.globalTime.NoYes1)
                        outPutInfo.append(formatted_message)
                        message = "faultFrom:{}({})"
                        formatted_message = message.format(classType.SFaultFromInfoDict[classType.SFaultFromInfo(resetLog.log.resetLog[index].base.faultFrom)], hex(resetLog.log.resetLog[index].base.faultFrom))
                        outPutInfo.append(formatted_message)
                        message = "feedWdg:{}"
                        formatted_message = message.format(hex(resetLog.log.resetLog[index].feedWdg))
                        outPutInfo.append(formatted_message)

                        # for i in range(classType.P_RESET_LOG_CORE_NUM):
                        #     if int(resetLog.log.resetLog[index].base.faultFrom) < 0x80:
                        #         message = "rstFaultInfo[{0}].RESET_LOG_CORE_NUM.mmRESET_LOG_CORE_NUM:{1}"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstFaultInfo[i].RESET_LOG_CORE_NUM.mmRESET_LOG_CORE_NUM))
                        #         outPutInfo.append(formatted_message)

                        #         message = "rstFaultInfo[{0}].RESET_LOG_CORE_NUM.bRESET_LOG_CORE_NUM:{1}"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstFaultInfo[i].RESET_LOG_CORE_NUM.bRESET_LOG_CORE_NUM))
                        #         outPutInfo.append(formatted_message)

                        #         message = "rstFaultInfo[{0}].RESET_LOG_CORE_NUM.uRESET_LOG_CORE_NUM:{1}"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstFaultInfo[i].RESET_LOG_CORE_NUM.uRESET_LOG_CORE_NUM))
                        #         outPutInfo.append(formatted_message)

                        #         message = "rstFaultInfo[{0}].RESET_LOG_CORE_NUM.hRESET_LOG_CORE_NUM:{1}"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstFaultInfo[i].RESET_LOG_CORE_NUM.hRESET_LOG_CORE_NUM))
                        #         outPutInfo.append(formatted_message)

                        #         message = "rstFaultInfo[{0}].RESET_LOG_CORE_NUM.mmfar:{1}"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstFaultInfo[i].RESET_LOG_CORE_NUM.mmfar))
                        #         outPutInfo.append(formatted_message)

                        #         message = "rstFaultInfo[{0}].RESET_LOG_CORE_NUM.bfar:{1}"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstFaultInfo[i].RESET_LOG_CORE_NUM.bfar))
                        #         outPutInfo.append(formatted_message)

                        #         message = "rstFaultInfo[{0}].RESET_LOG_CORE_NUM.cRESET_LOG_CORE_NUM:{1}"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstFaultInfo[i].RESET_LOG_CORE_NUM.cRESET_LOG_CORE_NUM))
                        #         outPutInfo.append(formatted_message)

                        #         message = "rstFaultInfo[{0}].RESET_LOG_CORE_NUM.sp:{1}"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstFaultInfo[i].RESET_LOG_CORE_NUM.sp))
                        #         outPutInfo.append(formatted_message)

                        #         message = "rstFaultInfo[{0}].RESET_LOG_CORE_NUM.lr:{1}"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstFaultInfo[i].RESET_LOG_CORE_NUM.lr))
                        #         outPutInfo.append(formatted_message)

                        #         message = "rstFaultInfo[{0}].RESET_LOG_CORE_NUM.pc:{1}"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstFaultInfo[i].RESET_LOG_CORE_NUM.pc))
                        #         outPutInfo.append(formatted_message)
                        #         message = "rstFaultInfo[{0}].status:[{1}]"
                        #         formatted_message = message.format(i, hex(resetLog.log.resetLog[index].rstInfoUnion.rstFaultInfo[i].status))
                        #         outPutInfo.append(formatted_message)
                        #         for j in range(classType.RESET_LOG_CALL_STACK_HIERARCHY):
                        #             message = "rstFaultInfo[{0}].callStack[{1}]:{2}"
                        #             formatted_message = message.format(i, j, hex(resetLog.log.resetLog[index].rstInfoUnion.rstFaultInfo[i].callStack[j]))
                        #             outPutInfo.append(formatted_message)

                        #         message = "rstFaultInfo[{0}].isrIndex:[{1}]"
                        #         formatted_message = message.format(i, hex(resetLog.log.resetLog[index].rstInfoUnion.rstFaultInfo[i].isrIndex))
                        #         outPutInfo.append(formatted_message)
                        #         message = "rstFaultInfo[{0}].taskIndex:[{1}]"
                        #         formatted_message = message.format(i, hex(resetLog.log.resetLog[index].rstInfoUnion.rstFaultInfo[i].taskIndex))
                        #         outPutInfo.append(formatted_message)
                        #     else:
                        #         message = "rstWdgInfo[{0}].runnableIn:[index={1}, timeX={2}]"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstWdgInfo[i].runnableIn.index), hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstWdgInfo[i].runnableIn.timeX))
                        #         outPutInfo.append(formatted_message)
                        #         message = "rstWdgInfo[{0}].runnableOut:[index={1}, timeX={2}]"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstWdgInfo[i].runnableOut.index), hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstWdgInfo[i].runnableOut.timeX))
                        #         outPutInfo.append(formatted_message)
                        #         for j in range(classType.STORE_RESET_INFO_SUB_NUM):
                        #             message = "rstWdgInfo[{0}].anormalRunnable[{1}]:[index={2}, timeX={3}]"
                        #             formatted_message = message.format(i, j, hex(
                        #                 resetLog.log.resetLog[index].rstInfoUnion.rstWdgInfo[i].anormalRunnable[j].index),
                        #                                                hex(resetLog.log.resetLog[
                        #                                                        index].rstInfoUnion.rstWdgInfo[
                        #                                                        i].anormalRunnable[j].timeX))
                        #             outPutInfo.append(formatted_message)
                        #             message = "rstWdgInfo[{0}].anormalTask[{1}]:[index={2}, timeX={3}]"
                        #             formatted_message = message.format(i, j, hex(
                        #                 resetLog.log.resetLog[index].rstInfoUnion.rstWdgInfo[i].anormalTask[j].index), hex(
                        #                 resetLog.log.resetLog[index].rstInfoUnion.rstWdgInfo[i].anormalTask[j].timeX))
                        #             outPutInfo.append(formatted_message)

                        #         message = "rstWdgInfo[{0}].isrIn:[index={1}, timeX={2}]"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstWdgInfo[i].isrIn.index), hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstWdgInfo[i].isrIn.timeX))
                        #         outPutInfo.append(formatted_message)
                        #         message = "rstWdgInfo[{0}].isrOut:[index={1}, timeX={2}]"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstWdgInfo[i].isrOut.index), hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstWdgInfo[i].isrOut.timeX))
                        #         outPutInfo.append(formatted_message)
                        #         message = "rstWdgInfo[{0}].runnableSubIndex:[{1}]"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstWdgInfo[i].runnableSubIndex))
                        #         outPutInfo.append(formatted_message)
                        #         message = "rstWdgInfo[{0}].taskSubIndex:[{1}]"
                        #         formatted_message = message.format(i, hex(
                        #             resetLog.log.resetLog[index].rstInfoUnion.rstWdgInfo[i].taskSubIndex))
                        #         outPutInfo.append(formatted_message)
                        
                        for i in range(classType.S_RESET_LOG_CORE_NUM):                            
                            message = "rstFaultInfo[{0}].fsr.mmfsr:{1}"
                            formatted_message = message.format(i, hex(resetLog.log.resetLog[index].rstFaultInfo[i].fsr.mmfsr))
                            outPutInfo.append(formatted_message)
                            message = "rstFaultInfo[{0}].fsr.bfsr:{1}"
                            formatted_message = message.format(i, hex(resetLog.log.resetLog[index].rstFaultInfo[i].fsr.bfsr))
                            outPutInfo.append(formatted_message)
                            message = "rstFaultInfo[{0}].fsr.ufsr:{1}"
                            formatted_message = message.format(i, hex(resetLog.log.resetLog[index].rstFaultInfo[i].fsr.ufsr))
                            outPutInfo.append(formatted_message)
                            message = "rstFaultInfo[{0}].fsr.hfsr:{1}"
                            formatted_message = message.format(i, hex(resetLog.log.resetLog[index].rstFaultInfo[i].fsr.hfsr))
                            outPutInfo.append(formatted_message)
                            message = "rstFaultInfo[{0}].fsr.mmfar:{1}"
                            formatted_message = message.format(i, hex(resetLog.log.resetLog[index].rstFaultInfo[i].fsr.mmfar))
                            outPutInfo.append(formatted_message)
                            message = "rstFaultInfo[{0}].fsr.bfar:{1}"
                            formatted_message = message.format(i, hex(resetLog.log.resetLog[index].rstFaultInfo[i].fsr.bfar))
                            outPutInfo.append(formatted_message)
                            message = "rstFaultInfo[{0}].fsr.cfsr:{1}"
                            formatted_message = message.format(i, hex(resetLog.log.resetLog[index].rstFaultInfo[i].fsr.cfsr))
                            outPutInfo.append(formatted_message)
                            message = "rstFaultInfo[{0}].fsr.sp:{1}"
                            formatted_message = message.format(i, hex(resetLog.log.resetLog[index].rstFaultInfo[i].fsr.sp))
                            outPutInfo.append(formatted_message)
                            message = "rstFaultInfo[{0}].fsr.lr:{1}"
                            formatted_message = message.format(i, hex(resetLog.log.resetLog[index].rstFaultInfo[i].fsr.lr))
                            outPutInfo.append(formatted_message)
                            message = "rstFaultInfo[{0}].fsr.pc:{1}"
                            formatted_message = message.format(i, hex(resetLog.log.resetLog[index].rstFaultInfo[i].fsr.pc))
                            outPutInfo.append(formatted_message)

                            message = "rstFaultInfo[{0}].status:{1}"
                            formatted_message = message.format(i, hex(resetLog.log.resetLog[index].rstFaultInfo[i].status))
                            outPutInfo.append(formatted_message)
                            message = "rstFaultInfo[{0}].isrIndex:{1}"
                            formatted_message = message.format(i, hex(resetLog.log.resetLog[index].rstFaultInfo[i].isrIndex))
                            outPutInfo.append(formatted_message)
                            message = "rstFaultInfo[{0}].taskIndex:{1}"
                            formatted_message = message.format(i, hex(resetLog.log.resetLog[index].rstFaultInfo[i].taskIndex))
                            outPutInfo.append(formatted_message)  

                        message = "safetyErrLog.Errortype:{}"
                        formatted_message = message.format(hex(resetLog.log.resetLog[index].safetyErrLog.Errortype))
                        outPutInfo.append(formatted_message)
                        message = "safetyErrLog.Para:{}"
                        formatted_message = message.format(hex(resetLog.log.resetLog[index].safetyErrLog.Para))
                        outPutInfo.append(formatted_message)
                        message = "safetyErrLog.Subpara:{}"
                        formatted_message = message.format(hex(resetLog.log.resetLog[index].safetyErrLog.Subpara))
                        outPutInfo.append(formatted_message)

                        message = "osLimit:{}"
                        formatted_message = message.format(hex(resetLog.log.resetLog[index].osLimit))
                        outPutInfo.append(formatted_message)
                        message = "cpuAvg:{}"
                        formatted_message = message.format(hex(resetLog.log.resetLog[index].cpuAvg))
                        outPutInfo.append(formatted_message)

                        message = "ContiSwVersion: XXRX{}{}{}{}{}{}{}{}{}"
                        formatted_message = message.format(chr(resetLog.log.resetLog[index].swVersion[0]),
                                                           chr(resetLog.log.resetLog[index].swVersion[1]), 
                                                           chr(resetLog.log.resetLog[index].swVersion[2]), 
                                                           chr(resetLog.log.resetLog[index].swVersion[3]), 
                                                           chr(resetLog.log.resetLog[index].swVersion[4]), 
                                                           chr(resetLog.log.resetLog[index].swVersion[5]), 
                                                           chr(resetLog.log.resetLog[index].swVersion[6]), 
                                                           chr(resetLog.log.resetLog[index].swVersion[7]), 
                                                           chr(resetLog.log.resetLog[index].swVersion[8]))
                        outPutInfo.append(formatted_message)
                        message = ""
                        formatted_message = message.format(index)
                        outPutInfo.append(formatted_message)
                    message = "########################################-END-##############################################" 
                    formatted_message = message.format()
                    outPutInfo.append(formatted_message)
                    message = "nextIndex:{}"
                    formatted_message = message.format(hex(resetLog.log.nextIndex))
                    outPutInfo.append(formatted_message)
                    message = "count:{}"
                    formatted_message = message.format(hex(resetLog.log.count))
                    outPutInfo.append(formatted_message)              
                
                else:
                    QMessageBox.critical(self.pushButton, 'Error', "Not support.")

                self.contents.clear()
                self.outputListToTextEdit(outPutInfo)

            except:
                QMessageBox.question(self.pushButton, "Warring!", "出现未知错误了！")
        else:
            QMessageBox.critical(self.pushButton, 'Error', "Info byte is error!")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Dialog()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())

