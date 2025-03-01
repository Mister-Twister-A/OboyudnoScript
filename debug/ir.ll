; ModuleID = "main"
target triple = "x86_64-pc-linux-gnu"
target datalayout = ""

@"true" = constant i1 1
@"false" = constant i1 0
define i32 @"main"()
{
main_entry:
  %".2" = alloca i32
  store i32 11, i32* %".2"
  %".4" = load i32, i32* %".2"
  %".5" = icmp eq i32 %".4", 10
  br i1 %".5", label %"main_entry.if", label %"main_entry.else"
main_entry.if:
  store i32 5, i32* %".2"
  br label %"main_entry.endif"
main_entry.else:
  store i32 52, i32* %".2"
  br label %"main_entry.endif"
main_entry.endif:
  %".11" = load i32, i32* %".2"
  ret i32 %".11"
}

define float @"main52"()
{
main52_entry:
  %".2" = alloca float
  store float 0x40454cccc0000000, float* %".2"
  %".4" = alloca i32
  store i32 130, i32* %".4"
  %".6" = load float, float* %".2"
  %".7" = fcmp oeq float %".6", 0x4045428f60000000
  br i1 %".7", label %"main52_entry.if", label %"main52_entry.else"
main52_entry.if:
  store i32 27, i32* %".4"
  br label %"main52_entry.endif"
main52_entry.else:
  store i32 143, i32* %".4"
  br label %"main52_entry.endif"
main52_entry.endif:
  %".13" = load float, float* %".2"
  ret float %".13"
}
