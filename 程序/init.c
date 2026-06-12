/**********************************Copyright (c)**********************************/
/*                       BeiJing Jiaotong University    EE  DQL206LAB            */
/*-------------------------------File Information--------------------------------*/
/* File name:        init.c                                                      */
/* Author:           YZY                                                         */
/* Current Version:  V1.0                                                        */
/* Time:             2021-01-10                                                  */
/* Function:         LLC converter                                               */
/*********************************************************************************/

/***********************************Header File***********************************/
#include "header.h"      /* main header definitions and Declaration*/

/******************************Function Declaration*******************************/
struct CPUTIMER_VARS CpuTimer0;
struct CPUTIMER_VARS CpuTimer1;
struct CPUTIMER_VARS CpuTimer2;

/****************************Global Variable Definition***************************/
#pragma CODE_SECTION(InitFlash, "ramfuncs");

/************************************Function*************************************/
/*********************************************************************************/
/* Name:      DisableDog ()                                                      */
/* Author:    nchen                                                              */
/* Time:      20190101                                                           */
/* Parameters:none                                                               */
/* Returns:   none                                                               */
/* Description:                                                                  */
/*                                                                               */
/*********************************************************************************/
void DisableDog(void)
{
    EALLOW;
    SysCtrlRegs.WDKEY = 0x55;
    SysCtrlRegs.WDKEY = 0xAA;
    SysCtrlRegs.WDCR = 0x0068;
    EDIS;
}

/*********************************************************************************/
/* Name:      XtalOscSel()                                                       */
/* Author:    nchen                                                              */
/* Time:      20190101                                                           */
/* Parameters:none                                                               */
/* Returns:   none                                                               */
/* Description:                                                                  */
/*                                                                               */
/*********************************************************************************/
void XtalOscSel (void)
{
     EALLOW;
     SysCtrlRegs.XCLK.bit.XCLKINSEL = 1;        //GPIO19 is XCLKIN input source
     SysCtrlRegs.CLKCTL.bit.XTALOSCOFF = 1;     // 关�?? XTALOSC
     SysCtrlRegs.CLKCTL.bit.XCLKINOFF = 0;      // 打�?? XCLKIN
     SysCtrlRegs.CLKCTL.bit.OSCCLKSRC2SEL = 0;  // Switch to external clock
     SysCtrlRegs.CLKCTL.bit.OSCCLKSRCSEL = 1;   // Switch from INTOSC1 to INTOSC2/ext clk
     SysCtrlRegs.CLKCTL.bit.WDCLKSRCSEL = 0;    // Clock Watchdog off of INTOSC1
     SysCtrlRegs.CLKCTL.bit.INTOSC2OFF = 1;     // Turn off INTOSC2
     SysCtrlRegs.CLKCTL.bit.INTOSC1OFF = 0;     // Leave INTOSC1 on
     EDIS;
}

/*********************************************************************************/
/* Name:      InitPll()                                                          */
/* Author:    nchen                                                              */
/* Time:      20190101                                                           */
/* Parameters:none                                                               */
/* Returns:   none                                                               */
/* Description:60Mhz                                                             */
/*                                                                               */
/*********************************************************************************/
void InitPll(Uint16 val, Uint16 divsel)
{
   volatile Uint16 iVol;

   // Make sure the PLL is not running in limp mode
   //判断时钟�?否丢�?
   if (SysCtrlRegs.PLLSTS.bit.MCLKSTS != 0)
   {
      EALLOW;
      // OSCCLKSRC1 failure detected. PLL running in limp mode.
      // Re-enable missing clock logic.
      SysCtrlRegs.PLLSTS.bit.MCLKCLR = 1;
      EDIS;
      // Replace this line with a call to an appropriate
      // SystemShutdown(); function.
      asm("ESTOP0");     // Uncomment for debugging purposes
   }

   // DIVSEL MUST be 0 before PLLCR can be changed from
   // 0x0000. It is set to 0 by an external reset XRSn
   // This puts us in 1/4
   //PLLCR�?�?改之前DIVSEL必须设置�?0
   if (SysCtrlRegs.PLLSTS.bit.DIVSEL != 0)
   {
       EALLOW;
       SysCtrlRegs.PLLSTS.bit.DIVSEL = 0;
       EDIS;
   }

   // Change the PLLCR
   //�?改PLLCR
   if (SysCtrlRegs.PLLCR.bit.DIV != val)
   {

      EALLOW;
      // Before setting PLLCR turn off missing clock detect logic
      //设置PLLCR 之前关闭主时钟丢失�?��??
      SysCtrlRegs.PLLSTS.bit.MCLKOFF = 1;
      SysCtrlRegs.PLLCR.bit.DIV = val;
      EDIS;

      // Optional: Wait for PLL to lock.
      // During this time the CPU will switch to OSCCLK/2 until
      // the PLL is stable.  Once the PLL is stable the CPU will
      // switch to the new PLL value.
      //
      // This time-to-lock is monitored by a PLL lock counter.
      //
      // Code is not required to sit and wait for the PLL to lock.
      // However, if the code does anything that is timing critical,
      // and requires the correct clock be locked, then it is best to
      // wait until this switching has completed.

      // Wait for the PLL lock bit to be set.

      // The watchdog should be disabled before this loop, or fed within
      // the loop via ServiceDog().

      // Uncomment to disable the watchdog
      DisableDog();

      while(SysCtrlRegs.PLLSTS.bit.PLLLOCKS != 1) //当PLLCR�?改写的时??�，PLL会上锁�?�等待解锁完成�???
      {
          // Uncomment to service the watchdog
          // ServiceDog();
      }

      EALLOW;
      SysCtrlRegs.PLLSTS.bit.MCLKOFF = 0;// 打开主时钟丢失�?�测功�??
      EDIS;
    }

    // If switching to 1/2
    if((divsel == 1)||(divsel == 2))
    {
        EALLOW;
        SysCtrlRegs.PLLSTS.bit.DIVSEL = divsel;
        EDIS;
    }

    // If switching to 1/1
    // * First go to 1/2 and let the power settle
    //   The time required will depend on the system, this is only an example
    // * Then switch to 1/1
    if(divsel == 3)
    {
        EALLOW;
        SysCtrlRegs.PLLSTS.bit.DIVSEL = 2;
        DELAY_US(50L);
        SysCtrlRegs.PLLSTS.bit.DIVSEL = 3;
        EDIS;
    }
}

/*********************************************************************************/
/* Name:      InitPeripheralClocks()                                             */
/* Author:    nchen                                                              */
/* Time:      20190101                                                           */
/* Parameters:none                                                               */
/* Returns:   none                                                               */
/* Description:                                                                  */
/*                                                                               */
/*********************************************************************************/
void InitPeripheralClocks(void)
{
   EALLOW;

// LOSPCP prescale register settings, normally it will be set to default values

   SysCtrlRegs.LOSPCP.all = 0x0002;//LSPCLK=SYSCLKOUT/4=12M

// XCLKOUT to SYSCLKOUT ratio.  By default XCLKOUT = 1/4 SYSCLKOUT
   SysCtrlRegs.XCLK.bit.XCLKOUTDIV=2;//XCLKOUT=SYSCLKOUT=60M

// Peripheral clock enables set for the selected peripherals.
// If you are not using a peripheral leave the clock off
// to save on power.
//
// Note: not all peripherals are available on all 2803x derivates.
// Refer to the datasheet for your particular device.
//
// This function is not written to be an example of efficient code.

   SysCtrlRegs.PCLKCR0.bit.ADCENCLK = 1;      // ADC
//   SysCtrlRegs.PCLKCR3.bit.COMP1ENCLK = 1;    // COMP1
//   SysCtrlRegs.PCLKCR3.bit.COMP2ENCLK = 1;    // COMP2
//   SysCtrlRegs.PCLKCR3.bit.COMP3ENCLK = 1;    // COMP3
//   SysCtrlRegs.PCLKCR1.bit.ECAP1ENCLK = 1;    // eCAP1
   SysCtrlRegs.PCLKCR0.bit.ECANAENCLK=1;      // eCAN-A
//   SysCtrlRegs.PCLKCR1.bit.EQEP1ENCLK = 0;    // eQEP1
   SysCtrlRegs.PCLKCR1.bit.EPWM1ENCLK = 1;    // ePWM1
   SysCtrlRegs.PCLKCR1.bit.EPWM2ENCLK = 1;    // ePWM2
   SysCtrlRegs.PCLKCR1.bit.EPWM3ENCLK = 1;    // ePWM3
   SysCtrlRegs.PCLKCR1.bit.EPWM4ENCLK = 1;    // ePWM4
   SysCtrlRegs.PCLKCR1.bit.EPWM5ENCLK = 1;    // ePWM5
   SysCtrlRegs.PCLKCR1.bit.EPWM6ENCLK = 1;    // ePWM6
   SysCtrlRegs.PCLKCR1.bit.EPWM7ENCLK = 1;    // ePWM7
//   SysCtrlRegs.PCLKCR0.bit.HRPWMENCLK = 1;    // HRPWM
//   SysCtrlRegs.PCLKCR0.bit.I2CAENCLK = 0;     // I2C
//   SysCtrlRegs.PCLKCR0.bit.LINAENCLK = 0;     // LIN-A
   SysCtrlRegs.PCLKCR3.bit.CLA1ENCLK = 1;     // CLA1
   SysCtrlRegs.PCLKCR0.bit.SCIAENCLK = 1;     // SCI-A
//   SysCtrlRegs.PCLKCR0.bit.SPIAENCLK = 1;     // SPI-A
//   SysCtrlRegs.PCLKCR0.bit.SPIBENCLK = 0;     // SPI-B
   SysCtrlRegs.PCLKCR2.bit.HRCAP1ENCLK = 1;
//   SysCtrlRegs.PCLKCR2.bit.HRCAP2ENCLK = 1;
   SysCtrlRegs.PCLKCR3.bit.CPUTIMER0ENCLK= 1;

   SysCtrlRegs.PCLKCR0.bit.TBCLKSYNC = 1;     // Enable TBCLK within the ePWM

   EDIS;
}

/*********************************************************************************/
/* Name:      InitSysCtrl()                                                      */
/* Author:    nchen                                                              */
/* Time:      20190101                                                           */
/* Parameters:none                                                               */
/* Returns:   none                                                               */
/* Description:                                                                  */
/*                                                                               */
/*********************************************************************************/
void InitSysCtrl(void)
{
   PartIdRegs.PARTID.bit.PARTNO = 0x00BB; // for  TMS320F28034PN

   // Disable the watchdog
   DisableDog();

   // *IMPORTANT*
   // The Device_cal function, which copies the ADC & oscillator calibration values
   // from TI reserved OTP into the appropriate trim registers, occurs automatically
   // in the Boot ROM. If the boot ROM code is bypassed during the debug process, the
   // following function MUST be called for the ADC and oscillators to function according
   // to specification. The clocks to the ADC MUST be enabled before calling this
   // function.
   // See the device data manual and/or the ADC Reference
   // Manual for more information.

   EALLOW;
   SysCtrlRegs.PCLKCR0.bit.ADCENCLK = 1; // Enable ADC peripheral clock
   (*Device_cal)();
   SysCtrlRegs.PCLKCR0.bit.ADCENCLK = 0; // Return ADC clock to original state
   EDIS;

   // Select Internal Oscillator 1 as Clock Source (default), and turn off all unused clocks to
   // conserve power.
   XtalOscSel();

   // Initialize the PLL control: PLLCR and CLKINDIV
   // DSP28_PLLCR and DSP28_CLKINDIV are defined in DSP2803x_Examples.h
   InitPll(DSP28_PLLCR,DSP28_DIVSEL);//OSCCLK=8M,SYSCLKOUT=CLKIN=OSCCLK*12/2=48M
   // Initialize the peripheral clocks
   InitPeripheralClocks();
}

