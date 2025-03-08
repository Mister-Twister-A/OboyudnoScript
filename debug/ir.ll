; ModuleID = "main"
target triple = "x86_64-pc-linux-gnu"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

@"true" = constant i1 1
@"false" = constant i1 0
define i32 @"not_main"(i32 %".1")
{
not_main_entry:
  %".3" = alloca i32
  store i32 %".1", i32* %".3"
  %".5" = load i32, i32* %".3"
  %".6" = add i32 %".5", 1
  ret i32 %".6"
}

define i32 @"main"()
{
main_entry:
  %".2" = alloca i32
  store i32 0, i32* %".2"
  %".4" = load i32, i32* %".2"
  %".5" = icmp slt i32 %".4", 52
  br i1 %".5", label %"while_entry_1", label %"while_otherwise_1"
while_entry_1:
  %".7" = load i32, i32* %".2"
  %".8" = alloca [9 x i8]*
  store [9 x i8]* @"__str_2", [9 x i8]** %".8"
  %".10" = bitcast [9 x i8]* @"__str_2" to i8*
  %".11" = call i32 (i8*, ...) @"printf"(i8* %".10", i32 %".7")
  %".12" = load i32, i32* %".2"
  %".13" = call i32 @"not_main"(i32 %".12")
  store i32 %".13", i32* %".2"
  %".15" = load i32, i32* %".2"
  %".16" = icmp slt i32 %".15", 52
  br i1 %".16", label %"while_entry_1", label %"while_otherwise_1"
while_otherwise_1:
  %".18" = load i32, i32* %".2"
  ret i32 %".18"
}

@"__str_2" = internal constant [9 x i8] c"a = %i\0a\00\00"
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
  %".13" = load i32, i32* %".4"
  %".14" = icmp slt i32 %".13", 252
  br i1 %".14", label %"while_entry_3", label %"while_otherwise_3"
while_entry_3:
  %".16" = load i32, i32* %".4"
  %".17" = add i32 %".16", 52
  store i32 %".17", i32* %".4"
  %".19" = load i32, i32* %".4"
  %".20" = icmp slt i32 %".19", 252
  br i1 %".20", label %"while_entry_3", label %"while_otherwise_3"
while_otherwise_3:
  %".22" = load float, float* %".2"
  ret float %".22"
}
