/**********************************Copyright (c)**********************************/
/*                       BeiJing Jiaotong University    EE  DQL206LAB            */
/*-------------------------------File Information--------------------------------*/
/* File name:        main.c                                                      */
/* Author:                                                                       */
/* Current Version:  V1.0                                                        */
/* Time:             2021-01-10                                                  */
/* Function:         LLC converter                                               */
/*********************************************************************************/

/***********************************Header File***********************************/
#include "header.h"      /* main header definitions and Declaration*/
#include "DSP28x_Project.h"     // Device Headerfile and Examples Include File

extern Uint16 Cla1funcsLoadStart;
extern Uint16 Cla1funcsLoadEnd;
extern Uint16 Cla1funcsRunStart;

/******************************Function Declaration*******************************/
interrupt void CpuTimer0Isr(void);
interrupt void SciRxIsr(void);
interrupt void EpwmTZ2Isr(void);
interrupt void EpwmTZ1Isr(void);
interrupt void EPWM1_INT_Isr(void);
static void ApplyClaPwmCommands(void);

#pragma CODE_SECTION(CpuTimer0Isr, "ramfuncs");
#pragma DATA_SECTION(MAIN_PARA,"CpuFFTArray");

/****************************Global Variable Definition***************************/
dx_MAIN_PARA MAIN_PARA;
Uint16 flag[16];
//Uint16 error=0;
//Uint16 TBPRDVAL = 460;////Tpwm=2*TBPRD*TBCLK  60MHz=2* 460 *65K
//Uint16 TBPRDVAL = 1500; //Tpwm=2*TBPRD*TBCLK  60MHz=2* 1500 *20K  (Ŀǰ��������Ϊ40)
//Uint16 TBPRDVAL = 600;//Tpwm=2*TBPRD*TBCLK  60MHz=2* 600 *50K    ������20250705
Uint16 TBPRDVAL = 428;//70k
//Uint16 TBPRDVAL = 375;//Tpwm=2*TBPRD*TBCLK  60MHz=2* 375 *80K    ԭʼƵ��

Uint16 TBPRDVAL_OPENLOOP = 125;
// Uint16 START_TIME = 0 ;//   0.1ms * softtime = 5ms
Uint16 EN_sign = 0;
Uint16 yuchongdianjidianqi=1;  //yuchongdianjidianqi=0 ��
Uint16 zhudianjidianqi=1;      //���̵���=0��
#define DAB_PWM_DUTY_MIN          (0.001f)
#define DAB_PWM_DUTY_MAX          (0.999f)
#define DAB_PWM_PHASE_SCALE       (2.0f / 3.0f)
#define EPWM_ISR_CAN_DIVIDER       (30U) // Preserve about 2.34kHz CAN main-loop scheduling at 70kHz ISR.
#define CLA_CONTROL_DIVIDER        (4U)  // Run the full CLA Task2 control calculation at about 23.36kHz.

// Runtime diagnostics for PWM/CLA scheduling.
volatile Uint16 epwm1_isr_count = 0;
volatile Uint16 cla_task2_trigger_count = 0;
volatile Uint16 cla_task2_busy_count = 0;
volatile Uint16 pwm_output_state = 0;
volatile Uint16 cla_control_divider = 0;
volatile Uint16 epwm1_can_divider = 0;
volatile Uint16 can_receive_pending = 0;
//Uint16 binaryArray[]={0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0};  //�������տ�����
//Uint16 binaryArray1[]={0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0};  //���յ���ָ��
//Uint16 binaryArray2[]={0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0};  //����SOCָ��

//Unit16 StartStop_step =0;

//Unit16 flag1=0;
//Uint16 binaryArray1[];
/************************************Function*************************************/
/*********************************************************************************/
/* Name:      main()                                                             */
/* Author:                                                                       */
/* Time:      2021-01-10                                                         */
/* Description:                                                                  */
/*                                                                               */
/*********************************************************************************/
int timer =0 ;