/*********************************************************************************/
/* Name:      InitGpio()                                                         */
/* Author:    nchen                                                              */
/* Time:      20190101                                                           */
/* Parameters:none                                                               */
/* Returns:   none                                                               */
/* Description:                                                                  */
/*                                                                               */
/*********************************************************************************/
void InitGpio(void)
{
     EALLOW;
//==============================================================================
     //Step 1. Plan the device pin-out
     //GPIO0引脚（PWM1）：output；�?��??上拉；EPWM1A�?
     //GPIO1引脚（PWM2）：output；�?��??上拉；EPWM1B�?
     //GPIO2引脚（PWM3）：output；�?��??上拉；EPWM2A�?
     //GPIO3引脚（PWM4）：output；�?��??上拉；EPWM2B�?
     //GPIO4引脚（PWM5）：output；�?��??上拉；EPWM3A�?
     //GPIO5引脚（PWM6）：output；�?��??上拉；EPWM3B�?
     //GPIO6引脚（PWM7）：output；�?��??上拉；EPWM4A�?
     //GPIO7引脚（PWM8）：output；�?��??上拉；EPWM4B�?
     //GPIO8引脚（PWM9）：output；�?��??上拉；EPWM5A�?
     //GPIO9引脚（PWM10）：output；�?��??上拉；EPWM5B�?
     //GPIO10引脚（PWM11）：output；�?��??上拉；EPWM6A�?
     //GPIO11引脚（PWM12）：output；�?��??上拉；EPWM6B�?
     //GPIO12引脚（电池电流保护）：input；上拉；TZ1�?
     //GPIO16引脚（谐�?电压保护）：input；上拉；TZ2�?
     //GPIO17引脚（偏磁保护）：input；上拉；TZ3�?
     //GPIO20引脚（PHASEB）：output；�?��??上拉；GPIO20�?
     //GPIO21引脚（PHASEA）：output；�?��??上拉；GPIO21�?
     //GPIO25引脚（GPIO25）：output；�?��??上拉；GPIO25�?
     //GPIO26引脚（GPIO26）：output；�?��??上拉；GPIO26�?
     //GPIO39引脚（GPIO39）：output；�?��??上拉；GPIO39�?
     //GPIO13引脚（SPISOMIB）：output；上拉；SPISOMIB；�??
     //GPIO14引脚（SPICLKB）：output；上拉；SPICLKB；�??
     //GPIO15引脚（SPISTEB）：output；上拉；SPISTEB；�??
     //GPIO24引脚（SPISMOB）：output；上拉；SPISTEB；�??
     //GPIO22引脚�??485EN）：output；�?��??上拉；GPIO22�?
     //GPIO23引脚（WP）：output；�?��??上拉；GPIO23�?
     //GPIO32引脚（SDA）：output（可设置input)；上拉；GPIO32�?
     //GPIO33引脚（SCL）：output；上拉；GPIO33�?
     //GPIO28引脚（SCIRXDA）：input；上拉；SCIRXDA�?
     //GPIO29引脚（SCITXDA）：output;上拉；SCITXDA�?
     //GPIO30引脚（CANRXA）：input；上拉；CANRXA�?
     //GPIO31引脚（CANTXA）：output；上拉；CANTXA�?

//-------------------PWM-------------------------------------
     GpioCtrlRegs.GPADIR.bit.GPIO0 = 1;    // output
     GpioCtrlRegs.GPAMUX1.bit.GPIO0 = 1;   // EPWM
     GpioCtrlRegs.GPAPUD.bit.GPIO0 = 1;    // GPIO0作为output，�?��??上�??

     GpioCtrlRegs.GPADIR.bit.GPIO1 = 1;    // output
     GpioCtrlRegs.GPAMUX1.bit.GPIO1 = 1;   // EPWM
     GpioCtrlRegs.GPAPUD.bit.GPIO1 = 1;    // GPIO1作为output，�?��??上�??

     GpioCtrlRegs.GPADIR.bit.GPIO2 = 1;    // output
     GpioCtrlRegs.GPAMUX1.bit.GPIO2 = 1;   // EPWM
     GpioCtrlRegs.GPAPUD.bit.GPIO2 = 1;    // GPIO2作为output，�?��??上�??

     GpioCtrlRegs.GPADIR.bit.GPIO3 = 1;    // output
     GpioCtrlRegs.GPAMUX1.bit.GPIO3 = 1;   // EPWM
     GpioCtrlRegs.GPAPUD.bit.GPIO3 = 1;    // GPIO3作为output，�?��??上�??

     GpioCtrlRegs.GPADIR.bit.GPIO4 = 1;    // output
     GpioCtrlRegs.GPAMUX1.bit.GPIO4 = 1;   // EPWM
     GpioCtrlRegs.GPAPUD.bit.GPIO4 = 1;    // GPIO4作为output，�?��??上�??
//     GpioCtrlRegs.GPADIR.bit.GPIO4 = 1;    // 1 = 输出模式（这行你原本是对的）
//     GpioCtrlRegs.GPAMUX1.bit.GPIO4 = 0;   // 0 = 普通GPIO功能（关键修改：原1是EPWM复用，改为0）
//     GpioCtrlRegs.GPAPUD.bit.GPIO4 = 0;    // 0 = 使能上拉（输出模式建议使能上拉，更稳定）
//     GpioDataRegs.GPACLEAR.bit.GPIO4 = 1;  // 强制将GPIO6输出低电平（CLEAR寄存器写1则对应引脚置0）

     GpioCtrlRegs.GPADIR.bit.GPIO5 = 1;    // output
     GpioCtrlRegs.GPAMUX1.bit.GPIO5 = 1;   // EPWM
     GpioCtrlRegs.GPAPUD.bit.GPIO5 = 1;    // GPIO5作为output
//     GpioCtrlRegs.GPADIR.bit.GPIO5 = 1;    // 1 = 输出模式（这行你原本是对的）
//     GpioCtrlRegs.GPAMUX1.bit.GPIO5 = 0;   // 0 = 普通GPIO功能（关键修改：原1是EPWM复用，改为0）
//     GpioCtrlRegs.GPAPUD.bit.GPIO5 = 0;    // 0 = 使能上拉（输出模式建议使能上拉，更稳定）
//     GpioDataRegs.GPACLEAR.bit.GPIO5 = 1;  // 强制将GPIO6输出低电平（CLEAR寄存器写1则对应引脚置0）

     GpioCtrlRegs.GPADIR.bit.GPIO6 = 1;    // output
     GpioCtrlRegs.GPAMUX1.bit.GPIO6 = 1;   // EPWM
     GpioCtrlRegs.GPAPUD.bit.GPIO6 = 1;    // GPIO6作为output
//     GpioCtrlRegs.GPADIR.bit.GPIO6 = 1;    // 1 = 输出模式（这行你原本是对的）
//     GpioCtrlRegs.GPAMUX1.bit.GPIO6 = 0;   // 0 = 普通GPIO功能（关键修改：原1是EPWM复用，改为0）
//     GpioCtrlRegs.GPAPUD.bit.GPIO6 = 0;    // 0 = 使能上拉（输出模式建议使能上拉，更稳定）
//     GpioDataRegs.GPACLEAR.bit.GPIO6 = 1;  // 强制将GPIO6输出低电平（CLEAR寄存器写1则对应引脚置0）

     GpioCtrlRegs.GPADIR.bit.GPIO7 = 1;    // output
     GpioCtrlRegs.GPAMUX1.bit.GPIO7 = 1;   // EPWM
     GpioCtrlRegs.GPAPUD.bit.GPIO7 = 1;    // GPIO7作为output，�?��??上�??
//     GpioCtrlRegs.GPADIR.bit.GPIO7 = 1;    // 1 = 输出模式（这行你原本是对的）
//     GpioCtrlRegs.GPAMUX1.bit.GPIO7 = 0;   // 0 = 普通GPIO功能（关键修改：原1是EPWM复用，改为0）
//     GpioCtrlRegs.GPAPUD.bit.GPIO7 = 0;    // 0 = 使能上拉（输出模式建议使能上拉，更稳定）
//     GpioDataRegs.GPACLEAR.bit.GPIO7 = 1;  // 强制将GPIO6输出低电平（CLEAR寄存器写1则对应引脚置0）


//     GpioCtrlRegs.GPADIR.bit.GPIO8 = 1;    // output
//     GpioCtrlRegs.GPAMUX1.bit.GPIO8 = 1;   // EPWM
//     GpioCtrlRegs.GPAPUD.bit.GPIO8 = 1;    // GPIO8作为output，�?��??上�??
//
//     GpioCtrlRegs.GPADIR.bit.GPIO9 = 1;    // output
//     GpioCtrlRegs.GPAMUX1.bit.GPIO9 = 1;   // EPWM
//     GpioCtrlRegs.GPAPUD.bit.GPIO9 = 1;    // GPIO9作为output，�?��??上�??
//
//     GpioCtrlRegs.GPADIR.bit.GPIO10 = 1;    // output
//     GpioCtrlRegs.GPAMUX1.bit.GPIO10 = 1;   // EPWM
//     GpioCtrlRegs.GPAPUD.bit.GPIO10 = 1;    // GPIO10作为output，�?��??上�??
//
//     GpioCtrlRegs.GPADIR.bit.GPIO11 = 1;    // output
//     GpioCtrlRegs.GPAMUX1.bit.GPIO11 = 1;   // EPWM
//     GpioCtrlRegs.GPAPUD.bit.GPIO11 = 1;    // GPIO11作为output，�?��??上�??

//----------------------------保�??-------------------------------
     GpioCtrlRegs.GPADIR.bit.GPIO12 = 0;    // input
     GpioCtrlRegs.GPAMUX1.bit.GPIO12 = 1;   // TZ1
     GpioCtrlRegs.GPAPUD.bit.GPIO12 = 0;    // GPIO11作为input，上�??

     GpioCtrlRegs.GPADIR.bit.GPIO16 = 0;    // input
     GpioCtrlRegs.GPAMUX2.bit.GPIO16 = 1;   // TZ2
     GpioCtrlRegs.GPAPUD.bit.GPIO16 = 0;    // GPIO16作为input，上�??

     GpioCtrlRegs.GPADIR.bit.GPIO17 = 0;    // input
     GpioCtrlRegs.GPAMUX2.bit.GPIO17 = 1;   // TZ2
     GpioCtrlRegs.GPAPUD.bit.GPIO17 = 0;    // GPIO16作为input，上�??
//---------------------------------------------------------------
     GpioCtrlRegs.GPADIR.bit.GPIO20 = 1;    // output
     GpioCtrlRegs.GPAMUX2.bit.GPIO20 = 0;   // GPIO
     GpioCtrlRegs.GPAPUD.bit.GPIO20 = 1;    // GPIO20作为output，�?��??上�??

     GpioCtrlRegs.GPADIR.bit.GPIO21 = 1;    // output
     GpioCtrlRegs.GPAMUX2.bit.GPIO21 = 0;   // GPIO
     GpioCtrlRegs.GPAPUD.bit.GPIO21 = 1;    // GPIO21作为output，�?��??上�??

//     GpioCtrlRegs.GPADIR.bit.GPIO25 = 1;    // output    H桥输出主继电�?
//     GpioCtrlRegs.GPAMUX2.bit.GPIO25 = 0;   // GPIO
////     GpioCtrlRegs.GPAPUD.bit.GPIO25 = 1;    // GPIO25作为output，�?��??上�??
//
//     GpioCtrlRegs.GPADIR.bit.GPIO26 = 1;    // output
//     GpioCtrlRegs.GPAMUX2.bit.GPIO26 = 0;   // GPIO
//     GpioCtrlRegs.GPAPUD.bit.GPIO26 = 1;    // GPIO26作为output，�?��??上�??

//     GpioCtrlRegs.GPBDIR.bit.GPIO39 = 1;    // output                    //****************************************************88
//     GpioCtrlRegs.GPBMUX1.bit.GPIO39 = 0;   // GPIO
////     GpioCtrlRegs.GPBPUD.bit.GPIO39 = 1;    // GPIO39作为output，�?��??上�??
//---------------------------SPI------------------------------------


     GpioCtrlRegs.GPBDIR.bit.GPIO43 = 1;     //RL2  输入预充电继电器
     GpioCtrlRegs.GPBMUX1.bit.GPIO43 = 0;
     GpioCtrlRegs.GPBDIR.bit.GPIO42 = 1;     //RL1  输入主继电�??
     GpioCtrlRegs.GPBMUX1.bit.GPIO42 = 0;
     GpioCtrlRegs.GPBDIR.bit.GPIO39 = 1;     //RL3  旁路继电�??
     GpioCtrlRegs.GPBMUX1.bit.GPIO39 = 0;
     GpioCtrlRegs.GPADIR.bit.GPIO25 = 1;     //RL4  输出主继电�??
     GpioCtrlRegs.GPAMUX2.bit.GPIO25 = 0;
     GpioCtrlRegs.GPADIR.bit.GPIO18 = 1;     //RL5  输出预充电继电器
     GpioCtrlRegs.GPAMUX2.bit.GPIO18 = 0;
     GpioCtrlRegs.GPBDIR.bit.GPIO40 = 1;     //�?


//---------------------------SCI------------------------------------
     GpioCtrlRegs.GPADIR.bit.GPIO22 = 1;     // output
     GpioCtrlRegs.GPAMUX2.bit.GPIO22 = 0;    // GPIO
     GpioCtrlRegs.GPAPUD.bit.GPIO22 = 1;     // GPIO22作为output，�?��??上�??//485EN(旧版)

//     GpioCtrlRegs.GPADIR.bit.GPIO13 = 1;     // output
//     GpioCtrlRegs.GPAMUX1.bit.GPIO13 = 0;    // GPIO
//     GpioCtrlRegs.GPAPUD.bit.GPIO13 = 1;     // GPIO22作为output，�?��??上�??//485EN1

     GpioCtrlRegs.GPADIR.bit.GPIO23 = 1;     // output
     GpioCtrlRegs.GPAMUX2.bit.GPIO23 = 0;    // GPIO
     GpioCtrlRegs.GPAPUD.bit.GPIO23 = 1;     // GPIO23作为output，�?��??上�??//WP

     GpioCtrlRegs.GPBDIR.bit.GPIO32 = 1;     // output
     GpioCtrlRegs.GPBMUX1.bit.GPIO32 = 0;    // GPIO
     GpioCtrlRegs.GPBPUD.bit.GPIO32 = 1;     // GPIO32作为output，�?��??上�??//SDA

     GpioCtrlRegs.GPBMUX1.bit.GPIO33 = 1;    // SCL
     GpioCtrlRegs.GPBPUD.bit.GPIO33 = 0;     // GPIO33作为output，上�??//SCL

     GpioCtrlRegs.GPBMUX1.bit.GPIO32 = 1;    // SDA
     GpioCtrlRegs.GPBPUD.bit.GPIO32 = 0;     // GPIO32作为output，上�??//SDA

     GpioCtrlRegs.GPAMUX2.bit.GPIO28 = 1;    // SCIRXDA
     GpioCtrlRegs.GPAPUD.bit.GPIO28 = 0;     // 上�??

//     GpioCtrlRegs.GPAMUX1.bit.GPIO15 = 1;    // SCIRXDA
//     GpioCtrlRegs.GPAPUD.bit.GPIO15 = 0;     // 上�??

     GpioCtrlRegs.GPAMUX2.bit.GPIO29 = 1;    // SCITXDA
     GpioCtrlRegs.GPAPUD.bit.GPIO29 = 0;     // 上�??

//     GpioCtrlRegs.GPAMUX1.bit.GPIO14 = 1;    // SCITXDA
//     GpioCtrlRegs.GPAPUD.bit.GPIO14 = 0;     // 上�??
//---------------------------CAN------------------------------------
     GpioCtrlRegs.GPAMUX2.bit.GPIO30 = 1;    // CANRXA
     GpioCtrlRegs.GPAPUD.bit.GPIO30 = 0;     // 上�??

     GpioCtrlRegs.GPAMUX2.bit.GPIO31 = 1;    // CANTXA
     GpioCtrlRegs.GPAPUD.bit.GPIO31 = 0;     // 上�??
//------------------------------------------------------------------
//Step 3. Select input qualification  TZ
     GpioCtrlRegs.GPAQSEL1.bit.GPIO12 = 3;  // 6 sample
     GpioCtrlRegs.GPAQSEL2.bit.GPIO16 = 3;  // 6 sample
     GpioCtrlRegs.GPAQSEL2.bit.GPIO17 = 3;  // 6 sample
     GpioCtrlRegs.GPACTRL.bit.QUALPRD1 = 12;//=12*5*2*(1/SYSCLKOUT)=2us//GPIO8~15
     GpioCtrlRegs.GPACTRL.bit.QUALPRD2 = 12;//16~23
     GpioCtrlRegs.GPACTRL.bit.QUALPRD3 = 12;//24~31


     GpioCtrlRegs.GPAQSEL2.bit.GPIO28 = 3;  // asynch input//SCI
     GpioCtrlRegs.GPAQSEL2.bit.GPIO29 = 3;  // asynch input

//     GpioCtrlRegs.GPAQSEL1.bit.GPIO15 = 3;  // asynch input//SCI
//     GpioCtrlRegs.GPAQSEL1.bit.GPIO14 = 3;  // asynch input

     GpioCtrlRegs.GPAQSEL2.bit.GPIO30 = 3;  // asynch input//CAN
     GpioCtrlRegs.GPAQSEL2.bit.GPIO31 = 3;  // asynch input


//Step 4. Select the pin function
//     GpioCtrlRegs.GPAMUX1.all = 0x40500555; //EPWM1A~3B,6A~6B,TZ1~TZ3
//     GpioCtrlRegs.GPAMUX2.all = 0x05000030; //SCIA,XLKOUT

//Step 5. For digital general purpose I/O, select the direction of the pin
//     GpioDataRegs.GPACLEAR.bit.GPIO6 = 1;   // Load output latch//LED2
//     GpioDataRegs.GPACLEAR.bit.GPIO7 = 1;   // Load output latch//LED1

//     GpioDataRegs.GPACLEAR.bit.GPIO10 = 1;   // Load output latch//jidianqi

     GpioDataRegs.GPBCLEAR.bit.GPIO41 = 1;   // Load output latch//LED_Uin
     GpioDataRegs.GPACLEAR.bit.GPIO12 = 1;  // Load output latch//LED_Iin
     GpioDataRegs.GPACLEAR.bit.GPIO16 = 1;  // Load output latch//LED_IL
     GpioDataRegs.GPBCLEAR.bit.GPIO44 = 1;   // Load output latch//LED_Uo
//     GpioDataRegs.GPACLEAR.bit.GPIO25 = 1;  // Load output latch//LED_Io  //***************************************
//     GpioDataRegs.GPACLEAR.bit.GPIO26 = 1;  // Load output latch//485EN

//     GpioCtrlRegs.GPADIR.bit.GPIO6 = 1;     //  output
//     GpioCtrlRegs.GPADIR.bit.GPIO7 = 1;     //  output
//     GpioCtrlRegs.GPADIR.bit.GPIO10 = 1;     //  output
     GpioCtrlRegs.GPBDIR.bit.GPIO41 = 1;    //  output
     GpioCtrlRegs.GPADIR.bit.GPIO12 = 1;    //  output
     GpioCtrlRegs.GPADIR.bit.GPIO16 = 1;    //  output
     GpioCtrlRegs.GPBDIR.bit.GPIO44 = 1;    //  output
     GpioCtrlRegs.GPADIR.bit.GPIO25 = 1;    //  output
     GpioCtrlRegs.GPADIR.bit.GPIO26 = 1;    //  output

//     GpioCtrlRegs.GPAMUX1.bit.GPIO6 = 0;
//     GpioCtrlRegs.GPAMUX1.bit.GPIO7 = 0;
//     GpioCtrlRegs.GPAMUX1.bit.GPIO10 = 0;
     GpioCtrlRegs.GPBMUX1.bit.GPIO41 = 0;
     GpioCtrlRegs.GPAMUX1.bit.GPIO12 = 0;
     GpioCtrlRegs.GPAMUX2.bit.GPIO16 = 0;
     GpioCtrlRegs.GPBMUX1.bit.GPIO44 = 0;
     GpioCtrlRegs.GPAMUX2.bit.GPIO25 = 0;

//     GpioCtrlRegs.AIOMUX1.bit.AIO2 = 2;    // Configure AIO2 for A2 (analog input) operation
//     GpioCtrlRegs.AIOMUX1.bit.AIO4 = 2;    // Configure AIO4 for A4 (analog input) operation
//     GpioCtrlRegs.AIOMUX1.bit.AIO6 = 2;    // Configure AIO6 for A6 (analog input) operation
//     GpioCtrlRegs.AIOMUX1.bit.AIO10 = 2;   // Configure AIO10 for B2 (analog input) operation
//     GpioCtrlRegs.AIOMUX1.bit.AIO12 = 2;   // Configure AIO12 for B4 (analog input) operation
//     GpioCtrlRegs.AIOMUX1.bit.AIO14 = 2;   // Configure AIO14 for B6 (analog input) operation

     GpioCtrlRegs.GPAMUX2.bit.GPIO26 = 0;
     GpioCtrlRegs.GPADIR.bit.GPIO26  = 1;

     //test cputimer
//     GpioCtrlRegs.GPAMUX2.bit.GPIO19 = 0;
//     GpioCtrlRegs.GPADIR.bit.GPIO19 = 1;

     GpioCtrlRegs.GPAMUX2.bit.GPIO18 = 0;
     GpioCtrlRegs.GPADIR.bit.GPIO18 = 1;

     //keyS100
     GpioCtrlRegs.GPAMUX2.bit.GPIO27 = 0;
     GpioCtrlRegs.GPADIR.bit.GPIO27  = 0;
     GpioCtrlRegs.GPAMUX2.bit.GPIO21 = 0;
     GpioCtrlRegs.GPAMUX2.bit.GPIO20 = 0;

     EDIS;
}

