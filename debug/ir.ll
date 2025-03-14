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
  %".9" = load i32, i32* %".4"
  store i32 27, i32* %".4"
  br label %"main52_entry.endif"
main52_entry.else:
  %".12" = load i32, i32* %".4"
  store i32 143, i32* %".4"
  br label %"main52_entry.endif"
main52_entry.endif:
  %".15" = load i32, i32* %".4"
  %".16" = icmp slt i32 %".15", 252
  br i1 %".16", label %"while_entry_1", label %"while_otherwise_1"
while_entry_1:
  %".18" = load i32, i32* %".4"
  %".19" = add i32 %".18", 52
  %".20" = load i32, i32* %".4"
  store i32 %".19", i32* %".4"
  %".22" = load i32, i32* %".4"
  %".23" = icmp slt i32 %".22", 252
  br i1 %".23", label %"while_entry_1", label %"while_otherwise_1"
while_otherwise_1:
  %".25" = alloca i32
  store i32 0, i32* %".25"
  br label %"for_entr_2"
for_entr_2:
  %".28" = load i32, i32* %".25"
  %".29" = icmp eq i32 %".28", 6
  br i1 %".29", label %"for_entr_2.if", label %"for_entr_2.endif"
for_other_3:
  %".43" = load float, float* %".2"
  ret float %".43"
for_entr_2.if:
  br label %"for_other_3"
for_entr_2.endif:
  %".32" = load float, float* %".2"
  %".33" = fadd float %".32", 0x3fb99999a0000000
  %".34" = load float, float* %".2"
  store float %".33", float* %".2"
  %".36" = load i32, i32* %".25"
  %".37" = add i32 %".36", 1
  %".38" = load i32, i32* %".25"
  store i32 %".37", i32* %".25"
  %".40" = load i32, i32* %".25"
  %".41" = icmp slt i32 %".40", 10
  br i1 %".41", label %"for_entr_2", label %"for_other_3"
}

define i32 @"main"()
{
main_entry:
  %".2" = alloca i32
  store i32 1, i32* %".2"
  %".4" = call float @"main52"()
  %".5" = alloca float
  store float %".4", float* %".5"
  %".7" = alloca [11 x i8]*
  store [11 x i8]* @"__str_4", [11 x i8]** %".7"
  %".9" = bitcast [11 x i8]* @"__str_4" to i8*
  %".10" = call i32 (i8*, ...) @"printf"(i8* %".9", float 0x400c000000000000, i32 3)
  %".11" = mul i32 5, -1
  %".12" = alloca i32
  store i32 %".11", i32* %".12"
  br label %"for_entr_5"
for_entr_5:
  %".15" = load i32, i32* %".12"
  %".16" = icmp eq i32 %".15", 52
  br i1 %".16", label %"for_entr_5.if", label %"for_entr_5.endif"
for_other_6:
  %".41" = load i32, i32* %".2"
  ret i32 %".41"
for_entr_5.if:
  br label %"for_other_6"
for_entr_5.endif:
  %".19" = xor i1 0, -1
  br i1 %".19", label %"for_entr_5.endif.if", label %"for_entr_5.endif.endif"
for_entr_5.endif.if:
  %".21" = alloca [14 x i8]*
  store [14 x i8]* @"__str_7", [14 x i8]** %".21"
  %".23" = bitcast [14 x i8]* @"__str_7" to i8*
  %".24" = call i32 (i8*, ...) @"printf"(i8* %".23")
  br label %"for_entr_5.endif.endif"
for_entr_5.endif.endif:
  %".26" = load i32, i32* %".12"
  %".27" = alloca [15 x i8]*
  store [15 x i8]* @"__str_8", [15 x i8]** %".27"
  %".29" = bitcast [15 x i8]* @"__str_8" to i8*
  %".30" = call i32 (i8*, ...) @"printf"(i8* %".29", i32 %".26")
  %".31" = load i32, i32* %".2"
  %".32" = mul i32 %".31", 2
  store i32 %".32", i32* %".2"
  %".34" = load i32, i32* %".12"
  %".35" = sub i32 %".34", 1
  store i32 %".35", i32* %".12"
  %".37" = load i32, i32* %".12"
  %".38" = mul i32 10, -1
  %".39" = icmp sgt i32 %".37", %".38"
  br i1 %".39", label %"for_entr_5", label %"for_other_6"
}

@"__str_4" = internal constant [11 x i8] c"%.2f %i \0a\00\00"
@"__str_7" = internal constant [14 x i8] c"what ta heil \00"
@"__str_8" = internal constant [15 x i8] c"current i %i\0a\00\00"