void main(void)
{

//================================initial system===================================
//------------------------------initial WatchDog and PLL---------------------------
    InitSysCtrl();
//--------------------------------initial GPIO-------------------------------------
    InitGpio();
//------------------------------ALL interrupt disable------------------------------
    DINT;
//---------------------------initial PIE control registers-------------------------
    InitPieCtrl();
    InitTZ();
//-------------------------disable interrupt and clear flag------------------------
    IER = 0x0000;
    IFR = 0x0000;
//------------------------------initial PIE vector table---------------------------
    InitPieVectTable();
//-----------------------------------initial flash---------------------------------
    MemCopy(&RamfuncsLoadStart, &RamfuncsLoadEnd, &RamfuncsRunStart);
    MemCopy(&Cla1funcsLoadStart, &Cla1funcsLoadEnd, &Cla1funcsRunStart);
    InitFlash();
    InitCla();
//-----------------------------initial interrupt address---------------------------
    EALLOW;
    PieVectTable.TINT0 = &CpuTimer0Isr;


    PieVectTable.EPWM2_TZINT= &EpwmTZ2Isr;
    PieVectTable.EPWM1_INT=&EPWM1_INT_Isr;  //�޸�δEPWM1�ж�
    PieVectTable.SCIRXINTA = &SciRxIsr;
    EDIS;
//---------------------------------initial peripheral------------------------------
    InitState();
    InitCpuTimers();
    InitADC();
    InitEPwm();
    InitSci();
    InitSpi();
    InitCAN();
    eCAN_Config();
//  InitRELAY();
    //EnePwm_master();
//------------------------------enable peripheral interrupt------------------------
    PieCtrlRegs.PIEIER1.bit.INTx7 = 1;  //CpuTimer0Isr
//  PieCtrlRegs.PIEIER2.bit.INTx1 = 1;  //EpwmTZ1Isr
//  PieCtrlRegs.PIEIER2.bit.INTx2 = 1;  //EpwmTZ2Isr
//    PieCtrlRegs.PIEIER3.bit.INTx5 = 1; //EPWM5_INT_Isr�޸�1.4   ��������2025.07.08 �޸�Ϊ EPWM1_INT_Isr�жϣ�
    PieCtrlRegs.PIEIER9.bit.INTx1 = 1;  //SciRxIsr
    PieCtrlRegs.PIECTRL.bit.ENPIE = 1;
    PieCtrlRegs.PIEIER3.bit.INTx1 = 1;  //EPM1�ж�

    IER |= (M_INT1|M_INT2|M_INT3|M_INT9);
    EINT;   // Enable Global interrupt INTM
    ERTM;   // Enable Global realtime interrupt DBGM
//------------------------------start timer0 counter-------------------------------
    EALLOW;
    EPwm1Regs.TZEINT.bit.OST = 1;    //Enable Interrupt generation; a one-shot trip event will cause a EPWM1_TZINT PIE interrupt.
    EPwm2Regs.TZEINT.bit.OST = 1;
    EPwm3Regs.TZEINT.bit.OST = 1;
    EPwm4Regs.TZEINT.bit.OST = 1;
    EPwm5Regs.TZEINT.bit.OST = 1;
    EPwm6Regs.TZEINT.bit.OST = 1;
    EDIS;
    CpuTimer0Regs.TCR.bit.TSS = 0;

//--------------------------����ϴ���־λ--------------------
    M_ClrFlag(SL_Pulse_Finish);  //��������
    M_ClrFlag(SL_GUZHANG);        //����
    M_ClrFlag(SL_Slave_Precharge);    //Ԥ������
    M_ClrFlag(SL_LLC_Precharge_Finish);
    M_ClrFlag(SL_H_Precharge_Finish);
    M_ClrFlag(SL_SOFTSTART1);
    M_ClrFlag(SL_Host_Precharge);
    M_ClrFlag(SL_Host_Precharge_Finish);
    M_ClrFlag(SL_Precharge_Finish);
    M_ClrFlag(SL_Is_Host);
    M_ClrFlag(SL_Slave_Precharge);
    M_ClrFlag(SL_TEST);

    M_ClrFlag(SL_ERRSTOP);
//-----------------------����----------
//    M_ClrFlag(SL_MASTERSTOP);
//    M_ClrFlag(SL_ERRSTOP);
//    M_SetFlag(SL_WORKON);


//    GpioDataRegs.GPBSET.bit.GPIO42 = 1;  //Ԥ���
//    MAIN_PARA.Pre_charged_cnt=0;   //����޸����� 0527
//    M_ClrFlag(SL_YUCHONGOVER);

    GpioDataRegs.GPBCLEAR.bit.GPIO43 = 1;//RL2  ����Ԥ���̵���
    GpioDataRegs.GPBSET.bit.GPIO42 = 1;//RL1  �������̵���
    GpioDataRegs.GPBCLEAR.bit.GPIO39 = 1;//RL3  ��·�̵���
    GpioDataRegs.GPASET.bit.GPIO25 = 1;//RL4  ������̵���
    GpioDataRegs.GPACLEAR.bit.GPIO18 = 1;//RL5  ���Ԥ���̵���


//    _DP_SUBAT3 = 0;


    while(1)
    {
/////////////////////////////////TEST/////////////////////

        RS485Ctrl();
        // CAN receive processing runs after Modbus and is scheduled at 1/10 EPWM1 ISR rate.
        if(can_receive_pending != 0)
        {
            can_receive_pending = 0;
            eCAN_Rec();
            eCAN_data_recive();
        }

//        EnePwm_master();   //������H������������
//        GpioDataRegs.GPBCLEAR.bit.GPIO40 = 1;
//        GpioDataRegs.GPASET.bit.GPIO25 = 1;//H��������̵���K2
//        GpioDataRegs.GPBCLEAR.bit.GPIO39 = 1;//H����·�̵���K4

//----------------------------------������/ʹ���ź�ָ��----------------------------------------------
//        if(_MC_CLRDATA == 0) EN_sign=0;//������/��ֹ����PI����ֹ��Դ���
//        else if(_MC_CLRDATA == 1) EN_sign=1;//������/��������PI��������Դ���
//----------------------------------��ʾ������----------------------------------------------
        //--NO.1=200ms loop--
        if(MAIN_PARA.delay_50ms>=DELAY_50MS)//����Ƶ�ʵ���ʱ��
        {
            GpioDataRegs.GPASET.bit.GPIO20 = 1;
//            eCAN_Send();                              //��ʾ������
            MAIN_PARA.delay_50ms = 0;
            GpioDataRegs.GPACLEAR.bit.GPIO20 = 1;
        }
        if(MAIN_PARA.delay_200ms<=6384)        MAIN_PARA.delay_200ms++;
        if(MAIN_PARA.delay_200ms>=DELAY_200MS)//更改频率调节时间
        {
            DisplayCtrl();                              //显示屏更新
            MAIN_PARA.delay_200ms = 0;
        }
//---------------------------------------------------------------------------------
        if((MAIN_PARA.delay_poweron>=DELAY_POWERON)&&((M_ChkFlag(SL_POWERON))!=0))//5s=5000*10*100    MAIN_PARA.delay_poweron add in cputimer0
        {
            M_ClrFlag(SL_POWERON);
            MAIN_PARA.delay_poweron = 0;


            PieCtrlRegs.PIEIER2.bit.INTx2 = 1;  //EpwmTZ1Isr

            IER |= (M_INT2);
            EINT;   // Enable Global interrupt INTM      line 89 has already EINT
            ERTM;   // Enable Global realtime interrupt DBGM
        }
    }
}