/*********************************************************************************/
/* Name:      InitPieCtrl()                                                      */
/* Author:    nchen                                                              */
/* Time:      20190101                                                           */
/* Parameters:none                                                               */
/* Returns:   none                                                               */
/* Description:                                                                  */
/*                                                                               */
/*********************************************************************************/
void InitPieCtrl(void)
{
    // Disable PIE:
    PieCtrlRegs.PIECTRL.bit.ENPIE = 0;

    // Clear all PIEIER registers:
    PieCtrlRegs.PIEIER1.all = 0;
    PieCtrlRegs.PIEIER2.all = 0;
    PieCtrlRegs.PIEIER3.all = 0;
    PieCtrlRegs.PIEIER4.all = 0;
    PieCtrlRegs.PIEIER5.all = 0;
    PieCtrlRegs.PIEIER6.all = 0;
    PieCtrlRegs.PIEIER7.all = 0;
    PieCtrlRegs.PIEIER8.all = 0;
    PieCtrlRegs.PIEIER9.all = 0;
    PieCtrlRegs.PIEIER10.all = 0;
    PieCtrlRegs.PIEIER11.all = 0;
    PieCtrlRegs.PIEIER12.all = 0;

    // Clear all PIEIFR registers:
    PieCtrlRegs.PIEIFR1.all = 0;
    PieCtrlRegs.PIEIFR2.all = 0;
    PieCtrlRegs.PIEIFR3.all = 0;
    PieCtrlRegs.PIEIFR4.all = 0;
    PieCtrlRegs.PIEIFR5.all = 0;
    PieCtrlRegs.PIEIFR6.all = 0;
    PieCtrlRegs.PIEIFR7.all = 0;
    PieCtrlRegs.PIEIFR8.all = 0;
    PieCtrlRegs.PIEIFR9.all = 0;
    PieCtrlRegs.PIEIFR10.all = 0;
    PieCtrlRegs.PIEIFR11.all = 0;
    PieCtrlRegs.PIEIFR12.all = 0;

    // Enable PIE:
    PieCtrlRegs.PIECTRL.bit.ENPIE = 1;
    PieCtrlRegs.PIEACK.all = 0xFFFF;
}

