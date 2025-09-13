from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.mysql_operator import MySqlOperator
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.sensors.sql_sensor import SqlSensor
from airflow.utils.dates import days_ago
import random
import time

# Конфігурація DAG
default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Створення DAG
dag = DAG(
    'olympic_medal_processing',
    default_args=default_args,
    description='DAG для обробки олімпійських медалей',
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['olympic', 'medals', 'mysql'],
)

# Завдання 1: Створення таблиці
create_table_task = MySqlOperator(
    task_id='create_table',
    mysql_conn_id='mysql_default',
    sql="""
    CREATE TABLE IF NOT EXISTS medal_counts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        medal_type VARCHAR(10) NOT NULL,
        count INT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    dag=dag,
)

# Завдання 2: Випадковий вибір медалі
def pick_medal_function():
    """Функція для випадкового вибору типу медалі"""
    medals = ['Bronze', 'Silver', 'Gold']
    chosen_medal = random.choice(medals)
    print(f"Обрано медаль: {chosen_medal}")
    return f"calc_{chosen_medal}"

pick_medal_task = BranchPythonOperator(
    task_id='pick_medal_task',
    python_callable=pick_medal_function,
    dag=dag,
)

# Завдання 3: Розгалуження - три завдання для підрахунку медалей

# Завдання 3.1: Підрахунок Bronze медалей
calc_bronze_task = MySqlOperator(
    task_id='calc_Bronze',
    mysql_conn_id='mysql_default',
    sql="""
    INSERT INTO medal_counts (medal_type, count, created_at)
    SELECT 'Bronze', COUNT(*), NOW()
    FROM olympic_dataset.athlete_event_results
    WHERE medal = 'Bronze';
    """,
    dag=dag,
)

# Завдання 3.2: Підрахунок Silver медалей
calc_silver_task = MySqlOperator(
    task_id='calc_Silver',
    mysql_conn_id='mysql_default',
    sql="""
    INSERT INTO medal_counts (medal_type, count, created_at)
    SELECT 'Silver', COUNT(*), NOW()
    FROM olympic_dataset.athlete_event_results
    WHERE medal = 'Silver';
    """,
    dag=dag,
)

# Завдання 3.3: Підрахунок Gold медалей
calc_gold_task = MySqlOperator(
    task_id='calc_Gold',
    mysql_conn_id='mysql_default',
    sql="""
    INSERT INTO medal_counts (medal_type, count, created_at)
    SELECT 'Gold', COUNT(*), NOW()
    FROM olympic_dataset.athlete_event_results
    WHERE medal = 'Gold';
    """,
    dag=dag,
)

# Завдання 4: Затримка виконання
def generate_delay():
    """Функція для створення затримки"""
    print("Початок затримки на 35 секунд...")
    time.sleep(35)  # 35 секунд затримки для тестування сенсора
    print("Затримка завершена")

delay_task = PythonOperator(
    task_id='generate_delay',
    python_callable=generate_delay,
    trigger_rule='one_success',  # Виконується, якщо хоча б одне з попередніх завдань успішне
    dag=dag,
)

# Завдання 5: Сенсор для перевірки свіжості запису
check_freshness_sensor = SqlSensor(
    task_id='check_for_correctness',
    conn_id='mysql_default',
    sql="""
    SELECT 1
    FROM medal_counts
    WHERE created_at >= NOW() - INTERVAL 30 SECOND
    ORDER BY created_at DESC
    LIMIT 1;
    """,
    timeout=60,
    poke_interval=10,
    mode='poke',
    dag=dag,
)

# Встановлення залежностей між завданнями
create_table_task >> pick_medal_task

# Розгалуження від pick_medal_task до трьох завдань підрахунку
pick_medal_task >> [calc_bronze_task, calc_silver_task, calc_gold_task]

# Всі три завдання підрахунку ведуть до затримки
[calc_bronze_task, calc_silver_task, calc_gold_task] >> delay_task

# Затримка веде до сенсора
delay_task >> check_freshness_sensor