/*********************************************************************************/
/* Name:      CpuTimer0Isr()                                                     */
/* Author:    YZY                                                                */
/* Time:      2021-01-10                                                         */
/* Description:50us                                                              */
/*                                                                               */
/*********************************************************************************/
interrupt void CpuTimer0Isr(void)
{
//    if (_MC_SNUMBER4==1)
    Errojudgment(); //�����ж�
//    ERROR_HANDLE();
//---------------------------------------------------------------------------------
//    GpioDataRegs.GPASET.bit.GPIO19 =1;
//    GpioDataRegs.GPACLEAR.bit.GPIO19 =1;
//---------------------------------------------------------------------------------
    if(MODBUS_RS485.delay_sciover<=16384)   MODBUS_RS485.delay_sciover++;
    MAIN_PARA.pulse_cnt++;
    if(MAIN_PARA.pulse_cnt>=10)     MAIN_PARA.pulse_cnt = 0;

    if((M_ChkFlag(SL_SYS_START)!=0)&&(M_ChkFlag(SL_POWERON)!=1)) MAIN_PARA.softstart_cnt++;

//---------------------------------------------------------------------------------
    switch (MAIN_PARA.pulse_cnt)
    {

        case 0:
        {
//            Errojudgment();
//          ProtectCtrl();                              //system protect//TEST
            break;

        }
        case 1:
        {
//            Errojudgment();
//            eCAN_Send();
//          GiveCtrl();
            break;
        }
        case 2:
        {
//            eCAN_Send();
//            Errojudgment();
//          ProtectCtrl();                              //system protect
            break;
        }
        case 3:
        {
//            Errojudgment();
//            GpioDataRegs.GPASET.bit.GPIO21 = 1;
//            eCAN_Send();                              //����CAN
//            GpioDataRegs.GPACLEAR.bit.GPIO21 = 1;
//          GiveCtrl();                                 //give order
            break;
        }
        case 4:
        {
//            eCAN_Send();
//           Errojudgment();
//          ProtectCtrl();                              //system protect
            break;
        }
        case 6:
        {
//            eCAN_Send();
//            Errojudgment();
//          ProtectCtrl();                              //system protect
            break;
        }

        case 8:
        {
            MAIN_PARA.pulse_cnt2++;
            if(MAIN_PARA.pulse_cnt2>=50)
            {

                eCAN_Send();
                MAIN_PARA.pulse_cnt2 = 0;

            }

//            Errojudgment();
            //ProtectCtrl();                              //system protect
            break;
        }
        case 9:
            {
                //PowerCtrl();
                //if(MAIN_PARA.delay_5ms<=16384)          MAIN_PARA.delay_5ms++;
                //if(MAIN_PARA.delay_25ms<=16384)         MAIN_PARA.delay_25ms++;
                if(MAIN_PARA.delay_50ms<=16384)         MAIN_PARA.delay_50ms++;
                //if(MAIN_PARA.delay_100ms<=16384)        MAIN_PARA.delay_100ms++;
                if(MAIN_PARA.delay_200ms<=16384)        MAIN_PARA.delay_200ms++;
                if(MAIN_PARA.delay_500ms<=16384)        MAIN_PARA.delay_500ms++;
                if(MAIN_PARA.delay_poweron<=16384)      MAIN_PARA.delay_poweron++;
                //if(MODBUS_RS485.delay_sciover<=16384)   MODBUS_RS485.delay_sciover++;
                //if(MODBUS_RS485.allow_rec<=16384)       MODBUS_RS485.allow_rec++;
                //if(ARI_PARA.delay_pwmout<=16384)        ARI_PARA.delay_pwmout++;
                //if(POWER_PARA.delay_prec1<=16384)       POWER_PARA.delay_prec1++;
                //if(POWER_PARA.delay_prec2<=16384)       POWER_PARA.delay_prec2++;
  //              if(POWER_PARA.delay_prec6<=16384)       POWER_PARA.delay_prec6++;
                if(POWER_PARA.delay_start<=16384)       POWER_PARA.delay_start++;
                if(PRO_PARA.delay_recover<=16384)       PRO_PARA.delay_recover++;
      //          if(PRO_PARA.delay_scierror<=32000)      //PRO_PARA.delay_scierror++;
                if(PRO_PARA.delay_subatlv1<=16384)      PRO_PARA.delay_subatlv1++;
                if(PRO_PARA.delay_subuslv1<=16384)      PRO_PARA.delay_subuslv1++;
//                if(MAIN_PARA.delay_1s<=16384)         MAIN_PARA.delay_1s++;

                if(MAIN_PARA.delay_10s0<=16384)         MAIN_PARA.delay_10s0++;
                if(MAIN_PARA.delay_10s1<=16384)         MAIN_PARA.delay_10s1++;

                break;
            }
        default:
        {
            break;
        }
    }
//---------------------------------------------------------------------------------
//    PwmDriveCtrl();                                     //epwm
    //---------------------------------------------------------------------------------
    PieCtrlRegs.PIEACK.all = PIEACK_GROUP1;
    CpuTimer0Regs.TCR.bit.TRB = 1;
    CpuTimer0Regs.TCR.bit.TIF = 1;

}

