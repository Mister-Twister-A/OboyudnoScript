; ModuleID = "main"
target triple = "x86_64-pc-linux-gnu"
target datalayout = ""

define i32 @"main"()
{
main_entry:
  %".2" = srem i32 5, 3
  ret i32 52
}