/*********************************************************************************/
/* Name:      PieVectTableInit()                                                 */
/* Author:    nchen                                                              */
/* Time:      20190101                                                           */
/* Parameters:none                                                               */
/* Returns:   none                                                               */
/* Description:                                                                  */
/*                                                                               */
/*********************************************************************************/
const struct PIE_VECT_TABLE PieVectTableInit = {

      PIE_RESERVED,  // 0  Reserved space
      PIE_RESERVED,  // 1  Reserved space
      PIE_RESERVED,  // 2  Reserved space
      PIE_RESERVED,  // 3  Reserved space
      PIE_RESERVED,  // 4  Reserved space
      PIE_RESERVED,  // 5  Reserved space
      PIE_RESERVED,  // 6  Reserved space
      PIE_RESERVED,  // 7  Reserved space
      PIE_RESERVED,  // 8  Reserved space
      PIE_RESERVED,  // 9  Reserved space
      PIE_RESERVED,  // 10 Reserved space
      PIE_RESERVED,  // 11 Reserved space
      PIE_RESERVED,  // 12 Reserved space

// Non-Peripheral Interrupts
      INT13_ISR,     // CPU-Timer 1
      INT14_ISR,     // CPU-Timer2
      DATALOG_ISR,   // Datalogging interrupt
      RTOSINT_ISR,   // RTOS interrupt
      EMUINT_ISR,    // Emulation interrupt
      NMI_ISR,       // Non-maskable interrupt
      ILLEGAL_ISR,   // Illegal operation TRAP
      USER1_ISR,     // User Defined trap 1
      USER2_ISR,     // User Defined trap 2
      USER3_ISR,     // User Defined trap 3
      USER4_ISR,     // User Defined trap 4
      USER5_ISR,     // User Defined trap 5
      USER6_ISR,     // User Defined trap 6
      USER7_ISR,     // User Defined trap 7
      USER8_ISR,     // User Defined trap 8
      USER9_ISR,     // User Defined trap 9
      USER10_ISR,    // User Defined trap 10
      USER11_ISR,    // User Defined trap 11
      USER12_ISR,    // User Defined trap 12

// Group 1 PIE Vectors
      ADCINT1_ISR,     // 1.1 ADC  // if this is rsvd_ISR, then INT10.1 should be defined as ADCINT1_ISR
      ADCINT2_ISR,     // 1.2 ADC  // if this is rsvd_ISR, then INT10.2 should be defined as ADCINT2_ISR
      rsvd_ISR,        // 1.3
      XINT1_ISR,       // 1.4 External Interrupt
      XINT2_ISR,       // 1.5 External Interrupt
      ADCINT9_ISR,     // 1.6 ADC
      TINT0_ISR,       // 1.7 Timer 0
      WAKEINT_ISR,     // 1.8 WD, Low Power

// Group 2 PIE Vectors
      EPWM1_TZINT_ISR, // 2.1 EPWM-1 Trip Zone
      EPWM2_TZINT_ISR, // 2.2 EPWM-2 Trip Zone
      EPWM3_TZINT_ISR, // 2.3 EPWM-3 Trip Zone
      EPWM4_TZINT_ISR, // 2.4 EPWM-4 Trip Zone
      EPWM5_TZINT_ISR, // 2.4 EPWM-4 Trip Zone
      EPWM6_TZINT_ISR, // 2.4 EPWM-4 Trip Zone
      EPWM7_TZINT_ISR, // 2.4 EPWM-4 Trip Zone
      rsvd_ISR,        // 2.8

// Group 3 PIE Vectors
      EPWM1_INT_ISR,   // 3.1 EPWM-1 Interrupt
      EPWM2_INT_ISR,   // 3.2 EPWM-2 Interrupt
      EPWM3_INT_ISR,   // 3.3 EPWM-3 Interrupt
      EPWM4_INT_ISR,   // 3.4 EPWM-4 Interrupt
      EPWM5_INT_ISR,   // 3.5 EPWM-5 Interrupt
      EPWM6_INT_ISR,   // 3.6 EPWM-6 Interrupt
      EPWM7_INT_ISR,   // 3.7 EPWM-7 Interrupt
      rsvd_ISR,        // 3.8

// Group 4 PIE Vectors
      ECAP1_INT_ISR,   // 4.1 ECAP-1
      rsvd_ISR,        // 4.2
      rsvd_ISR,        // 4.3
      rsvd_ISR,        // 4.4
      rsvd_ISR,        // 4.5
      rsvd_ISR,        // 4.6
      rsvd_ISR,        // 4.7
      rsvd_ISR,        // 4.8

// Group 5 PIE Vectors

      EQEP1_INT_ISR,   // 5.1 EQEP-1
      rsvd_ISR,        // 5.2
      rsvd_ISR,        // 5.3
      rsvd_ISR,        // 5.4
      rsvd_ISR,        // 5.5
      rsvd_ISR,        // 5.6
      rsvd_ISR,        // 5.7
      rsvd_ISR,        // 5.8

// Group 6 PIE Vectors
      SPIRXINTA_ISR,   // 6.1 SPI-A
      SPITXINTA_ISR,   // 6.2 SPI-A
      SPIRXINTB_ISR,   // 6.3 SPI-B
      SPITXINTB_ISR,   // 6.4 SPI-B
      rsvd_ISR,        // 6.5
      rsvd_ISR,        // 6.6
      rsvd_ISR,        // 6.7
      rsvd_ISR,        // 6.8

// Group 7 PIE Vectors
      rsvd_ISR,        // 7.1
      rsvd_ISR,        // 7.2
      rsvd_ISR,        // 7.3
      rsvd_ISR,        // 7.4
      rsvd_ISR,        // 7.5
      rsvd_ISR,        // 7.6
      rsvd_ISR,        // 7.7
      rsvd_ISR,        // 7.8

// Group 8 PIE Vectors
      I2CINT1A_ISR,    // 8.1 I2C
      I2CINT2A_ISR,    // 8.2 I2C
      rsvd_ISR,        // 8.3
      rsvd_ISR,        // 8.4
      rsvd_ISR,        // 8.5
      rsvd_ISR,        // 8.6
      rsvd_ISR,        // 8.7
      rsvd_ISR,        // 8.8

// Group 9 PIE Vectors
      SCIRXINTA_ISR,   // 9.1 SCI-A
      SCITXINTA_ISR,   // 9.2 SCI-A
      LIN0INTA_ISR,    // 9.3 LIN-A
      LIN1INTA_ISR,    // 9.4 LIN-A
      ECAN0INTA_ISR,   // 9.5 eCAN-A
      ECAN1INTA_ISR,   // 9.6 eCAN-A
      rsvd_ISR,        // 9.7
      rsvd_ISR,        // 9.8

// Group 10 PIE Vectors
      rsvd_ISR,        // 10.1 If this is ADCINT1_ISR, then INT1.1 should be defined as rsvd_ISR
      rsvd_ISR,        // 10.2 If this is ADCINT2_ISR, then INT1.2 should be defined as rsvd_ISR
      ADCINT3_ISR,     // 10.3 ADC
      ADCINT4_ISR,     // 10.4 ADC
      ADCINT5_ISR,     // 10.5 ADC
      ADCINT6_ISR,     // 10.6 ADC
      ADCINT7_ISR,     // 10.7 ADC
      ADCINT8_ISR,     // 10.8 ADC

// Group 11 PIE Vectors
      CLA1_INT1_ISR,   // 11.1 CLA1
      CLA1_INT2_ISR,   // 11.2 CLA1
      CLA1_INT3_ISR,   // 11.3 CLA1
      CLA1_INT4_ISR,   // 11.4 CLA1
      CLA1_INT5_ISR,   // 11.5 CLA1
      CLA1_INT6_ISR,   // 11.6 CLA1
      CLA1_INT7_ISR,   // 11.7 CLA1
      CLA1_INT8_ISR,   // 11.8 CLA1

// Group 12 PIE Vectors
      XINT3_ISR,       // 12.1 External Interrupt
      rsvd_ISR,        // 12.2
      rsvd_ISR,        // 12.3
      rsvd_ISR,        // 12.4
      rsvd_ISR,        // 12.5
      rsvd_ISR,        // 12.6
      LVF_ISR,         // 12.7 CLA1
      LUF_ISR          // 12.8 CLA1
};

/*********************************************************************************/
/* Name:      InitPieVectTable()                                                 */
/* Author:    nchen                                                              */
/* Time:      20190101                                                           */
/* Parameters:none                                                               */
/* Returns:   none                                                               */
/* Description:                                                                  */
/* �?�?�??                                                                        */
/*********************************************************************************/
void InitPieVectTable(void)
{
    Uint16  i = 0;
    Uint32 *Source = (void *) &PieVectTableInit;
    Uint32 *Dest = (void *) &PieVectTable;
//--------------------------------------------------------------------------------

    Source = Source + 3;
    Dest = Dest + 3;

    EALLOW;
    for(i=0; i < 125; i++)
    {
        *Dest++ = *Source++;
    }
    EDIS;

    // Enable the PIE Vector Table
    PieCtrlRegs.PIECTRL.bit.ENPIE = 1;
}
//不�?�写�?3�?32位位�??(这些位置由Boot ROM用Boot变量初�?��??)

/*********************************************************************************/
/* Name:      MemCopy()                                                          */
/* Author:    nchen                                                              */
/* Time:      20190101                                                           */
/* Parameters:none                                                               */
/* Returns:   none                                                               */
/* Description:从源source�?拷贝n�?字节到目标destin�?                                                                  */
/* �?�?�??                                                                       */
/*********************************************************************************/
void MemCopy(Uint16 *SourceAddr, Uint16* SourceEndAddr, Uint16* DestAddr)
{
    while(SourceAddr < SourceEndAddr)
    {
       *DestAddr++ = *SourceAddr++;
    }
    return;
}

