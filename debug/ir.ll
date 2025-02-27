; ModuleID = "main"
target triple = "x86_64-pc-linux-gnu"
target datalayout = ""

define i32 @"main"()
{
main_entry:
  %".2" = alloca i32
  store i32 52, i32* %".2"
  %".4" = alloca float
  store float 0x40454cccc0000000, float* %".4"
  ret i32 52
}