/*********************************************************************************/
/* Name:      EpwmTZ1Isr()                                                       */
/* Author:    nchen                                                              */
/* Time:      20190101                                                           */
/* Parameters:none                                                               */
/* Returns:   none                                                               */
/* Description:Ts=200us+(ubus-440V)*100us/20V                                    */
/*             cap value->(440~800)V->800V@2ms@50%->2/2=1ms->60000               */
/*********************************************************************************/
interrupt void EpwmTZ2Isr(void) //г���ѹ����
{
//----------------------------------disable-ePWM1A-ePWM6B-----------------------------------------------
    DisePWM();
    EALLOW;
    EPwm2Regs.TZCLR.bit.INT = 1;            //clear FLG
    EPwm2Regs.TZCLR.bit.OST = 1;            //clear FLG
    EDIS;
    M_SetFlag(SL_TZ1INT);

//    GpioDataRegs.GPBCLEAR.bit.GPIO43 = 1;//LLC�������̵���K6
//    GpioDataRegs.GPBCLEAR.bit.GPIO42 = 1;//LLC����Ԥ���̵���K5
//
//    GpioDataRegs.GPACLEAR.bit.GPIO25 = 1;//H��������̵���K2
//    GpioDataRegs.GPACLEAR.bit.GPIO18 = 1;//H�����Ԥ���̵���K3

    PieCtrlRegs.PIEACK.all = PIEACK_GROUP2;
}

