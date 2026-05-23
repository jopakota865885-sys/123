# Инструкция по сборке CardCatalog.exe

Поскольку текущая среда работает на Linux, прямая компиляция в .exe невозможна.
Вместо этого настроена автоматическая сборка через GitHub Actions.

## Способ 1: Автоматическая сборка через GitHub (Рекомендуется)

1. **Загрузите код на GitHub:**
   ```bash
   git add .
   git commit -m "Add build configuration for Windows EXE"
   git push origin main
   ```

2. **Запустите сборку:**
   - Зайдите в репозиторий на GitHub
   - Перейдите во вкладку **Actions**
   - Выберите workflow **Build Windows EXE**
   - Нажмите **Run workflow** (или сборка запустится автоматически при пуше)

3. **Скачайте результат:**
   - После завершения сборки (зеленая галочка)
   - В разделе **Artifacts** скачайте файл `CardCatalog-Windows.zip`
   - Внутри будет готовый `CardCatalog.exe`

## Способ 2: Локальная сборка на Windows

Если у вас есть доступ к Windows-машине:

1. Скопируйте файлы проекта на Windows:
   - `main.py` (исходный код)
   - `build_exe.py` (скрипт сборки)
   - `requirements.txt` (зависимости, если есть)

2. Установите Python 3.8+ и выполните:
   ```cmd
   pip install pyinstaller
   python build_exe.py
   ```

3. Готовый `.exe` файл появится в папке `dist\CardCatalog.exe`

## Файлы для сборки

- `build_exe.py` — скрипт настройки PyInstaller
- `.github/workflows/build_exe.yml` — конфигурация GitHub Actions
