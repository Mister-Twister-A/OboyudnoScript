; ModuleID = "main"
target triple = "x86_64-pc-linux-gnu"
target datalayout = ""

define i32 @"main"()
{
main_entry:
  %".2" = add i32 5, 5
  %".3" = mul i32 %".2", 10
  ret i32 52
}