/*********************************************************************************/
/* Name:      InitFlash()                                                        */
/* Author:    nchen                                                              */
/* Time:      20190101                                                           */
/* Parameters:none                                                               */
/* Returns:   none                                                               */
/* Description:                                                                  */
/* �?�?�??                                                                        */
/*********************************************************************************/
void InitFlash(void)
{
    EALLOW;
    //Enable Flash Pipeline mode to improve performance
    //of code executed from Flash.
    FlashRegs.FOPT.bit.ENPIPE = 1;

    //Minimum waitstates required for the flash operating
    //at a given CPU rate must be characterized by TI.
    //Refer to the datasheet for the latest information.

    //Set the Paged Waitstate for the Flash
    FlashRegs.FBANKWAIT.bit.PAGEWAIT = 2;

    //Set the Random Waitstate for the Flash
    FlashRegs.FBANKWAIT.bit.RANDWAIT = 2;

    //Set the Waitstate for the OTP
    FlashRegs.FOTPWAIT.bit.OTPWAIT = 3;

    //ONLY THE DEFAULT VALUE FOR THESE 2 REGISTERS SHOULD BE USED
    FlashRegs.FSTDBYWAIT.bit.STDBYWAIT = 0x01FF;
    FlashRegs.FACTIVEWAIT.bit.ACTIVEWAIT = 0x01FF;

    EDIS;

    //Force a pipeline flush to ensure that the write to
    //the last register configured occurs before returning.
    asm(" RPT #7 || NOP");
}


/*********************************************************************************/
/* Name:      InitCpuTimers()                                                    */
/* Author:    nchen                                                              */
/* Time:      20190101                                                           */
/* Parameters:none                                                               */
/* Returns:   none                                                               */
/* Description:                                                                  */
/* �?�?�??                                                                        */
/*********************************************************************************/
void InitCpuTimers(void)
{
    // CPU Timer 0
    // Initialize address pointers to respective timer registers:
    CpuTimer0.RegsAddr = &CpuTimer0Regs;
    // Initialize timer period to maximum:
    CpuTimer0Regs.PRD.all  = 6000;      //100us=6000/60MHz  //10us=600/60MHz
    // Initialize pre-scale counter to divide by 1 (SYSCLKOUT):
    CpuTimer0Regs.TPR.all  = 0;         //TIMER0CLK=SYSOUTCLK=60MHz
    CpuTimer0Regs.TPRH.all = 0;
    // Make sure timer is stopped:
    CpuTimer0Regs.TCR.bit.TSS = 1;
    // Reload all counter register with period value:
    CpuTimer0Regs.TCR.bit.TRB = 1;
    CpuTimer0Regs.TCR.bit.SOFT = 0;
    CpuTimer0Regs.TCR.bit.FREE= 0;
    CpuTimer0Regs.TCR.bit.TIF = 1;
    CpuTimer0Regs.TCR.bit.TIE = 1;
    // Reset interrupt counters:
    CpuTimer0.InterruptCount = 0;

    // CpuTimer2 is reserved for DSP BIOS & other RTOS
    // Do not use this timer if you ever plan on integrating
    // DSP-BIOS or another realtime OS.

// Initialize address pointers to respective timer registers:
    CpuTimer1.RegsAddr = &CpuTimer1Regs;
    CpuTimer2.RegsAddr = &CpuTimer2Regs;
    // Initialize timer period to maximum:
    CpuTimer1Regs.PRD.all  = 0xFFFFFFFF;
    CpuTimer2Regs.PRD.all  = 0xFFFFFFFF;
    // Initialize pre-scale counter to divide by 1 (SYSCLKOUT):
    CpuTimer1Regs.TPR.all  = 0;
    CpuTimer1Regs.TPRH.all = 0;
    CpuTimer2Regs.TPR.all  = 0;
    CpuTimer2Regs.TPRH.all = 0;
    // Make sure timers are stopped:
    CpuTimer1Regs.TCR.bit.TSS = 1;
    CpuTimer2Regs.TCR.bit.TSS = 1;
    // Reload all counter register with period value:
    CpuTimer1Regs.TCR.bit.TRB = 1;
    CpuTimer2Regs.TCR.bit.TRB = 1;
    CpuTimer1Regs.TCR.bit.SOFT = 0;
    CpuTimer1Regs.TCR.bit.FREE= 0;
    CpuTimer2Regs.TCR.bit.SOFT = 0;
    CpuTimer2Regs.TCR.bit.FREE= 0;
    CpuTimer1Regs.TCR.bit.TIE= 0;
    CpuTimer2Regs.TCR.bit.TIE = 0;
    // Reset interrupt counters:
    CpuTimer1.InterruptCount = 0;
    CpuTimer2.InterruptCount = 0;
}

/*********************************************************************************/
/* Name:      InitADC()                                                          */
/* Author:    nchen                                                              */
/* Time:      20190101                                                           */
/* Parameters:none                                                               */
/* Returns:   none                                                               */
/* Description:                                                                  */
/*�?改：ADCREFSEL（�?�部参考电压）                                                                               */
/*********************************************************************************/
void InitADC(void)
{
    extern void DSP28x_usDelay(Uint32 Count);
//------------------------------------------------------------------------------
    EALLOW;
    SysCtrlRegs.PCLKCR0.bit.ADCENCLK = 1;
    (*Device_cal)();
    EDIS;

    EALLOW;
    AdcRegs.ADCCTL1.bit.ADCBGPWD  = 1;      // Power ADC BG
    AdcRegs.ADCCTL1.bit.ADCREFPWD = 1;      // Power reference
    AdcRegs.ADCCTL1.bit.ADCPWDN   = 1;      // Power ADC
    AdcRegs.ADCCTL1.bit.ADCENABLE = 1;      // Enable ADC
    AdcRegs.ADCCTL1.bit.ADCREFSEL = 1;      // Select external BG****使用外部参�??
    EDIS;

    DELAY_US(5000L); // Delay before converting ADC channels

    EALLOW;
    AdcRegs.ADCOFFTRIM.bit.OFFTRIM = 0;   //Apply artificial offset (+80) to account for a negative offset that may reside in the ADC core
    EDIS;

    // Configure ADC
    EALLOW;
    AdcRegs.ADCCTL1.bit.INTPULSEPOS = 1;  //INT pulse generation occurs 1 cycle prior to ADC result latching into its result register.
    AdcRegs.ADCINTSOCSEL1.all = 0x0000;   //No ADCInterrupt will trigger SOCx
    AdcRegs.ADCINTSOCSEL2.all = 0x0000;   //No ADCINT will trigger SOCx
    AdcRegs.ADCSAMPLEMODE.all = 0x0000;   //no Simultaneous samplemode,Single sample mode
    AdcRegs.ADCCTL1.bit.TEMPCONV = 0;      //setup Tempreture conversion, Result5   //wl20180925


    //Configure each channel
    AdcRegs.ADCSOC0CTL.bit.CHSEL = 0x00;    //ADCINA0  //IL   电感电流L1采�??
    AdcRegs.ADCSOC1CTL.bit.CHSEL = 0x01;    //ADCINA1  //Iin  输入电流采样（继电器内）
    AdcRegs.ADCSOC2CTL.bit.CHSEL = 0x02;    //ADCINA2  //VC   输出电�?�电???
    AdcRegs.ADCSOC3CTL.bit.CHSEL = 0x03;    //ADCINA3  //
    AdcRegs.ADCSOC4CTL.bit.CHSEL = 0x04;    //ADCINA4  //Vin1  输入电压（继电器外�??
    AdcRegs.ADCSOC5CTL.bit.CHSEL = 0x05;    //ADCINA5  //Vin2  输入电压（继电器内�??
    AdcRegs.ADCSOC6CTL.bit.CHSEL = 0x06;    //ADCINA6  //Vo1   输出电压（继电器内�??
    AdcRegs.ADCSOC7CTL.bit.CHSEL = 0x07;    //ADCINA7  //Vo2   输出电压（继电器外�??

    AdcRegs.ADCSOC8CTL.bit.CHSEL = 0x08;    //ADCINB0  //Io     输出电流采样（继电器内）
    AdcRegs.ADCSOC9CTL.bit.CHSEL = 0x09;    //ADCINB1  //Ibat   电池电流采样（继电器外）
    AdcRegs.ADCSOC10CTL.bit.CHSEL = 0x0A;   //ADCINB2
    AdcRegs.ADCSOC11CTL.bit.CHSEL = 0x0B;   //ADCINB3
    AdcRegs.ADCSOC12CTL.bit.CHSEL = 0x0C;   //ADCINB4
    AdcRegs.ADCSOC13CTL.bit.CHSEL = 0x0D;   //ADCINB5
    AdcRegs.ADCSOC14CTL.bit.CHSEL = 0x0E;   //ADCINB6
    AdcRegs.ADCSOC15CTL.bit.CHSEL = 0x0F;   //ADCINB7

    AdcRegs.ADCSOC0CTL.bit.TRIGSEL = 0x05;  //set SOC8 start trigger Software only, due to round-robin SOC0 converts first then SOC1
    AdcRegs.ADCSOC1CTL.bit.TRIGSEL = 0x05;  //�?改set SOC8 start trigger ePWM5 ADCSOCA, due to round-robin SOC0 converts first then SOC1
    AdcRegs.ADCSOC2CTL.bit.TRIGSEL = 0x05;  //�?改set SOC8 start trigger ePWM5 ADCSOCA, due to round-robin SOC0 converts first then SOC1
    AdcRegs.ADCSOC3CTL.bit.TRIGSEL = 0x05;  //�?改set SOC8 start trigger ePWM5 ADCSOCA, due to round-robin SOC0 converts first then SOC1
    AdcRegs.ADCSOC4CTL.bit.TRIGSEL = 0x05;  //�?改set SOC8 start trigger ePWM5 ADCSOCA, due to round-robin SOC0 converts first then SOC1
    AdcRegs.ADCSOC5CTL.bit.TRIGSEL = 0x05;  //set SOC8 start trigger Software only, due to round-robin SOC0 converts first then SOC1
    AdcRegs.ADCSOC6CTL.bit.TRIGSEL = 0x05;  //set SOC8 start trigger Software only, due to round-robin SOC0 converts first then SOC1
    AdcRegs.ADCSOC7CTL.bit.TRIGSEL = 0x05;  //set SOC8 start trigger Software only, due to round-robin SOC0 converts first then SOC1

    AdcRegs.ADCSOC8CTL.bit.TRIGSEL = 0x05;  //set SOC8 start trigger Software only, due to round-robin SOC0 converts first then SOC1
    AdcRegs.ADCSOC9CTL.bit.TRIGSEL = 0x05;  //set SOC9 start trigger Software only, due to round-robin SOC0 converts first then SOC1
    AdcRegs.ADCSOC10CTL.bit.TRIGSEL = 0x0D;  //set SOC10 start trigger Software only, due to round-robin SOC0 converts first then SOC1
    AdcRegs.ADCSOC11CTL.bit.TRIGSEL = 0x00;  //set SOC11 start trigger Software only, due to round-robin SOC0 converts first then SOC1
    AdcRegs.ADCSOC12CTL.bit.TRIGSEL = 0x00;  //set SOC12 start trigger Software only, due to round-robin SOC0 converts first then SOC1
    AdcRegs.ADCSOC13CTL.bit.TRIGSEL = 0x00;  //set SOC13 start trigger Software only, due to round-robin SOC0 converts first then SOC1
    AdcRegs.ADCSOC14CTL.bit.TRIGSEL = 0x00;  //set SOC14 start trigger Software only, due to round-robin SOC0 converts first then SOC1
    AdcRegs.ADCSOC15CTL.bit.TRIGSEL = 0x00;  //set SOC15 start trigger Software only, due to round-robin SOC0 converts first then SOC1

    AdcRegs.ADCSOC0CTL.bit.ACQPS = 12;  //set SOC0 S/H Window to 24 ADC Clock Cycles, (24/60M=0.4us)
    AdcRegs.ADCSOC1CTL.bit.ACQPS = 12;  //set SOC1 S/H Window to 24 ADC Clock Cycles,//Vout
    AdcRegs.ADCSOC2CTL.bit.ACQPS = 12;  //set SOC2 S/H Window to 24 ADC Clock Cycles, (12/60M=0.2us)//Vin
    AdcRegs.ADCSOC3CTL.bit.ACQPS = 12;  //set SOC3 S/H Window to 24 ADC Clock Cycles,//Iout
    AdcRegs.ADCSOC4CTL.bit.ACQPS = 12;  //set SOC5 S/H Window to 24 ADC Clock Cycles,// ILout
    AdcRegs.ADCSOC5CTL.bit.ACQPS = 12;  //set SOC6 S/H Window to 24 ADC Clock Cycles,
    AdcRegs.ADCSOC6CTL.bit.ACQPS = 12;  //set SOC7 S/H Window to 24 ADC Clock Cycles,
    AdcRegs.ADCSOC7CTL.bit.ACQPS = 12;  //set SOC7 S/H Window to 24 ADC Clock Cycles,

    AdcRegs.ADCSOC8CTL.bit.ACQPS = 12;  //set SOC8 S/H Window to 24 ADC Clock Cycles,
    AdcRegs.ADCSOC9CTL.bit.ACQPS = 12;  //set SOC9 S/H Window to 24 ADC Clock Cycles,
    AdcRegs.ADCSOC10CTL.bit.ACQPS = 12;  //set SOC10 S/H Window to 24 ADC Clock Cycles,
    AdcRegs.ADCSOC11CTL.bit.ACQPS = 12;  //set SOC11 S/H Window to 24 ADC Clock Cycles,
    AdcRegs.ADCSOC12CTL.bit.ACQPS = 12;  //set SOC12 S/H Window to 24 ADC Clock Cycles,
    AdcRegs.ADCSOC13CTL.bit.ACQPS = 12;  //set SOC13 S/H Window to 24 ADC Clock Cycles,
    AdcRegs.ADCSOC14CTL.bit.ACQPS = 12;  //set SOC14 S/H Window to 24 ADC Clock Cycles,
    AdcRegs.ADCSOC15CTL.bit.ACQPS = 12;  //set SOC15 S/H Window to 24 ADC Clock Cycles,

    EDIS;
    AdcRegs.ADCSOCFRC1.all = 0xFFFF;        //Force Start of Conversion Flag
}