interrupt void EpwmTZ1Isr(void) //��ص�����ĸ�ߵ�������
{
//----------------------------------disable-ePWM1A-ePWM6B-----------------------------------------------
    DisePWM();
//    EPwm1Regs.AQCSFRC.bit.CSFA = 1;
//    EPwm1Regs.AQCSFRC.bit.CSFB = 1;
//    EPwm2Regs.AQCSFRC.bit.CSFA = 1;
//    EPwm2Regs.AQCSFRC.bit.CSFB = 1;
//    EPwm3Regs.AQCSFRC.bit.CSFA = 1;
//    EPwm3Regs.AQCSFRC.bit.CSFB = 1;
//    EPwm4Regs.AQCSFRC.bit.CSFA = 1;
//    EPwm4Regs.AQCSFRC.bit.CSFB = 1;
//    EPwm5Regs.AQCSFRC.bit.CSFA = 1;
//    EPwm5Regs.AQCSFRC.bit.CSFB = 1;
//    EPwm6Regs.AQCSFRC.bit.CSFA = 1;
//    EPwm6Regs.AQCSFRC.bit.CSFB = 1;
    M_SetFlag(SL_TZ1INT);
//    GpioDataRegs.GPBCLEAR.bit.GPIO43 = 1;//LLC�������̵���K6
//    GpioDataRegs.GPBCLEAR.bit.GPIO42 = 1;//LLC����Ԥ���̵���K5
//
//    GpioDataRegs.GPACLEAR.bit.GPIO25 = 1;//H��������̵���K2
//    GpioDataRegs.GPACLEAR.bit.GPIO18 = 1;//H�����Ԥ���̵���K3

    PieCtrlRegs.PIEACK.all = PIEACK_GROUP2;
}
/*********************************************************************************/
/* Name:      SciRxIsr()                                                         */
/* Author:    YZY                                                                */
/* Time:      2021-01-10                                                         */
/* Parameters:none                                                               */
/* Returns:   none                                                               */
/* Description:                                                                  */
/*                                                                               */
/*********************************************************************************/
interrupt void SciRxIsr(void)
{
    MODBUS_RS485.rxb[MODBUS_RS485.data_num] = SciaRegs.SCIRXBUF.bit.RXDT&0xFF;
    MODBUS_RS485.data_num++;
    M_SetFlag(SL_RS485_RXINT);
    SciaRegs.SCIFFRX.bit.RXFFINTCLR = 1;
    SciaRegs.SCIFFRX.bit.RXFFOVRCLR = 1;

    PieCtrlRegs.PIEACK.all = PIEACK_GROUP9;
}

