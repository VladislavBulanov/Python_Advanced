# Выполнение статического анализа с помощью pylint:
pylint --output-format=json -r y decrypt.py > report.json
return_code=$?

# Вывод отчёта и метрик качества кода:
pylint --exit-zero decrypt.py

# Запуск юнит-тестов:
python3 ./test_decrypt.py
unittest_result=$?

# Проверка кодов возврата:
if [ $return_code -eq 0 ]; then
  echo "Program: OK"
else
  echo "Program: something's wrong"
fi

if [ $unittest_result -eq 0 ]; then
  echo "Tests: OK"
else
  echo "Tests: something's wrong"
fi