/*********************************************************************************/
/* Name:      InitEPwm()                                                         */
/* Author:    nchen                                                              */
/* Time:      20190101                                                           */
/* Parameters:none                                                               */
/* Returns:   none                                                               */
/* Description:                                                                  */
/*                                                                               */
/*********************************************************************************/
void InitEPwm(void)
{
    EALLOW;
    SysCtrlRegs.PCLKCR0.bit.TBCLKSYNC = 0;     // Disable TBCLK within the EPWM
    EDIS;
    //    /*------------------ePWM1  initialize----------------------------------------*/
        EPwm1Regs.AQSFRC.bit.RLDCSF = 3;
        EPwm1Regs.TBSTS.all=0;                       // ʱ��״???�Ĵ�����ʼ??
        EPwm1Regs.TBPHS.half.TBPHS=0;                // EPWM1��λ??0���ο���׼��
        EPwm1Regs.TBCTR=0;                           // ʱ����������0
        EPwm1Regs.TBCTL.bit.FREE_SOFT = 0;
        EPwm1Regs.TBCTL.bit.PHSDIR = 0;         // Count up when synchronization
        EPwm1Regs.TBCTL.bit.HSPCLKDIV = 0;      // TBCLK=SYSCLKOUT/1=60MHz
        EPwm1Regs.TBCTL.bit.CLKDIV = 0;
        EPwm1Regs.TBCTL.bit.PRDLD = 0;          // TBPRD LOAD ZERO
        EPwm1Regs.TBCTL.bit.PHSEN = 1;          // ʹ����λ����
        EPwm1Regs.TBCTL.bit.SYNCOSEL = 2;       // ������SYNCO = CTR=0�¼�����ģ�����ͬ���ź�??
        EPwm1Regs.TBCTL.bit.CTRMODE = 2;        // ��������ģʽ
        EPwm1Regs.TBPRD=TBPRDVAL;
        // 新调制同步主机：ePWM1 在 CTR=ZERO 发同步，且不加载外部相位。
        EPwm1Regs.TBPHS.half.TBPHS = 0;
        EPwm1Regs.TBCTL.bit.PHSEN = 0;
        EPwm1Regs.TBCTL.bit.SYNCOSEL = 1;
        // CMPA 使用 shadow，并在 CTR=ZERO 统一装载，避免周期中间更新毛刺。
        EPwm1Regs.CMPCTL.bit.SHDWAMODE = 0;
        EPwm1Regs.CMPCTL.bit.LOADAMODE = 0;
        EPwm1Regs.CMPA.half.CMPA =TBPRDVAL/2;   // 50%ռ��??
        EPwm1Regs.CMPB = TBPRDVAL;
        EPwm1Regs.AQCTLA.bit.CAD= 2;               // CTR�½���CMPA��ePWMA���??
        EPwm1Regs.AQCTLA.bit.CAU= 1;               // CTR������CMPA��ePWMA���??
        EPwm1Regs.DBCTL.bit.OUT_MODE=3;                 // ����ʹ��
        EPwm1Regs.DBRED=36;                                 // ��������??0
        EPwm1Regs.DBFED=36;                                 // �½�����??100ns
        EPwm1Regs.DBCTL.bit.POLSEL = 2;                    // ePWMB����
        EPwm1Regs.DBCTL.bit.IN_MODE = 0;
        EPwm1Regs.ETSEL.all=0;                             // �¼������ر�
        EPwm1Regs.ETFLG.all=0;
        EPwm1Regs.ETCLR.all=0;
        EPwm1Regs.ETFRC.all=0;

        EPwm1Regs.ETSEL.bit.INTEN = 1;   //1=Enable ePWM Interrupt Generration
        EPwm1Regs.ETSEL.bit.INTSEL = ET_CTR_ZERO;   //CTR=0;
        EPwm1Regs.ETPS.bit.INTPRD = 0x1;  // CTR=ZERO 每个 PWM 周期触发一次 EPWM1 ISR
        EPwm1Regs.ETSEL.bit.SOCAEN = 1;             //ʹ��ePWMSOCA�жϲ���??
        EPwm1Regs.ETSEL.bit.SOCASEL = ET_CTR_ZERO;   //CTR=0;
        EPwm1Regs.ETPS.bit.SOCAPRD = 0x1;         //�ڵ�??���¼�����ʱ������SOCA�ź�  20kHz

        /*------------------ePWM2  initialize----------------------------------------*/
        EPwm2Regs.AQSFRC.bit.RLDCSF = 3;
        EPwm2Regs.TBSTS.all=0;                       // ʱ��״???�Ĵ�����ʼ??
        EPwm2Regs.TBPHS.half.TBPHS = (Uint16)(TBPRDVAL * 0);  // ��������??30%��λƫ��
        EPwm2Regs.TBCTR=0;                           // ��������0
        EPwm2Regs.TBCTL.bit.FREE_SOFT = 0;
        EPwm2Regs.TBCTL.bit.PHSDIR = 0;         // Count up when synchronization
        EPwm2Regs.TBCTL.bit.HSPCLKDIV = 0;      // TBCLK=60MHz
        EPwm2Regs.TBCTL.bit.CLKDIV = 0;
        EPwm2Regs.TBCTL.bit.PRDLD = 2;          // TBPRD LOAD ZERO
        EPwm2Regs.TBCTL.bit.PHSEN = 1;          // ʹ����λ����
        EPwm2Regs.TBCTL.bit.SYNCOSEL = 0;       // ʹ��EPWM1��SYNCIN��Ϊͬ��??
        EPwm2Regs.TBCTL.bit.CTRMODE = 2;        // ��������ģʽ
        EPwm2Regs.TBPRD=TBPRDVAL;
        // 新调制：ePWM2 与 ePWM1 同相，仅由 CMPA 产生原边左右桥臂差异。
        EPwm2Regs.TBPHS.half.TBPHS = 0;
        EPwm2Regs.TBCTL.bit.PHSDIR = 0;
        EPwm2Regs.CMPCTL.bit.SHDWAMODE = 0;
        EPwm2Regs.CMPCTL.bit.LOADAMODE = 0;
        EPwm2Regs.CMPA.half.CMPA =TBPRDVAL/2;   // 50%ռ��??
        EPwm2Regs.CMPB = TBPRDVAL;
        EPwm2Regs.AQCTLA.bit.CAD= 2;               // CTR�½���CMPA��ePWMB���??
        EPwm2Regs.AQCTLA.bit.CAU= 1;               // CTR������CMPA��ePWMB���??
        EPwm2Regs.DBCTL.bit.OUT_MODE=3;                 // ����ʹ��
        EPwm2Regs.DBRED=36;                                 // ��������??0
        EPwm2Regs.DBFED=36;                                 // �½�����??100ns
        EPwm2Regs.DBCTL.bit.POLSEL = 1;                    // ePWMA����
        EPwm2Regs.DBCTL.bit.IN_MODE = 0;
        EPwm2Regs.ETSEL.all=0;                             // �¼������ر�
        EPwm2Regs.ETFLG.all=0;
        EPwm2Regs.ETCLR.all=0;
        EPwm2Regs.ETFRC.all=0;
       /*------------------ePWM3  initialize----------------------------------------*/
       EPwm3Regs.AQSFRC.bit.RLDCSF = 3;
       EPwm3Regs.TBSTS.all=0;                       //ʱ��״???�Ĵ�����ʼ??
       EPwm3Regs.TBPHS.half.TBPHS = (Uint16)(TBPRDVAL);   // �ͺ�EPWM1 phase_shift��TBCLK
       EPwm3Regs.TBCTR=0;                           //ʱ����������0
       EPwm3Regs.TBCTL.bit.FREE_SOFT = 0;
       EPwm3Regs.TBCTL.bit.PHSDIR = 0;         // Count up when synchronization
       EPwm3Regs.TBCTL.bit.HSPCLKDIV = 0;      // Clock ratio to TBCLK=SYSCLKOUT/1=60MHz
       EPwm3Regs.TBCTL.bit.CLKDIV = 0;
       EPwm3Regs.TBCTL.bit.PRDLD = 2;          // TBPRD LOAD ZERO
       EPwm3Regs.TBCTL.bit.PHSEN = 1;          // �޸ģ�ʹ����λ��??
       EPwm3Regs.TBCTL.bit.SYNCOSEL = 2;       // �޸ģ�ʹ��EPWM1��ͬ����??
       EPwm3Regs.TBCTL.bit.CTRMODE = 2;        // Count up and down
       EPwm3Regs.TBPRD=TBPRDVAL;
       // 新调制：移除旧 180 度初始偏置；ePWM3 传递同步给 ePWM4。
       EPwm3Regs.TBPHS.half.TBPHS = 0;
       EPwm3Regs.TBCTL.bit.SYNCOSEL = 0;
       EPwm3Regs.CMPCTL.bit.SHDWAMODE = 0;
       EPwm3Regs.CMPCTL.bit.LOADAMODE = 0;
       EPwm3Regs.CMPA.half.CMPA =TBPRDVAL/2;
       EPwm3Regs.CMPB = TBPRDVAL;
       EPwm3Regs.AQCTLA.bit.CAD= 2;               // CTR�½���CMPAֵ��ePWMA���??
       EPwm3Regs.AQCTLA.bit.CAU= 1;               // CTR������CMPAֵ��ePWMA���??
       EPwm3Regs.DBCTL.bit.OUT_MODE=3;                 //����ʹ��˫������??
       EPwm3Regs.DBRED=36;                                 //������������ʱ����������
       EPwm3Regs.DBFED=36;                                 //�����½�����ʱ������100ns����
       EPwm3Regs.DBCTL.bit.POLSEL = 2;                    //ePWMB����
       EPwm3Regs.DBCTL.bit.IN_MODE = 0;
       EPwm3Regs.ETSEL.all=0;                             //�¼������ر�
       EPwm3Regs.ETFLG.all=0;
       EPwm3Regs.ETCLR.all=0;
       EPwm3Regs.ETFRC.all=0;

       /*------------------ePWM4  initialize----------------------------------------*/
       EPwm4Regs.AQSFRC.bit.RLDCSF = 3;
       EPwm4Regs.TBSTS.all=0;                       //ʱ��״???�Ĵ�����ʼ??
       EPwm4Regs.TBPHS.half.TBPHS = (Uint16)(TBPRDVAL * 0);  // ��EPWM3��λ�෴
       EPwm4Regs.TBCTR=0;                           //ʱ����������0
       EPwm4Regs.TBCTL.bit.FREE_SOFT = 0;
       EPwm4Regs.TBCTL.bit.PHSDIR = 0;         // Count up when synchronization
       EPwm4Regs.TBCTL.bit.HSPCLKDIV = 0;      // Clock ratio to TBCLK=SYSCLKOUT/1=60MHz
       EPwm4Regs.TBCTL.bit.CLKDIV = 0;
       EPwm4Regs.TBCTL.bit.PRDLD = 2;          // TBPRD LOAD ZERO
       EPwm4Regs.TBCTL.bit.PHSEN = 1;          // �޸ģ�ʹ����λ��??
       EPwm4Regs.TBCTL.bit.SYNCOSEL = 0;       // �޸ģ�ʹ��EPWM1��ͬ����??
       EPwm4Regs.TBCTL.bit.CTRMODE = 2;        // Count up and down
       EPwm4Regs.TBPRD=TBPRDVAL;
       // 新调制：ePWM4 与 ePWM3 使用相同相位，仅由 CMPA 产生副边左右桥臂差异。
       EPwm4Regs.TBPHS.half.TBPHS = 0;
       EPwm4Regs.TBCTL.bit.PHSDIR = 0;
       EPwm4Regs.CMPCTL.bit.SHDWAMODE = 0;
       EPwm4Regs.CMPCTL.bit.LOADAMODE = 0;
       EPwm4Regs.CMPA.half.CMPA =TBPRDVAL/2;
       EPwm4Regs.CMPB = TBPRDVAL;
       EPwm4Regs.AQCTLA.bit.CAD= 2;               // CTR�½���CMPAֵ��ePWMA���??
       EPwm4Regs.AQCTLA.bit.CAU= 1;               // CTR������CMPAֵ��ePWMA���??
       EPwm4Regs.DBCTL.bit.OUT_MODE=3;                 //����ʹ��˫������??
       EPwm4Regs.DBRED=36;                                 //������������ʱ����������
       EPwm4Regs.DBFED=36;                                 //�����½�����ʱ������100ns����
       EPwm4Regs.DBCTL.bit.POLSEL = 1;                    //ePWMB����
       EPwm4Regs.DBCTL.bit.IN_MODE = 0;
       EPwm4Regs.ETSEL.all=0;                             //�¼������ر�
       EPwm4Regs.ETFLG.all=0;
       EPwm4Regs.ETCLR.all=0;
       EPwm4Regs.ETFRC.all=0;

    EALLOW;
    SysCtrlRegs.PCLKCR0.bit.TBCLKSYNC = 1;     // Enable TBCLK within the EPWM
    EDIS;


}


