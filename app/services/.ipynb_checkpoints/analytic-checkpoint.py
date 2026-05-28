import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

DATABASE_URL = "postgresql://admin:supersecretpassword@localhost:5432/iot_telemetry"

engine = create_engine(DATABASE_URL)

query = "SELECT * FROM telemetry_data ORDER BY timestamp ASC;"

df = pd.read_sql(query,engine)


#clear dataset
df = df[df['timestamp'] >= '2026-05-24']


print(f'кількість даних завантаженно: {len(df)}')
print(df.head())
print("Загальний опис числових даних (describe):")
print(df.describe())

critical_df = df[df['is_critical'] == True]
# print(f"DF where temperature is critical {critical_df}")

highest_temp = df[df['temperature'] > 25]
# print(f"DF where temperature more 25 {highest_temp}")

mean_humidity_critical = critical_df['humidity'].mean()
# print(f"AVG humidity when temperature is critical {mean_humidity_critical}")
print("---------------------------------")
#Vectorization
mean_temp = df['temperature'].mean()
df['temperature_deviation'] = df['temperature'] - mean_temp
print(df['temperature_deviation'].head())
#Dispersion
df['squared_deviation'] = df['temperature_deviation'] ** 2
manual_varience = df['squared_deviation'].mean()
print("--- Перші 5 рядків квадрату відхилень")
print(df[['temperature', 'temperature_deviation', 'squared_deviation']].head())
#standart deviation
manual_std = manual_varience ** 0.5
print(f'стандартне відхилення {manual_std}')

plt.figure(figsize=(12, 6))
plt.plot(df['timestamp'], df['temperature'], label='Сира температура (Шум DHT11)', color='blue', alpha=0.5)

# Малюємо центральну лінію (скаляр - середнє значення)
plt.axhline(mean_temp, color='red', linestyle='-', linewidth=2, label=f'Середнє: {mean_temp:.2f} °C')

# 3. Малюємо межі твого стандартного відхилення (коридор шуму)
plt.axhline(mean_temp + manual_std, color='green', linestyle='--', linewidth=2, label=f'+1 Відхилення ({mean_temp + manual_std:.2f} °C)')
plt.axhline(mean_temp - manual_std, color='green', linestyle='--', linewidth=2, label=f'-1 Відхилення ({mean_temp - manual_std:.2f} °C)')

plt.legend()
plt.title('Візуалізація математики: Середнє значення та Стандартне відхилення')
plt.grid(True)
plt.show()

        # Pandas автоматично порівняє температуру з вологістю
corr_matrix = df[['temperature', 'humidity']].corr(method='pearson')
print("Матриця кореляцій Пірсона:")
print(corr_matrix)

#Будуємо теплову карту через Matplotlib
plt.figure(figsize=(8, 6))
#Відображаємо матрицю як зображення (теплова карта)
cax = plt.matshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)

# Додаємо колірну шкалу (легенду) збоку
plt.colorbar(cax)
# Підписуємо осі
plt.xticks(range(len(corr_matrix.columns)), corr_matrix.columns, rotation=45)
plt.yticks(range(len(corr_matrix.columns)), corr_matrix.columns)
plt.title('Теплова карта кореляції Пірсона (ESP32 Telemetry)', pad=20)
spearman_corr = df[['temperature', 'humidity']].corr(method='spearman')
print("\n--- Кореляція Спірмена (Монотонна, стабільна до викидів) ---")
print(spearman_corr)

plt.show()

plt.figure(figsize=(10,6))
plt.scatter(df['temperature'], df['humidity'], color='purple', alpha=0.05)
plt.title('Залежність вологості від температури (Scatter Plot)', fontsize=14)
plt.xlabel('Температура (°C)', fontsize=12)
plt.ylabel('Вологість (%)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.show()