#if 0
static void UpdateDabPwmNewModulation(float d1, float d2, float fai)
{
    float duty1;
    float duty2;
    float duty3;
    float duty4;
    float phase_count;
    Uint16 phase_direction;

    // 新调制输入限幅：d1/d2 控制桥臂占空比，fai 控制原副边整体移相。
    if(d1 < 0.0f) d1 = 0.0f;
    if(d1 > 2.0f) d1 = 2.0f;
    if(d2 < 0.0f) d2 = 0.0f;
    if(d2 > 2.0f) d2 = 2.0f;
    if(fai < -1.0f) fai = -1.0f;
    if(fai > 1.0f) fai = 1.0f;

    // duty mapping：同一侧两桥臂同相，左右桥臂差异仅由 CMPA 产生。
    duty1 = 0.5f * d1;
    duty2 = 1.0f - 0.5f * d1;
    duty3 = 0.5f * d2;
    duty4 = 1.0f - 0.5f * d2;

    // 避免 0%/100% 极限占空比，Dead-Band 仍由 ePWM DB 模块产生。
    if(duty1 < DAB_PWM_DUTY_MIN) duty1 = DAB_PWM_DUTY_MIN;
    if(duty1 > DAB_PWM_DUTY_MAX) duty1 = DAB_PWM_DUTY_MAX;
    if(duty2 < DAB_PWM_DUTY_MIN) duty2 = DAB_PWM_DUTY_MIN;
    if(duty2 > DAB_PWM_DUTY_MAX) duty2 = DAB_PWM_DUTY_MAX;
    if(duty3 < DAB_PWM_DUTY_MIN) duty3 = DAB_PWM_DUTY_MIN;
    if(duty3 > DAB_PWM_DUTY_MAX) duty3 = DAB_PWM_DUTY_MAX;
    if(duty4 < DAB_PWM_DUTY_MIN) duty4 = DAB_PWM_DUTY_MIN;
    if(duty4 > DAB_PWM_DUTY_MAX) duty4 = DAB_PWM_DUTY_MAX;

    // phase mapping：报告实测 Delta_t/Tsw=fai/3，up-down 周期为 2*TBPRDVAL。
    if(fai >= 0.0f)
    {
        phase_count = fai * DAB_PWM_PHASE_SCALE * (float)TBPRDVAL;
        phase_direction = 0;
    }
    else
    {
        phase_count = (-fai) * DAB_PWM_PHASE_SCALE * (float)TBPRDVAL;
        phase_direction = 1;
    }
    if(phase_count > (float)TBPRDVAL) phase_count = (float)TBPRDVAL;

    EALLOW;
    // CMPA mapping：当前 CAU=clear/CAD=set，因此 duty=CMPA/TBPRDVAL。
    EPwm1Regs.CMPA.half.CMPA = (Uint16)(duty1 * (float)TBPRDVAL);
    EPwm2Regs.CMPA.half.CMPA = (Uint16)(duty2 * (float)TBPRDVAL);
    EPwm3Regs.CMPA.half.CMPA = (Uint16)(duty3 * (float)TBPRDVAL);
    EPwm4Regs.CMPA.half.CMPA = (Uint16)(duty4 * (float)TBPRDVAL);

    // 原边两桥臂同相；副边两桥臂同相并整体相对原边移相。
    EPwm1Regs.TBPHS.half.TBPHS = 0;
    EPwm2Regs.TBPHS.half.TBPHS = 0;
    EPwm3Regs.TBPHS.half.TBPHS = (Uint16)phase_count;
    EPwm4Regs.TBPHS.half.TBPHS = (Uint16)phase_count;
    EPwm1Regs.TBCTL.bit.PHSDIR = 0;
    EPwm2Regs.TBCTL.bit.PHSDIR = 0;
    EPwm3Regs.TBCTL.bit.PHSDIR = phase_direction;
    EPwm4Regs.TBCTL.bit.PHSDIR = phase_direction;
    EDIS;
}
#endif