/*********************************************************************************/
/* Name:      InitSci()                                                          */
/* Author:    nchen                                                              */
/* Time:      20190101                                                           */
/* Parameters:none                                                               */
/* Returns:   none                                                               */
/* Description:RS485,9600,8bits,1 stop,no parity                                 */
/*                                                                               */
/*********************************************************************************/
void InitSci(void)
{
    // scia_fifo_init
    EALLOW;
    SciaRegs.SCICCR.all = 0x07;             // 1 stop bit,No loopback,no parity,8 char bits
    SciaRegs.SCICTL1.all = 0x03;            // enable TX, RX, internal SCICLK, Disable RX_ERR, SLEEP, TXWAKE
    SciaRegs.SCICTL2.all = 0x00;            // fifo mode,they are ignored
    SciaRegs.SCIHBAUD = 0x00;               // 9600 bps=(12M/(9600*8))-1=155.25
    SciaRegs.SCILBAUD = 0xC2;
    SciaRegs.SCIFFTX.all = 0xC000;          // SCI FIFO enable,TX FIFO interrupt disabled
//  SciaRegs.SCIFFTX.all = 0xE000;
    SciaRegs.SCIFFRX.all = 0x0061;          // RX FIFO interrupt enabled when >1 byte
//  SciaRegs.SCIFFRX.all = 0x6040;
    SciaRegs.SCIFFCT.all = 0x0000;          // Disables auto-baud alignment

    SciaRegs.SCICTL1.all = 0x23;            // re-enable the SCI

    SciaRegs.SCIFFTX.bit.TXFIFOXRESET = 1;
    SciaRegs.SCIFFRX.bit.RXFIFORESET = 1;
    SciaRegs.SCIFFRX.bit.RXFFINTCLR = 1;
    EDIS;
}

/*********************************************************************************/
/* Name:      InitState()                                                        */
/* Author:    nchen                                                              */
/* Time:      20190101                                                           */
/* Parameters:none                                                               */
/* Returns:   none                                                               */
/* Description:claer ram and init flag                                           */
/*                                                                               */
/*********************************************************************************/
void InitState(void)
{
    Uint16 j;
//  Uint16 *p;
////---------------------------------------------------------------------------------
//  EALLOW;
//  Cla1Regs.MMEMCFG.bit.PROGE = 0;
//  EDIS;
//    p=(Uint16 *)0x009000;    //清�??9000-A000
//    for(i=0;i<0x001000;i++)
//    {
//        *p=0x0000;
//        p++;
//    }
//  EPwm3Regs.AQCSFRC.bit.CSFA = 0;
//---------------------------------------------------------------------------------
//  M_SetFlag(SL_POWERON);      //
//  M_SetFlag(SL_SOFTSTART);
    M_ClrFlag(SL_SOFTSTART1);
    MAIN_PARA.softstart_cnt = 0;
    MAIN_PARA.pulse_cnt = 0;    //count cputimer0 times,0-9
    MAIN_PARA.pulse_cnt1 = 0;
    MAIN_PARA.pulse_cnt2 = 0;
    MAIN_PARA.delay_poweron = 0;
    MAIN_PARA.ad_cnt = 0;
    ARI_PARA.ubus = 0;
    ARI_PARA.ubat = 0;
    ARI_PARA.ubus_last = 0;
    ARI_PARA.ubat_last = 0;//
    POWER_PARA.delay_prec1=0;
//  M_ClrFlag(SL_TZ1INT);
    M_ClrFlag(SL_SUBATOV1);
    M_ClrFlag(SL_SIBATOV1);
    M_ClrFlag(SL_SUBUSOV1);

    M_ClrFlag(SL_START);        //=上位机�?�求�?�??
    M_ClrFlag(SL_PREC1);//初�?�值为0，没有其他位�?使其�?零，�?执�?�一�?
    M_SetFlag(SL_STOPOK);//=1上电初�?�化完�???5
    M_SetFlag(SL_CODEOK);//=1功能码校验完�??
    M_ClrFlag(SL_OFFK);
    M_ClrFlag(SL_SERIOUS);
    M_ClrFlag(SL_ERROR);
    M_ClrFlag(SL_FFTFLAG1);//fft flag
    M_ClrFlag(SL_FFTFLAG2);
    M_ClrFlag(SL_FFTFLAG3);
//  M_ClrFlag(SL_PIDFLAG);
//  M_ClrFlag(SL_CLAPROG);
    M_ClrFlag(SL_SYS_START);
    M_ClrFlag(SL_BURST);
//  FFT_PARA.count1 = 0;
//  EPwm6Regs.AQCSFRC.bit.CSFA = 1;

    M_ClrFlag(SL_SUBUSOV1);
    M_ClrFlag(SL_SIBATOV1);
//---------------------------------------------------------------------------------
    for(j=0;j<NUM_ALL;j++)//
    {
      *(DATA_BASE[j].para) = DATA_BASE[j].init;
    }
//---------------------------------------------------------------------------------
//  tab_wn();//sin_tab  for fft
}


