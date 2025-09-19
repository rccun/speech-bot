import sys

print("Введите многострочный текст (Ctrl+D/Ctrl+Z для завершения):")
multiline_input = sys.stdin.read()
print(multiline_input.split('\n'))