static void ApplyClaPwmCommands(void)
{
    EALLOW;
    // CLA already completed all duty/phase math; CPU only writes integer commands.
    EPwm1Regs.CMPA.half.CMPA = (Uint16)cmpa1_cmd;
    EPwm2Regs.CMPA.half.CMPA = (Uint16)cmpa2_cmd;
    EPwm3Regs.CMPA.half.CMPA = (Uint16)cmpa3_cmd;
    EPwm4Regs.CMPA.half.CMPA = (Uint16)cmpa4_cmd;
    EPwm3Regs.TBPHS.half.TBPHS = (Uint16)tbphs3_cmd;
    EPwm4Regs.TBPHS.half.TBPHS = (Uint16)tbphs4_cmd;
    EPwm3Regs.TBCTL.bit.PHSDIR = (Uint16)phsdir_cmd;
    EPwm4Regs.TBCTL.bit.PHSDIR = (Uint16)phsdir_cmd;
    EDIS;
}

static void EnableDabPwmOutputs(void)
{
    EALLOW;
    GpioCtrlRegs.GPAPUD.bit.GPIO0 = 1;
    GpioCtrlRegs.GPAPUD.bit.GPIO1 = 1;
    GpioCtrlRegs.GPAPUD.bit.GPIO2 = 1;
    GpioCtrlRegs.GPAPUD.bit.GPIO3 = 1;
    GpioCtrlRegs.GPAPUD.bit.GPIO4 = 1;
    GpioCtrlRegs.GPAPUD.bit.GPIO5 = 1;
    GpioCtrlRegs.GPAPUD.bit.GPIO6 = 1;
    GpioCtrlRegs.GPAPUD.bit.GPIO7 = 1;
    GpioCtrlRegs.GPAMUX1.bit.GPIO0 = 1;
    GpioCtrlRegs.GPAMUX1.bit.GPIO1 = 1;
    GpioCtrlRegs.GPAMUX1.bit.GPIO2 = 1;
    GpioCtrlRegs.GPAMUX1.bit.GPIO3 = 1;
    GpioCtrlRegs.GPAMUX1.bit.GPIO4 = 1;
    GpioCtrlRegs.GPAMUX1.bit.GPIO5 = 1;
    GpioCtrlRegs.GPAMUX1.bit.GPIO6 = 1;
    GpioCtrlRegs.GPAMUX1.bit.GPIO7 = 1;
    EDIS;
}

