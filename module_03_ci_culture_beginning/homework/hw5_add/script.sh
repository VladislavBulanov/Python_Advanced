# Выполнение статического анализа с помощью pylint:
pylint -r json decrypt.py > report.json
return_code=$?

# Вывод отчёта и метрик качества кода:
pylint-json2html -f jsonextended -o report.html report.json
pylint --exit-zero decrypt.py

# Запуск юнит-тестов:
python3 test_decrypt.py
unittest_result=$?

# Проверка кодов возврата:
if [ $return_code -eq 0 ] && [ $unittest_result -eq 0 ]; then
  echo 'OK'
else
  echo 'Имеются ошибки'
fi
