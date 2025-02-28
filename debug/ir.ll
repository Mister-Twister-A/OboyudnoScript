; ModuleID = "main"
target triple = "x86_64-pc-linux-gnu"
target datalayout = ""

define i32 @"main"()
{
main_entry:
  %".2" = alloca i32
  store i32 10, i32* %".2"
  %".4" = load i32, i32* %".2"
  %".5" = load i32, i32* %".2"
  %".6" = sdiv i32 520, %".5"
  %".7" = add i32 %".4", %".6"
  ret i32 %".7"
}

define float @"main52"()
{
main52_entry:
  %".2" = alloca float
  store float 0x40454cccc0000000, float* %".2"
  %".4" = alloca i64
  store i64 130, i64* %".4"
  %".6" = load float, float* %".2"
  ret float %".6"
}
