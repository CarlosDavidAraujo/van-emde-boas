PY = py
INPUT = entrada.txt
OUTPUT = saida.txt

.PHONY: build run output test-output test-compare test

build:
	@echo "No build step required for Python"

run:
	$(PY) main.py $(INPUT)

output:
	$(PY) main.py $(INPUT) > $(OUTPUT)

test-output:
	$(PY) main.py test/1.txt > test/1_saida.txt
	$(PY) main.py test/2.txt > test/2_saida.txt
	$(PY) main.py test/3.txt > test/3_saida.txt
	$(PY) main.py test/4.txt > test/4_saida.txt
	$(PY) main.py test/5.txt > test/5_saida.txt
	$(PY) main.py test/6.txt > test/6_saida.txt
	$(PY) main.py test/7.txt > test/7_saida.txt

test-compare: test-output
	fc test\1_esperada.txt test\1_saida.txt
	fc test\2_esperada.txt test\2_saida.txt
	fc test\3_esperada.txt test\3_saida.txt
	fc test\4_esperada.txt test\4_saida.txt
	fc test\5_esperada.txt test\5_saida.txt
	fc test\6_esperada.txt test\6_saida.txt
	fc test\7_esperada.txt test\7_saida.txt

test: test-compare