/*********************************************************************************/
/* Name:      InitEZ()                                                        */
/* Author:    yzy                                                            */
/* Time:      20201102                                                           */
/* Parameters:none                                                               */
/* Returns:   none                                                               */
/* Description:                                     */
/*                                                                               */
/*********************************************************************************/
void InitTZ(void)
{
    EALLOW;

    EPwm1Regs.TZSEL.bit.OSHT1=1;//使能TZ1 one-short错�??联防功�??
    EPwm1Regs.TZSEL.bit.OSHT2=1;//使能TZ2 one-short错�??联防功�??
    EPwm1Regs.TZSEL.bit.OSHT3=1;//使能TZ3 one-short错�??联防功�??
    EPwm1Regs.TZCTL.bit.TZA = 2;//强制ePWM1A输出低状�?
    EPwm1Regs.TZCTL.bit.TZB = 2;//强制ePWM1B输出低状�?
    EPwm1Regs.TZEINT.bit.OST = 0;

    EPwm2Regs.TZSEL.bit.OSHT1=1;//使能TZ1 one-short错�??联防功�??
    EPwm2Regs.TZSEL.bit.OSHT2=1;//使能TZ2 one-short错�??联防功�??
    EPwm2Regs.TZSEL.bit.OSHT3=1;//使能TZ3 one-short错�??联防功�??
    EPwm2Regs.TZCTL.bit.TZA = 2;
    EPwm2Regs.TZCTL.bit.TZB = 2;
    EPwm2Regs.TZEINT.bit.OST = 0;

    EPwm3Regs.TZSEL.bit.OSHT1=1;//使能TZ1 one-short错�??联防功�??
    EPwm3Regs.TZSEL.bit.OSHT2=1;//使能TZ2 one-short错�??联防功�??
    EPwm3Regs.TZSEL.bit.OSHT3=1;//使能TZ3 one-short错�??联防功�??
    EPwm3Regs.TZCTL.bit.TZA = 2;
    EPwm3Regs.TZCTL.bit.TZB = 2;
    EPwm3Regs.TZEINT.bit.OST = 0;

    EPwm4Regs.TZSEL.bit.OSHT1=1;//使能TZ1 one-short错�??联防功�??
    EPwm4Regs.TZSEL.bit.OSHT2=1;//使能TZ2 one-short错�??联防功�??
    EPwm4Regs.TZSEL.bit.OSHT3=1;//使能TZ3 one-short错�??联防功�??
    EPwm4Regs.TZCTL.bit.TZA = 2;
    EPwm4Regs.TZCTL.bit.TZB = 2;
    EPwm4Regs.TZEINT.bit.OST = 0;

    EPwm5Regs.TZSEL.bit.OSHT1=1;//使能TZ1 one-short错�??联防功�??
    EPwm5Regs.TZSEL.bit.OSHT2=1;//使能TZ2 one-short错�??联防功�??
    EPwm5Regs.TZSEL.bit.OSHT3=1;//使能TZ3 one-short错�??联防功�??
    EPwm5Regs.TZCTL.bit.TZA = 2;
    EPwm5Regs.TZCTL.bit.TZB = 2;
    EPwm5Regs.TZEINT.bit.OST = 0;

    EPwm6Regs.TZSEL.bit.OSHT1=1;//使能TZ1 one-short错�??联防功�??
    EPwm6Regs.TZSEL.bit.OSHT2=1;//使能TZ2 one-short错�??联防功�??
    EPwm6Regs.TZSEL.bit.OSHT3=1;//使能TZ3 one-short错�??联防功�??
    EPwm6Regs.TZCTL.bit.TZA = 2;
    EPwm6Regs.TZCTL.bit.TZB = 2;
    EPwm6Regs.TZEINT.bit.OST = 0;

    EDIS;

}
/*********************************************************************************/
/* Name:      InitCla()                                                        */
/* Author:    yzy                                                            */
/* Time:      20201213                                                          */
/* Parameters:none                                                               */
/* Returns:   none                                                               */
/* Description:claer ram and init flag                                           */
/*                                                                               */
/*********************************************************************************/
void InitCla(void)
{
    EALLOW;/*cla init---yzy---2020-12-05*/

    // Cla1ForceTask2() issues IACK #0x0002, so Task2 must use the MVECT2 vector.
    // Task1 is not used in this project; leave MVECT1 unconfigured.
    Cla1Regs.MVECT2 = (uint16_t)(&Cla1Task2);
    Cla1Regs.MMEMCFG.bit.RAM0E = 0;
    Cla1Regs.MMEMCFG.bit.PROGE = 1;
    Cla1Regs.MMEMCFG.bit.RAM1E = 1;

//    Cla1Regs.MPISRCSEL1.bit.PERINT2SEL = CLA_INT2_EPWM2INT;
    Cla1Regs.MCTL.bit.IACKE = 1;
    Cla1Regs.MIER.all = 0x00FF;
    // Task2 is triggered only by the divided EPWM1 ISR scheduler after startup.
    Cla1Regs.MPISRCSEL1.bit.PERINT2SEL = CLA_INT2_NONE;


    EDIS;
}

/*********************************************************************************/
/* Name:      InitSpi()                                                        */
/* Author:    zlm                                                            */
/* Time:      20221109                                                          */
/* Parameters:none                                                               */
/* Returns:   none                                                               */
/* Description:                                         */
/*                                                                               */
/*********************************************************************************/
void InitSpi(void)
{
    EALLOW;
    //step1：Clear the SPI Software Reset bit (SPISWRESET) to 0 to force the SPI to the reset state
    SpiaRegs.SPICCR.bit.SPISWRESET=0;     //在�?�位状态下�?以更改SPI的寄???��??

    //step2�? Configure the SPI as desired:
    SpiaRegs.SPICTL.bit.MASTER_SLAVE=1;     //0:Slave 1:Master
    SpiaRegs.SPIPRI.bit.TRIWIRE = 1;      //�?�?三线模�???
    SpiaRegs.SPICCR.bit.CLKPOLARITY=0;     //总线闲置为低电平
    SpiaRegs.SPICTL.bit.CLK_PHASE=0;       //�?一�?时钟沿数�?采�??
                   //这两位决定：在上升沿进�?�数�?采样，下降沿数据发�???
    SpiaRegs.SPIBRR = 23;                   //12M/(23+1)=500k
    SpiaRegs.SPICCR.bit.SPICHAR=0xF;          //设置发�?�接??�字符的长度16�?
    SpiaRegs.SPISTS.all=0;                  //清除标志�?
    SpiaRegs.SPICTL.bit.SPIINTENA=1;         //�?�?�?�??
    //暂不使用FIFO
    SpiaRegs.SPICTL.bit.TALK=1;             //�?�?四线模�??? enable transmit path
    SpiaRegs.SPIPRI.bit.FREE = 1;           //�?由运�?

    //step3；Set SPISWRESET to 1 to release the SPI from the reset state
    SpiaRegs.SPICCR.bit.SPISWRESET = 1;
    EDIS;
}
/*===============================================================================*/
/* Name:      InitCAN()                                                          */
/* Author:    ZLM                                                              */
/* Time:      20240401                                                           */
/* Parameters:none                                                               */
/* Returns:   none                                                               */
/* Description:鍒濆CAN�?�?俊�?�勫瓨鍣�??
/*===============================================================================*/
/******************* (C) COPYRIGHT 2019  **************************END OF FILE****/
void InitCAN(void)
{
    struct ECAN_REGS ECanaShadow;//涓篊AN瀵勫瓨鍣ㄥ垱???�轰竴涓�?�瀛愬瘎�?�樺櫒缁撴�??銆傚洜涓鸿繖浜涘瘎瀛樺櫒鍙厑璁�??32浣嶈闂�傚杩欎簺�?�勫瓨鍣ㄧ�??16浣嶈闂彲鑳戒細鎹熷潖瀵勫瓨鍣ㄥ唴瀹�?�垨杩斿洖閿欒鏁版嵁銆�?

        EALLOW;     // EALLOW enables access to protected bits

        //閰嶇疆鍙戦�佹帴�?跺�?�鑳�?
        ECanaShadow.CANTIOC.all = ECanaRegs.CANTIOC.all;
        ECanaShadow.CANTIOC.bit.TXFUNC = 1;//CANTX�?曡剼�?ㄤ簬CAN浼犺�?鍔熻兘銆�?
        ECanaRegs.CANTIOC.all = ECanaShadow.CANTIOC.all;

        ECanaShadow.CANRIOC.all = ECanaRegs.CANRIOC.all;
        ECanaShadow.CANRIOC.bit.RXFUNC = 1;//CANRX�?曡剼�?ㄤ簬CAN鎺ユ敹鍔熻兘銆�
        ECanaRegs.CANRIOC.all = ECanaShadow.CANRIOC.all;

        //eCAN澧炲己妯″�??
        ECanaShadow.CANMC.all = ECanaRegs.CANMC.all;
        ECanaShadow.CANMC.bit.SCB = 1;//Select eCAN mode.
        ECanaRegs.CANMC.all = ECanaShadow.CANMC.all;

        //�?鍒濆鍖�?
        ECanaMboxes.MBOX0.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX1.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX2.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX3.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX4.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX5.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX6.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX7.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX8.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX9.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX10.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX11.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX12.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX13.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX14.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX15.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX16.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX17.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX18.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX19.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX20.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX21.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX22.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX23.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX24.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX25.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX26.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX27.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX28.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX29.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX30.MSGCTRL.all = 0x00000000;
        ECanaMboxes.MBOX31.MSGCTRL.all = 0x00000000;

        //鍙戦�佹秷鎭垚鍔熸爣蹇椾綅鍒濆鍖�??
        ECanaRegs.CANTA.all = 0xFFFFFFFF;   /* Clear all TAn bits */
        //鎺ユ敹娑堟伅鎸�???捣鏍囧織浣嶅垵濮�????
        ECanaRegs.CANRMP.all = 0xFFFFFFFF;  /* Clear all RMPn bits */
        //涓柇鍒濆鍖�
        ECanaRegs.CANGIF0.all = 0xFFFFFFFF; /* Clear all interrupt flag bits */
        ECanaRegs.CANGIF1.all = 0xFFFFFFFF;

        //CCR涓�??1鏃跺厑璁稿BTC閰嶇�??
        ECanaShadow.CANMC.all = ECanaRegs.CANMC.all;
        ECanaShadow.CANMC.bit.CCR = 1 ;            // Set CCR = 1
        ECanaRegs.CANMC.all = ECanaShadow.CANMC.all;

        //绛�?�緟CCE涓�??1鏃惰繘琛屼笅涓�姝ユ搷浣�?
        do
        {
          ECanaShadow.CANES.all = ECanaRegs.CANES.all;
        } while(ECanaShadow.CANES.bit.CCE != 1 );       // Wait for CCE bit to be set..

        ECanaShadow.CANBTC.all = 0;
        /* The following block is only for 60 MHz SYSCLKOUT. (30 MHz CAN module clock Bit rate = 1 Mbps
           See Note at end of file. */

        //璁剧疆娉㈢�?�鐜�?;sysclock=60MHz锛孋AN鏃堕挓涓�?/2.鍗�??30MHz
        //娉㈢壒鐜�?=SYSCLOCK/2/(brp+1)/(tseg1+1+tseg2+1+1)
        //=60M/2/(2+1)/(6+1+1+1+1)=1M=100k
//        ECanaShadow.CANBTC.bit.BRPREG = 2;
//        ECanaShadow.CANBTC.bit.TSEG2REG = 1;
//        ECanaShadow.CANBTC.bit.TSEG1REG = 6;
//        ECanaShadow.CANBTC.bit.SAM = 1;
//        ECanaRegs.CANBTC.all = ECanaShadow.CANBTC.all;
        ECanaShadow.CANBTC.bit.BRPREG = 5;     //500kb
        ECanaShadow.CANBTC.bit.TSEG2REG = 1;
        ECanaShadow.CANBTC.bit.TSEG1REG = 6;
        ECanaShadow.CANBTC.bit.SAM = 1;
        ECanaRegs.CANBTC.all = ECanaShadow.CANBTC.all;


        //娓呴櫎CCR浣嶏紝�?��?�富鎺у埗鍣ㄩ厤缃�?
        ECanaShadow.CANMC.all = ECanaRegs.CANMC.all;
        ECanaShadow.CANMC.bit.CCR = 0 ;            // Set CCR = 0
        ECanaRegs.CANMC.all = ECanaShadow.CANMC.all;

        // CCE浣嶆竻闄よ�?�鏄巈CAN�???�潡閰嶇疆�?�屾�??
        do
        {
          ECanaShadow.CANES.all = ECanaRegs.CANES.all;
        } while(ECanaShadow.CANES.bit.CCE != 0 );       // Wait for CCE bit to be  cleared..

        //MSGIDs閰嶇疆鍓嶅睆钄介偖绠憋紝MSGIDs鍙�??��ㄩ偖绠卞睆钄芥�?�閰嶇�??
        ECanaRegs.CANME.all = 0;        // Required before writing the MSGIDs

        EDIS;
}

void InitRELAY(void)
{
    GpioDataRegs.GPBCLEAR.bit.GPIO43 = 1;//LLC输入主继电器K6
    GpioDataRegs.GPBCLEAR.bit.GPIO42 = 1;//LLC输入预充电继电器K5
    GpioDataRegs.GPBSET.bit.GPIO39 = 1;//H桥旁�?继电器K4
    GpioDataRegs.GPACLEAR.bit.GPIO25 = 1;//H桥输出主继电器K2
    GpioDataRegs.GPACLEAR.bit.GPIO18 = 1;//H桥输出�?�充电继电�???3
}
