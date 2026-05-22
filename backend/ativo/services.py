from datetime import timedelta
import holidays # Biblioteca para lidar com feriados, garantindo que as datas calculadas sejam dias úteis.

feriados_br = holidays.Brazil() # Cria um objeto que contém os feriados do Brasil, permitindo verificar se uma data é um feriado ou não.

# Função para ajustar uma data para o próximo dia útil, considerando fins de semana e feriados.
def ajustar_para_dia_util(data):
    while (data.weekday() >= 5 or data in feriados_br ): # Verifica se a data é um sábado (5) ou domingo (6) ou um feriado. Se for, ajusta para o próximo dia.
        data += timedelta(days=1)

    return data

# Função para calcular a próxima data de manutenção preventiva, adicionando a periodicidade em dias à data da última manutenção e ajustando para o próximo dia útil.
def calcular_proxima_preventiva(dt_ultima_preventiva, periodicidade_dias):

    data_calculada = (dt_ultima_preventiva + timedelta(days=periodicidade_dias)) # Calcula a data da próxima manutenção preventiva somando a periodicidade em dias à data da última manutenção.

    return ajustar_para_dia_util(data_calculada)