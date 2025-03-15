; ModuleID = "main"
target triple = "x86_64-pc-linux-gnu"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

@"true" = constant i1 1
@"false" = constant i1 0
define i32 @"add"(i32 %".1", i32 %".2")
{
add_entry:
  %".4" = alloca i32
  store i32 %".1", i32* %".4"
  %".6" = alloca i32
  store i32 %".2", i32* %".6"
  %".8" = load i32, i32* %".4"
  %".9" = load i32, i32* %".6"
  %".10" = add i32 %".8", %".9"
  ret i32 %".10"
}

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
  %".72" = load i32, i32* %".2"
  ret i32 %".72"
for_entr_5.if:
  br label %"for_other_6"
for_entr_5.endif:
  %".19" = load i32, i32* %".12"
  %".20" = mul i32 6, -1
  %".21" = icmp eq i32 %".19", %".20"
  br i1 %".21", label %"for_entr_5.endif.if", label %"for_entr_5.endif.endif"
for_entr_5.endif.if:
  %".23" = alloca [13 x i8]*
  store [13 x i8]* @"__str_7", [13 x i8]** %".23"
  %".25" = bitcast [13 x i8]* @"__str_7" to i8*
  %".26" = call i32 (i8*, ...) @"printf"(i8* %".25")
  %".27" = load i32, i32* %".12"
  %".28" = mul i32 10, -1
  %".29" = icmp sgt i32 %".27", %".28"
  %".30" = load i32, i32* %".12"
  %".31" = sub i32 %".30", 1
  store i32 %".31", i32* %".12"
  br i1 %".29", label %"for_entr_5", label %"for_other_6"
for_entr_5.endif.endif:
  %".34" = load i32, i32* %".12"
  %".35" = mul i32 7, -1
  %".36" = icmp eq i32 %".34", %".35"
  br i1 %".36", label %"for_entr_5.endif.endif.if", label %"for_entr_5.endif.endif.endif"
for_entr_5.endif.endif.if:
  %".38" = alloca [15 x i8]*
  store [15 x i8]* @"__str_8", [15 x i8]** %".38"
  %".40" = bitcast [15 x i8]* @"__str_8" to i8*
  %".41" = call i32 (i8*, ...) @"printf"(i8* %".40")
  %".42" = load i32, i32* %".12"
  %".43" = mul i32 10, -1
  %".44" = icmp sgt i32 %".42", %".43"
  %".45" = load i32, i32* %".12"
  %".46" = sub i32 %".45", 1
  store i32 %".46", i32* %".12"
  br i1 %".44", label %"for_entr_5", label %"for_other_6"
for_entr_5.endif.endif.endif:
  %".49" = xor i1 0, -1
  br i1 %".49", label %"for_entr_5.endif.endif.endif.if", label %"for_entr_5.endif.endif.endif.endif"
for_entr_5.endif.endif.endif.if:
  %".51" = alloca [14 x i8]*
  store [14 x i8]* @"__str_9", [14 x i8]** %".51"
  %".53" = bitcast [14 x i8]* @"__str_9" to i8*
  %".54" = call i32 (i8*, ...) @"printf"(i8* %".53")
  br label %"for_entr_5.endif.endif.endif.endif"
for_entr_5.endif.endif.endif.endif:
  %".56" = load i32, i32* %".12"
  %".57" = alloca [15 x i8]*
  store [15 x i8]* @"__str_10", [15 x i8]** %".57"
  %".59" = bitcast [15 x i8]* @"__str_10" to i8*
  %".60" = call i32 (i8*, ...) @"printf"(i8* %".59", i32 %".56")
  %".61" = load i32, i32* %".2"
  %".62" = call i32 @"add"(i32 %".61", i32 1)
  %".63" = load i32, i32* %".2"
  store i32 %".62", i32* %".2"
  %".65" = load i32, i32* %".12"
  %".66" = sub i32 %".65", 1
  store i32 %".66", i32* %".12"
  %".68" = load i32, i32* %".12"
  %".69" = mul i32 10, -1
  %".70" = icmp sgt i32 %".68", %".69"
  br i1 %".70", label %"for_entr_5", label %"for_other_6"
}

@"__str_4" = internal constant [11 x i8] c"%.2f %i \0a\00\00"
@"__str_7" = internal constant [13 x i8] c"continued \0a\00\00"
@"__str_8" = internal constant [15 x i8] c"continued 2 \0a\00\00"
@"__str_9" = internal constant [14 x i8] c"what ta heil \00"
@"__str_10" = internal constant [15 x i8] c"current i %i\0a\00\00"