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
  %".4" = alloca i32
  store i32 0, i32* %".4"
  br label %"for_entr_1"
for_entr_1:
  %".7" = load i32, i32* %".4"
  %".8" = icmp eq i32 %".7", 52
  br i1 %".8", label %"for_entr_1.if", label %"for_entr_1.endif"
for_other_2:
  %".25" = load i32, i32* %".2"
  ret i32 %".25"
for_entr_1.if:
  br label %"for_other_2"
for_entr_1.endif:
  %".11" = load i32, i32* %".4"
  %".12" = alloca [15 x i8]*
  store [15 x i8]* @"__str_3", [15 x i8]** %".12"
  %".14" = bitcast [15 x i8]* @"__str_3" to i8*
  %".15" = call i32 (i8*, ...) @"printf"(i8* %".14", i32 %".11")
  %".16" = load i32, i32* %".2"
  %".17" = add i32 %".16", 1
  store i32 %".17", i32* %".2"
  %".19" = load i32, i32* %".4"
  %".20" = call i32 @"not_main"(i32 %".19")
  store i32 %".20", i32* %".4"
  %".22" = load i32, i32* %".4"
  %".23" = icmp slt i32 %".22", 10
  br i1 %".23", label %"for_entr_1", label %"for_other_2"
}

@"__str_3" = internal constant [15 x i8] c"current i %i\0a\00\00"
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
  br i1 %".14", label %"while_entry_4", label %"while_otherwise_4"
while_entry_4:
  %".16" = load i32, i32* %".4"
  %".17" = add i32 %".16", 52
  store i32 %".17", i32* %".4"
  %".19" = load i32, i32* %".4"
  %".20" = icmp slt i32 %".19", 252
  br i1 %".20", label %"while_entry_4", label %"while_otherwise_4"
while_otherwise_4:
  %".22" = load float, float* %".2"
  ret float %".22"
}
