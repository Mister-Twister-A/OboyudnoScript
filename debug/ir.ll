; ModuleID = "main"
target triple = "x86_64-pc-linux-gnu"
target datalayout = ""

@"true" = constant i1 1
@"false" = constant i1 0
define i32 @"not_main"(i32 %".1", i32 %".2", i32 %".3")
{
not_main_entry:
  %".5" = alloca i32
  store i32 %".1", i32* %".5"
  %".7" = alloca i32
  store i32 %".2", i32* %".7"
  %".9" = alloca i32
  store i32 %".3", i32* %".9"
  %".11" = load i32, i32* %".5"
  %".12" = load i32, i32* %".7"
  %".13" = add i32 %".11", %".12"
  %".14" = load i32, i32* %".9"
  %".15" = add i32 %".13", %".14"
  ret i32 %".15"
}

define i32 @"main"()
{
main_entry:
  %".2" = call i32 @"not_main"(i32 52, i32 52, i32 52)
  ret i32 %".2"
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