static void DisableDabPwmOutputs(void)
{
    EALLOW;
    GpioCtrlRegs.GPAMUX1.bit.GPIO0 = 0;
    GpioCtrlRegs.GPAMUX1.bit.GPIO1 = 0;
    GpioCtrlRegs.GPAMUX1.bit.GPIO2 = 0;
    GpioCtrlRegs.GPAMUX1.bit.GPIO3 = 0;
    GpioCtrlRegs.GPAMUX1.bit.GPIO4 = 0;
    GpioCtrlRegs.GPAMUX1.bit.GPIO5 = 0;
    GpioCtrlRegs.GPAMUX1.bit.GPIO6 = 0;
    GpioCtrlRegs.GPAMUX1.bit.GPIO7 = 0;

    GpioDataRegs.GPACLEAR.bit.GPIO0 = 1;
    GpioDataRegs.GPACLEAR.bit.GPIO1 = 1;
    GpioDataRegs.GPACLEAR.bit.GPIO2 = 1;
    GpioDataRegs.GPACLEAR.bit.GPIO3 = 1;
    GpioDataRegs.GPACLEAR.bit.GPIO4 = 1;
    GpioDataRegs.GPACLEAR.bit.GPIO5 = 1;
    GpioDataRegs.GPACLEAR.bit.GPIO6 = 1;
    GpioDataRegs.GPACLEAR.bit.GPIO7 = 1;

    // 停机时清除全部相移，避免恢复运行时残留相移。
    EPwm1Regs.TBPHS.half.TBPHS = 0;
    EPwm2Regs.TBPHS.half.TBPHS = 0;
    EPwm3Regs.TBPHS.half.TBPHS = 0;
    EPwm4Regs.TBPHS.half.TBPHS = 0;
    EDIS;
}


interrupt void EPWM1_INT_Isr(void)
{
    epwm1_isr_count++;

//    Errojudgment();    //ԭ ���� ������20250705
//    stop_host();
//    EPwm1Regs.CMPA.half.CMPA = TBPRDVAL/4;
//    EPwm2Regs.CMPA.half.CMPA = 0;

//    _MC_CLRDATA = 2; //����PI����
    MAIN_PARA.pulse_cnt1++;
//    START_TIME++;

    // GPIO0~7 MUX is changed only on PWM output state edges.
    if((_MC_RESUME == 1) && (errorcode == 0) && (pwm_output_state == 0))
    {
        EnableDabPwmOutputs();
        pwm_output_state = 1;
    }
    else if((_MC_RESUME == 0) && (pwm_output_state != 0))
    {
        DisableDabPwmOutputs();
        pwm_output_state = 0;
    }

    if(_MC_RESUME == 0)
    {
        errorcode = 0;
    }

    // Only schedule CAN work here; actual CAN processing runs in the main loop.
    epwm1_can_divider++;
    if(epwm1_can_divider >= EPWM_ISR_CAN_DIVIDER)
    {
        epwm1_can_divider = 0;
        can_receive_pending = 1;
    }

    if((_MC_RESUME == 1) && (errorcode == 0))
    {
        ApplyClaPwmCommands();
    }

    // Apply the latest completed CLA commands every PWM cycle, but run the full
    // CLA control calculation only every third cycle to keep Task2 schedulable.
    cla_control_divider++;
    if(cla_control_divider >= CLA_CONTROL_DIVIDER)
    {
        cla_control_divider = 0;
        if(Cla1Regs.MIRUN.bit.INT2 == 0)
        {
            Cla1ForceTask2();
            cla_task2_trigger_count++;
        }
        else
        {
            cla_task2_busy_count++;
        }
    }

//    DutyCtrl();

//   TEST();
//    PowerCtrl();    // ԭ����  ������20250705
//    Host_Pulse_on();// ԭ����  ������20250705
 //   Slave_Pulse_on();// ԭ����  ������20250705

    EPwm1Regs.ETCLR.bit.INT = 0x01;
    PieCtrlRegs.PIEACK.all = PIEACK_GROUP3;


}


/*===============================================================================*/
// no more
/*===============================================================================*/
/******************* (C) COPYRIGHT 2021  **************************END OF FILE****/
